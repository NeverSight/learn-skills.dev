---
name: finding-food-bloggers-and-creators
description: >
  Finds food content creators across Instagram TikTok and YouTube using apidojo's social media
  scrapers on Apify. Triggers when the user asks to: find food bloggers for brand partnerships,
  discover recipe creators in a cuisine niche, find cooking influencers for a food brand campaign,
  identify restaurant reviewers or food critics on social media, find home cook creators for
  kitchen tool promotions, build a food creator outreach list for a food or beverage brand,
  or discover the most engaged food content creators by platform and niche.
  Returns creator handle, platform, follower count, avg engagement, content theme, and post samples.
  Ideal for food and beverage brands, kitchen tool companies, restaurant chains, and food PR agencies.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actors: apidojo/instagram-scraper, apidojo/tiktok-scraper, apidojo/youtube-scraper
---

# Finding Food Bloggers and Creators

Discovers food content creators across Instagram, TikTok, and YouTube. Segments by content theme (recipes, restaurant reviews, meal prep, fine dining) and engagement quality.

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | ✅ | `[]` | Instagram URLs — profiles, hashtags, locations, audio pages, reels |
| `until` | string | Optional | — | Scrape posts until this date (YYYY-MM-DD) |
| `maxItems` | number | Optional | Unlimited | Maximum posts to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## Workflow

```
Progress:
- [ ] Step 1: Search food hashtags per platform
- [ ] Step 2: Collect unique creator handles
- [ ] Step 3: Enrich and score by platform
- [ ] Step 4: Cross-platform deduplication
- [ ] Step 5: Deliver segmented creator list
```

### Step 1: Platform Hashtags

**Instagram hashtags:**
```
["#[food_niche]", "#[food_niche]recipe", "#[food_niche]love", "#[food_niche]blogger",
 "#homecook", "#foodphotography", "#recipeoftheday"]
```

**TikTok hashtags:**
```
["#[food_niche]", "#[food_niche]tiktok", "#cookingtiktok", "#foodtok", "#recipeoftiktok"]
```

**YouTube search keywords:**
```
["[food_niche] recipe", "[food_niche] cooking", "how to make [food_niche]"]
```

**If Apify MCP is available (run for each platform):**
```
Instagram:
Tool: apify:run-actor
Actor: "apidojo~instagram-scraper"
Input: {"keywords": ["#[food_niche]", "#[food_niche]recipe"], "maxItems": 100}

TikTok:
Tool: apify:run-actor
Actor: "apidojo~tiktok-scraper"
Input: {"keywords": ["#[food_niche]", "#foodtok"], "maxItems": 200}

YouTube:
Tool: apify:run-actor
Actor: "apidojo~youtube-scraper"
Input: {"searchKeywords": ["[food_niche] recipe"], "maxResults": 50}
```

**REST API fallback (run one at a time):**
```bash
# Instagram
curl -X POST "https://api.apify.com/v2/acts/apidojo~instagram-scraper/runs?token=$APIFY_TOKEN"   -H "Content-Type: application/json"   -d '{"keywords": ["#italianrecipes", "#italianfood"], "maxItems": 100}'

# TikTok
curl -X POST "https://api.apify.com/v2/acts/apidojo~tiktok-scraper/runs?token=$APIFY_TOKEN"   -H "Content-Type: application/json"   -d '{"keywords": ["#italianrecipes", "#foodtok"], "maxItems": 200}'
```

### Step 2: Score Per Platform

**Instagram:**
```
engagement_rate = (avg_likes + avg_comments) / follower_count * 100
ig_score = (engagement_rate / 5.0) * 0.40 + (follower_count in 5K..100K ? 1 : 0.6) * 0.30 + (posts_in_niche/10) * 0.30
```

**TikTok:**
```
view_ratio = avg_views / follower_count
tt_score = (view_ratio > 1 ? 1 : view_ratio) * 0.40 + (engagement_rate / 5) * 0.30 + (posts_in_niche/10) * 0.30
```

**YouTube:**
```
view_ratio = avg_views / subscriber_count
yt_score = (view_ratio > 0.15 ? 1 : view_ratio/0.15) * 0.40 + (avg_comments/avg_views > 0.01 ? 1 : (avg_comments/avg_views)/0.01) * 0.30 + (subscriber_count in 5K..200K ? 1 : 0.6) * 0.30
```

### Step 3: Edge Cases

- **Same creator on multiple platforms**: Deduplicate by matching handle similarity; link as `cross_platform_creator` (higher reach value)
- **Recipe aggregator accounts** (not original creators): Drop accounts posting recipes from other sites — bio will mention "recipes from around the web"
- **Food brand official accounts appear**: Filter out `verified` accounts and accounts with > 500K followers
- **Inactive creators**: Filter `last_post_date > 45 days` from current date

## Output Format

```
# Food Creator List: [FOOD_NICHE]
Creators found: [N] | Instagram: [N] | TikTok: [N] | YouTube: [N] | Cross-platform: [N] | Date: [DATE]

## Top Creators by Platform

### Instagram
| Creator | @Handle | Followers | Avg Likes | Eng Rate | Content Theme | Score |
|---------|---------|-----------|-----------|----------|---------------|-------|

### TikTok
| Creator | @Handle | Followers | Avg Views | View Ratio | Score |
|---------|---------|-----------|-----------|-----------|-------|

### YouTube
| Creator | Channel | Subscribers | Avg Views | View Ratio | Score |
|---------|---------|------------|-----------|-----------|-------|

## Cross-Platform Creators (Highest Reach)
[Creator] is active on Instagram ([N] followers) + TikTok ([N] followers)
```

## Troubleshooting

**Too many professional food photographers (not bloggers)**: Filter out accounts where caption is consistently just a recipe title with no personal voice.
**Results dominated by restaurant accounts**: Add "home cook" or "recipe creator" qualifiers to hashtags; search `#homecook[niche]`.
**Low engagement on food content**: Food photography content typically has lower engagement than personal narrative — adjust `min_engagement_rate` to 1.5% for Instagram food accounts specifically.



**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~instagram-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~instagram-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~instagram-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

