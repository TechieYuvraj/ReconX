import argparse
from utils.robots import parse_robots_txt
from utils.export import export_urls
from integrations.dirsearch_runner import run_dirsearch
from integrations.sublist3r_runner import run_sublist3r
from utils.screenshotter import take_screenshot
from core.parallel_crawler import ParallelCrawler
import requests
from utils.forms import scan_for_forms
from utils.keywords import scan_for_keywords
from utils.links import extract_links
from utils.report_generator import ReportGenerator
from urllib.parse import urlparse


def run_recon(
    url,
    keyword_scan=False,
    form_detection=False,
    export_urls_flag=False,
    respect_nofollow=False,
    parse_robots=False,
    run_dirsearch_flag=False,
    run_sublist3r_flag=False,
    capture_screenshots=False,
    generate_pdf_report=False,
    threads=10
):
    if not url:
        print("[ERROR] No target URL provided.")
        return

    print(f"[+] Starting ReconX on {url}")
    print(f"[+] Threads: {threads}")
    
    disallowed_paths = parse_robots_txt(url) if parse_robots else []
    session = requests.Session()

    crawler = ParallelCrawler(
        max_workers=threads,
        screenshot_callback=take_screenshot if capture_screenshots else None,
        form_scanner=scan_for_forms if form_detection else None,
        keyword_scanner=scan_for_keywords if keyword_scan else None,
        respect_nofollow=respect_nofollow
    )

    visited = crawler.start_crawling(url, session, extract_links)

    if capture_screenshots:
        print("[*] Capturing screenshots...")
        for link in visited:
            take_screenshot(link)

    if export_urls_flag:
        print(f"[DEBUG] Number of URLs to export: {len(visited)}")
        print(f"[DEBUG] Sample URLs: {list(visited)[:5]}")
        export_urls(visited)

    if run_dirsearch_flag:
        run_dirsearch(url)

    if run_sublist3r_flag:
        domain = urlparse(url).netloc
        run_sublist3r(domain)

    if generate_pdf_report:
        settings = {
            "Keyword Scanning": keyword_scan,
            "Form Detection": form_detection,
            "Export URLs": export_urls_flag,
            "Respect Nofollow": respect_nofollow,
            "Parse robots.txt": parse_robots,
            "Dirsearch": run_dirsearch_flag,
            "Sublist3r": run_sublist3r_flag,
            "Screenshots": capture_screenshots,
            "Parallel Crawling": True
        }

        report = ReportGenerator(
            target_url=url,
            visited_urls=visited,
            scan_settings=settings,
            screenshots=[],  # Optional: Add screenshot paths if tracked
        )
        report.generate_pdf()


def main():
    parser = argparse.ArgumentParser(description="ReconX - Ethical Hacking Web Crawler")
    parser.add_argument("-u", "--url", required=True, help="Target URL to start crawling")
    parser.add_argument("--keywords", action="store_true", help="Enable keyword scanning")
    parser.add_argument("--forms", action="store_true", help="Enable form detection")
    parser.add_argument("--export", action="store_true", help="Export visited URLs to a file")
    parser.add_argument("--nofollow", action="store_true", help="Respect rel='nofollow' links")
    parser.add_argument("--robots", action="store_true", help="Parse and respect robots.txt")
    parser.add_argument("--dirsearch", action="store_true", help="Run dirsearch on target")
    parser.add_argument("--sublist3r", action="store_true", help="Run sublist3r on target domain")
    parser.add_argument("--screenshots", action="store_true", help="Enable screenshot capture")
    parser.add_argument("--report", action="store_true", help="Generate PDF report")
    parser.add_argument("--threads", type=int, default=10, help="Number of threads for parallel crawling (default=10)")

    args = parser.parse_args()

    run_recon(
        url=args.url,
        keyword_scan=args.keywords,
        form_detection=args.forms,
        export_urls_flag=args.export,
        respect_nofollow=args.nofollow,
        parse_robots=args.robots,
        run_dirsearch_flag=args.dirsearch,
        run_sublist3r_flag=args.sublist3r,
        capture_screenshots=args.screenshots,
        generate_pdf_report=args.report,
        threads=args.threads
    )


if __name__ == "__main__":
    main()
