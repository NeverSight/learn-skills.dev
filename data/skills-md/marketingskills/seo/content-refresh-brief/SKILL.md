---
name: content-refresh-brief
description: Produce a focused refresh brief for a declining page. Use when Codex needs to research SERP intent, competitor content, entity coverage, and internal link opportunities to create an actionable page refresh plan.
---

# Content Refresh Brief

## Overview

Given a URL and optionally its GSC/GA4 performance data, produce a structured refresh brief that covers SERP intent analysis, entity gaps, content outline, internal link plan, and technical recommendations.

## Inputs

- URL of the page to refresh
- Current GSC performance (clicks, impressions, CTR, avg position, top queries)
- Prior period GSC performance for comparison
- Optional: page content (if the user pastes it)
- Optional: GA4 engagement or conversion data

## Workflow

1. Search the page's primary query in a current SERP.
2. Analyze top 5 organic results for:
   - Content format (guide, list, tool, video, etc.)
   - Content depth (word count, section count, entities covered)
   - Date freshness (when each page was last updated)
   - SERP features present (featured snippets, People Also Ask, video, etc.)
3. Compare current page content against SERP expectations:
   - Does it match the dominant content format?
   - Are key entities missing?
   - Is the content depth competitive?
   - Is the page fresh enough?
4. Review GSC query data to identify:
   - Queries with declining CTR despite stable impressions
   - Queries where the page ranks but doesn't satisfy intent
   - Queries from the prior period that stopped driving traffic
5. Recommend:
   - Content changes (restructure, expand, add sections, update data)
   - Technical changes (title, meta description, schema, canonical)
   - Internal link additions (from high-traffic pages)
   - Entities to add or strengthen
6. Estimate effort and expected recovery.

## Output Format

```markdown
## Refresh Brief: /page-url

### Current Performance
| Metric | Current | Prior | Change |
|---|---|---|---|

### SERP Intent Analysis
[Format, depth, freshness expectations from top results]

### Gap Analysis
| Gap | Competitor Example | Our Action |
|---|---|---|

### Recommended Content Changes
1. [Action with details]

### Recommended Technical Changes
1. [Action with details]

### Internal Link Plan
| Source Page | Anchor Text | Rationale |
|---|---|---|

### Effort Estimate
[Low / Medium / High] — [estimated hours]

### Expected Recovery
[Estimated click/impression recovery range]
```

## Related Skills

- `traffic-decay-detector` — identifies which pages need briefs.
- `serp-authority-mark` — checks authority feasibility for the target query.
- `title-meta-rewriter` — produces title/meta alternatives for the refresh.
