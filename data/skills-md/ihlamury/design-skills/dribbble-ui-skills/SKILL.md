---
name: dribbble-ui-skills
description: Dribbble's UI design system. Use when building interfaces inspired by Dribbble's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://dribbble.com
---

# Dribbble UI Skills

Opinionated constraints for building Dribbble-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Dribbble-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#000000` as page background (`surface-base`)
- MUST use `#F2B5D7` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 40 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #000000 | rgb(0,0,0) | Page background |
| `surface-raised` | #FEFEFD | rgb(254,254,253) | Cards, modals, raised surfaces |
| `surface-overlay` | #1B1B1C | rgb(27,27,28) | Overlays, tooltips, dropdowns |
| `text-primary` | #5C5B60 | rgb(92,91,96) | Headings, body text |
| `text-secondary` | #797886 | rgb(121,120,134) | Secondary, muted text |
| `text-tertiary` | #9E9EA7 | rgb(158,158,167) | Additional text |
| `border-default` | #0C110F | rgb(12,17,15) | Subtle borders, dividers |
| `destructive` | #ECC6B6 | rgb(236,198,182) | Error states, delete actions |
| `accent` | #F2B5D7 | rgb(242,181,215) | Primary actions, links, focus |
| `warning` | #FEFEFD | rgb(254,254,253) | Warning states, cautions |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `42px` / `700` for primary headings
- MUST use `14px` / `300` for body text
- SHOULD reduce font weights (currently 6 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 42px | 700 | #1D1C27 | 1 |
| `text-37px` | Inter | 37px | 700 | #232323 | 1 |
| `text-34px` | Inter | 34px | extra_bold | #282342 | 1 |
| `text-27px` | Inter | 27px | semi_bold | #CCC9D8 | 1 |
| `text-19px` | Inter | 19px | 400 | #B7B7B7 | 1 |
| `text-17px` | Inter | 17px | 400 | #9E9EA7 | 1 |
| `text-16px` | Inter | 16px | 400 | #626262 | 1 |
| `body` | Inter | 14px | 300 | #46607F | 1 |
| `body-secondary` | Inter | 14px | 400 | #77767D | 1 |
| `body-secondary` | Inter | 14px | 400 | #616066 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 80x)

**Font Sizes:** 3px, 4px, 5px, 6px, 7px, 8px, 9px, 10px, 11px, 12px, 13px, 14px, 16px, 17px, 19px, 27px, 34px, 37px, 42px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 6px, 7px, 8px
- SHOULD use 4px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 1px, 2px, 3px, 4px, 5px, 6px, 7px, 9px, 14px, 15px, 16px, 19px, 22px, 23px
- SHOULD use 22px+ radius for pill-shaped elements
- SHOULD limit border widths to: 1px, 5px
- SHOULD use 14px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 1px, 2px, 3px, 4px, 5px, 6px, 7px, 9px, 14px, 15px, 16px, 19px, 22px, 23px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 8px, 13px, 18px, 9px, 24px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 1013px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #5C5B60 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#F2B5D7`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#FEFEFD` background
- List items: use `#FEFEFD` background

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
