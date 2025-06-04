from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

lock = threading.Lock()

class ParallelCrawler:
    def __init__(self, max_workers=10, screenshot_callback=None, form_scanner=None,
                 keyword_scanner=None, visited_urls=None, respect_nofollow=False):
        self.max_workers = max_workers
        self.visited_urls = visited_urls or set()
        self.screenshot_callback = screenshot_callback
        self.form_scanner = form_scanner
        self.keyword_scanner = keyword_scanner
        self.respect_nofollow = respect_nofollow
        self.found_keywords = set()
        self.found_forms = []
        self.screenshots = []

    def crawl_url(self, url, session, extract_links_fn):
        try:
            print(f"[+] Crawling: {url}")
            response = session.get(url, timeout=10, headers={"User-Agent": "ReconX-Bot"})
            html = response.text

            # Optional: Keyword scanner
            if self.keyword_scanner:
                keywords = self.keyword_scanner(url, html)
                if keywords:
                    self.found_keywords.update(keywords)

            # Optional: Form scanner
            if self.form_scanner:
                forms = self.form_scanner(url, html)
                if forms:
                    self.found_forms.extend(forms)

            # Optional: Screenshot
            if self.screenshot_callback:
                screenshot_path = self.screenshot_callback(url)
                if screenshot_path:
                    self.screenshots.append(screenshot_path)

            # Extract and return links
            return extract_links_fn(html, url)

        except Exception as e:
            print(f"[!] Error crawling {url}: {e}")
            return []

    def start_crawling(self, start_url, session, extract_links_fn, max_depth=2):
        to_visit = [(start_url, 0)]
        self.visited_urls.add(start_url)

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            while to_visit:
                futures = {}
                for url, depth in to_visit:
                    if depth >= max_depth:
                        continue
                    futures[executor.submit(self.crawl_url, url, session, extract_links_fn)] = (url, depth)

                to_visit = []

                for future in as_completed(futures):
                    url, depth = futures[future]
                    try:
                        new_links = future.result()
                        with lock:
                            for link in new_links:
                                if link not in self.visited_urls:
                                    self.visited_urls.add(link)
                                    to_visit.append((link, depth + 1))
                    except Exception as e:
                        print(f"[!] Error processing result from {url}: {e}")

        return {
            "visited_urls": self.visited_urls,
            "found_keywords": list(self.found_keywords),
            "found_forms": self.found_forms,
            "screenshots": self.screenshots
        }
