---
name: beehiiv-ui-skills
description: Beehiiv's UI design system. Use when building interfaces inspired by Beehiiv's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://beehiiv.com
---

# Beehiiv UI Skills

Opinionated constraints for building Beehiiv-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Beehiiv-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#221FAB` as page background (`surface-base`)
- MUST use `#221FAB` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 19 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #221FAB | rgb(34,31,171) | Page background |
| `surface-raised` | #070512 | rgb(7,5,18) | Cards, modals, raised surfaces |
| `text-primary` | #B6B8E7 | rgb(182,184,231) | Headings, body text |
| `text-secondary` | #B9B7BF | rgb(185,183,191) | Secondary, muted text |
| `text-tertiary` | #626076 | rgb(98,96,118) | Additional text |
| `border-default` | #252494 | rgb(37,36,148) | Subtle borders, dividers |
| `accent` | #221FAB | rgb(34,31,171) | Primary actions, links, focus |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `51px` / `700` for primary headings
- MUST use `12px` / `400` for body text
- SHOULD reduce font weights (currently 5 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 51px | 700 | #EF40B0 | 1 |
| `heading-2` | Inter | 51px | 700 | #F7F7F8 | 1 |
| `heading-3` | Inter | 51px | 700 | #F5F5F6 | 1 |
| `text-41px` | Inter | 41px | 400 | #B8B7BE | 1 |
| `text-34px` | Inter | 34px | 700 | #F4F4F5 | 1 |
| `text-26px` | Inter | 26px | semi_bold | #CDCCD1 | 1 |
| `text-23px` | Inter | 23px | semi_bold | #9B99A5 | 1 |
| `text-23px` | Inter | 23px | 500 | #CAC9D0 | 1 |
| `text-23px` | Inter | 23px | 700 | #D8D7DB | 1 |
| `text-23px` | Inter | 23px | semi_bold | #D1D0D5 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 61x)

**Font Sizes:** 5px, 8px, 9px, 10px, 11px, 12px, 13px, 14px, 15px, 16px, 17px, 18px, 19px, 20px, 21px, 22px, 23px, 26px, 34px, 41px, 51px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 4px, 5px, 15px, 21px, 23px, 53px, 56px, 79px
- SHOULD use 4px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 3px
- SHOULD limit border widths to: 1px, 2px
- SHOULD use 3px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 3px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 13px, 14px, 26px, 31px, 65px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 999px
- **Header**: height: 78px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #B6B8E7 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#221FAB`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#070512` background
- List items: use `#070512` background

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
