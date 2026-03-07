---
name: robinhood-ui-skills
description: Robinhood's UI design system. Use when building interfaces inspired by Robinhood's aesthetic - dark mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://robinhood.com
---

# Robinhood UI Skills

Opinionated constraints for building Robinhood-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building dark-mode interfaces
- Creating Robinhood-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- MUST use dark backgrounds (lightness < 20) for primary surfaces - detected lightness: 0
- MUST use `#000000` as page background (`surface-base`)
- MUST use `#B7DF2F` for primary actions and focus states (`accent`)
- SHOULD limit color palette to 10 distinct colors
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #000000 | rgb(0,0,0) | Page background |
| `surface-raised` | #C3FE09 | rgb(195,254,9) | Cards, modals, raised surfaces |
| `text-primary` | #A0A0A0 | rgb(160,160,160) | Headings, body text |
| `text-2` | #ECECEC | rgb(236,236,236) | Additional text |
| `text-secondary` | #497009 | rgb(73,112,9) | Secondary, muted text |
| `border-default` | #B7DF2F | rgb(183,223,47) | Subtle borders, dividers |
| `accent` | #B7DF2F | rgb(183,223,47) | Primary actions, links, focus |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `85px` / `700` for primary headings
- MUST use `14px` / `400` for body text
- SHOULD reduce font weights (currently 4 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 85px | 700 | #ECECEC | 1 |
| `text-18px` | Inter | 18px | 500 | #D9D9D9 | 1 |
| `text-17px` | Inter | 17px | 400 | #A0A0A0 | 1 |
| `body` | Inter | 14px | 400 | #A1A1A1 | 2 |
| `body-secondary` | Inter | 14px | 400 | #497009 | 1 |
| `body-secondary` | Inter | 14px | 400 | #899C47 | 1 |
| `body-secondary` | Inter | 14px | 400 | #A0A0A0 | 1 |
| `caption` | Inter | 11px | 400 | #A2A2A2 | 2 |
| `label` | Inter | 11px | 300 | #909090 | 1 |
| `label` | Inter | 11px | 400 | #A1A1A1 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 13x)

**Font Sizes:** 11px, 14px, 17px, 18px, 85px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 4px, 5px, 6px, 12px, 13px, 14px, 17px, 19px
- SHOULD use 4px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 19px, 21px
- SHOULD use 21px+ radius for pill-shaped elements
- SHOULD limit border widths to: 1px, 2px
- SHOULD use 21px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 19px, 21px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 12px, 74px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 1016px
- **Header**: height: 64px
- **Main Content**: width: 1920px, height: 608px
- **Main Content**: width: 1920px, height: 1001px
- **Header**: height: 63px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #497009 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#B7DF2F`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#C3FE09` background
- List items: use `#C3FE09` background

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
