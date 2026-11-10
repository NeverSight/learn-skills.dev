---
name: discovering-brand-ambassadors-across-platforms
description: >
  Discovers potential brand ambassadors across Instagram TikTok and Twitter using apidojo's scrapers. Triggers when the user asks to: find brand ambassadors across multiple platforms, discover cross-platform creators for brand ambassador programs, find creators who would make good ambassadors across social media, identify multi-platform influencers for ambassador recruitment, find creators with audiences on multiple platforms for a brand partnership, build a multi-platform brand ambassador pipeline, or discover creators with authentic brand affinity across channels.
  Returns creator handle per platform, combined reach estimate, brand affinity signals, engagement metrics, and ambassador tier.
  Ideal for brand partnership teams, DTC brands, and ambassador program managers needing multi-channel reach.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actors: apidojo/instagram-scraper, apidojo/tiktok-scraper, apidojo/twitter-user-scraper
---

# Discovering Brand Ambassadors Across Platforms

Executes discovering brand ambassadors across platforms using apidojo scrapers. Part of the apidojo intelligence skills library.

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | ✅ | `[]` | Instagram URLs — profiles, hashtags, locations, audio pages, reels |
| `until` | string | Optional | — | Scrape posts until this date (YYYY-MM-DD) |
| `maxItems` | number | Optional | Unlimited | Maximum posts to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## Workflow

```
Progress:
- [ ] Step 1: Define parameters
- [ ] Step 2: Run instagram-scraper
- [ ] Step 3: Filter and classify results
- [ ] Step 4: Score by quality and relevance
- [ ] Step 5: Deliver output
```

### Step 2: Run the Actor


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~instagram-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~instagram-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~instagram-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~instagram-scraper"
Input:
{
  "searchTerms": ["#[brand]", "#[brand]ambassador", "#[brand]fam"],
  "maxItems": 100
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~instagram-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"searchTerms": ["#[brand]", "#[brand]ambassador", "#[brand]fam"], "maxItems": 100}'
```

Wait for `SUCCEEDED`. Fetch dataset:
```bash
curl "https://api.apify.com/v2/actor-runs/$RUN_ID/dataset/items?token=$APIFY_TOKEN"
```

### Step 3: Classify Results

```
classification: MEGA (combined reach > 500K) | MACRO (100K-500K) | MICRO (10K-100K) | NANO (1K-10K)
```

### Step 4: Score Each Result

```
score = combined_reach = IG_followers + TikTok_followers * 0.8 + Twitter_followers * 0.5  # platform-weighted
```

### Step 5: Edge Cases

- **The same creator on multiple platforms often has very different audience sizes per platform — list per-platform stats separately, don't just sum**

Additional fallbacks:
- **< 20 results**: Broaden search terms; remove secondary filters
- **No results**: Verify the search terms are correct; try alternate phrasings
- **Data quality issues**: Remove entries with missing key fields; note count in output

## Output Format

```
# Discovering Brand Ambassadors Across Platforms
Results: [N] | Date: [DATE]

| # | [Key Field] | [Metric 1] | [Metric 2] | [Classification] | [Score] |
|---|------------|-----------|-----------|-----------------|---------|
| 1 | [value] | [value] | [value] | [type] | [0.XX] |

## Summary
Top result: [description]
Key finding: [insight]
```

## Troubleshooting

**Too few results:** Broaden the primary search term; remove restrictive filters.
**Low quality results:** Apply minimum score threshold (≥ 0.50) to filter noise.
**Actor fails to run:** Verify API key; check actor status at apify.com/apidojo.

