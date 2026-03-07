---
name: n26-ui-skills
description: N26's UI design system. Use when building interfaces inspired by N26's aesthetic - dark mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://n26.com
---

# N26 UI Skills

Opinionated constraints for building N26-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building dark-mode interfaces
- Creating N26-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- MUST use dark backgrounds (lightness < 20) for primary surfaces - detected lightness: 0
- MUST use `#000000` as page background (`surface-base`)
- MUST use `#116F64` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 18 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #000000 | rgb(0,0,0) | Page background |
| `surface-raised` | #929493 | rgb(146,148,147) | Cards, modals, raised surfaces |
| `surface-overlay` | #E0E0E0 | rgb(224,224,224) | Overlays, tooltips, dropdowns |
| `text-primary` | #555555 | rgb(85,85,85) | Headings, body text |
| `text-secondary` | #436960 | rgb(67,105,96) | Secondary, muted text |
| `text-tertiary` | #588378 | rgb(88,131,120) | Additional text |
| `border-default` | #D3D3D3 | rgb(211,211,211) | Subtle borders, dividers |
| `accent` | #116F64 | rgb(17,111,100) | Primary actions, links, focus |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `46px` / `extra_bold` for primary headings
- MUST use `27px` / `500` for body text
- SHOULD reduce font weights (currently 4 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 46px | extra_bold | #D9DBD7 | 1 |
| `text-32px` | Inter | 32px | 500 | #393939 | 1 |
| `body` | Inter | 27px | 500 | #A09D98 | 1 |
| `text-23px` | Inter | 23px | 500 | #545454 | 1 |
| `text-14px` | Inter | 14px | 400 | #5A8C83 | 1 |
| `text-13px` | Inter | 13px | 400 | #616161 | 1 |
| `text-13px` | Inter | 13px | 400 | #595959 | 1 |
| `text-12px` | Inter | 12px | 300 | #7C7C7C | 1 |
| `text-12px` | Inter | 12px | 400 | #9FD4D0 | 1 |
| `text-11px` | Inter | 11px | 400 | #555555 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 36x)

**Font Sizes:** 7px, 8px, 9px, 10px, 11px, 12px, 13px, 14px, 23px, 27px, 32px, 46px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 2px, 3px, 5px, 6px, 7px, 8px, 25px, 35px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 1px, 3px, 5px
- MUST use 1px border width consistently
- SHOULD use 5px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 1px, 3px, 5px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 35px, 41px, 54px, 15px, 14px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Header**: height: 72px
- **Main Content**: width: 1920px, height: 1009px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #436960 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#116F64`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#929493` background
- List items: use `#929493` background

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
