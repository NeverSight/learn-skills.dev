---
name: tracking-hiring-signals-from-company-tweets
description: >
  Tracks hiring signals and growth indicators from company Twitter accounts using apidojo's Tweet
  scraper on Apify. Triggers when the user asks to: find companies that are actively hiring on
  Twitter, track job posting announcements from company accounts on X, identify startups that are
  growing based on their hiring tweets, find companies hiring for specific roles from their Twitter,
  monitor competitor hiring activity on social media, discover which companies are expanding teams
  in a specific sector, or build a list of companies actively hiring for your skill set.
  Returns company handle, role being hired, team/department signal, post date, and growth indicator.
  Ideal for job seekers, talent intelligence teams, VCs tracking portfolio growth, and competitor analysts.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/tweet-scraper
---

# Tracking Hiring Signals from Company Tweets

Monitors company Twitter accounts for hiring announcements and growth signals. Companies tweet about openings before jobs.page or LinkedIn posts go live — Twitter is an early signal channel.

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `searchTerms` | array | ✅ | `[]` | Twitter advanced search queries (e.g. `["#AI lang:en", "from:NASA"]`) |
| `sort` | string | Optional | `Top` | Sort order: `Latest`, `Top`, or `Latest+Top` |
| `tweetLanguage` | string | Optional | — | ISO 639-1 language code (e.g. `en`) |
| `maxItems` | number | Optional | Unlimited | Maximum tweets to return |
| `onlyVerifiedUsers` | boolean | Optional | `false` | Only tweets from verified users |
| `onlyTwitterBlue` | boolean | Optional | `false` | Only Twitter Blue subscribers |
| `onlyImage` | boolean | Optional | `false` | Only tweets with images |
| `onlyVideo` | boolean | Optional | `false` | Only tweets with videos |
| `onlyQuote` | boolean | Optional | `false` | Only quote tweets |
| `author` | string | Optional | — | Filter to a specific author handle |
| `inReplyTo` | string | Optional | — | Tweets replying to a specific handle |
| `mentioning` | string | Optional | — | Tweets mentioning a specific handle |
| `geotaggedNear` | string | Optional | — | Tweets near a location |
| `withinRadius` | string | Optional | — | Radius around geotaggedNear |
| `geocode` | string | Optional | — | Lat/lng + radius string |
| `placeObjectId` | string | Optional | — | Tweets tagged with a place |
| `minimumRetweets` | number | Optional | — | Minimum retweet count |
| `minimumFavorites` | number | Optional | — | Minimum like count |
| `minimumReplies` | number | Optional | — | Minimum reply count |
| `start` | string | Optional | — | Tweets after this date (YYYY-MM-DD) |
| `end` | string | Optional | — | Tweets before this date (YYYY-MM-DD) |
| `includeSearchTerms` | boolean | Optional | `false` | Add the matched search term to each tweet |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## Workflow

```
Progress:
- [ ] Step 1: Search for hiring-signal tweets in sector
- [ ] Step 2: (Optional) Scrape specific company accounts
- [ ] Step 3: Extract role and team info from tweet text
- [ ] Step 4: Score growth signal strength
- [ ] Step 5: Deliver hiring intelligence report
```

### Step 1: Search Hiring Signals


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~tweet-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~tweet-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~tweet-scraper" \
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
  "searchTerms": ["we're hiring [SECTOR]", "join our team [SECTOR]", "[ROLE] hiring [SECTOR]"],
  "maxItems": 300
}
```

**REST API fallback:**
```bash
curl -X POST   "https://api.apify.com/v2/acts/apidojo~tweet-scraper/runs?token=$APIFY_TOKEN"   -H "Content-Type: application/json"   -d '{
    "searchTerms": ["we are hiring fintech", "join our team SaaS startup", "software engineer hiring"],
    "maxItems": 300
  }'
```

### Step 2: Extract Role Signals from Tweet Text

```
role_mentioned = extract noun phrases after "hiring a/an", "looking for a/an", "seeking a"
team_mentioned = extract from: "engineering team", "sales team", "marketing", "product team"
urgency = "immediately", "ASAP", "urgent" → HIGH; "growing team" → MEDIUM; general → LOW
```

### Step 3: Growth Signal Score

```
hiring_signal_score = (is_confirmed_company_account ? 1 : 0.5) * 0.30
                    + (role_is_specific ? 1 : 0.5) * 0.25
                    + (post_is_recent: ≤7 days = 1, 8-14 = 0.7, 15-30 = 0.4) * 0.25
                    + (link_to_job_page ? 1 : 0) * 0.20
```

**Growth tier:** Multiple hiring tweets in 30 days = HIGH_GROWTH; 1-2 = STEADY_HIRE; no link = SIGNAL_ONLY

### Step 4: Edge Cases

- **Retweets from employee accounts**: If a company employee retweets a job post, keep — it's still a valid signal; note it's not the company's official account
- **Job boards posting on behalf of company**: Filter out accounts named "JobsAt[Company]", staffing agencies, or accounts posting > 10 hiring tweets/day (aggregators)
- **Role extraction fails**: Note the tweet verbatim and mark `role = "unspecified"` — still a growth signal
- **Same company posts 5 roles**: Deduplicate by `author.username`; count unique companies, not unique tweets

## Output Format

```
# Hiring Signal Intelligence: [SECTOR/ROLE]
Tweets analyzed: [N] | Companies with hiring signals: [N] | Date: [DATE]

## High-Growth Companies (Multiple Roles Posted)
| Company | @Handle | Roles Mentioned | Teams | Posts | Link to Jobs | Score |
|---------|---------|----------------|-------|-------|-------------|-------|
| [name] | @[handle] | [role list] | [eng/mktg] | [N] | [Yes/No] | [0.XX] |

## Single Hire Signals
| Company | @Handle | Role | Team | Tweet Date | Job Link |
|---------|---------|------|------|-----------|---------|

## Role Distribution Across All Companies
| Role Category | # Companies Hiring | Urgency |
|--------------|-------------------|---------|
| Engineering | [N] | [High/Med] |
| Marketing | [N] | |
| Sales | [N] | |
```

## Troubleshooting

**Results dominated by job boards**: Add negative terms to search: `-jobs -jobboard -staffing -recruiting`
**Sector too broad**: Narrow with a sub-sector or specific stage: "Series A fintech" instead of "fintech".
**Job links are broken/expired**: Hiring tweets are posted in real-time; check within 48h for best link validity.

