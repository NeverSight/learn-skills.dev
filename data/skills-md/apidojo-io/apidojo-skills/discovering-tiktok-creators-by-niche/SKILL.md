---
name: discovering-tiktok-creators-by-niche
description: >
  Discovers and ranks TikTok creators in any niche or topic using apidojo's TikTok scrapers on Apify.
  Triggers when the user asks to: find TikTok influencers in a specific niche, discover creators
  for a campaign, identify who's growing fastest on TikTok in a category, find micro-influencers
  on TikTok under a certain follower count, build a list of TikTok creators for brand partnerships,
  compare TikTok creator engagement rates in a vertical, or identify rising TikTok stars.
  Returns creator username, follower count, avg views, engagement rate, bio, and profile URL.
  Ideal for influencer marketers, brand partnership teams, and talent managers.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actors: apidojo/tiktok-scraper, apidojo/tiktok-profile-scraper
---

# Discovering TikTok Creators by Niche

Finds TikTok creators in any topic area by scraping relevant hashtags and profiles. Returns a ranked list with follower count, engagement rate, and contact-ready profile data for influencer outreach.

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
- [ ] Step 1: Define niche and targeting criteria
- [ ] Step 2: Build hashtag list for the niche
- [ ] Step 3: Run tiktok-scraper to find creators
- [ ] Step 4: Optionally enrich with tiktok-profile-scraper
- [ ] Step 5: Rank and format output
```

### Step 1: Clarify Parameters

Ask the user for:
- **Niche/topic** (e.g., "fitness", "sustainable fashion", "personal finance")
- **Max followers** (for micro-influencers, e.g., 100000)
- **Min followers** (optional, e.g., 10000)
- **Number of creators** (default: 50)
- **Language/region** (optional)

### Step 2: Build Hashtag List

Generate 5-8 relevant hashtags for the niche. Examples:
- Fitness → `#fitness`, `#workout`, `#gymtok`, `#fitnessmotivation`, `#homeworkout`
- Finance → `#personalfinance`, `#investing`, `#moneytips`, `#financetok`, `#budgeting`
- Beauty → `#beautytok`, `#skincareroutine`, `#makeuptutorial`, `#glowup`, `#skincare`

### Step 3: Run tiktok-scraper


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
  "keywords": ["[hashtag1]", "[hashtag2]", "[hashtag3]"],
  "shouldDownloadCovers": false
}
```

**If Apify MCP is not available:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~tiktok-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": ["[hashtag1]", "[hashtag2]"],
    "shouldDownloadCovers": false
  }'
```

Save `RUN_ID`. Wait for `status: SUCCEEDED`.

### Step 4: Fetch and Deduplicate Creators

```bash
curl "https://api.apify.com/v2/actor-runs/$RUN_ID/dataset/items?token=$APIFY_TOKEN"
```

From the results, extract unique `authorMeta.id` values. Deduplicate — same creator often appears across hashtags. Sort by `authorMeta.fans` (follower count).

**Optional enrichment:** If the user wants deeper profile data, run `apidojo/tiktok-profile-scraper` with the top creator usernames to get engagement rate and video performance.

### Step 5: Apply Filters and Rank

Apply user's follower range filters. Compute a simple engagement score:
```
engagement_score = (avg_likes + avg_comments) / follower_count * 100
```

Rank by engagement score within the follower range.

## Output Format

```
# TikTok Creator Discovery: [NICHE] Niche
Found: [N] creators | Follower range: [MIN]–[MAX] | Date: [DATE]

| # | Username | Followers | Avg Views | Eng. Rate | Niche Tags | Profile |
|---|----------|-----------|-----------|-----------|------------|---------|
| 1 | @[name]  | [N]       | [N]       | [X.X%]    | [tags]     | [url]   |
| 2 | @[name]  | [N]       | [N]       | [X.X%]    | [tags]     | [url]   |

## Top Picks for Outreach
1. **@[name]** — [N] followers, [X.X%] engagement, posts primarily about [topic]
2. **@[name]** — [N] followers, [X.X%] engagement, posts primarily about [topic]
3. **@[name]** — [N] followers, [X.X%] engagement, posts primarily about [topic]

## Notes
- Engagement rate > 5% is considered high for this follower range
- [N] creators filtered out (outside follower range)
- Data freshness: ~24h from TikTok public API
```

## Troubleshooting

**Too few results:** Add more hashtags or remove follower filters.
**All results are large accounts:** Niche hashtags tend to surface mega-influencers — try sub-niche hashtags (e.g., `#homegymtok` instead of `#fitness`).
**Stale follower counts:** TikTok data cached by Apify is typically 24-48h old.

