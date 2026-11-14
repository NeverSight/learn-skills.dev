---
name: data-viz-deck
description: Transform audit data, performance reports, and structured analyses into polished visual deliverables. Generates presentation decks (PPTX), interactive HTML dashboards, or styled markdown reports with charts. Includes a customizable design system with forest green accent and warm cream backgrounds. Use when the user has analysis data and needs a visual deliverable.
license: MIT
origin: custom
author: Rebecca Rae Barton
author_url: https://github.com/thatrebeccarae
metadata:
  version: 1.0.0
  category: reporting
  domain: data-visualization
  updated: 2026-03-18
  tested: 2026-03-18
  tested_with: "Claude Code v2.1"
---

# Data Visualization & Deck Builder

Transform structured data and analysis into polished visual deliverables: presentation decks, interactive dashboards, and visual reports.

## Install

```bash
git clone https://github.com/thatrebeccarae/claude-marketing.git && cp -r claude-marketing/skills/data-viz-deck ~/.claude/skills/
```

## When to Use This Skill

- User has completed an audit or analysis and wants a visual deliverable
- User says "make a deck," "create a presentation," "build a dashboard," "visualize this"
- User wants to turn a markdown report into client-ready slides
- User needs charts, tables, or visual summaries from performance data

## Output Formats

### 1. PPTX Deck (Primary)
Native PowerPoint with editable charts, styled tables, and professional layouts. Best for client handoffs and presentations.

**Requires:** python-pptx (installed), pandas (installed)

### 2. Interactive HTML Dashboard
Single-file HTML with plotly.js charts (loaded via CDN), filterable tables, and responsive layout. Best for sharing interactive reports.

**Requires:** jinja2 (installed), pandas (installed). Plotly.js loaded via CDN at runtime.

### 3. Visual Markdown Report
Enhanced markdown with embedded chart images (requires matplotlib: `pip install matplotlib`). Best for vault reports and documentation.

## Workflow

### Step 1: Identify the Data Source

Read the source file (audit markdown, CSV, JSON, or database query results). Parse the key metrics, tables, and findings into a pandas DataFrame or structured dict.

### Step 2: Select Chart Types

| Data Pattern | Chart Type | When to Use |
|-------------|------------|-------------|
| Categories with values | **Bar chart** (horizontal) | Revenue by category |
| Categories + benchmark | **Bar chart with reference line** | Performance vs benchmark |
| Parts of a whole | **Doughnut/Pie chart** | Revenue concentration, channel mix |
| Values over time | **Line chart** | Trend data, period-over-period |
| Two variables | **Scatter plot** | Correlation analysis |
| Performance scoring | **Heatmap table** | Color-coded metrics (green/amber/red) |
| Before/after or gaps | **Waterfall chart** | Revenue opportunity sizing |
| Ranked items | **Horizontal bar** | Top 10 sorted |
| Funnels | **Funnel chart** | Delivered > opened > clicked > converted |
| Status overview | **Scorecard/KPI tiles** | Executive summary metrics |

### Step 3: Apply the Design System

All deliverables use a configurable design system. Override the color tokens and font choices to match your brand.

#### Color Palette

```python
COLORS = {
    # Brand accent -- change to your brand color
    "accent":      "#3D7A5C",  # Forest green
    "accent_light":"#6AB88A",  # Light green

    # Chart series (ordered for visual distinction)
    "series": ["#3D7A5C", "#6AB88A", "#8B7EC8", "#D4845A", "#C9A84C", "#C75B6F", "#93C9A8", "#8B949E"],

    # Semantic
    "good":        "#2E8B57",  # Green -- above benchmark
    "warning":     "#D97706",  # Amber -- watch
    "critical":    "#C0392B",  # Red -- action needed
    "neutral":     "#8B949E",  # Slate -- no judgment

    # Dark mode (title slides, section dividers)
    "bg_deep":     "#141414",
    "bg_surface":  "#1E1E1E",
    "text_bright": "#F0F3F6",
    "text_secondary_dark": "#9CA3AF",

    # Light mode (content slides -- the default)
    "bg_light":    "#FAF7F2",  # Warm cream, NOT white
    "bg_surface_light": "#F2EDE6",
    "text_primary":"#0F0E0E",
    "text_secondary": "#57606A",
    "text_muted":  "#8B949E",
}
```

**Color rules:**
- Light mode (`#FAF7F2` warm cream) is default for all content slides. NOT white.
- Dark mode (`#141414`) only for: title slides, section dividers, closing slides.
- Accent color used sparingly: top-performing bars, key metrics, accent callouts.
- Semantic colors (green/amber/red) only for status indicators, never decoration.

#### Typography (PPTX)

```python
FONTS = {
    "title":    "Switzer",        # Slide titles -- Light (300), 28-36pt, NOT bold
    "subtitle": "Switzer",        # Subtitles -- Regular (400), 18-22pt
    "body":     "Switzer",        # Body text -- Regular (400), 12-14pt
    "data":     "Cartograph CF",  # Numbers, tables -- Regular/Bold, 11-12pt
    "kpi":      "Cartograph CF",  # KPI big numbers -- Bold (700), 44-60pt
    "label":    "Cartograph CF",  # ALL CAPS labels -- Regular, 9-10pt, +tracking
}
# Fallbacks: Switzer -> Inter -> system-ui | Cartograph CF -> Consolas -> monospace
```

**Critical typography rules:**
1. **Headlines use Light weight, NOT Bold.** Light at large sizes = confident, premium.
2. **Monospace font for ALL numeric/data content.** KPIs, table numbers, labels, footers.
3. **Negative tracking on headlines.** -0.03em to -0.04em.
4. **Positive tracking on ALL CAPS labels.** +0.08em to +0.1em.

#### Slide Layouts

Every deck follows this structure:

```
1. Title Slide         -- Report name, date (dark mode)
2. Executive Summary   -- 3-5 KPI tiles + key findings bullets
3. Scorecard           -- Color-coded performance overview table
4. Deep Dive slides    -- One per major finding (chart + insight + recommendation)
5. Opportunity Sizing  -- Waterfall or bar chart of revenue opportunities
6. Recommendations     -- Prioritized table (Quick Wins / Strategic / Maintenance)
7. Appendix            -- Full data tables
```

#### Slide Dimensions (python-pptx)

```
Width:  13.333"
Height: 7.5"
Aspect: 16:9
```

### Step 4: Generate the Deliverable

Follow the code patterns in REFERENCE.md for the chosen output format.

## Key Principles

1. **One insight per slide.** Never cram multiple findings onto one slide. Each deep-dive slide has: chart (left 60%), insight + recommendation (right 40%).

2. **Lead with the number.** Every slide title should contain the key metric: "Post-Purchase RPR at $0.07 -- 14x Below Benchmark" not "Post-Purchase Flow Analysis."

3. **Benchmark everything.** Never show a metric without context. Show the benchmark, the gap, and what closing the gap is worth.

4. **Color = meaning.** Green means good/above benchmark. Amber means watch. Red means action needed. Never use color decoratively in data slides.

5. **Simplify chart data.** Max 6-8 items per chart. Aggregate the tail into "Other."

6. **Executive summary is the deck.** If someone only reads slide 2, they should understand the full story.

7. **Never estimate when actuals exist.** If the data has exact values, compute precise totals.

8. **No white backgrounds.** Always warm cream `#FAF7F2` for light content.

9. **No bold headlines.** Light weight for all hero/section titles.

For complete code templates and reference, see [REFERENCE.md](REFERENCE.md).
