---
name: data-visualization-mastery
description: "50+ chart types with selection criteria, dashboard composition, data tables, KPI cards, sparklines, heatmaps, and accessible data presentation, with React code (Recharts, D3, Nivo) and data-viz tokens. Use when designing charts, dashboards, or any data-dense screen."
---

# Data Visualization Mastery

## Why Data Visualization Mastery Matters

Data visualization is the art and science of encoding information visually so humans can perceive patterns, outliers, and trends faster than reading raw numbers. A poorly chosen chart misleads. A poorly designed chart confuses. A well-designed chart tells the truth instantly. This skill codifies the principles of Edward Tufte, Stephen Few, Jacques Bertin, and Tamara Munzner into a systematic framework for building data-dense UIs that are beautiful, honest, and accessible.

The gap between a developer-built dashboard and a professionally designed data experience is systematic craft: choosing the right chart type, encoding data correctly, managing visual hierarchy across dozens of data points, and ensuring every pixel of ink serves the data.

## Reference Architecture

| File | Contents | Use When |
|------|----------|----------|
| `references/chart-type-encyclopedia.md` | 50+ chart types organized by purpose (comparison, trend, distribution, relationship, part-to-whole, flow, geo, hierarchy). Each chart: when to use, when NOT to use, data shape, max data points, design specs (colors, spacing, typography, gridlines), accessibility notes, thumbnail description. | Selecting the right chart for a dataset. Reviewing chart design specs. Auditing chart choices in an existing UI. |
| `references/dashboard-layout-patterns.md` | 30+ dashboard layout patterns: KPI rows, chart grids, filter bars, drill-down hierarchies, real-time monitoring, executive summary, operational, analytical, mobile card-stack. Each: CSS grid layout, spacing, component hierarchy, responsive collapse strategy. | Designing dashboard layouts. Reviewing dashboard information architecture. Building responsive analytics UIs. |
| `references/data-table-mastery.md` | Complete data table design system: anatomy, column types (15+), sorting, filtering, pagination, selection, expansion, fixed headers, inline editing, cell formatting, empty/loading states, responsive strategies, density modes, full accessibility spec, production React/TypeScript code. | Designing or building data tables. Auditing table usability. Adding features to existing tables. |
| `references/dataviz-accessibility.md` | Dataviz accessibility: alt text patterns for every chart type, data table alternatives, 8 colorblind-safe palettes with hex codes, pattern fills, high contrast mode, screen reader announcements, keyboard navigation, sonification, WCAG success criteria mapping. | Making charts accessible. Auditing dataviz accessibility. Building inclusive dashboards. |
| `references/dataviz-code-patterns.md` | Production code for top 20 chart types using Recharts (React). Chart wrapper component with loading/error/empty states. Design tokens for dataviz. Responsive containers. Theme integration. Tooltip and legend customization. Print styles. | Implementing charts in React. Building chart component libraries. Setting up dataviz design tokens. |

## Cross-References

- **`visual-design-mastery`** -- Color science (oklch, palette generation) applies directly to dataviz color palettes. Typography mastery (tabular figures, alignment) is critical for number-heavy UIs.
- **`ui-pattern-intelligence`** -- Dashboard and table patterns at the component level. This skill provides the deeper dataviz-specific design intelligence.
- **`accessibility-inclusive-design`** -- WCAG foundation. This skill extends it with dataviz-specific accessibility patterns.
- **`component-patterns-code`** -- Component architecture. This skill provides dataviz-specific component patterns and code.
- **`design-systems-architecture`** -- Token architecture. This skill defines dataviz-specific tokens (chart colors, gridlines, axes).
- **`performance-states-patterns`** -- Loading, error, and empty states apply to every chart and table component.
- **`cognitive-psychology-ux`** -- Perceptual principles (pre-attentive processing, Gestalt grouping) underpin all visual encoding decisions.

---

## 1. Foundational Principles

### 1.1 Edward Tufte's Core Principles

**Data-Ink Ratio:** Maximize the share of ink devoted to data. Every pixel that does not encode data should be questioned and likely removed. Remove chartjunk: decorative gridlines, 3D effects, gradient fills, drop shadows on bars, unnecessary legends, redundant labels.

```
Data-Ink Ratio = (Data Ink) / (Total Ink Used in the Graphic)
Target: > 0.8
```

**Lie Factor:** The size of an effect shown in the graphic divided by the size of the effect in the data. A lie factor of 1.0 is truthful. Above 1.05 or below 0.95 is distortion.

```
Lie Factor = (Size of effect in graphic) / (Size of effect in data)
Acceptable range: 0.95 - 1.05
```

**Chartjunk Checklist -- Remove These:**
- 3D effects on 2D data (bars, pies)
- Gradient fills that imply data variation where none exists
- Decorative background images
- Heavy gridlines that compete with data
- Redundant legends (when labels are directly on data)
- Unnecessary borders and boxes
- Excessive decimal places
- Animated entrances that delay comprehension

**Small Multiples:** When comparing across categories or time periods, use small multiples (the same chart repeated with different data) rather than cramming everything into one chart. Same scale, same axes, same visual encoding -- only the data changes.

### 1.2 Visual Encoding Hierarchy (Jacques Bertin + Cleveland & McGill)

Humans decode visual channels with different accuracy. Always use the most accurate channel for the most important data dimension:

```
MOST ACCURATE (use first)
  1. Position on a common scale (bar chart, dot plot, scatter plot)
  2. Position on non-aligned scales (small multiples)
  3. Length (bar chart)
  4. Direction / Angle (slope, but NOT pie chart angles)
  5. Area (bubble chart, treemap)
  6. Volume (3D -- almost never use)
  7. Color saturation / Luminance (heatmap, choropleth)
  8. Color hue (categorical encoding only)
LEAST ACCURATE (use last)
```

**Practical implication:** A bar chart (position + length) will ALWAYS be more accurately read than a pie chart (angle + area). Use pie charts only when part-to-whole relationship matters more than precise comparison, and only with 2-5 slices.

### 1.3 Stephen Few's Dashboard Design Principles

1. **Fit on a single screen** -- no scrolling for the primary view
2. **Group related information** using Gestalt proximity and enclosure
3. **Place the most important information top-left** (F-pattern scanning)
4. **Use consistent visual encoding** across all charts on the dashboard
5. **Provide context** -- comparison values, targets, historical ranges
6. **Highlight what matters** -- use pre-attentive attributes (color, size) to draw attention to exceptions, not to decorate
7. **Minimize non-data pixels** -- every border, background, and separator should earn its place
8. **Support progressive disclosure** -- summary first, details on demand

### 1.4 Tamara Munzner's Nested Model

Four levels of visualization design, each validated differently:

| Level | Question | Validation |
|-------|----------|------------|
| **Domain situation** | Who are the users? What are their tasks? | Observe users in context |
| **Data/task abstraction** | What data types? What analytical tasks? | Test task completion |
| **Visual encoding/interaction** | What marks and channels? What interactions? | Perceptual experiments |
| **Algorithm** | How to compute and render efficiently? | Performance benchmarks |

---

## 2. Chart Selection Decision Framework

### 2.1 By Analytical Purpose

| Purpose | Best Charts | Avoid |
|---------|-------------|-------|
| **Compare values** | Bar (horizontal for many categories), Column, Dot plot, Lollipop | Pie (bad for comparison), Radar (distorts) |
| **Show trend over time** | Line, Area, Sparkline, Slope chart | Bar (unless discrete periods), Pie |
| **Show part-to-whole** | Stacked bar (100%), Treemap, Donut (2-5 parts), Waffle | Pie (>5 slices), Stacked area (hard to read middle layers) |
| **Show distribution** | Histogram, Box plot, Violin, Density, Strip plot | Bar chart (not the same as histogram) |
| **Show relationship** | Scatter, Bubble, Correlation matrix | Line chart (implies time sequence) |
| **Show flow/process** | Sankey, Funnel, Alluvial | Pie, Bar |
| **Show geographic data** | Choropleth, Bubble map, Heat map | Bar chart (loses spatial context) |
| **Show hierarchy** | Treemap, Sunburst, Circle packing, Dendrogram | Pie (flat, no hierarchy) |
| **Show composition over time** | Stacked area, Stream graph | Multiple pie charts over time |

### 2.2 By Data Shape

| Data Shape | Recommended |
|------------|-------------|
| 1 number (KPI) | KPI card with delta, sparkline, context |
| 1 categorical + 1 quantitative | Bar/Column chart |
| 1 time + 1 quantitative | Line chart |
| 1 time + multiple quantitative | Multi-series line, Small multiples |
| 2 quantitative | Scatter plot |
| 3 quantitative | Bubble chart (3rd = size) |
| 1 categorical + parts | Stacked bar, Treemap |
| Hierarchical categories + 1 quantitative | Treemap, Sunburst |
| Source to Target + flow magnitude | Sankey diagram |
| Geographic + 1 quantitative | Choropleth |
| Matrix (rows x cols x value) | Heatmap |

### 2.3 By Audience

| Audience | Approach |
|----------|----------|
| **Executive** | KPI cards, sparklines, single-number summaries, traffic lights. Max 5-7 data points visible. Summary first, drill-down available. |
| **Analyst** | Interactive charts, filters, cross-filtering, tooltips with detail. Support exploration. Higher data density acceptable. |
| **General public** | Simple charts (bar, line, donut). Annotations explaining "what this means." No jargon. Large text. |
| **Domain expert** | Specialized chart types acceptable (candlestick for finance, survival curves for medicine). Dense data OK. |

---

## 3. Color for Data Visualization

### 3.1 Palette Types

**Sequential** (low to high): Single hue varying in lightness. Use for ordered data (temperature, population, revenue).
```
Example (Blue sequential):
#f7fbff -> #deebf7 -> #c6dbef -> #9ecae1 -> #6baed6 -> #4292c6 -> #2171b5 -> #084594
```

**Diverging** (negative <- neutral -> positive): Two hues diverging from a neutral midpoint. Use for data with a meaningful center (profit/loss, above/below average, sentiment).
```
Example (Red-Blue diverging):
#b2182b -> #d6604d -> #f4a582 -> #fddbc7 -> #f7f7f7 -> #d1e5f0 -> #92c5de -> #4393c3 -> #2166ac
```

**Categorical** (distinct groups): Maximally distinct hues at similar lightness. Use for nominal categories (product lines, regions, user segments). Maximum 8-10 colors before confusion.
```
Colorblind-safe categorical (8 colors):
#4e79a7  #f28e2b  #e15759  #76b7b2  #59a14f  #edc948  #b07aa1  #ff9da7
(Tableau 10 subset -- optimized for distinguishability including colorblind viewers)
```

### 3.2 Colorblind-Safe Design Rules

1. **Never use red/green as the only differentiator** -- 8% of males have red-green deficiency
2. **Use lightness variation** in addition to hue -- colorblind viewers can still distinguish light from dark
3. **Add redundant encoding** -- patterns, labels, icons, or position in addition to color
4. **Test with simulation** -- Sim Daltonism (macOS), Color Oracle, or Figma colorblind plugins
5. **Use pre-tested palettes** -- see `references/dataviz-accessibility.md` for 8 verified palettes

### 3.3 Color Assignment Rules

- **Semantic colors** should be respected: red = danger/loss/down, green = success/gain/up, blue = information/neutral, yellow/amber = warning
- **Gray for context**, saturated color for focal data -- e.g., gray bars for all categories, blue bar for the selected one
- **Consistent mapping** -- if "Product A" is blue on chart 1, it must be blue on chart 2
- **White/light background** for charts -- data should be the most visually prominent element
- **No more than 8 categorical colors** -- group remaining into "Other"

---

## 4. Typography for Data-Dense UI

### 4.1 Tabular (Monospace) Figures

Numbers in tables and charts MUST use tabular figures (all digits occupy the same width) so columns align perfectly. Most professional fonts include a `font-feature-settings: "tnum"` OpenType feature.

```css
/* Enable tabular figures for all data displays */
.dataviz-number,
.table-cell-number,
.kpi-value {
  font-feature-settings: "tnum" 1;
  font-variant-numeric: tabular-nums;
}
```

**Fonts with excellent tabular figures:** Inter, IBM Plex Sans, Roboto, SF Pro, DM Sans, JetBrains Mono.

### 4.2 Number Formatting Rules

| Context | Format | Example |
|---------|--------|---------|
| Currency | Symbol + comma grouping + 2 decimal | $1,234,567.89 |
| Large currency | Abbreviate with suffix | $1.2M, $3.4B |
| Percentage | 1 decimal max, % symbol | 45.2% |
| Large numbers | Comma grouping or abbreviate | 1,234,567 or 1.2M |
| Dates in tables | Consistent format, sortable | 2026-03-12 or Mar 12, 2026 |
| Deltas/changes | Sign + color + arrow | +12.3% with green up-arrow |
| Negative numbers | Parentheses or minus + red | ($1,234) or -$1,234 |

### 4.3 Alignment Rules

- **Numbers:** Right-align (decimal points line up)
- **Text:** Left-align
- **Headers:** Match cell alignment (right-align number headers, left-align text headers)
- **Dates:** Left-align or right-align consistently
- **Status/tags:** Center-align
- **Actions:** Right-align or center-align

### 4.4 Type Scale for Dashboards

```
KPI hero number:     32-48px, font-weight 700
KPI label:           12-14px, font-weight 500, text-transform uppercase, letter-spacing 0.05em, muted color
Chart title:         16-18px, font-weight 600
Axis labels:         11-12px, font-weight 400, muted color
Axis tick labels:    10-11px, font-weight 400, muted color
Tooltip title:       13-14px, font-weight 600
Tooltip value:       13-14px, font-weight 400
Data label on chart: 11-12px, font-weight 500
Table header:        12-13px, font-weight 600, text-transform uppercase, letter-spacing 0.03em
Table cell:          13-14px, font-weight 400
```

---

## 5. Grid and Spacing for Dashboards

### 5.1 Dashboard Grid System

```
Container max-width: 1440px (centered)
Outer padding:       24px (desktop), 16px (tablet), 12px (mobile)
Column grid:         12 columns, 24px gutter
Card padding:        20-24px
Card border-radius:  8-12px
Card gap:            16-24px
Chart minimum height: 240px (desktop), 180px (mobile)
KPI card height:     ~120px
```

### 5.2 Chart Internal Spacing

```
Chart title to chart area:    12-16px
Chart area to legend:         16-20px
Axis label to axis line:      8px
Axis tick label to axis line: 4px
Gridline opacity:             0.1-0.15 (barely visible)
Bar gap (within group):       2-4px
Bar gap (between groups):     8-16px (> within-group gap)
Minimum bar width:            12px
Line stroke width:            2px (primary), 1.5px (secondary)
Data point dot radius:        4px (hover: 6px)
Tooltip offset from cursor:   8-12px
```

---

## 6. Animation and Interaction in Dataviz

### 6.1 When to Animate

**DO animate:**
- Data transitions (values changing from old to new)
- Chart type transitions (bar morphing to line)
- Progressive data loading (bars growing from zero)
- Hover states (tooltip appearance, highlight active series)
- Drill-down transitions (zooming into a segment)

**DO NOT animate:**
- Initial page load with complex entrance sequences (delays comprehension)
- Gratuitous bouncing, spinning, or pulsing
- Decorative animations that do not encode data
- Anything that takes > 500ms before data is readable

### 6.2 Transition Timing

```css
/* Dataviz transition tokens */
--dataviz-transition-fast:    150ms ease-out;   /* hover highlights */
--dataviz-transition-medium:  300ms ease-in-out; /* data updates */
--dataviz-transition-slow:    500ms ease-in-out; /* chart type changes */
--dataviz-tooltip-delay:      200ms;             /* tooltip show delay */
--dataviz-tooltip-duration:   150ms ease-out;    /* tooltip fade in */
```

### 6.3 Interaction Patterns

| Interaction | Purpose | Implementation |
|-------------|---------|----------------|
| **Hover tooltip** | Show exact value for a data point | Appears after 200ms delay, follows cursor or anchors to point |
| **Click to filter** | Select a category to filter other charts | Click a bar/legend item, other charts cross-filter |
| **Brush selection** | Select a time range | Click-drag on time axis, zooms or filters to selection |
| **Zoom** | Explore dense data | Scroll to zoom, pinch on mobile, reset button always visible |
| **Pan** | Navigate large datasets | Click-drag on chart area (when zoomed), or scroll on time axis |
| **Toggle series** | Show/hide data series | Click legend items, hidden items gray out |
| **Drill-down** | Navigate hierarchy | Click a bar segment or treemap cell to see children |
| **Cross-filter** | Link multiple charts | Selection in one chart filters all related charts |

---

## 7. KPI Card Design

### 7.1 Anatomy of a KPI Card

```
+-------------------------------+
|  Revenue          *  Live     |  <- Label (12px, muted) + Status indicator
|                               |
|  $2.4M                        |  <- Hero value (36px, bold, tabular figures)
|  ^ 12.3% vs last month       |  <- Delta (14px, green + up arrow)
|                               |
|  ~~~~~~~~~~~~~~~~~~~~~~~~     |  <- Sparkline (past 30 days)
|                               |
|  Target: $2.1M   On track    |  <- Context line (12px, muted)
+-------------------------------+
```

### 7.2 KPI Card Rules

1. **One number per card** -- the hero metric should be instantly readable
2. **Always show context** -- delta (change), target, previous period, or benchmark
3. **Use semantic color for delta** -- green (positive/good), red (negative/bad), gray (neutral)
4. **Sparkline adds trend** without taking much space -- use 30-90 day window
5. **Label should be the dimension**, not "KPI" or "Metric"
6. **Consistent card height** across a row of KPIs
7. **3-5 KPIs per row** on desktop, stack to 1-2 per row on mobile

### 7.3 Delta Formatting

```
Positive good:  ^ 12.3%  (green, #16a34a)
Positive bad:   ^ 12.3%  (red, #dc2626) -- e.g., churn rate going up
Negative good:  v  8.1%  (green, #16a34a) -- e.g., error rate going down
Negative bad:   v  8.1%  (red, #dc2626)
No change:      -  0.0%  (gray, #6b7280)
```

---

## 8. Data Density and Information Architecture

### 8.1 Density Spectrum

| Level | Data Points Visible | Use For |
|-------|---------------------|---------|
| **Glanceable** | 3-7 | Executive KPIs, status monitors |
| **Scannable** | 8-30 | Standard dashboards, summary reports |
| **Explorable** | 30-200 | Analyst tools, detailed reports |
| **Dense** | 200-1000+ | Trading terminals, monitoring walls, scientific viz |

### 8.2 Progressive Disclosure for Data

```
Level 0: KPI number (visible on dashboard)
Level 1: KPI + sparkline + delta (visible on dashboard card)
Level 2: Full chart with tooltip details (click KPI card)
Level 3: Data table behind the chart (click "View data" link)
Level 4: Raw data export (click "Export CSV")
```

### 8.3 Information Scent

Every data point should provide "scent" of what detail lies beneath:
- KPI cards should look clickable if they drill down
- Chart segments should highlight on hover if they have detail
- Truncated table cells should show full content on hover
- "See more" or "View all" links when data is summarized

---

## 9. Dataviz Anti-Patterns

### 9.1 The Deadly Sins of Data Visualization

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| **Truncated Y-axis** | Bar chart not starting at 0 exaggerates differences | Always start bar charts at 0. Line charts may start at non-zero if clearly labeled |
| **Dual Y-axis** | Two different scales on left/right mislead about correlation | Use two separate charts, or normalize to same scale |
| **Pie chart > 5 slices** | Unreadable, angles are hard to compare | Use horizontal bar chart sorted by value |
| **3D charts** | Distorts visual encoding, pure decoration | Use 2D always |
| **Rainbow color scale** | Not perceptually uniform, misleading | Use sequential or diverging scale |
| **Too many series** | Spaghetti chart, impossible to follow | Highlight 1-2, gray out rest, or use small multiples |
| **Missing context** | Numbers without comparison are meaningless | Add targets, benchmarks, previous period, % change |
| **Overloaded dashboard** | Everything crammed together, nothing stands out | Reduce to 5-7 charts max, use progressive disclosure |
| **Inconsistent time scales** | One chart monthly, next chart daily, side by side | Standardize time scale across related charts |
| **Decorative gradients** | Imply data variation where none exists | Use flat fills |

### 9.2 Common Developer Mistakes

1. **Using the default chart library theme** -- always customize colors, fonts, spacing to match your design system
2. **Ignoring responsive behavior** -- charts should resize, not just scale down
3. **No loading states** -- show skeleton/shimmer while data loads
4. **No empty states** -- show a message when there is no data, not a blank chart
5. **No error states** -- show a clear error message when API fails, not a broken chart
6. **Tooltips clipped by container** -- ensure tooltips flip when near edges
7. **Legend taking up chart space** -- move legend below chart on mobile, or use direct labels
8. **Axis labels overlapping** -- rotate, abbreviate, or reduce ticks
9. **Not respecting prefers-reduced-motion** -- disable chart animations when user requests

---

## 10. Responsive Dataviz Strategy

### 10.1 Breakpoint Behavior

| Component | Desktop (>1024px) | Tablet (768-1024px) | Mobile (<768px) |
|-----------|-------------------|---------------------|-----------------|
| KPI row | 4-5 cards horizontal | 3 cards, wrap to 2 rows | 2 cards per row, stack |
| Chart | Full size, tooltips | Slightly smaller, tooltips | Full width, simplified |
| Legend | Right side or top | Below chart | Below chart, scrollable |
| Data table | Full columns visible | Hide low-priority columns | Card view or horizontal scroll |
| Filters | Sidebar or top bar | Top bar, collapsible | Bottom sheet or modal |
| Dashboard | 12-col grid | 8-col grid | Single column stack |

### 10.2 Mobile Chart Adaptations

- **Reduce data points** -- aggregate daily to weekly, or show top 10 instead of all
- **Increase touch targets** -- data points need 44x44px touch area
- **Simplify axis labels** -- abbreviate months (Jan, Feb), use K/M for numbers
- **Move legend below** -- side legends compress chart too much
- **Use horizontal bar** instead of vertical column (easier to read labels)
- **Support swipe** for time-based charts (pan through time)
- **Full-screen mode** for complex charts (tap to expand)

---

## 11. Dataviz Design Tokens

### 11.1 Token Definitions

```css
/* Chart Colors -- Categorical */
--dataviz-categorical-1: #4e79a7;
--dataviz-categorical-2: #f28e2b;
--dataviz-categorical-3: #e15759;
--dataviz-categorical-4: #76b7b2;
--dataviz-categorical-5: #59a14f;
--dataviz-categorical-6: #edc948;
--dataviz-categorical-7: #b07aa1;
--dataviz-categorical-8: #ff9da7;

/* Chart Colors -- Sequential (blue) */
--dataviz-sequential-1: #f7fbff;
--dataviz-sequential-2: #deebf7;
--dataviz-sequential-3: #c6dbef;
--dataviz-sequential-4: #9ecae1;
--dataviz-sequential-5: #6baed6;
--dataviz-sequential-6: #4292c6;
--dataviz-sequential-7: #2171b5;
--dataviz-sequential-8: #084594;

/* Chart Colors -- Diverging (red-blue) */
--dataviz-diverging-negative-4: #b2182b;
--dataviz-diverging-negative-3: #d6604d;
--dataviz-diverging-negative-2: #f4a582;
--dataviz-diverging-negative-1: #fddbc7;
--dataviz-diverging-neutral:    #f7f7f7;
--dataviz-diverging-positive-1: #d1e5f0;
--dataviz-diverging-positive-2: #92c5de;
--dataviz-diverging-positive-3: #4393c3;
--dataviz-diverging-positive-4: #2166ac;

/* Chart Colors -- Semantic */
--dataviz-positive: #16a34a;
--dataviz-negative: #dc2626;
--dataviz-warning:  #d97706;
--dataviz-neutral:  #6b7280;

/* Chart Structure */
--dataviz-grid-color: #e5e7eb;
--dataviz-grid-opacity: 0.15;
--dataviz-axis-color: #9ca3af;
--dataviz-axis-width: 1px;
--dataviz-tick-length: 4px;
--dataviz-line-width: 2px;
--dataviz-line-width-secondary: 1.5px;
--dataviz-point-radius: 4px;
--dataviz-point-radius-hover: 6px;
--dataviz-bar-radius: 4px 4px 0 0;
--dataviz-bar-gap: 4px;
--dataviz-bar-group-gap: 12px;

/* Tooltip */
--dataviz-tooltip-bg: #1f2937;
--dataviz-tooltip-text: #f9fafb;
--dataviz-tooltip-border-radius: 6px;
--dataviz-tooltip-padding: 8px 12px;
--dataviz-tooltip-shadow: 0 4px 12px rgba(0,0,0,0.15);
--dataviz-tooltip-max-width: 240px;

/* Typography */
--dataviz-font-family: 'Inter', system-ui, sans-serif;
--dataviz-font-mono: 'JetBrains Mono', 'SF Mono', monospace;
--dataviz-kpi-size: 36px;
--dataviz-kpi-weight: 700;
--dataviz-label-size: 12px;
--dataviz-label-weight: 500;
--dataviz-axis-label-size: 11px;
--dataviz-title-size: 16px;
--dataviz-title-weight: 600;

/* Spacing */
--dataviz-chart-min-height: 240px;
--dataviz-chart-padding: 20px;
--dataviz-card-padding: 20px;
--dataviz-card-gap: 16px;
--dataviz-card-radius: 8px;
```

### 11.2 Dark Mode Overrides

```css
[data-theme="dark"] {
  --dataviz-grid-color: #374151;
  --dataviz-axis-color: #6b7280;
  --dataviz-tooltip-bg: #f9fafb;
  --dataviz-tooltip-text: #1f2937;
  --dataviz-positive: #22c55e;
  --dataviz-negative: #ef4444;
  --dataviz-warning: #f59e0b;

  /* Lighten categorical colors for dark backgrounds */
  --dataviz-categorical-1: #6ba3d6;
  --dataviz-categorical-2: #f5a855;
  --dataviz-categorical-3: #e87b7d;
  --dataviz-categorical-4: #93cec9;
  --dataviz-categorical-5: #7dbd72;
  --dataviz-categorical-6: #f0d56e;
  --dataviz-categorical-7: #c499b8;
  --dataviz-categorical-8: #ffb4bc;
}
```

---

## 12. Print Optimization for Dataviz

### 12.1 Print CSS

```css
@media print {
  /* Remove interactive elements */
  .chart-tooltip,
  .chart-legend-toggle,
  .chart-zoom-controls,
  .dashboard-filter-bar { display: none; }

  /* Force white background */
  .chart-container,
  .dashboard-card { background: white !important; }

  /* Ensure visible borders for cards */
  .dashboard-card { border: 1px solid #d1d5db !important; }

  /* Increase contrast for print */
  .chart-gridline { opacity: 0.3 !important; }
  .chart-axis-label { color: #111827 !important; }

  /* Avoid page breaks inside charts */
  .dashboard-card { break-inside: avoid; }
  .chart-container { break-inside: avoid; }

  /* Ensure chart colors print distinctly */
  .chart-series { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
}
```

---

## 13. Quality Checklist: Dataviz Review

Use this checklist when reviewing any chart, graph, or dashboard:

### Data Integrity
- [ ] Chart type matches the analytical purpose
- [ ] Y-axis starts at 0 for bar charts
- [ ] Scales are clearly labeled with units
- [ ] No misleading truncation or distortion (lie factor ~1.0)
- [ ] Time axis direction is left-to-right, past-to-present
- [ ] Data source and last-updated timestamp visible

### Visual Design
- [ ] Data-ink ratio > 0.8 (minimal chartjunk)
- [ ] Consistent color mapping across all charts
- [ ] Categorical palette limited to 8 or fewer colors
- [ ] Sufficient contrast between data series
- [ ] Tabular figures enabled for all numbers
- [ ] Numbers right-aligned in tables
- [ ] Gridlines subtle (opacity 0.1-0.15)
- [ ] No 3D effects, no decorative gradients

### Accessibility
- [ ] Alt text describes the chart's key insight (not just "a bar chart")
- [ ] Data table alternative available for screen readers
- [ ] Colorblind-safe palette used
- [ ] Redundant encoding (not just color: shape, pattern, or label too)
- [ ] Keyboard navigable (for interactive charts)
- [ ] High contrast mode supported
- [ ] prefers-reduced-motion respected

### Responsiveness
- [ ] Charts resize gracefully (not just CSS scale)
- [ ] Mobile layout tested (card stack, simplified axes)
- [ ] Touch targets >= 44x44px for interactive elements
- [ ] Tooltips do not clip at container edges
- [ ] Legend repositions on narrow viewports

### States
- [ ] Loading state (skeleton/shimmer)
- [ ] Empty state (message + illustration)
- [ ] Error state (message + retry action)
- [ ] Partial data state (missing data points handled gracefully)

---

## Usage Examples

### When User Says: "I need a chart for this data"
1. Ask about the analytical purpose (compare, trend, distribution, relationship)
2. Ask about the data shape (dimensions, measures, cardinality)
3. Consult chart-type-encyclopedia.md for the recommended chart type
4. Provide design specs from the encyclopedia entry
5. Provide code pattern from dataviz-code-patterns.md

### When User Says: "Design a dashboard for..."
1. Identify the dashboard type (executive, operational, analytical)
2. Consult dashboard-layout-patterns.md for the matching layout
3. Select appropriate chart types for each data panel
4. Apply KPI card design from section 7
5. Ensure responsive behavior from section 10

### When User Says: "Make this chart accessible"
1. Consult dataviz-accessibility.md for the specific chart type
2. Write alt text following the pattern
3. Provide a data table alternative
4. Check color palette against colorblind simulation
5. Add keyboard navigation if interactive

### When User Says: "Build a data table"
1. Consult data-table-mastery.md for full spec
2. Determine column types, sorting, filtering needs
3. Select responsive strategy
4. Apply accessibility requirements (role=grid, aria-sort)
5. Provide production code pattern
