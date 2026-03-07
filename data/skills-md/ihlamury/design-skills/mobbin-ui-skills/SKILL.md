---
name: mobbin-ui-skills
description: Mobbin's UI design system. Use when building interfaces inspired by Mobbin's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://mobbin.com
---

# Mobbin UI Skills

Opinionated constraints for building Mobbin-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Mobbin-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#FFFFFF` as page background (`surface-base`)
- SHOULD reduce color palette (currently 11 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #FFFFFF | rgb(255,255,255) | Page background |
| `surface-raised` | #0F0F0F | rgb(15,15,15) | Cards, modals, raised surfaces |
| `surface-overlay` | #EEEEEF | rgb(238,238,239) | Overlays, tooltips, dropdowns |
| `text-primary` | #B1B1B1 | rgb(177,177,177) | Headings, body text |
| `text-secondary` | #939393 | rgb(147,147,147) | Secondary, muted text |
| `text-tertiary` | #4A4A4A | rgb(74,74,74) | Additional text |
| `border-default` | #DEDEDE | rgb(222,222,222) | Subtle borders, dividers |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `75px` / `700` for primary headings
- MUST use `18px` / `400` for body text
- MUST limit font weights to: bold, regular, medium
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 75px | 700 | #1B1B1B | 1 |
| `text-20px` | Inter | 20px | 500 | #ACACAC | 1 |
| `text-19px` | Inter | 19px | 400 | #7C7C7C | 1 |
| `body` | Inter | 18px | 400 | #B3B3B3 | 1 |
| `body-secondary` | Inter | 18px | 500 | #3A3A3A | 1 |
| `body-secondary` | Inter | 16px | 500 | #AFAFAF | 2 |
| `body-secondary` | Inter | 16px | 500 | #B2B2B2 | 1 |
| `body-secondary` | Inter | 16px | 500 | #B5B5B5 | 1 |
| `body-secondary` | Inter | 15px | 400 | #4D4D4D | 2 |
| `body-secondary` | Inter | 15px | 500 | #B1B1B1 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 17x)

**Font Sizes:** 8px, 11px, 12px, 14px, 15px, 16px, 18px, 19px, 20px, 75px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 2px, 3px, 4px, 5px, 18px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 8px, 21px, 22px, 28px
- SHOULD use 21px+ radius for pill-shaped elements
- MUST use 1px border width consistently
- SHOULD use 21px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 8px, 21px, 22px, 28px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 72px, 61px, 27px, 78px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 850px
- **Header**: height: 49px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #4A4A4A | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#5E6AD2`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#0F0F0F` background
- List items: use `#0F0F0F` background

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
