---
name: perf-virtual-lists
description: Specialist in high-performance list virtualization for Android TV (React).
---

# Performance: Virtualized Lists on TV

Rendering large lists (movies, episodes) on Android TV requires **virtualization** to maintain 60FPS.
Standard `map()` rendering will freeze the UI on low-end TV boxes (1GB RAM).

## 🚀 Core Technology
Use **`react-window`** + **`react-virtualized-auto-sizer`**.
It is lighter and faster than `react-virtualized`.

## 📺 TV-Specific Optimizations

### 1. Overscan is Critical
On TV, users scroll FAST (holding the Down button).
You MUST set `overscanCount` (or `overscanRowCount`) to at least **2-3 rows** to prevent "blank" areas during rapid scrolling.

```jsx
<FixedSizeGrid
  overscanRowCount={3} // Prevents blank cells during fast scroll
  ...
/>
```

### 2. Focus Management Strategy
**Problem:** Virtualization unmounts off-screen items. If the focused item is scrolled out, focus is lost, and the browser resets it to `body`.
**Solution:** Do NOT rely on DOM focus (`document.activeElement`) for state.
1.  Use `useTVNavigation` to track `focusedIndex` (data index).
2.  Programmatically scroll to the focused item *before* it gets unmounted? No, just keep the index.
3.  When the item re-mounts (scrolled back properly), the `ref` callback should re-apply focus if needed, or simply render it as `.focused`.

### 3. Fixed vs Variable Size
ALWAYS prefer **`FixedSizeGrid`** or **`FixedSizeList`**.
Variable sizing triggers expensive layout recalculations on every scroll frame, killing performance on TV hardware.

### 4. Image Handling
- Use `loading="lazy"` on `<img>`.
- Even better: Use a custom `<FadeInImage>` that only sets `src` when `inView` (though `react-window` handles visibility well).
- **Crucial:** Set explicit `width` and `height` on images to prevent layout shifts.

## 🛠 Usage Pattern

```jsx
import { FixedSizeGrid } from 'react-window';
import AutoSizer from 'react-virtualized-auto-sizer';

// ... inside your component
<div style={{ height: '100vh', width: '100%' }}>
  <AutoSizer>
    {({ height, width }) => (
      <FixedSizeGrid
        columnCount={4}
        columnWidth={width / 4}
        height={height}
        rowCount={Math.ceil(items.length / 4)}
        rowHeight={300} // Fixed height!
        width={width}
        overscanRowCount={3} // CRITICAL FOR TV
      >
        {({ columnIndex, rowIndex, style }) => {
          const index = rowIndex * 4 + columnIndex;
          if (index >= items.length) return null;
          
          return (
            <div style={style}>
              <MovieCard 
                 item={items[index]} 
                 isFocused={index === focusedIndex} 
              />
            </div>
          );
        }}
      </FixedSizeGrid>
    )}
  </AutoSizer>
</div>
```

## ⚠️ Anti-Patterns
- **❌ `react-virtualized` (standard)**: Too heavy for some older TVs.
- **❌ Inline Functions**: `itemData={items}` is fine, but avoid defining the render function inline if possible (hoist it).
- **❌ Complex Cards**: Keep the item component simple. Heavy CSS effects (blur, shadows) on 20 items at once will drop frames.
