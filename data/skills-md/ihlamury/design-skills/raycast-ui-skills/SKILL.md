---
name: raycast-ui-skills
description: Raycast's UI design system. Use when building interfaces inspired by Raycast's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://raycast.com
---

# Raycast UI Skills

Opinionated constraints for building Raycast-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Raycast-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#DFDFDF` as page background (`surface-base`)
- SHOULD limit color palette to 9 distinct colors
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #DFDFDF | rgb(223,223,223) | Page background |
| `surface-raised` | #08090B | rgb(8,9,11) | Cards, modals, raised surfaces |
| `text-primary` | #636162 | rgb(99,97,98) | Headings, body text |
| `text-secondary` | #A9A7A8 | rgb(169,167,168) | Secondary, muted text |
| `text-tertiary` | #E99CA8 | rgb(233,156,168) | Additional text |
| `border-default` | #282223 | rgb(40,34,35) | Subtle borders, dividers |
| `destructive` | #E99CA8 | rgb(233,156,168) | Error states, delete actions |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `64px` / `700` for primary headings
- MUST use `12px` / `400` for body text
- MUST limit font weights to: regular, bold, light
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 64px | 700 | #F1DADF | 1 |
| `text-18px` | Inter | 18px | 400 | #E99CA8 | 1 |
| `text-16px` | Inter | 16px | 400 | #A5A5A7 | 1 |
| `text-15px` | Inter | 15px | 400 | #A9A7A8 | 1 |
| `text-14px` | Inter | 14px | 400 | #5C5C5C | 1 |
| `text-14px` | Inter | 14px | 300 | #616163 | 1 |
| `text-14px` | Inter | 14px | 400 | #5E5E60 | 1 |
| `text-14px` | Inter | 14px | 400 | #626264 | 1 |
| `text-14px` | Inter | 14px | 400 | #5D5E60 | 1 |
| `body` | Inter | 12px | 400 | #5E5E5E | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 21x)

**Font Sizes:** 9px, 10px, 11px, 12px, 14px, 15px, 16px, 18px, 64px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 3px, 5px, 6px, 7px, 8px, 9px, 12px, 56px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 4px, 6px, 10px, 13px, 18px
- MUST use 1px border width consistently
- SHOULD use 4px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 4px, 6px, 10px, 13px, 18px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 1px, 14px, 1209px, 65px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1558px, height: 990px
- **Main Content**: width: 1196px, height: 945px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #636162 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#5E6AD2`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#08090B` background
- List items: use `#08090B` background

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
