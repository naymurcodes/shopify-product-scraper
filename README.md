# Shopify Product Scraper Tool

A fast, automated Python scraper designed to extract full product catalogs from any public Shopify store. It automatically retrieves product details, variants, pricing, tags, and images using Shopify's public JSON API endpoints and exports the data directly into `products.csv` and `products.json`.

---

## Features

* **Universal Store Compatibility:** Scrapes any public Shopify storefront.
* **Continuous Auto-Saving:** Automatically writes progress to CSV and JSON after every page fetch to ensure zero data loss.
* **Comprehensive Data Extraction:** Captures product IDs, titles, handles, product types, vendors, tags, min/max prices, variants, SKUs, and image URLs.
* **Zero Input Delays:** Pre-configured `TARGET_URL` execution—press run and it starts extracting immediately.
* **Bot-Block Bypass:** Uses standard browser user-agent headers to navigate security checks smoothly.

---

## Output Data Formats

The tool generates two files in your project directory upon running:

* **`products.csv`**: Tabular format containing essential fields (ID, Title, Vendor, Type, Tags, Direct URL, Min Price, Max Price).
* **`products.json`**: Complete structured JSON containing nested variant details (titles, prices, SKUs, availability) and image lists.

---

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/naymurcodes/shopify-product-scraper.git](https://github.com/naymurcodes/shopify-product-scraper.git)
   cd shopify-product-scraper