---
name: ux-tables
description: Design or critique data tables and lists — scannable structure, alignment rules (left for text, right for numbers), sorting/filtering, row interactions, and the right list type for the content. Trigger when the user asks to design or review a data table, data grid, admin table, list view, email/feed list, or asks how to present tabular or structured data.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Tables & Lists Skill

## How this skill behaves (read first)

This is a **generative** skill. The default failure modes: **decoration over data** (heavy borders, zebra everything, centered text, mixed formats), **missing manipulation** (no sorting, no customization — fatal at real data volumes), and **density extremes** (cramped 32px rows or wasteful spacing). A table's only job is letting users *scan, compare, and act on* data — every visual choice either serves that or fights it. This skill gates:

1. **Establish the data shape and tasks** — 2-D comparison (table) vs. 1-D scanning (list), volume, and what users do with rows.
2. **Apply the always-true core** — alignment rules, hierarchy, formats, interaction states.
3. **Surface the context-dependent decisions** (density, pagination type, customization, list variants) with trade-offs.

Then it **hands off to `ux-heuristics-audit`, `ux-accessibility-audit`, `ux-aesthetics-audit`, and `ux-microcopy-audit`** for validation.

---

## Step 0 — Establish context before designing

Ask if not known; state the assumption if proceeding without an answer:

- **Table or list?** Multi-attribute comparison across columns → table. One item per row scanned linearly (emails, results, settings) → list. Simple-table content often reads better as a list — and lists are easier for screen-reader users.
- **Data volume and growth** — tens of rows need none of the machinery; thousands need sorting, filtering, pagination, items-per-page, search.
- **What do users do with rows?** Read-only, single-row actions (inline ⋮ menu), bulk operations (multi-select checkboxes), or editing — each adds specific UI.
- **Density tolerance** — data-dense ops tools (condensed 40px rows) vs. consumer comfort (regular 48px / relaxed 56px).

---

## The always-apply core (correct for almost every case)

### Alignment and formatting (the silent rules everyone breaks)

- **Text left-aligned** (LTR), matching the reading direction.
- **Numbers right-aligned, in tabular figures** (equal-width digits) — that's what makes columns of numbers comparable at a glance.
- **One consistent format per column** — never "22.04.2018" next to "4.6.2018"; one date, currency, and unit format throughout.
- **Legible sans-serif typeface**; column margins wide enough to scan, compare, and edit comfortably.

### Hierarchy without noise

- **Headers visibly distinct** (weight, slightly darker background) but not shouting; **never empty header cells** — including the top-left one.
- **Borders are a last resort:** minimal lines beat grid-everything. Horizontal dividers only when row spacing is tight or tables are very long; zebra striping for wide, dense data sets.
- **Overflow handled explicitly:** truncate with ellipsis + tooltip for full text, resizable columns, or hideable/reorderable columns.

### Interaction (what makes it a tool, not a picture)

- **Sorting on every meaningful column** — alphabetical, numeric, date, ascending/descending. Non-negotiable at volume.
- **Hover state + selected state on rows** — users lose their place in uniform rows without them.
- **Row actions hidden until hover** (or behind an inline ⋮ menu — see `ux-menus`); **bulk-action checkboxes always visible**, with bulk actions appearing on selection.
- **Toolbar above the table** for search, filter, export, print when the data warrants it.
- **Links look like links** — recognizable styling, distinct from body text, hover feedback.

### Lists: structure and loading

- **Type from content:** single-line (names, settings) → multi-line (email: sender + subject + preview) → rich (media + actions) → image list (galleries) → nested (hierarchies, with clear indentation) → ordered only when sequence matters.
- **Vertical beats horizontal** — fewer eye movements, natural scrolling; horizontal lists only for short, non-scrolling sets.
- **Keyline alignment:** text and icons aligned to invisible vertical guides; thumbnails left; control elements (checkboxes, menus) right; text vertically centered against images.
- **Dividers when items span 3+ lines** (email-style); indented dividers for lists with thumbnails; otherwise white space.
- **Loading: skeleton screens loading sequentially top-to-bottom** — not a fullscreen spinner.

---

## The context-dependent decisions (surface, don't auto-apply)

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Row density** | Condensed (40px) when seeing everything at once matters (ops, trading) | Condensed for casual reading (strain) | Regular 48px; relaxed 56px for consumer comfort |
| **Pagination vs. infinite vs. "Load more"** | Pagination: refindability, reports, position sense. Infinite: leisure feeds. Manual "Load more": browsing + control | Infinite scroll where users must refind or cite rows | Pagination for data work + items-per-page control; "Load more" as the middle ground |
| **Zebra striping** | Wide tables where the eye drifts across long rows | Narrow tables (visual noise) | Plain rows + hover state first; zebra at width |
| **Column customization** | Power users, many columns (resize, hide, reorder) | Simple fixed tables (overhead) | Offer at >6–8 columns or mixed audiences |
| **Toolbar (search/filter/export)** | Real data volume; recurring lookup tasks | A 20-row table (clutter) | Add capabilities as volume demands them |
| **List vs. grid view toggle** | Mixed browsing styles, visual + spec content | One clearly right view | Default to the fit; toggle for diverse audiences (see `ux-search` for results pages) |
| **Searchable/filterable lists** | Long lists (contacts, catalogs) | Short lists | Search bar on top once scanning stops being instant |
| **Simple vs. complex table structure** | Merged cells/multi-level headers only when the data truly demands it | Screen readers and cognition both struggle with complex structures | Split complex tables into simple ones; one header level |

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After generating or revising, hand the result to the audit lenses rather than declaring it done. These are **candidate** lenses — posture is set by `docs/orchestration-policy.md`, or route the whole thing through `ux-design-review`. Here, **`heuristics` and `microcopy` are Tier A (auto-run); `accessibility`, `aesthetics`, and `mobile-responsiveness` are Tier B (offered)** — under an existing design system `aesthetics` is suppressed and `accessibility` narrows to usage; `mobile-responsiveness` applies only on mobile. If the user invoked this skill for one specific thing, respect that scope.

- **`ux-heuristics-audit`** *(Tier A)* — visibility of state (sort direction, selection), user control (customization, items-per-page), consistency of formats.
- **`ux-accessibility-audit`** *(Tier B — offer; narrow under a design system)* — semantic structure (real `<table>`, `<th>` + scope, captions; list markup for lists), header completeness, proportional widths, link contrast — assistive tech depends on markup this skill specifies.
- **`ux-aesthetics-audit`** *(Tier B — offer; suppress under a design system)* — border/zebra restraint, density rhythm, alignment discipline.
- **`ux-microcopy-audit`** *(Tier A)* — header label clarity and brevity, empty-state and toolbar wording.
- **`ux-mobile-responsiveness-audit`** *(Tier B — offer; applies only on mobile)* — when the context is mobile: responsive list adaptation, column collapsing strategy.

If the audits surface a conflict (e.g., brand styling vs. scannability), resolve back toward the primary task: users come to compare and find — decoration that slows a scan is a defect.

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Center-align everything | Text left, numbers right in tabular figures |
| "22.04.2018" and "4.6.2018" in one column | One consistent format per column |
| Full grid borders on every cell | Minimal lines; dividers/zebra only when they earn it |
| Large table with no sorting | Sortable columns, toolbar at volume |
| Uniform rows, no hover/selected state | Hover + selection states so users keep their place |
| Action buttons cluttering every row | Hover-revealed actions / inline ⋮; visible checkboxes for bulk |
| Cell text silently clipped | Ellipsis + tooltip; resizable/hideable columns |
| Infinite scroll on a financial report | Pagination + items-per-page; refindability wins |
| Merged cells and double-decker headers | Simple structure; split tables |
| Fullscreen spinner while a list loads | Sequential skeleton loading |
| Layout-by-table, headerless data tables | Semantic markup — real headers, captions (→ accessibility) |
| Ship without checking | Hand off to heuristics + accessibility + aesthetics + microcopy |

---

## Source lessons (Uxcel)

- [When & How to Use Tables in UIs](https://uxcel.com/lessons/tables-152)
- [Best Practices for Designing Tables in UIs](https://uxcel.com/lessons/tables-best-practices-356)
- [Tables & Lists Accessibility](https://uxcel.com/lessons/accessible-tables-712)
- [UI Lists & When to Use Them](https://uxcel.com/lessons/anatomy-758)
- [Best Practices for Designing Lists](https://uxcel.com/lessons/lists-best-practices-814)
