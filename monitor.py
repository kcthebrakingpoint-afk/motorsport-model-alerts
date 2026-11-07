import urllib.request
import urllib.parse

BASE = "https://rapi.sparkmodel.com"

tests = [
    {"site": "sparkmodel-web", "lang": "en", "state": "INDEVELOPMENT", "pageSize": "48"},
    {"site": "sparkmodel-web", "lang": "en", "webcatalogue_state": "INDEVELOPMENT", "pageSize": "48"},
    {"site": "sparkmodel-web", "lang": "en", "state": "INDEVELOPMENT", "limit": "48"},
    {"site": "sparkmodel-web", "lang": "en", "webcatalogue_state": "INDEVELOPMENT", "limit": "48"},
]

for params in tests:
    url = BASE + "/products?" + urllib.parse.urlencode(params)
    print("\nTesting:", url)

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0", "Content-Language": "en"}
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            data = response.read().decode("utf-8")
            print("Status:", response.status)
            print("Response:", data[:2500])
    except Exception as error:
        print("Error:", error)
