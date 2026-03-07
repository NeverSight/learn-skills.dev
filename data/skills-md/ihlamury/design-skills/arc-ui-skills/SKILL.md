---
name: arc-ui-skills
description: Arc's UI design system. Use when building interfaces inspired by Arc's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://arc.net
---

# Arc UI Skills

Opinionated constraints for building Arc-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Arc-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#E4E4E4` as page background (`surface-base`)
- MUST use `#6FADE2` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 26 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #E4E4E4 | rgb(228,228,228) | Page background |
| `surface-raised` | #1B00B5 | rgb(27,0,181) | Cards, modals, raised surfaces |
| `surface-overlay` | #FEFEFD | rgb(254,254,253) | Overlays, tooltips, dropdowns |
| `text-primary` | #BFAFEA | rgb(191,175,234) | Headings, body text |
| `text-secondary` | #513EA3 | rgb(81,62,163) | Secondary, muted text |
| `text-tertiary` | #E0DCEA | rgb(224,220,234) | Additional text |
| `border-default` | #1902BE | rgb(25,2,190) | Subtle borders, dividers |
| `accent` | #6FADE2 | rgb(111,173,226) | Primary actions, links, focus |
| `warning` | #FEFEFD | rgb(254,254,253) | Warning states, cautions |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `53px` / `700` for primary headings
- MUST use `22px` / `500` for body text
- SHOULD reduce font weights (currently 5 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 53px | 700 | #E4E3EF | 1 |
| `text-36px` | Inter | 36px | 700 | #2D2C2B | 1 |
| `body` | Inter | 22px | 500 | #C7C7C7 | 1 |
| `text-19px` | Inter | 19px | 400 | #666664 | 1 |
| `text-14px` | Inter | 14px | semi_bold | #E0DCEA | 1 |
| `text-13px` | Inter | 13px | 400 | #37556A | 1 |
| `text-13px` | Inter | 13px | 300 | #C0C2C2 | 1 |
| `text-13px` | Inter | 13px | 400 | #AEACF0 | 1 |
| `text-12px` | Inter | 12px | 400 | #BFAFEA | 1 |
| `text-12px` | Inter | 12px | 400 | #513EA3 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 28x)

**Font Sizes:** 5px, 6px, 8px, 9px, 10px, 11px, 12px, 13px, 14px, 19px, 22px, 36px, 53px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 6px, 7px, 10px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 2px, 3px, 4px, 5px, 6px, 7px, 8px, 9px, 21px, 22px
- SHOULD use 21px+ radius for pill-shaped elements
- SHOULD limit border widths to: 1px, 2px
- SHOULD use 7px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 2px, 3px, 4px, 5px, 6px, 7px, 8px, 9px, 21px, 22px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 69px, 11px, 10px, 70px, 15px
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 602px
- **Main Content**: width: 1920px, height: 613px
- **Header**: height: 99px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #BFAFEA | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#6FADE2`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#1B00B5` background
- List items: use `#1B00B5` background

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
