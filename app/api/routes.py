from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from integrations.dirsearch_runner import run_dirsearch
from integrations.sublist3r_runner import run_sublist3r
from urllib.parse import urlparse
from app.api.schemas import CrawlOptions
from core.parallel_crawler import ParallelCrawler
from utils.forms import scan_for_forms
from utils.keywords import scan_for_keywords
from utils.screenshotter import take_screenshot
from utils.links import extract_links
from utils.report_generator import ReportGenerator
import requests
from fastapi.responses import FileResponse
import os
from uuid import uuid4
from fastapi import HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()

class URLRequest(BaseModel):
    url: HttpUrl

@router.get("/")
def root():
    return {"message": "ReconX API is live!"}

@router.get("/ping")
def ping():
    return {"status": "ok"}

@router.post("/crawl")
def crawl_site(options: CrawlOptions):
    try:
        session = requests.Session()

        crawler = ParallelCrawler(
            max_workers=10,
            screenshot_callback=take_screenshot if options.enable_screenshots else None,
            form_scanner=scan_for_forms if options.enable_forms else None,
            keyword_scanner=scan_for_keywords if options.enable_keywords else None,
            respect_nofollow=False
        )

        crawl_results = crawler.start_crawling(options.url, session, extract_links)

        dirsearch_results = None
        if options.enable_dirsearch:
            dirsearch_results = run_dirsearch(options.url)

        sublist3r_results = None
        if options.enable_subdomains:
            domain = urlparse(str(options.url)).netloc
            sublist3r_results = run_sublist3r(domain)

        scan_settings = {
            "keywords": options.enable_keywords,
            "form_detection": options.enable_forms,
            "dirsearch": options.enable_dirsearch,
            "subdomains": options.enable_subdomains,
            "screenshots": options.enable_screenshots
        }

        if options.enable_pdf_report:
            report = ReportGenerator(
                target_url=options.url,
                visited_urls=crawl_results["visited_urls"],
                scan_settings=scan_settings,
                screenshots=crawl_results.get("screenshots", []),
                found_keywords=crawl_results.get("found_keywords", []),
                found_forms=crawl_results.get("found_forms", []),
                dirsearch_results=dirsearch_results,
                sublist3r_results=sublist3r_results
            )
            report_path = report.generate_pdf()

            if not os.path.isfile(report_path):
                raise HTTPException(status_code=500, detail="Report generation failed.")

            # Return the URL to download the PDF
            return {
                "message": "Crawl completed",
                "total_urls": len(crawl_results["visited_urls"]),
                "report_generated": True,
                "report_url": f"/reports/{os.path.basename(report_path)}",
                "dirsearch_results": dirsearch_results,
                "sublist3r_results": sublist3r_results
            }

        return {
            "message": "Crawl completed",
            "total_urls": len(crawl_results["visited_urls"]),
            "report_generated": False,
            "dirsearch_results": dirsearch_results,
            "sublist3r_results": sublist3r_results
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.get("/reports/{filename}")
def download_report(filename: str):
    path = os.path.join("reports", filename)
    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path, media_type="application/pdf", filename=filename)

@router.post("/dirsearch")
def dirsearch_route(request: URLRequest):
    try:
        result = run_dirsearch(request.url)
        return {"success": True, "output": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sublist3r")
def sublist3r_route(request: URLRequest):
    try:
        domain = urlparse(request.url).netloc
        result = run_sublist3r(domain)
        return {"success": True, "output": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
