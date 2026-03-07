---
name: gusto-ui-skills
description: Gusto's UI design system. Use when building interfaces inspired by Gusto's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://gusto.com
---

# Gusto UI Skills

Opinionated constraints for building Gusto-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Gusto-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#116D6C` as page background (`surface-base`)
- MUST use `#116D6C` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 23 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #116D6C | rgb(17,109,108) | Page background |
| `surface-raised` | #FFFFFF | rgb(255,255,255) | Cards, modals, raised surfaces |
| `surface-overlay` | #063E82 | rgb(6,62,130) | Overlays, tooltips, dropdowns |
| `text-primary` | #606060 | rgb(96,96,96) | Headings, body text |
| `text-secondary` | #717171 | rgb(113,113,113) | Secondary, muted text |
| `text-tertiary` | #898989 | rgb(137,137,137) | Additional text |
| `border-default` | #E3ECED | rgb(227,236,237) | Subtle borders, dividers |
| `accent` | #116D6C | rgb(17,109,108) | Primary actions, links, focus |
| `destructive` | #DA6966 | rgb(218,105,102) | Error states, delete actions |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `51px` / `extra_bold` for primary headings
- MUST use `15px` / `400` for body text
- SHOULD reduce font weights (currently 6 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 51px | extra_bold | #353636 | 1 |
| `text-35px` | Inter | 35px | 700 | #E0554C | 1 |
| `text-32px` | Inter | 32px | extra_bold | #D62833 | 1 |
| `text-30px` | Inter | 30px | semi_bold | #343434 | 1 |
| `text-28px` | Inter | 28px | extra_bold | #FADAD3 | 1 |
| `text-25px` | Inter | 25px | extra_bold | #2E2E2E | 1 |
| `text-23px` | Inter | 23px | semi_bold | #DA6966 | 1 |
| `text-22px` | Inter | 22px | 500 | #323232 | 1 |
| `text-18px` | Inter | 18px | 500 | #575757 | 1 |
| `text-18px` | Inter | 18px | 400 | #5B677E | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 80x)

**Font Sizes:** 6px, 7px, 8px, 9px, 10px, 11px, 12px, 13px, 14px, 15px, 17px, 18px, 22px, 23px, 25px, 28px, 30px, 32px, 35px, 51px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 6px, 7px, 9px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 4px, 6px, 7px, 9px, 10px, 15px, 16px, 22px, 23px
- SHOULD use 22px+ radius for pill-shaped elements
- SHOULD limit border widths to: 1px, 2px
- SHOULD use 7px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 4px, 6px, 7px, 9px, 10px, 15px, 16px, 22px, 23px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 15px, 24px, 23px, 48px, 11px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 864px
- **Main Content**: width: 1920px, height: 789px
- **Header**: height: 76px
- **Header**: height: 51px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #807F7D | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#116D6C`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#FFFFFF` background
- List items: use `#FFFFFF` background

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
