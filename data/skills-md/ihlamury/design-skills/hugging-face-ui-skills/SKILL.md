---
name: hugging-face-ui-skills
description: Hugging Face's UI design system. Use when building interfaces inspired by Hugging Face's aesthetic - dark mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://huggingface.co
---

# Hugging Face UI Skills

Opinionated constraints for building Hugging Face-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building dark-mode interfaces
- Creating Hugging Face-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- MUST use dark backgrounds (lightness < 20) for primary surfaces - detected lightness: 7
- MUST use `#0D1119` as page background (`surface-base`)
- SHOULD reduce color palette (currently 13 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #0D1119 | rgb(13,17,25) | Page background |
| `surface-raised` | #FFFFFF | rgb(255,255,255) | Cards, modals, raised surfaces |
| `surface-overlay` | #171D2A | rgb(23,29,42) | Overlays, tooltips, dropdowns |
| `text-primary` | #3D3D3D | rgb(61,61,61) | Headings, body text |
| `text-secondary` | #909199 | rgb(144,145,153) | Secondary, muted text |
| `text-tertiary` | #4F4F57 | rgb(79,79,87) | Additional text |
| `border-default` | #0B0F16 | rgb(11,15,22) | Subtle borders, dividers |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `61px` / `700` for primary headings
- MUST use `15px` / `500` for body text
- SHOULD reduce font weights (currently 4 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 61px | 700 | #E5E6E7 | 1 |
| `text-18px` | Inter | 18px | 500 | #303030 | 1 |
| `text-17px` | Inter | 17px | 500 | #3B3B3B | 1 |
| `text-17px` | Inter | 17px | 400 | #A9ACB1 | 1 |
| `text-17px` | Inter | 17px | 400 | #65676F | 1 |
| `body` | Inter | 15px | 500 | #353535 | 1 |
| `body-secondary` | Inter | 14px | 400 | #525252 | 2 |
| `body-secondary` | Inter | 14px | 400 | #3C3C3C | 1 |
| `body-secondary` | Inter | 14px | 500 | #383838 | 1 |
| `body-secondary` | Inter | 14px | 400 | #7F848C | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 106x)

**Font Sizes:** 7px, 8px, 9px, 10px, 11px, 12px, 13px, 14px, 15px, 17px, 18px, 61px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 6px, 7px, 8px
- SHOULD use 2px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 0px, 2px, 3px, 4px, 5px, 6px, 7px, 8px, 9px, 10px, 11px, 12px, 13px, 14px, 15px, 21px
- SHOULD use 21px+ radius for pill-shaped elements
- SHOULD limit border widths to: 1px, 2px, 5px
- SHOULD use 4px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 0px, 2px, 3px, 4px, 5px, 6px, 7px, 8px, 9px, 10px, 11px, 12px, 13px, 14px, 15px, 21px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 12px, 10px, 14px, 9px, 11px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1510px, height: 754px
- **Main Content**: width: 1103px, height: 796px
- **Header**: height: 60px

## Components

- MUST use `0px` height for input fields

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #777B84 | none | - | - |

### Inputs

- Height: `0px`

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#5E6AD2`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#FFFFFF` background
- List items: use `#FFFFFF` background

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
