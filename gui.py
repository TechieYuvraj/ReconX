import tkinter as tk
from tkinter import ttk, messagebox
from reconx import main as run_reconx
import sys, threading

class ReconXGUI:
    def __init__(self, root):
        self.root = root
        root.title("ReconX - Ethical Hacking Web Crawler")

        # ── Tk variables ───────────────────────────────────────────────────────
        self.url         = tk.StringVar()
        self.keywords    = tk.BooleanVar()
        self.forms       = tk.BooleanVar()
        self.nofollow    = tk.BooleanVar()
        self.robots      = tk.BooleanVar()
        self.dirsearch   = tk.BooleanVar()
        self.sublist3r   = tk.BooleanVar()
        self.screenshots = tk.BooleanVar()
        self.threads     = tk.IntVar(value=10)

        self.build_ui()

    # ── UI layout ─────────────────────────────────────────────────────────────
    def build_ui(self):
        ttk.Label(self.root, text="Target URL:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(self.root, textvariable=self.url, width=50).grid(row=0, column=1, columnspan=2, padx=5, pady=5)

        options = [
            ("Keyword Scanning", self.keywords),
            ("Form Detection",   self.forms),
            ("Respect 'nofollow'", self.nofollow),
            ("Parse robots.txt", self.robots),
            ("Run dirsearch",    self.dirsearch),
            ("Run sublist3r",    self.sublist3r),
            ("Capture Screenshots", self.screenshots)
        ]

        for i, (label, var) in enumerate(options, start=1):
            ttk.Checkbutton(self.root, text=label, variable=var)\
               .grid(row=i, column=0, sticky="w", padx=5)

        ttk.Label(self.root, text="Threads:").grid(row=10, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(self.root, textvariable=self.threads, width=5)\
           .grid(row=10, column=1, sticky="w", padx=5, pady=5)

        ttk.Button(self.root, text="Start Recon", command=self.start_recon)\
           .grid(row=11, column=0, columnspan=3, pady=10)

    # ── Build argv list and launch the scan in a thread ───────────────────────
    def start_recon(self):
        print(f"[DEBUG] URL value: '{self.url.get()}'")
        
        if not self.url.get().strip():
            messagebox.showerror("Error", "Please enter a target URL.")
            return

        argv = ["reconx.py", "-u", self.url.get().strip()]

        if self.keywords.get():    argv.append("--keywords")
        if self.forms.get():       argv.append("--forms")
        if self.nofollow.get():    argv.append("--nofollow")
        if self.robots.get():      argv.append("--robots")
        if self.dirsearch.get():   argv.append("--dirsearch")
        if self.sublist3r.get():   argv.append("--sublist3r")
        if self.screenshots.get(): argv.append("--screenshots")

        # threads as “--threads 8” (argparse handles it)
        argv += ["--threads", str(self.threads.get())]

        # put argv where reconx.py expects it
        sys.argv = argv
        # pass “screenshots” via hidden attr
        sys.enable_screenshots = self.screenshots.get()

        # run scan in a background thread so GUI stays responsive
        threading.Thread(target=self._run_scan, daemon=True).start()

    def _run_scan(self):
        try:
            # Build args for run_recon function
            from reconx import run_recon

            pdf_path = run_recon(
                url=self.url.get().strip(),
                keyword_scan=self.keywords.get(),
                form_detection=self.forms.get(),
                respect_nofollow=self.nofollow.get(),
                parse_robots=self.robots.get(),
                run_dirsearch_flag=self.dirsearch.get(),
                run_sublist3r_flag=self.sublist3r.get(),
                capture_screenshots=self.screenshots.get(),
                threads=self.threads.get()
            )

        except Exception as e:
            # back to main thread to show dialog
            self.root.after(0, lambda e=e: messagebox.showerror("ReconX Error", str(e)))
        else:
            self.root.after(0, lambda: messagebox.showinfo("Done", f"ReconX scan completed successfully.\nPDF report generated at:\n{pdf_path}"))

# ── Launch GUI ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app  = ReconXGUI(root)
    root.mainloop()
