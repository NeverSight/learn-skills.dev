---
name: warp-ui-skills
description: Warp's UI design system. Use when building interfaces inspired by Warp's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://warp.dev
---

# Warp UI Skills

Opinionated constraints for building Warp-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Warp-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#FFFFFF` as page background (`surface-base`)
- SHOULD reduce color palette (currently 16 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #FFFFFF | rgb(255,255,255) | Page background |
| `surface-raised` | #222222 | rgb(34,34,34) | Cards, modals, raised surfaces |
| `surface-overlay` | #D2D1CE | rgb(210,209,206) | Overlays, tooltips, dropdowns |
| `text-primary` | #AAAAAA | rgb(170,170,170) | Headings, body text |
| `text-secondary` | #6C6C6C | rgb(108,108,108) | Secondary, muted text |
| `text-tertiary` | #393939 | rgb(57,57,57) | Additional text |
| `border-default` | #DCDBD7 | rgb(220,219,215) | Subtle borders, dividers |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `74px` / `700` for primary headings
- MUST use `24px` / `700` for body text
- SHOULD reduce font weights (currently 5 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 74px | 700 | #F0F0F0 | 1 |
| `body` | Inter | 24px | 700 | #4E4E4E | 1 |
| `body-secondary` | Inter | 22px | 300 | #797D7E | 1 |
| `text-21px` | Inter | 21px | 300 | #7B7F81 | 1 |
| `text-20px` | Inter | 20px | 300 | #7B8081 | 1 |
| `text-20px` | Inter | 20px | semi_bold | #D2D2D2 | 1 |
| `text-20px` | Inter | 20px | 500 | #686868 | 1 |
| `text-20px` | Inter | 20px | 400 | #595959 | 1 |
| `text-19px` | Inter | 19px | 500 | #393939 | 1 |
| `text-19px` | Inter | 19px | 400 | #5E5E5E | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 45x)

**Font Sizes:** 6px, 7px, 8px, 9px, 11px, 12px, 13px, 14px, 15px, 16px, 18px, 19px, 20px, 21px, 22px, 24px, 74px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 6px, 9px, 10px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 3px, 9px, 16px, 18px
- SHOULD limit border widths to: 1px, 2px
- SHOULD use 18px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 3px, 9px, 16px, 18px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 8px, 10px, 14px, 9px, 5px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 1025px
- **Main Content**: width: 1920px, height: 1032px
- **Header**: height: 48px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #AAAAAA | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#5E6AD2`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#222222` background
- List items: use `#222222` background

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
