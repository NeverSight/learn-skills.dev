---
name: craft-ui-skills
description: Craft's UI design system. Use when building interfaces inspired by Craft's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://craft.do
---

# Craft UI Skills

Opinionated constraints for building Craft-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Craft-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#F3EFEC` as page background (`surface-base`)
- MUST use `#D0E8F4` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 35 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #F3EFEC | rgb(243,239,236) | Page background |
| `surface-raised` | #E3F2E6 | rgb(227,242,230) | Cards, modals, raised surfaces |
| `surface-overlay` | #FEFCCD | rgb(254,252,205) | Overlays, tooltips, dropdowns |
| `text-primary` | #586588 | rgb(88,101,136) | Headings, body text |
| `text-secondary` | #C1D1C6 | rgb(193,209,198) | Secondary, muted text |
| `text-tertiary` | #7E8E83 | rgb(126,142,131) | Additional text |
| `border-default` | #E3E3E1 | rgb(227,227,225) | Subtle borders, dividers |
| `warning` | #050402 | rgb(5,4,2) | Warning states, cautions |
| `destructive` | #EAA277 | rgb(234,162,119) | Error states, delete actions |
| `success` | #E3F2E6 | rgb(227,242,230) | Success states, confirmations |
| `accent` | #D0E8F4 | rgb(208,232,244) | Primary actions, links, focus |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `75px` / `700` for primary headings
- MUST use `12px` / `400` for body text
- SHOULD reduce font weights (currently 4 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 75px | 700 | #1C282E | 1 |
| `text-20px` | Inter | 20px | 700 | #171B1D | 1 |
| `text-17px` | Inter | 17px | 300 | #C2ADC1 | 1 |
| `text-16px` | Inter | 16px | 500 | #313E45 | 1 |
| `text-15px` | Inter | 15px | 400 | #475964 | 1 |
| `text-14px` | Inter | 14px | 500 | #5B5C5E | 1 |
| `text-14px` | Inter | 14px | 400 | #B4B5B3 | 1 |
| `text-14px` | Inter | 14px | 400 | #3F525D | 1 |
| `text-14px` | Inter | 14px | 400 | #445661 | 1 |
| `text-14px` | Inter | 14px | 400 | #3B4E57 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 51x)

**Font Sizes:** 6px, 7px, 8px, 9px, 10px, 11px, 12px, 13px, 14px, 15px, 16px, 17px, 20px, 75px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 6px, 7px, 8px
- SHOULD use 4px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 3px, 9px, 10px, 13px, 15px, 16px, 18px, 19px, 21px, 22px
- SHOULD use 21px+ radius for pill-shaped elements
- SHOULD limit border widths to: 1px, 2px, 4px, 6px, 7px
- SHOULD use 18px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 3px, 9px, 10px, 13px, 15px, 16px, 18px, 19px, 21px, 22px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 12px, 39px, 13px, 178px, 10px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 1024px
- **Main Content**: width: 1920px, height: 998px
- **Main Content**: width: 1920px, height: 674px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #313E45 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#D0E8F4`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#E3F2E6` background
- List items: use `#E3F2E6` background

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
