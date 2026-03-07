---
name: descript-ui-skills
description: Descript's UI design system. Use when building interfaces inspired by Descript's aesthetic - dark mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://descript.com
---

# Descript UI Skills

Opinionated constraints for building Descript-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building dark-mode interfaces
- Creating Descript-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- MUST use dark backgrounds (lightness < 20) for primary surfaces - detected lightness: 10
- MUST use `#2C0814` as page background (`surface-base`)
- SHOULD reduce color palette (currently 17 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #2C0814 | rgb(44,8,20) | Page background |
| `surface-raised` | #F9F6F3 | rgb(249,246,243) | Cards, modals, raised surfaces |
| `surface-overlay` | #F2212E | rgb(242,33,46) | Overlays, tooltips, dropdowns |
| `text-primary` | #484543 | rgb(72,69,67) | Headings, body text |
| `text-secondary` | #747474 | rgb(116,116,116) | Secondary, muted text |
| `text-tertiary` | #F4A9AF | rgb(244,169,175) | Additional text |
| `border-default` | #ECE3E4 | rgb(236,227,228) | Subtle borders, dividers |
| `destructive` | #F2212E | rgb(242,33,46) | Error states, delete actions |
| `warning` | #F9F6F3 | rgb(249,246,243) | Warning states, cautions |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `79px` / `700` for primary headings
- MUST use `18px` / `400` for body text
- MUST limit font weights to: regular, bold, medium
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 79px | 700 | #F1E6E3 | 1 |
| `body` | Inter | 18px | 400 | #BEBEBE | 1 |
| `body-secondary` | Inter | 17px | 500 | #3E3337 | 1 |
| `body-secondary` | Inter | 16px | 400 | #C6ACB4 | 1 |
| `body-secondary` | Inter | 16px | 400 | #3E3236 | 1 |
| `caption` | Inter | 15px | 500 | #484543 | 1 |
| `label` | Inter | 15px | 400 | #A52335 | 1 |
| `label` | Inter | 15px | 400 | #413438 | 1 |
| `label` | Inter | 14px | 400 | #747474 | 1 |
| `label` | Inter | 14px | 400 | #F4A9AF | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 15x)

**Font Sizes:** 13px, 14px, 15px, 16px, 17px, 18px, 79px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 5px, 6px, 12px, 30px, 31px, 57px, 68px
- SHOULD use 6px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 3px, 6px, 7px, 9px, 13px
- SHOULD limit border widths to: 1px, 3px, 4px
- SHOULD use 6px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 3px, 6px, 7px, 9px, 13px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 8px, 621px, 620px, 9px, 68px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 1080px
- **Main Content**: width: 1920px, height: 920px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #F4A9AF | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#5E6AD2`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#F9F6F3` background
- List items: use `#F9F6F3` background

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
