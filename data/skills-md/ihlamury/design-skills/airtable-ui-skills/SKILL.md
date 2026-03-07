---
name: airtable-ui-skills
description: Airtable's UI design system. Use when building interfaces inspired by Airtable's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://airtable.com
---

# Airtable UI Skills

Opinionated constraints for building Airtable-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Airtable-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#FDF5EA` as page background (`surface-base`)
- SHOULD limit color palette to 8 distinct colors
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #FDF5EA | rgb(253,245,234) | Page background |
| `surface-raised` | #13151D | rgb(19,21,29) | Cards, modals, raised surfaces |
| `text-primary` | #B5B8BC | rgb(181,184,188) | Headings, body text |
| `text-2` | #666159 | rgb(102,97,89) | Additional text |
| `text-tertiary` | #6B2B66 | rgb(107,43,102) | Additional text |
| `border-default` | #2F2C2F | rgb(47,44,47) | Subtle borders, dividers |
| `warning` | #FDF5EA | rgb(253,245,234) | Warning states, cautions |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `145px` / `700` for primary headings
- MUST use `24px` / `400` for body text
- MUST limit font weights to: medium, regular, bold
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 145px | 700 | #23211E | 1 |
| `body` | Inter | 24px | 400 | #6B2B66 | 1 |
| `text-20px` | Inter | 20px | 500 | #343231 | 1 |
| `text-18px` | Inter | 18px | 400 | #666159 | 1 |
| `text-18px` | Inter | 18px | 400 | #6D2862 | 1 |
| `caption` | Inter | 17px | 400 | #706A62 | 1 |
| `label` | Inter | 15px | 400 | #B5B8BC | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 7x)

**Font Sizes:** 15px, 17px, 18px, 20px, 24px, 145px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 5px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 7px
- MUST use 1px border width consistently
- SHOULD use 7px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 7px

## Layout

- MUST design for 1920px base viewport width
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #B5B8BC | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#5E6AD2`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#13151D` background
- List items: use `#13151D` background

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
