import os
from datetime import datetime
from fpdf import FPDF

class ReportGenerator:
    def __init__(self, target_url, visited_urls, scan_settings, screenshots=None, output_dir="reports"):
        self.target_url = target_url
        self.visited_urls = visited_urls
        self.scan_settings = scan_settings
        self.screenshots = screenshots or []
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_pdf(self):
        report_file = os.path.join(self.output_dir, f"ReconX_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, f"ReconX Report - {self.target_url}", ln=True)

        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
        pdf.cell(0, 10, f"Features Enabled: {', '.join([k for k,v in self.scan_settings.items() if v])}", ln=True)
        pdf.ln(5)

        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Crawled URLs:", ln=True)
        pdf.set_font("Arial", "", 11)
        for url in list(self.visited_urls)[:50]:
            pdf.multi_cell(0, 6, url)
        if len(self.visited_urls) > 50:
            pdf.cell(0, 6, f"...and {len(self.visited_urls)-50} more URLs.", ln=True)

        if self.screenshots:
            pdf.add_page()
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, "Captured Screenshots:", ln=True)
            for img_path in self.screenshots[:5]:
                try:
                    pdf.image(img_path, w=120)
                    pdf.ln(10)
                except RuntimeError:
                    pdf.cell(0, 10, f"Error displaying {img_path}", ln=True)

        pdf.output(report_file)
        print(f"[✓] PDF Report generated: {report_file}")
