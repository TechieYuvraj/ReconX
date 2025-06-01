KEYWORDS = ["login", "admin", "dashboard", "signup", "user", "password"]

# def check_keywords(soup, url):
#     text = soup.get_text().lower()
#     for keyword in KEYWORDS:
#         if keyword in text:
#             print(f"[!] Keyword '{keyword}' found at {url}")


def scan_for_keywords(url, html):
    for word in KEYWORDS:
        if word.lower() in html.lower():
            print(f"[!] Keyword '{word}' found on {url}")
