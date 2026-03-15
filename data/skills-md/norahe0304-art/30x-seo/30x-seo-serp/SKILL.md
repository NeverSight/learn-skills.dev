---
name: 30x-seo-serp
description: >
  Track SERP rankings, monitor position changes, analyze SERP features, and identify
  ranking opportunities using DataForSEO. Alternative to Google Search Console for
  ranking data. Use when user says "rankings", "SERP tracking", "position monitoring",
  "rank tracking", "keyword positions", or "SERP analysis".
allowed-tools:
  - Bash
  - Read
---

# SEO SERP Tracking

Track rankings, monitor SERP changes, and analyze search result features using DataForSEO API via direct curl calls.

## API Configuration

Credentials stored in `~/.config/dataforseo/auth` (Base64 encoded).

```bash
# Read auth token
AUTH=$(cat ~/.config/dataforseo/auth)
```

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/seo serp rank <domain>` | Get all keywords domain ranks for |
| `/seo serp check <keyword>` | Live SERP check for keyword |
| `/seo serp history <keyword>` | Historical SERP changes |
| `/seo serp features <keyword>` | Analyze SERP features present |
| `/seo serp competitors <keyword>` | Who ranks for this keyword |
| `/seo serp overview <domain>` | Domain ranking overview |

## API Endpoints

### Live SERP Check
```bash
curl -s -X POST "https://api.dataforseo.com/v3/serp/google/organic/live/advanced" \
  -H "Authorization: Basic $(cat ~/.config/dataforseo/auth)" \
  -H "Content-Type: application/json" \
  -d '[{"keyword": "TARGET_KEYWORD", "location_name": "United States", "language_code": "en", "depth": 100}]'
```

### Domain Rank Overview
```bash
curl -s -X POST "https://api.dataforseo.com/v3/dataforseo_labs/google/domain_rank_overview/live" \
  -H "Authorization: Basic $(cat ~/.config/dataforseo/auth)" \
  -H "Content-Type: application/json" \
  -d '[{"target": "example.com", "location_name": "United States", "language_code": "en"}]'
```

### Ranked Keywords (Site Rankings)
```bash
curl -s -X POST "https://api.dataforseo.com/v3/dataforseo_labs/google/ranked_keywords/live" \
  -H "Authorization: Basic $(cat ~/.config/dataforseo/auth)" \
  -H "Content-Type: application/json" \
  -d '[{"target": "example.com", "location_name": "United States", "language_code": "en", "limit": 100}]'
```

### Historical SERP
```bash
curl -s -X POST "https://api.dataforseo.com/v3/dataforseo_labs/google/historical_serps/live" \
  -H "Authorization: Basic $(cat ~/.config/dataforseo/auth)" \
  -H "Content-Type: application/json" \
  -d '[{"keyword": "TARGET_KEYWORD", "location_name": "United States", "language_code": "en"}]'
```

### SERP Competitors
```bash
curl -s -X POST "https://api.dataforseo.com/v3/dataforseo_labs/google/serp_competitors/live" \
  -H "Authorization: Basic $(cat ~/.config/dataforseo/auth)" \
  -H "Content-Type: application/json" \
  -d '[{"keywords": ["kw1", "kw2", "kw3"], "location_name": "United States", "language_code": "en"}]'
```

### Keyword Overview
```bash
curl -s -X POST "https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_overview/live" \
  -H "Authorization: Basic $(cat ~/.config/dataforseo/auth)" \
  -H "Content-Type: application/json" \
  -d '[{"keywords": ["kw1", "kw2"], "location_name": "United States", "language_code": "en"}]'
```

## Analysis Modes

### 1. Domain Ranking Overview

Get complete ranking profile for a domain.

```
Input: domain (e.g., "example.com")
Output:
- Total ranking keywords
- Position distribution (1-3, 4-10, 11-20, 21-100)
- Estimated organic traffic
- Top ranking keywords
- SERP feature presence
```

**Position Distribution Chart:**
```
Position 1-3:   ############ 45 keywords
Position 4-10:  #################### 89 keywords
Position 11-20: ########## 42 keywords
Position 21-50: ######## 35 keywords
Position 51+:   #### 18 keywords
```

### 2. Live SERP Check

Get current SERP for any keyword.

```
Input: keyword, location (optional)
Output:
- Top 10/20/100 results
- SERP features present
- Ads above/below organic
- Related searches
- People Also Ask
```

**SERP Feature Detection:**
| Feature | SEO Impact |
|---------|-----------|
| AI Overview | Reduces organic CTR |
| Featured Snippet | High visibility opportunity |
| People Also Ask | Content expansion signals |
| Local Pack | Local SEO needed |
| Image Pack | Image optimization opportunity |
| Video Carousel | Video content opportunity |
| Knowledge Panel | Brand authority signal |

### 3. Historical SERP Analysis

Track SERP changes over time.

```
Input: keyword
Output:
- SERP snapshots over time
- Position changes per domain
- Feature appearance/disappearance
- Volatility assessment
```

**Use cases:**
- Track algorithm update impact
- Identify ranking trends
- Detect competitor movements
- Plan content updates

### 4. SERP Competitor Analysis

Find who's competing for keywords.

```
Input: keyword(s)
Output:
- All ranking domains
- Average position per domain
- Traffic share estimates
- Content type analysis
```

### 5. Keyword Position Check

Check specific keyword positions for your domain.

```
Input: domain, keywords[]
Output:
- Current position per keyword
- URL ranking for each
- SERP features captured
- Position change from last check
```

## Ranking Metrics

### Position Tiers

| Tier | Positions | CTR Estimate | Priority |
|------|-----------|--------------|----------|
| Premium | 1-3 | 15-30% | Defend |
| Strong | 4-10 | 2-8% | Optimize |
| Striking Distance | 11-20 | 1-2% | Push |
| Opportunity | 21-50 | <1% | Content gap |
| Long-tail | 51+ | Minimal | Low priority |

### Traffic Estimation

DataForSEO provides estimated traffic based on:
- Search volume
- Position
- CTR model
- SERP features present

**Note:** These are estimates, not actual traffic data.

## Output Formats

### Ranking Report

```markdown
# SERP Rankings: [domain]
Generated: [Date]

## Overview
- Total Keywords: X
- Estimated Monthly Traffic: X
- Average Position: X
- Keywords in Top 10: X

## Position Distribution

| Position | Keywords | % of Total |
|----------|----------|------------|
| 1-3 | X | X% |
| 4-10 | X | X% |
| 11-20 | X | X% |
| 21-50 | X | X% |
| 51+ | X | X% |

## Top Keywords

| Keyword | Position | Volume | URL |
|---------|----------|--------|-----|
| [kw1] | 3 | 5,400 | /page1 |
| [kw2] | 7 | 3,200 | /page2 |

## SERP Features Captured

| Feature | Count | Keywords |
|---------|-------|----------|
| Featured Snippet | 5 | kw1, kw2, ... |
| People Also Ask | 12 | ... |

## Opportunities

### Striking Distance (Position 11-20)
Keywords close to page 1 - prioritize optimization:
1. [keyword] - Position 12, Volume 2,400
2. [keyword] - Position 15, Volume 1,800
```

### SERP Analysis Report

```markdown
# SERP Analysis: "[keyword]"
Location: [location]
Generated: [Date]

## SERP Composition

### Above the Fold
- Ads: 4
- AI Overview: Yes
- Featured Snippet: Yes (domain.com)

### Organic Results
1. domain1.com/page - Title
2. domain2.com/page - Title
...

### SERP Features Present
- [x] AI Overview
- [x] Featured Snippet
- [x] People Also Ask (4 questions)
- [ ] Local Pack
- [x] Image Pack
- [ ] Video Carousel

## Recommendations
1. Content type to create: [based on top results]
2. Target word count: [based on analysis]
3. SERP feature to target: [based on gaps]
```

## Comparison: DataForSEO vs GSC

| Capability | DataForSEO (this skill) | GSC |
|------------|------------------------|-----|
| Ranking data | Yes (estimated) | Yes (actual) |
| Click data | No | Yes |
| Impression data | No | Yes |
| CTR data | No | Yes |
| Any domain | Yes | Only verified |
| Historical depth | Months | 16 months |
| Real-time SERP | Yes | No |
| SERP features | Detailed | Limited |

**Use DataForSEO when:**
- Analyzing competitors
- Real-time SERP checks
- SERP feature analysis
- No GSC access

**Use GSC when:**
- Actual click/impression data needed
- CTR optimization
- Your own verified properties

## Integration with Other Skills

- Use `seo-keywords` to find keywords to track
- Use `seo-content` to optimize underperforming pages
- Use `seo-backlinks` to understand ranking factors

## Best Practices

### Tracking Setup

1. **Core keywords** - 20-50 most important terms
2. **Brand keywords** - Brand name variations
3. **Competitor keywords** - Where competitors rank
4. **Opportunity keywords** - Striking distance terms

### Monitoring Cadence

| Keyword Type | Check Frequency |
|--------------|-----------------|
| Core (top 20) | Weekly |
| Secondary (21-50) | Bi-weekly |
| Long-tail (51+) | Monthly |
| Competitor tracking | Weekly |

### Action Triggers

| Signal | Action |
|--------|--------|
| Position drop >5 | Investigate content/links |
| New competitor in top 5 | Analyze their content |
| SERP feature lost | Re-optimize for feature |
| Position 11-15 | Push to page 1 |

[PROTOCOL]: Update this header on changes, then check CLAUDE.md
