from bs4 import BeautifulSoup

def scan_for_forms(url, html):
    forms = []
    try:
        soup = BeautifulSoup(html, "html.parser")
        form_tags = soup.find_all("form")
        if form_tags:
            print(f"[+] Form found on: {url}")
            forms.append(url)
    except Exception as e:
        print(f"[!] Error parsing HTML for forms on {url}: {e}")
    return forms
