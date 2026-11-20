---
name: dashboard-design
description: Designs dashboards that answer specific questions at a glance, defining users and key questions, KPI cards with deltas and sparklines, layout by importance, filters and date ranges, drill-down paths, density, data freshness and per-panel loading states. Use when asked to design an analytics, admin or monitoring dashboard, a metrics overview, or to declutter an existing one. Not for choosing or styling individual charts (use data-visualization).
---

# Dashboard Design

Produces a dashboard where every panel answers a named question for a named user, the most important answers are seen first, and every number comes with context.

## When to use
- "Design an analytics / admin / ops dashboard for X."
- "Our dashboard is cluttered and nobody uses it."
- Building the home or overview screen of a SaaS product or internal tool.
- Deciding which KPIs, filters, and charts belong on one screen.
- Reviewing a dashboard for hierarchy, density, or misleading numbers.

## Workflow
1. Identify the primary user role and the decisions they make. Write 3–5 key questions the dashboard must answer ("Are sign-ups on track this month?", "Which region is behind target?"). If unknown, ask once; otherwise assume a role and say so.
2. Map each question to a metric, its comparison (target, previous period, benchmark), time granularity, and data source. Drop any panel that answers no question.
3. Classify the dashboard: operational (monitor and act, frequent refresh), analytical (explore, filter, drill), or strategic (periodic summary). This sets refresh rate and density.
4. Rank the questions; put the top answers in the first row and top-left, where F- and Z-pattern scanning starts. Supporting charts and detail tables go below.
5. Choose the form per question: KPI card, line, bar, or table. Use data-visualization for chart details and data-tables for tabular panels.
6. Design global filters and the date range at the top, panel-level options inside panels, and a drill-down path for each summary.
7. Specify loading, empty, error, stale, and partial states for every panel (see ui-states).
8. Build it responsive: 12-column grid on desktop, 2 columns on tablet, 1 column on mobile with KPIs first.

## Rules
**KPI cards**
- Each card: label, current value, delta versus comparison (sign, arrow, and % or absolute), comparison period ("vs previous 30 days"), optional sparkline without axes.
- 3–6 KPI cards in the top row. More dilutes attention; move the rest into a secondary section.
- Delta color follows meaning, not direction: rising cost or churn is negative. Never rely on color alone; the sign and arrow carry it too.
- Values use tabular figures and consistent units and precision (1.24M, 98.2%), with the exact value available on hover and focus.

**Layout and density**
- One dashboard, one purpose. If a view needs more than about 9 panels, split it by audience or question.
- Align panels to the grid with consistent gutters (16–24px) and group related panels under section headings.
- Panel titles state the metric or question; units appear in the title or axis label.

**Filters and time**
- Date range with presets (Today, Last 7 days, Last 30 days, Quarter to date, Custom) and the timezone shown.
- Applied filters are visible as removable chips with Clear all; filter and date state live in the URL so views can be shared.
- Panels that ignore global filters say so in their header.

**Drill-down and freshness**
- Every summary (KPI, bar, segment) links to its underlying detail, filtered to match; breadcrumbs keep the path back.
- Show "Updated 3 min ago" with the absolute time on hover and focus, plus a manual refresh. Auto-refresh no faster than the data changes, and never shift layout or reset scroll when it does.

**Loading and accessibility**
- Panels load independently with skeletons sized like the final content; one failed panel shows its own error and Retry.
- Each chart has a text summary or an accessible data table; a KPI card reads as one phrase to screen readers ("Revenue, $48,200, up 12% vs last month").

## Output
- A question map: question → metric → comparison → visual → position.
- Annotated layout for desktop and mobile (grid sketch in markdown or a wireframe description).
- Implementation in the project's stack: semantic HTML and CSS grid with custom properties, or React + Tailwind; charts only with the chart library already installed.
- A KPI card component with value, delta, period, sparkline, and all states.

## Avoid
- Vanity metrics with no decision attached; panels added because the data happened to exist.
- Gauges, 3D charts, and pie charts with more than 5 slices.
- Numbers without a comparison, period, or unit.
- Panels using different date ranges without labels.
- Red and green as the only signal.
- A full-page spinner that hides everything while one slow query finishes.
- Auto-refresh that moves content while someone is reading it.

## Final check
- [ ] Every panel maps to one of the 3–5 key questions.
- [ ] The most important answers sit in the first row, top-left.
- [ ] Every KPI shows value, delta, comparison period, and unit.
- [ ] Date range, timezone, and last-updated time are visible.
- [ ] Filters persist in the URL and appear as removable chips.
- [ ] Every panel has loading, empty, error, and stale states.
- [ ] Text contrast ≥4.5:1, chart marks ≥3:1 against the background, and color is never the only signal.
