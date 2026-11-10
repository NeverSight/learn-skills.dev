---
name: finding-tiktok-creators-by-location
description: >
  Discovers TikTok creators and content by geographic location using apidojo's TikTok Location
  Scraper on Apify. Triggers when the user asks to: find TikTok creators in a specific city, discover
  local TikTok influencers by location, find content creators posting from a particular place, identify
  TikTok accounts active in a geographic area, find local micro-influencers by location tag, or build
  a list of TikTok creators in a target market region. Returns video data, creator username, follower
  count, verification status, hashtags, and engagement metrics per post.
  Ideal for local brand campaigns, geo-targeted influencer marketing, and regional market research.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/tiktok-location-scraper
---

# Finding Tiktok Creators By Location

---

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | ✅ | `[]` | TikTok location/place URLs (e.g. `https://www.tiktok.com/tag/newyork?location=true`) |
| `maxItems` | number | Optional | Unlimited | Maximum posts to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## How to Run

### Using run_actor.js (recommended)

```bash
# Quick answer (table)
node scripts/run_actor.js --actor "apidojo~tiktok-location-scraper" --input '{"startUrls": ["https://www.tiktok.com/place/Miami-Florida-123456"], "maxItems": 100}'

# Save as CSV
node scripts/run_actor.js --actor "apidojo~tiktok-location-scraper" --input '{"startUrls": ["https://www.tiktok.com/place/Miami-Florida-123456"], "maxItems": 100}' --output results.csv --format csv

# Save as JSON
node scripts/run_actor.js --actor "apidojo~tiktok-location-scraper" --input '{"startUrls": ["https://www.tiktok.com/place/Miami-Florida-123456"], "maxItems": 100}' --output results.json --format json
```

### REST API fallback

```bash
curl -X POST "https://api.apify.com/v2/acts/apidojo~tiktok-location-scraper/runs" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"startUrls": ["https://www.tiktok.com/place/Miami-Florida-123456"], "maxItems": 100}'
```

If Apify MCP is available:
Use the Apify MCP `call_actor` tool with actor `apidojo~tiktok-location-scraper` and the input above.

---

## Scoring & Ranking

Score each creator by:
- `followers` → normalized 0-1 (cap at 500K), weight 0.40
- `avg_engagement = (likes + comments + shares) / views` → weight 0.35
- `verified` → 0 or 1, weight 0.25

```python
score = 0.40 * min(followers / 500000, 1.0) + 0.35 * min(avg_engagement / 0.08, 1.0) + 0.25 * int(verified)
```

---

## Classification

| Score | Tier | Label |
|-------|------|-------|
| ≥ 0.70 | A | PRIME_CREATOR |
| 0.40–0.69 | B | GOOD_FIT |
| < 0.40 | C | LOW_PRIORITY |

---

## Edge Cases

- **No TikTok location URL**: Must provide a TikTok location page URL — not a city name. Tell user to find it via TikTok search.
- **Few results**: Some locations have limited geotagged content. Return what's available.
- **Duplicate creators**: Same creator may post multiple videos from the location — deduplicate by channel.username.
- **Irrelevant content**: Location posts may include tourists, not locals. Cross-check bio for location signals.
- **Stale content**: Sort by most recent if freshness is important.
