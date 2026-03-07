---
name: monzo-ui-skills
description: Monzo's UI design system. Use when building interfaces inspired by Monzo's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://monzo.com
---

# Monzo UI Skills

Opinionated constraints for building Monzo-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Monzo-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#FFFFFF` as page background (`surface-base`)
- SHOULD reduce color palette (currently 15 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #FFFFFF | rgb(255,255,255) | Page background |
| `surface-raised` | #C1C5C8 | rgb(193,197,200) | Cards, modals, raised surfaces |
| `surface-overlay` | #DEDEDE | rgb(222,222,222) | Overlays, tooltips, dropdowns |
| `text-primary` | #606366 | rgb(96,99,102) | Headings, body text |
| `text-2` | #494D50 | rgb(73,77,80) | Additional text |
| `text-secondary` | #BEC4C7 | rgb(190,196,199) | Secondary, muted text |
| `border-default` | #8A8D8F | rgb(138,141,143) | Subtle borders, dividers |
| `destructive` | #ED4948 | rgb(237,73,72) | Error states, delete actions |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `48px` / `700` for primary headings
- MUST use `21px` / `extra_bold` for body text
- SHOULD reduce font weights (currently 5 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 48px | 700 | #F0F1EE | 1 |
| `body` | Inter | 21px | extra_bold | #ED4948 | 1 |
| `body-secondary` | Inter | 19px | 300 | #723C7E | 1 |
| `text-17px` | Inter | 17px | semi_bold | #373737 | 1 |
| `text-16px` | Inter | 16px | 400 | #9EA0A2 | 1 |
| `text-15px` | Inter | 15px | 400 | #606366 | 1 |
| `text-15px` | Inter | 15px | 400 | #494D50 | 1 |
| `text-15px` | Inter | 15px | 400 | #BEC4C7 | 1 |
| `text-15px` | Inter | 15px | 400 | #C4C6BC | 1 |
| `text-13px` | Inter | 13px | 400 | #4D4D4D | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 16x)

**Font Sizes:** 8px, 9px, 11px, 12px, 13px, 15px, 16px, 17px, 19px, 21px, 48px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 2px, 4px, 5px, 6px, 9px, 11px, 20px, 54px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 3px, 4px, 6px, 16px, 25px
- SHOULD use 25px+ radius for pill-shaped elements
- MUST use 1px border width consistently
- SHOULD use 16px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 3px, 4px, 6px, 16px, 25px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 12px, 116px, 43px, 60px, 299px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1470px, height: 870px
- **Main Content**: width: 1455px, height: 762px
- **Header**: height: 82px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #494D50 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#5E6AD2`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#C1C5C8` background
- List items: use `#C1C5C8` background

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
