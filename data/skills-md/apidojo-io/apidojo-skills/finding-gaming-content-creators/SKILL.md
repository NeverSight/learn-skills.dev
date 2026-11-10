---
name: finding-gaming-content-creators
description: >
  Finds gaming content creators on TikTok and YouTube using apidojo's scrapers on Apify.
  Triggers when the user asks to: find gaming influencers for brand campaigns, discover streamers
  or gaming YouTubers in a specific game or genre, find TikTok creators posting gaming content,
  identify gaming micro-influencers for product sponsorships, find gaming creators who review
  hardware or accessories, build a gaming creator outreach list for a gaming brand or peripheral
  company, or discover rising gaming creators before they go mainstream.
  Returns creator handle, platform, subscriber count, avg views, game focus, and engagement signals.
  Ideal for gaming peripheral brands, energy drink sponsors, game publishers, and esports orgs.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actors: apidojo/tiktok-scraper, apidojo/youtube-scraper
---

# Finding Gaming Content Creators

Discovers gaming creators on TikTok and YouTube. Segments by game genre and creator stage — early-stage gaming creators are cost-effective for hardware and peripheral sponsorships.

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
- [ ] Step 1: Search game-specific content on target platforms
- [ ] Step 2: Collect creator handles
- [ ] Step 3: Enrich and score
- [ ] Step 4: Classify creator type
- [ ] Step 5: Deliver creator list
```

### Step 1: Platform Searches

**TikTok:**
```
Tool: apify:run-actor
Actor: "apidojo~tiktok-scraper"
Input:
{
  "keywords": ["#[game_or_genre]", "#[game_or_genre]tiktok", "#gamingtiktok", "#[game]gameplay"],
  "maxItems": 300
}
```

**YouTube:**
```
Tool: apify:run-actor
Actor: "apidojo~youtube-scraper"
Input:
{
  "searchKeywords": ["[game_or_genre] gameplay", "[game_or_genre] review", "[game_or_genre] tips", "[game_or_genre] highlights"],
  "maxResults": 50,
  "type": "video"
}
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

**REST API fallback:**
```bash
# TikTok
curl -X POST "https://api.apify.com/v2/acts/apidojo~tiktok-scraper/runs?token=$APIFY_TOKEN"   -H "Content-Type: application/json"   -d '{"keywords": ["#valorant", "#valorantclips", "#gamingtiktok"], "maxItems": 300}'

# YouTube
curl -X POST "https://api.apify.com/v2/acts/apidojo~youtube-scraper/runs?token=$APIFY_TOKEN"   -H "Content-Type: application/json"   -d '{"searchKeywords": ["valorant gameplay", "valorant tips 2026"], "maxResults": 50}'
```

### Step 2: Score Creators

**TikTok gaming score:**
```
tt_score = (avg_views / (follower_count + 1)) * 0.40   # view-to-follower ratio
         + (avg_likes / (avg_views + 1)) * 100 * 0.30  # like rate
         + (posts_about_game / total_posts) * 0.30      # niche focus
```

**YouTube gaming score:**
```
view_ratio = avg_views / (subscriber_count + 1)
yt_score = (view_ratio > 0.10 ? 1 : view_ratio/0.10) * 0.35
         + (avg_comments / (avg_views+1) > 0.01 ? 1 : ratio/0.01) * 0.25
         + (subscriber_count in 1000..100000 ? 1 : 0.5) * 0.20
         + (niche_focus_ratio) * 0.20
```

**Creator stage:**
- Rising (< 10K subs): Affordable, high engagement, fast growing — best for early partnerships
- Mid-tier (10K–100K): Established audience, proven niche authority
- Macro (> 100K): Large reach, premium pricing

### Step 3: Edge Cases

- **Gaming news / outlet accounts appear**: Drop accounts with "news", "esports org", "official" — keep individual creators only
- **Clip compilation accounts** (reposts, not originals): Flag if `video_upload_frequency > 3/day` — likely compilation not original content
- **TikTok gaming creators also streaming**: Note in output if bio mentions "Twitch" or "stream" — these creators have dual platform value
- **Game-specific niche too small**: If < 15 creators found for a specific game, widen to genre

## Output Format

```
# Gaming Creator List: [GAME/GENRE]
Creators found: [N] | TikTok: [N] | YouTube: [N] | Rising: [N] | Mid-tier: [N] | Date: [DATE]

## Top TikTok Gaming Creators
| Creator | @Handle | Followers | Avg Views | View Ratio | Niche Focus | Stage | Score |
|---------|---------|-----------|-----------|-----------|-------------|-------|-------|

## Top YouTube Gaming Creators
| Creator | Channel | Subscribers | Avg Views | View Ratio | Content Type | Score |
|---------|---------|------------|-----------|-----------|-------------|-------|

## Rising Creators (< 10K — Early Partnership Opportunity)
| Creator | Platform | Subscribers | Avg Views | Game | Last Post |
|---------|---------|------------|-----------|------|----------|
```

## Troubleshooting

**Only mega-channels appear**: Add "small", "indie", or "growing" to search keywords to surface smaller creators.
**Gaming genre too broad**: Narrow by adding specific game title or mechanic: "FPS" → "Valorant", "battle royale".
**TikTok gaming content dominated by clips with no creator**: These are highlight reels — filter out accounts with very high posting frequency (> 2 posts/day likely aggregators).

