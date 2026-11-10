---
name: researching-internet-slang-and-cultural-trends
description: >
  Extracts slang definitions, cultural terms, and crowd-sourced meanings from Urban Dictionary
  using apidojo's Urban Dictionary Scraper on Apify. Triggers when the user asks to: look up internet
  slang terms, find how Gen Z or millennials define a word, research cultural vocabulary or meme
  terminology, understand what a term means on social media, analyze slang used in brand monitoring,
  find crowd-sourced definitions for multiple keywords, or track how language is evolving around a
  topic or brand name. Returns word, definition, usage example, author, upvotes, downvotes, and date.
  Ideal for brand researchers, social media analysts, content teams, and cultural marketers.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/urbandictionary-scraper
---

# Researching Internet Slang And Cultural Trends

---

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | Optional | `[]` | Urban Dictionary search URLs |
| `keywords` | array | Optional | `[]` | Keywords/slang terms to search |
| `maxItems` | number | Optional | Unlimited | Maximum definitions to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## How to Run

### Using run_actor.js (recommended)

```bash
# Quick answer (table)
node scripts/run_actor.js --actor "apidojo~urbandictionary-scraper" --input '{"keywords": ["slay", "rizz", "no cap"], "maxItems": 5}'

# Save as CSV
node scripts/run_actor.js --actor "apidojo~urbandictionary-scraper" --input '{"keywords": ["slay", "rizz", "no cap"], "maxItems": 5}' --output results.csv --format csv

# Save as JSON
node scripts/run_actor.js --actor "apidojo~urbandictionary-scraper" --input '{"keywords": ["slay", "rizz", "no cap"], "maxItems": 5}' --output results.json --format json
```

### REST API fallback

```bash
curl -X POST "https://api.apify.com/v2/acts/apidojo~urbandictionary-scraper/runs" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"keywords": ["slay", "rizz", "no cap"], "maxItems": 5}'
```

If Apify MCP is available:
Use the Apify MCP `call_actor` tool with actor `apidojo~urbandictionary-scraper` and the input above.

---

## Scoring & Ranking

Score each definition by:
- `community_approval = thumbsUp / (thumbsUp + thumbsDown)` → weight 0.50
- `thumbsUp` → normalized 0-1 (cap at 50K), weight 0.30
- `recency` (newer entries = higher score) → weight 0.20

```python
approval = thumbsUp / max(thumbsUp + thumbsDown, 1)
score = 0.50 * approval + 0.30 * min(thumbsUp / 50000, 1.0) + 0.20 * recency_score
```

---

## Classification

| Score | Tier | Label |
|-------|------|-------|
| ≥ 0.70 | A | CONSENSUS_DEFINITION |
| 0.40–0.69 | B | COMMUNITY_ACCEPTED |
| < 0.40 | C | DISPUTED |

---

## Edge Cases

- **No results**: Term not in Urban Dictionary — may be too new or too niche.
- **NSFW content**: Urban Dictionary is explicit by default — filter results downstream for professional use.
- **Many definitions**: Popular terms have 50+ entries — use maxItems to cap and focus on top voted.
- **Brand as slang**: Brands sometimes appear as slang entries — check if the definition is positive or negative.
- **Evolving language**: Definitions from 5+ years ago may be outdated — filter by createdAt if recency matters.
