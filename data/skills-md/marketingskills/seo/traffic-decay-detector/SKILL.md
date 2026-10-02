---
name: traffic-decay-detector
description: Find pages losing clicks, impressions, CTR, or rankings using GSC/GA4 when available or from pasted data. Use when Codex needs to identify declining organic performance, surface the queries driving the decline, and recommend which pages to refresh first.
---

# Traffic Decay Detector

## Overview

Identify pages with declining organic traffic, what queries are driving the loss, and which pages are worth refreshing. Works with live GSC/GA4 data (via `marketingskills/seo/skills/live-search-console-data`) or pasted exports.

## Inputs

- Current period GSC data (queries + pages): clicks, impressions, CTR, avg position
- Prior period GSC data (same dimensions, same property)
- Optional: GA4 landing page sessions or conversion data
- Optional: threshold for minimum clicks (default: 10 clicks/period)

If no live data is available, ask the user to paste GSC exports for both periods.

## Workflow

1. Load GSC data from live connection or pasted export.
2. Compare current period vs prior period for each page.
3. Calculate absolute and relative change for clicks, impressions, CTR, position.
4. Filter to pages with click decline > configured threshold.
5. For each declining page, find which queries drove the loss.
6. Classify the cause: SERP position drop, CTR collapse, impression loss, or seasonal.
7. Surface the queries with the biggest click loss per page.
8. Rank pages by total click loss and confidence in recovery.
9. Recommend refresh candidates with rationale.

## Output Format

```markdown
## Traffic Decay Report

**Period:** [current range] vs [prior range]
**Pages analyzed:** N
**Declining pages found:** N

### Top Declining Pages
| Page | Clicks (curr) | Clicks (prev) | Change | Primary Query | Cause |
|---|---|---|---|---|---|
| /page-url | 1,200 | 2,000 | -800 (-40%) | "keyword" | Position drop (2→6) |

### Top Queries Driving Decline
| Query | Click Loss | Current Pos | Prior Pos | Page Affected |
|---|---|---|---|---|

### Refresh Candidates
Priority-ordered list with reasoning.

### Stable Pages (for reference)
Pages with flat or growing traffic.
```

## Interpretation

- A page losing clicks while impressions are stable likely has a CTR or ranking issue.
- A page losing both clicks and impressions may have lost search volume or been overtaken.
- Pages with high impression counts and low CTR may need title/meta rewrites or featured snippet targeting.
- Seasonal declines should be marked but not recommended for immediate refresh unless the trend is accelerating.

## Related Skills

- `content-refresh-brief` — produce a focused brief for any page identified here.
- `serp-authority-mark` — check if the page's primary query is winnable.
- `marketingskills/seo/skills/live-search-console-data` — live GSC/GA4 data bridge.
