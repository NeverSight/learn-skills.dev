---
name: data-tables
description: Designs and builds data tables that people can scan, compare and act on, covering column priority, alignment with tabular figures, sticky headers, sorting and filtering, pagination versus virtualization, row selection and bulk actions, inline editing, density, truncation, responsive patterns and accessible table semantics. Use when asked to build a table, data grid, admin list or records view. Not for charts (use data-visualization).
---

# Data Tables

Produces a table that is easy to scan, compare, and act on at any screen size, with correct semantics, predictable keyboard behavior, and a plan for large data.

## When to use
- "Build a table for users / orders / invoices" or "make this list a data grid."
- Adding sorting, filtering, search, pagination, or bulk actions.
- The table is too wide on mobile or slow with thousands of rows.
- Inline editing of records, or a spreadsheet-like admin view.
- Auditing a table for alignment, density, or accessibility.

## Workflow
1. Gather columns, data types, typical and maximum row counts, and the top 2–3 tasks (find a record, compare values, update in bulk). State assumptions if not given.
2. Rank columns: the identifier plus 2–4 decision-driving columns first; secondary columns hidden by default, behind a column picker, or in a detail view.
3. Write a column spec: type, alignment, format, min and max width, sortable, filterable, priority.
4. Choose the scaling strategy from row count and task (see Rules).
5. Define interactions: sort, filter, search, row click target, selection, bulk actions, inline edit.
6. Define density options and the responsive strategy for narrow screens.
7. Build with native table semantics; add loading, empty, no-results, and error states (see ui-states).
8. Test with keyboard only, a screen reader, 1,000+ rows of realistic data, and a 320px viewport.

## Rules
**Alignment and format**
- Text left-aligned; numbers and currency right-aligned with `font-variant-numeric: tabular-nums`; each header aligns with its column's data.
- One precision per column (all 2 decimals); units in the header ("Amount (USD)"), not repeated in every cell. Dates use one consistent format per column.
- Status shown as text plus icon or badge, never color alone.

**Structure**
- Use `table`, `caption` (visually hidden if needed), `thead`, `th scope="col"`, and `th scope="row"` for the identifier cell. Reserve `role="grid"` for tables that implement full arrow-key cell navigation.
- Sticky header (`position: sticky; top: 0` on `th`) when the table is taller than the viewport; sticky first column when it scrolls horizontally.
- Horizontal scrolling happens inside a wrapper with `role="region"`, an `aria-label`, and `tabindex="0"` so keyboard users can scroll it.

**Sorting, filtering, search**
- The sort control is a `button` inside the `th`; only the sorted column has `aria-sort` (`ascending` or `descending`) and a direction icon. The default sort is meaningful (newest first, highest priority) and visible.
- Active filters appear as removable chips with a result count ("124 of 2,310 orders") and Clear all; search input is debounced about 250–300ms.

**Scale**
- Paginate when users reference positions or share views: show range and total, page sizes 25/50/100. Avoid infinite scroll on tables people return to or that have content below them.
- Virtualize when rendering more than about 1,000 rows; set `aria-rowcount` on the table and `aria-rowindex` on rendered rows.

**Selection, actions, editing**
- Checkbox column with a header select-all that shows an indeterminate state; Shift+click selects a range.
- With rows selected, a bulk action bar shows "N selected", the actions, and Clear; selecting all results across pages is an explicit second step ("Select all 2,310"). Destructive bulk actions confirm with the count or offer Undo.
- Inline edit: Enter or double-click to edit, Enter to save, Escape to cancel; show saving and error per cell and never discard the typed value on failure.

**Density, truncation, responsive**
- Offer density only for daily-use tables: compact about 32–36px, default 44–48px, comfortable 52–56px row height. Interactive targets stay at least 24×24px.
- Truncate long text with an ellipsis and expose the full value on hover and keyboard focus; never truncate numbers, IDs, or the identifier column.
- Below the table's minimum width, hide low-priority columns or switch to stacked cards with label–value pairs, keeping the identifier and primary value visible.

## Output
- Column spec table (name, type, alignment, format, width, sortable, filterable, priority).
- Table component in semantic HTML with CSS custom properties, or React + Tailwind; use a table library such as TanStack Table only if it is already installed.
- Loading skeleton rows, empty state, no-results state with Clear filters, and error state with Retry.

## Avoid
- `div` grids with no table or grid roles, or tables used for page layout.
- Centered or proportional-width numbers that cannot be compared down a column.
- Zebra stripes, full cell borders, and heavy row hover all at once; one or two separators are enough.
- Row actions visible only on hover; give each row a visible, focusable overflow menu.
- Truncated text with no way to read the full value.
- A fully clickable row containing nested buttons; make the identifier the link instead.
- Resetting scroll position, sort, or selection after an edit or refresh.

## Final check
- [ ] Numbers right-aligned with tabular-nums, text left-aligned, headers matching their columns.
- [ ] `caption`, `th scope`, and `aria-sort` on the sorted column are present.
- [ ] Header stays visible on long tables; the scroll container is keyboard focusable.
- [ ] Select-all with indeterminate state and a bulk bar with count both work.
- [ ] Large datasets use pagination or virtualization with `aria-rowcount`.
- [ ] Works at 320px without page-level horizontal scrolling.
- [ ] Loading, empty, no-results, and error states exist.
