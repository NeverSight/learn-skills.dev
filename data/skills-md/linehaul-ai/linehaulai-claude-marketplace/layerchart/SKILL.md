---
name: layerchart
description: Expert guide for LayerChart, a Svelte component library for building diverse data visualizations (Cartesian, radial, hierarchical, geo, graph) with unopinionated building blocks, motion primitives, and advanced interactions.
keywords: [visualization, charts, svelte, layerchart, data-visualization]
disable-model-invocation: false
user-invocable: true
---

# LayerChart Skill

LayerChart is a comprehensive Svelte visualization framework built on Layer Cake, providing composable components for creating responsive, interactive charts across multiple visualization types.

## Core Architecture

LayerChart operates on a component-based, data-driven philosophy. The library provides three primary categories of components:

**Data-Driven Components** render visual marks directly from data (Area, Bars, Spline, Pie, Sunburst, Treemap, Sankey, etc.). These components automatically handle scale transformations through LayerCake's context.

**Motion-Enabled SVG Primitives** (Rect, Circle, Arc, Group, Line, Path) provide low-level drawing utilities with built-in Svelte transition support for animated data updates.

**Utility Components** handle legends, tooltips, pan/zoom interactions, annotations, and layout operations (hierarchy, geo projections).

## Visualization Types

- **Cartesian**: Bar, Area, Stack, Scatter, Histogram, ClevelandDotPlot, BarStack, BarGroup
- **Radial**: Pie, Arc, Sunburst, Threshold
- **Hierarchical**: Pack, Tree, Treemap, Partition
- **Graph**: Sankey, Link, Graph utilities
- **Geographic**: Choropleth, Spike Map, Bubble Map, GeoTile, GeoPath, StateMap, AnimatedGlobe, Globe projections (Mercator, Azimuthal, Equal Earth, etc.)

## Key Patterns

### Data Preparation

Use LayerChart's data transformation utilities before passing to visualizations:

- `stack()` - converts wide-format data into stacked series with baseline/top values
- `bin()` - groups data into histogram bins with x0/x1 bounds
- `groupLonger()` - pivots wide-format to long-format (one row per value)
- `flatten()` - flattens nested arrays one level, with optional accessor
- `calcExtents()` - calculates min/max across multiple fields, skipping nulls

### Component Composition

All LayerChart visualizations sit within a LayerCake wrapper that establishes scales and context. Child components access scales via Svelte's context API.

```svelte
<LayerCake x="date" y="value" data={data} padding={{...}}>
  <Svg>
    <Area />
    <Line />
    <AxisX />
  </Svg>
  <Canvas>
    <Points />  <!-- High-performance canvas rendering -->
  </Canvas>
  <Html>
    <Tooltip />
  </Html>
</LayerCake>
```

### Interaction Patterns

- **Tooltips**: Position over data with snap-to-data options
- **Pan/Zoom**: Built-in context utilities for interactive navigation
- **Highlighting**: Hover states trigger visual emphasis (opacity, stroke changes)
- **Selection**: Use reactive variables and event handlers for interactive filtering

### Responsive Design

LayerChart automatically handles responsive layouts via `padding` configuration and container dimensions. Components reactively update when data or scales change.

## Common Implementation Tasks

**Bar Charts**: Use `Bars` component with `x` as categorical field. Stack with `BarStack` or group with `BarGroup` for multi-series.

**Time Series**: Configure `xScale={scaleTime()}` with temporal data. Use `AxisX` with `tickFormat` for readable date labels.

**Geographic Visualizations**: Select appropriate projection (Mercator for web maps, Azimuthal for polar), use `GeoPath` for boundaries, `Choropleth` for value mapping.

**High-Volume Data**: Render marks via Canvas instead of SVG for 5000+ points. Layer SVG axes/legends with Canvas for hybrid rendering.

**Stacked/Grouped Series**: Use `stack()` utility to transform data, then render via `AreaStack`/`BarStack` components.

## Performance Considerations

- Canvas rendering for 5000+ points (~60fps on modern hardware)
- SVG for interactive elements and animations (<500 points recommended)
- Hybrid approach: Canvas for marks + SVG for axes/legends
- Scale calculations are reactive—only update scales when data/domain changes
- Memoize expensive data transforms outside component lifecycle

## Styling and Customization

All primitive components support standard SVG/Canvas attributes (stroke, fill, opacity, strokeWidth). Use Svelte's reactive statements for conditional styling based on interaction state or data values.

Gradient fills, patterns, and clipping available via `ClipPath`, `RectClipPath`, `CircleClipPath` components with SVG `<defs>`.

## Integration Notes

- Works seamlessly with D3 scales (linear, time, ordinal, log, threshold)
- Supports multiple render contexts in same chart (SVG + Canvas + HTML)
- Fully accessible with ARIA attributes on SVG elements
- SSR-compatible for server-side rendering in SvelteKit
- Zero external dependencies beyond Svelte and d3-array utilities
