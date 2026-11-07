
import json
import os
import urllib.request
import urllib.parse
import urllib.error

API_URL = "https://rapi.sparkmodel.com/products"
BASE_URL = "https://www.sparkmodel.com/products/"
STATE_FILE = "seen_refs.json"


def api_request(url):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Content-Language": "en"
        }
    )

    with urllib.request.urlopen(request, timeout=40) as response:
        return json.loads(response.read().decode("utf-8"))


def get_all_products():
    products = []

    params = {
        "site": "sparkmodel-web",
        "lang": "en",
        "state": "INDEVELOPMENT",
        "page_number": "1"
    }

    url = API_URL + "?" + urllib.parse.urlencode(params)
    first_result = api_request(url)

    products.extend(first_result.get("data", []))

    total_pages = first_result.get("meta", {}).get("total_pages", 1)
    print(f"Found {total_pages} pages of models.")

    for page in range(2, total_pages + 1):
        params["page_number"] = str(page)
        url = API_URL + "?" + urllib.parse.urlencode(params)

        result = api_request(url)
        products.extend(result.get("data", []))

        print(f"Retrieved page {page}/{total_pages}.")

    return products


def get_category(product):
    categories = product.get("simplified_categories", [])

    if not categories:
        return "Not specified"

    try:
        name = json.loads(categories[0].get("name", "{}"))
        return name.get("en", "Not specified")
    except (TypeError, json.JSONDecodeError):
        return "Not specified"


def save_seen(seen):
    with open(STATE_FILE, "w", encoding="utf-8") as file:
        json.dump(sorted(seen), file, indent=2)


def send_discord_alert(product):
    webhook = os.environ.get("DISCORD_WEBHOOK_URL")

    if not webhook:
        raise RuntimeError(
            "DISCORD_WEBHOOK_URL secret is missing from GitHub."
        )

    product_id = product.get("product_id")
    product_name = product.get("name", "New Spark model").strip()
    product_url = BASE_URL + product_id

    embed = {
        "title": product_name[:256],
        "url": product_url,
        "color": 0x7136A8,
        "image": {
            "url": product.get("primary_image_url", "")
        },
        "fields": [
            {
                "name": "Brand",
                "value": "Spark Model",
                "inline": True
            },
            {
                "name": "Reference",
                "value": product.get("code") or "N/A",
                "inline": True
            },
            {
                "name": "Scale",
                "value": product.get("scale_name") or "N/A",
                "inline": True
            },
            {
                "name": "Year",
                "value": str(product.get("year") or "N/A"),
                "inline": True
            },
            {
                "name": "Category",
                "value": get_category(product),
                "inline": True
            },
            {
                "name": "Status",
                "value": "In Development",
                "inline": True
            }
        ],
        "footer": {
            "text": "Motorsport Models • Spark Model Alerts"
        }
    }

    payload = {"embeds": [embed]}

    request = urllib.request.Request(
        webhook,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            print("Discord response:", response.status)

    except urllib.error.HTTPError as error:
        print("Discord error status:", error.code)
        print(
            "Discord error details:",
            error.read().decode("utf-8")
        )
        raise


def main():
    print("Checking Spark Model in-development collection...")

    products = get_all_products()
    print(f"Retrieved {len(products)} models.")

    if not os.path.exists(STATE_FILE):
        seen = {
            product["product_id"]
            for product in products
            if product.get("product_id")
        }

        save_seen(seen)
        print(f"Initial setup complete. Saved {len(seen)} existing models.")
        print("No announcements sent during initial setup.")
        return

    with open(STATE_FILE, "r", encoding="utf-8") as file:
        seen = set(json.load(file))

    new_products = [
        product for product in products
        if product.get("product_id")
        and product["product_id"] not in seen
    ]

    if not new_products:
        print("No new models found.")
        return

    print(f"Found {len(new_products)} new models.")

    for product in new_products:
        send_discord_alert(product)

        seen.add(product["product_id"])
        save_seen(seen)

        print(f"Announced: {product.get('code', 'Unknown reference')}")

    print("Monitoring check complete.")


if __name__ == "__main__":
    main()
