---
name: apple-ui-skills
description: Apple's UI design system. Use when building interfaces inspired by Apple's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://apple.com
---

# Apple UI Skills

Opinionated constraints for building Apple-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Apple-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#FFFFFF` as page background (`surface-base`)
- MUST use `#155BD0` for primary actions and focus states (`accent`)
- SHOULD limit color palette to 10 distinct colors
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #FFFFFF | rgb(255,255,255) | Page background |
| `surface-raised` | #0858DC | rgb(8,88,220) | Cards, modals, raised surfaces |
| `text-primary` | #808080 | rgb(128,128,128) | Headings, body text |
| `text-secondary` | #6D89B5 | rgb(109,137,181) | Secondary, muted text |
| `text-tertiary` | #90C5F1 | rgb(144,197,241) | Additional text |
| `border-default` | #B5C7D8 | rgb(181,199,216) | Subtle borders, dividers |
| `accent` | #155BD0 | rgb(21,91,208) | Primary actions, links, focus |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `51px` / `700` for primary headings
- MUST use `27px` / `500` for body text
- SHOULD reduce font weights (currently 4 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 51px | 700 | #2D2B30 | 1 |
| `text-43px` | Inter | 43px | 700 | #272729 | 1 |
| `body` | Inter | 27px | 500 | #454547 | 1 |
| `body-secondary` | Inter | 26px | 500 | #3D3C41 | 1 |
| `text-16px` | Inter | 16px | 400 | #6D89B5 | 1 |
| `text-15px` | Inter | 15px | 400 | #8EC7F2 | 1 |
| `text-14px` | Inter | 14px | 400 | #90C5F1 | 1 |
| `text-12px` | Inter | 12px | 300 | #808080 | 1 |
| `caption` | Inter | 11px | 300 | #707070 | 1 |
| `label` | Inter | 10px | 400 | #7E7E7E | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 18x)

**Font Sizes:** 9px, 10px, 11px, 12px, 14px, 15px, 16px, 26px, 27px, 43px, 51px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 2px, 4px, 13px, 34px
- SHOULD use 4px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 21px
- SHOULD use 21px+ radius for pill-shaped elements
- MUST use 1px border width consistently
- SHOULD use 21px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 21px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 46px, 50px, 36px, 47px, 32px
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Header**: height: 43px
- **Main Content**: width: 1920px, height: 694px
- **Main Content**: width: 1920px, height: 695px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #6D89B5 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#155BD0`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#0858DC` background
- List items: use `#0858DC` background

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
