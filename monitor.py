import urllib.request
import re

URL = "https://www.sparkmodel.com/main-C42EPFXI.js"

request = urllib.request.Request(
    URL,
    headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(request, timeout=30) as response:
    js = response.read().decode("utf-8", errors="ignore")

print("Main script downloaded:", len(js), "characters")

print("\n--- API ENDPOINTS ---")

paths = sorted(set(re.findall(
    r'apiURL\s*\+\s*["\']([^"\']+)',
    js
)))

for path in paths:
    print(path)

print("\n--- PRODUCT-RELATED API CODE ---")

for term in ["products", "product_id", "productId", "productStates"]:
    print("\nSearching:", term)

    for match in list(re.finditer(term, js, re.IGNORECASE))[:5]:
        start = max(0, match.start() - 250)
        end = min(len(js), match.end() + 400)
        print(js[start:end])
        print("---")
