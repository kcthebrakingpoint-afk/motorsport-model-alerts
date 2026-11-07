import urllib.request
import urllib.parse
import json

base = {
    "site": "sparkmodel-web",
    "lang": "en",
    "state": "INDEVELOPMENT"
}

tests = [
    {"currentPage": "2"},
    {"current_page": "2"},
    {"page_number": "2"},
    {"pageNo": "2"},
    {"page_no": "2"},
    {"pageIndex": "2"},
    {"per_page": "20"},
    {"hitsPerPage": "20"}
]

for extra in tests:
    params = {**base, **extra}
    url = "https://rapi.sparkmodel.com/products?" + urllib.parse.urlencode(params)

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0", "Content-Language": "en"}
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
            products = result.get("data", [])
            meta = result.get("meta", {})

            print("\nTest:", extra)
            print("Page:", meta.get("page"))
            print("Total pages:", meta.get("total_pages"))
            print("First reference:", products[0].get("code") if products else "None")

    except Exception as error:
        print("Error:", error)
