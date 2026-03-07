---
name: neon-ui-skills
description: Neon's UI design system. Use when building interfaces inspired by Neon's aesthetic - dark mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://neon.tech
---

# Neon UI Skills

Opinionated constraints for building Neon-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building dark-mode interfaces
- Creating Neon-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- MUST use dark backgrounds (lightness < 20) for primary surfaces - detected lightness: 0
- MUST use `#000000` as page background (`surface-base`)
- SHOULD reduce color palette (currently 15 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #000000 | rgb(0,0,0) | Page background |
| `surface-raised` | #262626 | rgb(38,38,38) | Cards, modals, raised surfaces |
| `surface-overlay` | #FEFEFE | rgb(254,254,254) | Overlays, tooltips, dropdowns |
| `text-primary` | #E3E3E3 | rgb(227,227,227) | Headings, body text |
| `text-2` | #ACACAC | rgb(172,172,172) | Additional text |
| `text-secondary` | #6A6B6E | rgb(106,107,110) | Secondary, muted text |
| `border-default` | #262626 | rgb(38,38,38) | Subtle borders, dividers |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `54px` / `700` for primary headings
- MUST use `16px` / `500` for body text
- SHOULD reduce font weights (currently 5 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 54px | 700 | #E8E9E8 | 1 |
| `text-26px` | Inter | 26px | semi_bold | #E3E3E3 | 1 |
| `text-24px` | Inter | 24px | 500 | #2C2D2E | 1 |
| `text-22px` | Inter | 22px | semi_bold | #7A7B80 | 1 |
| `text-20px` | Inter | 20px | 500 | #6A6B6E | 1 |
| `text-20px` | Inter | 20px | 500 | #6C6D70 | 1 |
| `text-18px` | Inter | 18px | semi_bold | #74757A | 1 |
| `text-17px` | Inter | 17px | 500 | #CECECE | 1 |
| `body` | Inter | 16px | 500 | #707175 | 1 |
| `body-secondary` | Inter | 14px | 400 | #9E9E9E | 2 |

### Typography Reference

**Font Families:**
- `Inter` (used 26x)

**Font Sizes:** 5px, 9px, 11px, 12px, 14px, 16px, 17px, 18px, 20px, 22px, 24px, 26px, 54px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 4px, 5px, 8px, 22px, 58px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 16px, 17px, 19px, 21px
- SHOULD use 21px+ radius for pill-shaped elements
- MUST use 1px border width consistently
- SHOULD use 19px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 16px, 17px, 19px, 21px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 8px, 50px, 26px, 28px, 37px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Header**: height: 37px
- **Main Content**: width: 1920px, height: 988px
- **Main Content**: width: 1850px, height: 711px
- **Main Content**: width: 1920px, height: 721px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #A3A3A3 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#5E6AD2`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#262626` background
- List items: use `#262626` background

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
