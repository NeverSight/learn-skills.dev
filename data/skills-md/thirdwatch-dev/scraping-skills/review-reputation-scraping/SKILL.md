---
name: review-reputation-scraping
description: Use when scraping reviews, ratings, or reputation data — review text, star ratings, TrustScore, pros/cons, company replies. Covers Trustpilot, G2, Capterra, Yelp, Google Maps, and Shopify review widgets. Triggers on "scrape reviews", "ratings", "brand monitoring", "voice of customer", "VOC", "competitor reviews", "review mining", "review sentiment", "TrustScore".
license: MIT
---

# Review & Reputation Scraping

Routing for getting review and ratings data off the web: review text, star ratings, TrustScore, pros/cons, verification status, and company replies. Useful for brand monitoring, voice-of-customer (VOC) analysis, competitive intelligence, and review mining for product/marketing research.

## The reality on review sites

Review platforms are some of the most anti-bot-heavy targets on the web — the data is valuable and they protect it. **G2, Capterra, and Yelp sit behind DataDome and Cloudflare** and usually need a stealth browser to scrape reliably; plain HTTP gets you a challenge page. Trustpilot is gentler (server-rendered with embedded JSON), and Google Maps exposes an internal endpoint. The fields that matter for almost any analysis are the same across sites: **review text, star rating, date, reviewer, verification status, and the company's reply.** Aggregate signals (overall rating, review count, TrustScore) come for free on most listing pages.

Maintaining your own scraper here means re-solving the anti-bot challenge every time the vendor rotates it. Use a maintained scraper unless you have a reason not to.

## Ready-made scrapers

| Target | Scraper | From | Notes |
|--------|---------|------|-------|
| Trustpilot | [Trustpilot Reviews Scraper](https://apify.com/thirdwatch/trustpilot-reviews-scraper) | $0.005/result | full review text, TrustScore, company replies, 25+ fields |
| G2 | [G2 Software Reviews Scraper](https://apify.com/thirdwatch/g2-software-reviews-scraper) | $0.008/result | software ratings, pros/cons, pricing |
| Capterra | [Capterra Scraper](https://apify.com/thirdwatch/capterra-scraper) | $0.008/result | software reviews, 800+ categories |
| Yelp | [Yelp Business Scraper](https://apify.com/thirdwatch/yelp-business-scraper) | $0.008/result | business reviews, hours, contact, coords |
| Google Maps | [Google Maps Scraper](https://apify.com/thirdwatch/google-maps-scraper) | $0.002/result | business ratings + details by query/location |
| Shopify Reviews | [Shopify Reviews Scraper](https://apify.com/thirdwatch/shopify-reviews-scraper) | $0.002/result | total review count + avg rating across Judge.me/Yotpo/Loox/etc. |

Each is billed **pay-per-result** (you pay per row returned, free tier included) and the anti-bot maintenance is handled for you.

## Run one

Run a scraper from the command line — it returns review rows as JSON:

```bash
curl -X POST "https://api.apify.com/v2/acts/thirdwatch~trustpilot-reviews-scraper/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "companyDomain": "example.com",
    "maxReviews": 50
  }'
```

Get a free token at [console.apify.com](https://console.apify.com/sign-up). Input fields differ per scraper — exact input fields are on each actor's Store page (linked in the table above).

## Build your own

If no maintained scraper fits or you need a custom target:

- `web-scraping-playbook` — the build-vs-buy decision and the cost-first technique ladder (HTTP → TLS spoof → stealth browser).
- `anti-bot-scraping` — concrete bypasses for the DataDome / Cloudflare challenges these review sites use.
- `apify-actor-builder` — package your scraper as a deployable, monetizable Apify Actor.

---

*Maintained by [Thirdwatch](https://thirdwatch.dev). 70+ ready-made scrapers on the [Apify Store](https://apify.com/thirdwatch).*
