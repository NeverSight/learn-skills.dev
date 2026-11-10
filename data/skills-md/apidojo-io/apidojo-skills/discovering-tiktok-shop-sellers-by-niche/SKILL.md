---
name: discovering-tiktok-shop-sellers-by-niche
description: >
  Discovers TikTok Shop sellers and product listings in a specific niche using apidojo's TikTok
  scraper on Apify. Triggers when the user asks to: find TikTok Shop sellers in a product category,
  discover what products are selling on TikTok Shop, identify top-selling items in a niche on TikTok,
  find competitors selling on TikTok Shop, research TikTok Shop product opportunities, discover
  trending products with affiliate links on TikTok, or build a database of TikTok Shop merchants.
  Returns seller handle, product name, price, estimated sales signals, and niche category.
  Ideal for e-commerce sellers, product researchers, affiliate marketers, and TikTok Shop entrants.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/tiktok-scraper
---

# Discovering TikTok Shop Sellers by Niche

Maps the TikTok Shop seller landscape in a product category. Identifies which products are being heavily promoted, which creators drive the most sales content, and where product gaps exist.

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | Optional | `[]` | TikTok URLs — user profiles, hashtags, music pages, search, locations |
| `keywords` | array | Optional | `[]` | Search keywords/terms to find posts |
| `sortType` | string | Optional | `RELEVANCE` | Sort order for keyword results: `RELEVANCE`, `MOST_LIKED`, `DATE_POSTED` |
| `location` | string | Optional | — | ISO 3166-1 alpha-2 country code for regional filtering (e.g. `US`, `GB`) |
| `maxItems` | number | Optional | Unlimited | Maximum posts to return across the run |
| `includeSearchKeywords` | boolean | Optional | `false` | Add the matched search keyword field to each post |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## Workflow

```
Progress:
- [ ] Step 1: Search niche hashtags with TikTok Shop signals
- [ ] Step 2: Filter posts with shop product links
- [ ] Step 3: Extract seller profiles and products
- [ ] Step 4: Rank by sales signal strength
- [ ] Step 5: Deliver seller/product map
```

### Step 1: Search Hashtags

```
TikTok Shop hashtags: #tiktokshop[niche], #[niche]shop, #[niche]deals, #tiktokmademebuyit,
                      #[niche]affiliate, #[niche]haul
```


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~tiktok-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~tiktok-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~tiktok-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~tiktok-scraper"
Input:
{
  "keywords": ["#tiktokshop", "#[niche]shop", "#tiktokmademebuyit"],
  "maxItems": 300
}
```

**REST API fallback:**
```bash
curl -X POST   "https://api.apify.com/v2/acts/apidojo~tiktok-scraper/runs?token=$APIFY_TOKEN"   -H "Content-Type: application/json"   -d '{
    "keywords": ["#tiktokshop", "#kitchentools", "#tiktokmademebuyit"],
    "maxItems": 300
  }'
```

### Step 2: Score Seller Strength

```
sales_signal = (playCount / 10000) * 0.35
             + (diggCount / 1000) * 0.25
             + (commentCount / 100) * 0.15
             + (shareCount / 500) * 0.15
             + (hasShopLink ? 1 : 0) * 0.10
```
Normalize to [0, 1]. Sellers with multiple high-signal posts get `multi_post_bonus = 0.15`.

### Step 3: Classify Seller Type

```
seller_type:
  BRAND = account.verified OR followerCount > 50K AND bio contains brand name
  CREATOR_AFFILIATE = individual account, earns commission per sale
  DROPSHIPPER = posts multiple unrelated products with generic descriptions
```

### Step 4: Edge Cases

- **Non-Shop posts in results**: Drop posts where caption has no shop signal AND no product link
- **Same product from many creators**: De-duplicate by product name; count unique promoters as a "sales momentum" signal
- **Saturated niche** (> 50 active sellers): Flag as HIGH_COMPETITION; present gap analysis (underserved sub-niches)
- **Views inflated by one viral post**: Use median views across seller's last 10 posts as the signal, not max

## Output Format

```
# TikTok Shop Seller Map: [NICHE]
Posts scanned: [N] | Unique sellers: [N] | Brands: [N] | Creator-affiliates: [N] | Date: [DATE]

## Top Sellers by Sales Signal
| Seller | Type | Product(s) | Avg Views/Post | Shop Posts | Signal Score |
|--------|------|-----------|----------------|-----------|-------------|
| @[handle] | Creator | [product] | [N] | [N] | [0.XX] |

## Top Products (by Promotion Frequency)
| Product Name | # Sellers Promoting | Avg Post Views | Price Range |
|-------------|--------------------|--------------------|-------------|
| [product] | [N] | [N] | $[X]-$[X] |

## Market Saturation
Competition level: [LOW / MEDIUM / HIGH] ([N] active sellers)
Potential gap: [sub-niche or product type with < 3 sellers]
```

## Troubleshooting

**Hashtag returns non-shop content**: Combine niche hashtag with `#tiktokshop` in the same search to anchor on shop-linked posts.
**Can't determine product price**: TikTok Shop prices aren't always in the video — note URL pattern includes product ID which can be cross-referenced manually.
**All results from one mega-creator**: Add `max_posts_per_creator = 5` to surface diverse sellers.

