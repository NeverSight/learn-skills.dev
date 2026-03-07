---
name: gumroad-ui-skills
description: Gumroad's UI design system. Use when building interfaces inspired by Gumroad's aesthetic - dark mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://gumroad.com
---

# Gumroad UI Skills

Opinionated constraints for building Gumroad-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building dark-mode interfaces
- Creating Gumroad-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- MUST use dark backgrounds (lightness < 20) for primary surfaces - detected lightness: 0
- MUST use `#000000` as page background (`surface-base`)
- SHOULD reduce color palette (currently 16 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #000000 | rgb(0,0,0) | Page background |
| `surface-raised` | #FDFEFE | rgb(253,254,254) | Cards, modals, raised surfaces |
| `surface-overlay` | #F0F1EB | rgb(240,241,235) | Overlays, tooltips, dropdowns |
| `text-primary` | #353535 | rgb(53,53,53) | Headings, body text |
| `text-secondary` | #626262 | rgb(98,98,98) | Secondary, muted text |
| `text-tertiary` | #1D1D1D | rgb(29,29,29) | Additional text |
| `border-default` | #2C2C2C | rgb(44,44,44) | Subtle borders, dividers |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `92px` / `700` for primary headings
- MUST use `18px` / `400` for body text
- SHOULD reduce font weights (currently 5 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 92px | 700 | #181817 | 1 |
| `text-33px` | Inter | 33px | semi_bold | #1D1D1D | 1 |
| `text-30px` | Inter | 30px | 700 | #151515 | 1 |
| `text-25px` | Inter | 25px | 500 | #1E1E1E | 1 |
| `text-22px` | Inter | 22px | 500 | #353632 | 1 |
| `text-20px` | Inter | 20px | 400 | #353535 | 1 |
| `text-19px` | Inter | 19px | 400 | #C7C7C7 | 1 |
| `body` | Inter | 18px | 400 | #8A8B85 | 1 |
| `body-secondary` | Inter | 16px | 400 | #4B4B4B | 2 |
| `body-secondary` | Inter | 16px | 400 | #B2B2B2 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 22x)

**Font Sizes:** 8px, 10px, 11px, 12px, 13px, 14px, 15px, 16px, 18px, 19px, 20px, 22px, 25px, 30px, 33px, 92px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 5px, 6px
- SHOULD use 6px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 16px, 19px, 21px, 22px, 23px
- SHOULD use 21px+ radius for pill-shaped elements
- SHOULD limit border widths to: 1px, 2px
- SHOULD use 19px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 16px, 19px, 21px, 22px, 23px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 16px, 730px, 246px, 31px, 196px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Header**: height: 81px
- **Main Content**: width: 1920px, height: 997px
- **Main Content**: width: 1920px, height: 1001px
- **Header**: height: 78px

## Components

- MUST use `0px` height for input fields

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #C7C7C7 | none | - | - |

### Inputs

- Height: `0px`

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#5E6AD2`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#FDFEFE` background
- List items: use `#FDFEFE` background

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
