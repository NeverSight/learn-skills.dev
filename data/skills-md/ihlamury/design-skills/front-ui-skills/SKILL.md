---
name: front-ui-skills
description: Front's UI design system. Use when building interfaces inspired by Front's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://front.com
---

# Front UI Skills

Opinionated constraints for building Front-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Front-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#FFFFFF` as page background (`surface-base`)
- MUST use `#C8CC51` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 30 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #FFFFFF | rgb(255,255,255) | Page background |
| `surface-raised` | #240733 | rgb(36,7,51) | Cards, modals, raised surfaces |
| `surface-overlay` | #503AF3 | rgb(80,58,243) | Overlays, tooltips, dropdowns |
| `text-primary` | #978BF0 | rgb(151,139,240) | Headings, body text |
| `text-secondary` | #D1D1D1 | rgb(209,209,209) | Secondary, muted text |
| `text-tertiary` | #8F8F8F | rgb(143,143,143) | Additional text |
| `border-default` | #DDD4F5 | rgb(221,212,245) | Subtle borders, dividers |
| `accent` | #C8CC51 | rgb(200,204,81) | Primary actions, links, focus |
| `warning` | #B49F65 | rgb(180,159,101) | Warning states, cautions |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `58px` / `700` for primary headings
- MUST use `26px` / `700` for body text
- SHOULD reduce font weights (currently 4 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 58px | 700 | #E7E1E8 | 1 |
| `body` | Inter | 26px | 700 | #EBE5EC | 1 |
| `text-17px` | Inter | 17px | 400 | #AC99B3 | 1 |
| `text-16px` | Inter | 16px | 400 | #46541B | 1 |
| `text-15px` | Inter | 15px | 400 | #977FAF | 1 |
| `text-15px` | Inter | 15px | 400 | #594B5F | 1 |
| `text-15px` | Inter | 15px | 400 | #BCABC2 | 1 |
| `text-15px` | Inter | 15px | 400 | #C8B8CD | 1 |
| `text-14px` | Inter | 14px | 400 | #977FB0 | 1 |
| `text-14px` | Inter | 14px | 400 | #9880B0 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 79x)

**Font Sizes:** 5px, 6px, 7px, 8px, 9px, 10px, 11px, 12px, 13px, 14px, 15px, 16px, 17px, 26px, 58px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 6px, 8px, 14px
- SHOULD use 2px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 1px, 2px, 3px, 5px, 6px, 18px, 20px
- SHOULD use 20px+ radius for pill-shaped elements
- SHOULD limit border widths to: 1px, 2px, 5px
- SHOULD use 3px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 1px, 2px, 3px, 5px, 6px, 18px, 20px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 10px, 11px, 6px, 8px, 20px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 639px
- **Main Content**: width: 1267px, height: 569px
- **Main Content**: width: 1255px, height: 569px
- **Header**: height: 75px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #978BF0 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#C8CC51`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#240733` background
- List items: use `#240733` background

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
