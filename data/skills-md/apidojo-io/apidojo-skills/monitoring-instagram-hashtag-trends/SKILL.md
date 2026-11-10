---
name: monitoring-instagram-hashtag-trends
description: >
  Monitors Instagram hashtag performance and trends using apidojo's Instagram scraper on Apify.
  Triggers when the user asks to: track Instagram hashtag performance, monitor trending hashtags
  in a niche on Instagram, find the best hashtags for a content category, analyze hashtag reach
  and engagement on Instagram, discover new hashtags gaining traction in an industry, compare
  hashtag performance for a brand, or build an optimal Instagram hashtag strategy for a post.
  Returns hashtag volume, avg engagement per post, growth trend, and top-performing posts per tag.
  Ideal for Instagram content creators, social media managers, and brand content teams.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/instagram-scraper
---

# Monitoring Instagram Hashtag Trends

Analyzes hashtag performance on Instagram to identify which tags drive the best engagement for a content category. Builds a tiered hashtag strategy (broad/mid/niche) based on actual post data.

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
- [ ] Step 1: Scrape recent posts for each hashtag
- [ ] Step 2: Calculate per-hashtag metrics
- [ ] Step 3: Tier hashtags by competition/opportunity
- [ ] Step 4: Build recommended hashtag set
```

### Step 1: Scrape Hashtags


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
  "keywords": ["[HASHTAG_1]", "[HASHTAG_2]", "..."],
  "maxItems": 50
}
```

**REST API fallback:**
```bash
curl -X POST   "https://api.apify.com/v2/acts/apidojo~instagram-scraper/runs?token=$APIFY_TOKEN"   -H "Content-Type: application/json"   -d '{"keywords": ["#[hashtag1]", "#[hashtag2]"], "maxItems": 50}'
```

Run per hashtag (or in batch if MCP supports multiple hashtags in one run).

### Step 2: Calculate Metrics

For each hashtag:
```
avg_likes = mean(likesCount for all sampled posts)
avg_comments = mean(commentsCount for all sampled posts)
engagement_per_post = avg_likes + avg_comments
post_volume_estimate = total posts shown (from platform, if available)

opportunity_score = engagement_per_post / (post_volume_estimate / 10000 + 1)
```
Higher score = better engagement relative to competition.

**Hashtag tier:**
- HIGH_COMPETITION: > 1M posts — hard to rank; use rarely
- MID_TIER: 100K–1M posts — good reach/competition balance
- NICHE: < 100K posts — easier to rank, less reach but more targeted

### Step 3: Edge Cases

- **Hashtag is banned**: If scrape returns 0 posts, hashtag may be banned by Instagram — drop from strategy
- **Very new hashtag** (< 1K posts): Can't calculate reliable metrics; flag as `EMERGING — LOW DATA`
- **Same posts appear across multiple hashtags**: Deduplicate when calculating engagement metrics; report true unique post count

## Output Format

```
# Instagram Hashtag Strategy: [NICHE]
Hashtags tested: [N] | Date: [DATE]

## Performance by Hashtag
| Hashtag | Est. Posts | Avg Likes/Post | Avg Comments | Tier | Opportunity Score |
|---------|-----------|---------------|-------------|------|-----------------|
| #[tag] | [N] | [N] | [N] | MID_TIER | [0.XX] |

## Recommended Hashtag Set (Mix Strategy)
Use 20-30 hashtags per post in this ratio:
- 5 HIGH_COMPETITION tags: [list]
- 10 MID_TIER tags: [list]
- 10 NICHE tags: [list]

## Banned / Restricted Hashtags
Avoid: [list of any hashtags that returned 0 results]
```

## Troubleshooting

**Engagement data varies widely**: Normal for Instagram; use median, not mean, to reduce outlier impact.
**Hashtag has many posts but low engagement**: High volume + low engagement = dominated by bots or spam — low-value for reach; deprioritize.
**Niche hashtag auto-generation produces no results**: Not all niches have well-established hashtag communities — focus on the ones that exist and perform.

