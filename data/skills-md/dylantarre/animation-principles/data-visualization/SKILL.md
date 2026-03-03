---
name: data-visualization
description: Use when animating charts, graphs, dashboards, data transitions, or any information visualization work.
---

# Data Visualization Animation

Apply Disney's 12 animation principles to charts, graphs, dashboards, and information displays.

## Quick Reference

| Principle | Data Viz Implementation |
|-----------|------------------------|
| Squash & Stretch | Bar overshoot, elastic settling |
| Anticipation | Brief pause before data loads |
| Staging | Sequential reveal, focus hierarchy |
| Straight Ahead / Pose to Pose | Streaming vs snapshot data |
| Follow Through / Overlapping | Staggered element entry |
| Slow In / Slow Out | Smooth value interpolation |
| Arc | Pie chart sweeps, flow diagrams |
| Secondary Action | Labels following data points |
| Timing | Entry 300-500ms, updates 200-300ms |
| Exaggeration | Emphasize significant changes |
| Solid Drawing | Consistent scales, clear relationships |
| Appeal | Satisfying reveals, professional polish |

## Principle Applications

**Squash & Stretch**: Bars can overshoot target height then settle. Pie slices expand slightly on hover. Bubbles compress on collision. Keep total values accurate—animation is transitional.

**Anticipation**: Brief loading state before data appears. Slight shrink before expansion. Counter briefly pauses before rapid counting. Prepares user for incoming information.

**Staging**: Reveal data in meaningful sequence—most important first. Highlight active data series. Dim unrelated elements during focus. Guide the data story with motion.

**Straight Ahead vs Pose to Pose**: Real-time streaming data animates continuously (straight ahead). Dashboard snapshots transition between states (pose to pose). Match approach to data nature.

**Follow Through & Overlapping**: Data points enter with staggered timing. Labels settle after their data elements. Grid lines appear before data. Legends animate with slight delay.

**Slow In / Slow Out**: Value changes ease smoothly—no jarring jumps. Use `d3.easeCubicInOut` or equivalent. Counter animations accelerate then decelerate. Progress bars ease to completion.

**Arc**: Pie charts sweep clockwise from 12 o'clock. Sankey diagram flows follow curved paths. Network graphs use force-directed arcs. Radial charts expand from center.

**Secondary Action**: Tooltips follow data point movement. Value labels count up as bars grow. Axis tick marks respond to scale changes. Shadows indicate data depth.

**Timing**: Initial entry: 300-500ms staggered. Data updates: 200-300ms. Hover states: 100-150ms. Filter transitions: 400-600ms. Slower timing aids comprehension.

**Exaggeration**: Significant changes deserve attention—pulse or glow outliers. Threshold crossings trigger emphasis. Anomalies animate more dramatically. Don't exaggerate the data itself.

**Solid Drawing**: Maintain consistent scales during animation. Transitions shouldn't distort data relationships. Preserve axis alignment. Visual hierarchy must remain clear throughout motion.

**Appeal**: Data entry should feel satisfying. Professional, purposeful motion builds trust. Avoid gratuitous animation—every motion should aid understanding.

## Code Patterns

### D3.js
```javascript
// Staggered bar entry with easing
bars.transition()
    .duration(500)
    .delay((d, i) => i * 50)
    .ease(d3.easeCubicOut)
    .attr("height", d => yScale(d.value))
    .attr("y", d => height - yScale(d.value));

// Smooth data updates
bars.transition()
    .duration(300)
    .ease(d3.easeCubicInOut)
    .attr("height", d => yScale(d.value));
```

### Chart.js
```javascript
// Animation configuration
options: {
    animation: {
        duration: 500,
        easing: 'easeOutQuart',
        delay: (context) => context.dataIndex * 50
    }
}
```

## Data Type Timing

| Visualization | Entry | Update | Hover |
|--------------|-------|--------|-------|
| Bar chart | 400ms stagger | 300ms | 100ms |
| Line chart | 600ms draw | 400ms | 150ms |
| Pie chart | 500ms sweep | 300ms | 100ms |
| Scatter plot | 300ms stagger | 200ms | 100ms |
| Dashboard | 500-800ms cascade | 300ms | 150ms |

## Accessibility Note

Always respect `prefers-reduced-motion`. Data visualization animation should aid comprehension, not hinder it. Provide instant-state fallback for users who disable motion.
