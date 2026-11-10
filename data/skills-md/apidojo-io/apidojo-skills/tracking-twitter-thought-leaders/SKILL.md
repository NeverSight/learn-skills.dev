---
name: tracking-twitter-thought-leaders
description: >
  Identifies and tracks thought leaders and key voices in any industry on Twitter/X using apidojo's scrapers.
  Triggers when the user asks to: find the top voices in an industry on Twitter, identify thought leaders
  in a niche, discover who has the most influence in a topic area on X, find experts tweeting about
  a subject, build a list of influencers to engage with on Twitter, track who is gaining followers
  fastest in a category, or identify key opinion leaders in a field for PR or partnership outreach.
  Returns name, handle, follower count, engagement rate, bio keywords, and recent top tweets.
  Ideal for PR teams, community managers, and B2B content marketers.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actors: apidojo/twitter-user-scraper, apidojo/tweet-scraper
---

# Tracking Twitter Thought Leaders

Finds Twitter/X accounts with genuine influence in a topic area — not just high follower counts, but accounts whose tweets get shared and discussed. Delivers a ranked list for PR outreach, community engagement, or partnership targeting.

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
- [ ] Step 1: Define topic, industry, and influence criteria
- [ ] Step 2: Search for topic-relevant tweets to find active voices
- [ ] Step 3: Enrich top accounts with profile data
- [ ] Step 4: Score by influence signals
- [ ] Step 5: Deliver ranked thought leader list
```

### Step 1: Clarify Parameters

Ask the user for:
- **Topic or industry** (e.g., "AI safety", "B2B SaaS growth", "climate tech")
- **Influence type** — broad reach (high followers), community depth (high engagement), or rising voices (growing fast)
- **Follower range** (default: 5,000–2,000,000 — excludes unknown accounts and mega-celebrities)
- **Geography/language** (optional)
- **List size** (default: 25)

### Step 2: Search for Topic Tweets

Find who's actively tweeting about the topic — recent activity matters more than old follower counts.


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
  "searchTerms": ["[TOPIC_KEYWORD_1]", "[TOPIC_KEYWORD_2]", "[TOPIC_KEYWORD_3]"],
  "maxItems": 300,
  "tweetLanguage": "en"
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~tweet-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "searchTerms": ["[TOPIC_KEYWORD_1]", "[TOPIC_KEYWORD_2]"],
    "maxItems": 300
  }'
```

Extract unique `author.username` values from all results. Sort by their tweet's retweet+like count — accounts whose topic tweets get the most engagement are the most influential voices.

### Step 3: Enrich with Profile Data

Take top 100 candidate usernames. Fetch full profiles.

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~twitter-user-scraper"
Input:
{
  "usernames": ["[username1]", "[username2]", "...up to 100"]
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~twitter-user-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"usernames": ["[username1]", "[username2]"]}'
```

### Step 4: Score by Influence

Calculate composite influence score for each account:

```
topic_engagement = avg(likes + retweets) on topic-related tweets
audience_quality = followers / following ratio (>1 is healthy)
influence_score = topic_engagement * log(followers) * audience_quality
```

Filter: keep only accounts within follower range AND whose bio suggests topical relevance.

### Step 5: Format Output

## Output Format

```
# Twitter Thought Leaders: [TOPIC/INDUSTRY]
Accounts analyzed: [N] | Final list: [N] | Date: [DATE]

## Top Thought Leaders

| # | Name | @Handle | Followers | Influence Score | Bio Excerpt | Recent Top Tweet |
|---|------|---------|-----------|-----------------|-------------|------------------|
| 1 | [name] | @[handle] | [N] | [score] | [bio] | "[tweet excerpt]" |

## Tier Breakdown

### 🏆 Power Voices (500K+ followers)
[list with brief bio and latest relevant tweet]

### 🎯 Core Influencers (50K–500K followers)
[list — best for outreach: big enough to matter, accessible enough to respond]

### 🌱 Rising Voices (5K–50K followers)
[list — early partnership opportunity, lower cost, high engagement]

## Best Accounts for Direct Outreach
[Top 5 picks with rationale — why they're ideal for PR, partnership, or co-content]

## Content Themes These Voices Tweet About
- [Theme 1]: [N] of the accounts tweet regularly about this
- [Theme 2]: [N] accounts
```

## Troubleshooting

**Results dominated by one person:** Some topics have one mega-voice. Exclude them and surface the next tier.
**Not enough topically relevant accounts:** Expand keyword list with synonyms, adjacent topic terms, and industry jargon.
**Follower counts seem off:** Cached data — for final list, spot-check top 5 accounts directly on Twitter.

