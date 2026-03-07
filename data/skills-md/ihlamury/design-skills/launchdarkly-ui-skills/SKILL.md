---
name: launchdarkly-ui-skills
description: Launchdarkly's UI design system. Use when building interfaces inspired by Launchdarkly's aesthetic - dark mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://launchdarkly.com
---

# Launchdarkly UI Skills

Opinionated constraints for building Launchdarkly-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building dark-mode interfaces
- Creating Launchdarkly-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- MUST use dark backgrounds (lightness < 20) for primary surfaces - detected lightness: 0
- MUST use `#000000` as page background (`surface-base`)
- MUST use `#AAB7F5` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 13 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #000000 | rgb(0,0,0) | Page background |
| `surface-raised` | #131313 | rgb(19,19,19) | Cards, modals, raised surfaces |
| `text-primary` | #DFDFDF | rgb(223,223,223) | Headings, body text |
| `text-secondary` | #3D69B0 | rgb(61,105,176) | Secondary, muted text |
| `text-tertiary` | #C1C1CD | rgb(193,193,205) | Additional text |
| `accent` | #AAB7F5 | rgb(170,183,245) | Primary actions, links, focus |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `138px` / `700` for primary headings
- MUST use `32px` / `700` for body text
- SHOULD reduce font weights (currently 6 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 138px | 700 | #F7F7F7 | 1 |
| `heading-2` | Inter | 138px | 700 | #D5D7F0 | 1 |
| `body` | Inter | 32px | 700 | #DFDFDF | 1 |
| `text-29px` | Inter | 29px | semi_bold | #E0E0E0 | 1 |
| `text-25px` | Inter | 25px | 700 | #DFDFDF | 1 |
| `text-23px` | Inter | 23px | semi_bold | #D1D1D1 | 1 |
| `text-21px` | Inter | 21px | 500 | #C2C2C2 | 1 |
| `text-21px` | Inter | 21px | 400 | #5557A0 | 1 |
| `text-20px` | Inter | 20px | 400 | #3D69B0 | 1 |
| `text-20px` | Inter | 20px | 400 | #C1C1CD | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 31x)

**Font Sizes:** 9px, 10px, 11px, 12px, 13px, 14px, 15px, 16px, 18px, 19px, 20px, 21px, 23px, 25px, 29px, 32px, 138px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 4px, 5px, 7px, 9px, 12px, 21px, 28px, 69px
- SHOULD use 4px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 10px, 14px, 25px, 29px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 949px
- **Main Content**: width: 1920px, height: 1031px
- **Header**: height: 47px
- **Header**: height: 48px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #3D69B0 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#AAB7F5`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#131313` background
- List items: use `#131313` background

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
