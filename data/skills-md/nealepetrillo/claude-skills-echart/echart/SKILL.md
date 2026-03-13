---
name: echart
description: Create and edit Apache ECharts v6 visualizations. Use when users want to build interactive charts, dashboards, or data visualizations. Supports line, bar, pie, scatter, radar, heatmap, treemap, sunburst, gauge, chord, and 20+ other chart types. Generates working HTML, JavaScript, React, or Vue component code.
---

# ECharts v6 Visualization Skill

Create professional, accessible data visualizations using Apache ECharts v6.

**Version**: ECharts 6.x | Download: https://github.com/apache/echarts/releases

- **Design guidelines** (color palettes, chart selection, accessibility): see `references/design-principles.md`
- **Detailed code examples** (all chart types): see `references/chart-examples.md`

## Installation

Download from GitHub releases: https://github.com/apache/echarts/releases

**Files to download:**
- `echarts.min.js` - Full minified build (recommended)
- `echarts.js` - Full unminified build (for debugging)

Place the file in your project (e.g., `./lib/echarts.min.js` or `./vendor/echarts.min.js`).

## Core Pattern

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./lib/echarts.min.js"></script>
</head>
<body>
  <div id="chart" style="width: 800px; height: 500px;"></div>
  <script>
    const chart = echarts.init(document.getElementById('chart'));
    const option = {
      // Configuration goes here
    };
    chart.setOption(option);
    window.addEventListener('resize', () => chart.resize());
  </script>
</body>
</html>
```

### CDN (Only if explicitly requested)

```html
<script src="https://cdn.jsdelivr.net/npm/echarts@6/dist/echarts.min.js"></script>
```

## Option Structure

The `option` object is the heart of ECharts configuration:

```javascript
const option = {
  title: { text: 'Chart Title', subtext: 'Subtitle', left: 'center' },
  tooltip: { trigger: 'axis' }, // or 'item' for pie/scatter
  legend: { data: ['Series 1', 'Series 2'], top: 'bottom' },
  grid: { left: '10%', right: '10%', bottom: '15%', containLabel: true },
  xAxis: { type: 'category', data: ['A', 'B', 'C'] },
  yAxis: { type: 'value' },
  series: [
    { name: 'Series 1', type: 'bar', data: [10, 20, 30] }
  ],
  toolbox: { feature: { saveAsImage: {}, dataZoom: {} } },
  dataZoom: [{ type: 'slider', start: 0, end: 100 }],
  color: ['#4477AA', '#EE6677', '#228833', '#CCBB44', '#66CCEE', '#AA3377'] // Paul Tol Bright
};
```

## Chart Types Reference

### Cartesian Charts (use xAxis/yAxis)
- `line` - Line charts, area charts (with `areaStyle: {}`)
- `bar` - Vertical/horizontal bar charts (swap xAxis/yAxis types)
- `scatter` - Scatter plots, bubble charts (use `symbolSize`)

### Polar Charts
- `radar` - Radar/spider charts (use `radar` instead of axis)

### Pie-like Charts (no axes needed)
- `pie` - Pie, donut (with `radius: ['40%', '70%']`)
- `sunburst` - Hierarchical sunburst
- `treemap` - Hierarchical treemap
- `tree` - Tree diagrams

### Statistical
- `boxplot` - Box and whisker plots
- `candlestick` - Financial candlestick charts
- `heatmap` - Heat maps (use with `visualMap`)

### Specialty
- `gauge` - Speedometer-style gauges
- `funnel` - Funnel charts
- `sankey` - Flow diagrams
- `graph` - Network/relationship graphs
- `chord` - Relationship networks with gradient arcs (v6)
- `map` - Geographic maps (requires geo data)
- `parallel` - Parallel coordinates

For code examples of each type, see `references/chart-examples.md`.

## Framework Integration

For vanilla JavaScript projects, use the core pattern above. Wrapper libraries are available for React and Vue with build systems.

### React (with build system)
```jsx
import ReactECharts from 'echarts-for-react';

function MyChart({ data }) {
  const option = {
    xAxis: { type: 'category', data: data.labels },
    yAxis: { type: 'value' },
    series: [{ type: 'bar', data: data.values }]
  };
  return <ReactECharts option={option} style={{ height: 400 }} />;
}
```

### Vue (with build system)
```vue
<template>
  <v-chart :option="option" style="height: 400px" />
</template>

<script setup>
import VChart from 'vue-echarts';
const option = {
  xAxis: { type: 'category', data: ['A', 'B', 'C'] },
  yAxis: { type: 'value' },
  series: [{ type: 'bar', data: [10, 20, 30] }]
};
</script>
```

## Styling

### Responsive Charts
```javascript
window.addEventListener('resize', () => chart.resize());
```

### Dark Theme
```javascript
const chart = echarts.init(container, 'dark');
```

### Tooltip Formatting
```javascript
tooltip: {
  formatter: (params) => `${params.name}: ${params.value.toLocaleString()}`
}
```

### Value Formatting
```javascript
yAxis: {
  axisLabel: {
    formatter: (value) => `$${value / 1000}k`
  }
}
```

### Animations
```javascript
option = {
  animation: true,
  animationDuration: 1000,
  animationEasing: 'cubicOut',
};
```

## ECharts Best Practices

- Always include `tooltip` for data exploration
- Handle resize: `window.addEventListener('resize', () => chart.resize())`
- Use `chart.showLoading()` / `chart.hideLoading()` for async data
- Tooltips supplement, not replace — key data should be visible without hover

For design best practices (color, accessibility, chart selection): see `references/design-principles.md`.

## ECharts v6 Features

### New in v6
- **Chord Chart** - Relationship networks with gradient coloring
- **Beeswarm/Jitter** - `jitter` and `jitterOverlap: false` for dense scatter data
- **Dynamic Theme Switching** - `chart.setTheme('dark')` without reinitializing
- **Dark Mode Support** - Auto-adapts to system preferences
- **Broken Axis** - For data with large magnitude differences

### v6 Breaking Changes
```javascript
// v6 has new default theme. To use v5 color palette:
const v5Colors = ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc'];
const option = { color: v5Colors, /* ... */ };

// Rich text now inherits from plain label styles by default
// To restore v5 behavior:
const option = { richInheritPlainLabel: false };
```

### Dynamic Theme Switching (v6)
```javascript
const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
mediaQuery.addEventListener('change', (e) => {
  chart.setTheme(e.matches ? 'dark' : 'light');
});
```

## Resources

- Documentation: https://echarts.apache.org/en/option.html
- Examples: https://echarts.apache.org/examples/en/index.html
- v6 Features: https://echarts.apache.org/handbook/en/basics/release-note/v6-feature
- v6 Upgrade Guide: https://echarts.apache.org/handbook/en/basics/release-note/v6-upgrade-guide
- `references/design-principles.md` - Color palettes, chart selection, accessibility guidelines
- `references/chart-examples.md` - Detailed code examples for all chart types
- Paul Tol's Color Schemes: https://personal.sron.nl/~pault/
