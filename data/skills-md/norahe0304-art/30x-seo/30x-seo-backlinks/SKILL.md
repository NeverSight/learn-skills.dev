---
name: 30x-seo-backlinks
description: >
  Comprehensive backlink analysis using DataForSEO API. Analyze backlink profiles,
  find link building opportunities, detect toxic links, compare with competitors,
  and identify link gaps. Use when user says "backlinks", "link building",
  "referring domains", "link profile", "toxic links", "link gap", "competitor links",
  or "domain authority".
allowed-tools:
  - Bash
  - Read
---

# SEO Backlinks Analysis

Comprehensive backlink analysis and link building intelligence using DataForSEO API via direct curl calls.

## API Configuration

Credentials stored in `~/.config/dataforseo/auth` (Base64 encoded).

```bash
# Read auth token
AUTH=$(cat ~/.config/dataforseo/auth)
```

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/seo backlinks profile <domain>` | Full backlink profile analysis |
| `/seo backlinks compare <domain1> <domain2>` | Compare two domains' backlink profiles |
| `/seo backlinks gap <your-domain> <competitor1> [competitor2]` | Find link gap opportunities |
| `/seo backlinks toxic <domain>` | Identify potentially toxic/spammy links |
| `/seo backlinks anchors <domain>` | Analyze anchor text distribution |
| `/seo backlinks trend <domain>` | New/lost backlinks over time |
| `/seo backlinks competitors <domain>` | Find competitors by backlink overlap |

## API Endpoints

### Backlink Summary
```bash
curl -s -X POST "https://api.dataforseo.com/v3/backlinks/summary/live" \
  -H "Authorization: Basic $(cat ~/.config/dataforseo/auth)" \
  -H "Content-Type: application/json" \
  -d '[{"target": "example.com"}]'
```

### Get Backlinks
```bash
curl -s -X POST "https://api.dataforseo.com/v3/backlinks/backlinks/live" \
  -H "Authorization: Basic $(cat ~/.config/dataforseo/auth)" \
  -H "Content-Type: application/json" \
  -d '[{"target": "example.com", "limit": 100, "order_by": ["rank,desc"]}]'
```

### Anchor Text Analysis
```bash
curl -s -X POST "https://api.dataforseo.com/v3/backlinks/anchors/live" \
  -H "Authorization: Basic $(cat ~/.config/dataforseo/auth)" \
  -H "Content-Type: application/json" \
  -d '[{"target": "example.com", "limit": 100}]'
```

### Bulk Backlinks (Multiple Domains)
```bash
curl -s -X POST "https://api.dataforseo.com/v3/backlinks/bulk_backlinks/live" \
  -H "Authorization: Basic $(cat ~/.config/dataforseo/auth)" \
  -H "Content-Type: application/json" \
  -d '[{"targets": ["domain1.com", "domain2.com", "domain3.com"]}]'
```

### Bulk Referring Domains
```bash
curl -s -X POST "https://api.dataforseo.com/v3/backlinks/bulk_referring_domains/live" \
  -H "Authorization: Basic $(cat ~/.config/dataforseo/auth)" \
  -H "Content-Type: application/json" \
  -d '[{"targets": ["domain1.com", "domain2.com"]}]'
```

### Bulk Ranks (Domain Authority)
```bash
curl -s -X POST "https://api.dataforseo.com/v3/backlinks/bulk_ranks/live" \
  -H "Authorization: Basic $(cat ~/.config/dataforseo/auth)" \
  -H "Content-Type: application/json" \
  -d '[{"targets": ["domain1.com", "domain2.com"]}]'
```

### Bulk Spam Score
```bash
curl -s -X POST "https://api.dataforseo.com/v3/backlinks/bulk_spam_score/live" \
  -H "Authorization: Basic $(cat ~/.config/dataforseo/auth)" \
  -H "Content-Type: application/json" \
  -d '[{"targets": ["domain1.com", "domain2.com"]}]'
```

### Domain Intersection (Link Gap)
```bash
curl -s -X POST "https://api.dataforseo.com/v3/backlinks/domain_intersection/live" \
  -H "Authorization: Basic $(cat ~/.config/dataforseo/auth)" \
  -H "Content-Type: application/json" \
  -d '[{"targets": {"1": "competitor1.com", "2": "competitor2.com"}, "exclude_targets": ["your-domain.com"], "limit": 100}]'
```

### Competitors by Backlinks
```bash
curl -s -X POST "https://api.dataforseo.com/v3/backlinks/competitors/live" \
  -H "Authorization: Basic $(cat ~/.config/dataforseo/auth)" \
  -H "Content-Type: application/json" \
  -d '[{"target": "example.com", "limit": 20}]'
```

### New/Lost Backlinks Timeline
```bash
curl -s -X POST "https://api.dataforseo.com/v3/backlinks/timeseries_new_lost_summary/live" \
  -H "Authorization: Basic $(cat ~/.config/dataforseo/auth)" \
  -H "Content-Type: application/json" \
  -d '[{"target": "example.com", "date_from": "2024-01-01"}]'
```

### Referring Domains
```bash
curl -s -X POST "https://api.dataforseo.com/v3/backlinks/referring_domains/live" \
  -H "Authorization: Basic $(cat ~/.config/dataforseo/auth)" \
  -H "Content-Type: application/json" \
  -d '[{"target": "example.com", "limit": 100, "order_by": ["rank,desc"]}]'
```

## Analysis Modes

### 1. Backlink Profile Analysis

Get a comprehensive overview of a domain's backlink profile:

```
Input: domain (e.g., "example.com")
Output:
- Total backlinks count
- Referring domains count
- Domain rank (0-1000)
- Spam score (0-100)
- Dofollow vs nofollow ratio
- Top referring domains
- Anchor text distribution
- New/lost links trend
```

### 2. Competitor Comparison

Compare your backlink profile against competitors:

```
Input: [your-domain, competitor1, competitor2, ...]
Output:
- Side-by-side metrics comparison
- Unique referring domains per site
- Shared referring domains
- Gap opportunities
```

### 3. Link Gap Analysis

Find domains that link to competitors but not to you:

```
Input: [your-domain, competitor1, competitor2]
Output:
- Domains linking to competitors but not you
- Sorted by authority/relevance
- Prioritized outreach list
```

This is the most valuable analysis for link building strategy.

### 4. Toxic Link Detection

Identify potentially harmful backlinks:

```
Input: domain
Output:
- Links from high spam score domains
- Suspicious anchor text patterns
- Low-quality referring domains
- Disavow candidates
```

### 5. Anchor Text Analysis

Analyze anchor text distribution:

```
Input: domain
Output:
- Anchor text distribution chart
- Brand vs keyword vs generic ratio
- Over-optimized anchor warnings
- Natural vs unnatural patterns
```

**Healthy distribution guidelines:**
- Brand anchors: 30-40%
- Naked URLs: 20-30%
- Generic (click here, etc.): 15-20%
- Keyword-rich: 10-15% (over 20% = warning)
- LSI/related: 5-10%

## Interpretation Guidelines

### Domain Rank (0-1000)
- 0-100: Low authority
- 100-300: Moderate authority
- 300-500: Good authority
- 500-700: Strong authority
- 700-1000: Excellent authority

### Spam Score (0-100)
- 0-10: Clean profile
- 10-30: Low risk
- 30-60: Moderate risk (review needed)
- 60-100: High risk (cleanup recommended)

### Red Flags
- Sudden spike in backlinks (potential negative SEO)
- High percentage of nofollow links from unique domains
- Anchor text dominated by exact-match keywords
- Links from irrelevant industries/topics
- Many links from same IP range or C-class

## Output Format

### Summary Report
```markdown
# Backlink Profile: [domain]

## Overview
- Total Backlinks: X
- Referring Domains: X
- Domain Rank: X/1000
- Spam Score: X/100

## Health Assessment
[OK/WARN/BAD] Anchor distribution
[OK/WARN/BAD] Referring domain quality
[OK/WARN/BAD] Link velocity
[OK/WARN/BAD] Spam indicators

## Top Referring Domains
1. [domain] - X backlinks, rank Y
2. ...

## Anchor Text Distribution
[chart or table]

## Recommendations
1. [Priority action]
2. [Secondary action]
```

## Link Building Prioritization

When generating outreach lists from link gap analysis:

**Tier 1 (High Priority)**
- Domain rank > 500
- Relevant to your industry
- Editorial links (not directories)

**Tier 2 (Medium Priority)**
- Domain rank 200-500
- Related industry or topic
- Resource pages, roundups

**Tier 3 (Low Priority)**
- Domain rank < 200
- Directories, forums
- Comment sections

## Integration with Other SEO Skills

- Use `seo-content` to analyze pages that attract backlinks
- Use `seo-keywords` to find keywords for linkable content
- Use `seo-serp` to track ranking impact of new links

[PROTOCOL]: Update this header on changes, then check CLAUDE.md
