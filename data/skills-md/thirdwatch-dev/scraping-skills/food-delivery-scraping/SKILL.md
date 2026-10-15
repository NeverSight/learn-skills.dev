---
name: food-delivery-scraping
description: Use when you need data from food-delivery platforms — restaurants, menus, item prices, ratings, and delivery times/fees — for menu and price intelligence, restaurant coverage analysis, market analysis, or competitor menu tracking. Covers Swiggy and Zomato (India), Talabat (Middle East), Deliveroo (UK/UAE/EU), and Noon Food. Triggers on "scrape restaurants", "menu data", "food delivery", "restaurant prices", "menu prices", "delivery fees", "restaurant ratings".
license: MIT
---

# Food-Delivery Scraping

Routes food-delivery data needs to a maintained scraper, or to the build path if none fits.

Food-delivery sites split into two technical camps. Some expose a Next.js/data API that hands back full menus over plain HTTP with no proxy — Talabat is the clean example, returning 130+ items per restaurant. Others are client-rendered behind anti-bot (Cloudflare, PerimeterX, Akamai) and need a stealth browser plus a residential proxy; these are usually **zone-based or address-based** (you pick a delivery area, then list its restaurants). The fields worth pulling are the same across all of them: restaurant **name, rating, cuisine, delivery time, delivery fee**, plus **menu items with prices**.

## Ready-made scrapers

| Target | Scraper | From | Notes |
|--------|---------|------|-------|
| Swiggy (India) | [Swiggy](https://apify.com/thirdwatch/swiggy-scraper) | $0.005/result | 30 cities, ratings/cuisines/delivery + menu items |
| Zomato (India) | [Zomato](https://apify.com/thirdwatch/zomato-scraper) | $0.002/result | 20 cities, ratings, cost-for-two, cuisines |
| Talabat (Middle East) | [Talabat](https://apify.com/thirdwatch/talabat-scraper) | $0.002/result | 9 countries, full menus (130+ items), no proxy |
| Deliveroo (UK/UAE/EU) | [Deliveroo](https://apify.com/thirdwatch/deliveroo-scraper) | $0.008/result | restaurants + full menus with prices |
| Noon Food (UAE/KSA) | [Noon Food](https://apify.com/thirdwatch/noon-food-scraper) | $0.005/result | zone-based restaurants + menus |

All billed pay-per-result (free tier included); anti-bot maintenance is handled for you.

## Run one

Each scraper runs from the CLI and returns JSON rows directly:

```bash
curl -X POST "https://api.apify.com/v2/acts/thirdwatch~talabat-scraper/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
        "country": "ae",
        "search": "burger",
        "maxResults": 25,
        "includeMenu": true
      }'
```

Get a free token at [console.apify.com](https://console.apify.com/sign-up). Input shapes differ by platform — zone/address-based scrapers (Deliveroo, Noon Food) take a location or area instead of a free-text city. **Exact input fields are on each actor's Store page.**

## Build your own

No maintained scraper for the platform you need? Start with the engineering skills:

- `web-scraping-playbook` — the build-vs-buy decision and the cost-first technique ladder (try the data API before the browser).
- `anti-bot-scraping` — concrete bypasses for the Cloudflare / DataDome / PerimeterX / Akamai walls these sites sit behind.
- `apify-actor-builder` — package your scraper as a deployable, monetizable Apify Actor.

Most food sites render restaurant lists and menus client-side via XHR — open DevTools → Network → XHR and look for the menu/search endpoint before reaching for a headless browser.

---

*Maintained by [Thirdwatch](https://thirdwatch.dev). 70+ ready-made scrapers on the [Apify Store](https://apify.com/thirdwatch).*
