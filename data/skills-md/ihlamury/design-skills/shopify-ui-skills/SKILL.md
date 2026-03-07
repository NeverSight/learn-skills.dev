---
name: shopify-ui-skills
description: Shopify's UI design system. Use when building interfaces inspired by Shopify's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://shopify.com
---

# Shopify UI Skills

Opinionated constraints for building Shopify-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Shopify-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#FEFEFE` as page background (`surface-base`)
- SHOULD limit color palette to 10 distinct colors
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #FEFEFE | rgb(254,254,254) | Page background |
| `surface-raised` | #04090B | rgb(4,9,11) | Cards, modals, raised surfaces |
| `text-primary` | #858A8E | rgb(133,138,142) | Headings, body text |
| `text-secondary` | #C9CCCD | rgb(201,204,205) | Secondary, muted text |
| `text-tertiary` | #B9BCBF | rgb(185,188,191) | Additional text |
| `border-default` | #DFE1E2 | rgb(223,225,226) | Subtle borders, dividers |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `88px` / `extra_bold` for primary headings
- MUST use `39px` / `500` for body text
- SHOULD reduce font weights (currently 5 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 88px | extra_bold | #D5D6D7 | 1 |
| `text-63px` | Inter | 63px | semi_bold | #C9CCCD | 1 |
| `body` | Inter | 39px | 500 | #858A8E | 1 |
| `text-29px` | Inter | 29px | semi_bold | #DBDCDE | 1 |
| `text-27px` | Inter | 27px | 400 | #B7BABD | 1 |
| `text-17px` | Inter | 17px | 400 | #B9BCBF | 1 |
| `text-16px` | Inter | 16px | 400 | #9FA2A6 | 1 |
| `text-15px` | Inter | 15px | 300 | #A5A8AC | 1 |
| `text-15px` | Inter | 15px | 400 | #A4A7AA | 1 |
| `caption` | Inter | 13px | 400 | #3E3E3E | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 14x)

**Font Sizes:** 12px, 13px, 15px, 16px, 17px, 27px, 29px, 39px, 63px, 88px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 4px, 5px, 6px, 7px, 65px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 19px, 26px, 28px
- SHOULD use 26px+ radius for pill-shaped elements
- MUST use 2px border width consistently
- SHOULD use 19px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 19px, 26px, 28px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 11px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1855px, height: 1080px
- **Main Content**: width: 1920px, height: 747px
- **Main Content**: width: 1920px, height: 745px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #B9BCBF | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#5E6AD2`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#04090B` background
- List items: use `#04090B` background

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
