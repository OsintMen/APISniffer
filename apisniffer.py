#!/usr/bin/env python3

import requests
import argparse
import os
import json
import csv
from datetime import datetime
from urllib.parse import urljoin
from colorama import Fore, Style, init

init(autoreset=True)

BANNER = r"""
    _    ____ ___ ____        _  __  __           
   / \  |  _ \_ _/ ___| _ __ (_)/ _|/ _| ___ _ __ 
  / _ \ | |_) | |\___ \| '_ \| | |_| |_ / _ \ '__|
 / ___ \|  __/| | ___) | | | | |  _|  _|  __/ |   
/_/   \_\_|  |___|____/|_| |_|_|_| |_|  \___|_|    
         
          Author: OsintMen
          Educational Use Only
"""

COMMON_SWAGGER = [
    "/swagger",
    "/swagger-ui",
    "/swagger-ui.html",
    "/api-docs",
    "/v2/api-docs",
    "/v3/api-docs",
    "/openapi.json"
]

COMMON_GRAPHQL = [
    "/graphql",
    "/api/graphql",
    "/v1/graphql"
]

def detect_technology(headers):
    server = headers.get("Server", "")
    powered = headers.get("X-Powered-By", "")

    if "nginx" in server.lower():
        return "Nginx"
    if "apache" in server.lower():
        return "Apache"
    if "express" in powered.lower():
        return "Express.js"
    if "django" in powered.lower():
        return "Django"
    if "asp" in powered.lower():
        return "ASP.NET"

    return "Unknown"

def classify_status(code):
    if code == 200:
        return "Accessible"
    elif code == 401:
        return "Auth Required"
    elif code == 403:
        return "Forbidden"
    elif code == 429:
        return "Rate Limited"
    elif code >= 500:
        return "Server Error"
    else:
        return "Other"

def scan_path(base_url, path, headers, timeout):
    full_url = urljoin(base_url, path)

    try:
        response = requests.get(full_url, headers=headers, timeout=timeout)
        size = len(response.content)

        return {
            "url": full_url,
            "status": response.status_code,
            "size": size,
            "classification": classify_status(response.status_code),
            "technology": detect_technology(response.headers)
        }

    except requests.RequestException:
        return None

def generate_html(results, filename):
    html = """
    <html>
    <head>
    <title>APISniffer Report</title>
    <style>
    body {background:#111;color:#eee;font-family:Arial;}
    table {border-collapse:collapse;width:100%;}
    th,td {border:1px solid #444;padding:8px;}
    th {background:#222;}
    </style>
    </head>
    <body>
    <h1>APISniffer Report</h1>
    <table>
    <tr>
    <th>URL</th>
    <th>Status</th>
    <th>Classification</th>
    <th>Size</th>
    <th>Technology</th>
    </tr>
    """

    for r in results:
        html += f"""
        <tr>
        <td>{r['url']}</td>
        <td>{r['status']}</td>
        <td>{r['classification']}</td>
        <td>{r['size']}</td>
        <td>{r['technology']}</td>
        </tr>
        """

    html += "</table></body></html>"

    with open(filename, "w") as f:
        f.write(html)

def main():
    print(Fore.CYAN + BANNER)

    parser = argparse.ArgumentParser(description="APISniffer v2.0 FINAL")
    parser.add_argument("-u", "--url", required=True, help="Target base URL")
    parser.add_argument("-w", "--wordlist", required=True, help="API wordlist")
    parser.add_argument("--auth", help="Authorization header (Bearer token)")
    parser.add_argument("--timeout", type=int, default=5, help="Request timeout")
    parser.add_argument("--filter", type=int, help="Show only specific status code")

    args = parser.parse_args()

    if not os.path.exists("reports"):
        os.makedirs("reports")

    headers = {}
    if args.auth:
        headers["Authorization"] = f"Bearer {args.auth}"

    with open(args.wordlist, "r") as f:
        paths = [line.strip() for line in f if line.strip()]

    paths += COMMON_SWAGGER
    paths += COMMON_GRAPHQL

    results = []

    print(Fore.YELLOW + "[*] Scanning...")

    for path in paths:
        result = scan_path(args.url, path, headers, args.timeout)
        if result:
            if args.filter and result["status"] != args.filter:
                continue

            print(
                f"{Fore.GREEN}[+] {result['url']} | "
                f"{result['status']} | "
                f"{result['classification']} | "
                f"{result['technology']}"
            )

            results.append(result)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    json_file = f"reports/report_{timestamp}.json"
    html_file = f"reports/report_{timestamp}.html"
    csv_file = f"reports/report_{timestamp}.csv"

    with open(json_file, "w") as jf:
        json.dump(results, jf, indent=4)

    generate_html(results, html_file)

    with open(csv_file, "w", newline="") as cf:
        writer = csv.DictWriter(cf, fieldnames=results[0].keys() if results else [])
        writer.writeheader()
        writer.writerows(results)

    print(Fore.CYAN + f"\n[✓] JSON: {json_file}")
    print(Fore.CYAN + f"[✓] HTML: {html_file}")
    print(Fore.CYAN + f"[✓] CSV : {csv_file}")
    print(Fore.CYAN + "\nScan Complete!")

if __name__ == "__main__":
    main()
