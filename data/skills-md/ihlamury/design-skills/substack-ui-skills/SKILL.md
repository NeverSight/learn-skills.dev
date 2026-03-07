---
name: substack-ui-skills
description: Substack's UI design system. Use when building interfaces inspired by Substack's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://substack.com
---

# Substack UI Skills

Opinionated constraints for building Substack-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Substack-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#FFFFFF` as page background (`surface-base`)
- SHOULD reduce color palette (currently 15 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #FFFFFF | rgb(255,255,255) | Page background |
| `surface-raised` | #FC5013 | rgb(252,80,19) | Cards, modals, raised surfaces |
| `surface-overlay` | #E9E9E9 | rgb(233,233,233) | Overlays, tooltips, dropdowns |
| `text-primary` | #999999 | rgb(153,153,153) | Headings, body text |
| `text-2` | #515151 | rgb(81,81,81) | Additional text |
| `text-secondary` | #717171 | rgb(113,113,113) | Secondary, muted text |
| `border-default` | #E7E7E7 | rgb(231,231,231) | Subtle borders, dividers |
| `destructive` | #E26739 | rgb(226,103,57) | Error states, delete actions |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `36px` / `semi_bold` for primary headings
- MUST use `17px` / `500` for body text
- SHOULD reduce font weights (currently 4 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 36px | semi_bold | #BCDBD7 | 1 |
| `text-19px` | Inter | 19px | semi_bold | #4C4D4D | 1 |
| `body` | Inter | 17px | 500 | #535353 | 1 |
| `body-secondary` | Inter | 16px | 400 | #717171 | 1 |
| `body-secondary` | Inter | 16px | 400 | #6E6E6F | 1 |
| `body-secondary` | Inter | 16px | 400 | #F5C0A3 | 1 |
| `body-secondary` | Inter | 15px | 400 | #969696 | 2 |
| `body-secondary` | Inter | 15px | 500 | #515151 | 1 |
| `body-secondary` | Inter | 15px | 400 | #6F6F6F | 1 |
| `body-secondary` | Inter | 15px | 500 | #5D5D5D | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 43x)

**Font Sizes:** 5px, 9px, 10px, 11px, 12px, 13px, 14px, 15px, 16px, 17px, 19px, 36px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 3px, 4px, 5px, 8px, 9px, 10px, 13px
- SHOULD use 4px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 3px, 4px, 6px, 7px, 8px, 9px, 16px, 18px
- MUST use 1px border width consistently
- SHOULD use 9px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 3px, 4px, 6px, 7px, 8px, 9px, 16px, 18px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 12px, 16px, 18px, 17px, 22px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 1080px

## Components

- MUST use `0px` height for input fields

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #515151 | none | - | - |

### Inputs

- Height: `0px`

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#5E6AD2`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#FC5013` background
- List items: use `#FC5013` background

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
