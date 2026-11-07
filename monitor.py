import urllib.request
import re
from urllib.parse import urljoin

URL = "https://www.sparkmodel.com/collections?pageSize=48&state=INDEVELOPMENT"

def download(url):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="ignore")

html = download(URL)

scripts = re.findall(
    r'<script[^>]+src=["\']([^"\']+)',
    html,
    re.IGNORECASE
)

print("JavaScript files found:", len(scripts))

for script in scripts:
    script_url = urljoin(URL, script)
    print("\n---", script_url, "---")

    try:
        js = download(script_url)

        # Find API URLs and nearby references
        for match in re.finditer(r'api\.sparkmodel\.com', js, re.IGNORECASE):
            start = max(0, match.start() - 250)
            end = min(len(js), match.end() + 400)
            print(js[start:end])
            print("---")

        # Find likely product-data endpoints
        endpoints = set(re.findall(
            r'["\']([^"\']{0,150}(?:product|collection|model|search)[^"\']{0,150})["\']',
            js,
            re.IGNORECASE
        ))

        for endpoint in list(endpoints)[:30]:
            print("Possible endpoint:", endpoint)

    except Exception as error:
        print("Could not download:", error)
