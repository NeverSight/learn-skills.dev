---
name: cal-ui-skills
description: Cal's UI design system. Use when building interfaces inspired by Cal's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://cal.com
---

# Cal UI Skills

Opinionated constraints for building Cal-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Cal-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#FDFDFD` as page background (`surface-base`)
- SHOULD reduce color palette (currently 16 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #FDFDFD | rgb(253,253,253) | Page background |
| `surface-raised` | #EDEDED | rgb(237,237,237) | Cards, modals, raised surfaces |
| `surface-overlay` | #1C1C1C | rgb(28,28,28) | Overlays, tooltips, dropdowns |
| `text-primary` | #6B6B6B | rgb(107,107,107) | Headings, body text |
| `text-secondary` | #A1A1A1 | rgb(161,161,161) | Secondary, muted text |
| `text-tertiary` | #404040 | rgb(64,64,64) | Additional text |
| `border-default` | #E5E5E5 | rgb(229,229,229) | Subtle borders, dividers |
| `destructive` | #FCC9C1 | rgb(252,201,193) | Error states, delete actions |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `70px` / `700` for primary headings
- MUST use `16px` / `400` for body text
- SHOULD reduce font weights (currently 5 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 70px | 700 | #2A2A2A | 1 |
| `text-23px` | Inter | 23px | semi_bold | #C1C1C1 | 1 |
| `text-22px` | Inter | 22px | semi_bold | #494949 | 1 |
| `text-21px` | Inter | 21px | 500 | #676767 | 1 |
| `text-21px` | Inter | 21px | semi_bold | #383838 | 1 |
| `text-19px` | Inter | 19px | 500 | #2C2C2C | 1 |
| `text-19px` | Inter | 19px | 500 | #3C3C3C | 1 |
| `text-19px` | Inter | 19px | 500 | #D4D4D4 | 1 |
| `text-18px` | Inter | 18px | 500 | #404040 | 1 |
| `body` | Inter | 16px | 400 | #A4A4A4 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 65x)

**Font Sizes:** 8px, 9px, 10px, 11px, 12px, 13px, 14px, 15px, 16px, 18px, 19px, 21px, 22px, 23px, 70px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 6px, 7px, 9px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 1px, 2px, 3px, 4px, 6px, 7px, 8px, 9px, 10px, 11px
- SHOULD limit border widths to: 1px, 3px
- SHOULD use 3px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 1px, 2px, 3px, 4px, 6px, 7px, 8px, 9px, 10px, 11px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 16px, 8px, 11px, 10px, 52px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1565px, height: 814px
- **Main Content**: width: 1920px, height: 1080px
- **Main Content**: width: 1180px, height: 717px
- **Main Content**: width: 1178px, height: 701px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #6B6B6B | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#5E6AD2`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#EDEDED` background
- List items: use `#EDEDED` background

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
