---
name: data-visualization-principles
description: Data visualization design principles, chart selection, color theory, accessibility, and storytelling with data
license: Apache-2.0
---

# Data Visualization Principles Skill

## Purpose
Establishes principles for creating effective, accessible, and honest data visualizations for political intelligence data.

## Chart Selection Guide
| Data Type | Recommended Chart |
|-----------|------------------|
| Comparison | Bar chart, grouped bar |
| Trend over time | Line chart, area chart |
| Part-to-whole | Pie/donut, stacked bar |
| Distribution | Histogram, box plot |
| Correlation | Scatter plot |
| Relationships | Network diagram, force graph |
| Geographic | Choropleth map |
| Hierarchical | Treemap, sunburst |

## Design Principles
1. **Data-ink ratio** — Maximize data, minimize decoration
2. **Clarity** — Clear labels, legends, and titles
3. **Honesty** — No misleading scales or truncated axes
4. **Accessibility** — WCAG 2.1 AA compliant colors and patterns
5. **Responsiveness** — Adapt to screen sizes
6. **Interactivity** — Tooltips, zoom, filter where appropriate

## Color Guidelines
- Use colorblind-safe palettes
- Maintain 4.5:1 contrast ratio for text
- Use patterns/textures as secondary encoding
- Follow cyberpunk theme variables
- Limit to 7±2 colors per chart

## Political Data Considerations
- Show confidence intervals for predictions
- Include data source attribution
- Indicate data freshness/staleness
- Support party-specific color coding
- Handle missing data transparently

## Performance
- Canvas for large datasets (>1000 points)
- SVG for interactive/accessible charts
- Lazy load charts below the fold
- Optimize re-renders on data updates

## Related Policies
- [Secure Development Policy](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Secure_Development_Policy.md)
