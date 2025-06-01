def scan_for_forms(url, html):
    if "<form" in html.lower():
        print(f"[+] Form found on: {url}")
