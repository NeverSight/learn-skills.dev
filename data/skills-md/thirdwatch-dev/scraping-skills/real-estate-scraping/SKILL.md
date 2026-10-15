---
name: real-estate-scraping
description: Use when you need property or real-estate listing data — sale and rental listings, asking prices, BHK / bed-bath counts, carpet/built-up area, floor, location and coordinates, and agent/owner details. Covers Rightmove (UK), 99acres, MagicBricks, NoBroker, CommonFloor (India), and Craigslist housing. Triggers on "scrape property listings", "real estate data", "rental prices", "property prices", "housing", "for-sale listings", "rental comps", "real estate lead gen".
license: MIT
---

# Real-Estate Scraping

Property portals are some of the most JSON-friendly targets on the web. Most render listing data server-side and embed it in `__NEXT_DATA__` / `__NUXT__` or a JSON-LD block, or load it from an internal search API you can call directly — so you rarely need a browser. The fields that matter for almost every use case:

- **Price** — asking price (sale) or monthly rent; watch for currency, "price on request", and per-sqft figures.
- **Configuration** — BHK / bedrooms + bathrooms, furnishing status, property type (apartment, villa, plot, PG, commercial).
- **Area** — carpet, built-up, and super built-up area (and the unit — sqft vs sqm).
- **Location** — locality, city, full address, and lat/lng coordinates for mapping and comps.
- **Listing meta** — floor / total floors, listing age, sale-vs-rent, photos.
- **Source** — agent vs owner-direct, agent/brokerage name, and (in India) the RERA registration ID.

Common use cases: price monitoring, market/area analysis, rental comps, and lead generation for agents.

## Ready-made scrapers

These are maintained, pay-per-result scrapers — anti-bot upkeep and field extraction are handled for you.

| Target | Scraper | From | Notes |
|--------|---------|------|-------|
| Rightmove (UK) | [Rightmove](https://apify.com/thirdwatch/rightmove-scraper) | $0.002/result | for-sale + to-rent, agent data, coords, 20+ fields |
| 99acres (India) | [99acres](https://apify.com/thirdwatch/acres99-scraper) | $0.003/result | rent/buy/PG/commercial, RERA ID, 40+ fields |
| MagicBricks (India) | [MagicBricks](https://apify.com/thirdwatch/magicbricks-scraper) | $0.003/result | rent/buy, BHK/area/floor/furnishing |
| NoBroker (India) | [NoBroker](https://apify.com/thirdwatch/nobroker-scraper) | $0.003/result | owner-direct, no brokerage |
| CommonFloor (India) | [CommonFloor](https://apify.com/thirdwatch/commonfloor-scraper) | $0.003/result | rent/buy/PG, 25+ fields |
| Craigslist (housing) | [Craigslist](https://apify.com/thirdwatch/craigslist-scraper) | $0.0015/result | apartments/rooms by city |

## Run one

Each scraper returns listing rows as JSON. Run one from the command line:

```bash
curl -X POST "https://api.apify.com/v2/acts/thirdwatch~rightmove-scraper/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "location": "London",
    "listingType": "for-sale",
    "maxResults": 25
  }'
```

Get a free token at [console.apify.com](https://console.apify.com/sign-up). Exact input fields are on each actor's Store page (linked in the table above).

## Build your own

No maintained scraper for the portal you need? Start with `web-scraping-playbook` for the build-vs-buy decision and the cost-first technique ladder (try the internal search API / embedded JSON before reaching for a browser). If the site fights back with Cloudflare, DataDome, or similar, see `anti-bot-scraping`. To package your scraper as a deployable, monetizable Apify Actor, see `apify-actor-builder`.

---

*Maintained by [Thirdwatch](https://thirdwatch.dev). 70+ ready-made scrapers on the [Apify Store](https://apify.com/thirdwatch).*
