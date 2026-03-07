---
name: things-ui-skills
description: Things's UI design system. Use when building interfaces inspired by Things's aesthetic - light mode, Inter font, 8px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://culturedcode.com/things
---

# Things UI Skills

Opinionated constraints for building Things-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Things-inspired design systems
- Implementing UIs with Inter font and 8px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#EEF2F5` as page background (`surface-base`)
- MUST use `#729AE0` for primary actions and focus states (`accent`)
- SHOULD limit color palette to 5 distinct colors
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #EEF2F5 | rgb(238,242,245) | Page background |
| `text-primary` | #729AE0 | rgb(114,154,224) | Headings, body text |
| `text-2` | #5A5E61 | rgb(90,94,97) | Additional text |
| `text-tertiary` | #2F343B | rgb(47,52,59) | Additional text |
| `accent` | #729AE0 | rgb(114,154,224) | Primary actions, links, focus |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `49px` / `700` for primary headings
- MUST use `23px` / `400` for body text
- SHOULD reduce font weights (currently 4 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 49px | 700 | #2F343B | 1 |
| `body` | Inter | 23px | 400 | #5A5E61 | 1 |
| `text-20px` | Inter | 20px | 500 | #729AE0 | 1 |
| `text-19px` | Inter | 19px | semi_bold | #9298A0 | 1 |
| `text-14px` | Inter | 14px | 400 | #9499A1 | 1 |
| `text-14px` | Inter | 14px | 400 | #989CA4 | 1 |
| `caption` | Inter | 11px | 400 | #989DA4 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 7x)

**Font Sizes:** 11px, 14px, 19px, 20px, 23px, 49px

## Spacing

- MUST use 8px grid for spacing
- SHOULD use spacing from scale: 72px
- SHOULD use 72px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 35px, 64px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 1080px
- **Main Content**: width: 1920px, height: 1024px

## Components

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#729AE0`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `surface-raised` background
- List items: use `surface-raised` background

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
