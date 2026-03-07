---
name: railway-ui-skills
description: Railway's UI design system. Use when building interfaces inspired by Railway's aesthetic - dark mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://railway.app
---

# Railway UI Skills

Opinionated constraints for building Railway-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building dark-mode interfaces
- Creating Railway-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- MUST use dark backgrounds (lightness < 20) for primary surfaces - detected lightness: 7
- MUST use `#0F0E14` as page background (`surface-base`)
- MUST use `#0B1025` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 19 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #0F0E14 | rgb(15,14,20) | Page background |
| `surface-raised` | #1E1C25 | rgb(30,28,37) | Cards, modals, raised surfaces |
| `surface-overlay` | #0B1025 | rgb(11,16,37) | Overlays, tooltips, dropdowns |
| `text-primary` | #85848A | rgb(133,132,138) | Headings, body text |
| `text-secondary` | #48464F | rgb(72,70,79) | Secondary, muted text |
| `text-tertiary` | #A09FA5 | rgb(160,159,165) | Additional text |
| `border-default` | #15181F | rgb(21,24,31) | Subtle borders, dividers |
| `accent` | #0B1025 | rgb(11,16,37) | Primary actions, links, focus |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `54px` / `extra_bold` for primary headings
- MUST use `11px` / `300` for body text
- SHOULD reduce font weights (currently 4 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 54px | extra_bold | #E9ECED | 1 |
| `text-19px` | Inter | 19px | 400 | #90959E | 1 |
| `text-19px` | Inter | 19px | 500 | #C6C5CA | 1 |
| `text-18px` | Inter | 18px | 500 | #DACEE6 | 1 |
| `text-15px` | Inter | 15px | 400 | #5C3C82 | 1 |
| `text-14px` | Inter | 14px | 400 | #C0C4C7 | 1 |
| `text-14px` | Inter | 14px | 400 | #8C929B | 1 |
| `text-14px` | Inter | 14px | 400 | #A5A4AA | 1 |
| `text-14px` | Inter | 14px | 400 | #8D8C93 | 1 |
| `text-14px` | Inter | 14px | 400 | #95949B | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 74x)

**Font Sizes:** 7px, 8px, 9px, 10px, 11px, 12px, 13px, 14px, 15px, 18px, 19px, 54px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 8px, 12px, 14px
- SHOULD use 2px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 0px, 2px, 3px, 4px, 5px, 6px, 8px, 10px
- SHOULD limit border widths to: 1px, 2px, 6px
- SHOULD use 3px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 0px, 2px, 3px, 4px, 5px, 6px, 8px, 10px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 81px, 8px, 72px, 62px, 708px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 1080px
- **Main Content**: width: 1710px, height: 958px
- **Main Content**: width: 1853px, height: 724px
- **Header**: height: 53px
- **Header**: height: 52px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #2C2B33 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#0B1025`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#1E1C25` background
- List items: use `#1E1C25` background

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
