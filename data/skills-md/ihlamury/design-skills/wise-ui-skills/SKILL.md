---
name: wise-ui-skills
description: Wise's UI design system. Use when building interfaces inspired by Wise's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://wise.com
---

# Wise UI Skills

Opinionated constraints for building Wise-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Wise-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#91E75E` as page background (`surface-base`)
- SHOULD reduce color palette (currently 20 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #91E75E | rgb(145,231,94) | Page background |
| `surface-raised` | #FEFEFE | rgb(254,254,254) | Cards, modals, raised surfaces |
| `surface-overlay` | #E6EAE5 | rgb(230,234,229) | Overlays, tooltips, dropdowns |
| `text-primary` | #7C7C7C | rgb(124,124,124) | Headings, body text |
| `text-2` | #525B4B | rgb(82,91,75) | Additional text |
| `text-tertiary` | #4A4A4A | rgb(74,74,74) | Additional text |
| `border-default` | #EFFEE5 | rgb(239,254,229) | Subtle borders, dividers |
| `success` | #112501 | rgb(17,37,1) | Success states, confirmations |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `70px` / `700` for primary headings
- MUST use `41px` / `700` for body text
- SHOULD reduce font weights (currently 4 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 70px | 700 | #122902 | 1 |
| `heading-2` | Inter | 70px | 700 | #142E05 | 1 |
| `body` | Inter | 41px | 700 | #1E2F10 | 1 |
| `text-38px` | Inter | 38px | 700 | #213213 | 1 |
| `text-20px` | Inter | 20px | 700 | #1A3F0B | 1 |
| `text-19px` | Inter | 19px | 500 | #225411 | 1 |
| `text-17px` | Inter | 17px | 400 | #2C6418 | 1 |
| `text-16px` | Inter | 16px | 400 | #464646 | 1 |
| `text-16px` | Inter | 16px | 400 | #7CAF59 | 1 |
| `text-16px` | Inter | 16px | 400 | #7BAD57 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 26x)

**Font Sizes:** 11px, 12px, 13px, 14px, 15px, 16px, 17px, 19px, 20px, 38px, 41px, 70px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 3px, 4px, 5px, 6px, 7px, 19px, 33px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 4px, 15px, 18px, 19px, 20px, 21px, 22px, 37px
- SHOULD use 20px+ radius for pill-shaped elements
- SHOULD limit border widths to: 1px, 2px
- SHOULD use 20px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 4px, 15px, 18px, 19px, 20px, 21px, 22px, 37px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 7px, 66px, 14px, 503px, 48px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #3A3F39 | none | - | - |

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
