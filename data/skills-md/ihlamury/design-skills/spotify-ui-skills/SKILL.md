---
name: spotify-ui-skills
description: Spotify's UI design system. Use when building interfaces inspired by Spotify's aesthetic - dark mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://spotify.com
---

# Spotify UI Skills

Opinionated constraints for building Spotify-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building dark-mode interfaces
- Creating Spotify-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- MUST use dark backgrounds (lightness < 20) for primary surfaces - detected lightness: 9
- MUST use `#171717` as page background (`surface-base`)
- MUST use `#010002` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 14 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #171717 | rgb(23,23,23) | Page background |
| `surface-raised` | #FEFEFE | rgb(254,254,254) | Cards, modals, raised surfaces |
| `surface-overlay` | #010002 | rgb(1,0,2) | Overlays, tooltips, dropdowns |
| `text-primary` | #555555 | rgb(85,85,85) | Headings, body text |
| `text-secondary` | #6A6A6A | rgb(106,106,106) | Secondary, muted text |
| `text-tertiary` | #AEAEAE | rgb(174,174,174) | Additional text |
| `border-default` | #838486 | rgb(131,132,134) | Subtle borders, dividers |
| `accent` | #010002 | rgb(1,0,2) | Primary actions, links, focus |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `41px` / `500` for primary headings
- MUST use `13px` / `400` for body text
- SHOULD reduce font weights (currently 4 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 41px | 500 | #2D2D2D | 1 |
| `text-24px` | Inter | 24px | semi_bold | #DBDBDB | 1 |
| `text-24px` | Inter | 24px | 500 | #DBDBDB | 1 |
| `text-24px` | Inter | 24px | semi_bold | #DCDCDC | 1 |
| `text-17px` | Inter | 17px | 400 | #676667 | 1 |
| `text-16px` | Inter | 16px | 400 | #A6A6A6 | 1 |
| `text-15px` | Inter | 15px | 400 | #AEAEAE | 1 |
| `text-15px` | Inter | 15px | 400 | #6B6B6B | 1 |
| `text-15px` | Inter | 15px | 400 | #A4A4A4 | 1 |
| `text-15px` | Inter | 15px | 400 | #717171 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 81x)

**Font Sizes:** 8px, 9px, 10px, 11px, 12px, 13px, 14px, 15px, 16px, 17px, 24px, 41px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 6px, 7px, 8px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 10px, 15px, 17px, 18px, 22px, 24px
- SHOULD use 22px+ radius for pill-shaped elements
- SHOULD limit border widths to: 1px, 2px
- SHOULD use 15px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 10px, 15px, 17px, 18px, 22px, 24px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 172px, 68px, 171px, 185px, 38px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 1080px
- **Header**: height: 60px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #B8B8B8 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#010002`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#FEFEFE` background
- List items: use `#FEFEFE` background

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
