---
name: finding-podcast-hosts-for-outreach
description: >
  Finds podcast hosts for PR and guest outreach using apidojo's Twitter scrapers on Apify.
  Triggers when the user asks to: find podcast hosts to pitch for a guest spot, discover podcasters
  in a niche for PR outreach, build a podcast outreach list from Twitter, find podcast hosts who
  cover a specific topic or industry, identify podcasters who interview guests in a business niche,
  find B2B podcast hosts for thought leadership placement, or compile a list of podcast hosts
  for a media relations campaign.
  Returns podcast host handle, show name, topic focus, follower count, and audience size signals.
  Ideal for PR agencies, executives doing thought leadership, authors, and startup founders.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actors: apidojo/twitter-user-scraper, apidojo/tweet-scraper
---

# Finding Podcast Hosts for Outreach

Discovers podcast hosts on Twitter by episode announcements, guest mentions, and show promotion signals.

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
- [ ] Step 1: Search for podcast announcement tweets
- [ ] Step 2: Collect unique host handles
- [ ] Step 3: Enrich host profiles
- [ ] Step 4: Score outreach priority
- [ ] Step 5: Deliver podcast outreach list
```

### Step 1: Search Queries


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
Actor: "apidojo~tweet-scraper"
Input:
{
  "searchTerms": ["[TOPIC] podcast", "new episode [TOPIC]", "podcast host [TOPIC]"],
  "maxItems": 300
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~tweet-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"searchTerms": ["entrepreneurship podcast", "new episode startup"], "maxItems": 300}'
```

### Step 2: Enrich and Filter

Run `apidojo~twitter-user-scraper` on handles. Keep profiles where bio contains "podcast", "host", "show", "episodes".

**Guest format:** bio or tweets mention "guest", "interview", "this week's guest" → `has_guest_format = true`

### Step 3: Score Outreach Priority

```
outreach_score = (has_guest_format ? 1 : 0.3) * 0.35
               + (tweeted_episode_in_last_30_days ? 1 : 0) * 0.25
               + (followerCount in 1000..100000 ? 1 : 0.6) * 0.25
               + (topic_alignment: strong=1, weak=0.5) * 0.15
```

### Step 4: Edge Cases

- **Account shares content but is not host**: Verify bio says "host" — some accounts share show content without hosting
- **Show name not findable**: Note as `show_name_unknown`; LinkedIn search needed
- **Large media company podcast**: Flag as `PREMIUM_PLACEMENT` — A-list guests only

## Output Format

```
# Podcast Host Outreach List: [TOPIC]
Hosts found: [N] | Guest-format: [N] | Active: [N] | Date: [DATE]

## Priority (Guest-Format + Active + Mid-Tier)
| Host | @Handle | Show | Followers | Last Episode | Score |
|------|---------|------|-----------|-------------|-------|

## Small Shows (Easier to Land)
| Host | @Handle | Followers | Last Active |
|------|---------|-----------|------------|

## Personalization Tip
Reference the host's most recent episode topic in your pitch — hosts receive dozens of pitches, relevance is the strongest differentiator.
```

## Troubleshooting

**Results include listeners not hosts**: Require "podcast host" OR "host of [show]" in bio.
**No show found on Twitter**: Supplement with Spotify/Apple Podcasts search.
**Host inactive > 60 days**: Flag as potentially on hiatus; verify before pitching.

