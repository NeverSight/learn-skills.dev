---
name: amplitude-ui-skills
description: Amplitude's UI design system. Use when building interfaces inspired by Amplitude's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://amplitude.com
---

# Amplitude UI Skills

Opinionated constraints for building Amplitude-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Amplitude-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#000000` as page background (`surface-base`)
- MUST use `#3151E1` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 25 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #000000 | rgb(0,0,0) | Page background |
| `surface-raised` | #FFFFFF | rgb(255,255,255) | Cards, modals, raised surfaces |
| `surface-overlay` | #EFF0F4 | rgb(239,240,244) | Overlays, tooltips, dropdowns |
| `text-primary` | #171717 | rgb(23,23,23) | Headings, body text |
| `text-2` | #383838 | rgb(56,56,56) | Additional text |
| `text-secondary` | #BBBBBB | rgb(187,187,187) | Secondary, muted text |
| `border-default` | #3A3A3A | rgb(58,58,58) | Subtle borders, dividers |
| `accent` | #3151E1 | rgb(49,81,225) | Primary actions, links, focus |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `58px` / `700` for primary headings
- MUST use `23px` / `500` for body text
- SHOULD reduce font weights (currently 4 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 58px | 700 | #1D46E1 | 1 |
| `heading-2` | Inter | 56px | 700 | #161616 | 1 |
| `text-40px` | Inter | 40px | 700 | #171717 | 1 |
| `body` | Inter | 23px | 500 | #282828 | 1 |
| `text-19px` | Inter | 19px | 400 | #656565 | 1 |
| `text-16px` | Inter | 16px | 400 | #383838 | 1 |
| `text-14px` | Inter | 14px | 400 | #474747 | 1 |
| `text-14px` | Inter | 14px | 400 | #3E3E3E | 1 |
| `text-13px` | Inter | 13px | 400 | #BBBBBB | 1 |
| `text-13px` | Inter | 13px | 400 | #575757 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 51x)

**Font Sizes:** 5px, 6px, 7px, 8px, 9px, 10px, 11px, 13px, 14px, 16px, 19px, 23px, 40px, 56px, 58px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 6px, 7px, 11px
- SHOULD use 4px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 1px, 2px, 3px, 5px, 6px, 12px, 18px, 25px
- SHOULD use 25px+ radius for pill-shaped elements
- SHOULD limit border widths to: 1px, 2px, 4px
- SHOULD use 25px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 1px, 2px, 3px, 5px, 6px, 12px, 18px, 25px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 118px, 17px, 135px, 14px, 9px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1465px, height: 988px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #383838 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#3151E1`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#FFFFFF` background
- List items: use `#FFFFFF` background

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
