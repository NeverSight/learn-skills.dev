---
name: brex-ui-skills
description: Brex's UI design system. Use when building interfaces inspired by Brex's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://brex.com
---

# Brex UI Skills

Opinionated constraints for building Brex-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Brex-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#D9D1CF` as page background (`surface-base`)
- MUST use `#00070D` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 13 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #D9D1CF | rgb(217,209,207) | Page background |
| `surface-raised` | #FEFEFD | rgb(254,254,253) | Cards, modals, raised surfaces |
| `surface-overlay` | #FF4206 | rgb(255,66,6) | Overlays, tooltips, dropdowns |
| `text-primary` | #D98C71 | rgb(217,140,113) | Headings, body text |
| `text-secondary` | #F3AB84 | rgb(243,171,132) | Secondary, muted text |
| `text-tertiary` | #949397 | rgb(148,147,151) | Additional text |
| `border-default` | #DFE0E1 | rgb(223,224,225) | Subtle borders, dividers |
| `destructive` | #D98C71 | rgb(217,140,113) | Error states, delete actions |
| `accent` | #00070D | rgb(0,7,13) | Primary actions, links, focus |
| `warning` | #FEFEFD | rgb(254,254,253) | Warning states, cautions |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `68px` / `700` for primary headings
- MUST use `24px` / `400` for body text
- MUST limit font weights to: medium, bold, regular
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 68px | 700 | #242528 | 1 |
| `body` | Inter | 24px | 400 | #7D7E81 | 1 |
| `text-17px` | Inter | 17px | 500 | #3B3A3D | 1 |
| `text-15px` | Inter | 15px | 400 | #5B5B5C | 1 |
| `text-15px` | Inter | 15px | 400 | #545455 | 1 |
| `text-14px` | Inter | 14px | 400 | #D98C71 | 1 |
| `text-14px` | Inter | 14px | 400 | #949397 | 1 |
| `caption` | Inter | 13px | 400 | #F3AB84 | 1 |
| `label` | Inter | 13px | 400 | #F2A47B | 1 |
| `label` | Inter | 12px | 400 | #565656 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 15x)

**Font Sizes:** 11px, 12px, 13px, 14px, 15px, 17px, 24px, 68px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 5px, 60px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 6px, 7px, 15px
- MUST use 1px border width consistently
- SHOULD use 7px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 6px, 7px, 15px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 10px, 74px, 48px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 969px
- **Main Content**: width: 1920px, height: 752px
- **Header**: height: 61px
- **Header**: height: 50px
- **Header**: height: 49px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #F3AB84 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#00070D`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#FEFEFD` background
- List items: use `#FEFEFD` background

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
