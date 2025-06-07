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

## Installation

Please refer to `requirements.txt` files in the root and subdirectories for dependencies.

## License

This project is licensed under the terms specified in the LICENSE file.

