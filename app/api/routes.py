# app/api/routes.py
from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from app.core.reconx_runner import run_reconx_scan
import os

router = APIRouter()

class ScanRequest(BaseModel):
    url: str
    keywords: bool = False
    forms: bool = False
    export: bool = False
    nofollow: bool = False
    robots: bool = False
    dirsearch: bool = False
    sublist3r: bool = False
    screenshots: bool = False
    report: bool = False
    threads: int = 10

@router.post("/scan")
def start_scan(data: ScanRequest, background_tasks: BackgroundTasks):
    scan_id = str(uuid4())
    background_tasks.add_task(run_reconx_scan, scan_id, data)
    return {"status": "queued", "scan_id": scan_id}

@router.get("/status/{scan_id}")
def get_status(scan_id: str):
    status_file = f"output/{scan_id}/status.txt"
    if not os.path.exists(status_file):
        raise HTTPException(status_code=404, detail="Scan not found")
    with open(status_file) as f:
        return {"scan_id": scan_id, "status": f.read().strip()}

@router.get("/report/{scan_id}")
def download_report(scan_id: str):
    file_path = f"output/{scan_id}/report.pdf"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Report not found")
    return FileResponse(path=file_path, filename="report.pdf", media_type="application/pdf")
