---
name: client-report-writer
description: Turn GSC/GA4 performance data into a client-ready weekly or monthly narrative. Use when Codex needs to produce a professional SEO performance report with executive summary, metrics breakdown, trend analysis, and action recommendations.
---

# Client Report Writer

## Overview

Transforms raw GSC and GA4 data into a structured client-ready report. The report tells a clear story: what happened, why it happened, and what to do next. Works with live data or pasted exports.

## Inputs

- Current period GSC data (clicks, impressions, CTR, avg position by page and query)
- Prior period GSC data for comparison
- Optional: GA4 data (sessions, users, conversions, landing pages)
- Optional: goals or KPIs the client tracks
- Optional: previous report for trend continuity
- Client name or brand voice preferences

## Workflow

1. Collect metrics for current and prior periods.
2. Calculate period-over-period changes for all key metrics.
3. Identify:
   - Top-level trend (up, down, flat with magnitude).
   - Pages that drove the change (top gainers, top decliners).
   - Queries that drove the change.
   - Technical issues detected (indexing drops, coverage changes).
4. Categorize changes as:
   - Expected (seasonal, planned launches, known ranking shifts).
   - Actionable (fixable issues with clear ROI).
   - Monitoring (needs observation before action).
5. Write the report in professional narrative form.
6. Add a recommendations section with prioritized actions.

## Output Format

```markdown
## SEO Performance Report
**Client:** [Name] | **Period:** [Range] | **Date:** [Date]

### Executive Summary
[3-5 sentence narrative of overall performance]

### Key Metrics
| Metric | Current | Prior | Change |
|---|---|---|---|

### What Changed
[Explanation of the main movements]

### Pages Driving Performance
#### Top Gainers
[Table with page, metric change, probable cause]

#### Top Decliners
[Table with page, metric change, probable cause]

### Query Trends
[Notable query movements, new opportunities, declining terms]

### Technical Health
[Index status, coverage issues, crawl stats if available]

### Recommendations
1. [Priority action with expected impact]
2. [Secondary action]
3. [Monitoring item]

### Appendix
Data sources, date ranges, methodology notes.
```

## Style Guidance

- Use professional, direct language. Avoid jargon where possible.
- Frame negative movements as situations with clear next actions, not failures.
- Include both absolute numbers and percentages.
- Call out what the client should be excited about and what needs attention.
- Keep the executive summary to 3-5 sentences — senior stakeholders should get the full picture from it.
- Separate signal from noise: if a 5% drop is normal fluctuation, say so.

## Related Skills

- `traffic-decay-detector` — feeds declining page data into the report.
- `proposal-builder` — for converting prospect data into a proposal (consulting version of this).
- `marketingskills/seo/skills/live-search-console-data` — live GSC/GA4 data bridge.
