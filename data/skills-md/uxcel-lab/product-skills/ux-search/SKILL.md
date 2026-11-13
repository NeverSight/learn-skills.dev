---
name: ux-search
description: Design or critique search experiences — search input, auto-suggest, results page, filtering/sorting, and zero-results recovery. Matches search features to how users actually seek (known-item vs. exploratory) and gates levers like rich suggestions, filter layout, and chips. Trigger when the user asks to design or review search, a search bar, autocomplete/auto-suggest, search results, filters, sorting, or a "no results" page.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Search Skill

## How this skill behaves (read first)

This is a **generative** skill. The default failure modes: **a box and nothing more** (an input that returns a bare list — no suggestions, no query persistence, no recovery), **dead ends** ("No results found." period), and **feature stacking** (rich suggestions + trending + recent + filters + chips everywhere, even where search is a minor utility). Search is a *journey* — formulate → suggest → results → refine — and which stages need investment depends on how users seek. This skill gates:

1. **Establish how users seek and how central search is** — that decides which stages to invest in.
2. **Apply the always-true core** — discoverable placement, working input conventions, suggestion basics, a scannable results page, no dead ends.
3. **Surface the context-dependent decisions** (rich auto-suggest, filter layout, chips, view options) with trade-offs.

Then it **hands off to `ux-heuristics-audit`, `ux-accessibility-audit`, `ux-aesthetics-audit`, and `ux-microcopy-audit`** for validation.

---

## Step 0 — Establish context before designing

Ask if not known; state the assumption if proceeding without an answer:

- **How do users seek here?** **Known-item** (they can name what they want — invest in the input, auto-suggest, re-finding) vs. **exploratory/semi-directed** (vague needs that evolve — invest in suggestions, related searches, filters, browsing). **Re-finding** is chronically underserved: recent searches and history pay off everywhere.
- **How central is search?** Search-first product (e-commerce, docs, booking) → persistent, prominent search and a rich results page. Search-as-emergency-exit → simpler treatment, but still discoverable.
- **Platform** — mobile: persistent search (search-focused apps) vs. expandable icon (search-secondary apps); filters concealed behind a Filter button; comfortable one-handed targets.
- **Result type** — products with images vs. documents vs. data rows: drives list-vs-grid and what a result row shows.

Remember information needs **evolve mid-search** and people **browse rapidly** (most page visits <10s) — design for iteration and scanning, not one perfect query.

---

## The always-apply core (correct for almost every case)

### The input

- **Put search where users look for it:** top center or top right, on every page. Never behind a hamburger; on desktop, show the field itself, not just an icon.
- **Magnifying-glass icon inside the bar, and it's a working button** that submits the query.
- **~27-character input width** — cramped inputs cause cramped, worse queries.
- **Placeholder = example queries** ("Search flights, hotels, destinations"), muted so it can't read as filled-in text — never a label replacement.

### Suggestions (the formulate stage)

- **Auto-suggest as users type** — fewer typos, less cognitive load, faster queries. Cap at **~10 suggestions, no scrolling** in the dropdown.
- **Visually split typed vs. suggested characters** (bold/color) so users can scan why each suggestion appears.
- **Recent searches when the field is focused** — recognition over recall for re-finding.

### The results page

- **Keep the query visible and editable** — first attempts usually need tweaking; never make users retype.
- **Show the match count** — it tells users whether to refine, broaden, or start reviewing.
- **Highlight matching keywords in results** — users scan, they don't read.
- **Loading is part of the experience:** skeleton screens for result areas; progress/spinner with a short explanation for longer waits.
- **Pagination type fits the content** (see `ux-navigation` for the pagination vs. infinite scroll decision and control specs).

### No dead ends — ever

A bare "No results found" is the single worst search failure. The No-Results page **always** offers a way forward: alternative query suggestions, category links, similar/related items, or recommendations from past behavior.

---

## The context-dependent decisions (surface, don't auto-apply)

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Rich auto-suggest** (thumbnails, category links, product previews) | Known-item seeking with visual goods (e-commerce) | Simple utility search — clutter slows the dropdown | Plain query suggestions first; enrich only when recognition genuinely speeds choice |
| **Trending/related searches before typing** | Exploratory products where inspiration helps (stores, media) | Task tools where it's noise | Show for discovery-driven products only |
| **Persistent vs. expandable search (mobile)** | Persistent for search-focused apps; expandable icon to save space elsewhere | Hiding search in a search-first app | Match prominence to search centrality |
| **Filters** | Results sets large enough to need narrowing | A dozen results (filters are overhead) | 5–7 visible filters, rest behind "More filters"; most-used first (from data); checkboxes for multi-select; familiar words ("Fabric," not "Textile") |
| **Filter layout** | Vertical sidebar: many filter groups, desktop. Horizontal panel: few, attention-grabbing. Mobile: behind a Filter button above results | Horizontal with many groups (eats the screen); sidebars users overlook | Vertical for filter-heavy desktop; horizontal for ≤ a handful; concealed on mobile |
| **Auto-update vs. Apply button** | Auto-update results as filters change (low interaction cost) | Slow connections / heavy queries — batch with an Apply button showing the match count | Auto-update when fast; Apply+count when not |
| **Filter chips** | Compact, tappable refinement ("Open now," "Price: $$") updating results in place; applied-filter overview tags with × to remove | Mixing single- and multi-select chip sets on one page; chips below 48px touch targets | Chips for quick filters + applied-filter overview; full panel for deep filtering |
| **Sorting** | Always for comparable items (price, date, popularity) — users often prefer sorting over filtering | Merging it into the filter panel (different mental model) | Separate, visible sort control |
| **List vs. grid view** | List: spec-comparison (model numbers, ratings). Grid: visual goods | Forcing one view for mixed content | Default to the fit; offer a view toggle |

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After generating or revising, hand the result to the audit lenses rather than declaring it done. These are **candidate** lenses — posture is set by `docs/orchestration-policy.md`, or route the whole thing through `ux-design-review`. Here, **`heuristics` and `microcopy` are Tier A (auto-run); `accessibility`, `aesthetics`, `information-architecture`, and `mobile-responsiveness` are Tier B (offered)** — under an existing design system `aesthetics` is suppressed and `accessibility` narrows to usage; `mobile-responsiveness` applies only on mobile. If the user invoked this skill for one specific thing, respect that scope.

- **`ux-heuristics-audit`** *(Tier A)* — visibility of system status (loading, match counts, applied filters shown twice), user control (clear-all-filters, editable query), recognition over recall (recent searches).
- **`ux-accessibility-audit`** *(Tier B — offer; narrow under a design system)* — keyboard operability of the suggestion dropdown, touch targets (chips ≥48px, spacing ≥8px), contrast, focus management between input and results.
- **`ux-aesthetics-audit`** *(Tier B — offer; suppress under a design system)* — results-page density and scannability, dropdown clutter, filter-panel visual organization.
- **`ux-microcopy-audit`** *(Tier A)* — placeholder examples, filter labels in users' language, No-Results message tone and guidance.
- **`ux-information-architecture-audit`** *(Tier B — offer)* — whether the content structure feeding search (categories, facets, metadata) supports the seeking modes, and whether browse paths complement search; this skill designs the search journey, IA owns the structure it searches.
- **`ux-mobile-responsiveness-audit`** *(Tier B — offer; applies only on mobile)* — when the context is mobile: expandable/persistent pattern, concealed filters, one-handed reach.

If the audits surface a conflict (e.g., rich suggestions vs. dropdown speed and clarity), resolve back toward the primary task: the user wants to *find the thing* — every feature must shorten that path.

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Search behind a hamburger / icon-only on desktop | Visible field, top center/right, every page |
| Tiny input that fits two words | ~27 characters — room to think in keywords |
| Suggestion dropdown with 25 scrolling entries | ≤10, no scroll, typed vs. suggested visually split |
| Query vanishes when results load | Query stays, editable |
| "No results found." and nothing else | Alternatives: corrected queries, categories, related items |
| Bare result list with no count | Match count + highlighted keywords |
| 20 filters dumped in a sidebar | 5–7 visible, popular first, rest behind "More filters" |
| Applied filters invisible once set | Shown twice: checked in panel + removable overview tags |
| Sorting buried inside filters | Separate sort control — different mental model |
| Radio buttons for combinable criteria | Checkboxes / multi-select chips |
| Blank screen while results load | Skeleton screens; spinner + explanation for long waits |
| Ship without checking | Hand off to heuristics + accessibility + aesthetics + microcopy |

---

## Source lessons (Uxcel)

- [How to Design Good Search Experiences in UIs](https://uxcel.com/lessons/anatomy-350)
- [Best Practices for UI Search Design](https://uxcel.com/lessons/search-best-practices-248)
- [How People Seek Information](https://uxcel.com/lessons/how-people-seek-information-191)
- [Best Practices for Filtering & Sorting Design](https://uxcel.com/lessons/filter--sort-best-practices-369)
- [How to Design UI Chips for Filtering & Selection](https://uxcel.com/lessons/anatomy-694)
