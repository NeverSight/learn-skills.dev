---
name: plaid-ui-skills
description: Plaid's UI design system. Use when building interfaces inspired by Plaid's aesthetic - dark mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://plaid.com
---

# Plaid UI Skills

Opinionated constraints for building Plaid-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building dark-mode interfaces
- Creating Plaid-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- MUST use dark backgrounds (lightness < 20) for primary surfaces - detected lightness: 11
- MUST use `#1B1B1B` as page background (`surface-base`)
- MUST use `#7FB4D5` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 17 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #1B1B1B | rgb(27,27,27) | Page background |
| `surface-raised` | #1376C1 | rgb(19,118,193) | Cards, modals, raised surfaces |
| `surface-overlay` | #A6C5D9 | rgb(166,197,217) | Overlays, tooltips, dropdowns |
| `text-primary` | #40645C | rgb(64,100,92) | Headings, body text |
| `text-secondary` | #2D4B49 | rgb(45,75,73) | Secondary, muted text |
| `text-tertiary` | #9E9E9F | rgb(158,158,159) | Additional text |
| `border-default` | #373D3E | rgb(55,61,62) | Subtle borders, dividers |
| `accent` | #7FB4D5 | rgb(127,180,213) | Primary actions, links, focus |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `72px` / `700` for primary headings
- MUST use `23px` / `400` for body text
- SHOULD reduce font weights (currently 4 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 72px | 700 | #7CD5B9 | 1 |
| `body` | Inter | 23px | 400 | #BDE4F1 | 1 |
| `text-19px` | Inter | 19px | 500 | #2D4B49 | 1 |
| `text-19px` | Inter | 19px | 500 | #93CAE6 | 1 |
| `text-19px` | Inter | 19px | 400 | #D1D1D1 | 1 |
| `text-17px` | Inter | 17px | 400 | #7FB4D5 | 1 |
| `text-16px` | Inter | 16px | 500 | #83BEE0 | 1 |
| `text-15px` | Inter | 15px | 400 | #35615B | 1 |
| `text-15px` | Inter | 15px | 400 | #374D5A | 1 |
| `text-14px` | Inter | 14px | 400 | #364854 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 20x)

**Font Sizes:** 7px, 11px, 12px, 13px, 14px, 15px, 16px, 17px, 19px, 23px, 72px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 3px, 4px, 5px, 6px, 11px, 41px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 18px, 19px, 26px, 32px
- SHOULD use 26px+ radius for pill-shaped elements
- SHOULD limit border widths to: 1px, 2px, 3px
- SHOULD use 26px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 18px, 19px, 26px, 32px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 5px, 6px, 24px, 77px, 210px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 1080px
- **Main Content**: width: 1920px, height: 874px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #D1D1D1 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#7FB4D5`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#1376C1` background
- List items: use `#1376C1` background

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
