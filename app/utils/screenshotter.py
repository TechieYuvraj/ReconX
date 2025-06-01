from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os

def take_screenshot(url, output_dir="screenshots"):
    try:
        os.makedirs(output_dir, exist_ok=True)
        options = Options()
        options.headless = True
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        
        from selenium.webdriver.chrome.service import Service
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        driver.get(url)

        safe_url = url.replace("https://", "").replace("http://", "").replace("/", "_")
        filepath = os.path.join(output_dir, f"{safe_url}.png")
        driver.save_screenshot(filepath)
        print(f"[✓] Screenshot saved: {filepath}")
        driver.quit()
    except Exception as e:
        print(f"[!] Screenshot failed for {url}: {e}")
