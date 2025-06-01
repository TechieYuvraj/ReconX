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
    session = requests.Session()

    crawler = ParallelCrawler(
        max_workers=10,
        screenshot_callback=take_screenshot if options.enable_screenshots else None,
        form_scanner=scan_for_forms if options.enable_forms else None,
        keyword_scanner=scan_for_keywords if options.enable_keywords else None,
        respect_nofollow=False
    )

    visited_urls = crawler.start_crawling(options.url, session, extract_links)

    report_path = None
    if options.enable_pdf_report:
        report = ReportGenerator(
            target_url=options.url,
            visited_urls=visited_urls,
            scan_settings={
                "Keywords": options.enable_keywords,
                "Forms": options.enable_forms,
                "Screenshots": options.enable_screenshots
            },
            screenshots=[]  # Can update with screenshot paths later
        )
        report_path = report.generate_pdf()

    return {
        "message": "Crawl completed",
        "total_urls": len(visited_urls),
        "report_generated": bool(report_path),
        "report_path": report_path
    }

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
