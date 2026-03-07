---
name: linear-ui-skills
description: Linear's UI design system. Use when building interfaces inspired by Linear's aesthetic - dark mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://linear.app
---

# Linear UI Skills

Opinionated constraints for building Linear-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building dark-mode interfaces
- Creating Linear-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- MUST use dark backgrounds (lightness < 20) for primary surfaces - detected lightness: 4
- MUST use `#080A0A` as page background (`surface-base`)
- SHOULD limit color palette to 10 distinct colors
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #080A0A | rgb(8,10,10) | Page background |
| `surface-raised` | #D2D2D3 | rgb(210,210,211) | Cards, modals, raised surfaces |
| `surface-overlay` | #E3E3E6 | rgb(227,227,230) | Overlays, tooltips, dropdowns |
| `text-primary` | #5C5C5C | rgb(92,92,92) | Headings, body text |
| `text-secondary` | #2D2E30 | rgb(45,46,48) | Secondary, muted text |
| `text-tertiary` | #444749 | rgb(68,71,73) | Additional text |
| `border-default` | #B0B1B1 | rgb(176,177,177) | Subtle borders, dividers |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `60px` / `700` for primary headings
- MUST use `17px` / `400` for body text
- SHOULD reduce font weights (currently 4 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 60px | 700 | #E2E4E3 | 1 |
| `body` | Inter | 17px | 400 | #444749 | 1 |
| `body-secondary` | Inter | 16px | 400 | #5C5C5C | 1 |
| `body-secondary` | Inter | 15px | 500 | #2D2E30 | 1 |
| `text-14px` | Inter | 14px | 400 | #B2B3B3 | 1 |
| `text-13px` | Inter | 13px | 400 | #4C4C4C | 1 |
| `text-13px` | Inter | 13px | 400 | #525355 | 1 |
| `text-12px` | Inter | 12px | 400 | #525456 | 1 |
| `caption` | Inter | 9px | 400 | #545557 | 1 |
| `label` | Inter | 9px | 400 | #565759 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 13x)

**Font Sizes:** 9px, 12px, 13px, 14px, 15px, 16px, 17px, 60px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 5px, 11px, 12px, 13px, 14px, 16px, 19px, 20px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 6px, 8px
- MUST use 1px border width consistently
- SHOULD use 6px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 6px, 8px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 52px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 1013px
- **Header**: height: 63px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #5C5C5C | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#5E6AD2`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#D2D2D3` background
- List items: use `#D2D2D3` background

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
