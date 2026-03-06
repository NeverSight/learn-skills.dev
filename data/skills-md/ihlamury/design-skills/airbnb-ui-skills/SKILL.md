---
name: airbnb-ui-skills
description: Airbnb's UI design system. Use when building interfaces inspired by Airbnb's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://airbnb.com
---

# Airbnb UI Skills

Opinionated constraints for building Airbnb-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Airbnb-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#FEFEFE` as page background (`surface-base`)
- SHOULD reduce color palette (currently 13 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #FEFEFE | rgb(254,254,254) | Page background |
| `surface-raised` | #EEEBE4 | rgb(238,235,228) | Cards, modals, raised surfaces |
| `surface-overlay` | #D5D3D1 | rgb(213,211,209) | Overlays, tooltips, dropdowns |
| `text-primary` | #8F8F8F | rgb(143,143,143) | Headings, body text |
| `text-2` | #5C5955 | rgb(92,89,85) | Additional text |
| `text-secondary` | #686868 | rgb(104,104,104) | Secondary, muted text |
| `border-default` | #E6DECC | rgb(230,222,204) | Subtle borders, dividers |
| `destructive` | #E25275 | rgb(226,82,117) | Error states, delete actions |
| `warning` | #E6DECC | rgb(230,222,204) | Warning states, cautions |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `19px` / `500` for primary headings
- MUST use `15px` / `400` for body text
- MUST limit font weights to: light, regular, medium
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 19px | 500 | #4A4A4A | 1 |
| `heading-2` | Inter | 19px | 500 | #E25275 | 1 |
| `heading-3` | Inter | 15px | 300 | #C3C0BC | 1 |
| `body` | Inter | 15px | 400 | #919191 | 1 |
| `body-secondary` | Inter | 15px | 500 | #494949 | 1 |
| `body-secondary` | Inter | 15px | 500 | #474747 | 1 |
| `body-secondary` | Inter | 14px | 400 | #919191 | 5 |
| `body-secondary` | Inter | 14px | 300 | #919191 | 3 |
| `body-secondary` | Inter | 14px | 300 | #929292 | 3 |
| `body-secondary` | Inter | 14px | 400 | #909090 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 65x)

**Font Sizes:** 6px, 8px, 9px, 10px, 11px, 13px, 14px, 15px, 19px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 5px, 6px, 9px, 10px, 41px
- SHOULD use 2px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 11px, 12px, 13px, 14px, 28px
- SHOULD use 28px+ radius for pill-shaped elements
- MUST use 1px border width consistently
- SHOULD use 11px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 11px, 12px, 13px, 14px, 28px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 249px, 24px, 97px, 28px, 78px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 1080px
- **Main Content**: width: 1920px, height: 879px

## Components

- MUST use `0px` height for input fields

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #5C5955 | none | - | - |

### Inputs

- Height: `0px`

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#5E6AD2`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#EEEBE4` background
- List items: use `#EEEBE4` background

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
