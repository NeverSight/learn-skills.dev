---
name: planetscale-ui-skills
description: Planetscale's UI design system. Use when building interfaces inspired by Planetscale's aesthetic - dark mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://planetscale.com
---

# Planetscale UI Skills

Opinionated constraints for building Planetscale-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building dark-mode interfaces
- Creating Planetscale-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- MUST use dark backgrounds (lightness < 20) for primary surfaces - detected lightness: 0
- MUST use `#000000` as page background (`surface-base`)
- MUST use `#7967D3` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 23 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #000000 | rgb(0,0,0) | Page background |
| `surface-raised` | #F8F8F9 | rgb(248,248,249) | Cards, modals, raised surfaces |
| `surface-overlay` | #EC4011 | rgb(236,64,17) | Overlays, tooltips, dropdowns |
| `text-primary` | #202020 | rgb(32,32,32) | Headings, body text |
| `text-secondary` | #787878 | rgb(120,120,120) | Secondary, muted text |
| `text-tertiary` | #54565C | rgb(84,86,92) | Additional text |
| `border-default` | #D44927 | rgb(212,73,39) | Subtle borders, dividers |
| `destructive` | #EC4011 | rgb(236,64,17) | Error states, delete actions |
| `success` | #41D731 | rgb(65,215,49) | Success states, confirmations |
| `accent` | #7967D3 | rgb(121,103,211) | Primary actions, links, focus |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `51px` / `700` for primary headings
- MUST use `17px` / `400` for body text
- SHOULD reduce font weights (currently 5 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 51px | 700 | #DF5C2E | 1 |
| `text-44px` | Inter | 44px | 700 | #36F91F | 1 |
| `text-40px` | Inter | 40px | extra_bold | #202020 | 1 |
| `text-39px` | Inter | 39px | extra_bold | #1A1A1A | 1 |
| `text-38px` | Inter | 38px | 700 | #1E1E1E | 1 |
| `text-35px` | Inter | 35px | extra_bold | #1D1D1D | 1 |
| `text-34px` | Inter | 34px | 700 | #1A1A1A | 1 |
| `text-31px` | Inter | 31px | 700 | #141414 | 1 |
| `text-30px` | Inter | 30px | 700 | #1A1A1A | 1 |
| `text-30px` | Inter | 30px | 400 | #D76B60 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 55x)

**Font Sizes:** 11px, 12px, 13px, 14px, 15px, 16px, 17px, 18px, 21px, 22px, 23px, 24px, 25px, 26px, 29px, 30px, 31px, 34px, 35px, 38px, 39px, 40px, 44px, 51px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 3px, 4px, 5px, 6px, 7px, 25px, 28px, 32px
- SHOULD use 38px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use 1px border width consistently
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 220px, 221px, 2px, 30px, 1px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 1041px
- **Main Content**: width: 1114px, height: 664px
- **Main Content**: width: 1104px, height: 667px
- **Header**: height: 39px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #F0B095 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#7967D3`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#F8F8F9` background
- List items: use `#F8F8F9` background

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
