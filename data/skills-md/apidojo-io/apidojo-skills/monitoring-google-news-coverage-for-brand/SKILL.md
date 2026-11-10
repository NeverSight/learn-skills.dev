---
name: monitoring-google-news-coverage-for-brand
description: >
  Monitors Google News coverage for a brand using apidojo's Google Search scraper on Apify.
  Triggers when the user asks to: track news coverage about a brand on Google, monitor press
  mentions in Google News, find recent news articles mentioning a company, track media coverage
  for a brand or executive, monitor competitor news coverage, find press releases or news stories
  about a brand on Google, or research how a company is being covered in the press.
  Returns article title, publication, date, URL, and coverage sentiment per article.
  Ideal for PR agencies, communications teams, brand managers, and reputation monitoring services.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/google-search-scraper
---

# Monitoring Google News Coverage for a Brand

Tracks press and media coverage of a brand across Google News. Identifies publications, volume, sentiment, and stories that need PR attention.

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
- [ ] Step 1: Search Google News for brand + time filter
- [ ] Step 2: Classify editorial vs. press release
- [ ] Step 3: Classify coverage sentiment
- [ ] Step 4: Identify top publications and story themes
- [ ] Step 5: Deliver press monitoring report
```

### Step 1: Run google-search-scraper


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
  "queries": ["\"[BRAND_NAME]\" news", "[BRAND_NAME] announcement"],
  "maxPagesPerQuery": 3,
  "countryCode": "US",
  "searchType": "news"
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~google-search-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"queries": ["\"[BRAND_NAME]\" news"], "maxPagesPerQuery": 3, "searchType": "news"}'
```

### Step 2: Classify Coverage

```
coverage_type:
  PRESS_RELEASE = domain: prnewswire, businesswire, globenewswire
  EDITORIAL = major publication (TechCrunch, Forbes, WSJ, Bloomberg)
  TRADE = industry publication
  NEGATIVE_FLAG = title contains: "lawsuit", "scandal", "fraud", "investigation"

sentiment_from_headline:
  POSITIVE = "raises", "launches", "wins", "grows", "partners", "expands"
  NEGATIVE = "cuts", "loses", "sued", "drops", "fails", "controversy"
```

### Step 3: Edge Cases

- **Brand name is common word**: Use exact match quotes; add qualifier
- **Old coverage returned**: Use `after:[DATE]` query operator
- **Negative from major publication**: Flag as `PR_ATTENTION_NEEDED`
- **Competitor coverage much higher volume**: PR gap analysis signal

## Output Format

```
# Google News Monitor: [BRAND_NAME]
Period: [DATE_RANGE] | Articles: [N] | Publications: [N] | Date: [DATE]

Coverage: Editorial [N] | Press Releases [N] | Negative flags [N]
Sentiment: [X%] Positive | [X%] Negative | [X%] Neutral

## Headlines (Chronological)
| Date | Publication | Headline | Type | Sentiment | URL |
|------|------------|---------|------|-----------|-----|

## ⚠️ PR Attention Needed
[Negative articles requiring monitoring]
```

## Troubleshooting

**Too few results**: Brand has limited press; try without quotes for broader matching.
**Reviews not press in results**: Add `-site:yelp.com -site:glassdoor.com` to queries.
**Google blocks news search**: Use `searchType: "web"` with news-domain anchors.

