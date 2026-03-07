---
name: loops-ui-skills
description: Loops's UI design system. Use when building interfaces inspired by Loops's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://loops.so
---

# Loops UI Skills

Opinionated constraints for building Loops-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Loops-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#FFFFFF` as page background (`surface-base`)
- SHOULD reduce color palette (currently 17 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #FFFFFF | rgb(255,255,255) | Page background |
| `surface-raised` | #ECECEC | rgb(236,236,236) | Cards, modals, raised surfaces |
| `text-primary` | #CCCCCE | rgb(204,204,206) | Headings, body text |
| `text-secondary` | #AAAAAE | rgb(170,170,174) | Secondary, muted text |
| `text-tertiary` | #85B1A4 | rgb(133,177,164) | Additional text |
| `border-default` | #F4F5F6 | rgb(244,245,246) | Subtle borders, dividers |
| `destructive` | #D77B5F | rgb(215,123,95) | Error states, delete actions |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `39px` / `700` for primary headings
- MUST use `22px` / `700` for body text
- SHOULD reduce font weights (currently 4 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 39px | 700 | #2B2A29 | 1 |
| `body` | Inter | 22px | 700 | #423029 | 1 |
| `text-18px` | Inter | 18px | 400 | #626262 | 1 |
| `text-17px` | Inter | 17px | 400 | #93908E | 1 |
| `text-17px` | Inter | 17px | 500 | #525252 | 1 |
| `text-16px` | Inter | 16px | 500 | #525252 | 1 |
| `text-15px` | Inter | 15px | 500 | #544542 | 1 |
| `text-15px` | Inter | 15px | 400 | #6D6D6D | 1 |
| `text-14px` | Inter | 14px | 400 | #CCCCCE | 1 |
| `text-14px` | Inter | 14px | 300 | #CCCCCE | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 86x)

**Font Sizes:** 7px, 8px, 9px, 10px, 11px, 12px, 13px, 14px, 15px, 16px, 17px, 18px, 22px, 39px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 6px, 8px, 9px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 0px, 1px, 2px, 3px, 4px, 6px, 7px, 9px, 10px, 26px
- SHOULD use 26px+ radius for pill-shaped elements
- MUST use 1px border width consistently
- SHOULD use 1px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 0px, 1px, 2px, 3px, 4px, 6px, 7px, 9px, 10px, 26px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 13px, 27px, 50px, 12px, 7px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 1030px
- **Main Content**: width: 994px, height: 568px
- **Header**: height: 52px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #AAAAAE | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#5E6AD2`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#ECECEC` background
- List items: use `#ECECEC` background

### Disabled

- MUST use `opacity: 0.5`
- MUST use `cursor: not-allowed`

## Interaction

- MUST use an `AlertDialog` for destructive or irreversible actions
- SHOULD use structural skeletons for loading states
- MUST show errors next to where the action happens
- NEVER block paste in `input` or `textarea` elements
- MUST add an `aria-label` to icon-only buttons

## Animation

- NEVER add animation unless it is explicitly requested
- MUST animate only compositor props (`transform`, `opacity`)
- NEVER animate layout properties (`width`, `height`, `top`, `left`, `margin`, `padding`)
- SHOULD use `ease-out` on entrance animations
- NEVER exceed `200ms` for interaction feedback
- SHOULD respect `prefers-reduced-motion`

## Performance

- NEVER animate large `blur()` or `backdrop-filter` surfaces
- NEVER apply `will-change` outside an active animation
- NEVER use `useEffect` for anything that can be expressed as render logic
