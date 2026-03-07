---
name: ashby-ui-skills
description: Ashby's UI design system. Use when building interfaces inspired by Ashby's aesthetic - dark mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://ashby.com
---

# Ashby UI Skills

Opinionated constraints for building Ashby-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building dark-mode interfaces
- Creating Ashby-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- MUST use dark backgrounds (lightness < 20) for primary surfaces - detected lightness: 9
- MUST use `#0E1122` as page background (`surface-base`)
- SHOULD limit color palette to 8 distinct colors
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #0E1122 | rgb(14,17,34) | Page background |
| `surface-raised` | #FEFEFE | rgb(254,254,254) | Cards, modals, raised surfaces |
| `text-primary` | #D6D9DD | rgb(214,217,221) | Headings, body text |
| `text-secondary` | #34384D | rgb(52,56,77) | Secondary, muted text |
| `text-tertiary` | #797979 | rgb(121,121,121) | Additional text |
| `border-default` | #818288 | rgb(129,130,136) | Subtle borders, dividers |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `28px` / `700` for primary headings
- MUST use `24px` / `semi_bold` for body text
- SHOULD reduce font weights (currently 4 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 28px | 700 | #E6E8EB | 1 |
| `heading-2` | Inter | 25px | semi_bold | #D1D3D8 | 1 |
| `heading-3` | Inter | 24px | semi_bold | #E2E5E9 | 1 |
| `body` | Inter | 24px | semi_bold | #E0E2E6 | 1 |
| `body-secondary` | Inter | 24px | semi_bold | #D7D9DD | 1 |
| `text-19px` | Inter | 19px | semi_bold | #D6D9DD | 1 |
| `text-19px` | Inter | 19px | 400 | #507A5D | 1 |
| `text-16px` | Inter | 16px | 400 | #797979 | 1 |
| `text-15px` | Inter | 15px | 400 | #34384D | 1 |
| `caption` | Inter | 14px | 400 | #313549 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 16x)

**Font Sizes:** 12px, 13px, 14px, 15px, 16px, 19px, 24px, 25px, 28px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 2px, 3px, 4px, 5px, 88px
- SHOULD use 2px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 10px
- MUST use 4px border width consistently
- SHOULD use 10px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 10px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 560px, 17px, 564px, 1px, 79px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

## Components

- MUST use `0px` height for input fields

### Inputs

- Height: `0px`

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#5E6AD2`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#FEFEFE` background
- List items: use `#FEFEFE` background

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
