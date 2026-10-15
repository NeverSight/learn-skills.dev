---
name: ecommerce-product-scraping
description: Use when you need to scrape e-commerce product data — titles, brands, prices, MRP/list price, discounts, ratings, variants/sizes, availability, images, and product URLs — from online storefronts and marketplaces. Covers Amazon, Flipkart, AliExpress, Myntra, Nykaa, Meesho, Snapdeal, Noon, AJIO, FirstCry, Tata Cliq, and any Shopify store. For price monitoring / MAP enforcement, catalog building, competitor price tracking, and dropshipping product research. Triggers on "scrape products", "price monitoring", "product catalog", "competitor prices", "MAP", "track prices", "build a product database", "compare prices across stores".
license: MIT
---

# E-commerce Product Scraping

Routes product-data tasks to the right scraper or build path. The goal is structured product rows — title, brand, price, MRP/list price, discount, rating, variants, image, URL — at the lowest cost per result.

## How storefronts expose product data

Most e-commerce sites embed full product JSON in the page, so you rarely need to parse HTML:

- **SSR / embedded JSON** — `__NEXT_DATA__` (Next.js), `__NUXT__`, `window.__INITIAL_STATE__`, or site-specific blobs (Myntra's `__myx`). Full structured catalog with no DOM parsing.
- **Internal search/PDP APIs** — open DevTools → Network → XHR while browsing; listings and product pages almost always fetch JSON you can call directly. Find the endpoint the page calls for itself rather than parsing HTML.
- **Stealth-browser-only** — a few storefronts sit behind Akamai or DataDome (Nykaa, Meesho, Tata Cliq) and serve a skeleton to HTTP clients. These need a hardened browser; intercept the XHR or walk product anchors rather than fighting hashed CSS-module class names.

**Key fields to capture:** `title`, `brand`, `price`, `mrp`/list price, `discount`, `rating`, `variants`/sizes, `availability`, `image`, `url`. MRP + discount together are what make a row useful for price/MAP monitoring.

## Ready-made scrapers

Skip the anti-bot fight — these are maintained and billed pay-per-result.

| Target | Scraper | From | Notes |
|--------|---------|------|-------|
| Amazon | [Amazon Products](https://apify.com/thirdwatch/amazon-product-scraper) | $0.002/result | 18+ country domains, ASIN/price/rating |
| Flipkart | [Flipkart Products](https://apify.com/thirdwatch/flipkart-products-scraper) | $0.003/result | India, price/rating/seller |
| AliExpress | [AliExpress Products](https://apify.com/thirdwatch/aliexpress-product-scraper) | $0.003/result | price/sales count/ratings |
| Myntra | [Myntra](https://apify.com/thirdwatch/myntra-scraper) | $0.002/result | India fashion, sizes + variants |
| Nykaa | [Nykaa](https://apify.com/thirdwatch/nykaa-scraper) | $0.005/result | India beauty |
| Meesho | [Meesho](https://apify.com/thirdwatch/meesho-scraper) | $0.005/result | India social commerce |
| Snapdeal | [Snapdeal](https://apify.com/thirdwatch/snapdeal-scraper) | $0.002/result | India marketplace |
| Noon.com | [Noon](https://apify.com/thirdwatch/noon-scraper) | $0.002/result | UAE/KSA/Egypt |
| AJIO | [AJIO](https://apify.com/thirdwatch/ajio-scraper) | $0.002/result | India fashion |
| FirstCry | [FirstCry](https://apify.com/thirdwatch/firstcry-scraper) | $0.002/result | India baby/kids |
| Tata Cliq | [Tata Cliq](https://apify.com/thirdwatch/tatacliq-scraper) | $0.005/result | India marketplace |
| Shopify Store | [Shopify Store Products](https://apify.com/thirdwatch/shopify-store-scraper) | $0.001/result | any Shopify store, full variants/SKU/price |
| Shopify Reviews | [Shopify Reviews](https://apify.com/thirdwatch/shopify-reviews-scraper) | $0.002/result | review count + rating across widgets |

## Run one

Each scraper takes a JSON input and returns product rows. Run synchronously from the CLI:

```bash
curl -X POST "https://api.apify.com/v2/acts/thirdwatch~amazon-product-scraper/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "queries": ["wireless earbuds"],
    "maxResults": 25
  }'
```

Get a free token at [console.apify.com](https://console.apify.com/sign-up). Exact input fields are on each actor's Store page — input keys differ per site (search term vs. category URL vs. product URL).

## Build your own

No scraper for your target, or you need to own it? Start with the engineering skills in this collection:

- `web-scraping-playbook` — the build-vs-buy decision and the cost-first technique ladder (HTTP → TLS spoof → stealth browser).
- `anti-bot-scraping` — concrete bypasses for Akamai, DataDome, Cloudflare, PerimeterX (the protections in front of Nykaa, Meesho, Tata Cliq).
- `apify-actor-builder` — package it as a deployable, monetizable Apify Actor.

---

*Maintained by [Thirdwatch](https://thirdwatch.dev). 70+ ready-made scrapers on the [Apify Store](https://apify.com/thirdwatch).*
