---
name: analyzing-competitor-instagram-content-strategy
description: >
  Analyzes a competitor's Instagram content strategy and performance using apidojo's Instagram
  scraper on Apify. Triggers when the user asks to: analyze what a competitor posts on Instagram,
  benchmark a competitor's Instagram engagement, see what content types perform best for a
  competitor on Instagram, reverse-engineer a competitor's Instagram content calendar, identify
  content gaps vs. a competitor on Instagram, compare posting frequency or content themes, or
  understand why a competitor's Instagram is growing.
  Returns post frequency, content type mix, top-performing posts, hashtag strategy, and engagement benchmarks.
  Ideal for social media managers, brand strategists, and content marketing teams.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/instagram-scraper
---

# Analyzing Competitor Instagram Content Strategy

Reverse-engineers a competitor's Instagram content strategy by analyzing their last 50+ posts. Identifies what content formats, themes, and posting patterns drive their highest engagement.

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
- [ ] Step 1: Scrape competitor's recent posts
- [ ] Step 2: Classify content types
- [ ] Step 3: Calculate engagement metrics per content type
- [ ] Step 4: Analyze posting patterns
- [ ] Step 5: (Optional) Compare to your account
- [ ] Step 6: Deliver strategy report
```

### Step 1: Scrape Competitor Profile


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

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~instagram-scraper"
Input:
{
  "usernames": ["[COMPETITOR_HANDLE]"],
  "maxItems": 50
}
```

**REST API fallback:**
```bash
curl -X POST   "https://api.apify.com/v2/acts/apidojo~instagram-scraper/runs?token=$APIFY_TOKEN"   -H "Content-Type: application/json"   -d '{"usernames": ["competitor_handle"], "maxItems": 50}'
```

### Step 2: Content Classification

For each post, classify:
```
content_type:
  PRODUCT = post primarily shows product
  LIFESTYLE = product in context / aspirational
  EDUCATIONAL = tips, how-to, facts (carousel with text)
  SOCIAL_PROOF = testimonial, user tag, press feature
  ENTERTAINMENT = meme, trending audio, humor
  PROMOTIONAL = sale, discount, CTA-heavy
  BEHIND_SCENES = team, office, process
```

Format: `IMAGE` | `VIDEO` | `CAROUSEL`

### Step 3: Calculate Metrics

```
engagement_rate = (likes + comments) / follower_count * 100

per_type_avg_engagement = avg(engagement_rate for all posts of that type)

content_type_share = count(posts of type) / total_posts * 100
```

Top performing post: highest `(likes + comments * 3)` — comments weighted higher as active signal.

**Posting cadence:**
```
posts_per_week = total_posts / (date_range_days / 7)
best_day = day_of_week with highest avg engagement
best_hour = hour_of_day with highest avg engagement (use post `timestamp`)
```

### Step 4: Edge Cases

- **Competitor has very few posts** (< 20): Report available data; note low sample size; extend to 180-day window
- **Engagement rate << 1%**: Account may have bot followers or inactive audience; note this as "audience quality concern"
- **All posts are product/promo**: This competitor is over-indexed on promotional content — opportunity for content that educates or entertains
- **Carousel shows as single image**: Some scrapers return first image only; note when `type = CAROUSEL` for accurate content type count

## Output Format

```
# Competitor Instagram Strategy: @[COMPETITOR_HANDLE]
Posts analyzed: [N] | Followers: [N] | Overall Eng Rate: [X%] | Date: [DATE]

## Content Mix
| Type | % of Posts | Avg Eng Rate | Best Post Example |
|------|-----------|-------------|------------------|
| Product | [X%] | [X%] | [post excerpt] |
| Lifestyle | [X%] | [X%] | |
| Educational | [X%] | [X%] | |

## Format Distribution
Images: [X%] | Carousels: [X%] | Videos/Reels: [X%]
Best format by engagement: [FORMAT] ([X%] eng rate)

## Top 5 Posts (by Engagement)
| # | Type | Format | Likes | Comments | Eng Rate | Caption Preview |
|---|------|--------|-------|----------|----------|----------------|

## Posting Cadence
Frequency: [X] posts/week | Best day: [Day] | Best hour: [HH:00]

## Key Observations
1. [Pattern observation — e.g. "Carousel educational posts get 2× engagement of product posts"]
2. [Observation]
3. [Opportunity gap]
```

## Troubleshooting

**Scraper returns only recent 12 posts**: Instagram limits API access to recent posts. For 50-post analysis, run scraper and note actual count returned.
**Engagement rate seems wrong**: Verify `follower_count` is current — scraper may return the follower count at time of scrape, which could differ from post-date count for historical posts.
**Competitor has very high engagement**: Distinguish between genuine engagement and pods/bought engagement — genuine engagement shows variety in commenters; pod engagement shows the same accounts commenting repeatedly.

