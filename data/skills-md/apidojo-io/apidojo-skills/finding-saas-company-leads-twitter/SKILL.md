---
name: finding-saas-company-leads-twitter
description: >
  Finds SaaS companies and software startup leads from Twitter/X using apidojo's Twitter scrapers on Apify.
  Triggers when the user asks to: find SaaS companies on Twitter for partnership or sales outreach,
  build a list of software startups by vertical, find B2B SaaS founders or decision-makers on X,
  identify early-stage software companies by their Twitter activity, discover SaaS products in a
  specific niche from Twitter, find software vendors posting about product launches or fundraising,
  or compile a SaaS company contact list from social media.
  Returns company handle, founder name (from bio), follower count, product description, and recent tweets.
  Ideal for SaaS integration partners, investor outreach, B2B sales teams, and startup press.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actors: apidojo/twitter-user-scraper, apidojo/tweet-scraper
---

# Finding SaaS Company Leads on Twitter

Discovers SaaS companies and software product accounts via Twitter signals — product launches, feature announcements, founder activity, and niche-specific hashtags. Twitter is where early-stage B2B SaaS companies are most active before establishing a formal web presence.

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
- [ ] Step 1: Build keyword and hashtag search list for vertical
- [ ] Step 2: Run tweet-scraper to find active companies
- [ ] Step 3: Extract unique company handles
- [ ] Step 4: Enrich via twitter-user-scraper
- [ ] Step 5: Score and classify by stage
- [ ] Step 6: Deliver lead list
```

### Step 1: Search Keywords

Build from vertical. Example for "project management SaaS":
```
Keywords: ["project management software", "PM tool", "#pmtools", "task management SaaS",
           "launched a product", "we built", "try our tool", "project management app"]
```

Standard SaaS signal phrases (always include):
```
["just launched", "we built", "our product", "sign up free", "#buildinpublic",
 "new feature", "we're hiring", "Series A", "product update", "[vertical] tool"]
```

### Step 2: Run tweet-scraper


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
  "searchTerms": ["[VERTICAL] software", "[VERTICAL] SaaS", "[VERTICAL] tool launch", "we built [VERTICAL]"],
  "maxItems": 300,
  "tweetLanguage": "en"
}
```

**REST API fallback:**
```bash
curl -X POST   "https://api.apify.com/v2/acts/apidojo~tweet-scraper/runs?token=$APIFY_TOKEN"   -H "Content-Type: application/json"   -d '{
    "searchTerms": ["HR tech SaaS", "HR software launch", "we built HR tool"],
    "maxItems": 300
  }'
```

Collect unique `author.username` values.

### Step 3: Enrich Profiles

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~twitter-user-scraper"
Input:
{
  "usernames": ["[username1]", "[username2]", "...up to 100 usernames"]
}
```

**REST API fallback:**
```bash
curl -X POST   "https://api.apify.com/v2/acts/apidojo~twitter-user-scraper/runs?token=$APIFY_TOKEN"   -H "Content-Type: application/json"   -d '{"usernames": ["handle1", "handle2"]}'
```

### Step 4: Filter and Classify

**Is a SaaS company?** Keep if bio contains:
- Product keywords: "software", "SaaS", "platform", "app", "tool", "API", "dashboard"
- Launch signals: "try", "sign up", "free trial", "beta"
- Funding signals: "backed by", "YC", "Techstars", "seed", "Series A/B"

**Stage classification from followerCount:**
```
early: followerCount < 1,000
growing: 1,000–10,000
established: > 10,000
```

**Company score:**
```
lead_score = (is_saas_signal ? 1 : 0) * 0.40
           + (has_website ? 1 : 0) * 0.25
           + (tweeted_in_last_30_days ? 1 : 0) * 0.20
           + min(followerCount / 5000, 1) * 0.15
```

### Step 5: Edge Cases

- **Personal accounts return instead of company**: Filter — prefer accounts where `name` != `username` and bio describes a product; deprioritize accounts with personal pronouns in bio ("I build...")
- **< 20 companies found**: Widen vertical keywords; try hashtags `#buildinpublic`, `#indiehacker`, `#saas` directly
- **Duplicate company** (founder + company account both found): Keep company account; link to founder handle as contact

## Output Format

```
# SaaS Company Leads: [VERTICAL]
Companies found: [N] | Early: [N] | Growing: [N] | Established: [N] | Date: [DATE]

## Growing-Stage Companies (Best Outreach Window)
| Company | Handle | Product | Stage | Followers | Website | Score |
|---------|--------|---------|-------|-----------|---------|-------|
| [name] | @[handle] | [1-line description from bio] | Growing | [N] | [url] | [0.XX] |

## Early-Stage (High Receptivity)
| Company | Handle | Product | Followers | Last Active |
|---------|--------|---------|-----------|------------|

## Established (Formal Sales Cycle)
| Company | Handle | Product | Followers | Website |
|---------|--------|---------|-----------|---------|
```

## Troubleshooting

**Results are mostly personal accounts:** Add `"software" OR "app" OR "platform"` to search and filter aggressively by bio keywords.
**Vertical too broad (returns 500+ companies):** Narrow to a sub-vertical (e.g., "project management" → "async project management for remote teams").
**Companies inactive (last tweet > 60 days):** Flag as potentially dormant; cross-reference product website for active status.

