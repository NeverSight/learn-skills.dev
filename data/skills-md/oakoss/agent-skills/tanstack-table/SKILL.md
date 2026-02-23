---
name: tanstack-table
description: |
  TanStack Table v8 headless data tables for React. Covers column definitions, sorting, filtering (fuzzy/faceted), server-side pagination with TanStack Query, infinite scroll, virtualization (TanStack Virtual), column/row pinning, row expanding/grouping, column resizing, and reusable Shadcn-styled components. Prevents 15 documented errors including infinite re-renders, React Compiler incompatibility, and server-side state mismatches.

  Use when building data tables, fixing table performance, implementing server-side pagination, adding filtering/sorting, or debugging table state issues.
license: MIT
metadata:
  author: oakoss
  version: '1.1'
  source: 'https://tanstack.com/table/latest/docs'
---

# TanStack Table

## Overview

TanStack Table is a **headless** table library — it provides state management and logic but no UI. You supply the rendering; it handles sorting, filtering, pagination, selection, and more.

**When to use:** Complex data tables with sorting/filtering/pagination, server-side data, large datasets (1000+ rows with virtualization), row selection/expanding/grouping.

**When NOT to use:** Simple static tables (use `<table>` directly), display-only lists (use a list component), spreadsheet-like editing (consider AG Grid).

## Quick Reference

| Pattern           | API / Config                                         | Key Points                                   |
| ----------------- | ---------------------------------------------------- | -------------------------------------------- |
| Basic table       | `useReactTable({ data, columns, getCoreRowModel })`  | Memoize data/columns to prevent re-renders   |
| Column helper     | `createColumnHelper<T>()`                            | Type-safe column definitions                 |
| Column groups     | `columnHelper.group({ header, columns })`            | Nested headers; don't pin group columns      |
| Sorting           | `getSortedRowModel()` + `onSortingChange`            | `manualSorting: true` for server-side        |
| Filtering         | `getFilteredRowModel()` + `onColumnFiltersChange`    | `manualFiltering: true` for server-side      |
| Pagination        | `getPaginationRowModel()` + `onPaginationChange`     | `manualPagination: true` + `pageCount`       |
| Row selection     | `enableRowSelection` + `onRowSelectionChange`        | Set `getRowId` for stable selection keys     |
| Column visibility | `onColumnVisibilityChange`                           | Toggle with `column.toggleVisibility()`      |
| Column pinning    | `enableColumnPinning` + `initialState.columnPinning` | Don't pin group columns (known bug)          |
| Row expanding     | `getExpandedRowModel()` + `getSubRows`               | For nested/tree data                         |
| Column resizing   | `enableColumnResizing` + `columnResizeMode`          | `onChange` for live, `onEnd` for performant  |
| Row grouping      | `getGroupedRowModel()` + `aggregationFn`             | Performance degrades at 10k+ rows            |
| Server-side       | `manual*: true` flags + include state in queryKey    | All state in query key for proper refetching |
| Infinite scroll   | `useInfiniteQuery` + flatten pages                   | Combine with TanStack Virtual for best perf  |
| Virtualization    | `useVirtualizer` from `@tanstack/react-virtual`      | Disable when container hidden (tabs/modals)  |
| React 19 Compiler | `'use no memo'` directive                            | Required until v9 fixes compiler compat      |

## Common Operations

| Task              | Method                         |
| ----------------- | ------------------------------ |
| Sort column       | `column.toggleSorting()`       |
| Filter column     | `column.setFilterValue(value)` |
| First page        | `table.firstPage()`            |
| Next page         | `table.nextPage()`             |
| Previous page     | `table.previousPage()`         |
| Last page         | `table.lastPage()`             |
| Go to page        | `table.setPageIndex(n)`        |
| Select row        | `row.toggleSelected()`         |
| Hide column       | `column.toggleVisibility()`    |
| Get original data | `row.original`                 |
| Pin column        | `column.pin('left')`           |
| Resize column     | `header.getResizeHandler()`    |
| Expand row        | `row.toggleExpanded()`         |

## Row Models

| Import                   | Purpose                 |
| ------------------------ | ----------------------- |
| `getCoreRowModel`        | Required                |
| `getSortedRowModel`      | Sorting                 |
| `getFilteredRowModel`    | Filtering               |
| `getPaginationRowModel`  | Pagination              |
| `getExpandedRowModel`    | Expanding               |
| `getGroupedRowModel`     | Grouping                |
| `getFacetedRowModel`     | Faceted filter counts   |
| `getFacetedUniqueValues` | Unique values per facet |
| `getFacetedMinMaxValues` | Min/max per facet       |

## Common Mistakes

| Mistake                                     | Correct Pattern                                            |
| ------------------------------------------- | ---------------------------------------------------------- |
| Unstable data/columns reference             | Memoize with `useMemo` or define outside component         |
| Missing `manual*` flags for server-side     | Set `manualPagination`, `manualSorting`, `manualFiltering` |
| Query key missing table state               | Include pagination, sorting, filters in queryKey           |
| Import from `@tanstack/table-core`          | Import from `@tanstack/react-table`                        |
| Using v7 `useTable` / `Header` / `accessor` | Use v8 `useReactTable` / `header` / `accessorKey`          |
| Pinning group columns                       | Pin individual columns within the group, not parent        |
| Grouping on 10k+ rows                       | Use server-side grouping or disable for large datasets     |
| Column filter not clearing on page change   | Reset `pageIndex` to 0 when filters change                 |
| Missing `'use no memo'` with React Compiler | Add directive to components using `useReactTable`          |
| Missing `getRowId` with row selection       | Set `getRowId: (row) => row.id` for stable selection keys  |
| Filter value type mismatch                  | Match value types; clear with `undefined`, not `null`      |

## Delegation

- **Table pattern discovery**: Use `Explore` agent
- **Server integration review**: Use `Task` agent
- **Code review**: Delegate to `code-reviewer` agent

> If the `tanstack-query` skill is available, delegate data fetching, caching, and infinite query patterns to it.
> If the `tanstack-virtual` skill is available, delegate standalone virtualization patterns to it.
> If the `tanstack-router` skill is available, delegate URL search param sync for server-side table state to it.
> If the `tanstack-start` skill is available, delegate server functions for server-side data loading to it.

## References

- [Column definitions, helpers, visibility, and selection](references/column-definitions.md)
- [Filtering: column, global, fuzzy, and faceted](references/filtering.md)
- [Server-side patterns with TanStack Query](references/server-side-patterns.md)
- [Infinite scroll with cursor pagination](references/infinite-scroll.md)
- [Reusable table components (Shadcn-styled)](references/reusable-components.md)
- [Virtualization for large datasets](references/virtualization.md)
- [Column and row pinning](references/column-row-pinning.md)
- [Row expanding and grouping](references/expanding-grouping.md)
- [Known issues and solutions (15 documented)](references/known-issues.md)
- [v7 to v8 migration guide](references/v7-migration.md)
