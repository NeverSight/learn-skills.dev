---
name: data-dashboard
description: |
  Create visual data dashboards with charts, KPIs, and insights.
  TRIGGERS - Use when user wants a dashboard, data visualization, or metrics overview.
---

# Data Dashboard Creator

## Overview
Creates interactive or static dashboards with KPI cards, charts, and trend analysis. Can output as HTML/React artifacts, Excel, or design specs.

## Workflow

### Step 1: Define the Dashboard
1. **Purpose**: What decisions should this dashboard inform?
2. **Audience**: Who views it? (exec, team, clients)
3. **Data source**: Where does the data come from?
4. **KPIs**: What are the 3-5 most important metrics?
5. **Update frequency**: Real-time, daily, weekly, monthly?
6. **Output format**: Interactive (HTML/React), Excel, or design spec?

### Step 2: Design the Layout

**Dashboard hierarchy:**
```
TOP ROW: KPI Cards (3-5 key numbers)
MIDDLE: Primary chart (biggest insight)
BOTTOM LEFT: Secondary chart
BOTTOM RIGHT: Table or list
```

### Step 3: Select Visualizations

| Data Type | Best Chart | When to Use |
|-----------|-----------|-------------|
| Trend over time | Line chart | Revenue, users, growth |
| Comparison | Bar chart | Month vs month, team vs team |
| Composition | Pie/donut | Market share, budget allocation |
| Distribution | Histogram | Customer segments, pricing |
| Relationship | Scatter plot | Correlation analysis |
| Progress | Gauge/progress | Goal tracking |
| Ranking | Horizontal bar | Top performers |

### Step 4: Build the Dashboard

Create as HTML/React artifact with:
- Responsive layout
- Color-coded KPI cards (green = good, red = needs attention)
- Interactive hover states
- Clean, professional design
- Dark or light theme

## Output Format
Generate an interactive HTML or React dashboard artifact, or provide design specifications for implementation.

## Quality Checklist
- [ ] 3-5 KPI cards at top
- [ ] Most important insight is the largest visual
- [ ] Colors are meaningful (not decorative)
- [ ] Readable on mobile
- [ ] Time period clearly stated
- [ ] Data source noted
