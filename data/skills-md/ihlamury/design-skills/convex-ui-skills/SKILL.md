---
name: convex-ui-skills
description: Convex's UI design system. Use when building interfaces inspired by Convex's aesthetic - dark mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://convex.dev
---

# Convex UI Skills

Opinionated constraints for building Convex-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building dark-mode interfaces
- Creating Convex-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- MUST use dark backgrounds (lightness < 20) for primary surfaces - detected lightness: 6
- MUST use `#0F0F0F` as page background (`surface-base`)
- MUST use `#214AE8` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 31 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #0F0F0F | rgb(15,15,15) | Page background |
| `surface-raised` | #262523 | rgb(38,37,35) | Cards, modals, raised surfaces |
| `surface-overlay` | #F2EAD3 | rgb(242,234,211) | Overlays, tooltips, dropdowns |
| `text-primary` | #676151 | rgb(103,97,81) | Headings, body text |
| `text-secondary` | #403D37 | rgb(64,61,55) | Secondary, muted text |
| `text-tertiary` | #515151 | rgb(81,81,81) | Additional text |
| `border-default` | #3A3934 | rgb(58,57,52) | Subtle borders, dividers |
| `accent` | #214AE8 | rgb(33,74,232) | Primary actions, links, focus |
| `destructive` | #4F3727 | rgb(79,55,39) | Error states, delete actions |
| `warning` | #F2EAD3 | rgb(242,234,211) | Warning states, cautions |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `40px` / `semi_bold` for primary headings
- MUST use `21px` / `400` for body text
- SHOULD reduce font weights (currently 5 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 40px | semi_bold | #DDDDD7 | 1 |
| `text-31px` | Inter | 31px | 700 | #403D37 | 1 |
| `body` | Inter | 21px | 400 | #676151 | 1 |
| `body-secondary` | Inter | 20px | 700 | #EBEBE7 | 1 |
| `text-18px` | Inter | 18px | 400 | #B4B4AC | 1 |
| `text-18px` | Inter | 18px | 500 | #CBCBC3 | 1 |
| `text-15px` | Inter | 15px | 400 | #5B5B5B | 1 |
| `text-15px` | Inter | 15px | 400 | #B5B5AD | 1 |
| `text-14px` | Inter | 14px | 500 | #5B5B5B | 1 |
| `text-14px` | Inter | 14px | 400 | #5D5D5D | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 95x)

**Font Sizes:** 4px, 6px, 7px, 8px, 9px, 10px, 11px, 12px, 13px, 14px, 15px, 18px, 20px, 21px, 31px, 40px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 6px, 7px, 8px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 1px, 3px, 4px, 6px, 7px, 10px, 13px, 15px, 18px, 21px, 50px, 54px
- SHOULD use 21px+ radius for pill-shaped elements
- SHOULD limit border widths to: 1px, 2px
- SHOULD use 3px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 1px, 3px, 4px, 6px, 7px, 10px, 13px, 15px, 18px, 21px, 50px, 54px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 12px, 7px, 8px, 2px, 24px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1777px, height: 831px
- **Main Content**: width: 1513px, height: 852px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #5C5646 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#214AE8`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#262523` background
- List items: use `#262523` background

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
