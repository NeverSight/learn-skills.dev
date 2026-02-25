---
name: recharts
description: >-
  Use when building charts, data visualisations, or dashboards with Recharts.
  Also use when integrating Recharts with HeroUI, reviewing chart components,
  or creating responsive chart containers. Generates Recharts charts styled
  with HeroUI v3 design tokens and Tailwind CSS v4.
allowed-tools: Read Write Edit Glob Grep mcp__heroui-react__get_theme_variables
metadata:
  model: sonnet
---

You build Recharts charts integrated with HeroUI v3 design tokens and Tailwind CSS v4. Infer the project's language variant (US/UK English) from existing commits, docs, and code, and match it in all output.

Read individual rule files in `rules/` for detailed patterns and code examples.

## Rules Overview

| Rule | Impact | File |
|------|--------|------|
| Container pattern | HIGH | `rules/container-pattern.md` |
| Theme integration | HIGH | `rules/theme-integration.md` |
| Custom components | HIGH | `rules/custom-components.md` |

## Workflow

### Building a chart?

1. **Detect setup** — Confirm `recharts` is in `package.json`. Check if HeroUI v3 is installed (`@heroui/react` or individual packages). Detect Tailwind CSS v4 (`@tailwindcss/*`).
2. **Read rules** — Read all files in `rules/` to load the container pattern, theme token mapping, and custom component templates.
3. **Fetch theme tokens** — Use `mcp__heroui-react__get_theme_variables` to confirm the current HeroUI token names available in the project.
4. **Generate component** — Build the chart component applying all three rules: outer container wrapper, CSS variable colours, and custom tooltip/legend.
5. **Verify** — Check the generated code against each rule. Confirm no hardcoded hex colours, `ResponsiveContainer` is wrapped correctly, and tooltip uses HeroUI classes.

### Reviewing existing charts?

1. **Scan** — Glob for files importing from `recharts`. Read each file and check against every rule in `rules/`.
2. **Report** — List violations grouped by rule with file paths and line numbers.
3. **Fix** — Apply corrections using the Edit tool, one violation at a time.

## Quick Reminders

- Always add `<AccessibilityLayer />` as the first child inside every chart for screen reader support
- Set `isAnimationActive={false}` on chart elements when inside components that re-render frequently (tables, filters)
- Recharts uses SVG — style with `stroke` and `fill` props, not CSS `color`
- Export chart prop interfaces separately so consumers can extend them
- Use `cartesianGrid` with `strokeDasharray="3 3"` and theme-aware stroke colour
- Never set a fixed `width` on `ResponsiveContainer` — it must always be `width="100%"`

## Assumptions

- React + TypeScript project
- Recharts installed (`recharts` in dependencies)
- HeroUI v3 installed with Tailwind CSS v4
- CSS variables from HeroUI theme are available globally
