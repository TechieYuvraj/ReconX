import argparse
from utils.robots import parse_robots_txt
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
    respect_nofollow=False,
    parse_robots=False,
    run_dirsearch_flag=False,
    run_sublist3r_flag=False,
    capture_screenshots=False,
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
    print(f"[DEBUG] Type of visited: {type(visited)}")
    print(f"[DEBUG] Sample of visited: {list(visited)[:5] if hasattr(visited, '__iter__') else visited}")

    if capture_screenshots:
        print("[*] Capturing screenshots...")
        for link in visited:
            take_screenshot(link)

    if run_dirsearch_flag:
        run_dirsearch(url)

    if run_sublist3r_flag:
        domain = urlparse(url).netloc
        run_sublist3r(domain)

    # Always generate PDF report
    settings = {
        "keywords": keyword_scan,
        "form_detection": form_detection,
        "respect_nofollow": respect_nofollow,
        "parse_robots": parse_robots,
        "dirsearch": run_dirsearch_flag,
        "subdomains": run_sublist3r_flag,
        "screenshots": capture_screenshots,
        "parallel_crawling": True
    }

    # Capture detailed results
    found_keywords = getattr(crawler, 'found_keywords', [])
    found_forms = getattr(crawler, 'found_forms', [])
    screenshots_list = []  # You may need to track screenshot paths if available

    dirsearch_results = None
    if run_dirsearch_flag:
        dirsearch_results = run_dirsearch(url)

    sublist3r_results = None
    if run_sublist3r_flag:
        domain = urlparse(url).netloc
        sublist3r_results = run_sublist3r(domain)

    report = ReportGenerator(
        target_url=url,
        visited_urls=visited["visited_urls"],
        scan_settings=settings,
        screenshots=screenshots_list,
        found_keywords=found_keywords,
        found_forms=found_forms,
        dirsearch_results=dirsearch_results,
        sublist3r_results=sublist3r_results
    )
    pdf_path = report.generate_pdf()
    return pdf_path


def main():
    parser = argparse.ArgumentParser(description="ReconX - Ethical Hacking Web Crawler")
    parser.add_argument("-u", "--url", required=True, help="Target URL to start crawling")
    parser.add_argument("--keywords", action="store_true", help="Enable keyword scanning")
    parser.add_argument("--forms", action="store_true", help="Enable form detection")
    parser.add_argument("--nofollow", action="store_true", help="Respect rel='nofollow' links")
    parser.add_argument("--robots", action="store_true", help="Parse and respect robots.txt")
    parser.add_argument("--dirsearch", action="store_true", help="Run dirsearch on target")
    parser.add_argument("--sublist3r", action="store_true", help="Run sublist3r on target domain")
    parser.add_argument("--screenshots", action="store_true", help="Enable screenshot capture")
    parser.add_argument("--threads", type=int, default=10, help="Number of threads for parallel crawling (default=10)")

    args = parser.parse_args()

    run_recon(
        url=args.url,
        keyword_scan=args.keywords,
        form_detection=args.forms,
        respect_nofollow=args.nofollow,
        parse_robots=args.robots,
        run_dirsearch_flag=args.dirsearch,
        run_sublist3r_flag=args.sublist3r,
        capture_screenshots=args.screenshots,
        threads=args.threads
    )


if __name__ == "__main__":
    main()
