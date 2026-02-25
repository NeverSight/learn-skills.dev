---
name: amazon-data
description: Retrieve Amazon product data including pricing, reviews, sales estimates, stock levels, search results, deals, and more via the Canopy API REST endpoints using Python.
---

# Amazon Data Skill

Use this skill to retrieve Amazon product data via the Canopy API REST endpoints using Python.

Canopy API provides real-time access to 350M+ Amazon products across 25K+ categories. With this skill you can fetch:

- **Product details** — titles, descriptions, pricing, images, feature bullets, and brand info
- **Sales and stock estimates** — weekly, monthly, and annual unit sales alongside current stock levels
- **Reviews** — ratings, review text, verified purchase status, and helpful vote counts
- **Search** — find products by keyword with filters for price, condition, category, and sort order
- **Offers** — compare pricing and fulfillment details across multiple sellers
- **Deals** — browse current Amazon deals and discounts across 12 international domains
- **Categories** — navigate the full Amazon category taxonomy
- **Sellers and authors** — look up seller profiles, ratings, and author bibliographies

## Setup

1. Sign up and create an account at [canopyapi.co](https://canopyapi.co)
2. Get an API key from your dashboard
3. Set the API key in your environment:

```bash
export API_KEY="your_api_key_here"
```

## Base URL

```
https://rest.canopyapi.co
```

## Authentication

All requests require the `API-KEY` header:

```python
import os
import requests

API_KEY = os.environ["API_KEY"]
BASE_URL = "https://rest.canopyapi.co"
HEADERS = {"API-KEY": API_KEY}
```

## Endpoints

### Get Product Information

```python
response = requests.get(f"{BASE_URL}/api/amazon/product", headers=HEADERS, params={
    "asin": "B01HY0JA3G",  # or use "url" or "gtin"
    "domain": "US",         # optional, defaults to "US"
})
```

Returns product title, brand, price, rating, images, feature bullets, categories, and seller info.

### Get Product Variants

```python
response = requests.get(f"{BASE_URL}/api/amazon/product/variants", headers=HEADERS, params={
    "asin": "B01HY0JA3G",
})
```

### Get Stock Estimates

```python
response = requests.get(f"{BASE_URL}/api/amazon/product/stock", headers=HEADERS, params={
    "asin": "B01HY0JA3G",
})
```

### Get Sales Estimates

```python
response = requests.get(f"{BASE_URL}/api/amazon/product/sales", headers=HEADERS, params={
    "asin": "B01HY0JA3G",
})
```

Returns weekly, monthly, and annual unit sales estimates.

### Get Product Reviews

```python
response = requests.get(f"{BASE_URL}/api/amazon/product/reviews", headers=HEADERS, params={
    "asin": "B01HY0JA3G",
})
```

### Get Product Offers

```python
response = requests.get(f"{BASE_URL}/api/amazon/product/offers", headers=HEADERS, params={
    "asin": "B01HY0JA3G",
    "page": 1,  # optional
})
```

### Search Products

```python
response = requests.get(f"{BASE_URL}/api/amazon/search", headers=HEADERS, params={
    "searchTerm": "wireless headphones",
    "domain": "US",          # optional
    "page": 1,               # optional
    "limit": 20,             # optional, 20-40
    "minPrice": 10,          # optional
    "maxPrice": 100,         # optional
    "conditions": "NEW",     # optional: NEW, USED, RENEWED (comma-separated)
    "sort": "FEATURED",      # optional: FEATURED, MOST_RECENT, PRICE_ASCENDING, PRICE_DESCENDING, AVERAGE_CUSTOMER_REVIEW
})
```

### Get Autocomplete Suggestions

```python
response = requests.get(f"{BASE_URL}/api/amazon/autocomplete", headers=HEADERS, params={
    "searchTerm": "wireless",
})
```

### Get Category Taxonomy

```python
response = requests.get(f"{BASE_URL}/api/amazon/categories", headers=HEADERS, params={
    "domain": "US",  # optional
})
```

### Get Category Information

```python
response = requests.get(f"{BASE_URL}/api/amazon/category", headers=HEADERS, params={
    "categoryId": "1234567890",
    "domain": "US",          # optional
    "page": 1,               # optional
    "sort": "FEATURED",      # optional
})
```

### Get Seller Information

```python
response = requests.get(f"{BASE_URL}/api/amazon/seller", headers=HEADERS, params={
    "sellerId": "A2R2RITDJNW1Q6",
    "domain": "US",  # optional
    "page": 1,       # optional
})
```

### Get Author Information

```python
response = requests.get(f"{BASE_URL}/api/amazon/author", headers=HEADERS, params={
    "asin": "B000AQ5RM0",
    "domain": "US",  # optional
    "page": 1,       # optional
})
```

### Get Deals

```python
response = requests.get(f"{BASE_URL}/api/amazon/deals", headers=HEADERS, params={
    "domain": "US",  # optional: US, UK, CA, DE, FR, IT, ES, AU, IN, MX, BR, JP
    "page": 1,       # optional
    "limit": 20,     # optional
})
```

## Product Lookup Options

Product endpoints accept one of these identifiers:

| Parameter | Description             | Example                            |
| --------- | ----------------------- | ---------------------------------- |
| `asin`    | Amazon product ASIN     | `B01HY0JA3G`                       |
| `url`     | Full Amazon product URL | `https://amazon.com/dp/B01HY0JA3G` |
| `gtin`    | ISBN, UPC, or EAN code  | `9780141036144`                    |

## Supported Domains

US (default), UK, CA, DE, FR, IT, ES, AU, IN, MX, BR, JP

## Error Handling

| Status | Meaning                    |
| ------ | -------------------------- |
| 400    | Invalid parameters         |
| 401    | Invalid or missing API key |
| 402    | Payment required           |
| 500    | Server error               |

```python
response = requests.get(f"{BASE_URL}/api/amazon/product", headers=HEADERS, params={"asin": "B01HY0JA3G"})
if response.ok:
    data = response.json()
else:
    print(f"Error {response.status_code}: {response.text}")
```
