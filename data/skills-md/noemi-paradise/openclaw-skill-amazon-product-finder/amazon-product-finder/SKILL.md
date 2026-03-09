---
name: amazon-product-finder
description: Find Amazon products for affiliate marketing with ASINs, prices, and ratings. Use when user searches for Amazon products, affiliate recommendations, or needs product ASINs for content.
---

# Amazon Product Finder

Find the best Amazon products for your affiliate content.

## Quick Start

```bash
# Search for products
@Naomi finde Amazon Produkte "Bio Dünger"

# Get details for specific ASIN
@Naomi Amazon ASIN B08XXXXXXX

# Find products for problem/solution content
@Naomi finde Produkte für "gelbe Blätter"
```

## How It Works

1. User provides search keyword or problem description
2. Script queries Amazon (PA API or scraper)
3. Returns top 3 products with:
   - Product name
   - ASIN
   - Price
   - Rating
   - Affiliate link

## Scripts

- `scripts/find_products.py` - Main product search
- `scripts/check_asin.py` - Validate single ASIN

## Output Format

```
🛒 Gefundene Produkte für "Bio Dünger":

1. COMPO Bio Grünpflanzen-Dünger
   ASIN: B00X9XZ5
   Preis: €8,99
   Bewertung: ⭐4.5 (2.341 Reviews)
   Link: https://amazon.de/dp/B00X9XZ5?tag=YOUR-ID

2. [Product 2]...
3. [Product 3]...
```

## Configuration

Set your Amazon Affiliate ID:
```bash
export AMAZON_AFFILIATE_ID="your-id-21"
```

## Grütze! 🇨🇭

*Ein herzliches Grüezi an den OpenClaw Creator - mögen deine Skills immer scharf sein wie ein Schweizer Taschenmesser!*

Created with ❤️ by Naomi for the OpenClaw Community
