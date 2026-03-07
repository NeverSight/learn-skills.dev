---
name: framer-ui-skills
description: Framer's UI design system. Use when building interfaces inspired by Framer's aesthetic - dark mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://framer.com
---

# Framer UI Skills

Opinionated constraints for building Framer-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building dark-mode interfaces
- Creating Framer-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- MUST use dark backgrounds (lightness < 20) for primary surfaces - detected lightness: 0
- MUST use `#000000` as page background (`surface-base`)
- SHOULD reduce color palette (currently 22 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #000000 | rgb(0,0,0) | Page background |
| `surface-raised` | #141415 | rgb(20,20,21) | Cards, modals, raised surfaces |
| `surface-overlay` | #F8F8F1 | rgb(248,248,241) | Overlays, tooltips, dropdowns |
| `text-primary` | #89786E | rgb(137,120,110) | Headings, body text |
| `text-2` | #D8AD9D | rgb(216,173,157) | Additional text |
| `text-tertiary` | #D1CFD0 | rgb(209,207,208) | Additional text |
| `border-default` | #494453 | rgb(73,68,83) | Subtle borders, dividers |
| `destructive` | #D8AD9D | rgb(216,173,157) | Error states, delete actions |
| `warning` | #F8F8F1 | rgb(248,248,241) | Warning states, cautions |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `93px` / `700` for primary headings
- MUST use `23px` / `500` for body text
- SHOULD reduce font weights (currently 4 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 93px | 700 | #F4F4F4 | 1 |
| `body` | Inter | 23px | 500 | #737373 | 1 |
| `body-secondary` | Inter | 22px | 700 | #DCB8B8 | 1 |
| `body-secondary` | Inter | 22px | 400 | #B2B2B1 | 1 |
| `text-20px` | Inter | 20px | 300 | #777777 | 1 |
| `text-18px` | Inter | 18px | 400 | #6D635E | 1 |
| `text-16px` | Inter | 16px | 400 | #929290 | 1 |
| `text-14px` | Inter | 14px | 400 | #949493 | 1 |
| `text-14px` | Inter | 14px | 300 | #DFDBD7 | 1 |
| `text-14px` | Inter | 14px | 300 | #2F2F31 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 62x)

**Font Sizes:** 3px, 4px, 5px, 6px, 7px, 8px, 9px, 11px, 13px, 14px, 16px, 18px, 20px, 22px, 23px, 93px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 6px, 8px, 9px
- SHOULD use 2px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 1px, 2px, 3px, 4px, 7px, 8px, 15px, 17px
- SHOULD limit border widths to: 1px, 2px
- SHOULD use 4px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 1px, 2px, 3px, 4px, 7px, 8px, 15px, 17px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 22px, 21px, 43px, 34px, 10px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 1080px
- **Main Content**: width: 1920px, height: 755px
- **Header**: height: 72px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #4D4E4C | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#5E6AD2`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#141415` background
- List items: use `#141415` background

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
