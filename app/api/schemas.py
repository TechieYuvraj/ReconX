from pydantic import BaseModel, HttpUrl

class CrawlOptions(BaseModel):
    url: HttpUrl
    enable_keywords: bool = False
    enable_forms: bool = False
    enable_screenshots: bool = False
    enable_pdf_report: bool = False
