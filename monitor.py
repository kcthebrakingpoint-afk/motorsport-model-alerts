import urllib.request
import json

BASE = "https://rapi.sparkmodel.com"
PRODUCT_ID = "4d0fdfda-04fd-4e6e-9951-47627a398b3a"

def test_api(path):
    url = BASE + path
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Content-Language": "en"
        }
    )

    print("\nTesting:", url)

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            data = response.read().decode("utf-8")
            print("Status:", response.status)
            print("Response:", data[:5000])

    except Exception as error:
        print("Error:", error)

test_api("/products/" + PRODUCT_ID + "?site=sparkmodel-web&lang=en")
test_api("/products/" + PRODUCT_ID + "/images?sort=position")
