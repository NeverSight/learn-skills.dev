---
name: analyzing-competitor-youtube-content-strategy
description: >
  Analyzes a competitor's YouTube channel content strategy and performance using apidojo's YouTube
  scraper on Apify. Triggers when the user asks to: analyze what a competitor posts on YouTube,
  see what video types perform best for a competitor, reverse-engineer a competitor's YouTube
  content calendar, benchmark your YouTube channel against a competitor, identify content gaps
  vs. a competitor on YouTube, understand what topics drive views for a competitor, or compare
  subscriber growth and video performance between two YouTube channels.
  Returns video cadence, format mix, top-performing topics, view benchmarks, and engagement analysis.
  Ideal for content marketing teams, YouTube strategists, and brand video teams.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/youtube-scraper
---

# Analyzing Competitor YouTube Content Strategy

Reverse-engineers a competitor's YouTube channel by analyzing their last 20-50 videos. Identifies which video topics, formats, and lengths drive the most views and engagement.

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | Optional | `[]` | YouTube URLs — channels, playlists, Shorts, search results |
| `youtubeHandles` | array | Optional | `[]` | YouTube channel handles (e.g. `@kurzgesagt`) |
| `getTrending` | boolean | Optional | `false` | Retrieve trending videos |
| `keywords` | array | Optional | `[]` | Search keywords |
| `gl` | string | Optional | `us` | Country code for results (e.g. `US`, `GB`) |
| `hl` | string | Optional | `en` | Language code (e.g. `en`, `de`) |
| `uploadDate` | string | Optional | `all` | Upload date filter: `any`, `hour`, `today`, `week`, `month`, `year` |
| `duration` | string | Optional | `all` | Duration filter: `any`, `short`, `long` |
| `features` | string | Optional | `all` | Feature filter: `4k`, `hd`, `live`, `cc`, `3d`, `hdr`, etc. |
| `sort` | string | Optional | `r` | Sort order for search results |
| `maxItems` | number | Optional | Unlimited | Maximum videos to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## Workflow

```
Progress:
- [ ] Step 1: Scrape competitor's recent videos
- [ ] Step 2: Classify video types and topics
- [ ] Step 3: Calculate performance metrics
- [ ] Step 4: Identify patterns and top performers
- [ ] Step 5: (Optional) Compare with own channel
- [ ] Step 6: Deliver strategy report
```

### Step 1: Scrape Channel


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~youtube-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~youtube-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~youtube-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~youtube-scraper"
Input:
{
  "startUrls": [{"url": "[COMPETITOR_CHANNEL_URL]"}],
  "maxResults": 30,
  "type": "video"
}
```

**REST API fallback:**
```bash
curl -X POST   "https://api.apify.com/v2/acts/apidojo~youtube-scraper/runs?token=$APIFY_TOKEN"   -H "Content-Type: application/json"   -d '{"startUrls": [{"url": "https://www.youtube.com/@competitorhandle"}], "maxResults": 30, "type": "video"}'
```

### Step 2: Classify Videos

```
video_type:
  TUTORIAL = title contains "how to", "step by step", "guide", "tutorial"
  LIST = title contains "top [N]", "[N] best", "[N] things", "mistakes"
  REVIEW = title contains "review", "tested", "worth it", "vs"
  THOUGHT_LEADERSHIP = opinion, trend analysis, "the future of", "why"
  NEWS = title contains news, announcement, breaking
  CASE_STUDY = "how [brand] grew", "inside", "behind the scenes"

video_length_tier:
  SHORT = < 5 min
  MEDIUM = 5–15 min
  LONG = 15–30 min
  DEEP_DIVE = > 30 min
```

### Step 3: Performance Metrics

```
view_ratio = viewCount / subscriberCount  # corrected by subscriberCount at time of analysis

engagement_rate = (likeCount + commentCount) / viewCount * 100

publish_cadence = total_videos / (date_range_weeks)  # videos per week
```

**Top performer:** Sort by `viewCount`; also identify `hidden gems` where engagement_rate > 2× channel average despite lower views.

### Step 4: Edge Cases

- **Channel is very new** (< 6 months, < 20 videos): Reduce `videos_to_analyze` to all available; note limited sample
- **Views are all very low** (< 1K per video): Channel may be struggling or niche is very small; provide absolute numbers, not just ratios
- **One mega-viral video skews averages**: Report median views alongside mean; flag outlier
- **Channel posts in multiple languages**: Group by language; analyze each cohort separately

## Output Format

```
# Competitor YouTube Strategy: [CHANNEL_NAME]
Videos analyzed: [N] | Subscribers: [N] | Avg Views: [N] | Avg Eng Rate: [X%] | Date: [DATE]

## Content Mix
| Video Type | % of Videos | Avg Views | Avg Eng Rate | Best Example |
|-----------|------------|-----------|-------------|-------------|
| Tutorial | [X%] | [N] | [X%] | [title] |
| List | [X%] | [N] | [X%] | |
| Review | [X%] | [N] | [X%] | |

## Video Length Performance
| Length Tier | % | Avg Views | Avg Eng Rate |
|------------|---|-----------|-------------|
| Short (< 5min) | [X%] | [N] | [X%] |

## Top 5 Videos (by Views)
| # | Title | Type | Views | Likes | Comments | Length | Eng Rate |
|---|-------|------|-------|-------|----------|--------|---------|

## Publishing Cadence
Videos/week: [X] | Best day to publish: [Day] | Monthly trend: [↑/↓/flat]

## Key Opportunities vs. Their Strategy
1. [Gap: e.g. "No case studies — this format gets 3× their avg views when they do it"]
2. [Opportunity]
3. [Their weakness]
```

## Troubleshooting

**Scraper returns channel page but no videos**: Try direct video search for channel name as keyword; some channel URLs need the `/videos` suffix.
**View counts are very low for an established channel**: Channel may have declined — check publish date of latest video; may be dormant.
**Can't determine channel subscriber count from scrape**: Use the video view-to-video count ratio as a proxy for channel health when subscriber count is unavailable.

