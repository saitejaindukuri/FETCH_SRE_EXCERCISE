import sys
import yaml
import requests
import time
from urllib.parse import urlparse

def get_domain(url):
    return urlparse(url).hostname.split(':')[0]

if len(sys.argv) == 1:
    print("Usage: python main.py <config.yaml>")
    sys.exit(1)

yaml_file = sys.argv[1]

try:
    with open(yaml_file, 'r') as file:
        endpoints = yaml.safe_load(file)
except Exception as error:
    print(f"Error reading file: {error}")
    sys.exit(1)

stats = {}

while True:
    for endpoint in endpoints:
        url = endpoint.get("url")
        method = endpoint.get("method", "GET").upper()
        headers = endpoint.get("headers")
        body = endpoint.get("body")

        domain = get_domain(url)

        if domain not in stats:
            stats[domain] = {"total": 0, "success": 0}

        try:
            start_time = time.time()

            if method == "POST":
                response = requests.post(url, headers=headers, data=body, timeout=2)
            elif method == "GET":
                response = requests.get(url, headers=headers, timeout=2)
            else:
                print(f"Unsupported method: {method} for domain {domain}")
                continue

            end_time = time.time()
            duration_ms = (end_time - start_time) * 1000
            status = response.status_code

            is_available = (200 <= status < 300) and (duration_ms <= 500)

            stats[domain]["total"] += 1
            if is_available:
                stats[domain]["success"] += 1

            if is_available:
                print(f"{domain} is AVAILABLE (Status: {status}, Time: {duration_ms:.2f}ms)")
            else:
                print(f"{domain} is UNAVAILABLE (Status: {status}, Time: {duration_ms:.2f}ms)")

            total = stats[domain]["total"]
            success = stats[domain]["success"]
            percentage = (success / total) * 100
            print(f"{domain} cumulative availability: {percentage:.2f}% ({success}/{total})\n")

        except Exception as err:
            print(f"{domain} — Failed to connect to {url}: {err}")

    print("waiting for next check")

    time.sleep(15)
