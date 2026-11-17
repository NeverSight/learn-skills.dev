---
name: extracting-google-paa-questions-for-seo
description: >
  Extracts Google People Also Ask questions for SEO content planning using apidojo's Google Search
  scraper on Apify. Triggers when the user asks to: find People Also Ask questions on Google for
  SEO, extract PAA questions for keyword research, discover what questions Google shows for a topic,
  find long-tail SEO questions from Google, research FAQ content opportunities from Google SERP,
  build a list of questions to answer in blog content from Google, or extract Google autocomplete
  and PAA data for content planning.
  Returns PAA questions, SERP position, related keywords, and content structure recommendations.
  Ideal for SEO strategists, content writers, and blog editors building search-optimized content.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/google-search-scraper
---

# Extracting Google PAA Questions for SEO

Pulls People Also Ask (PAA) questions from Google SERPs for a target keyword. PAA questions are Google-validated signals of what real users want to know — use them as H2/H3 headings or FAQ sections in content.

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
- [ ] Step 1: Run google-search-scraper for keyword and variants
- [ ] Step 2: Extract PAA questions from results
- [ ] Step 3: Classify questions by search intent
- [ ] Step 4: Score content opportunity per question
- [ ] Step 5: Deliver SEO content brief
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
  "queries": ["[KEYWORD]", "best [KEYWORD]", "how to [KEYWORD]", "[KEYWORD] for beginners"],
  "maxPagesPerQuery": 3,
  "countryCode": "US",
  "languageCode": "en",
  "includePeopleAlsoAsk": true
}
```

**REST API fallback:**
```bash
curl -X POST   "https://api.apify.com/v2/acts/apidojo~google-search-scraper/runs?token=$APIFY_TOKEN"   -H "Content-Type: application/json"   -d '{
    "queries": ["email marketing tools", "best email marketing tools", "how to email marketing"],
    "maxPagesPerQuery": 3,
    "countryCode": "US",
    "includePeopleAlsoAsk": true
  }'
```

### Step 2: Classify PAA Questions by Intent

```
intent:
  INFORMATIONAL = "what is", "how does", "what does", "explain"
  COMPARATIVE = "vs", "or", "better", "difference between"
  TRANSACTIONAL = "how to buy", "where to get", "best price", "free"
  NAVIGATIONAL = "[brand] how to", "login", "sign up"
  TROUBLESHOOTING = "not working", "error", "fix", "issue"
```

### Step 3: Score Content Opportunity

```
paa_score = (question_appears_across_multiple_keywords ? 1 : 0.5) * 0.35
          + (intent == INFORMATIONAL ? 1 : 0.7) * 0.30
          + (current_SERP_has_no_featured_snippet ? 1 : 0.4) * 0.35
```

**Featured snippet opportunity:** if PAA answer shown is > 200 words or from a weak domain → high opportunity to claim.

### Step 4: Edge Cases

- **PAA questions not returned**: Some queries return no PAA boxes; try more question-form queries ("how to [keyword]", "what is [keyword]")
- **Duplicate questions across keywords**: Deduplicate by question text similarity (≥ 80% overlap = same question); count as one, note it appeared for [N] keywords
- **Questions are too broad**: Flag as `BROAD_QUESTION` — better suited for a pillar page or FAQ section, not a standalone post
- **Questions are brand-specific competitors**: Include with `COMPETITIVE_INTELLIGENCE` flag — these tell you what users are asking about your competitors

## Output Format

```
# Google PAA Questions: "[KEYWORD]"
Queries run: [N] | Unique PAA questions: [N] | Featured snippet opportunities: [N] | Date: [DATE]

## PAA Question Bank (Sorted by Opportunity Score)
| # | Question | Intent | Appears For | Featured Snippet? | Score |
|---|---------|--------|------------|------------------|-------|
| 1 | "[question]" | INFORMATIONAL | [N] keywords | No | [0.XX] |

## High-Priority Questions (Use as H2/H3 in Content)
1. "[question]" — Answer in [X] words; [informational guide / comparison table / step-by-step]
2. "[question]"

## FAQ Section Builder
Questions suitable for FAQ schema markup:
1. Q: "[question]" — A: [1-sentence answer start]

## Content Angle Recommendations
- For "[primary keyword]" blog post: Use [N] of these PAA questions as headers
- For FAQ page: [N] questions qualify for FAQ schema
- For comparison page: [N] vs/comparison questions found
```

## Troubleshooting

**"includePeopleAlsoAsk" returns no results**: Not all keywords trigger PAA boxes. Try adding "how", "why", "best", "what" as prefixes to force question-form SERPs.
**PAA questions are all branded (competitor names)**: High competitor brand presence on SERPs — separate branded vs. non-branded question sets in your content plan.
**Questions are too obscure**: PAA expands dynamically based on prior searches — the questions returned reflect real user journeys; trust them even if obscure.

