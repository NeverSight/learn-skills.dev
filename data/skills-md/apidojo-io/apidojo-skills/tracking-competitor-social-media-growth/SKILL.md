---
name: tracking-competitor-social-media-growth
description: >
  Tracks and compares competitor follower growth across social platforms using apidojo's scrapers on Apify.
  Triggers when the user asks to: compare competitor social media growth, track how fast a competitor is
  growing on Twitter, TikTok, or Instagram, benchmark social media performance against competitors,
  monitor competitor follower counts over time, analyze a competitor's social media strategy, build a
  competitive social media analysis report, or see which competitor is winning on social.
  Returns platform, handle, follower count, growth indicators, and engagement benchmarks per competitor.
  Ideal for competitive intelligence analysts, CMOs, and growth strategy teams.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actors: apidojo/twitter-user-scraper, apidojo/tiktok-profile-scraper, apidojo/instagram-scraper
---

# Tracking Competitor Social Media Growth

Pulls current follower counts and engagement metrics for competitor accounts across Twitter/X, TikTok, and Instagram. Creates a side-by-side competitive snapshot. Designed to be run on a schedule for ongoing tracking.

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed


## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | Optional | `[]` | Twitter profile or tweet URLs |
| `twitterHandles` | array | Optional | `[]` | Twitter usernames (without @) |
| `twitterUserIds` | array | Optional | `[]` | Twitter user IDs |
| `getFollowers` | boolean | Optional | `false` | Extract follower lists |
| `getFollowing` | boolean | Optional | `false` | Extract following lists |
| `getRetweeters` | boolean | Optional | `false` | Extract retweeters of a tweet URL |
| `includeUnavailableUsers` | boolean | Optional | `false` | Include unavailable/suspended users |
| `maxItems` | number | Optional | Unlimited | Maximum users to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |
## Workflow

```
Progress:
- [ ] Step 1: Define competitors and target platforms
- [ ] Step 2: Scrape Twitter/X profiles
- [ ] Step 3: Scrape TikTok profiles
- [ ] Step 4: Scrape Instagram profiles
- [ ] Step 5: Compile cross-platform comparison
```

### Step 1: Clarify Parameters

Ask the user for:
- **Competitor handles per platform** — e.g.:
  - Twitter: `@competitorA`, `@competitorB`
  - TikTok: `@competitorA`, `@competitorB`
  - Instagram: `@competitorA`, `@competitorB`
- **Platforms to analyze** (Twitter, TikTok, Instagram — one or all)
- **Include your own account?** (default: yes — for direct benchmarking)

### Step 2: Scrape Twitter/X Profiles


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~twitter-user-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~twitter-user-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~twitter-user-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~twitter-user-scraper"
Input:
{
  "usernames": ["[handle1]", "[handle2]", "[handle3]", "[your_handle]"]
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~twitter-user-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"usernames": ["[handle1]", "[handle2]"]}'
```

Key fields to extract: `followersCount`, `followingCount`, `statusesCount`, `createdAt`, `verified`.

### Step 3: Scrape TikTok Profiles

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~tiktok-profile-scraper"
Input:
{
  "usernames": ["[handle1]", "[handle2]", "[handle3]"]
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~tiktok-profile-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"usernames": ["[handle1]", "[handle2]"]}'
```

Key fields: `fans` (followers), `heart` (total likes), `video` (video count), `diggCount`.

### Step 4: Scrape Instagram Profiles

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~instagram-scraper"
Input:
{
  "usernames": ["[handle1]", "[handle2]"],
  "maxItems": 12
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~instagram-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"usernames": ["[handle1]", "[handle2]"], "maxItems": 12}'
```

Key fields: `followersCount`, `followsCount`, `postsCount`, `biography`.

### Step 5: Compile Report

Calculate engagement rate per account per platform. Compare all on one view.

## Output Format

```
# Competitive Social Media Analysis
Competitors: [N] | Platforms: [list] | Date: [DATE]

## Cross-Platform Follower Summary

| Competitor | Twitter Followers | TikTok Followers | Instagram Followers | Total Reach |
|------------|-------------------|------------------|---------------------|-------------|
| [Your Brand] | [N]             | [N]              | [N]                 | [N]         |
| Competitor A | [N]             | [N]              | [N]                 | [N]         |
| Competitor B | [N]             | [N]              | [N]                 | [N]         |

## Platform-by-Platform Analysis

### Twitter/X
| Account | Followers | Following | Tweets | Eng. Rate | Verified |
|---------|-----------|-----------|--------|-----------|----------|
| @[handle] | [N]     | [N]       | [N]    | [X.X%]    | [Y/N]    |
**Leader:** [handle] with [N] followers | **Most engaged:** [handle] at [X.X%]

### TikTok
| Account | Followers | Total Likes | Videos | Avg Views |
|---------|-----------|-------------|--------|-----------|
| @[handle] | [N]     | [N]         | [N]    | [N]       |
**Leader:** [handle] | **Most viral:** [handle]

### Instagram
| Account | Followers | Posts | Avg Likes | Eng. Rate |
|---------|-----------|-------|-----------|-----------|
| @[handle] | [N]     | [N]   | [N]       | [X.X%]    |

## Key Takeaways
1. [Competitor] is winning on [platform] — [brief insight]
2. [Your brand] has [strength/gap] on [platform]
3. Biggest opportunity: [specific platform + action]
```

## Setting Up Recurring Tracking

To track growth over time, run this skill weekly and store the output. The delta between runs shows growth velocity. For automated weekly tracking, use a scheduled task to run this skill every Monday at 9am.

## Troubleshooting

**Missing platform handles:** Ask the user to provide handles per platform — they often differ from brand name.
**One platform returns no data:** Private accounts or accounts that don't exist on that platform. Confirm handle accuracy.

