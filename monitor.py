import urllib.request
import re

BASE = "https://www.sparkmodel.com"

def download(url):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="ignore")

url = BASE + "/chunk-ClaZaUFg.js"
js = download(url)

print("Downloaded collection component:", len(js), "characters")

print("\n--- API REQUESTS ---")

for match in re.finditer(r'apiURL|\.http\.(?:get|post)\(', js):
    start = max(0, match.start() - 300)
    end = min(len(js), match.end() + 500)
    print(js[start:end])
    print("\n---")

print("\n--- COLLECTION AND PRODUCT REFERENCES ---")

for term in ["collection", "product", "page_size", "pageSize", "INDEVELOPMENT"]:
    print("\nSearching for:", term)

    for match in list(re.finditer(term, js, re.IGNORECASE))[:5]:
        start = max(0, match.start() - 200)
        end = min(len(js), match.end() + 300)
        print(js[start:end])
        print("---")
