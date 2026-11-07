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

html = download(BASE + "/collections?pageSize=48&state=INDEVELOPMENT")

scripts = re.findall(
    r'<script[^>]+src=["\']([^"\']+)',
    html,
    re.IGNORECASE
)

main_script = next(s for s in scripts if "main-" in s)
js = download(BASE + "/" + main_script.lstrip("/"))

print("API CONFIGURATION")
for match in re.finditer(r'apiURL', js):
    print(js[max(0, match.start()-100):match.start()+200])
    print("---")

print("\nCOLLECTION COMPONENT")
for match in re.finditer(r'CollectionsPageComponent', js):
    print(js[max(0, match.start()-500):match.start()+200])
    print("---")

print("\nCOLLECTION CHUNK FILES")
chunks = set(re.findall(
    r'import\(["\']([^"\']+\.js)["\']\)\.then\([^)]*CollectionsPageComponent',
    js
))
for chunk in sorted(chunks):
    print(chunk)

print("\nPOSSIBLE API PATHS")
paths = set(re.findall(
    r'["\'](/[^"\']*(?:collection|product|model)[^"\']*)["\']',
    js,
    re.IGNORECASE
))
for path in sorted(paths):
    print(path)
