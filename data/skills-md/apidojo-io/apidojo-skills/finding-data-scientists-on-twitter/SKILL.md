---
name: finding-data-scientists-on-twitter
description: >
  Finds data scientists and ML engineers to recruit using apidojo's Twitter scrapers on Apify.
  Triggers when the user asks to: find data scientists on Twitter for recruiting, discover machine learning engineers or AI researchers to hire from X, find data analysts or ML practitioners by specialization on Twitter, identify NLP computer vision or LLM engineers via social signals, find data science professionals open to work on Twitter, build a data science talent pipeline from social, or find researchers posting about job opportunities.
  Returns handle, name, ML specialty (from bio/tweets), stack (Python/R/TensorFlow), follower count, and open-to-work signals.
  Ideal for ML engineering hiring managers, AI research labs, and data-driven startups.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actors: apidojo/twitter-user-scraper, apidojo/tweet-scraper
---

# Finding Data Scientists And Ml Engineers on Twitter

Discovers data scientists and ML engineers on Twitter via skill keywords, portfolio/project signals, and open-to-work indicators. Twitter surfaces professionals who actively discuss their craft — a strong passive candidate signal.

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
- [ ] Step 1: Search for role-specific tweets
- [ ] Step 2: Collect unique handles
- [ ] Step 3: Enrich profiles
- [ ] Step 4: Score candidate fit
- [ ] Step 5: Deliver candidate list
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
  "searchTerms": ["data scientist", "ML engineer", "LLM engineer", "machine learning open to work"],
  "maxItems": 300,
  "tweetLanguage": "en"
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~tweet-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"searchTerms": ["data scientist", "ML engineer", "LLM engineer", "machine learning open to work"], "maxItems": 300}'
```

Collect unique `author.username` from results.

### Step 2: Enrich Profiles

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~twitter-user-scraper"
Input: {"usernames": ["[username1]", "[username2]", "..."]}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~twitter-user-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"usernames": ["handle1", "handle2"]}'
```

### Step 3: Filter and Score

**Skill confirmation:** bio contains keywords: "data science", "machine learning", "ML", "NLP", "LLM", "AI", "neural network", "PyTorch", "TensorFlow", "scikit-learn"

**research_signal = bio contains 'PhD', 'researcher', or links to papers/Google Scholar**

**Candidate score:**
```
candidate_score = (skill_confirmed ? 1 : 0) * 0.35
                + (open_to_work_signal ? 1 : 0) * 0.30
                + (followerCount in 200..20000 ? 1 : 0.6) * 0.20
                + (tweeted_in_last_30_days ? 1 : 0) * 0.15
```

Activity: active (< 30 days) | passive (30–90 days) | dormant (> 90 days)

### Step 4: Edge Cases

- **Company/brand accounts in results**: Filter where `followerCount > 50K` AND bio contains no personal pronouns; these are likely brand accounts
- **< 20 candidates found**: Broaden skill term; remove location or seniority filter; try adjacent skills
- **Bot detection**: Flag `followerCount / followingCount < 0.05` AND `tweetsCount < 20` as potential bot
- **Location not matching**: Bio location is free text — use fuzzy match; accept partial city/country names

## Output Format

```
# Data Scientists And Ml Engineers Candidates: [ML_SPECIALTY]
Profiles found: [N] | Open-to-work: [N] | Active: [N] | Date: [DATE]

## Priority: Open-to-Work Candidates
| Name | @Handle | Specialty | Location | Followers | Last Active | Score |
|------|---------|----------|---------|-----------|------------|-------|

## Passive Candidates
| Name | @Handle | Specialty | Location | Followers | Score |
|------|---------|----------|---------|-----------|-------|

## Bio Highlights (Top 5)
1. @[handle]: "[bio excerpt]"
```

## Troubleshooting

**All results are agencies/companies not individuals**: Add personal pronouns filter or search `"I am a [role]"`, `"I do [skill]"`.
**Role too generic returns too many results**: Add location OR seniority qualifier.
**No open-to-work signals**: Most candidates don't signal publicly — treat passive candidates as warm leads with personalized outreach referencing their recent content.

