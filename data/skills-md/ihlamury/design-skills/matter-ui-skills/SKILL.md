---
name: matter-ui-skills
description: Matter's UI design system. Use when building interfaces inspired by Matter's aesthetic - dark mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://hq.getmatter.com
---

# Matter UI Skills

Opinionated constraints for building Matter-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building dark-mode interfaces
- Creating Matter-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- MUST use dark backgrounds (lightness < 20) for primary surfaces - detected lightness: 0
- MUST use `#000000` as page background (`surface-base`)
- MUST use `#5560EC` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 19 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #000000 | rgb(0,0,0) | Page background |
| `surface-raised` | #CFE3F9 | rgb(207,227,249) | Cards, modals, raised surfaces |
| `surface-overlay` | #8DBDF7 | rgb(141,189,247) | Overlays, tooltips, dropdowns |
| `text-primary` | #627EA1 | rgb(98,126,161) | Headings, body text |
| `text-2` | #8C9BAB | rgb(140,155,171) | Additional text |
| `text-secondary` | #888888 | rgb(136,136,136) | Secondary, muted text |
| `border-default` | #D4E5F8 | rgb(212,229,248) | Subtle borders, dividers |
| `accent` | #5560EC | rgb(85,96,236) | Primary actions, links, focus |
| `destructive` | #200D11 | rgb(32,13,17) | Error states, delete actions |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `81px` / `700` for primary headings
- MUST use `35px` / `700` for body text
- SHOULD reduce font weights (currently 6 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 81px | 700 | #F0F0F0 | 1 |
| `body` | Inter | 35px | 700 | #818181 | 1 |
| `text-32px` | Inter | 32px | semi_bold | #747474 | 1 |
| `text-26px` | Inter | 26px | extra_bold | #8C8C8C | 1 |
| `text-24px` | Inter | 24px | 700 | #848484 | 1 |
| `text-21px` | Inter | 21px | semi_bold | #494949 | 1 |
| `text-20px` | Inter | 20px | 500 | #515151 | 1 |
| `text-19px` | Inter | 19px | 400 | #666666 | 1 |
| `text-16px` | Inter | 16px | 400 | #3C3C3C | 1 |
| `text-15px` | Inter | 15px | 400 | #525252 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 32x)

**Font Sizes:** 8px, 9px, 10px, 11px, 12px, 13px, 14px, 15px, 16px, 19px, 20px, 21px, 24px, 26px, 32px, 35px, 81px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 4px, 5px, 6px, 7px, 9px, 10px
- SHOULD use 2px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 0px, 1px, 10px, 15px
- SHOULD limit border widths to: 1px, 2px
- SHOULD use 1px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 0px, 1px, 10px, 15px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 13px, 102px, 38px, 37px, 14px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Header**: height: 58px
- **Main Content**: width: 1920px, height: 1025px
- **Main Content**: width: 1920px, height: 1023px
- **Header**: height: 59px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #8C9BAB | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#5560EC`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#CFE3F9` background
- List items: use `#CFE3F9` background

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
