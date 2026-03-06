---
name: awwwards-ui-skills
description: Awwwards's UI design system. Use when building interfaces inspired by Awwwards's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://awwwards.com
---

# Awwwards UI Skills

Opinionated constraints for building Awwwards-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Awwwards-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#E4E4E4` as page background (`surface-base`)
- SHOULD reduce color palette (currently 15 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #E4E4E4 | rgb(228,228,228) | Page background |
| `surface-raised` | #2F2E30 | rgb(47,46,48) | Cards, modals, raised surfaces |
| `surface-overlay` | #191919 | rgb(25,25,25) | Overlays, tooltips, dropdowns |
| `text-primary` | #565656 | rgb(86,86,86) | Headings, body text |
| `text-secondary` | #939393 | rgb(147,147,147) | Secondary, muted text |
| `text-tertiary` | #B5B5B5 | rgb(181,181,181) | Additional text |
| `border-default` | #3A3A3A | rgb(58,58,58) | Subtle borders, dividers |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `127px` / `700` for primary headings
- MUST use `16px` / `500` for body text
- SHOULD reduce font weights (currently 5 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 127px | 700 | #1C1C1C | 1 |
| `text-28px` | Inter | 28px | 700 | #ECEEE4 | 1 |
| `text-18px` | Inter | 18px | 500 | #3C3C3C | 1 |
| `text-17px` | Inter | 17px | semi_bold | #3D3D3D | 1 |
| `body` | Inter | 16px | 500 | #B5B5B5 | 1 |
| `body-secondary` | Inter | 16px | 500 | #B0B3A3 | 1 |
| `body-secondary` | Inter | 15px | 400 | #4A4A4A | 1 |
| `body-secondary` | Inter | 15px | 400 | #4D4D4D | 1 |
| `body-secondary` | Inter | 15px | 400 | #646464 | 1 |
| `body-secondary` | Inter | 14px | 400 | #5C5C5C | 2 |

### Typography Reference

**Font Families:**
- `Inter` (used 31x)

**Font Sizes:** 7px, 8px, 9px, 10px, 11px, 12px, 14px, 15px, 16px, 17px, 18px, 28px, 127px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 6px, 8px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 2px, 3px, 4px, 6px, 7px, 8px, 9px
- MUST use 1px border width consistently
- SHOULD use 7px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 2px, 3px, 4px, 6px, 7px, 8px, 9px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 91px, 58px, 32px, 42px, 88px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 629px
- **Main Content**: width: 1601px, height: 632px

## Components

- MUST use `0px` height for input fields

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #565656 | none | - | - |

### Inputs

- Height: `0px`

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#5E6AD2`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#2F2E30` background
- List items: use `#2F2E30` background

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
