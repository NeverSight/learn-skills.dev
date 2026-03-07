---
name: mem-ui-skills
description: Mem's UI design system. Use when building interfaces inspired by Mem's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://mem.ai
---

# Mem UI Skills

Opinionated constraints for building Mem-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Mem-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#F9F5ED` as page background (`surface-base`)
- MUST use `#95A3DC` for primary actions and focus states (`accent`)
- SHOULD limit color palette to 9 distinct colors
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #F9F5ED | rgb(249,245,237) | Page background |
| `surface-raised` | #EADCC3 | rgb(234,220,195) | Cards, modals, raised surfaces |
| `text-primary` | #474449 | rgb(71,68,73) | Headings, body text |
| `text-2` | #665E53 | rgb(102,94,83) | Additional text |
| `text-tertiary` | #2F2C3D | rgb(47,44,61) | Additional text |
| `border-default` | #534F59 | rgb(83,79,89) | Subtle borders, dividers |
| `warning` | #F9F5ED | rgb(249,245,237) | Warning states, cautions |
| `accent` | #95A3DC | rgb(149,163,220) | Primary actions, links, focus |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `86px` / `700` for primary headings
- MUST use `20px` / `400` for body text
- MUST limit font weights to: regular, bold, semi_bold
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 86px | 700 | #2F2C3D | 1 |
| `body` | Inter | 20px | 400 | #665E53 | 1 |
| `body-secondary` | Inter | 20px | 400 | #423E44 | 1 |
| `body-secondary` | Inter | 19px | 400 | #474349 | 1 |
| `body-secondary` | Inter | 19px | 400 | #514B51 | 1 |
| `body-secondary` | Inter | 19px | 400 | #605A60 | 1 |
| `body-secondary` | Inter | 19px | semi_bold | #34313F | 1 |
| `body-secondary` | Inter | 18px | 400 | #504B4F | 1 |
| `body-secondary` | Inter | 18px | 400 | #514D53 | 1 |
| `text-16px` | Inter | 16px | 400 | #474449 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 13x)

**Font Sizes:** 13px, 14px, 16px, 18px, 19px, 20px, 86px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 4px, 5px, 6px, 8px, 13px, 28px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 16px, 29px, 32px, 33px, 37px, 39px
- SHOULD use 29px+ radius for pill-shaped elements
- SHOULD limit border widths to: 1px, 2px, 3px
- SHOULD use 37px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 16px, 29px, 32px, 33px, 37px, 39px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 302px, 304px, 74px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 937px
- **Main Content**: width: 1920px, height: 920px
- **Header**: height: 72px
- **Header**: height: 71px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #474449 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#95A3DC`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#EADCC3` background
- List items: use `#EADCC3` background

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
