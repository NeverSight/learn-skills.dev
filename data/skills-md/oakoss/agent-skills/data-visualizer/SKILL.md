---
name: data-visualizer
description: 'Charts, dashboards, and data visualizations using Recharts, Chart.js, and D3.js. Use when building charts, dashboards, or interactive data displays. Use for chart type selection, data storytelling, annotation patterns, responsive design, accessibility, and performance optimization.'
license: MIT
metadata:
  author: oakoss
  version: '1.2'
---

# Data Visualizer

Build charts, dashboards, and interactive data visualizations using modern libraries. Covers Recharts (React), Chart.js (framework-agnostic), and D3.js (custom/advanced).

## Library Selection

| Library  | Best For                            | React   | Custom   | Bundle (gzip)          |
| -------- | ----------------------------------- | ------- | -------- | ---------------------- |
| Recharts | Quick React charts, standard types  | Native  | Limited  | ~139KB                 |
| Chart.js | Framework-agnostic, simple API      | Wrapper | Moderate | ~68KB (tree-shakeable) |
| D3.js    | Custom visualizations, full control | Manual  | Full     | ~13-30KB per module    |

## Chart Type Selection

| Chart     | Best For                             | Avoid When                        |
| --------- | ------------------------------------ | --------------------------------- |
| Line      | Trends over time, continuous data    | Categorical data                  |
| Bar       | Comparing categories, rankings       | Continuous data                   |
| Pie/Donut | Part-to-whole (max 5-7 slices)       | >7 categories, precise comparison |
| Area      | Volume over time, stacked categories | Too many overlapping series       |
| Scatter   | Correlation, outliers, distribution  | Time series                       |
| Heatmap   | Intensity across two dimensions      | Simple comparisons                |

## Dashboard Patterns

| Pattern             | Use Case             | Key Feature                        |
| ------------------- | -------------------- | ---------------------------------- |
| KPI Dashboard       | Executive metrics    | Trend indicators, card grid        |
| Real-Time           | Live monitoring      | SSE/WebSocket, animation disabled  |
| Interactive Filters | Exploratory analysis | Period/region selects, drill-down  |
| Drill-Down          | Hierarchical data    | Click to zoom (year → month → day) |

## Responsive Design

| Approach               | Implementation                                    |
| ---------------------- | ------------------------------------------------- |
| Container-based sizing | `<ResponsiveContainer width="100%" height={300}>` |
| Aspect ratio mode      | `<ResponsiveContainer width="100%" aspect={2}>`   |
| Mobile-aware           | Reduce `strokeWidth`, `height` on small screens   |
| Label simplification   | Fewer axis labels on mobile                       |

## Common Mistakes

| Mistake                      | Fix                                            |
| ---------------------------- | ---------------------------------------------- |
| Fixed width/height           | Use `ResponsiveContainer`                      |
| Animation on real-time data  | Set `isAnimationActive={false}`                |
| Too many pie slices          | Max 5-7 slices, group rest as "Other"          |
| Non-accessible colors        | Use WCAG AA compliant, colorblind-safe palette |
| Loading entire chart library | Lazy load with dynamic imports                 |
| No data formatting           | Use `Intl.NumberFormat` for currency/percent   |

## Delegation

- **Explore data shape and available fields before choosing chart type**: Use `Explore` agent
- **Build a complete multi-chart dashboard from requirements**: Use `Task` agent
- **Plan visualization architecture for large-scale analytics pages**: Use `Plan` agent

## References

- [Library Selection](references/library-selection.md) — Recharts, Chart.js, D3.js setup and examples
- [Chart Types](references/chart-types.md) — line, bar, pie, area, scatter, heatmap with use cases
- [Dashboard Patterns](references/dashboard-patterns.md) — KPI, real-time SSE, interactive filters, drill-down
- [Design and Accessibility](references/design-and-accessibility.md) — color schemes, colorblind-safe palettes, responsive, animation
- [Data Formatting and Export](references/data-formatting-and-export.md) — number formatters, CSV export, PNG export
- [Performance](references/performance.md) — lazy loading, virtualization for large datasets
- [Storytelling and Annotation](references/storytelling-and-annotation.md) — data narratives, annotations, color strategy, edge states
