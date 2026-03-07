---
name: pinterest-ui-skills
description: Pinterest's UI design system. Use when building interfaces inspired by Pinterest's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://pinterest.com
---

# Pinterest UI Skills

Opinionated constraints for building Pinterest-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Pinterest-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#FFFFFF` as page background (`surface-base`)
- SHOULD reduce color palette (currently 11 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #FFFFFF | rgb(255,255,255) | Page background |
| `surface-raised` | #DC001A | rgb(220,0,26) | Cards, modals, raised surfaces |
| `surface-overlay` | #DDDED8 | rgb(221,222,216) | Overlays, tooltips, dropdowns |
| `text-primary` | #3B3B3A | rgb(59,59,58) | Headings, body text |
| `text-secondary` | #ED93A1 | rgb(237,147,161) | Secondary, muted text |
| `text-tertiary` | #EB5B3E | rgb(235,91,62) | Additional text |
| `border-default` | #BC1C31 | rgb(188,28,49) | Subtle borders, dividers |
| `destructive` | #EB5B3E | rgb(235,91,62) | Error states, delete actions |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `49px` / `700` for primary headings
- MUST use `19px` / `400` for body text
- MUST limit font weights to: bold, semi_bold, regular
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 49px | 700 | #383538 | 1 |
| `heading-2` | Inter | 46px | 700 | #EB5B3E | 1 |
| `text-37px` | Inter | 37px | 700 | #111111 | 1 |
| `body` | Inter | 19px | 400 | #3B3B3A | 1 |
| `text-16px` | Inter | 16px | semi_bold | #D03A52 | 1 |
| `text-14px` | Inter | 14px | 400 | #484848 | 1 |
| `text-14px` | Inter | 14px | 400 | #40413C | 1 |
| `text-14px` | Inter | 14px | 400 | #F19AA6 | 1 |
| `text-14px` | Inter | 14px | 400 | #3D3D3D | 1 |
| `text-14px` | Inter | 14px | 400 | #353535 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 15x)

**Font Sizes:** 11px, 12px, 14px, 16px, 19px, 37px, 46px, 49px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 3px, 4px, 5px, 51px, 71px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 13px, 15px
- MUST use 1px border width consistently
- SHOULD use 15px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 13px, 15px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 10px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 759px
- **Main Content**: width: 1920px, height: 690px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #ED93A1 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#5E6AD2`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#DC001A` background
- List items: use `#DC001A` background

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
