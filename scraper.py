import csv
import json
import time
from urllib.parse import urlparse
import requests

# ==============================================================================
# CHANGE YOUR TARGET SHOPIFY STORE URL HERE:
TARGET_URL = "ENTER YOUR TARGET SHOPIFY STORE URL"
# ==============================================================================


def clean_url(url: str) -> str:
    """Formats and normalizes any given Shopify store URL."""
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


def save_to_json(data: list, filename: str = "products.json"):
    """Saves output data to a JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def save_to_csv(data: list, filename: str = "products.csv"):
    """Saves output data to a CSV file."""
    if not data:
        return
    fieldnames = [
        "id",
        "title",
        "vendor",
        "product_type",
        "tags",
        "url",
        "min_price",
        "max_price",
    ]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            prices = [
                float(v["price"]) for v in item["variants"] if v.get("price")
            ]
            min_p = min(prices) if prices else 0.0
            max_p = max(prices) if prices else 0.0
            writer.writerow(
                {
                    "id": item["id"],
                    "title": item["title"],
                    "vendor": item["vendor"],
                    "product_type": item["product_type"],
                    "tags": item["tags"],
                    "url": item["url"],
                    "min_price": min_p,
                    "max_price": max_p,
                }
            )


def scrape_shopify_json(base_url: str) -> list:
    """Scrapes product data from any target Shopify site."""
    all_products = []
    page = 1
    start_time = time.time()

    print("\n[*] Connecting to target website...")
    print(f"[*] Base URL: {base_url}")
    print("[*] Extraction started...\n" + "-" * 60)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
    }

    while True:
        page_start = time.time()
        endpoint = f"{base_url}/products.json?page={page}&limit=250"

        try:
            response = requests.get(endpoint, headers=headers, timeout=15)

            if response.status_code != 200:
                print(
                    f"[!] Failed page {page}. HTTP Status Code: {response.status_code}"
                )
                break

            data = response.json()
            products = data.get("products", [])

            if not products:
                print("[✓] No more products found. Extraction completed!")
                break

            for product in products:
                variants = [
                    {
                        "title": v.get("title"),
                        "price": v.get("price"),
                        "sku": v.get("sku"),
                        "available": v.get("available"),
                    }
                    for v in product.get("variants", [])
                ]

                images = [img.get("src") for img in product.get("images", [])]

                all_products.append(
                    {
                        "id": product.get("id"),
                        "title": product.get("title"),
                        "handle": product.get("handle"),
                        "vendor": product.get("vendor"),
                        "product_type": product.get("product_type"),
                        "tags": ", ".join(product.get("tags", [])),
                        "created_at": product.get("created_at"),
                        "variants": variants,
                        "images": images,
                        "url": f"{base_url}/products/{product.get('handle')}",
                    }
                )

            # Continuous Autosave
            save_to_json(all_products)
            save_to_csv(all_products)

            page_duration = round(time.time() - page_start, 2)
            print(
                f"[Page {page}] Extracted {len(products)} items | Total: {len(all_products)} | Time: {page_duration}s"
            )
            page += 1

        except Exception as e:
            print(f"[!] Error occurred: {e}")
            break

    total_time = round(time.time() - start_time, 2)
    print("-" * 60)
    print(
        f"[✓] Scraping complete: {len(all_products)} total products saved in {total_time}s."
    )
    print("[✓] Output saved to products.json and products.csv.")
    return all_products


def main():
    print("=" * 60)
    print("      SHOPIFY PRODUCT SCRAPER TOOL")
    print("=" * 60)

    base_url = clean_url(TARGET_URL)
    scrape_shopify_json(base_url)


if __name__ == "__main__":
    main()
