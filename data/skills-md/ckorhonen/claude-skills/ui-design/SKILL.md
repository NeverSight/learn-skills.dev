---
name: ui-design
description: Opinionated constraints for building better interfaces with agents. Use when building UI components, implementing animations, designing layouts, reviewing frontend accessibility, or working with Tailwind CSS, motion/react, or accessible primitives like Radix/Base UI.
---

# UI Design

Opinionated constraints for building better interfaces with agents.

## When to Use

- Building UI components with Tailwind CSS
- Implementing animations or transitions
- Adding interactive elements with keyboard/focus behavior
- Reviewing frontend code for accessibility
- Designing layouts with proper z-index and spacing
- Working with loading states, error handling, or empty states

## Stack

| Requirement | Rule |
|-------------|------|
| Tailwind CSS | MUST use defaults (spacing, radius, shadows) before custom values |
| Animation library | MUST use `motion/react` (formerly `framer-motion`) for JS animation |
| CSS animation | SHOULD use `tw-animate-css` for entrance and micro-animations |
| Class logic | MUST use `cn` utility (`clsx` + `tailwind-merge`) |

## Components

| Requirement | Rule |
|-------------|------|
| Interactive primitives | MUST use accessible primitives (`Base UI`, `React Aria`, `Radix`) for keyboard/focus behavior |
| Existing components | MUST use project's existing primitives first |
| Consistency | NEVER mix primitive systems within the same interaction surface |
| New primitives | SHOULD prefer [`Base UI`](https://base-ui.com/react/components) if compatible with stack |
| Icon buttons | MUST add `aria-label` to icon-only buttons |
| Custom behavior | NEVER rebuild keyboard or focus behavior by hand unless explicitly requested |

## Interaction

| Requirement | Rule |
|-------------|------|
| Destructive actions | MUST use `AlertDialog` for destructive or irreversible actions |
| Loading states | SHOULD use structural skeletons |
| Viewport height | NEVER use `h-screen`, use `h-dvh` |
| Fixed elements | MUST respect `safe-area-inset` |
| Error display | MUST show errors next to where the action happens |
| Input behavior | NEVER block paste in `input` or `textarea` elements |

## Animation

| Requirement | Rule |
|-------------|------|
| Default | NEVER add animation unless explicitly requested |
| Compositor props | MUST animate only `transform`, `opacity` |
| Layout props | NEVER animate `width`, `height`, `top`, `left`, `margin`, `padding` |
| Paint props | SHOULD avoid `background`, `color` except for small, local UI (text, icons) |
| Entrance easing | SHOULD use `ease-out` on entrance |
| Feedback timing | NEVER exceed `200ms` for interaction feedback |
| Looping | MUST pause looping animations when off-screen |
| Accessibility | MUST respect `prefers-reduced-motion` |
| Custom easing | NEVER introduce custom easing curves unless explicitly requested |
| Large surfaces | SHOULD avoid animating large images or full-screen surfaces |

## Typography

| Requirement | Rule |
|-------------|------|
| Headings | MUST use `text-balance` |
| Body text | MUST use `text-pretty` for paragraphs |
| Data | MUST use `tabular-nums` |
| Dense UI | SHOULD use `truncate` or `line-clamp` |
| Letter spacing | NEVER modify `letter-spacing` (`tracking-`) unless explicitly requested |

## Layout

| Requirement | Rule |
|-------------|------|
| Z-index | MUST use a fixed scale (no arbitrary `z-x`) |
| Square elements | SHOULD use `size-x` instead of `w-x` + `h-x` |

## Performance

| Requirement | Rule |
|-------------|------|
| Blur effects | NEVER animate large `blur()` or `backdrop-filter` surfaces |
| Will-change | NEVER apply `will-change` outside an active animation |
| useEffect | NEVER use for anything expressible as render logic |

## Design

| Requirement | Rule |
|-------------|------|
| Gradients | NEVER use unless explicitly requested |
| Purple/multicolor gradients | NEVER use |
| Glow effects | NEVER use as primary affordances |
| Shadows | SHOULD use Tailwind CSS default scale unless explicitly requested |
| Empty states | MUST give one clear next action |
| Accent colors | SHOULD limit to one per view |
| Color tokens | SHOULD use existing theme or Tailwind CSS tokens before introducing new ones |

## Quick Reference

### Allowed Animation Properties
```
transform, opacity
```

### Forbidden Animation Properties
```
width, height, top, left, margin, padding, blur(), backdrop-filter
```

### Required Accessibility Patterns
```tsx
// Icon button - always add aria-label
<button aria-label="Close dialog">
  <XIcon />
</button>

// Respect reduced motion
@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; }
}
```

### Class Utility Pattern
```tsx
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```
