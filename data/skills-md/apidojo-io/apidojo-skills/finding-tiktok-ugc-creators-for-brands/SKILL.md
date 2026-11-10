---
name: finding-tiktok-ugc-creators-for-brands
description: >
  Finds TikTok UGC creators for brand campaigns using apidojo's TikTok scrapers on Apify.
  Triggers when the user asks to: find TikTok creators for user-generated content, discover UGC
  creators in a product category on TikTok, find micro-creators who post organic product reviews
  on TikTok, identify TikTok creators for paid UGC campaigns, find authentic content creators
  in beauty food tech or fitness on TikTok, or build a UGC creator roster for a brand.
  Returns creator handle, follower count, avg views, engagement rate, niche, and content samples.
  Ideal for e-commerce brands, DTC companies, and influencer marketing managers.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actors: apidojo/tiktok-scraper, apidojo/tiktok-profile-scraper
---

# Finding TikTok UGC Creators for Brands

Discovers TikTok micro-creators who produce authentic product content. UGC creators (1K–100K followers) deliver the highest ROI for paid campaigns — authentic feel, affordable rates, and high engagement relative to follower count.

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
- [ ] Step 1: Search hashtags for niche UGC content
- [ ] Step 2: Collect creator handles from search
- [ ] Step 3: Enrich profiles
- [ ] Step 4: Score UGC fit
- [ ] Step 5: Deliver creator roster
```

### Step 1: Build Hashtag Searches

```
Hashtags for niche: #[niche]review, #[niche]haul, #[niche]unboxing, #[niche]honest review,
                    #[niche]foryou, #ugc[niche], #[niche]tiktokmademebuyit
```

Example for skincare:
```
["#skincarereviews", "#skincarehaul", "#skincaretiktok", "#ugcskincare", "#honestskincarereview"]
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
  "keywords": ["#[niche]review", "#[niche]haul", "#ugc[niche]"],
  "maxItems": 200
}
```

**REST API fallback:**
```bash
curl -X POST   "https://api.apify.com/v2/acts/apidojo~tiktok-scraper/runs?token=$APIFY_TOKEN"   -H "Content-Type: application/json"   -d '{
    "keywords": ["#skincarereviews", "#skincarehaul"],
    "maxItems": 200
  }'
```

Collect unique `authorMeta.name` (handles) with > 2 posts in niche.

### Step 2: Enrich Creator Profiles

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~tiktok-profile-scraper"
Input:
{
  "profiles": ["https://www.tiktok.com/@[handle1]", "https://www.tiktok.com/@[handle2]"]
}
```

**REST API fallback:**
```bash
curl -X POST   "https://api.apify.com/v2/acts/apidojo~tiktok-profile-scraper/runs?token=$APIFY_TOKEN"   -H "Content-Type: application/json"   -d '{"profiles": ["https://www.tiktok.com/@handle1"]}'
```

### Step 3: Score UGC Fit

```
engagement_rate = (avg_likes + avg_comments) / follower_count * 100

view_to_follower_ratio = avg_views / follower_count

ugc_score = (engagement_rate > 5 ? 1 : engagement_rate / 5) * 0.35
          + (view_to_follower_ratio > 1 ? 1 : view_to_follower_ratio) * 0.30
          + (follower_count in 5000..50000 ? 1 : 0.6) * 0.20
          + (posts_in_niche >= 3 ? 1 : posts_in_niche / 3) * 0.15
```

**UGC tier classification:**
- **TIER 1** (score ≥ 0.75): High engagement, consistent niche content — ideal for paid UGC
- **TIER 2** (score 0.50–0.74): Good engagement, some niche overlap — worth testing
- **TIER 3** (score < 0.50): Low engagement or single niche post — aspirational / monitoring list

### Step 4: Edge Cases

- **Brand accounts appear in hashtag results**: Drop entries where bio contains "Official", "brand", "@company" — keep only individual creators
- **Views from single viral video inflating avg**: Calculate avg from last 10 posts; flag if std_dev > 3× avg (viral outlier)
- **Creator posts in multiple niches**: Track `niche_concentration = niche_posts / total_posts`; flag if < 30%
- **Inactive creators**: Skip if `lastPostDate > 60 days ago`

## Output Format

```
# TikTok UGC Creator Roster: [NICHE]
Creators evaluated: [N] | TIER 1: [N] | TIER 2: [N] | Date: [DATE]

## TIER 1 — Prime UGC Creators
| Creator | Handle | Followers | Avg Views | Eng Rate | View/Follower | Niche % | Score |
|---------|--------|-----------|-----------|----------|---------------|---------|-------|
| [name] | @[handle] | [N] | [N] | [X%] | [X.X×] | [X%] | [0.XX] |

## TIER 2 — Worth Testing
| Creator | Followers | Avg Views | Eng Rate | Last Active |
|---------|-----------|-----------|----------|------------|

## Niche Hashtag Performance
| Hashtag | Posts Scraped | Avg Views per Post | Top Creator Found |
|---------|--------------|-------------------|-------------------|
```

## Troubleshooting

**Too many brand accounts**: Tighten filter — drop accounts with `follower_count > 500K` and accounts with verification badge.
**Hashtag returns mainly brand posts**: Switch to user-driven hashtags: `#tiktokmademebuyit[niche]`, `#[niche]recommendation`.
**Creators found aren't making product content**: Use hashtags that explicitly signal product review intent rather than broad niche tags.

