---
name: ux-navigation
description: Design or critique navigation systems — match the nav pattern (top bar, sidebar, tabs, hamburger, mega menu, bottom nav) to the information architecture, and apply wayfinding, header, breadcrumb, and pagination best practices. Trigger when the user asks to design or review navigation, menus, navbars, sidebars, tabs, breadcrumbs, headers, pagination, or asks "how should users move around" a site or app.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Navigation Skill

## How this skill behaves (read first)

This is a **generative** skill. The default failure modes: **pattern-by-habit** (a top bar with a hamburger regardless of IA depth, breadth, or platform), **hidden essentials** (core sections buried behind icons), and **missing wayfinding** (no "you are here" signals, so users dropped in by search are lost). Navigation is chosen by the *structure of the content* and *how users move through it* — not by what modern sites look like. This skill gates:

1. **Establish the IA shape and platform** — these mostly decide the pattern.
2. **Apply the always-true core** — system layering, wayfinding signals, visible essentials, interaction basics.
3. **Surface the pattern decisions** (top bar vs. sidebar, hamburger, mega menu, tabs, breadcrumbs, pagination vs. infinite scroll) with trade-offs.

Then it **hands off to `ux-heuristics-audit`, `ux-accessibility-audit`, `ux-aesthetics-audit`, and `ux-microcopy-audit`** — and, as a multi-screen structure, to `ux-information-architecture-audit`.

---

## Step 0 — Establish context before designing

Ask if not known; state the assumption if proceeding without an answer:

- **IA shape** — how many top-level sections, how deep the hierarchy, and is it expected to grow? (Breadth/growth pushes toward vertical nav and mega menus; shallow + stable fits a top bar or tabs.)
- **Platform** — desktop, mobile, or responsive? Mobile flips defaults: bottom nav for top destinations, single-breadcrumb, hamburger placement by OS convention.
- **Content-focused or task-based?** Content apps (news, video) can minimize chrome and hide secondary nav; task apps (booking, fitness) need persistent, visible navigation.
- **Entry points** — do users land deep via search/links? Then wayfinding signals (breadcrumbs, titles, URLs) matter far more than the homepage path.

---

## The always-apply core (correct for almost every case)

### Layer the navigation systems — each has a job

**Global** (main sections, consistent on every page) · **local** (within a section; inverted-L with global on top) · **contextual** (related links in/after content) · **utility** (login, search, language, account — top corner, familiar labels, *text* language names not flags) · **footer** (legal, sitemap, contact, social; a "fat footer" can carry rich secondary nav). Don't make one layer do another's job — breadcrumbs never replace global nav.

### Always answer "where am I?"

- **Selected state in the nav** — the current section is visually marked (color, underline, offset). Same for the active tab and current pagination page.
- **Breadcrumbs for deep hierarchies** (see specs) so search-engine arrivals get context.
- **Descriptive HTML titles and clean, readable URLs** (`/blog/how-to-bake-cookies`, not `/page1`) — the browser chrome is part of navigation.
- **Logo top-left, always clickable, always to the homepage** — the universal reset button. Centered/right logos measurably hurt navigation.
- **Test it:** show someone a deep page cold and ask "where are you on this site?" If they can't answer, the signals are too subtle.

### Keep essentials visible

- **Never bury primary sections behind a hamburger when space allows.** Hidden navigation is less discoverable; hamburgers are for genuinely secondary items.
- **Visible options beat hidden ones** at every scale: prefer exposed tabs/links over dropdowns when count allows.

### Interaction basics (non-negotiable)

- **Touch targets ≥44×44px**, link text ≥16px, adequate spacing between links.
- **Activate menus on click, not hover-only** — hover fails on touchscreens and keyboards. If using hover (mega menus): 0.5s intent delay, 0.1s display.
- **Caret/arrow icons signal submenus**; grayed-out (not removed) unavailable options.
- **Icons accompany labels, not replace them** — icon-only nav gets ignored or misread.
- **Frequent destinations within easy reach** (Fitts's law — order menu items by real usage).
- **Sticky headers/menus on long pages** so navigation never requires scrolling back up — kept compact so they don't eat the viewport.

---

## The context-dependent decisions (surface, don't auto-apply)

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Top bar vs. vertical sidebar** | Top bar: ≤7 stable sections, content-first sites. Sidebar: many/growing categories, B2B/enterprise/gov, apps — better scanning (attention leans left), drops into mobile unchanged | Sidebar eats horizontal space on small screens — plan breakpoints | Top bar for shallow/stable; left sidebar for broad/growing IA |
| **Hamburger menu** | Secondary options; mobile space constraints | Hiding primary sections; desktop with room to expose them | Essentials visible + hamburger for the rest; top-left on Android, per-platform elsewhere |
| **Mega menu** | Large catalogs needing 2-D scannable category panels | Few categories (a plain dropdown is calmer); uncontrolled hover triggers | Chunk into medium-granularity groups (card-sort informed), concise labels, don't cover the page |
| **Tabs** | 2–9 parallel content categories with short labels, same hierarchy level | Sequential steps (use a progress tracker); >1 row of tabs (never stack rows) | Fixed tabs on desktop; scrollable tabs for many categories on mobile |
| **Bottom nav (mobile)** | 3–5 global destinations needing one-handed reach | More than 5 (clutter); secondary actions | The mobile default for top-level app navigation |
| **Breadcrumbs** | Deep hierarchies (e-commerce, docs, large blogs); users land mid-site | Flat sites (1–2 levels) — pure noise | Add at depth ≥3; on mobile, a single "up one level" link |
| **Pagination vs. infinite scroll** | Users need to refind items, compare, feel progress (catalogs, search results, archives) — finite pages aid decisions and conversion | Pure leisure feeds | Pagination for goal-driven browsing; infinite scroll only for ambient consumption |
| **Gesture navigation** | Engaging mobile patterns (swipe actions) with onboarding cues | As the *only* path to a function (undiscoverable) | Gestures as accelerators on top of visible controls |
| **Quick links** | Frequently needed or hard-to-find content promoted site-wide | Duplicating what global nav already exposes | A small, curated set — not a second menu |

---

## Component specs (when the pattern is chosen)

**Headers** — logo top-left + meaningful section labels + at most one primary CTA (top-right). Don't overload: menu, logo, search, one CTA. Compact height; 16px+ text; 44px+ targets; padding so elements never touch edges; visually distinct from content (contrast or border). Responsive: collapses gracefully, secondary items into the hamburger — never the essentials.

**Tabs** — uniform look and behavior; selected tab clearly highlighted *and* visually connected to its content; unselected tabs visible (not disabled-looking); hover effect for interactivity; one row only; white space over vertical dividers; content transition direction matches tab direction (parenting principle); ≥12px vertical padding, 44px touch targets; concise labels ("Orders," not "Order History").

**Breadcrumbs** — show **hierarchy, not browsing history**; start at Home; current page last, styled distinct and not clickable; every other item a real, clickable page; familiar dividers (> / →); positioned top of page below the header, left-aligned (mirrored for RTL); subtle styling — it's secondary nav (but still ≥4.5:1 contrast); overflow menus truncate long trails (keep first + last visible); truncate long labels with tooltip access to full text.

**Pagination** — current page clearly marked; previous/next plus first/last (« ») controls; page counter ("Page 3 of 10"); smart truncation of long page lists (always show first, last, current); optional manual page input and items-per-page selector for data-heavy lists; controls at the bottom of the content, generous click areas, 4.5:1 contrast.

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After generating or revising, hand the result to the audit lenses rather than declaring it done. These are **candidate** lenses — posture is set by `docs/orchestration-policy.md`, or route the whole thing through `ux-design-review`. Here, **`heuristics` and `microcopy` are Tier A (auto-run); `accessibility`, `aesthetics`, `information-architecture`, and `mobile-responsiveness` are Tier B (offered)** — under an existing design system `aesthetics` is suppressed and `accessibility` narrows to usage; `mobile-responsiveness` applies only on mobile. If the user invoked this skill for one specific thing, respect that scope.

- **`ux-heuristics-audit`** *(Tier A)* — visibility of system status (selected states), match to mental models, consistency, recognition over recall.
- **`ux-accessibility-audit`** *(Tier B — offer; narrow under a design system)* — keyboard operability of menus, touch targets, contrast, hover-dependence, focus order through nav.
- **`ux-aesthetics-audit`** *(Tier B — offer; suppress under a design system)* — header/menu density, spacing rhythm, whether chrome overwhelms content.
- **`ux-microcopy-audit`** *(Tier A)* — section/tab/breadcrumb label clarity and conciseness, descriptive titles.
- **`ux-information-architecture-audit`** *(Tier B — offer)* — whether the category structure itself (grouping, depth, labels) matches user mental models; this skill places the nav, IA owns the structure.
- **`ux-mobile-responsiveness-audit`** *(Tier B — offer; applies only on mobile)* — when the context is mobile: bottom nav, breakpoints, one-handed reach.

If the audits surface a conflict (e.g., brand wants a minimal icon-only sidebar vs. findability), resolve back toward the primary task: users must always know where they are, what's here, and how to get where they're going.

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Hamburger-everything because it's clean | Essentials visible; hamburger only for secondary items |
| Pick top bar vs. sidebar by aesthetics | Decide by IA breadth, growth, and platform |
| Breadcrumbs that record the user's click path | Breadcrumbs that mirror the site hierarchy |
| Hover-only dropdowns | Click activation; hover with 0.5s intent delay as enhancement |
| Icon-only nav items | Icons + text labels |
| Two rows of tabs | One row; scrollable tabs or restructure categories |
| No selected state anywhere | Current section, tab, and page always marked |
| Centered logo linking nowhere | Logo top-left, clickable, → homepage |
| Infinite scroll on a product catalog | Pagination — users need to refind and compare |
| Flags as language selectors | Text labels in each language's own name |
| Ship without checking | Hand off to heuristics + accessibility + aesthetics + microcopy |

---

## Source lessons (Uxcel)

- [Types of Navigation Systems](https://uxcel.com/lessons/types-of-navigation-systems-403)
- [Common Navigation Patterns](https://uxcel.com/lessons/common-navigation-patterns-046)
- ["You're Here" Navigation System](https://uxcel.com/lessons/youre-here-navigation-system-654)
- [Utility Navigation](https://uxcel.com/lessons/utility-navigation-960)
- [Best Practices for Vertical Navigation](https://uxcel.com/lessons/best-practices-for-vertical-navigation-466)
- [How to Design Tabs for Clear Navigation](https://uxcel.com/lessons/horizontal-navigation-242)
- [Best Practices for Designing Tab Navigation](https://uxcel.com/lessons/navigation-best-practices-771)
- [How to Design Breadcrumbs for Better Navigation](https://uxcel.com/lessons/best-practices-382)
- [Best Practices for Designing Breadcrumbs](https://uxcel.com/lessons/breadcrumbs-best-practices-269)
- [When & How to Use Headers in UIs](https://uxcel.com/lessons/headers-441)
- [Best Practices for Designing Headers](https://uxcel.com/lessons/headers-best-practices-255)
- [Guide to Designing Pagination](https://uxcel.com/lessons/anatomy-216)
- [Best Practices for Designing Pagination](https://uxcel.com/lessons/best-practices-005)
- [Mobile Navigation Design](https://uxcel.com/lessons/navigation-678)
