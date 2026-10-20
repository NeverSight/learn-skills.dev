---
name: Component Reference Design
description: >-
  Positive reference library of modern, non-monotonous UI — the constructive
  companion to Anti-AI-Slop. Curated, copy-pasteable, accessible patterns sourced
  from trusted design authorities (MUI, shadcn/ui, Radix, Headless UI, Ant Design,
  Chakra, Mantine, Tailwind UI, Material Design 3, Apple HIG, IBM Carbon, NNG,
  Refactoring UI). Covers layout skeletons (with/without animation), typography
  systems & font pairings, every card variant, buttons & forms, navigation,
  data-display, overlays & feedback, tasteful accessible motion, a design-system
  index, and varied marketing-section anatomies. Use when designing or building
  any UI and you want a reference for "what good looks like."
metadata:
  author: b4r7x
  version: 1.0.0
  references:
    - references/layouts.md
    - references/typography.md
    - references/components.md
    - references/animation.md
    - references/design-systems.md
    - references/charts.md
    - references/dashboards.md
---

# Component Reference Design — Positive Pattern Library

## Purpose
A **reference of what good looks like**, sourced from trusted design systems.
Where `Anti-AI-Slop` tells you what to AVOID, this skill shows you what to BUILD:
modern layouts, varied section anatomies, proven type systems, every card and
component variant, and tasteful accessible motion — all copy-pasteable and a11y-correct.

> Use the two skills together: **Anti-AI-Slop = the filter, Component Reference = the palette.**

## How To Use This Skill
1. Identify what you're building (a page layout? a card? a form? a nav?).
2. Open the matching reference file (see Category Map) and pick a pattern by its
   **when-to-use** note — not by "what looks coolest in isolation."
3. Copy the concrete markup; swap in real content, brand color, and a non-Inter
   display font.
4. Apply the **Anti-Monotony Rules** below so the page doesn't feel templated.
5. Run the Anti-AI-Slop **Pre-Delivery Audit** before shipping.

## Category Map (where to look)

| You're building… | Open | Contains |
|------------------|------|----------|
| Page/app skeleton, grid, responsive structure | `references/layouts.md` | Holy-grail, sidebar shell, dashboard, split-screen, full-bleed, bento, masonry, magazine, asymmetric, sticky-aside, container-query, Z/F patterns, Every-Layout primitives |
| Type scale, font pairing, fluid type | `references/typography.md` | 8+ display+body pairings, modular scales (1.2/1.25/1.333), clamp() recipes, per-role leading/measure/tracking, Tailwind config, MUI/MD3/Apple/Carbon scales compared |
| Card, button, form, nav, table, list, badge | `references/components.md` | Card variants (17), buttons (10), form controls (13), navigation (13), data-display (16) |
| Modal, drawer, toast, tooltip, popover, animation | `references/animation.md` | Overlay/feedback components + tasteful motion patterns (timing, easing, reduced-motion, 13 motion recipes) |
| Choosing a library / design tokens | `references/design-systems.md` | 18 design-system index (ecosystem, styling, a11y, theming, license, URL) + W3C DTCG tokens + decision matrix |
| Charts, graphs, KPI cards, sparklines, data-viz | `references/charts.md` | Beautiful modern Recharts patterns: color systems (teal/Okabe-Ito/OKLCH), premium chrome (custom tooltip/legend/axes/grid), bar/line/area/donut/radial, KPI+sparkline cards, specialty (heatmap/treemap/funnel/radar/scatter/bullet/waffle), motion, dark-mode/responsive, a11y, 15-point anti-slop scan |
| Admin dashboard — app shell, sidebar, topbar, widgets, tables, filters | `references/dashboards.md` | Modern clean admin dashboard: 15 clean-dashboard principles, app shell (grid sidebar+header), sidebar nav (collapsible/rail/groups/footer), topbar (breadcrumb/⌘K search/notif/avatar/org-switcher), command palette, grid composition (KPI→hero+side→table, bento), KPI/stat cards (delta inversion), chart placement/chrome, filters & toolbar (date-range/segmented/chips/saved-views), data table (TanStack/density/sort/selection/pagination), all states (skeleton/empty/error/zero), 3-tier color tokens + dark, anti-pattern cheat sheet |

## The Anti-Monotony Rules (apply to every multi-section page)
1. **Never repeat the same section anatomy consecutively.** Vary: centered → split → bento → stats-bar → full-bleed → alternating.
2. **Vary container widths by content** — text `max-w-3xl`, grids `max-w-6xl`, ≥1 full-bleed break per page.
3. **Vary section padding** — hero `py-32`, features `py-16`, CTA `py-12`. Never one uniform `py-20`.
4. **One dominant element per section** — size/weight ≥1.5× its neighbours.
5. **Break rhythm every 2–3 sections** — a full-bleed image, colour block, or stats bar.
6. **Mix grid structures** — 2-col, 4-col, asymmetric spans; a bento needs a real 2×2 dominant cell (else it's just a card grid).
7. **≥2 deliberate asymmetric moments per page** — unequal columns, off-centre headings, left-aligned text.

## Proven Storytelling Sequence (Evil Martians, 100 dev-tool landing pages)
`Hero (what is it?) → Trust (who uses it?) → Features (what/why?) → Social proof (what do users say?) → Supporting (FAQ / comparison / pricing) → Final CTA (what now?)` — with each section using a DIFFERENT anatomy.

## Non-Negotiable Quality Bar (every pattern here already follows it)
- **Semantic HTML first** — `<table>`, `<ul>`, `<dl>`, `<dialog>`, `<nav>`, `<button>`, `<a>` before div-soup.
- **Accessible by default** — labels wired, `aria-*` present, focus-visible rings, keyboard reachable, focus trap on modals.
- **`prefers-reduced-motion`** gates every spatial animation.
- **Radius is a scale** — inputs/buttons `rounded-md`, cards `rounded-lg`, modals `rounded-xl`, pills `rounded-full`.
- **Type** — distinctive display font (NOT Inter-everywhere), modular scale, `max-w-prose` body, 2–3 weights.
- **Motion budget** — hovers 100–150ms, entrances 200–300ms, exits faster; `transform`+`opacity` only.
- **WCAG AA contrast** — 4.5:1 body, 3:1 large/UI; test light + dark.

## Trusted Sources (full index in `references/design-systems.md`)
MUI · shadcn/ui · Radix Primitives & Themes · Headless UI · Ant Design · Chakra UI ·
Mantine · Tailwind UI · Material Design 3 · Apple HIG · IBM Carbon · Atlassian ·
Polaris (Shopify) · Fluent (Microsoft) · Base Web (Uber) · Park UI / Ark UI · daisyUI ·
Tremor · TanStack Table · Recharts · NNG · Refactoring UI · Every-Layout · Josh Comeau ·
Framer Motion / Motion · Emil Kowalski (Sonner, Vaul) · cmdk · W3C WAI-ARIA APG · W3C DTCG.

## Output Expectations
Use these patterns as a starting point, then make ≥1 deliberate, content-specific
choice per section (color, type, layout variation). The result should read as
**intentional, branded, varied, accessible, production-ready** — never templated.
