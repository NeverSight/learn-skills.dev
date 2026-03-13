---
name: d3-viz
description: Creates D3.js data visualizations using Tufte principles. Use when the user asks to visualize data, create a chart, build a D3 visualization, or explore data visually.
user_invocable: true
---

# D3 Data Visualization Builder

Creates publication-quality D3.js visualizations grounded in Edward Tufte's information design principles: high data-ink ratio, information density, meaningful annotation, and purposeful interaction. Produces single-file HTML with inline D3 v7.

---

## Workflow Decision Table

Route the user's request to the right mode:

| User intent | Signal words | Action |
|-------------|-------------|--------|
| Direct visualization | "chart", "plot", "graph", "visualize" | Generate standalone HTML → open in browser |
| Chart type help | "what chart", "how should I show", "best way to display" | Consult `reference/d3-gallery.md` → recommend → generate |
| Data exploration | "explore", "play with", "try different", "experiment" | Build D3 playground → see §7 Playground Integration |
| Small multiples | "compare across", "facet by", "each category" | Generate small multiples layout (one chart per group, shared axes) |
| Annotation focus | "annotate", "highlight", "call out", "story" | Generate with heavy annotation layer |

---

## Chart Selection Framework

**Start with the data question, not the chart name.** Walk this decision tree:

### Step 1 — What question is the user asking?

| Question pattern | Category | Go to |
|-----------------|----------|-------|
| "How does X change over time?" | Temporal | `d3-gallery.md` → Temporal |
| "How does X compare to Y?" | Comparison | `d3-gallery.md` → Comparison |
| "How is X distributed / spread?" | Distribution | `d3-gallery.md` → Distribution |
| "How do X and Y relate?" | Correlation | `d3-gallery.md` → Correlation |
| "What are the parts of the whole?" | Composition | `d3-gallery.md` → Composition |
| "How do things connect or flow?" | Flow/Network | `d3-gallery.md` → Flow & Network |
| "Where is X?" | Spatial | `d3-gallery.md` → Spatial |

### Step 2 — Data shape narrows the choice

| Shape | Constraint |
|-------|-----------|
| <20 data points | Prefer dot plot, lollipop, direct-labeled bar |
| 20–500 points | Standard charts: line, bar, scatter |
| 500–5000 points | Consider hexbin, contour, aggregation |
| 5000+ points | Hexbin, density, canvas rendering, or small multiples |
| Hierarchical | Treemap, sunburst, pack, icicle, tree |
| Network/graph | Force-directed, arc, adjacency matrix, chord |

### Step 3 — Select and generate

Read `reference/d3-gallery.md` for the selected chart type to get:
- Key D3 modules needed
- When NOT to use (important for avoiding bad choices)
- Tufte considerations specific to that chart type

---

## Tufte Principles as Code Rules

Apply these rules to every visualization generated. These are non-negotiable.

### 1. Maximize data-ink ratio

**DO:** Remove axis domain lines, minimize tick marks, use subtle reference lines (`stroke-opacity: 0.15`).
**DON'T:** Add gridlines by default, use 3D effects, add drop shadows, use gradient fills on data elements.

```javascript
// After rendering axis:
g.select(".domain").remove();
g.selectAll(".tick line").attr("stroke-opacity", 0.15);
g.selectAll(".tick text").attr("fill", "#888").attr("font-size", "11px");
```

### 2. Direct labels, not legends

**DO:** Label line endpoints, bar values, notable scatter points directly on the chart with matching colors.
**DON'T:** Use a separate legend box unless there are >5 series and direct labeling is impractical.

```javascript
// Direct label at end of each line:
groups.forEach(group => {
  const last = group.values[group.values.length - 1];
  svg.append("text")
    .attr("x", x(last.date) + 6).attr("y", y(last.value))
    .attr("fill", color(group.name)).attr("font-size", "12px")
    .attr("dominant-baseline", "middle")
    .text(group.name);
});
```

### 3. Small multiples over toggles

**DO:** When comparing 4+ subgroups, render one small chart per group in a grid with shared axes.
**DON'T:** Hide groups behind a dropdown selector or toggle that forces sequential viewing.

### 4. Annotate the interesting

**DO:** Add at least one text annotation calling out a peak, drop, crossover, or milestone directly on the chart.
**DON'T:** Leave the chart without any annotation. Every chart tells a story — make it explicit.

```javascript
// Annotation pattern:
svg.append("text")
  .attr("x", x(annotationDate)).attr("y", y(annotationValue) - 16)
  .attr("fill", "#e0e0e0").attr("font-size", "11px").attr("text-anchor", "middle")
  .text("Peak: 1,234 users");
svg.append("line")
  .attr("x1", x(annotationDate)).attr("y1", y(annotationValue) - 10)
  .attr("x2", x(annotationDate)).attr("y2", y(annotationValue) - 2)
  .attr("stroke", "#888").attr("stroke-width", 1);
```

### 5. Color carries meaning

**DO:** Use `d3.schemeTableau10` for categorical data. Use sequential scales (`d3.interpolateBlues`) for quantities. Use diverging scales when there's a meaningful midpoint.
**DON'T:** Use rainbow for sequential data. Use more than 7–8 distinct colors. Add decorative color that doesn't encode data.

### 6. Title is a finding

**DO:** Write the chart title as a key insight: "Revenue doubled after the March campaign".
**DON'T:** Use generic titles like "Revenue over Time". If a descriptive title is truly needed, add the finding as a subtitle.

### 7. Interactions reveal, not decorate

**DO:** Tooltips show additional dimensions. Hover dims non-hovered elements. Brush filters linked views.
**DON'T:** Add bounce animations, elastic easing, or interaction that gates essential data.
Transition duration: ≤300ms. Easing: `d3.easeCubicOut`.

---

## D3 Code Generation Template

Every visualization follows this canonical single-file HTML structure. Adapt as needed but maintain the skeleton.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Insight-based title]</title>
  <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
  <style>
    * { margin: 0; box-sizing: border-box; }
    body {
      background: #1a1a2e; color: #e0e0e0;
      font-family: system-ui, -apple-system, sans-serif;
      display: flex; justify-content: center; align-items: center;
      min-height: 100vh; padding: 24px;
    }
    .chart-container { max-width: 900px; width: 100%; }
    h1 { font-size: 18px; font-weight: 600; margin-bottom: 4px; }
    .subtitle { font-size: 13px; color: #888; margin-bottom: 20px; }
    .source { font-size: 11px; color: #666; margin-top: 12px; }

    /* Axis styles */
    .axis text { fill: #888; font-size: 11px; }
    .axis .domain { display: none; }
    .axis .tick line { stroke: #2a2a4a; stroke-opacity: 0.3; }

    /* Annotation styles */
    .annotation { fill: #e0e0e0; font-size: 11px; }
    .annotation-line { stroke: #888; stroke-width: 1; }

    /* Tooltip */
    .tooltip {
      position: absolute; pointer-events: none;
      background: #16213e; border: 1px solid #2a2a4a;
      border-radius: 4px; padding: 8px 12px;
      font-size: 12px; color: #e0e0e0;
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
      opacity: 0; transition: opacity 0.15s;
    }
  </style>
</head>
<body>
  <div class="chart-container">
    <h1>[Insight title — key finding from the data]</h1>
    <p class="subtitle">[Context: date range, methodology, or secondary finding]</p>
    <div id="chart"></div>
    <p class="source">Source: [data source]</p>
  </div>

  <script>
    // === DATA ===
    const data = [ /* inline data or fetch */ ];

    // === DIMENSIONS (margin convention) ===
    const margin = { top: 20, right: 120, bottom: 40, left: 60 };
    const width = 860 - margin.left - margin.right;
    const height = 480 - margin.top - margin.bottom;

    // === SVG ===
    const svg = d3.select("#chart").append("svg")
      .attr("viewBox", `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)
      .style("max-width", "100%")
      .style("height", "auto")
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    // === SCALES ===
    const x = d3.scaleTime()  // or scaleLinear, scaleBand
      .domain(d3.extent(data, d => d.date))
      .range([0, width]);

    const y = d3.scaleLinear()
      .domain([0, d3.max(data, d => d.value)])
      .range([height, 0])
      .nice();

    // === AXES (Tufte-clean) ===
    svg.append("g")
      .attr("class", "axis")
      .attr("transform", `translate(0,${height})`)
      .call(d3.axisBottom(x).ticks(6))
      .call(g => g.select(".domain").remove());

    svg.append("g")
      .attr("class", "axis")
      .call(d3.axisLeft(y).ticks(5).tickFormat(d3.format(",.0f")))
      .call(g => g.select(".domain").remove())
      .call(g => g.selectAll(".tick line").clone()
        .attr("x2", width).attr("stroke-opacity", 0.08));

    // Axis labels
    svg.append("text")
      .attr("x", width / 2).attr("y", height + 36)
      .attr("fill", "#888").attr("font-size", "12px").attr("text-anchor", "middle")
      .text("[X label]");

    svg.append("text")
      .attr("transform", "rotate(-90)")
      .attr("x", -height / 2).attr("y", -44)
      .attr("fill", "#888").attr("font-size", "12px").attr("text-anchor", "middle")
      .text("[Y label]");

    // === DATA RENDERING ===
    // [Chart-specific code: lines, bars, circles, etc.]

    // === DIRECT LABELS ===
    // [Label line ends, notable bars, key points — no legend]

    // === ANNOTATIONS ===
    // [At least one call-out on a notable data point]

    // === TOOLTIP ===
    const tooltip = d3.select("body").append("div").attr("class", "tooltip");
    // [Mouseover/mouseout handlers on data elements]
  </script>
</body>
</html>
```

### Adapting the template

- **Right margin**: Set to 120px+ when direct-labeling line endpoints on the right
- **viewBox**: Always use `viewBox` for responsive sizing — never hardcode `width`/`height` attributes
- **Data**: Inline small datasets (<100 rows). For larger data, use `d3.csv()` or `d3.json()` with the file path
- **Multiple charts**: For small multiples, create one SVG per facet in a CSS grid container

---

## Interactive Patterns

Add interaction only when it reveals additional data, not for decoration.

| Interaction | When to use | D3 pattern | Notes |
|------------|-------------|------------|-------|
| **Tooltip** | Always (for detail-on-demand) | `mouseover` → position div → `mouseout` → hide | Show dimensions not in the static view |
| **Voronoi hover** | Scatter, multi-line (nearest point detection) | `d3.Delaunay.from()` → `find()` on mousemove | Better UX than hovering tiny elements |
| **Brush** | Time-series range selection, scatter filtering | `d3.brushX()` or `d3.brush()` → filter data | Combine with linked views for exploration |
| **Zoom + pan** | Maps, dense scatter, treemaps | `d3.zoom()` → transform group | Set `scaleExtent` and `translateExtent` bounds |
| **Linked views** | Dashboard with 2+ coordinated charts | Shared selection state → re-render both | Highlight in one, filter in another |
| **Transitions** | Sorting, chart type switching, data updates | `selection.transition().duration(250).ease(d3.easeCubicOut)` | Max 300ms; no elastic/bounce |

See `reference/d3-modules.md` → Interaction Behaviors for full code patterns.

---

## Playground Integration

When the user wants to **explore** data interactively (try different chart types, adjust fields, toggle Tufte features), build a D3 playground following the `/playground` skill conventions.

### Detection

Trigger playground mode on signals like: "explore", "play with", "try different views", "experiment", "what chart works best".

### How to build

1. **Analyze the data** — detect column names, types (numeric, temporal, categorical), and row count
2. **Build the playground HTML** following `reference/playground-integration.md`:
   - Controls panel on the left (chart type cards, field dropdowns, scale radios, color swatches, Tufte toggles)
   - D3 SVG preview on the right (re-renders fully on every state change)
   - Prompt output at bottom with copy button
3. **Populate controls from data** — field dropdowns list actual column names; chart type options are filtered to those compatible with the data shape
4. **Set intelligent defaults** — auto-detect time columns for x-axis, largest numeric column for y-axis, any low-cardinality string column for color grouping
5. **Include presets**: "Tufte minimal", "Annotated", "Dense", "Presentation"

### State management

Follow the playground skill pattern: single `state` object, `updateAll()` triggers `renderPreview()` + `updatePrompt()`. Every control writes to `state` and calls `updateAll()`.

### Prompt output

Natural language, not a value dump. Only mentions non-default choices. Example:
> "Create a scatter plot of price vs. square footage, colored by neighborhood, using a log scale for price, with direct labels on outliers and an annotation on the cluster of high-value properties."

---

## Data Handling

Handle data input in order of preference:

| Input type | How to handle |
|-----------|---------------|
| **File path provided** (CSV/JSON) | Read the file, analyze columns, auto-detect types. Use `d3.csv()` or `d3.json()` with relative path in the HTML |
| **Inline data** (pasted values) | Parse and embed directly in the `const data = [...]` block |
| **URL** | Fetch with `d3.csv(url)` or `d3.json(url)`. Warn about CORS if not a known open data source |
| **Description only** ("monthly sales data with columns date, revenue, region") | Generate realistic sample data matching the description. Note clearly in subtitle: "Sample data — replace with actual data" |
| **No data** (just a chart type request) | Generate with illustrative sample data. Note in subtitle |

### Data analysis steps

1. **Read the data** — first 5 rows + column names
2. **Detect types** — numeric, date (try common formats), categorical (string with <20 unique values), ID (unique strings)
3. **Compute summary stats** — min, max, mean, count, unique values for categoricals
4. **Select chart type** — using the Chart Selection Framework above
5. **Map fields** — assign columns to x, y, color, size, tooltip based on types and chart requirements

---

## Post-Generation Audit

After generating the visualization HTML, **before presenting it to the user**:

1. Read `reference/tufte-checklist.md`
2. Audit the generated code against every checklist item
3. Fix any violations found:
   - Remove gridlines if present (unless explicitly requested)
   - Replace legend with direct labels
   - Add annotation if missing
   - Check title is a finding not a description
   - Verify color encodes data, not decoration
   - Ensure tooltip reveals additional dimensions
4. Write the final HTML file
5. Open in browser: `open <filename>.html`

---

## Examples

### Example 1: Time-series data

**User:** "Visualize this CSV of monthly revenue by region"
**Flow:** Read CSV → detect date + numeric + categorical columns → select multi-line chart → generate with direct-labeled line endpoints → annotate peak month → audit checklist → open in browser

### Example 2: Comparison

**User:** "Show me how departments compare on headcount"
**Flow:** Detect categorical + numeric → select horizontal bar chart (sorted by value) → direct-label each bar → annotate the largest and smallest → title: "Engineering has 3x the headcount of Marketing" → audit → open

### Example 3: Exploration

**User:** "Let me explore this sales dataset"
**Flow:** Detect playground intent → analyze data columns → build D3 playground with chart type cards, field dropdowns, Tufte toggles → set intelligent defaults → write HTML → open in browser

### Example 4: Distribution

**User:** "What does the distribution of response times look like?"
**Flow:** Detect single numeric variable → select histogram → add KDE overlay → annotate median and p99 → add rug plot for individual data points → title: "95% of responses complete under 200ms" → audit → open
