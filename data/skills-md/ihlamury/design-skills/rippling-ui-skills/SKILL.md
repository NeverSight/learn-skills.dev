---
name: rippling-ui-skills
description: Rippling's UI design system. Use when building interfaces inspired by Rippling's aesthetic - dark mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://rippling.com
---

# Rippling UI Skills

Opinionated constraints for building Rippling-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building dark-mode interfaces
- Creating Rippling-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- MUST use dark backgrounds (lightness < 20) for primary surfaces - detected lightness: 0
- MUST use `#000000` as page background (`surface-base`)
- MUST use `#FDF6FD` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 13 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #000000 | rgb(0,0,0) | Page background |
| `surface-raised` | #FD9717 | rgb(253,151,23) | Cards, modals, raised surfaces |
| `surface-overlay` | #FEFEFE | rgb(254,254,254) | Overlays, tooltips, dropdowns |
| `text-primary` | #8D8884 | rgb(141,136,132) | Headings, body text |
| `text-secondary` | #23201F | rgb(35,32,31) | Secondary, muted text |
| `text-tertiary` | #713C12 | rgb(113,60,18) | Additional text |
| `border-default` | #F9E2C1 | rgb(249,226,193) | Subtle borders, dividers |
| `accent` | #FDF6FD | rgb(253,246,253) | Primary actions, links, focus |
| `destructive` | #713C12 | rgb(113,60,18) | Error states, delete actions |
| `warning` | #FD9717 | rgb(253,151,23) | Warning states, cautions |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `43px` / `extra_bold` for primary headings
- MUST use `16px` / `400` for body text
- SHOULD reduce font weights (currently 5 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 43px | extra_bold | #E6DAE8 | 1 |
| `heading-2` | Inter | 39px | 700 | #23201F | 1 |
| `body` | Inter | 16px | 400 | #8D8884 | 1 |
| `body-secondary` | Inter | 16px | 400 | #93619F | 1 |
| `body-secondary` | Inter | 14px | 400 | #965D9D | 1 |
| `body-secondary` | Inter | 14px | 400 | #9563A1 | 1 |
| `body-secondary` | Inter | 14px | 400 | #CBA8CF | 1 |
| `body-secondary` | Inter | 14px | 400 | #C9A9CD | 1 |
| `body-secondary` | Inter | 14px | 400 | #C8ABCD | 1 |
| `body-secondary` | Inter | 14px | 400 | #D2AED3 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 27x)

**Font Sizes:** 10px, 11px, 12px, 13px, 14px, 16px, 39px, 43px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 2px, 3px, 5px, 15px, 71px
- SHOULD use 2px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- SHOULD limit border widths to: 1px, 5px
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 14px, 8px, 22px, 506px, 24px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 788px
- **Main Content**: width: 1920px, height: 717px
- **Header**: height: 70px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #713C12 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#FDF6FD`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#FD9717` background
- List items: use `#FD9717` background

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
