---
name: resend-ui-skills
description: Resend's UI design system. Use when building interfaces inspired by Resend's aesthetic - dark mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://resend.com
---

# Resend UI Skills

Opinionated constraints for building Resend-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building dark-mode interfaces
- Creating Resend-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- MUST use dark backgrounds (lightness < 20) for primary surfaces - detected lightness: 2
- MUST use `#060606` as page background (`surface-base`)
- SHOULD limit color palette to 5 distinct colors
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #060606 | rgb(6,6,6) | Page background |
| `surface-raised` | #1D1D1D | rgb(29,29,29) | Cards, modals, raised surfaces |
| `text-primary` | #6E6E6E | rgb(110,110,110) | Headings, body text |
| `text-2` | #BBBBBB | rgb(187,187,187) | Additional text |
| `border-default` | #191919 | rgb(25,25,25) | Subtle borders, dividers |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `88px` / `700` for primary headings
- MUST use `18px` / `400` for body text
- MUST limit font weights to: bold, regular, medium
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 88px | 700 | #C8C8C8 | 1 |
| `body` | Inter | 18px | 400 | #646464 | 1 |
| `body-secondary` | Inter | 17px | 500 | #BFBFBF | 1 |
| `text-15px` | Inter | 15px | 400 | #6A6A6A | 1 |
| `text-14px` | Inter | 14px | 400 | #666666 | 1 |
| `text-14px` | Inter | 14px | 400 | #626262 | 1 |
| `text-14px` | Inter | 14px | 400 | #646464 | 1 |
| `caption` | Inter | 13px | 400 | #6E6E6E | 1 |
| `label` | Inter | 12px | 500 | #BBBBBB | 1 |
| `label` | Inter | 11px | 400 | #B6B6B5 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 13x)

**Font Sizes:** 11px, 12px, 13px, 14px, 15px, 17px, 18px, 88px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 4px, 5px, 13px, 19px, 22px, 60px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 15px
- SHOULD limit border widths to: 2px, 3px
- SHOULD use 15px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 15px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 8px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 963px
- **Header**: height: 57px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #BBBBBB | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#5E6AD2`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#1D1D1D` background
- List items: use `#1D1D1D` background

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
