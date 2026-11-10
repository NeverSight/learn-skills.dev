---
name: discovering-viral-youtube-videos-by-category
description: >
  Discovers trending and viral YouTube videos by category and country using apidojo's YouTube
  Trending Scraper on Apify. Triggers when the user asks to: find viral YouTube videos today, discover
  what's trending on YouTube in a specific country, get trending gaming or music videos on YouTube,
  find top YouTube videos this week by category, identify viral content on YouTube for inspiration,
  research what topics are dominating YouTube trending, or track trending YouTube content for content
  strategy. Returns video title, views, likes, channel info, duration, keywords, and thumbnail.
  Ideal for content strategists, YouTubers, and trend researchers.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/youtube-trending-scraper
---

# Discovering Viral Youtube Videos By Category

---

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `type` | string | Optional | `n` | Trending category: `n` (now), `music`, `movies`, `gaming` |
| `gl` | string | Optional | `us` | Country code (e.g. `US`, `GB`) |
| `hl` | string | Optional | `en` | Language code (e.g. `en`) |
| `maxItems` | number | Optional | Unlimited | Maximum videos to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## How to Run

### Using run_actor.js (recommended)

```bash
# Quick answer (table)
node scripts/run_actor.js --actor "apidojo~youtube-trending-scraper" --input '{"type": "n", "gl": "us", "hl": "en", "maxItems": 50}'

# Save as CSV
node scripts/run_actor.js --actor "apidojo~youtube-trending-scraper" --input '{"type": "n", "gl": "us", "hl": "en", "maxItems": 50}' --output results.csv --format csv

# Save as JSON
node scripts/run_actor.js --actor "apidojo~youtube-trending-scraper" --input '{"type": "n", "gl": "us", "hl": "en", "maxItems": 50}' --output results.json --format json
```

### REST API fallback

```bash
curl -X POST "https://api.apify.com/v2/acts/apidojo~youtube-trending-scraper/runs" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type": "n", "gl": "us", "hl": "en", "maxItems": 50}'
```

If Apify MCP is available:
Use the Apify MCP `call_actor` tool with actor `apidojo~youtube-trending-scraper` and the input above.

---

## Scoring & Ranking

Score each video by:
- `views` → normalized 0-1 (cap at 10M), weight 0.40
- `likes` → normalized 0-1 (cap at 500K), weight 0.35
- `recency` (trending = 1.0 by definition), weight 0.25

```python
score = 0.40 * min(views / 10000000, 1.0) + 0.35 * min(likes / 500000, 1.0) + 0.25
```

---

## Classification

| Score | Tier | Label |
|-------|------|-------|
| ≥ 0.70 | A | MEGA_VIRAL |
| 0.40–0.69 | B | TRENDING |
| < 0.40 | C | RISING |

---

## Edge Cases

- **Category not available for country**: Some countries only have `n` (all). Fall back to `type=n`.
- **Stale data**: Trending changes throughout the day — data is a snapshot.
- **Music/movies category**: Returns full songs or trailers — content type differs from regular videos.
- **Livestreams in results**: isLive=true items are ongoing streams — filter if you need VOD only.
- **Country mismatch**: gl must be a valid ISO country code (e.g., `us`, `gb`, `de`).
