---
name: finding-youtube-micro-influencers
description: >
  Finds YouTube micro-influencers and niche creators using apidojo's YouTube scraper on Apify.
  Triggers when the user asks to: find YouTube channels under 100k subscribers in a niche,
  discover emerging YouTube creators for sponsorship deals, find YouTubers covering a specific topic,
  identify high-engagement YouTube channels with smaller audiences, build a YouTube influencer outreach
  list, compare YouTube channel growth rates in a category, or find YouTube channels for affiliate
  or brand partnership programs.
  Returns channel name, subscriber count, total views, average views per video, and contact info.
  Ideal for brand sponsors, podcast networks, and affiliate marketing teams.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/youtube-scraper
---

# Finding YouTube Micro-Influencers

Searches YouTube for channels in a specific niche, then filters by subscriber count to surface micro-influencers (typically under 100K subscribers) who have high engagement relative to their audience size. Ideal for affiliate programs and brand sponsorships where micro audiences convert better.

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
- [ ] Step 1: Define niche and subscriber range
- [ ] Step 2: Build keyword and search term list
- [ ] Step 3: Run youtube-scraper
- [ ] Step 4: Filter and calculate view-to-sub ratio
- [ ] Step 5: Deliver ranked channel list
```

### Step 1: Clarify Parameters

Ask the user for:
- **Niche/topic** (e.g., "personal finance for millennials", "vegan cooking", "PC gaming")
- **Max subscribers** (default: 100,000 — micro-influencer threshold)
- **Min subscribers** (default: 5,000 — filters out very new channels)
- **Min videos** (default: 20 — ensures established presence)
- **Number of channels** to return (default: 30)

### Step 2: Build Search Term List

Generate 3-5 YouTube search queries for the niche. Think like a viewer, not a marketer:
- Personal finance → `"how to save money"`, `"budget for beginners"`, `"investing in your 20s"`
- Vegan cooking → `"easy vegan recipes"`, `"vegan meal prep"`, `"vegan on a budget"`
- PC gaming → `"budget PC build"`, `"PC gaming tips"`, `"indie game reviews"`

### Step 3: Run the Actor


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
  "searchQuery": "[SEARCH_TERM]",
  "maxResults": 50,
  "scrapeVideoDetails": false,
  "scrapeChannelDetails": true
}
```

Run for each search query. Merge channel results, deduplicate by channel ID.

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~youtube-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "searchQuery": "[SEARCH_TERM]",
    "maxResults": 50,
    "scrapeChannelDetails": true
  }'
```

Wait for `SUCCEEDED`. Fetch dataset.

### Step 4: Filter and Score

Apply subscriber range filter. Then calculate view-to-subscriber ratio as the micro-influencer quality signal:

```
view_ratio = (total_views / subscriber_count)
recent_momentum = avg_views_last_10_videos / subscriber_count
```

High `recent_momentum` (>0.5) = channel punching above its weight — ideal micro-influencer.

### Step 5: Format Output

## Output Format

```
# YouTube Micro-Influencer Discovery: [NICHE]
Subscriber range: [MIN]–[MAX] | Results: [N] channels | Date: [DATE]

| # | Channel | Subscribers | Avg Views | View/Sub Ratio | Videos | Contact | URL |
|---|---------|-------------|-----------|----------------|--------|---------|-----|
| 1 | [name]  | [N]         | [N]       | [X.Xx]         | [N]    | [email?]| [url] |

## Top 5 Picks for Outreach

1. **[Channel Name]** — [N] subs | [X.Xx] view ratio | Posts [X]x/month
   Why: [brief reason — high engagement, relevant niche, consistent posting]
   Contact: [email from About page if available]
   Latest video: "[title]" — [N] views

2–5. [same structure]

## Notes
- [N] channels found total across all search queries
- [N] filtered out (outside subscriber range or too few videos)
- View/Sub Ratio > 1.0 = exceptional engagement (views exceed subscriber count per video avg)
```

## Troubleshooting

**Only large channels in results:** YouTube search ranks by relevance + views, surfacing big channels first. Try more niche-specific search terms or filter more aggressively on subscriber count.
**No contact info:** Most YouTubers list business email in the About tab. If missing from scraper output, check the channel URL manually.
**Stale subscriber counts:** YouTube data on Apify can be 24-72h old. For final outreach list, verify top picks manually.

