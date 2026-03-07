---
name: pitch-ui-skills
description: Pitch's UI design system. Use when building interfaces inspired by Pitch's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://pitch.com
---

# Pitch UI Skills

Opinionated constraints for building Pitch-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Pitch-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#000000` as page background (`surface-base`)
- MUST use `#5836F6` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 28 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #000000 | rgb(0,0,0) | Page background |
| `surface-raised` | #FDFDFD | rgb(253,253,253) | Cards, modals, raised surfaces |
| `surface-overlay` | #5836F6 | rgb(88,54,246) | Overlays, tooltips, dropdowns |
| `text-primary` | #7D7D7D | rgb(125,125,125) | Headings, body text |
| `text-secondary` | #929293 | rgb(146,146,147) | Secondary, muted text |
| `text-tertiary` | #868856 | rgb(134,136,86) | Additional text |
| `border-default` | #F3F3F3 | rgb(243,243,243) | Subtle borders, dividers |
| `accent` | #5836F6 | rgb(88,54,246) | Primary actions, links, focus |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `68px` / `700` for primary headings
- MUST use `26px` / `semi_bold` for body text
- SHOULD reduce font weights (currently 5 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 68px | 700 | #F5EEFA | 1 |
| `body` | Inter | 26px | semi_bold | #E4D1F9 | 1 |
| `text-23px` | Inter | 23px | 400 | #D8B1F7 | 1 |
| `text-19px` | Inter | 19px | 300 | #B47CF7 | 1 |
| `text-18px` | Inter | 18px | 500 | #3D3F3B | 1 |
| `text-18px` | Inter | 18px | 400 | #BE84F8 | 1 |
| `text-16px` | Inter | 16px | 400 | #8768D8 | 1 |
| `text-16px` | Inter | 16px | 400 | #8768D4 | 1 |
| `text-16px` | Inter | 16px | 400 | #E2C5F7 | 1 |
| `text-15px` | Inter | 15px | 400 | #BB82F9 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 39x)

**Font Sizes:** 8px, 9px, 10px, 11px, 12px, 13px, 14px, 15px, 16px, 18px, 19px, 23px, 26px, 68px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 7px, 8px, 9px
- SHOULD use 4px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 3px, 4px, 6px, 7px, 8px
- SHOULD limit border widths to: 1px, 2px, 3px
- SHOULD use 6px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 3px, 4px, 6px, 7px, 8px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 14px, 20px, 17px, 19px, 9px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 1038px
- **Main Content**: width: 1920px, height: 798px
- **Header**: height: 39px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #868856 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#5836F6`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#FDFDFD` background
- List items: use `#FDFDFD` background

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
