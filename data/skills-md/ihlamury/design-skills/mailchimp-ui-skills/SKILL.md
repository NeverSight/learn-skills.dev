---
name: mailchimp-ui-skills
description: Mailchimp's UI design system. Use when building interfaces inspired by Mailchimp's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://mailchimp.com
---

# Mailchimp UI Skills

Opinionated constraints for building Mailchimp-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Mailchimp-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#000000` as page background (`surface-base`)
- MUST use `#2E114B` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 35 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #000000 | rgb(0,0,0) | Page background |
| `surface-raised` | #191610 | rgb(25,22,16) | Cards, modals, raised surfaces |
| `surface-overlay` | #F2F2F2 | rgb(242,242,242) | Overlays, tooltips, dropdowns |
| `text-primary` | #1A1A1A | rgb(26,26,26) | Headings, body text |
| `text-2` | #4D4D4D | rgb(77,77,77) | Additional text |
| `text-secondary` | #A7A7A7 | rgb(167,167,167) | Secondary, muted text |
| `border-default` | #F7F7F7 | rgb(247,247,247) | Subtle borders, dividers |
| `warning` | #FDDB17 | rgb(253,219,23) | Warning states, cautions |
| `accent` | #2E114B | rgb(46,17,75) | Primary actions, links, focus |
| `success` | #72DF58 | rgb(114,223,88) | Success states, confirmations |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `53px` / `extra_bold` for primary headings
- MUST use `31px` / `semi_bold` for body text
- SHOULD reduce font weights (currently 6 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 53px | extra_bold | #34332F | 1 |
| `text-40px` | Inter | 40px | semi_bold | #D9D7D3 | 1 |
| `text-36px` | Inter | 36px | extra_bold | #1A1A1A | 1 |
| `body` | Inter | 31px | semi_bold | #3E3E3E | 1 |
| `text-24px` | Inter | 24px | 500 | #898989 | 1 |
| `text-22px` | Inter | 22px | 400 | #42423F | 1 |
| `text-20px` | Inter | 20px | 500 | #3F3F3F | 1 |
| `text-18px` | Inter | 18px | 500 | #252525 | 1 |
| `text-18px` | Inter | 18px | 700 | #E4DCE8 | 1 |
| `text-18px` | Inter | 18px | 500 | #BFBFBF | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 55x)

**Font Sizes:** 5px, 6px, 7px, 8px, 9px, 10px, 11px, 12px, 13px, 14px, 15px, 17px, 18px, 20px, 22px, 24px, 31px, 36px, 40px, 53px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 6px, 11px, 13px
- SHOULD use 2px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 0px, 1px, 2px, 3px, 4px, 5px, 6px, 7px, 9px, 22px, 25px
- SHOULD use 22px+ radius for pill-shaped elements
- SHOULD limit border widths to: 1px, 2px
- SHOULD use 1px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 0px, 1px, 2px, 3px, 4px, 5px, 6px, 7px, 9px, 22px, 25px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 10px, 12px, 16px, 11px, 27px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 607px
- **Header**: height: 30px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #A7A7A7 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#2E114B`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#191610` background
- List items: use `#191610` background

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
