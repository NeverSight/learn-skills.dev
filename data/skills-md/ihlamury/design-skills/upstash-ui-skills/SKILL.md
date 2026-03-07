---
name: upstash-ui-skills
description: Upstash's UI design system. Use when building interfaces inspired by Upstash's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://upstash.com
---

# Upstash UI Skills

Opinionated constraints for building Upstash-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Upstash-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#000000` as page background (`surface-base`)
- MUST use `#15B169` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 21 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #000000 | rgb(0,0,0) | Page background |
| `surface-raised` | #F2F2F2 | rgb(242,242,242) | Cards, modals, raised surfaces |
| `surface-overlay` | #15B169 | rgb(21,177,105) | Overlays, tooltips, dropdowns |
| `text-primary` | #7E7D82 | rgb(126,125,130) | Headings, body text |
| `text-secondary` | #F7E89F | rgb(247,232,159) | Secondary, muted text |
| `text-tertiary` | #C04351 | rgb(192,67,81) | Additional text |
| `border-default` | #E6E8E7 | rgb(230,232,231) | Subtle borders, dividers |
| `accent` | #15B169 | rgb(21,177,105) | Primary actions, links, focus |
| `destructive` | #C04351 | rgb(192,67,81) | Error states, delete actions |
| `success` | #3FA25D | rgb(63,162,93) | Success states, confirmations |
| `warning` | #F7E89F | rgb(247,232,159) | Warning states, cautions |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `100px` / `700` for primary headings
- MUST use `25px` / `400` for body text
- SHOULD reduce font weights (currently 5 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 100px | 700 | #3FA25D | 1 |
| `heading-2` | Inter | 96px | 700 | #3CA662 | 1 |
| `body` | Inter | 25px | 400 | #7A8686 | 1 |
| `body-secondary` | Inter | 24px | semi_bold | #314440 | 1 |
| `body-secondary` | Inter | 23px | 500 | #2B3F3A | 1 |
| `body-secondary` | Inter | 23px | 500 | #2D423D | 1 |
| `body-secondary` | Inter | 23px | 500 | #487163 | 1 |
| `text-19px` | Inter | 19px | 500 | #818085 | 1 |
| `text-18px` | Inter | 18px | 500 | #7B7A7F | 1 |
| `text-18px` | Inter | 18px | semi_bold | #C04351 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 38x)

**Font Sizes:** 10px, 11px, 12px, 13px, 14px, 15px, 16px, 17px, 18px, 19px, 23px, 24px, 25px, 96px, 100px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 6px, 7px, 8px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 6px, 9px, 10px, 12px, 13px, 15px, 16px
- SHOULD limit border widths to: 1px, 2px
- SHOULD use 15px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 6px, 9px, 10px, 12px, 13px, 15px, 16px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 20px, 24px, 18px, 172px, 199px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 1038px
- **Header**: height: 43px
- **Main Content**: width: 1855px, height: 1080px
- **Main Content**: width: 1920px, height: 598px

## Components

- MUST use `0px` height for input fields

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #7E7D82 | none | - | - |

### Inputs

- Height: `0px`

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#15B169`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#F2F2F2` background
- List items: use `#F2F2F2` background

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
