---
name: expandable-card
description: Creates expandable/collapsible cards using CSS grid-rows animation with smooth transitions. Use when building accordions, expandable panels, collapsible sections, or show/hide card content.
---

# Expandable Card Pattern

Build smooth expand/collapse animations using CSS grid-rows, avoiding height:auto animation issues.

## Why grid-rows?

Traditional height animation requires explicit pixel values. The `grid-rows` technique allows smooth animation to/from `auto` height:

- `grid-rows-[0fr]` + `overflow-hidden` = collapsed (0 height)
- `grid-rows-[1fr]` = expanded (natural height)

## Core Implementation

```tsx
"use client";

import { useState } from "react";
import { ChevronDown } from "lucide-react";

function ExpandableCard() {
  const [expanded, setExpanded] = useState(true);

  return (
    <div className="rounded-xl border overflow-hidden transition-all duration-300">
      {/* Header - clickable toggle */}
      <div
        className="flex items-center justify-between px-4 py-3 cursor-pointer hover:bg-zinc-50 transition-colors"
        onClick={() => setExpanded(!expanded)}
      >
        <span className="font-medium">Card Title</span>
        <ChevronDown
          className={`w-5 h-5 transition-transform duration-200 ${
            expanded ? "rotate-180" : ""
          }`}
        />
      </div>

      {/* Content - animated container */}
      <div
        className={`grid transition-all duration-300 ease-in-out ${
          expanded ? "grid-rows-[1fr]" : "grid-rows-[0fr]"
        }`}
      >
        <div className="overflow-hidden">
          <div className="px-4 py-4 border-t">
            {/* Your content here */}
            <p>Expandable content goes here.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
```

## Key Elements

### 1. State Management
```tsx
const [expanded, setExpanded] = useState(true); // Start expanded
// or
const [expanded, setExpanded] = useState(false); // Start collapsed
```

### 2. Header Click Handler
```tsx
<div
  className="cursor-pointer hover:bg-zinc-50 transition-colors"
  onClick={() => setExpanded(!expanded)}
>
```

### 3. ChevronDown Rotation
```tsx
<ChevronDown
  className={`transition-transform duration-200 ${
    expanded ? "rotate-180" : ""
  }`}
/>
```

### 4. Grid Container Animation
```tsx
<div
  className={`grid transition-all duration-300 ease-in-out ${
    expanded ? "grid-rows-[1fr]" : "grid-rows-[0fr]"
  }`}
>
  <div className="overflow-hidden">
    {/* Content wrapper - REQUIRED for animation */}
  </div>
</div>
```

## Timing Recommendations

| Duration | Use Case |
|----------|----------|
| `duration-150` | Small cards, quick feedback |
| `duration-200` | Chevron rotation |
| `duration-300` | Content expansion (recommended) |
| `duration-500` | Large content areas |

## Shadow Transition (Optional)

Add shadow that changes with state:

```tsx
<div
  className={`rounded-xl border overflow-hidden transition-all duration-300 ${
    expanded ? "shadow-lg" : "shadow-sm hover:shadow-md"
  }`}
>
```

## Accessibility Considerations

```tsx
<div
  role="button"
  tabIndex={0}
  aria-expanded={expanded}
  onClick={() => setExpanded(!expanded)}
  onKeyDown={(e) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      setExpanded(!expanded);
    }
  }}
>
```

## Common Variations

### Multiple Cards (Accordion)
```tsx
const [expandedId, setExpandedId] = useState<string | null>("first");

// Toggle logic
onClick={() => setExpandedId(expandedId === id ? null : id)}
```

### Nested Content Protection
Prevent clicks on interactive content from toggling:
```tsx
<a
  href="..."
  onClick={(e) => e.stopPropagation()}
>
```

**Important**: Always add `stopPropagation` to:
- Links (`<a>`)
- Buttons that perform actions other than toggling
- Form inputs
- Any interactive element that shouldn't trigger expand/collapse

```tsx
// Full example with multiple interactive elements
<div className="overflow-hidden">
  <div className="px-4 py-4 border-t">
    <a
      href="https://example.com"
      onClick={(e) => e.stopPropagation()}
      className="text-blue-500 hover:underline"
    >
      External link
    </a>

    <button
      onClick={(e) => {
        e.stopPropagation();
        // Handle button action
      }}
    >
      Action Button
    </button>
  </div>
</div>
```

## Checklist

- [ ] `overflow-hidden` on inner wrapper (required for animation)
- [ ] `transition-all` on grid container
- [ ] ChevronDown has `transition-transform`
- [ ] Header has `cursor-pointer` and hover state
- [ ] Timing consistent (300ms recommended)
