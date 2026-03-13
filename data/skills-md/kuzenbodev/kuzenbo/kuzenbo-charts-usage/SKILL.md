---
name: kuzenbo-charts-usage
description: Build production charts with @kuzenbo/charts on top of @kuzenbo/core and @kuzenbo/theme. Use when tasks mention chart selection, chart migration, dashboard visualization, series/data wiring, chart styling, legends/tooltips, or responsive chart layout.
---

# Kuzenbo Charts Usage

Use this skill for external app code that consumes the stable public package `@kuzenbo/charts@0.0.6`.

## Runtime Setup

1. Install required runtime set:

```bash
npm install @kuzenbo/charts @kuzenbo/core @kuzenbo/theme recharts
```

2. Ensure theme stylesheet is loaded once:

```ts
import "@kuzenbo/theme/prebuilt/kuzenbo.css";
```

## Chart Workflow

1. Choose the chart primitive from `references/chart-exports.md`.
2. Shape data as array records and define a typed `series` list with `name`, `label`, and `color`.
3. Add formatter functions (`valueFormatter`, axis formatters) early to avoid formatting drift.
4. Turn on only needed affordances (`withLegend`, `withTooltip`, axis toggles) to keep charts readable.

## Guardrails

- Stay on public exports only (`@kuzenbo/charts/ui/*` listed in references).
- Keep `@kuzenbo/core` and `@kuzenbo/theme` present in runtime.
- Use semantic chart color vars (`var(--color-chart-1)` etc.) instead of hardcoded palette literals when possible.
- If a requested chart type is absent, choose the nearest exported primitive and state the tradeoff.

## References

- `references/chart-exports.md`
- `references/chart-starter-pattern.md`
