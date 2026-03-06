---
name: superhuman-ui-skills
description: Superhuman's UI design system. Use when building interfaces inspired by Superhuman's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://superhuman.com
---

# Superhuman UI Skills

Opinionated constraints for building Superhuman-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Superhuman-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#C9B7FD` as page background (`surface-base`)
- MUST use `#BCBAFC` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 24 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #C9B7FD | rgb(201,183,253) | Page background |
| `surface-raised` | #4B5196 | rgb(75,81,150) | Cards, modals, raised surfaces |
| `surface-overlay` | #351027 | rgb(53,16,39) | Overlays, tooltips, dropdowns |
| `text-primary` | #B8B1D7 | rgb(184,177,215) | Headings, body text |
| `text-secondary` | #BDC6DF | rgb(189,198,223) | Secondary, muted text |
| `text-tertiary` | #B398A9 | rgb(179,152,169) | Additional text |
| `border-default` | #4D5498 | rgb(77,84,152) | Subtle borders, dividers |
| `accent` | #BCBAFC | rgb(188,186,252) | Primary actions, links, focus |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `56px` / `extra_bold` for primary headings
- MUST use `25px` / `400` for body text
- SHOULD reduce font weights (currently 4 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 56px | extra_bold | #DDE3EC | 1 |
| `body` | Inter | 25px | 400 | #CEDCEE | 1 |
| `text-17px` | Inter | 17px | 400 | #7F5D77 | 1 |
| `text-16px` | Inter | 16px | 400 | #B1AFB9 | 1 |
| `text-15px` | Inter | 15px | 400 | #ABB1D6 | 1 |
| `text-15px` | Inter | 15px | 400 | #B49EBA | 1 |
| `text-14px` | Inter | 14px | 400 | #B1B5D9 | 1 |
| `text-14px` | Inter | 14px | 400 | #AFB5DB | 1 |
| `text-14px` | Inter | 14px | 400 | #A592B5 | 1 |
| `text-14px` | Inter | 14px | 400 | #B9ACD4 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 44x)

**Font Sizes:** 10px, 11px, 12px, 13px, 14px, 15px, 16px, 17px, 25px, 56px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 6px, 7px, 8px
- SHOULD use 3px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 3px, 4px, 7px, 8px, 10px, 15px, 21px, 22px, 23px
- SHOULD use 21px+ radius for pill-shaped elements
- SHOULD limit border widths to: 1px, 2px, 3px, 5px
- SHOULD use 10px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 3px, 4px, 7px, 8px, 10px, 15px, 21px, 22px, 23px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 11px, 10px, 14px, 44px, 220px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 1006px
- **Main Content**: width: 1920px, height: 1047px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #B8B1D7 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#BCBAFC`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#4B5196` background
- List items: use `#4B5196` background

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
