---
name: webflow-ui-skills
description: Webflow's UI design system. Use when building interfaces inspired by Webflow's aesthetic - dark mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://webflow.com
---

# Webflow UI Skills

Opinionated constraints for building Webflow-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building dark-mode interfaces
- Creating Webflow-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- MUST use dark backgrounds (lightness < 20) for primary surfaces - detected lightness: 8
- MUST use `#151515` as page background (`surface-base`)
- MUST use `#8DB8F2` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 33 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #151515 | rgb(21,21,21) | Page background |
| `surface-raised` | #1252F1 | rgb(18,82,241) | Cards, modals, raised surfaces |
| `surface-overlay` | #FFFFFF | rgb(255,255,255) | Overlays, tooltips, dropdowns |
| `text-primary` | #505050 | rgb(80,80,80) | Headings, body text |
| `text-secondary` | #383838 | rgb(56,56,56) | Secondary, muted text |
| `text-tertiary` | #2A5090 | rgb(42,80,144) | Additional text |
| `border-default` | #0E0E0E | rgb(14,14,14) | Subtle borders, dividers |
| `accent` | #8DB8F2 | rgb(141,184,242) | Primary actions, links, focus |
| `destructive` | #855C37 | rgb(133,92,55) | Error states, delete actions |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `62px` / `700` for primary headings
- MUST use `28px` / `semi_bold` for body text
- SHOULD reduce font weights (currently 5 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 62px | 700 | #171719 | 1 |
| `text-52px` | Inter | 52px | 700 | #969395 | 1 |
| `text-52px` | Inter | 52px | 700 | #958B81 | 1 |
| `body` | Inter | 28px | semi_bold | #82736E | 1 |
| `text-24px` | Inter | 24px | 400 | #999999 | 1 |
| `text-23px` | Inter | 23px | semi_bold | #C8C8C8 | 1 |
| `text-20px` | Inter | 20px | semi_bold | #BEBEBE | 1 |
| `text-20px` | Inter | 20px | 500 | #B4B3B3 | 1 |
| `text-20px` | Inter | 20px | 400 | #4E525C | 1 |
| `text-19px` | Inter | 19px | 500 | #A9A9A9 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 71x)

**Font Sizes:** 3px, 5px, 6px, 7px, 8px, 9px, 10px, 11px, 12px, 13px, 14px, 15px, 16px, 17px, 18px, 19px, 20px, 23px, 24px, 28px, 52px, 62px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 7px, 9px, 13px
- SHOULD use 3px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 1px, 2px, 3px, 18px
- SHOULD limit border widths to: 1px, 2px
- SHOULD use 2px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 1px, 2px, 3px, 18px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 49px, 27px, 107px, 21px, 11px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 620px
- **Main Content**: width: 1693px, height: 623px
- **Header**: height: 64px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #505050 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#8DB8F2`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#1252F1` background
- List items: use `#1252F1` background

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
