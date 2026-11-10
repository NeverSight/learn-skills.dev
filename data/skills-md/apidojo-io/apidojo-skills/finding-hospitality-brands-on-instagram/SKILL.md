---
name: finding-hospitality-brands-on-instagram
description: >
  Discovers hotels, travel brands, resorts, and hospitality businesses on Instagram using
  apidojo's Instagram Scraper on Apify. Triggers when the user asks to: find hotels on Instagram
  for B2B outreach, discover travel brands or resorts active on social media, build a list of
  hospitality businesses on Instagram, find boutique hotels or tour operators via Instagram,
  prospect hotel and resort brands for software or vendor sales, or identify travel companies
  active on Instagram. Returns account handle, follower count, bio, engagement data per post.
  Ideal for hospitality SaaS vendors, travel tech providers, and B2B service companies targeting hotels.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/instagram-scraper
---

# Finding Hospitality Brands On Instagram

---

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | ✅ | `[]` | Instagram URLs — profiles, hashtags, locations, audio pages, reels |
| `until` | string | Optional | — | Scrape posts until this date (YYYY-MM-DD) |
| `maxItems` | number | Optional | Unlimited | Maximum posts to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## How to Run

### Using run_actor.js (recommended)

```bash
# Quick answer (table)
node scripts/run_actor.js --actor "apidojo~instagram-scraper" --input '{"startUrls": ["https://www.instagram.com/explore/tags/boutiquehotel/"], "maxItems": 100}'

# Save as CSV
node scripts/run_actor.js --actor "apidojo~instagram-scraper" --input '{"startUrls": ["https://www.instagram.com/explore/tags/boutiquehotel/"], "maxItems": 100}' --output results.csv --format csv

# Save as JSON
node scripts/run_actor.js --actor "apidojo~instagram-scraper" --input '{"startUrls": ["https://www.instagram.com/explore/tags/boutiquehotel/"], "maxItems": 100}' --output results.json --format json
```

### REST API fallback

```bash
curl -X POST "https://api.apify.com/v2/acts/apidojo~instagram-scraper/runs" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"startUrls": ["https://www.instagram.com/explore/tags/boutiquehotel/"], "maxItems": 100}'
```

If Apify MCP is available:
Use the Apify MCP `call_actor` tool with actor `apidojo~instagram-scraper` and the input above.

---

## Scoring & Ranking

Score each account by:
- `followerCount` → normalized 0-1 (cap at 100K), weight 0.35
- `engagement_rate = (likeCount + commentCount) / followerCount` → weight 0.35
- `has_location_tag` (post has location data) → 0 or 1, weight 0.30

```python
score = 0.35 * min(followerCount / 100000, 1.0) + 0.35 * min(engagement_rate / 0.03, 1.0) + 0.30 * int(has_location)
```

---

## Classification

| Score | Tier | Label |
|-------|------|-------|
| ≥ 0.70 | A | PRIME_PROSPECT |
| 0.40–0.69 | B | WARM_LEAD |
| < 0.40 | C | LOW_PRIORITY |

---

## Edge Cases

- **Travel bloggers vs hotel brands**: Bloggers post travel content too. Filter by accounts with location tag + bio mentions "hotel" or "resort".
- **Broad hashtag**: #travel returns too many posts. Use #boutiquehotel, #hotelowner, #hotelmarketing.
- **Aggregator accounts**: TripAdvisor or Booking.com aggregators — filter out by domain check.
- **Low engagement**: Hospitality brands often have lower engagement than influencers — adjust threshold.
- **Consumer posts**: Guests tag hotels in posts — filter by account follower count > 500.
