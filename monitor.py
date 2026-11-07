import urllib.request
import urllib.parse
import json

BASE = "https://rapi.sparkmodel.com/products"
base_params = {
    "site": "sparkmodel-web",
    "lang": "en",
    "state": "INDEVELOPMENT",
    "pageSize": "48"
}

tests = [
    {},
    {"page": "2"},
    {"pageNumber": "2"},
    {"offset": "48"},
    {"skip": "48"},
    {"pageIndex": "1"}
]

for extra in tests:
    params = {**base_params, **extra}
    url = BASE + "?" + urllib.parse.urlencode(params)

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0", "Content-Language": "en"}
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
            products = result.get("data", [])

            print("\nParameters:", extra or "default")
            print("Response keys:", list(result.keys()))
            print("Products returned:", len(products))

            if products:
                print("First:", products[0].get("code"))
                print("Last:", products[-1].get("code"))

    except Exception as error:
        print("Error:", error)
