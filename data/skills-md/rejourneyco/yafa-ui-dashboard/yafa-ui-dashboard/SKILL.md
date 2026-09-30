---
name: yafa-ui-dashboard
description: Design, build, refactor, or review polished responsive analytics dashboards, SaaS admin dashboards, business intelligence interfaces, and data-heavy product UI using Yafa-UI. Covers sidebar navigation, one-row page headers, multi-color KPI cards, charts, tables, filters, Lucide icons, accessible states, and mobile dashboard layouts across React, Next.js, Tailwind CSS, Vue, Svelte, and other frontend stacks. Do not use this visual system as the default for marketing sites, authentication, setup wizards, account or billing settings, or unrelated public pages.
---

# Yafa-UI: Dashboard

Create dashboards that feel like precise analytical instruments: calm, bright, information-dense, approachable, and fast to scan. Preserve the host product's brand and framework while applying this system's hierarchy, geometry, color allocation, and responsive behavior.

## Read the relevant references

- Read [references/dashboard-visual-system.md](references/dashboard-visual-system.md) for shell, typography, geometry, cards, tables, and interaction work.
- Read [references/color-system.md](references/color-system.md) whenever choosing or reviewing route accents, KPI colors, chart series, status colors, or sidebar icon colors.
- Read [references/icon-system.md](references/icon-system.md) whenever adding, replacing, sizing, or coloring icons or the skill mark.
- Read [references/responsive-adaptation.md](references/responsive-adaptation.md) whenever changing layout, navigation, filters, charts, tables, overlays, or screen-size behavior.
- For a design or implementation review, also read [references/review-checklist.md](references/review-checklist.md).

## Preserve these invariants

- For a net-new full dashboard or a host shell that is compatible with this pattern, build four layers: white sidebar, compact white top bar, compact page identity/filter bar, then a pale `#f8fafd` analytical canvas. Inside an established host shell, preserve its chrome and apply Yafa-UI to the page identity, analytical hierarchy, surfaces, and responsive behavior instead of replacing navigation without authorization.
- For a full Yafa-UI shell, keep navigation semantic and scannable. Use stable group accents, centrally registered route-colored destination icons, neutral inactive labels, and an active route tint plus 3px left rail. In the icon-only rail, both icon and active rail use the route's contrast-safe `uiStrong` variant. Treat a 300px resizable rail, 64px collapsed rail, and accessible mobile drawer as net-new defaults; adapt to an established host navigation contract when one exists.
- Keep the sidebar header terse: one short product name followed by compact value-only context selectors when the product actually has team, project, or workspace scope. Do not invent selectors or repeat a tagline or visible context eyebrow when position and icon already explain the value.
- For a new or unbranded dashboard, use self-hosted Inter with compact 13–14px body text, 15–16px/800 page titles, 14–15px/600 card titles, and 26–32px/700 primary metrics. If the host has an established product typeface, preserve it and reproduce this hierarchy through scale and weight. Never name Inter without loading it.
- Build ordinary analytical surfaces from white, a 1px neutral border, an 8px radius, little or no shadow, an optional 3–4px accent rule, and 16–20px internal spacing.
- Put standard KPI cards immediately after the page header. Do not add decorative upper-right KPI icons. Use a concise dotted-underlined title as the hover/focus/tap description affordance, a quiet divider, a primary value, and a comparison.
- Position metric-description tooltips beside their title with viewport-aware right/left flipping. Prefer above on narrow screens; do not default underneath where the tooltip covers the card's value.
- When the header content pane is at least about `720px` and the localized labels fit, keep page identity on the left and the complete global view/time/period lens cluster that actually exists on the right in one compact row. This is the canonical desktop treatment. Do not invent a platform lens. First collapse the rail, truncate optional copy, disclose secondary lenses, and move route-specific filters into content; only a genuinely narrower content pane may place the intact global cluster below identity rather than overflowing or shrinking touch targets.
- Apply one stable route-identity pair, a deliberate multi-color analytical palette, and semantic state colors on a neutral foundation. Do not make every chart, KPI, or sidebar icon blue.
- Use named Lucide icons for ordinary interface actions and route identity. Do not mix icon packs, substitute emoji, hand-draw lookalike controls, or generate raster interface icons.
- Keep ordinary actions rectangular. Query, Generate, Search, Reset, Clear, Edit, Add, and filter controls use 0–8px corners and consistent 32/36/40px heights; they are not pills.
- Render statuses as a 6px semantic dot or compact icon plus plain neutral text. Never wrap the dot and label in a bordered or tinted capsule.
- A numeric delta may use a compact capsule, but its surface stays white or transparent with a neutral border. Apply semantic color only to the arrow, sign, number, and percent text.
- Order content from overview to evidence: identity and lenses, KPI summary, primary analysis, supporting charts or rankings, then dense tables or evidence.
- Preserve critical information across widths. Choose layout from the content pane after chrome, not viewport width alone, and never introduce page-level horizontal overflow.
- Cover default, hover, focus, active, disabled, loading, empty, partial-error, and full-error states. Keep rendered data visible during background refresh; use full skeletons only before useful data exists.

## Build or revise a dashboard

1. Inspect the host product's existing tokens, components, navigation model, data hierarchy, and accessibility conventions. Established brand identity, terminology, and required workflows win; apply Yafa-UI to hierarchy, analytical surfaces, geometry, and responsive behavior unless the task explicitly requests broader redesign.
2. Classify the page as a standard overview, dense list/database, or canvas-first workbench.
3. Sketch the analytical order before styling controls. Every panel should answer one clear question.
4. Create centralized registries for route identity, sidebar group identity, icons, and chart-category colors. Do not assign colors from render order.
5. Compose with existing primitives where they produce the intended effective result; otherwise create small semantic components rather than page-wide element overrides.
6. Apply the responsive matrix and verify at `320px`, `375–390px`, `768px`, `1024px`, and `1440px`. Test both sides of changed breakpoints.
7. Exercise keyboard focus, Escape and focus restoration for drawers/overlays, touch targets, 200% zoom, reduced motion, long labels, overflow, and all data states.
8. Run the host repository's focused typecheck, tests, and visual verification. Report any intentional departure from this system.

Do not silently restyle unrelated product areas while applying this skill. Shared shell changes may affect them; verify the impact without treating those pages as visual references.
