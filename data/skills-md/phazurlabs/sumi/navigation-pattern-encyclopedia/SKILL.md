---
name: navigation-pattern-encyclopedia
description: "Every navigation pattern with specs, trade-offs, and production code: top bars, sidebars, bottom tabs, mega menus, breadcrumbs, command palettes, and contextual and mobile navigation. Use when choosing a nav model, fixing discoverability, or structuring information architecture."
---

# Navigation Pattern Encyclopedia — Every Nav Pattern

## Mental model

Navigation answers three questions, in this order: *where am I*, *where can I
go*, and *how do I get back*. A pattern that answers only the second is a menu,
not a navigation system.

- **Visible beats hidden.** Nielsen Norman's study (179 participants, six sites)
  found hidden navigation cuts content discoverability by nearly half and raises
  both time on task and perceived difficulty. Hide navigation only when the
  screen genuinely cannot hold it.
- **Information scent is the whole game.** A label must let someone predict what
  is behind it. "Solutions" has no scent; "Pricing" has perfect scent.
- **Depth costs more than breadth.** Two levels of fifteen items beat four
  levels of four. Every extra level is a place to get lost.
- **The pattern follows the destination count.** Three to five destinations means
  bottom tabs or a top bar. Twenty-plus means a mega menu or search-first. Fifty
  means a command palette, because no menu structure survives that.

## Index

| If | Pattern | Reference |
|---|---|---|
| 5-7 destinations, marketing or app shell | Top horizontal bar | `primary-navigation-patterns.md` |
| 20+ destinations, e-commerce or enterprise | Mega menu | `primary-navigation-patterns.md` |
| Brand-led marketing site | Centered logo nav | `primary-navigation-patterns.md` |
| Search is the primary action | Nav with integrated search | `primary-navigation-patterns.md` |
| Deep app, many sections | Sidebar | `primary-navigation-patterns.md` |
| Power users, 50+ destinations | Command palette | `primary-navigation-patterns.md` |
| Mobile, 3-5 destinations | Bottom tab bar | `mobile-navigation-patterns.md` |
| Mobile, more than 5 | Drawer or hamburger | `mobile-navigation-patterns.md` |
| Showing position in a hierarchy | Breadcrumbs | `secondary-navigation-patterns.md` |
| Switching views of one object | Tabs, segmented control | `secondary-navigation-patterns.md` |
| Long result sets | Pagination | `secondary-navigation-patterns.md` |
| Linear multi-step process | Stepper | `secondary-navigation-patterns.md` |
| Any of the above, made accessible | — | `navigation-accessibility.md` |
| Deciding the structure underneath | — | `information-architecture.md` |

## Reference architecture

| File | Covers | Lines |
|---|---|---|
| `references/primary-navigation-patterns.md` | 27 primary patterns with TSX | 1822 |
| `references/secondary-navigation-patterns.md` | 22 secondary patterns | 1339 |
| `references/mobile-navigation-patterns.md` | mobile-specific patterns | 1146 |
| `references/navigation-accessibility.md` | ARIA, keyboard, focus | 1046 |
| `references/information-architecture.md` | IA methods, taxonomy, URLs | 861 |

## What every reference file contains

1. Anatomy — the structural parts and what each is called
2. When to use it, and the condition that rules it out
3. Complete React/TSX plus CSS, runnable, no placeholders
4. The responsive transformation at each breakpoint
5. ARIA roles, keyboard map, and focus order
6. Anti-patterns specific to that pattern

## Routing

For **primary navigation** — 27 patterns with specs and TSX, including top bar,
mega menu, centered logo, integrated search, sidebar and command palette: read
`references/primary-navigation-patterns.md`.

For **secondary navigation** — breadcrumbs (simple, dropdown, truncated), tabs,
segmented controls, pagination and steppers: read
`references/secondary-navigation-patterns.md`.

For **mobile** — bottom tab bar (iOS), bottom navigation (Material 3), hamburger
and drawer variants, and the gesture patterns around them: read
`references/mobile-navigation-patterns.md`.

For **making it accessible** — ARIA landmarks, skip navigation, current-page
indication, expanded/collapsed state, and focus management: read
`references/navigation-accessibility.md`.

For **structuring the content underneath** — IA research methods, IA structures,
labeling and taxonomy, sitemap design and URL structure: read
`references/information-architecture.md`.

For **odds and ends** — the patterns that had no home in the files above when this skill was converted to a router: read `references/navigation-supplementary.md`.

## Cross-References
- **mobile-ux-design** — iOS and Android navigation deep dives
- **desktop-app-design** — Desktop navigation conventions
- **layout-block-intelligence** — Header/nav block patterns and layout integration
- **accessibility-inclusive-design** — Full WCAG navigation requirements
- **screen-flow-patterns** — User flow patterns that connect to navigation
- **component-patterns-code** — Production code for nav components
- **interaction-motion-design** — Navigation transition animations
- **responsive-block-patterns** — Responsive transformation specs
