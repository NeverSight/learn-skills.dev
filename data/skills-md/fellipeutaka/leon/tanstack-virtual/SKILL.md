---
name: tanstack-virtual
description: |
  TanStack Virtual headless virtualization for React. Use when rendering large lists (100+ items),
  implementing virtual scroll, building infinite scroll feeds, virtualizing grids or tables,
  using window-level scrolling, or implementing masonry/lane layouts with @tanstack/react-virtual.
  Triggers on: useVirtualizer, useWindowVirtualizer, virtual list, virtual scroll, list virtualization.
metadata:
  tags: tanstack-virtual, react-virtual, virtualization, virtual-scroll, performance, react
---

# TanStack Virtual (React)

## Installation

```bash
npm install @tanstack/react-virtual
```

## Core Concept

Three required options — everything else is optional:

```
count          — total item count
getScrollElement — () => scrollableElement
estimateSize   — (index) => number (px)
```

You must:
1. Create a full-height container using `getTotalSize()`
2. Absolutely position each virtual item using `virtualItem.start`

## Fixed Size (Vertical)

```tsx
import { useRef } from 'react'
import { useVirtualizer } from '@tanstack/react-virtual'

function List({ items }: { items: string[] }) {
  const parentRef = useRef<HTMLDivElement>(null)

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 35,
  })

  return (
    <div ref={parentRef} style={{ height: '400px', overflow: 'auto' }}>
      <div style={{ height: `${virtualizer.getTotalSize()}px`, position: 'relative' }}>
        {virtualizer.getVirtualItems().map((item) => (
          <div
            key={item.key}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: `${item.size}px`,
              transform: `translateY(${item.start}px)`,
            }}
          >
            {items[item.index]}
          </div>
        ))}
      </div>
    </div>
  )
}
```

## Dynamic Size (measured at runtime)

```tsx
const virtualizer = useVirtualizer({
  count: items.length,
  getScrollElement: () => parentRef.current,
  estimateSize: () => 100, // err large for better scroll-to-index accuracy
})

{virtualizer.getVirtualItems().map((item) => (
  <div
    key={item.key}
    data-index={item.index}          // required for measureElement
    ref={virtualizer.measureElement} // measures on mount/resize
    style={{
      position: 'absolute',
      top: 0,
      left: 0,
      width: '100%',
      transform: `translateY(${item.start}px)`,
      // Do NOT set height — virtualizer controls it
    }}
  >
    {items[item.index]}
  </div>
))}
```

## Window Virtualizer

```tsx
import { useRef, useEffect } from 'react'
import { useWindowVirtualizer } from '@tanstack/react-virtual'

function WindowList({ items }: { items: string[] }) {
  const listRef = useRef<HTMLDivElement>(null)

  const virtualizer = useWindowVirtualizer({
    count: items.length,
    estimateSize: () => 35,
    scrollMargin: listRef.current?.offsetTop ?? 0,
  })

  return (
    <div ref={listRef}>
      <div style={{ height: `${virtualizer.getTotalSize()}px`, position: 'relative' }}>
        {virtualizer.getVirtualItems().map((item) => (
          <div
            key={item.key}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: `${item.size}px`,
              transform: `translateY(${item.start - virtualizer.options.scrollMargin}px)`,
            }}
          >
            {items[item.index]}
          </div>
        ))}
      </div>
    </div>
  )
}
```

`scrollMargin` = distance from page top to list top. Subtract it from `item.start` in the transform.

## Imperative Scroll

```tsx
virtualizer.scrollToIndex(50, { align: 'start' }) // 'start' | 'center' | 'end' | 'auto'
virtualizer.scrollToOffset(1200, { behavior: 'smooth' })
```

## Critical Rules

**Always:**
- `overflow: auto` on scroll container
- Explicit `height`/`width` on scroll container
- `position: relative` on inner container sized to `getTotalSize()`
- `position: absolute` on each virtual item
- `translateY`/`translateX` for positioning (not `top`/`left`)
- `data-index` on items when using `measureElement`
- `item.key` as React key (not `item.index`)
- `scrollMargin` for window virtualizers when content precedes the list

**Never:**
- Set `height` on dynamically measured items
- Omit `overflow: auto` on scroll container
- Use `smooth` scroll behavior with dynamic-size items (documented limitation)

## Key Options

| Option | Default | Purpose |
|--------|---------|---------|
| `overscan` | 1 | Extra items rendered outside visible area |
| `gap` | 0 | Spacing between items (px) — use instead of CSS margin |
| `paddingStart` | 0 | Padding before first item (px) |
| `paddingEnd` | 0 | Padding after last item (px) |
| `horizontal` | false | Horizontal orientation |
| `lanes` | 1 | Columns (vertical) or rows (horizontal) for masonry |
| `getItemKey` | index | Stable item keys — always set when items have IDs |
| `enabled` | true | Set false to disable observers and reset state |
| `isRtl` | false | RTL horizontal scroll |

## References

- [Full API: Virtualizer options, instance methods, VirtualItem](references/api.md)
- [Patterns: horizontal, variable size, masonry, sticky, infinite scroll, SSR](references/patterns.md)
