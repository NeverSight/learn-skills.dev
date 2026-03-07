---
name: ramp-ui-skills
description: Ramp's UI design system. Use when building interfaces inspired by Ramp's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://ramp.com
---

# Ramp UI Skills

Opinionated constraints for building Ramp-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Ramp-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#FFFFFF` as page background (`surface-base`)
- MUST use `#EBF123` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 14 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #FFFFFF | rgb(255,255,255) | Page background |
| `surface-raised` | #DDF21A | rgb(221,242,26) | Cards, modals, raised surfaces |
| `surface-overlay` | #5A544C | rgb(90,84,76) | Overlays, tooltips, dropdowns |
| `text-primary` | #B8B8B8 | rgb(184,184,184) | Headings, body text |
| `text-secondary` | #8B8B8B | rgb(139,139,139) | Secondary, muted text |
| `text-tertiary` | #A7A7A7 | rgb(167,167,167) | Additional text |
| `border-default` | #EAF380 | rgb(234,243,128) | Subtle borders, dividers |
| `accent` | #EBF123 | rgb(235,241,35) | Primary actions, links, focus |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `61px` / `700` for primary headings
- MUST use `19px` / `500` for body text
- SHOULD reduce font weights (currently 6 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 61px | 700 | #DDDCDA | 1 |
| `heading-2` | Inter | 58px | extra_bold | #EDEDEA | 1 |
| `body` | Inter | 19px | 500 | #A9A9A9 | 1 |
| `body-secondary` | Inter | 17px | semi_bold | #A4A4A4 | 1 |
| `body-secondary` | Inter | 17px | 500 | #ACACAC | 1 |
| `body-secondary` | Inter | 17px | 400 | #6D6E6D | 1 |
| `text-16px` | Inter | 16px | semi_bold | #9D9D9D | 1 |
| `text-16px` | Inter | 16px | 500 | #B4B4B4 | 1 |
| `text-16px` | Inter | 16px | 400 | #B4B4B4 | 1 |
| `text-16px` | Inter | 16px | 400 | #ACACAC | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 33x)

**Font Sizes:** 10px, 11px, 12px, 13px, 14px, 15px, 16px, 17px, 19px, 58px, 61px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 3px, 4px, 5px, 8px, 38px, 65px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 4px, 5px
- SHOULD limit border widths to: 1px, 3px
- SHOULD use 4px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 4px, 5px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 20px, 24px, 54px, 75px, 28px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Header**: height: 50px
- **Main Content**: width: 1920px, height: 871px
- **Main Content**: width: 1920px, height: 872px
- **Header**: height: 39px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #51590E | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#EBF123`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#DDF21A` background
- List items: use `#DDF21A` background

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
