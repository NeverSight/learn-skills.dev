---
name: tanstack-virtual
description: 'TanStack Virtual for virtualizing large lists, grids, and tables. Use when rendering thousands of rows, implementing infinite scroll, or optimizing large data displays. Use for virtual, virtualize, virtual-list, virtual-scroll, useVirtualizer, infinite-scroll, windowing.'
license: MIT
metadata:
  author: oakoss
  version: '1.1'
  source: 'https://tanstack.com/virtual/latest'
---

# TanStack Virtual

## Overview

TanStack Virtual is a headless UI utility for virtualizing large lists, grids, and tables. It renders only the visible items in the viewport, dramatically reducing DOM nodes and improving performance for datasets with thousands of rows. Framework adapters are available for React, Vue, Solid, Svelte, Lit, and Angular.

**When to use:** Rendering thousands of rows or columns, building virtualized tables, implementing infinite scroll, displaying large datasets where DOM node count impacts performance.

**When NOT to use:** Small lists under ~100 items (no performance benefit), server-rendered static content, layouts where all items must be in the DOM for SEO or accessibility, simple pagination (render one page at a time instead).

## Quick Reference

| Pattern             | API                                                         | Key Points                                               |
| ------------------- | ----------------------------------------------------------- | -------------------------------------------------------- |
| Vertical list       | `useVirtualizer({ count, getScrollElement, estimateSize })` | Wrap items in absolute-positioned container              |
| Horizontal list     | `useVirtualizer({ horizontal: true, ... })`                 | Use `getTotalSize()` for width instead of height         |
| Grid layout         | Row virtualizer + column virtualizer                        | Two virtualizer instances sharing one scroll element     |
| Dynamic sizing      | `ref={virtualizer.measureElement}`                          | Set `data-index` on each element                         |
| Window scroller     | `useWindowVirtualizer({ count, estimateSize })`             | No `getScrollElement` needed                             |
| Scroll to item      | `virtualizer.scrollToIndex(index)`                          | Supports `align: 'start' \| 'center' \| 'end' \| 'auto'` |
| Scroll to offset    | `virtualizer.scrollToOffset(px)`                            | Supports `align` and `behavior: 'smooth'`                |
| Custom keys         | `getItemKey: (index) => items[index].id`                    | Stable keys improve measurement cache                    |
| Overscan            | `overscan: 5`                                               | Renders extra items outside viewport (default: 1)        |
| Gap between items   | `gap: 8`                                                    | Space between virtualized items in pixels                |
| Multi-lane layout   | `lanes: 3`                                                  | Masonry-style column layouts                             |
| Padding             | `paddingStart: 100, paddingEnd: 100`                        | Space before first and after last item                   |
| RTL support         | `isRtl: true`                                               | Right-to-left horizontal scrolling                       |
| Range extractor     | `rangeExtractor: (range) => [...]`                          | Customize rendered indices (sticky headers, footers)     |
| Disable virtualizer | `enabled: false`                                            | Renders nothing, resets internal state                   |
| Force remeasure     | `virtualizer.measure()`                                     | Call after external layout changes                       |

## Common Mistakes

| Mistake                                             | Correct Pattern                                                                                             |
| --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Missing `overflow: auto` on scroll container        | Parent element must have `overflow: auto` and a fixed height/width                                          |
| Using `virtualItem.index` as React key              | Use `virtualItem.key` which accounts for dynamic reordering                                                 |
| Forgetting `position: relative` on inner container  | The total-size container must be `position: relative`                                                       |
| Not setting `data-index` with `measureElement`      | Dynamic measurement requires `data-index={virtualItem.index}` on each element                               |
| Setting `estimateSize` too small for dynamic items  | Overestimate to prevent scroll jumping; use largest expected size                                           |
| Recreating `getScrollElement` on every render       | Use a ref callback: `() => parentRef.current`                                                               |
| Not using `getTotalSize()` for container dimensions | Inner container height/width must equal `virtualizer.getTotalSize()`                                        |
| Absolute positioning without `transform`            | Use `transform: translateY(item.start)` for GPU-accelerated positioning                                     |
| Using `contain: strict` without fixed dimensions    | `contain: strict` requires explicit width and height on the scroll container                                |
| Using with React Compiler without opting out        | Add `'use no memo'` directive to components using `useVirtualizer` — interior mutability breaks memoization |

## Delegation

> If the `tanstack-table` skill is available, delegate data table virtualization to it. TanStack Table has built-in virtualization integration.
> Otherwise, recommend: `npx skills add oakoss/agent-skills --skill tanstack-table`
>
> If the `tanstack-query` skill is available, delegate data fetching and infinite query patterns to it.
> Otherwise, recommend: `npx skills add oakoss/agent-skills --skill tanstack-query`

## References

- [List virtualization with useVirtualizer](references/list-virtualization.md)
- [Grid virtualization with row and column virtualizers](references/grid-virtualization.md)
- [Dynamic sizing with measureElement](references/dynamic-sizing.md)
- [Infinite scroll with TanStack Query integration](references/infinite-scroll.md)
