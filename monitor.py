import urllib.request
import re

URL = "https://www.sparkmodel.com/collections?pageSize=48&state=INDEVELOPMENT"

request = urllib.request.Request(
    URL,
    headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(request, timeout=30) as response:
    html = response.read().decode("utf-8", errors="ignore")

print("Page downloaded successfully.")
print("HTML size:", len(html), "characters")

print("\nProduct references found:")
refs = sorted(set(re.findall(r'\b[A-Z0-9]{3,8}\b', html)))
for ref in refs:
    if re.match(r'^(SJ|S|18S|64S|5H|SP|SG)', ref):
        print(ref)

print("\nProduct page links found:")
links = sorted(set(re.findall(
    r'https?://(?:www\.)?sparkmodel\.com/products/[^"\'\s<>]+',
    html
)))

for link in links[:60]:
    print(link)

print("\nImage links found:")
images = sorted(set(re.findall(
    r'https?://[^"\'\s<>]+\.(?:jpg|jpeg|png|webp)(?:\?[^"\'\s<>]*)?',
    html,
    re.IGNORECASE
)))

for image in images[:20]:
    print(image)
