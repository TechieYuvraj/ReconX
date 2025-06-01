import subprocess

def run_sublist3r(domain):
    print("[*] Running sublist3r...")
    subprocess.run(["python3", "sublist3r/sublist3r.py", "-d", domain])