---
name: obsidian-ui-skills
description: Obsidian's UI design system. Use when building interfaces inspired by Obsidian's aesthetic - dark mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://obsidian.md
---

# Obsidian UI Skills

Opinionated constraints for building Obsidian-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building dark-mode interfaces
- Creating Obsidian-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- MUST use dark backgrounds (lightness < 20) for primary surfaces - detected lightness: 0
- MUST use `#000000` as page background (`surface-base`)
- MUST use `#6930C7` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 24 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #000000 | rgb(0,0,0) | Page background |
| `surface-raised` | #FEFEFD | rgb(254,254,253) | Cards, modals, raised surfaces |
| `surface-overlay` | #151027 | rgb(21,16,39) | Overlays, tooltips, dropdowns |
| `text-primary` | #858585 | rgb(133,133,133) | Headings, body text |
| `text-secondary` | #3A2F66 | rgb(58,47,102) | Secondary, muted text |
| `text-tertiary` | #555555 | rgb(85,85,85) | Additional text |
| `border-default` | #2F2F2F | rgb(47,47,47) | Subtle borders, dividers |
| `warning` | #FEFEFD | rgb(254,254,253) | Warning states, cautions |
| `accent` | #6930C7 | rgb(105,48,199) | Primary actions, links, focus |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `78px` / `700` for primary headings
- MUST use `14px` / `400` for body text
- SHOULD reduce font weights (currently 5 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 78px | 700 | #CDCDCD | 1 |
| `text-41px` | Inter | 41px | 500 | #8D8D8D | 1 |
| `text-24px` | Inter | 24px | semi_bold | #393939 | 1 |
| `text-20px` | Inter | 20px | 400 | #695C94 | 1 |
| `text-19px` | Inter | 19px | 500 | #939393 | 1 |
| `text-19px` | Inter | 19px | 400 | #DDB5F8 | 1 |
| `text-16px` | Inter | 16px | 500 | #666666 | 1 |
| `text-16px` | Inter | 16px | semi_bold | #B8B8B8 | 1 |
| `body` | Inter | 14px | 400 | #707070 | 1 |
| `body-secondary` | Inter | 14px | 400 | #747474 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 71x)

**Font Sizes:** 7px, 8px, 9px, 10px, 11px, 12px, 13px, 14px, 16px, 19px, 20px, 24px, 41px, 78px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 6px, 7px, 8px
- SHOULD use 2px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 3px, 4px, 5px, 6px, 8px, 11px, 23px
- SHOULD use 23px+ radius for pill-shaped elements
- SHOULD limit border widths to: 1px, 2px
- SHOULD use 4px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 3px, 4px, 5px, 6px, 8px, 11px, 23px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 8px, 11px, 10px, 12px, 9px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 1080px
- **Main Content**: width: 1920px, height: 643px

## Components

- MUST use `0px` height for input fields

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #3A2F66 | none | - | - |

### Inputs

- Height: `0px`

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#6930C7`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#FEFEFD` background
- List items: use `#FEFEFD` background

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
