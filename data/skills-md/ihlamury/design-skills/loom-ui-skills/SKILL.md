---
name: loom-ui-skills
description: Loom's UI design system. Use when building interfaces inspired by Loom's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://loom.com
---

# Loom UI Skills

Opinionated constraints for building Loom-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Loom-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#E4EDFE` as page background (`surface-base`)
- MUST use `#2256C7` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 14 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #E4EDFE | rgb(228,237,254) | Page background |
| `surface-raised` | #FFFFFF | rgb(255,255,255) | Cards, modals, raised surfaces |
| `surface-overlay` | #171718 | rgb(23,23,24) | Overlays, tooltips, dropdowns |
| `text-primary` | #B6B6B7 | rgb(182,182,183) | Headings, body text |
| `text-2` | #363B43 | rgb(54,59,67) | Additional text |
| `text-secondary` | #B1CFEF | rgb(177,207,239) | Secondary, muted text |
| `border-default` | #E8EEF8 | rgb(232,238,248) | Subtle borders, dividers |
| `accent` | #2256C7 | rgb(34,86,199) | Primary actions, links, focus |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `54px` / `700` for primary headings
- MUST use `25px` / `500` for body text
- MUST limit font weights to: medium, bold, regular
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 54px | 700 | #1D1D1F | 1 |
| `body` | Inter | 25px | 500 | #3C3C3C | 1 |
| `text-20px` | Inter | 20px | 500 | #333433 | 1 |
| `text-16px` | Inter | 16px | 400 | #656565 | 1 |
| `text-16px` | Inter | 16px | 400 | #626262 | 1 |
| `text-16px` | Inter | 16px | 400 | #676767 | 1 |
| `text-15px` | Inter | 15px | 400 | #666666 | 1 |
| `caption` | Inter | 13px | 500 | #B6B6B7 | 1 |
| `label` | Inter | 13px | 400 | #4A505C | 1 |
| `label` | Inter | 12px | 400 | #B1CFEF | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 15x)

**Font Sizes:** 11px, 12px, 13px, 15px, 16px, 20px, 25px, 54px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 4px, 5px, 6px, 7px, 9px, 10px, 13px, 14px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 4px, 15px, 18px, 22px, 26px, 28px
- SHOULD use 22px+ radius for pill-shaped elements
- SHOULD limit border widths to: 1px, 2px
- SHOULD use 28px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 4px, 15px, 18px, 22px, 26px, 28px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 137px, 144px, 6px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 1080px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #B6B6B7 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#2256C7`)
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
