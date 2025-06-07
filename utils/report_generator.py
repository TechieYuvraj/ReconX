import os
from datetime import datetime
from fpdf import FPDF

class ReportGenerator:
    def __init__(self, target_url, visited_urls, scan_settings, screenshots=None, found_keywords=None, found_forms=None, dirsearch_results=None, sublist3r_results=None, output_dir="reports"):
        self.target_url = target_url
        self.visited_urls = visited_urls
        self.scan_settings = scan_settings
        self.enable_form_detection = scan_settings.get("form_detection", False)
        self.enable_dirsearch = scan_settings.get("dirsearch", False)
        self.screenshots = screenshots or []
        self.found_keywords = found_keywords or []
        self.found_forms = found_forms or []
        self.dirsearch_results = dirsearch_results
        self.sublist3r_results = sublist3r_results
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
        
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Scan Configuration:", ln=True)
        pdf.set_font("Arial", "", 11)
        for k, v in self.scan_settings.items():
            pdf.cell(0, 6, f"{k}: {v}", ln=True)

        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 6, "Features Enabled:", ln=True)
        pdf.set_font("Arial", "", 12)
        features = []
        if self.scan_settings.get("keywords", False):
            features.append("Keyword Scanning")
        if self.enable_form_detection:
            features.append("Form Detection")
        if self.enable_dirsearch:
            features.append("Directory Bruteforcing")
        if self.scan_settings.get("subdomains", False):
            features.append("Subdomain Enumeration")
        if self.scan_settings.get("screenshots", False):
            features.append("Screenshot Capture")
        # Add more features as needed
        if features:
            for f in features:
                pdf.cell(0, 6, f"- {f}", ln=True)
        else:
            pdf.cell(0, 6, "None", ln=True)
            
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Crawled URLs:", ln=True)
        pdf.set_font("Arial", "", 11)
        for url in list(self.visited_urls)[:50]:
            pdf.set_text_color(0, 0, 255)  # Blue color for links
            pdf.cell(0, 6, str(url), ln=True, link=str(url))

        if len(self.visited_urls) > 50:
            pdf.cell(0, 6, f"...and {len(self.visited_urls)-50} more URLs.", ln=True)

        # Add detailed feature results
        if self.found_keywords:
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, "Keywords Found:", ln=True)
            pdf.set_font("Arial", "", 11)
            for kw in self.found_keywords:
                keyword = kw.get("keyword", "")
                url = kw.get("url", "")
                pdf.cell(0, 6, f"- {keyword} (found on {url})", ln=True)

        if self.found_forms:
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, "Forms Detected:", ln=True)
            pdf.set_font("Arial", "", 11)
            for form in self.found_forms:
                pdf.cell(0, 6, f"- {form}", ln=True)
        else:
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, "Forms Detected:", ln=True)
            pdf.set_font("Arial", "", 11)
            pdf.cell(0, 6, "No Form Detected", ln=True)

        if self.dirsearch_results:
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, "Directory Bruteforcing Results:", ln=True)
            pdf.set_font("Arial", "", 11)
            pdf.multi_cell(0, 6, str(self.dirsearch_results))

        if self.sublist3r_results:
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, "Subdomain Enumeration Results:", ln=True)
            pdf.set_font("Arial", "", 11)
            pdf.multi_cell(0, 6, str(self.sublist3r_results))

        if self.screenshots:
            print(f"[DEBUG] Adding screenshots to report: {self.screenshots[:5]}")
            pdf.add_page()
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, "Captured Screenshots:", ln=True)
            for img_path in self.screenshots[:5]:
                try:
                    pdf.image(img_path, w=120)
                    pdf.ln(10)
                except Exception as e:
                    print(f"[!] Error displaying screenshot {img_path}: {e}")
                    pdf.cell(0, 10, f"Error displaying {img_path}", ln=True)



        pdf.add_page()
        pdf.set_font("Arial", 'I', 11)
        pdf.cell(0, 10, f"Total URLs Crawled: {len(self.visited_urls)}", ln=True)
        pdf.cell(0, 10, "Generated by ReconX - Automated Reconnaissance Tool", ln=True)


        pdf.output(report_file)
        print(f"[✓] PDF Report generated: {report_file}")
        return report_file
