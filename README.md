# ReconX

ReconX is an ethical hacking web reconnaissance tool designed to perform comprehensive web crawling and reconnaissance tasks. It provides multiple interfaces including a command-line interface (CLI), a graphical user interface (GUI), and a web API.

## 🚀 Current Status

ReconX is **production-ready** and actively maintained. The tool has been successfully deployed and tested with the following features fully implemented:

### ✅ Implemented Features

- **Parallel web crawling** with configurable thread count
- **Keyword scanning** for sensitive information discovery
- **Form detection** to identify input fields and forms
- **Robots.txt parsing** and compliance
- **Respect for rel="nofollow"** directives
- **Screenshot capture** during crawling
- **Dirsearch integration** for directory brute forcing
- **Sublist3r integration** for subdomain enumeration
- **PDF report generation** with detailed scan results
- **Web API** built with FastAPI for programmatic access
- **GUI interface** built with Tkinter for easy configuration
- **CLI interface** with comprehensive argument support

## 🛠️ Architecture Overview

### Core Components
- **ParallelCrawler**: Main crawling engine with thread pool management
- **ReportGenerator**: PDF report generation with detailed findings
- **Screenshotter**: Automated screenshot capture during crawling
- **Integration modules**: Seamless integration with dirsearch and sublist3r

### Available Interfaces
1. **CLI**: `python reconx.py -u <target_url> [options]`
2. **GUI**: `python gui.py` - User-friendly Tkinter interface
3. **Web API**: `uvicorn app.main:app --reload` - RESTful FastAPI endpoints

## 📁 Project Structure

```
ReconX/
├── app/                    # FastAPI web application
│   ├── main.py            # FastAPI app initialization
│   ├── api/
│   │   ├── routes.py      # API endpoints
│   │   └── schemas.py     # Pydantic models
├── core/                   # Core crawling logic
│   └── parallel_crawler.py # Main crawling engine
├── dirsearch/             # Directory brute forcing tool
├── sublist3r/             # Subdomain enumeration tool
├── frontend/              # Static web assets
├── templates/             # HTML templates for web interface
├── utils/                 # Utility modules
│   ├── export.py          # Data export functionality
│   ├── forms.py           # Form detection utilities
│   ├── keywords.py        # Keyword scanning utilities
│   ├── links.py           # Link extraction utilities
│   ├── report_generator.py # PDF report generation
│   ├── robots.py          # Robots.txt parsing
│   └── screenshotter.py   # Screenshot capture utilities
├── integrations/          # External tool integrations
│   ├── dirsearch_runner.py
│   └── sublist3r_runner.py
├── reports/               # Generated PDF reports
├── screenshots/           # Captured screenshots
├── gui.py                # GUI application
├── reconx.py             # CLI application
└── requirements.txt       # Python dependencies
```

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/TechieYuvraj/ReconX
   cd ReconX
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install dirsearch dependencies:**
   ```bash
   pip install -r dirsearch/requirements.txt
   ```

4. **Install sublist3r dependencies:**
   ```bash
   pip install -r sublist3r/requirements.txt
   ```

### Usage Examples

#### Command Line Interface
```bash
# Basic scan
python reconx.py -u https://example.com

# Advanced scan with all features
python reconx.py -u https://example.com --keywords --forms --screenshots --dirsearch --sublist3r --threads 20
```

#### Graphical User Interface
```bash
python gui.py
```

#### Web API
```bash
# Start the server
uvicorn app.main:app --reload

# Access the web interface
# Open http://localhost:8000 in your browser
```

## 🔧 Configuration Options

| Option | CLI Flag | GUI Checkbox | Description |
|--------|----------|--------------|-------------|
| Keyword Scanning | `--keywords` | ✅ | Scan for sensitive keywords |
| Form Detection | `--forms` | ✅ | Identify HTML forms |
| Respect nofollow | `--nofollow` | ✅ | Skip rel="nofollow" links |
| Parse robots.txt | `--robots` | ✅ | Respect robots.txt directives |
| Dirsearch | `--dirsearch` | ✅ | Run directory brute forcing |
| Sublist3r | `--sublist3r` | ✅ | Enumerate subdomains |
| Screenshots | `--screenshots` | ✅ | Capture page screenshots |
| Thread Count | `--threads N` | Input field | Number of parallel threads |

## 📊 Output

### Generated Reports
- **PDF Report**: Comprehensive scan results with findings
- **Screenshots**: Visual documentation of discovered pages
- **Structured Data**: JSON export available via API

### Report Contents
- Discovered URLs with status codes
- Found keywords and sensitive information
- Identified forms and input fields
- Directory brute force results
- Subdomain enumeration results
- Screenshots of key pages
- Scan configuration summary

## 🌐 Web API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main web interface |
| `/api/scan` | POST | Start a new scan |
| `/api/reports` | GET | List available reports |
| `/api/reports/{id}` | GET | Download specific report |
| `/about` | GET | About page |
| `/contact` | GET | Contact page |

## 🛡️ Security & Ethics

ReconX is designed for **ethical hacking and authorized security testing only**. Users are responsible for:
- Obtaining proper authorization before scanning
- Complying with applicable laws and regulations
- Using the tool responsibly and ethically

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/TechieYuvraj/ReconX/issues)
- **Contact**: [Yuvraj Singh](https://yuvraj.rtunotes.in)
- **Portfolio**: [Developer Portfolio](https://dev.rtunotes.in)

## 🔄 Changelog

### Latest Updates
- ✅ FastAPI web API implementation
- ✅ GUI interface with Tkinter
- ✅ Enhanced PDF report generation
- ✅ Screenshot capture functionality
- ✅ Dirsearch and Sublist3r integration
- ✅ Parallel crawling with thread management
- ✅ Comprehensive CLI with argument parsing

---

**Note**: This tool is for educational and authorized security testing purposes only. Users are responsible for ensuring they have proper authorization before scanning any targets.
