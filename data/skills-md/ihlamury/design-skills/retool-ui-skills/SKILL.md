---
name: retool-ui-skills
description: Retool's UI design system. Use when building interfaces inspired by Retool's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://retool.com
---

# Retool UI Skills

Opinionated constraints for building Retool-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Retool-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#E3E6D7` as page background (`surface-base`)
- MUST use `#80AEF2` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 21 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #E3E6D7 | rgb(227,230,215) | Page background |
| `surface-raised` | #081319 | rgb(8,19,25) | Cards, modals, raised surfaces |
| `surface-overlay` | #3469F5 | rgb(52,105,245) | Overlays, tooltips, dropdowns |
| `text-primary` | #80AEF2 | rgb(128,174,242) | Headings, body text |
| `text-secondary` | #A49369 | rgb(164,147,105) | Secondary, muted text |
| `text-tertiary` | #646560 | rgb(100,101,96) | Additional text |
| `border-default` | #255DF1 | rgb(37,93,241) | Subtle borders, dividers |
| `accent` | #80AEF2 | rgb(128,174,242) | Primary actions, links, focus |
| `warning` | #9B7C4A | rgb(155,124,74) | Warning states, cautions |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `54px` / `700` for primary headings
- MUST use `19px` / `500` for body text
- SHOULD reduce font weights (currently 4 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 54px | 700 | #C4C6BC | 1 |
| `text-45px` | Inter | 45px | 500 | #6E6E6B | 1 |
| `text-45px` | Inter | 45px | 500 | #C2C3BD | 1 |
| `text-38px` | Inter | 38px | 500 | #B5B6AF | 1 |
| `text-38px` | Inter | 38px | 500 | #6C6C69 | 1 |
| `text-36px` | Inter | 36px | 500 | #AFB0A9 | 1 |
| `text-36px` | Inter | 36px | 500 | #767673 | 1 |
| `text-36px` | Inter | 36px | 500 | #CECFC7 | 1 |
| `body` | Inter | 19px | 500 | #BDBEB8 | 1 |
| `body-secondary` | Inter | 18px | 400 | #7F7F7D | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 40x)

**Font Sizes:** 7px, 8px, 9px, 10px, 11px, 12px, 13px, 14px, 15px, 16px, 18px, 19px, 36px, 38px, 45px, 54px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 15px, 24px, 35px
- SHOULD use 2px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 2px, 3px, 4px, 19px, 32px, 99px
- SHOULD use 32px+ radius for pill-shaped elements
- SHOULD limit border widths to: 1px, 4px
- SHOULD use 32px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 2px, 3px, 4px, 19px, 32px, 99px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 8px, 11px, 7px, 6px, 1364px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 900px
- **Main Content**: width: 1307px, height: 661px
- **Main Content**: width: 1364px, height: 702px
- **Header**: height: 88px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #80AEF2 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#80AEF2`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#081319` background
- List items: use `#081319` background

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
