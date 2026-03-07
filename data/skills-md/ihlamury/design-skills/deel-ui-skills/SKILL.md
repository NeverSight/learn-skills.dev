---
name: deel-ui-skills
description: Deel's UI design system. Use when building interfaces inspired by Deel's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://deel.com
---

# Deel UI Skills

Opinionated constraints for building Deel-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Deel-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#FDFDFD` as page background (`surface-base`)
- MUST use `#A2CDFB` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 32 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #FDFDFD | rgb(253,253,253) | Page background |
| `surface-raised` | #141414 | rgb(20,20,20) | Cards, modals, raised surfaces |
| `surface-overlay` | #000000 | rgb(0,0,0) | Overlays, tooltips, dropdowns |
| `text-primary` | #909090 | rgb(144,144,144) | Headings, body text |
| `text-secondary` | #C4C4C4 | rgb(196,196,196) | Secondary, muted text |
| `text-tertiary` | #344C65 | rgb(52,76,101) | Additional text |
| `border-default` | #86ADD7 | rgb(134,173,215) | Subtle borders, dividers |
| `accent` | #A2CDFB | rgb(162,205,251) | Primary actions, links, focus |
| `warning` | #907848 | rgb(144,120,72) | Warning states, cautions |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `53px` / `700` for primary headings
- MUST use `15px` / `400` for body text
- SHOULD reduce font weights (currently 6 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 53px | 700 | #27303B | 1 |
| `heading-2` | Inter | 51px | 700 | #272623 | 1 |
| `text-27px` | Inter | 27px | 700 | #2C2C2C | 1 |
| `text-26px` | Inter | 26px | 700 | #5A748E | 1 |
| `text-26px` | Inter | 26px | semi_bold | #55708C | 1 |
| `text-25px` | Inter | 25px | 700 | #576F88 | 1 |
| `text-24px` | Inter | 24px | 700 | #546A85 | 1 |
| `text-24px` | Inter | 24px | 700 | #516A83 | 1 |
| `text-18px` | Inter | 18px | 400 | #3D5A78 | 1 |
| `text-18px` | Inter | 18px | 400 | #6080A0 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 75x)

**Font Sizes:** 5px, 6px, 7px, 8px, 9px, 10px, 11px, 12px, 13px, 15px, 16px, 18px, 24px, 25px, 26px, 27px, 51px, 53px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 6px, 7px, 8px
- SHOULD use 2px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 0px, 1px, 2px, 3px, 4px, 5px, 6px, 7px, 9px, 12px, 15px, 17px, 18px, 22px, 23px
- SHOULD use 22px+ radius for pill-shaped elements
- SHOULD limit border widths to: 1px, 2px
- SHOULD use 3px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 0px, 1px, 2px, 3px, 4px, 5px, 6px, 7px, 9px, 12px, 15px, 17px, 18px, 22px, 23px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 9px, 12px, 11px, 20px, 14px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 876px
- **Main Content**: width: 1920px, height: 879px
- **Main Content**: width: 1920px, height: 596px
- **Header**: height: 64px
- **Header**: height: 63px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #344C65 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#A2CDFB`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#141414` background
- List items: use `#141414` background

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
