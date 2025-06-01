from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def extract_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    links = set()

    for tag in soup.find_all("a", href=True):
        href = tag["href"]
        rel = tag.get("rel", [])

        # Optional: Skip nofollow if flag is enabled
        if "nofollow" in rel:
            continue

        full_url = urljoin(base_url, href)
        parsed = urlparse(full_url)

        if parsed.scheme in ["http", "https"]:
            links.add(full_url)

    return list(links)
