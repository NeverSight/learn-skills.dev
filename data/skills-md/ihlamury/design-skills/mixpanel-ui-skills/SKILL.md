---
name: mixpanel-ui-skills
description: Mixpanel's UI design system. Use when building interfaces inspired by Mixpanel's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://mixpanel.com
---

# Mixpanel UI Skills

Opinionated constraints for building Mixpanel-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Mixpanel-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#F4F3F4` as page background (`surface-base`)
- MUST use `#201757` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 32 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #F4F3F4 | rgb(244,243,244) | Page background |
| `surface-raised` | #85292D | rgb(133,41,45) | Cards, modals, raised surfaces |
| `surface-overlay` | #BF4038 | rgb(191,64,56) | Overlays, tooltips, dropdowns |
| `text-primary` | #CFCFCF | rgb(207,207,207) | Headings, body text |
| `text-secondary` | #868686 | rgb(134,134,134) | Secondary, muted text |
| `text-tertiary` | #737373 | rgb(115,115,115) | Additional text |
| `border-default` | #D9D5F2 | rgb(217,213,242) | Subtle borders, dividers |
| `accent` | #201757 | rgb(32,23,87) | Primary actions, links, focus |
| `destructive` | #FAAEA0 | rgb(250,174,160) | Error states, delete actions |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `62px` / `700` for primary headings
- MUST use `15px` / `400` for body text
- SHOULD reduce font weights (currently 5 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 62px | 700 | #2C2B2D | 1 |
| `text-28px` | Inter | 28px | semi_bold | #423C50 | 1 |
| `text-22px` | Inter | 22px | semi_bold | #505050 | 1 |
| `text-22px` | Inter | 22px | semi_bold | #4F4F4F | 1 |
| `text-19px` | Inter | 19px | 500 | #4A4A4C | 1 |
| `text-16px` | Inter | 16px | 400 | #CFCFCF | 1 |
| `text-16px` | Inter | 16px | 400 | #717171 | 1 |
| `body` | Inter | 15px | 400 | #808080 | 1 |
| `body-secondary` | Inter | 15px | semi_bold | #313131 | 1 |
| `body-secondary` | Inter | 15px | 500 | #3E3E3E | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 129x)

**Font Sizes:** 5px, 6px, 7px, 8px, 9px, 10px, 11px, 12px, 13px, 14px, 15px, 16px, 19px, 22px, 28px, 62px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 6px, 7px, 8px
- SHOULD use 3px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 1px, 2px, 3px, 4px, 6px, 7px, 9px, 10px, 13px, 15px, 18px, 19px, 21px, 28px
- SHOULD use 21px+ radius for pill-shaped elements
- SHOULD limit border widths to: 1px, 2px, 3px, 4px
- SHOULD use 3px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 1px, 2px, 3px, 4px, 6px, 7px, 9px, 10px, 13px, 15px, 18px, 19px, 21px, 28px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 15px, 10px, 16px, 18px, 214px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 1080px
- **Main Content**: width: 1150px, height: 562px
- **Header**: height: 56px

## Components

- MUST use `0px` height for input fields

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #C0C0C0 | none | - | - |

### Inputs

- Height: `0px`

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#201757`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#85292D` background
- List items: use `#85292D` background

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
