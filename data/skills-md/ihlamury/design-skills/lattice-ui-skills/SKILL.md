---
name: lattice-ui-skills
description: Lattice's UI design system. Use when building interfaces inspired by Lattice's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://lattice.com
---

# Lattice UI Skills

Opinionated constraints for building Lattice-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Lattice-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#FEFDFC` as page background (`surface-base`)
- MUST use `#26B177` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 37 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #FEFDFC | rgb(254,253,252) | Page background |
| `surface-raised` | #DDFCDA | rgb(221,252,218) | Cards, modals, raised surfaces |
| `surface-overlay` | #EDFAF3 | rgb(237,250,243) | Overlays, tooltips, dropdowns |
| `text-primary` | #6B6F6E | rgb(107,111,110) | Headings, body text |
| `text-secondary` | #969C9B | rgb(150,156,155) | Secondary, muted text |
| `text-tertiary` | #5E9892 | rgb(94,152,146) | Additional text |
| `border-default` | #F5F4F2 | rgb(245,244,242) | Subtle borders, dividers |
| `accent` | #26B177 | rgb(38,177,119) | Primary actions, links, focus |
| `success` | #EDFAF3 | rgb(237,250,243) | Success states, confirmations |
| `warning` | #FEFDFC | rgb(254,253,252) | Warning states, cautions |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `71px` / `700` for primary headings
- MUST use `40px` / `700` for body text
- SHOULD reduce font weights (currently 6 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 71px | 700 | #122424 | 1 |
| `heading-2` | Inter | 71px | 700 | #205D42 | 1 |
| `text-57px` | Inter | 57px | 700 | #144F36 | 1 |
| `body` | Inter | 40px | 700 | #162625 | 1 |
| `text-21px` | Inter | 21px | 500 | #929896 | 1 |
| `text-20px` | Inter | 20px | 400 | #3B4342 | 1 |
| `text-20px` | Inter | 20px | 400 | #919593 | 1 |
| `text-19px` | Inter | 19px | 500 | #949A98 | 1 |
| `text-19px` | Inter | 19px | 500 | #9AA09F | 1 |
| `text-17px` | Inter | 17px | 400 | #626968 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 76x)

**Font Sizes:** 3px, 4px, 5px, 6px, 7px, 8px, 9px, 10px, 11px, 12px, 13px, 14px, 15px, 16px, 17px, 19px, 20px, 21px, 40px, 57px, 71px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 6px, 7px, 8px
- SHOULD use 1px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 0px, 1px, 2px, 3px, 4px, 5px, 6px, 7px, 8px, 9px, 10px, 12px, 13px, 16px, 18px, 19px, 56px, 63px
- SHOULD use 56px+ radius for pill-shaped elements
- SHOULD limit border widths to: 1px, 2px, 3px, 4px
- SHOULD use 4px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 0px, 1px, 2px, 3px, 4px, 5px, 6px, 7px, 8px, 9px, 10px, 12px, 13px, 16px, 18px, 19px, 56px, 63px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 6px, 15px, 7px, 14px, 474px
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 918px
- **Header**: height: 47px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | - | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#26B177`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#DDFCDA` background
- List items: use `#DDFCDA` background

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
