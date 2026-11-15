---
name: antislop-dashboard
description: "Dashboard, analytics, metric-card, table, and chart rules: real data hierarchy, no decorative metric cards, honest visualizations, and complete table states. Map to antislop-master C-10 and G-3/G-4/G-5. Use when building or auditing an admin/analytics interface."
allowed-tools: Read Write Edit Glob Grep
---
# antislop-dashboard

> Dashboard rules for anti-ai-slop. Map to **C-10** (metric cards), **A-2/A-3** (decorative), and **G-3/G-4/G-5** (states) in `antislop-master`.
>
> A dashboard is a tool, not a trophy case. The moment a chart or card exists to look impressive, it is slop.

---

## Metric cards

- **Avoid** the four identical metric cards ("Revenue", "Users", "Uptime", "Growth") always laid out the same, each with a sparkline that means nothing. (C-10)
- **Every number needs**: a source and a period. `+23%` with no "of what / since when" is a fake metric. (H-1)
- **Only show a metric that drives a decision.** If nobody acts on it, cut it. A dashboard is a list of decisions, not a wall of numbers.
- **Vary the card emphasis** by importance — the number someone checks daily should be visually more important than a vanity count.

## Charts

- **Honest scale.** Label both axes, give the unit, and don't truncate the y-axis to exaggerate change. (H-1, P5)
- **One chart, one message.** If a chart needs a paragraph of explanation, it's two charts or a table.
- **No decorative glow/gradient charts** just to look "analytics-y". (A-2, A-3)
- **Line + bars for the same axis in the same chart only when** the comparison genuinely needs both.

## Tables

- **Complete table treat states.** A table with rows but no empty state, no loading state, and no error state is incomplete. (G-3, G-4, G-5)
- **Empty, loading, error are three different visuals**, not one gray placeholder.
- **Sorting, filtering, and pagination must be real** — a button that does nothing is a P4 interactivity failure. (G-1)
- **Long lists need** an empty-search result state and a "no matches" message. (G-8)

## Hierarchy

- The whole dashboard should not be the same visual weight. A **primary area** (what the user opens to see) must be visually distinct from supporting panels. (I-3)
- **No spinning/repeating identical widgets** across the page — variation reflects real data weight. (C-7)

---

## Audit checklist

- [ ] Every metric has a source and a period. (H-1)
- [ ] Every number drives a decision. (C-10)
- [ ] Charts have labelled, honest axes. (P5)
- [ ] Tables have empty / loading / error states. (G-3, G-4, G-5)
- [ ] Controls (sort/filter/paginate) actually work. (G-1)
- [ ] One primary area carries the most weight. (I-3)

Findings cite the code from `antislop-master` plus one honest reason.
