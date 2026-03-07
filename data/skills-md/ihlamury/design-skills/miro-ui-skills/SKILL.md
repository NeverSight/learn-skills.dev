---
name: miro-ui-skills
description: Miro's UI design system. Use when building interfaces inspired by Miro's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://miro.com
---

# Miro UI Skills

Opinionated constraints for building Miro-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Miro-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#FEFEFE` as page background (`surface-base`)
- MUST use `#C2BBFE` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 39 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #FEFEFE | rgb(254,254,254) | Page background |
| `surface-raised` | #000000 | rgb(0,0,0) | Cards, modals, raised surfaces |
| `surface-overlay` | #EBE4F6 | rgb(235,228,246) | Overlays, tooltips, dropdowns |
| `text-primary` | #4D4E4F | rgb(77,78,79) | Headings, body text |
| `text-secondary` | #4A68AA | rgb(74,104,170) | Secondary, muted text |
| `text-tertiary` | #666666 | rgb(102,102,102) | Additional text |
| `border-default` | #F1F1F2 | rgb(241,241,242) | Subtle borders, dividers |
| `accent` | #C2BBFE | rgb(194,187,254) | Primary actions, links, focus |
| `warning` | #4F4826 | rgb(79,72,38) | Warning states, cautions |
| `destructive` | #E5802A | rgb(229,128,42) | Error states, delete actions |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `47px` / `700` for primary headings
- MUST use `7px` / `400` for body text
- SHOULD reduce font weights (currently 5 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 47px | 700 | #373737 | 1 |
| `text-37px` | Inter | 37px | 700 | #383839 | 1 |
| `text-23px` | Inter | 23px | semi_bold | #292929 | 1 |
| `text-22px` | Inter | 22px | 400 | #717378 | 1 |
| `text-17px` | Inter | 17px | 400 | #B0B0B2 | 1 |
| `text-16px` | Inter | 16px | 400 | #4A68AA | 1 |
| `text-16px` | Inter | 16px | 400 | #5A5A5A | 1 |
| `text-15px` | Inter | 15px | 400 | #4D4E4F | 1 |
| `text-15px` | Inter | 15px | 400 | #B6C3F8 | 1 |
| `text-14px` | Inter | 14px | 400 | #525252 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 74x)

**Font Sizes:** 2px, 3px, 4px, 5px, 6px, 7px, 8px, 10px, 11px, 12px, 13px, 14px, 15px, 16px, 17px, 22px, 23px, 37px, 47px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 6px, 7px, 8px
- SHOULD use 2px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 1px, 3px, 4px, 5px, 6px, 7px, 9px, 15px, 16px, 17px, 18px
- SHOULD limit border widths to: 1px, 2px
- SHOULD use 1px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 1px, 3px, 4px, 5px, 6px, 7px, 9px, 15px, 16px, 17px, 18px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 9px, 4px, 10px, 12px, 7px
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Header**: height: 79px
- **Main Content**: width: 1920px, height: 929px
- **Main Content**: width: 1920px, height: 1003px
- **Header**: height: 80px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #4A68AA | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#C2BBFE`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#000000` background
- List items: use `#000000` background

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
