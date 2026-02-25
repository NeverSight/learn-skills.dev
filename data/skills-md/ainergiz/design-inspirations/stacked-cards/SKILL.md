---
name: stacked-cards
description: Creates horizontally fanned/cascading card stacks with proper z-index ordering and hover lift animations. Use when building album browsers, card fans, stacked previews, or any overlapping card collection.
---

# Stacked Cards Pattern

Build horizontally cascading card stacks where cards overlap in order, with hover animations that lift cards in place without breaking the cascade.

## Why This Pattern?

Stacked cards have three common bugs:

1. **Wrong stacking order** - Later cards in the array appear on top
2. **Hover breaks cascade** - Changing z-index on hover disrupts the visual order
3. **Tooltip trapped in stacking context** - Tooltips inside cards can't escape their parent's z-index

This pattern solves all three.

## Core Concept

```
First card (front)    Last card (back)
     ↓                      ↓
┌─────┐
│     │┌─────┐
│  1  ││     │┌─────┐
│     ││  2  ││     │
└─────┘│     ││  3  │
       └─────┘│     │
              └─────┘
```

- First item in array = front (highest z-index)
- Each subsequent item = behind and offset right
- Hover lifts card UP without changing z-index

## Core Implementation

```tsx
"use client";

import { useState } from "react";
import Image from "next/image";

interface Card {
  id: string;
  imageUrl: string;
  title: string;
}

function StackedCards({ cards }: { cards: Card[] }) {
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);

  const spacing = 40;      // Horizontal offset between cards
  const cardSize = 130;    // Card width
  const stackWidth = (cards.length - 1) * spacing + cardSize;

  return (
    <div className="relative h-[180px] w-full flex items-center justify-center">
      {/* CRITICAL: Reverse render order so first card renders LAST in DOM (appears on top) */}
      {[...cards].reverse().map((card, renderIndex, arr) => {
        // Convert render index back to actual card index
        const cardIndex = arr.length - 1 - renderIndex;

        // Center the stack horizontally
        const translateX = -stackWidth / 2 + cardIndex * spacing + cardSize / 2;

        // Z-index: first card (index 0) has HIGHEST z-index
        const zIndex = arr.length - cardIndex;

        // Hover: lift UP only, do NOT change z-index
        const translateY = hoveredIndex === cardIndex ? -20 : 0;

        return (
          <div
            key={card.id}
            className="absolute left-1/2 cursor-pointer transition-all duration-300 ease-out"
            style={{
              transform: `translateX(calc(-50% + ${translateX}px)) translateY(${translateY}px)`,
              zIndex,
            }}
            onMouseEnter={() => setHoveredIndex(cardIndex)}
            onMouseLeave={() => setHoveredIndex(null)}
          >
            <div className="relative w-[130px] h-[130px] rounded-2xl overflow-hidden shadow-xl">
              <Image
                src={card.imageUrl}
                alt={card.title}
                fill
                className="object-cover"
              />
            </div>
          </div>
        );
      })}

      {/* Tooltip rendered OUTSIDE the stack to escape z-index stacking context */}
      {hoveredIndex !== null && cards[hoveredIndex] && (() => {
        const translateX = -stackWidth / 2 + hoveredIndex * spacing + cardSize / 2;
        const card = cards[hoveredIndex];

        // Position: center (50%) - half card - lift - gap
        const tooltipTop = 'calc(50% - 95px)';

        return (
          <div
            className="absolute px-3 py-2 rounded-xl whitespace-nowrap shadow-lg z-50 pointer-events-none bg-white/95 backdrop-blur-md border border-zinc-200/80"
            style={{
              left: '50%',
              top: tooltipTop,
              transform: `translateX(calc(-50% + ${translateX}px)) translateY(-100%)`,
            }}
          >
            <p className="text-sm font-semibold text-zinc-900">{card.title}</p>
          </div>
        );
      })()}
    </div>
  );
}
```

## Key Elements

### 1. Reverse Render Order

```tsx
// CORRECT - First card renders LAST in DOM, appears on top
{[...cards].reverse().map((card, renderIndex, arr) => {
  const cardIndex = arr.length - 1 - renderIndex;
  // ...
})}

// WRONG - First card renders first, appears BEHIND others
{cards.map((card, index) => {
  // ...
})}
```

**Why?** DOM order determines stacking when z-index values are the same within a parent. By rendering in reverse, the first logical card is the last DOM element, appearing on top.

### 2. Z-Index Without Hover Change

```tsx
// CORRECT - Z-index based only on position, unchanged on hover
const zIndex = arr.length - cardIndex;

// WRONG - Changing z-index on hover breaks the cascade
const zIndex = hoveredIndex === cardIndex ? 20 : arr.length - cardIndex;
```

**Why?** When you change z-index on hover, the card jumps to the front, breaking the visual illusion of a physical stack. Real cards lift UP in place while staying behind cards in front.

### 3. Hover Lift Only (No Scale)

```tsx
// CORRECT - Only translateY, preserves cascade illusion
const translateY = hoveredIndex === cardIndex ? -20 : 0;

// AVOID - Scale makes card "pop out" visually
const scale = hoveredIndex === cardIndex ? 1.05 : 1;
```

### 4. Tooltip Outside Stacking Context

```tsx
// WRONG - Tooltip inside card div is trapped by parent's z-index
<div style={{ zIndex: 3 }}>
  <div className="card">...</div>
  {hovered && <div className="tooltip z-50">...</div>}  {/* z-50 doesn't help! */}
</div>

// CORRECT - Tooltip as sibling, outside all card divs
{cards.map(...)}
{hoveredIndex !== null && (
  <div className="absolute z-50" style={{ /* calculated position */ }}>
    Tooltip content
  </div>
)}
```

**Why?** A child element cannot escape its parent's stacking context. Tooltips inside cards with lower z-index will be covered by sibling cards with higher z-index.

### 5. Centering Formula

```tsx
const spacing = 40;      // Gap between card left edges
const cardSize = 130;    // Card width
const stackWidth = (cards.length - 1) * spacing + cardSize;

// For each card, calculate horizontal offset from center
const translateX = -stackWidth / 2 + cardIndex * spacing + cardSize / 2;
```

Then use `left-1/2` with `translateX(calc(-50% + ${translateX}px))` for centering.

### 6. Clear Hover State on Navigation

```tsx
const handleSelectCard = (index: number) => {
  setHoveredIndex(null);  // Clear before view change
  setSelectedCard(index);
  setView("detail");
};

const handleBack = () => {
  setHoveredIndex(null);  // Clear when returning
  setView("list");
};
```

**Why?** Without clearing, the previously hovered card stays elevated when returning to the list view.

## Tooltip Position Calculation

Position the tooltip above the lifted card:

```tsx
// Container height: 180px, card height: 130px, lift: 20px
// Card top when lifted = center - halfCard - lift = 90 - 65 - 20 = 5px

// Tooltip should be above this with gap
// Position: center (50%) - halfCard (65px) - lift (20px) - gap (10px) = 50% - 95px
const tooltipTop = 'calc(50% - 95px)';

// translateY(-100%) moves tooltip up by its own height
style={{
  top: tooltipTop,
  transform: `translateX(...) translateY(-100%)`,
}}
```

## Sizing Variations

| Context | Card Size | Spacing | Lift | Container Height |
|---------|-----------|---------|------|------------------|
| Preview | `80px` | `28px` | `-12px` | `110px` |
| Full | `130px` | `40px` | `-20px` | `180px` |

## Light/Dark Variants

| Element | Light Mode | Dark Mode |
|---------|------------|-----------|
| Card shadow | `shadow-zinc-400/50` | `shadow-black/70` |
| Tooltip bg | `bg-white/95` | `bg-zinc-800/95` |
| Tooltip border | `border-zinc-200/80` | `border-zinc-700/80` |
| Tooltip text | `text-zinc-900` | `text-zinc-100` |

## Checklist

- [ ] Render order reversed with `[...array].reverse().map()`
- [ ] Card index calculated from render index: `arr.length - 1 - renderIndex`
- [ ] Z-index decreases with card index: `arr.length - cardIndex`
- [ ] Z-index does NOT change on hover
- [ ] Hover only applies `translateY`, no scale
- [ ] Tooltip rendered OUTSIDE the card loop as sibling
- [ ] Tooltip has `pointer-events-none` to avoid hover interference
- [ ] Hover state cleared on view transitions
- [ ] Container has `relative` with fixed height
- [ ] Cards use `absolute left-1/2` with calculated translateX
