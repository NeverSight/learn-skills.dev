---
name: vercel-ui-skills
description: Vercel's UI design system. Use when building interfaces inspired by Vercel's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://vercel.com
---

# Vercel UI Skills

Opinionated constraints for building Vercel-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Vercel-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#F9F9F9` as page background (`surface-base`)
- MUST use `#000001` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 12 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #F9F9F9 | rgb(249,249,249) | Page background |
| `surface-raised` | #111111 | rgb(17,17,17) | Cards, modals, raised surfaces |
| `surface-overlay` | #000001 | rgb(0,0,1) | Overlays, tooltips, dropdowns |
| `text-primary` | #797979 | rgb(121,121,121) | Headings, body text |
| `text-secondary` | #929292 | rgb(146,146,146) | Secondary, muted text |
| `text-tertiary` | #1B1B1B | rgb(27,27,27) | Additional text |
| `border-default` | #C8CDD1 | rgb(200,205,209) | Subtle borders, dividers |
| `accent` | #000001 | rgb(0,0,1) | Primary actions, links, focus |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `44px` / `extra_bold` for primary headings
- MUST use `29px` / `700` for body text
- SHOULD reduce font weights (currently 5 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 44px | extra_bold | #383838 | 1 |
| `body` | Inter | 29px | 700 | #1B1B1B | 1 |
| `body-secondary` | Inter | 28px | 500 | #717171 | 1 |
| `text-25px` | Inter | 25px | 500 | #828282 | 1 |
| `text-24px` | Inter | 24px | 500 | #797979 | 1 |
| `text-24px` | Inter | 24px | 700 | #1E1E1E | 1 |
| `text-23px` | Inter | 23px | 400 | #6C6C6C | 1 |
| `text-20px` | Inter | 20px | 500 | #262626 | 1 |
| `text-18px` | Inter | 18px | 400 | #797979 | 1 |
| `text-18px` | Inter | 18px | 500 | #373737 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 21x)

**Font Sizes:** 10px, 12px, 13px, 14px, 15px, 18px, 20px, 23px, 24px, 25px, 28px, 29px, 44px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 4px, 5px, 6px, 10px, 25px, 54px, 59px, 92px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 5px, 6px, 7px, 22px, 23px
- SHOULD use 22px+ radius for pill-shaped elements
- SHOULD limit border widths to: 1px, 3px
- SHOULD use 23px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 5px, 6px, 7px, 22px, 23px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 8px, 181px, 66px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 1080px
- **Main Content**: width: 1511px, height: 790px
- **Main Content**: width: 1098px, height: 735px
- **Header**: height: 59px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #545454 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#000001`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#111111` background
- List items: use `#111111` background

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
