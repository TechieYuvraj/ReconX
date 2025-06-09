# ReconX

ReconX is an ethical hacking web reconnaissance tool designed to perform comprehensive web crawling and reconnaissance tasks. It provides multiple interfaces including a command-line interface (CLI), a graphical user interface (GUI), and a web API.

## Features

- Parallel web crawling with support for keyword scanning and form detection.
- Export of discovered URLs.
- Respect for robots.txt and rel="nofollow" directives.
- Integration with Dirsearch for directory brute forcing.
- Integration with Sublist3r for subdomain enumeration.
- Screenshot capture of crawled pages.
- Generation of detailed PDF reports summarizing scan results.
- Web API for programmatic access and automation.
- User-friendly GUI for easy scan configuration and execution.

## Usage

- CLI: Run `reconx.py` with appropriate flags to start scans.
- GUI: Launch `gui.py` for a graphical interface to configure and run scans.
- Web API: Start the FastAPI server in `app/main.py` and use the provided endpoints.

## Directory Structure

- `app/`: FastAPI web application and API routes.
- `core/`: Core crawling logic and parallel crawler implementation.
- `dirsearch/`: Included directory brute forcing tool.
- `sublist3r/`: Included subdomain enumeration tool.
- `utils/`: Utility modules for scanning, exporting, screenshotting, and reporting.
- `frontend/`: Frontend assets for the web interface.
- `reports/`: Generated PDF reports.
- `screenshots/`: Captured screenshots during scans.

## Installation and Setup

1. Clone the repository:
   ```
   git clone https://github.com/TechieYuvraj/ReconX
   cd ReconX
   ```

2. Create and activate a Python virtual environment (optional but recommended):
   ```
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Unix or MacOS
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. For submodules like `dirsearch` and `sublist3r`, install their dependencies:
   ```
   pip install -r dirsearch/requirements.txt
   pip install -r sublist3r/requirements.txt
   ```

5. To run the web API server:
   ```
   uvicorn app.main:app --reload
   ```

6. To launch the GUI:
   ```
   python gui.py
   ```

7. To run scans via CLI:
   ```
   python reconx.py -u <target_url> [options]
   ```

## License

This project is licensed under the terms specified in the LICENSE file.

## Support

- Feel free to open an issue if you encounter any problems or have questions. I'll do my best.
- Contact the developer at https://yuvraj.rtunotes.in
- Developer's Portfolio https://dev.rtunotes.in
