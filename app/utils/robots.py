import requests
from urllib.parse import urljoin

def parse_robots_txt(base_url):
    try:
        robots_url = urljoin(base_url, "/robots.txt")
        response = requests.get(robots_url, timeout=5)
        disallowed = []
        for line in response.text.splitlines():
            if line.lower().startswith("disallow:"):
                path = line.split(":")[1].strip()
                disallowed.append(urljoin(base_url, path))
        return disallowed
    except:
        return []