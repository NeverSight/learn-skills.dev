---
name: chart-chooser
description: Selects the most appropriate chart type for a given dataset and analytical question, then produces a clean, honest, well-labeled visualization spec. Use this skill when a user asks "what chart should I use", "how should I visualize this data", "which graph fits", "make a chart for X", "is a pie chart right here", "how do I show change over time / comparison / distribution / correlation / part-to-whole", or when reviewing an existing chart for clarity and honesty. Covers chart-type decision-making, encoding choices (axis, color, size), labeling, axis-truncation ethics, accessibility, and avoiding misleading visuals.
license: MIT
---

# Chart Chooser

## Overview
This skill turns a dataset plus an analytical question into the *right* chart, and ensures the result is clean, accurate, and not misleading. It covers two jobs:

1. **Choose** — map the question intent and data shape to a chart type.
2. **Polish** — apply encoding, labeling, axis, color, and honesty rules so the chart reads correctly at a glance.

Keywords: data visualization, chart type, graph selection, bar chart, line chart, scatter plot, histogram, heatmap, pie chart, dashboard, axis truncation, misleading charts, color accessibility, data-ink, encoding.

Use this skill whenever someone needs to decide *how* to show data, or wants an existing visual critiqued.

## Workflow

Follow these steps in order. Do not jump to a chart type before clarifying intent and data shape.

1. **Identify the question intent.** Pick the dominant one (a chart should answer one question well):
   - Comparison (which is bigger/smaller across categories)
   - Trend / change over time
   - Distribution (shape, spread, outliers of one variable)
   - Relationship / correlation (two+ numeric variables)
   - Part-to-whole (composition of a total)
   - Ranking (ordered comparison)
   - Geospatial (values across places)
   - Flow / part-to-whole over stages
2. **Profile the data shape.** Note for each variable: type (categorical / ordinal / quantitative / temporal / geographic), cardinality (number of distinct values), and whether values can be summed to a meaningful total (needed for part-to-whole).
3. **Match intent + shape to a chart.** Use the decision table in `references/chart-decision-matrix.md`. Resolve ties with the "pick the simplest that answers the question" rule.
4. **Choose encodings.** Assign data fields to position, length, color, and size using the accuracy ranking in Best Practices. Position/length beat color/area for quantitative accuracy.
5. **Apply honesty + clarity rules.** Run the checklist in `references/clarity-and-honesty-checklist.md`: axis baselines, sorting, direct labels, color accessibility, decluttering.
6. **Produce the output.** Either describe the spec (chart type, x, y, color, sort, annotations) or generate code. Use `scripts/suggest_chart.py` to get a programmatic recommendation from a quick data profile.
7. **Self-review.** Verify the chart answers the original question in under 5 seconds and contains no misleading element.

## Quick Decision Cheats

- **Over time, continuous:** line chart (one or few series), area only when part-to-whole over time matters.
- **Compare categories:** bar chart (horizontal if labels are long or many). Sort by value unless order is inherent (time, age bands).
- **Distribution of one number:** histogram; box/violin to compare distributions across groups.
- **Two numbers, relationship:** scatter plot; add trend line only if a relationship is real and labeled.
- **Part-to-whole, few parts (2-4), single total:** consider a stacked bar; a pie is acceptable only with ≤4 slices and clear differences.
- **Part-to-whole, many parts:** sorted bar of the parts, not a pie.
- **Two categorical dimensions + a value:** heatmap.
- **Ranking emphasis:** sorted horizontal bar; lollipop to reduce ink.
- Never use a second y-axis to imply correlation; it can fabricate relationships.

## Best Practices

- **Encoding accuracy order** (most to least precise): position on common scale → position on non-aligned scale → length → angle/slope → area → color saturation → color hue. Encode the most important quantity with the most accurate channel.
- **Start bars at zero.** Bar length encodes magnitude; a non-zero baseline lies. Line charts may use a non-zero baseline if change, not magnitude, is the point — label it clearly.
- **Sort meaningfully.** Sort categorical bars by value. Keep natural order for time, age, or other ordinals.
- **Direct-label** lines and important points instead of forcing legend lookups. Limit to ~5-7 series before a chart becomes spaghetti.
- **One idea per chart.** Split a busy chart into small multiples rather than overloading one canvas.
- **Color with purpose.** Categorical = distinct hues; sequential = single-hue ramp; diverging = two hues around a meaningful midpoint. Test for color-vision deficiency; never rely on red/green alone — add labels, shapes, or patterns.
- **Maximize data-ink.** Remove chartjunk, heavy gridlines, 3D effects, and redundant decoration.
- **Title states the takeaway** ("Revenue grew 30% in Q3"), not just the variable ("Revenue").
- **Annotate context** — reference lines, target, average, or events that explain the shape.

## Common Pitfalls

- Pie chart with many or similar slices — humans compare angles poorly. Use a sorted bar.
- Truncated bar-chart y-axis exaggerating tiny differences.
- Dual y-axes implying a causal/correlated relationship that the scaling invented.
- 3D bars/pies that distort proportions.
- Rainbow/jet color ramps for sequential data (perceptually non-uniform and inaccessible).
- Too many categories or series, producing unreadable spaghetti.
- Unsorted bars when the question is "which is biggest".
- Using area/bubble size for precise comparison (area is hard to judge).
- Missing units, missing axis labels, or unlabeled aggregation (sum vs average).
- Connecting points with a line when the x-axis is categorical, not continuous.

## Supporting Files

- `references/chart-decision-matrix.md` — full intent × data-shape → chart-type matrix with notes and runners-up.
- `references/clarity-and-honesty-checklist.md` — pre-publish checklist for labeling, axes, color, accessibility, and avoiding deception.
- `scripts/suggest_chart.py` — stdlib Python tool: feed it a CSV (or a column profile) and the question intent; it recommends a chart type and encodings.
- `examples/sales-by-region.md` — worked example: messy request → chosen chart → clean spec → critique.
