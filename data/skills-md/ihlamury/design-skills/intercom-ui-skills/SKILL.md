---
name: intercom-ui-skills
description: Intercom's UI design system. Use when building interfaces inspired by Intercom's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://intercom.com
---

# Intercom UI Skills

Opinionated constraints for building Intercom-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Intercom-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#FEFEFE` as page background (`surface-base`)
- MUST use `#4F3FE6` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 19 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #FEFEFE | rgb(254,254,254) | Page background |
| `surface-raised` | #110D0C | rgb(17,13,12) | Cards, modals, raised surfaces |
| `surface-overlay` | #4F3FE6 | rgb(79,63,230) | Overlays, tooltips, dropdowns |
| `text-primary` | #8492A8 | rgb(132,146,168) | Headings, body text |
| `text-secondary` | #ABAAAB | rgb(171,170,171) | Secondary, muted text |
| `text-tertiary` | #939393 | rgb(147,147,147) | Additional text |
| `border-default` | #EAEBE7 | rgb(234,235,231) | Subtle borders, dividers |
| `accent` | #4F3FE6 | rgb(79,63,230) | Primary actions, links, focus |
| `success` | #278019 | rgb(39,128,25) | Success states, confirmations |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `46px` / `extra_bold` for primary headings
- MUST use `14px` / `400` for body text
- SHOULD reduce font weights (currently 6 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 46px | extra_bold | #E1E0DF | 1 |
| `text-26px` | Inter | 26px | semi_bold | #DFE0E2 | 1 |
| `text-24px` | Inter | 24px | semi_bold | #E7E6E5 | 1 |
| `text-18px` | Inter | 18px | 400 | #848A92 | 1 |
| `text-16px` | Inter | 16px | 400 | #A29E9D | 1 |
| `text-16px` | Inter | 16px | 400 | #827F7F | 1 |
| `text-15px` | Inter | 15px | 400 | #BABDC3 | 1 |
| `text-15px` | Inter | 15px | 400 | #9B9BA1 | 1 |
| `text-15px` | Inter | 15px | 400 | #818181 | 1 |
| `text-15px` | Inter | 15px | 400 | #8F87E8 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 72x)

**Font Sizes:** 6px, 7px, 8px, 9px, 10px, 11px, 12px, 13px, 14px, 15px, 16px, 18px, 24px, 26px, 46px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 6px, 7px, 8px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 3px, 4px, 6px, 7px, 9px, 10px, 13px, 15px, 16px, 18px, 19px
- SHOULD limit border widths to: 1px, 2px, 3px
- SHOULD use 6px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 3px, 4px, 6px, 7px, 9px, 10px, 13px, 15px, 16px, 18px, 19px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 9px, 8px, 6px, 4px, 20px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Header**: height: 42px
- **Header**: height: 88px
- **Header**: height: 53px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #8492A8 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#4F3FE6`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#110D0C` background
- List items: use `#110D0C` background

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
