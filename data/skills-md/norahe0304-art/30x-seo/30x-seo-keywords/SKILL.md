---
name: 30x-seo-keywords
description: >
  Comprehensive keyword research and analysis using DataForSEO API. Discover keyword
  opportunities, analyze search volume and difficulty, find related keywords, track
  rankings, and identify content gaps. Use when user says "keywords", "keyword research",
  "search volume", "keyword difficulty", "ranking keywords", "keyword ideas",
  "keyword suggestions", or "content gap".
allowed-tools:
  - Bash
  - Read
---

# SEO Keywords Analysis

Comprehensive keyword research and analysis using DataForSEO API via direct curl calls.

## API Configuration

Credentials stored in `~/.config/dataforseo/auth` (Base64 encoded).

```bash
# Read auth token
AUTH=$(cat ~/.config/dataforseo/auth)
```

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/seo keywords research <seed>` | Generate keyword ideas from seed keyword |
| `/seo keywords volume <keyword1, keyword2, ...>` | Get search volume for keywords |
| `/seo keywords difficulty <keyword1, keyword2, ...>` | Analyze keyword difficulty scores |
| `/seo keywords site <domain>` | Find keywords a site ranks for |
| `/seo keywords gap <your-domain> <competitor>` | Find keyword opportunities |
| `/seo keywords intent <keyword1, keyword2, ...>` | Analyze search intent |
| `/seo keywords trending` | Find trending search queries |
| `/seo keywords history <keyword>` | Historical search volume data |

## API Endpoints

### Keyword Ideas
```bash
curl -s -X POST "https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_ideas/live" \
  -H "Authorization: Basic $(cat ~/.config/dataforseo/auth)" \
  -H "Content-Type: application/json" \
  -d '[{"keywords": ["SEED_KEYWORD"], "location_name": "United States", "language_code": "en", "limit": 50}]'
```

### Keyword Suggestions (Autocomplete)
```bash
curl -s -X POST "https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_suggestions/live" \
  -H "Authorization: Basic $(cat ~/.config/dataforseo/auth)" \
  -H "Content-Type: application/json" \
  -d '[{"keyword": "SEED_KEYWORD", "location_name": "United States", "language_code": "en", "limit": 50}]'
```

### Related Keywords
```bash
curl -s -X POST "https://api.dataforseo.com/v3/dataforseo_labs/google/related_keywords/live" \
  -H "Authorization: Basic $(cat ~/.config/dataforseo/auth)" \
  -H "Content-Type: application/json" \
  -d '[{"keyword": "SEED_KEYWORD", "location_name": "United States", "language_code": "en", "limit": 50}]'
```

### Bulk Keyword Difficulty
```bash
curl -s -X POST "https://api.dataforseo.com/v3/dataforseo_labs/bulk_keyword_difficulty/live" \
  -H "Authorization: Basic $(cat ~/.config/dataforseo/auth)" \
  -H "Content-Type: application/json" \
  -d '[{"keywords": ["kw1", "kw2", "kw3"], "location_name": "United States", "language_code": "en"}]'
```

### Search Volume (Google Ads Data)
```bash
curl -s -X POST "https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live" \
  -H "Authorization: Basic $(cat ~/.config/dataforseo/auth)" \
  -H "Content-Type: application/json" \
  -d '[{"keywords": ["kw1", "kw2"], "location_code": 2840, "language_code": "en"}]'
```

### Ranked Keywords (Site Analysis)
```bash
curl -s -X POST "https://api.dataforseo.com/v3/dataforseo_labs/google/ranked_keywords/live" \
  -H "Authorization: Basic $(cat ~/.config/dataforseo/auth)" \
  -H "Content-Type: application/json" \
  -d '[{"target": "example.com", "location_name": "United States", "language_code": "en", "limit": 100}]'
```

### Search Intent
```bash
curl -s -X POST "https://api.dataforseo.com/v3/dataforseo_labs/google/search_intent/live" \
  -H "Authorization: Basic $(cat ~/.config/dataforseo/auth)" \
  -H "Content-Type: application/json" \
  -d '[{"keywords": ["kw1", "kw2"], "language_code": "en"}]'
```

### Historical Keyword Data
```bash
curl -s -X POST "https://api.dataforseo.com/v3/dataforseo_labs/google/historical_search_volume/live" \
  -H "Authorization: Basic $(cat ~/.config/dataforseo/auth)" \
  -H "Content-Type: application/json" \
  -d '[{"keywords": ["KEYWORD"], "location_name": "United States", "language_code": "en"}]'
```

## Analysis Modes

### 1. Keyword Research (Ideas Generation)

Generate keyword ideas from a seed keyword:

```
Input: seed keyword (e.g., "coffee maker")
Output:
- Related keyword ideas
- Search volume per keyword
- CPC and competition data
- Keyword difficulty score
- Search intent classification
```

### 2. Search Volume Analysis

Get accurate search volume data:

```
Input: list of keywords
Output:
- Monthly search volume
- Search volume trend (12 months)
- CPC estimate
- Competition level (0-1)
- Seasonal patterns
```

### 3. Keyword Difficulty Assessment

Analyze ranking difficulty:

```
Input: list of keywords
Output:
- Difficulty score (0-100)
- SERP feature presence
- Top 10 competitor strength
- Estimated effort to rank
```

**Difficulty Interpretation:**
- 0-20: Easy (new sites can rank)
- 20-40: Moderate (some authority needed)
- 40-60: Hard (established sites only)
- 60-80: Very Hard (high authority required)
- 80-100: Extremely Hard (dominant players only)

### 4. Site Keyword Analysis

Find keywords a domain ranks for:

```
Input: domain (e.g., "example.com")
Output:
- All ranking keywords
- Position for each keyword
- Search volume
- Traffic estimate
- Featured snippet presence
```

### 5. Search Intent Analysis

Classify keyword intent:

```
Input: list of keywords
Output:
- Intent type per keyword:
  - Informational (how, what, why)
  - Navigational (brand searches)
  - Commercial (best, review, compare)
  - Transactional (buy, price, discount)
- Content format recommendations
```

**Content Mapping:**
| Intent | Content Type |
|--------|-------------|
| Informational | Blog posts, guides, tutorials |
| Navigational | Landing pages, about pages |
| Commercial | Comparison pages, reviews |
| Transactional | Product pages, pricing pages |

## Keyword Prioritization Framework

### Priority Matrix

Score each keyword on these factors:

| Factor | Weight | Scoring |
|--------|--------|---------|
| Search Volume | 25% | High (3), Medium (2), Low (1) |
| Difficulty | 30% | Easy (3), Medium (2), Hard (1) |
| Business Relevance | 25% | High (3), Medium (2), Low (1) |
| Intent Match | 20% | Perfect (3), Good (2), Partial (1) |

### Quick Win Identification

Quick wins have:
- Search volume > 100/month
- Difficulty < 40
- Commercial or transactional intent
- Direct business relevance

## Output Format

### Keyword Research Report

```markdown
# Keyword Research: [seed keyword]

## Overview
- Total keywords found: X
- Average monthly volume: X
- Average difficulty: X

## Top Opportunities (Priority Sorted)

| Keyword | Volume | Difficulty | Intent | Priority |
|---------|--------|------------|--------|----------|
| [kw1] | X | X | Info | High |
| [kw2] | X | X | Trans | High |

## Keyword Clusters

### Cluster 1: [Topic]
- keyword a (vol: X, diff: X)
- keyword b (vol: X, diff: X)

## Content Recommendations

### Immediate Actions (Quick Wins)
1. [Keyword] -> Create [content type]
2. [Keyword] -> Create [content type]
```

## Integration with Other SEO Skills

- Use `seo-content` to create content for target keywords
- Use `seo-backlinks` to build authority for competitive keywords
- Use `seo-serp` to track ranking progress

[PROTOCOL]: Update this header on changes, then check CLAUDE.md
