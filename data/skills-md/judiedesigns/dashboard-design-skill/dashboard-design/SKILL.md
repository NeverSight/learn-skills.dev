---
name: dashboard-design
description: Build production-quality data dashboards in HTML or React. KPI cards with real deltas, 5 chart types, filter systems, sortable paginated tables, and CSV export — with three built-in style presets and a motion system. Use when the user asks to build, create, or generate a dashboard.
---

# Dashboard Design Skill

Build complete, working dashboards — not just pretty screenshots. Every output includes real calculated data, wired-up interactions, and correct component states.

## Output formats

- **HTML** — single file, Chart.js from CDN, no build step. Tell the agent: `"in HTML"` or `"as a single HTML file"`
- **React** — JSX component, Recharts. Tell the agent: `"in React"` or `"as a React component"`

## Style presets

Always specify a preset. If none is given, use `dark-terminal`.

| Preset | Accent | Background | Font | When to use |
|---|---|---|---|---|
| `dark-terminal` | `#06b6d4` cyan | `#080808` near-black | Geist Mono | SaaS, ops, developer tools |
| `carbon-light` | `#0f62fe` IBM blue | `#f4f4f4` warm white | IBM Plex Sans | Enterprise, B2B, formal reports |
| `neutral-bw` | `#111827` near-black | `#ffffff` white | Geist + Geist Mono | Any brand, law firms, finance |

See `references/styles.md` for all token values per preset.

## Layout order — always fixed

```
┌─ Sticky header (title + date range + export button) ─────────────────┐
├─ Filter bar (dropdowns, search, active filter pills) ─────────────────┤
├─ KPI row (3–4 cards max) ─────────────────────────────────────────────┤
├─ Charts row (primary chart 2/3 width + secondary 1/3) ────────────────┤
└─ Table (sortable, paginated, with empty state) ───────────────────────┘
```

Never put a chart above the KPIs. Never put the filter bar below the KPIs.

## Chart selection

| Data question | Chart type | Notes |
|---|---|---|
| How does X change over time? | Line with gradient fill | Y-axis may truncate |
| Compare quantities across categories | Grouped or stacked bar | Y-axis starts at zero |
| Part-to-whole breakdown? | Donut — max 5 segments | Always show % labels |
| Relationship between two variables? | Scatter plot | Add trend line if correlation is the point |
| Multiple streams over time? | Stacked area | Max 4 streams |
| One number that matters most? | KPI card — not a chart | |

## KPI card anatomy

```
LABEL          ← 10px mono uppercase, muted (Layer 4)
$48,204        ← 36px mono font-weight 300, full colour (Layer 1)
↑ +$3,681 (+8.2%) ← 12px mono, semantic colour (Layer 2)
▁▂▃▄▅▆▇█       ← sparkline 28px tall (Layer 3)
```

**Delta must show both absolute and relative:** `+$3,681 (+8.2%)` — never `+8.2%` alone.
**Calculate delta from real prior period data** — never use random numbers or hardcoded values.
**KPI value font-weight is 300 (light), not bold.** Large numbers in bold look cheap; light weight looks premium.

## Non-negotiable rules

1. **Layout order is fixed** — header → filters → KPIs → charts → table. Always.
2. **All numbers use monospace** — KPI values, table cells, axis labels. `font-family: monospace`
3. **One `update()` function rules all filters** — every filter change calls a single function that re-renders KPIs, all charts, and the table simultaneously. No partial updates.
4. **Charts use `chart.update()` not destroy/recreate** — prevents flicker on filter change.
5. **Never use `Math.random()` in a render path** — pre-generate all data at init.
6. **Bar chart Y-axis always starts at zero** — truncated bars misrepresent magnitude.
7. **Donut has 5 or fewer segments** — use "Other" to group the rest.

## Common mistakes and fixes

| Mistake | What to do instead |
|---|---|
| Random KPI deltas | Calculate from prior period in the same dataset |
| Static pagination HTML | Wire `tablePage` state to click handlers |
| Destroy + recreate charts on filter | `chart.update('active')` — smooth transition |
| Export downloads full raw data | Export only the currently filtered dataset |
| Blank table on no results | Show "No records match filters" empty state |
| `Math.random()` on render | Pre-generate all data at `init()`, never on update |
| Bold KPI values | Use `font-weight: 300` — lighter = more premium |
| Colour alone for status | Add icon + colour + border (never colour alone) |

## Component states

Every data component needs at minimum 3 states:
- `loading` — skeleton that mirrors live layout shape
- `empty-filtered` — "No records match your filters" + clear button
- `live` — the primary designed state

Platform dashboards also need: `stale` (timestamp badge) and `error` (message + retry).

## Reference files

- `references/html.md` — read this when building an HTML dashboard
- `references/react.md` — read this when building a React dashboard
- `references/styles.md` — all token values for the 3 presets
- `references/motion.md` — easing tokens, hover states, entry animations, skeleton loading
