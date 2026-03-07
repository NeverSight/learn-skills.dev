---
name: liveblocks-ui-skills
description: Liveblocks's UI design system. Use when building interfaces inspired by Liveblocks's aesthetic - dark mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://liveblocks.io
---

# Liveblocks UI Skills

Opinionated constraints for building Liveblocks-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building dark-mode interfaces
- Creating Liveblocks-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- MUST use dark backgrounds (lightness < 20) for primary surfaces - detected lightness: 0
- MUST use `#000000` as page background (`surface-base`)
- SHOULD reduce color palette (currently 11 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #000000 | rgb(0,0,0) | Page background |
| `surface-raised` | #E5E5E5 | rgb(229,229,229) | Cards, modals, raised surfaces |
| `surface-overlay` | #FEFEFE | rgb(254,254,254) | Overlays, tooltips, dropdowns |
| `text-primary` | #818181 | rgb(129,129,129) | Headings, body text |
| `text-secondary` | #5B595A | rgb(91,89,90) | Secondary, muted text |
| `text-tertiary` | #B5B5B5 | rgb(181,181,181) | Additional text |
| `border-default` | #EAEAEA | rgb(234,234,234) | Subtle borders, dividers |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `54px` / `700` for primary headings
- MUST use `19px` / `400` for body text
- MUST limit font weights to: medium, regular, bold
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 54px | 700 | #E9E9E9 | 1 |
| `body` | Inter | 19px | 400 | #818181 | 1 |
| `body-secondary` | Inter | 19px | 400 | #8E8E8E | 1 |
| `body-secondary` | Inter | 18px | 400 | #737373 | 1 |
| `body-secondary` | Inter | 18px | 500 | #C4C4C4 | 1 |
| `body-secondary` | Inter | 17px | 400 | #707070 | 1 |
| `text-15px` | Inter | 15px | 400 | #8E8E8E | 1 |
| `text-15px` | Inter | 15px | 400 | #747474 | 1 |
| `text-15px` | Inter | 15px | 400 | #777777 | 1 |
| `text-15px` | Inter | 15px | 400 | #797979 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 30x)

**Font Sizes:** 6px, 8px, 11px, 12px, 14px, 15px, 17px, 18px, 19px, 54px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 6px, 7px, 8px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 3px, 5px, 19px
- MUST use 1px border width consistently
- SHOULD use 3px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 3px, 5px, 19px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 36px, 48px, 1px, 8px, 47px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1855px, height: 1080px
- **Main Content**: width: 1920px, height: 769px
- **Main Content**: width: 1920px, height: 559px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #6B6B6B | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#5E6AD2`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#E5E5E5` background
- List items: use `#E5E5E5` background

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
