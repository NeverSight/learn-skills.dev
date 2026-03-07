---
name: stripe-ui-skills
description: Stripe's UI design system. Use when building interfaces inspired by Stripe's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://stripe.com
---

# Stripe UI Skills

Opinionated constraints for building Stripe-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Stripe-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#F2F6F9` as page background (`surface-base`)
- MUST use `#517BDF` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 30 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #F2F6F9 | rgb(242,246,249) | Page background |
| `surface-raised` | #071A34 | rgb(7,26,52) | Cards, modals, raised surfaces |
| `text-primary` | #9DA1A9 | rgb(157,161,169) | Headings, body text |
| `text-secondary` | #B1BCC7 | rgb(177,188,199) | Secondary, muted text |
| `text-tertiary` | #737883 | rgb(115,120,131) | Additional text |
| `border-default` | #131E2B | rgb(19,30,43) | Subtle borders, dividers |
| `success` | #75B88A | rgb(117,184,138) | Success states, confirmations |
| `accent` | #517BDF | rgb(81,123,223) | Primary actions, links, focus |
| `warning` | #FAE6C2 | rgb(250,230,194) | Warning states, cautions |
| `destructive` | #D29E79 | rgb(210,158,121) | Error states, delete actions |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `53px` / `700` for primary headings
- MUST use `28px` / `semi_bold` for body text
- SHOULD reduce font weights (currently 5 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 53px | 700 | #18105B | 1 |
| `body` | Inter | 28px | semi_bold | #242424 | 1 |
| `body-secondary` | Inter | 27px | semi_bold | #2D2D2D | 1 |
| `body-secondary` | Inter | 26px | semi_bold | #517BDF | 1 |
| `text-24px` | Inter | 24px | semi_bold | #EBD6F3 | 1 |
| `text-18px` | Inter | 18px | 500 | #E76874 | 1 |
| `text-18px` | Inter | 18px | semi_bold | #2D2D2D | 1 |
| `text-18px` | Inter | 18px | semi_bold | #3E3D3D | 1 |
| `text-16px` | Inter | 16px | 400 | #F6CFB7 | 1 |
| `text-15px` | Inter | 15px | 400 | #626870 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 62x)

**Font Sizes:** 5px, 6px, 7px, 8px, 9px, 10px, 11px, 12px, 13px, 14px, 15px, 16px, 18px, 24px, 26px, 27px, 28px, 53px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 11px, 12px, 13px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 3px, 4px, 7px, 15px, 22px, 33px, 35px
- SHOULD use 22px+ radius for pill-shaped elements
- SHOULD limit border widths to: 1px, 2px, 3px
- SHOULD use 22px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 3px, 4px, 7px, 15px, 22px, 33px, 35px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 10px, 227px, 7px, 30px, 17px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 1080px
- **Main Content**: width: 1920px, height: 1045px
- **Header**: height: 69px

## Components

- MUST use `0px` height for input fields

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #737883 | none | - | - |

### Inputs

- Height: `0px`

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#517BDF`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#071A34` background
- List items: use `#071A34` background

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
