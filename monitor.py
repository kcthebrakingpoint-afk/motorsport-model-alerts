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

main = download(BASE + "/main-C42EPFXI.js")

chunks = set(re.findall(
    r'import\(["\']([^"\']+\.js)["\']',
    main
))

chunks.add("./chunk-ClaZaUFg.js")
chunks.add("./chunk-CYmLvJit.js")

print("JavaScript files to inspect:", len(chunks))

for chunk in sorted(chunks):
    url = BASE + "/" + chunk.lstrip("./")

    try:
        js = download(url)
    except Exception:
        continue

    paths = set(re.findall(
        r'apiURL\s*\+\s*["\']([^"\']+)',
        js
    ))

    if paths:
        print("\nFILE:", chunk)
        print("API PATHS:", sorted(paths))

    if re.search(r'product|collection', js, re.IGNORECASE) and "apiURL" in js:
        print("\nPRODUCT/COLLECTION CODE:", chunk)

        for match in list(re.finditer(r'apiURL', js))[:5]:
            start = max(0, match.start() - 150)
            end = min(len(js), match.end() + 250)
            print(js[start:end])
