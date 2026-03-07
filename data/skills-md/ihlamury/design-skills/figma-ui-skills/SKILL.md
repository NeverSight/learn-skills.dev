---
name: figma-ui-skills
description: Figma's UI design system. Use when building interfaces inspired by Figma's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://figma.com
---

# Figma UI Skills

Opinionated constraints for building Figma-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Figma-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#FFFFFF` as page background (`surface-base`)
- MUST use `#BEBAF6` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 12 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #FFFFFF | rgb(255,255,255) | Page background |
| `surface-raised` | #3A28FA | rgb(58,40,250) | Cards, modals, raised surfaces |
| `surface-overlay` | #E7E7E7 | rgb(231,231,231) | Overlays, tooltips, dropdowns |
| `text-primary` | #545454 | rgb(84,84,84) | Headings, body text |
| `text-2` | #262626 | rgb(38,38,38) | Additional text |
| `text-tertiary` | #656565 | rgb(101,101,101) | Additional text |
| `border-default` | #4D3ECF | rgb(77,62,207) | Subtle borders, dividers |
| `accent` | #BEBAF6 | rgb(190,186,246) | Primary actions, links, focus |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `57px` / `extra_bold` for primary headings
- MUST use `36px` / `700` for body text
- SHOULD reduce font weights (currently 5 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 57px | extra_bold | #232323 | 1 |
| `body` | Inter | 36px | 700 | #272727 | 1 |
| `text-30px` | Inter | 30px | 700 | #2C2C2C | 1 |
| `text-28px` | Inter | 28px | 500 | #545454 | 1 |
| `text-26px` | Inter | 26px | semi_bold | #272727 | 1 |
| `text-22px` | Inter | 22px | 400 | #2D2D2D | 1 |
| `text-20px` | Inter | 20px | 500 | #545454 | 1 |
| `text-18px` | Inter | 18px | semi_bold | #262626 | 1 |
| `text-18px` | Inter | 18px | semi_bold | #373737 | 1 |
| `text-17px` | Inter | 17px | semi_bold | #313131 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 23x)

**Font Sizes:** 13px, 14px, 15px, 16px, 17px, 18px, 20px, 22px, 26px, 28px, 30px, 36px, 57px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 2px, 4px, 5px, 9px, 10px, 11px, 37px, 67px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 3px, 4px
- MUST use 1px border width consistently
- SHOULD use 3px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 3px, 4px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 36px, 12px, 18px, 79px, 21px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 900px
- **Main Content**: width: 1602px, height: 617px
- **Header**: height: 81px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #BEBAF6 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#BEBAF6`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#3A28FA` background
- List items: use `#3A28FA` background

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
