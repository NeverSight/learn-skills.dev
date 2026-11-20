---
name: data-visualization
description: Chooses and designs charts that answer a specific question, covering chart type selection, zero-based bar axes, direct labels, one highlighted series, colorblind-safe palettes, number formatting, takeaway titles, and text alternatives. Use when asked which chart to use, to make a chart or graph, fix a confusing visualization, or design charts for a report or dashboard. Not for whole dashboard layout, which is dashboard-design, or tabular data, which is data-tables.
---

# Data Visualization

Produces charts that make one point obvious at a glance: the right chart type, honest scales, accessible color, and a title that states the takeaway, delivered as code or a precise spec.

## When to use
- "Which chart should I use for this?" or "make a chart of this data."
- A chart is cluttered, misleading, or depends on a legend nobody reads.
- Charts for a report, a slide (see slide-design), a dashboard (see dashboard-design), or a social post.
- Choosing palettes for categories, ordered scales, or above/below comparisons.
- Making existing charts accessible.

## Workflow
1. Identify the question and the audience, then write the takeaway as one sentence before choosing a chart. If the data or the question is missing, ask once.
2. Inspect the data: types (categorical, ordinal, time, continuous), number of series and categories, ranges, outliers, missing values.
3. Choose the chart by question:
   - Comparison across categories: bar chart, horizontal when labels are long; sort by value unless the order is meaningful.
   - Trend over time: line chart; bars for a few discrete periods.
   - Part-to-whole: stacked or 100% bar, or a single highlighted share for one number; pie or donut only for 2–3 parts.
   - Distribution: histogram or box plot; dot or strip plot for small samples.
   - Relationship: scatter plot; add size as a third variable only if essential.
   - Many series: small multiples on shared axes instead of one spaghetti chart.
4. Set scales: bar and area axes start at zero; line axes may zoom in but must label the range; small multiples share one scale.
5. Apply color with intent: one accent for the series that carries the takeaway, grey for context. Use a full categorical palette only when every category must be told apart.
6. Label: the title states the takeaway, the subtitle gives metric, unit, and period, data is labeled directly at line ends or bar tips, and a source line sits at the bottom.
7. Add accessibility: a text alternative with the takeaway and key values, a data table or download, and labels, shapes, or patterns so color is never the only cue.

## Rules
**Color**
- Categorical: use a colorblind-safe palette such as Okabe–Ito (#E69F00, #56B4E9, #009E73, #F0E442, #0072B2, #D55E00, #CC79A7, #000000). Never rely on red versus green alone.
- On white, Okabe–Ito orange, sky blue, and yellow fall below 3:1 contrast; add a darker outline or direct labels, or reserve them for large filled areas.
- Graphical marks need 3:1 contrast against the background and text needs 4.5:1 (WCAG 2.2 AA).
- More than about 6 categories: group the tail into "Other", highlight the relevant one, or switch to small multiples.
- Sequential data (low to high): one hue stepping in lightness. Diverging data (around a meaningful midpoint such as 0, target, or average): two hues with a neutral middle.
- No rainbow palettes for ordered data; they create false boundaries.

**Labels and numbers**
- Direct labels over legends; if a legend is unavoidable, order it like the data and place it near it.
- Format for reading: thousands separators, consistent precision (usually 0–1 decimals), abbreviations (1.2M, 34K), units in the subtitle or axis title, tabular numerals on axes and labels.
- Keep gridlines light and few (3–5); remove borders, 3D, shadows, and background fills.

**Integrity**
- No truncated bar axes, no dual y-axes (use two aligned charts), no uneven time intervals presented as even.
- Show uncertainty or small sample sizes when they change the conclusion; never invent, smooth, or cherry-pick data.

## Output
- Recommendation: chart type, one-line reason, and the takeaway title.
- Code in the project's existing chart library; otherwise inline SVG or semantic HTML/CSS for simple charts, with no new dependency unless asked. Colors as CSS custom properties.
- Spec when code is not wanted: chart type, encodings (x, y, color, size), scale domains, palette hex values, label positions, title, subtitle, source, and alt text.

## Avoid
- Pies with more than 3 slices, or slices compared across several pies.
- Legends far from the data that force color matching from memory.
- Every series in a saturated color.
- Titles that only name the metric ("Revenue by month") when there is a point to make.
- Dual axes, 3D effects, and decorative chart junk.
- Spaghetti charts with more than about 5 overlapping lines.

## Final check
- [ ] The chart type fits the question and the title states the takeaway.
- [ ] Bar and area axes start at zero; related charts share scales.
- [ ] One series is highlighted and the rest are muted.
- [ ] The palette is colorblind-safe and color is not the only encoding.
- [ ] Numbers carry units and consistent precision.
- [ ] A text alternative lists the takeaway and key values.
