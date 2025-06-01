import subprocess

def run_dirsearch(url):
    print("[*] Running dirsearch...")
    subprocess.run(["python3", "dirsearch/dirsearch.py", "-u", url])