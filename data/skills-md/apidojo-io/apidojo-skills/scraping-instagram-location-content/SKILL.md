---
name: scraping-instagram-location-content
description: >
  Scrapes Instagram posts tagged at a specific location using apidojo's Instagram Location scraper on Apify.
  Triggers when the user asks to: find Instagram posts from a specific location or venue, scrape user-generated
  content from a restaurant, hotel, or event on Instagram, find photos tagged at a conference or festival,
  monitor what guests or visitors post from a location, discover content creators who visited a place,
  build a UGC library from a location tag, or find influencers who have been to a specific venue or city.
  Returns post URL, caption, author handle, likes, comments, and timestamp per location post.
  Ideal for hospitality brands, event marketers, and UGC content curation teams.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/instagram-location-scraper
---

# Scraping Instagram Location Content

Collects all public Instagram posts tagged at a specific location — useful for gathering UGC, finding visitors who post about a venue, or discovering creators with genuine affinity for a place.

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed


## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | Optional | `[]` | Instagram location page URLs |
| `locationIds` | array | Optional | `[]` | Instagram location IDs |
| `maxItems` | number | Optional | Unlimited | Maximum posts to return |
| `until` | string | Optional | — | Date filter (YYYY-MM-DD) |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |
## Workflow

```
Progress:
- [ ] Step 1: Find the Instagram location ID for the target venue
- [ ] Step 2: Run instagram-location-scraper
- [ ] Step 3: Fetch and filter posts
- [ ] Step 4: Identify top creators and posts
- [ ] Step 5: Deliver UGC report or creator list
```

### Step 1: Find the Location ID

Instagram location tags use a numeric location ID, not a text name. To find it:

1. Search for the location on Instagram's mobile app
2. Open the location page — the URL format is: `instagram.com/explore/locations/[LOCATION_ID]/[location-name]/`
3. Copy the numeric `LOCATION_ID`

Alternatively, ask the user for the full Instagram location URL and extract the ID from it.

**If the user only has a name (e.g., "Eiffel Tower Paris"):**
Run a brief Google search for `site:instagram.com/explore/locations "[venue name]"` to find the location page URL and extract the ID.

### Step 2: Run the Actor


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~instagram-location-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~instagram-location-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~instagram-location-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~instagram-location-scraper"
Input:
{
  "locationIds": ["[LOCATION_ID]"],
  "maxItems": 100
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~instagram-location-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "locationIds": ["[LOCATION_ID]"],
    "maxItems": 100
  }'
```

Wait for `SUCCEEDED`. Fetch results.

### Step 3: Filter Posts

From dataset, extract per post:
- `url` — link to the post
- `caption` — post text
- `ownerUsername` — creator's handle
- `likesCount` — post likes
- `commentsCount` — post comments
- `timestamp` — when posted
- `isVideo` — true/false (Reels vs. photo)

Filter options (ask user which apply):
- **Date range** — only recent posts (e.g., last 90 days)
- **Min likes** — surface higher-quality posts (e.g., ≥50 likes)
- **Min followers of poster** — surface posts by creators with real audiences

### Step 4: Identify Top Content and Creators

Rank posts by likes + comments. Identify the top 10 posts for potential repost/feature.

For creators with multiple posts at the location, they're genuine fans — flag these for influencer outreach.

Calculate: unique creators vs. total posts (gives a repeat-visitor signal).

### Step 5: Format Report

## Output Format

```
# Instagram Location Content: [VENUE NAME]
Location ID: [ID] | Posts collected: [N] | Date: [DATE]

## Overview
Total posts at this location: [N] (based on sample)
Unique creators: [N]
Date range of posts: [oldest] – [newest]
Avg engagement per post: [N] likes + [N] comments

## Top 10 Posts (by Engagement)
| # | Creator | Likes | Comments | Date | Type | Post URL |
|---|---------|-------|----------|------|------|----------|
| 1 | @[handle] | [N] | [N]   | [date] | [Photo/Reel] | [url] |

## Top Creators at This Location
Creators who appear most frequently in location posts:
1. @[handle] — [N] posts here | [N] followers (if available)
2. @[handle] — [N] posts here
3. @[handle] — [N] posts here

## Caption Themes
Common topics in captions at this location:
- [Theme] (e.g., "date night", "anniversary") — [N] posts
- [Theme] (e.g., "work trip") — [N] posts

## Outreach Picks
Top creators whose content could be repurposed as UGC or who are strong partnership candidates:
1. @[handle] — [post URL] — "[caption excerpt]"
```

## Troubleshooting

**Location ID not found:** Some small venues aren't indexed as Instagram locations. Try a nearby landmark or the city as a backup.
**Very few posts:** Low-traffic venues may have limited location-tagged posts. Lower the min-likes filter.
**Posts from wrong location:** Instagram location matching can be imprecise for similarly-named venues. Review posts manually for the top results.

