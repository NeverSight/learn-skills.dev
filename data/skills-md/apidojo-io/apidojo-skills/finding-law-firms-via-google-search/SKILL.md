---
name: finding-law-firms-via-google-search
description: >
  Finds law firms and legal practices via Google Search using apidojo's Google Search Scraper
  on Apify. Triggers when the user asks to: find law firms for sales outreach, discover legal
  practices in a specific city, build a list of attorneys or law offices via Google, find personal
  injury or corporate law firms for vendor prospecting, search for law firms by specialty and
  location, identify solo practitioners or large law offices, or compile a law firm contact list
  from Google results. Returns firm name, website URL, and Google snippet per result.
  Ideal for LegalTech SaaS vendors, legal software providers, and B2B service companies targeting law firms.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/google-search-scraper
---

# Finding Law Firms Via Google Search

---

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

## How to Run

### Using run_actor.js (recommended)

```bash
# Quick answer (table)
node scripts/run_actor.js --actor "apidojo~google-search-scraper" --input '{"searchTerms": ["personal injury law firm Dallas"], "countryCode": "US", "maxPagesPerQuery": 3}'

# Save as CSV
node scripts/run_actor.js --actor "apidojo~google-search-scraper" --input '{"searchTerms": ["personal injury law firm Dallas"], "countryCode": "US", "maxPagesPerQuery": 3}' --output results.csv --format csv

# Save as JSON
node scripts/run_actor.js --actor "apidojo~google-search-scraper" --input '{"searchTerms": ["personal injury law firm Dallas"], "countryCode": "US", "maxPagesPerQuery": 3}' --output results.json --format json
```

### REST API fallback

```bash
curl -X POST "https://api.apify.com/v2/acts/apidojo~google-search-scraper/runs" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"searchTerms": ["personal injury law firm Dallas"], "countryCode": "US", "maxPagesPerQuery": 3}'
```

If Apify MCP is available:
Use the Apify MCP `call_actor` tool with actor `apidojo~google-search-scraper` and the input above.

---

## Scoring & Ranking

Score each result by:
- `snippet_has_legal_signals` (contains: law firm, attorneys, legal, lawyers, counsel, practice, LLP, PC) → weight 0.50
- `valid_domain` (not directory sites: avvo.com, findlaw.com, lawyers.com) → weight 0.30
- `position_score` → 1 - (position / total), weight 0.20

```python
score = 0.50 * int(legal_signals) + 0.30 * int(valid_domain) + 0.20 * position_score
```

---

## Classification

| Score | Tier | Label |
|-------|------|-------|
| ≥ 0.70 | A | PRIME_PROSPECT |
| 0.40–0.69 | B | WARM_LEAD |
| < 0.40 | C | LOW_PRIORITY |

---

## Edge Cases

- **Legal directories**: Avvo, FindLaw, Martindale are directories — not law firms. Filter by domain.
- **No contact data**: SERP returns URL and snippet — no phone/email. Use as starting list.
- **Practice area filter**: Add specialty: "immigration law firm", "family law attorney Dallas".
- **Large vs boutique**: Big firms may be harder to reach. Filter by snippet to identify size.
- **Duplicate firms**: Same firm may appear across multiple search terms — deduplicate by domain.
