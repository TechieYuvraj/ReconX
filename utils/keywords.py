KEYWORDS = ["login", "admin", "dashboard", "signup", "user", "password"]

def scan_for_keywords(url, html):
    for word in KEYWORDS:
        if word.lower() in html.lower():
            print(f"[!] Keyword '{word}' found on {url}")
