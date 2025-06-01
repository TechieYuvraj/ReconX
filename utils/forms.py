# def detect_forms(soup, url):
#     forms = soup.find_all('form')
#     for i, form in enumerate(forms, 1):
#         print(f"[+] Found form #{i} at {url}")
#         for input_tag in form.find_all('input'):
#             input_type = input_tag.get("type", "text")
#             input_name = input_tag.get("name", "")
#             print(f"    Input: {input_type} - {input_name}")

def scan_for_forms(url, html):
    if "<form" in html.lower():
        print(f"[+] Form found on: {url}")
