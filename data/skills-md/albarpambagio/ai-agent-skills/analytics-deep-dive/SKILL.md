---
name: analytics-deep-dive
description: Drive from headline trends to root causes using North Star decomposition, cross-tabulation, and quantification. Use when you've found a high-level pattern and need to explain why it happened with defensible numbers.
---

# Analytics Deep Dive

Shift from *what* happened to *why* it happened. Decompose metrics, cross-tab dimensions, and quantify impact.

## Quick Start

```markdown
Headline finding: [metric] changed by [X%] over [period]
North Star metric: [primary KPI]
North Star dims: [2-3 slicing dimensions]

Step 1 — Decompose: [metric] = [sub-metric A] × [sub-metric B]
                     ⇒ [which drove the change?]
Step 2 — Slice by dims: [which segment explains the most variance?]
Step 3 — Cross-tab: [dim A] × [dim B] reveals [specific interaction]
Step 4 — Quantify: [segment] accounts for [$X / Y%] of the total change
```

## Workflow

### Step 1: Decompose the North Star

Most headline metrics are composites. Break them apart:

| Composite | Decomposition | What Each Tells You |
|-----------|--------------|---------------------|
| Revenue | Orders × AOV | Volume vs. price driver |
| Conversion | Closed / Started | Funnel efficiency |
| LTV | Revenue / Customers | Value per acquisition |

If the metric moved, ask: was it the numerator, denominator, or both?

### Step 2: Slice by Dimensions

For the sub-metric that moved, split by your North Star dimensions:
- **Time**: Is this a one-month spike or a steady trend?
- **Category**: Is it concentrated in one product/region/channel?
- **Segment**: Does every segment show the same pattern?

Eliminate low-impact segments early. If 3 products drive 90% of revenue, center analysis there.

### Step 3: Cross-Tab for Interaction Effects

Combine two dimensions to find where the real story lives:

| Dim A \ Dim B | Segment 1 | Segment 2 | Segment 3 |
|---------------|-----------|-----------|-----------|
| Category X | $100K | $50K | $10K |
| Category Y | $200K | $30K | $5K |

The cross-tab reveals whether a trend is:
- **Macro** (all cells move together) — external/market cause
- **Segment-specific** (one cell drives everything) — internal/operational cause

### Step 4: Quantify the Impact

Put a number on every finding:

> *"Direct North American sales dropped from $304K to $118K — a 61% decline. This single segment accounts for ~$200K of the $500K total revenue dip."*

**Formula:** `impact = (current - baseline) × segment_share`

If the cause can't be fully isolated, add a caveat: *"~$200K attributable based on available data; causal confirmation requires [additional data]."*

## Example: From Headline to Root Cause

| Layer | Finding | Type |
|-------|---------|------|
| Headline | Revenue dropped 12% in Q2 | Aggregate observation |
| Decomposed | AOV held steady, order count dropped 14% | Tells you it's a volume problem |
| Sliced | Order drop concentrated in one product category | Tells you it's not macro |
| Cross-tabbed | Category drop is specific to one marketing channel × region | Pinpoints the lever |
| Quantified | That segment = 40% of total revenue decline | Sizes the opportunity |

## Verification

- [ ] Headline metric decomposed into sub-metrics
- [ ] Sliced by at least 2 North Star dimensions
- [ ] Cross-tab reveals which segment drives the pattern
- [ ] Impact quantified with formula and caveats
