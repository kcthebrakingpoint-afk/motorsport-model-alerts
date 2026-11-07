import urllib.request
import urllib.parse
import json

url = "https://rapi.sparkmodel.com/products?" + urllib.parse.urlencode({
    "site": "sparkmodel-web",
    "lang": "en",
    "state": "INDEVELOPMENT"
})

request = urllib.request.Request(
    url,
    headers={"User-Agent": "Mozilla/5.0", "Content-Language": "en"}
)

with urllib.request.urlopen(request, timeout=30) as response:
    result = json.loads(response.read().decode("utf-8"))

print("PAGINATION METADATA:")
print(json.dumps(result.get("meta"), indent=2))
