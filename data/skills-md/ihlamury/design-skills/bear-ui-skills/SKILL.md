---
name: bear-ui-skills
description: Bear's UI design system. Use when building interfaces inspired by Bear's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://bear.app
---

# Bear UI Skills

Opinionated constraints for building Bear-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Bear-inspired design systems
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
| `surface-raised` | #DDDDDE | rgb(221,221,222) | Cards, modals, raised surfaces |
| `surface-overlay` | #232428 | rgb(35,36,40) | Overlays, tooltips, dropdowns |
| `text-primary` | #8B8C90 | rgb(139,140,144) | Headings, body text |
| `text-secondary` | #7D7D7F | rgb(125,125,127) | Secondary, muted text |
| `text-tertiary` | #AB8C8E | rgb(171,140,142) | Additional text |
| `border-default` | #EFEFEF | rgb(239,239,239) | Subtle borders, dividers |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `50px` / `700` for primary headings
- MUST use `14px` / `400` for body text
- SHOULD reduce font weights (currently 5 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 50px | 700 | #494949 | 1 |
| `text-23px` | Inter | 23px | semi_bold | #474747 | 1 |
| `text-23px` | Inter | 23px | 500 | #535353 | 1 |
| `text-22px` | Inter | 22px | 400 | #A6A6A6 | 1 |
| `text-20px` | Inter | 20px | 400 | #A7A7A7 | 1 |
| `text-17px` | Inter | 17px | 400 | #A4A4A4 | 1 |
| `text-17px` | Inter | 17px | 400 | #686868 | 1 |
| `text-16px` | Inter | 16px | 400 | #7D7D7D | 1 |
| `text-16px` | Inter | 16px | 300 | #808080 | 1 |
| `text-16px` | Inter | 16px | 400 | #9B9B9B | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 53x)

**Font Sizes:** 7px, 10px, 11px, 12px, 13px, 14px, 15px, 16px, 17px, 20px, 22px, 23px, 50px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 6px, 7px, 8px
- SHOULD use 7px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 7px, 11px, 18px
- SHOULD limit border widths to: 1px, 2px, 6px
- SHOULD use 11px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 7px, 11px, 18px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 16px, 178px, 14px, 177px, 10px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 1080px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #7D7D7F | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#5E6AD2`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#DDDDDE` background
- List items: use `#DDDDDE` background

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
