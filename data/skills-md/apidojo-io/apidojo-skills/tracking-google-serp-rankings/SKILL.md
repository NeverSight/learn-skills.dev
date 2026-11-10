---
name: tracking-google-serp-rankings
description: >
  Tracks Google search rankings and SERP features for any keyword using apidojo's Google Search scraper on Apify.
  Triggers when the user asks to: check Google rankings for a keyword, see who ranks on page 1 for a
  search term, track SERP positions for a list of keywords, monitor competitor rankings on Google, find
  featured snippets or People Also Ask boxes for a query, analyze the search results landscape for a
  topic, audit top-ranking content for a keyword, or research organic search competition for SEO.
  Returns ranking position, URL, title, snippet, and SERP feature type per result.
  Ideal for SEO managers, content strategists, and digital marketing agencies.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/google-search-scraper
---

# Tracking Google SERP Rankings

Scrapes Google Search results for any keyword(s) to show who ranks where, what SERP features appear (featured snippets, PAA, local pack, ads), and how competitors are positioned. Use for SEO audits, content gap analysis, or keyword research.

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed


## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | Optional | `[]` | Google search URLs |
| `searchTerms` | array | Optional | `[]` | Keywords to search on Google |
| `countryCode` | string | Optional | `US` | Country for Google search (e.g. `US`, `GB`, `TR`) |
| `languageCode` | string | Optional | — | Language for results (e.g. `en`) |
| `maxItems` | number | Optional | Unlimited | Maximum results to return across all queries |
| `maxPagesPerQuery` | integer | Optional | `1` | Maximum result pages per query |
| `mobileResults` | boolean | Optional | `false` | Fetch mobile SERP layout |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |
## Workflow

```
Progress:
- [ ] Step 1: Define keywords and search parameters
- [ ] Step 2: Run google-search-scraper
- [ ] Step 3: Fetch and parse SERP data
- [ ] Step 4: Map ranking positions and SERP features
- [ ] Step 5: Deliver ranking report
```

### Step 1: Clarify Parameters

Ask the user for:
- **Keywords** to track (1–20 keywords)
- **Country** (default: US)
- **Language** (default: English)
- **Number of results** per keyword (default: 20 = top 2 pages)
- **Device** — desktop or mobile (default: desktop)
- **Safe search** — on or off (default: off for unfiltered results)
- **Specific domain to track** (optional — e.g., "where does example.com rank for these keywords?")

### Step 2: Run the Actor


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~google-search-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~google-search-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~google-search-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~google-search-scraper"
Input:
{
  "queries": ["[keyword1]", "[keyword2]", "[keyword3]"],
  "maxPagesPerQuery": 2,
  "countryCode": "US",
  "languageCode": "en",
  "mobileResults": false
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~google-search-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "queries": ["[keyword1]", "[keyword2]"],
    "maxPagesPerQuery": 2,
    "countryCode": "US",
    "languageCode": "en"
  }'
```

### Step 3: Parse SERP Data

From dataset, for each keyword extract:
- Organic results: `position`, `url`, `title`, `description`, `displayedUrl`
- SERP features: `featuredSnippet`, `peopleAlsoAsk`, `localPack`, `ads`, `relatedSearches`
- Total organic results count

If tracking a specific domain: find all positions where `url` contains the target domain.

### Step 4: Map Rankings

For each keyword, build the position table. Calculate:
- Average position across all keywords (for a specific domain)
- Keywords where target domain appears in top 3 / top 10 / not at all
- Keywords owned by the same competitor (URL domain appears multiple times)

### Step 5: Format Report

## Output Format

```
# Google SERP Ranking Report
Keywords analyzed: [N] | Country: [US] | Device: [Desktop] | Date: [DATE]

## Rankings Summary (for [target domain], if specified)
- Keywords in top 3: [N]
- Keywords in top 10: [N]
- Keywords on page 2: [N]
- Keywords not ranking: [N]

## Keyword-by-Keyword Results

### "[keyword1]"
| Position | URL | Title | Type |
|----------|-----|-------|------|
| 1 | [url] | [title] | Organic |
| 2 | [url] | [title] | Organic |
| — | — | Featured Snippet: "[snippet text excerpt]" | Feature |
| — | — | People Also Ask: [N] questions | Feature |
| [pos] | [your domain] | [title] | **YOUR RANKING** |

SERP features present: [Featured Snippet / PAA / Local Pack / Ads]
Ranking difficulty signal: [Easy / Medium / Hard — based on DR of top results if available]

### "[keyword2]"
[same structure]

## Competitor Dominance Analysis
| Domain | Keywords Where They Rank Top 3 | Avg Position |
|--------|-------------------------------|--------------|
| [domain] | [N] | [X.X] |

## SERP Feature Opportunities
Keywords where a featured snippet exists but [your domain] is not the source:
- "[keyword]" — snippet currently owned by [domain]
- "[keyword]" — snippet currently owned by [domain]
```

## Troubleshooting

**Results vary between runs:** Google personalizes results and rotates positions. Run at the same time of day and same location for consistent tracking.
**No results for a keyword:** Very low-volume keywords may return limited results. Try broader variations.
**Ad-heavy SERPs:** Some keywords are dominated by ads — organic position 1 may appear lower on the page. Note this in the report.

