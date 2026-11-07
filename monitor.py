import urllib.request
import re

URL = "https://www.sparkmodel.com/collections?pageSize=48&state=INDEVELOPMENT"

request = urllib.request.Request(
    URL,
    headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(request, timeout=30) as response:
    html = response.read().decode("utf-8", errors="ignore")

print("Downloaded:", len(html), "characters")

print("\n--- JAVASCRIPT FILES ---")

scripts = re.findall(
    r'<script[^>]+src=["\']([^"\']+)',
    html,
    re.IGNORECASE
)

for script in scripts:
    print(script)

print("\n--- API REFERENCES ---")

matches = set(re.findall(
    r'["\']([^"\']*(?:api|graphql|product|collection)[^"\']*)["\']',
    html,
    re.IGNORECASE
))

for match in sorted(matches):
    print(match[:300])

print("\n--- PRODUCT DATA CHECK ---")

for term in ["SJ198", "products", "INDEVELOPMENT", "graphql"]:
    print(term, ":", term in html)
