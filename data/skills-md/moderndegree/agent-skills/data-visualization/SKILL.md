---
name: data-visualization
description: Chart selection, data viz accessibility, and dashboard patterns. Use when building charts, graphs, or data dashboards.
version: 1.0.0
---

# Data Visualization

This skill covers data visualization — chart selection, accessibility, and dashboard patterns for presenting data effectively.

## Use-When

This skill activates when:
- Agent builds charts, graphs, or visualizations
- Agent creates dashboards
- Agent displays data to users
- Agent needs to choose appropriate chart types

## Core Rules

- ALWAYS choose chart type based on data relationship (comparison, distribution, etc.)
- ALWAYS provide data tables as alternatives to charts
- ALWAYS label axes and include legends
- ALWAYS use color-blind friendly palettes
- NEVER use 3D charts (distort data)

## Common Agent Mistakes

- Wrong chart type for data
- No labels or legends
- 3D charts that distort perception
- No alternative (table) for accessibility
- Too many data series in one chart

## Examples

### ✅ Correct

```tsx
// Bar chart for comparison
<BarChart 
  data={data} 
  xAxis="month" 
  yAxis="revenue"
  labels={{ x: 'Month', y: 'Revenue' }}
/>
```

### ❌ Wrong

```tsx
// 3D pie chart
<PieChart3D>Data</PieChart3D>
```

## References

- [Data Visualization Guide](https://www.data-visualization.org/)
- [Chart.js Documentation](https://www.chartjs.org/)
