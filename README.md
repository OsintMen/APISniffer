# APISniffer 
## Professional API Recon Framework
```
    _    ____ ___ ____        _  __  __           
   / \  |  _ \_ _/ ___| _ __ (_)/ _|/ _| ___ _ __ 
  / _ \ | |_) | |\___ \| '_ \| | |_| |_ / _ \ '__|
 / ___ \|  __/| | ___) | | | | |  _|  _|  __/ |   
/_/   \_\_|  |___|____/|_| |_|_|_| |_|  \___|_|   
```
![APISniffer Banner](https://via.placeholder.com/800x150.png?text=APISniffer+v3)

**Author:** OsintMen  
**Purpose:** Educational & Authorized Security Testing Only  

APISniffer v3 is a professional tool to discover API endpoints safely, detect technologies, classify HTTP responses, and generate detailed reports.  

---

## ⚡ Features

- API endpoint discovery via custom wordlists (1000+ paths recommended)
- Swagger / OpenAPI detection
- GraphQL endpoint detection
- Status code classification (200, 401, 403, 404, 429, 500+)
- Technology detection from headers (Apache, Nginx, Express.js, Django, ASP.NET)
- Multi-format reporting:
  - JSON  
  - CSV  
  - HTML (professional table format)
- Authorization header support (Bearer tokens)
- Request timeout control
- Optional filter for specific status codes

---

## ⚙ Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/apisniffer.git
cd APISniffer
```

## Install dependencies:
```bash
pip install -r requirements.txt
```
## 🏃 Usage Examples

**1️⃣ Basic Scan**
```bash
python3 apisniffer.py -u https://target.com -w wordlists/api_paths.txt
```
**2️⃣ With Authorization Header**
```bash
python3 apisniffer.py -u https://target.com -w wordlists/api_paths.txt --auth "YOUR_BEARER_TOKEN"
```
**3️⃣ Custom Timeout**
```bash
python3 apisniffer.py -u https://target.com -w wordlists/api_paths.txt --timeout 10
```

**4️⃣ Filter Specific Status Codes**
```bash
python3 apisniffer.py -u https://target.com -w wordlists/api_paths.txt --filter 200
```
`Shows only endpoints returning HTTP 200.`

# 📂 Wordlists
You can use:
Your own custom API paths (wordlists/api_paths.txt)

[SecLists](https://github.com/danielmiessler/SecLists)for educational lab testing

**Example paths in api_paths.txt:**
```bash
api/
api/v1/
login/
auth/
users/
products/
orders/
admin/
dashboard/
config/
```
## 📂 Reports
**After scanning, all reports are stored in reports/:**
```bash
reports/
    report_20260223_152344.json
    report_20260223_152344.html
    report_20260223_152344.csv
```   

- JSON: structured raw results

- CSV: easy to open in Excel

- HTML: professional visual report

## ⚖ Legal Disclaimer

- Only scan systems you own or have explicit permission to test.

- Misuse for unauthorized testing is illegal.

- The author is not responsible for misuse.

- Intended for educational purposes and lab testing only.
