---
name: coda-ui-skills
description: Coda's UI design system. Use when building interfaces inspired by Coda's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://coda.io
---

# Coda UI Skills

Opinionated constraints for building Coda-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Coda-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#FEFEFE` as page background (`surface-base`)
- MUST use `#DCEBF4` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 21 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #FEFEFE | rgb(254,254,254) | Page background |
| `surface-raised` | #000000 | rgb(0,0,0) | Cards, modals, raised surfaces |
| `surface-overlay` | #FEE0BC | rgb(254,224,188) | Overlays, tooltips, dropdowns |
| `text-primary` | #6D6D6D | rgb(109,109,109) | Headings, body text |
| `text-secondary` | #8E8E8E | rgb(142,142,142) | Secondary, muted text |
| `text-tertiary` | #41505D | rgb(65,80,93) | Additional text |
| `border-default` | #325395 | rgb(50,83,149) | Subtle borders, dividers |
| `accent` | #DCEBF4 | rgb(220,235,244) | Primary actions, links, focus |
| `destructive` | #F1E7E2 | rgb(241,231,226) | Error states, delete actions |
| `warning` | #FEE0BC | rgb(254,224,188) | Warning states, cautions |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `71px` / `700` for primary headings
- MUST use `16px` / `500` for body text
- SHOULD reduce font weights (currently 5 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 71px | 700 | #26231F | 1 |
| `text-58px` | Inter | 58px | 700 | #27231F | 1 |
| `text-21px` | Inter | 21px | 400 | #8A7762 | 1 |
| `text-20px` | Inter | 20px | 400 | #919191 | 1 |
| `text-20px` | Inter | 20px | semi_bold | #4F4F4F | 1 |
| `text-20px` | Inter | 20px | semi_bold | #30271D | 1 |
| `text-19px` | Inter | 19px | 400 | #8E8E8E | 1 |
| `text-18px` | Inter | 18px | semi_bold | #878989 | 1 |
| `text-18px` | Inter | 18px | 500 | #595959 | 1 |
| `body` | Inter | 16px | 500 | #6D6D6D | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 45x)

**Font Sizes:** 7px, 9px, 10px, 11px, 12px, 13px, 14px, 15px, 16px, 18px, 19px, 20px, 21px, 58px, 71px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 3px, 4px, 5px, 6px, 9px, 10px, 12px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 3px, 4px, 5px, 6px, 7px, 15px
- SHOULD limit border widths to: 1px, 2px, 3px
- SHOULD use 5px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 3px, 4px, 5px, 6px, 7px, 15px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 14px, 10px, 13px, 40px, 16px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1848px, height: 1080px
- **Main Content**: width: 1135px, height: 583px
- **Main Content**: width: 1135px, height: 584px

## Components

- MUST use `0px` height for input fields

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #41505D | none | - | - |

### Inputs

- Height: `0px`

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#DCEBF4`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#000000` background
- List items: use `#000000` background

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
