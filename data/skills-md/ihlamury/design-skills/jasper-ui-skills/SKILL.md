---
name: jasper-ui-skills
description: Jasper's UI design system. Use when building interfaces inspired by Jasper's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://jasper.ai
---

# Jasper UI Skills

Opinionated constraints for building Jasper-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Jasper-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#F5261E` as page background (`surface-base`)
- MUST use `#6899D0` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 13 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #F5261E | rgb(245,38,30) | Page background |
| `surface-raised` | #FFFFFF | rgb(255,255,255) | Cards, modals, raised surfaces |
| `surface-overlay` | #EEEFEE | rgb(238,239,238) | Overlays, tooltips, dropdowns |
| `text-primary` | #6899D0 | rgb(104,153,208) | Headings, body text |
| `text-secondary` | #69B0F9 | rgb(105,176,249) | Secondary, muted text |
| `text-tertiary` | #282945 | rgb(40,41,69) | Additional text |
| `border-default` | #E8E3F4 | rgb(232,227,244) | Subtle borders, dividers |
| `accent` | #6899D0 | rgb(104,153,208) | Primary actions, links, focus |
| `destructive` | #F5261E | rgb(245,38,30) | Error states, delete actions |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `91px` / `700` for primary headings
- MUST use `40px` / `700` for body text
- MUST limit font weights to: regular, medium, bold
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 91px | 700 | #69B0F9 | 1 |
| `text-79px` | Inter | 79px | 700 | #191B3D | 1 |
| `body` | Inter | 40px | 700 | #282945 | 1 |
| `text-37px` | Inter | 37px | 700 | #E24843 | 1 |
| `text-23px` | Inter | 23px | 400 | #4E4F61 | 1 |
| `text-17px` | Inter | 17px | 500 | #6899D0 | 1 |
| `text-16px` | Inter | 16px | 700 | #F9A79D | 1 |
| `text-15px` | Inter | 15px | 400 | #F2A496 | 1 |
| `text-14px` | Inter | 14px | 400 | #F2A095 | 1 |
| `text-14px` | Inter | 14px | 400 | #424253 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 20x)

**Font Sizes:** 10px, 11px, 12px, 13px, 14px, 15px, 16px, 17px, 23px, 37px, 40px, 79px, 91px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 6px, 8px, 9px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 4px
- MUST use 1px border width consistently
- SHOULD use 4px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 4px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 141px, 91px, 101px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 1001px
- **Main Content**: width: 1920px, height: 1037px

## Components

- MUST use `0px` height for input fields

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #282945 | none | - | - |

### Inputs

- Height: `0px`

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#6899D0`)
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
