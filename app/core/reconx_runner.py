# app/core/reconx_runner.py
import os
from app.utils.file_manager import save_status
from reconx import main as reconx_main
import sys

def run_reconx_scan(scan_id: str, config):
    scan_dir = f"output/{scan_id}"
    os.makedirs(scan_dir, exist_ok=True)
    save_status(scan_dir, "running")

    sys.argv = [
        "reconx.py",
        "-u", config.url,
        "--threads", str(config.threads)
    ]
    if config.keywords: sys.argv.append("--keywords")
    if config.forms: sys.argv.append("--forms")
    if config.export: sys.argv.append("--export")
    if config.nofollow: sys.argv.append("--nofollow")
    if config.robots: sys.argv.append("--robots")
    if config.dirsearch: sys.argv.append("--dirsearch")
    if config.sublist3r: sys.argv.append("--sublist3r")
    if config.screenshots: sys.argv.append("--screenshots")

    sys.enable_screenshots = config.screenshots
    sys.generate_report = config.report
    sys.scan_output_path = scan_dir

    try:
        reconx_main()
        save_status(scan_dir, "completed")
    except Exception as e:
        save_status(scan_dir, f"error: {str(e)}")
