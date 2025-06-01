# app/utils/file_manager.py
import os

def save_status(scan_dir, status):
    with open(os.path.join(scan_dir, "status.txt"), "w") as f:
        f.write(status)
