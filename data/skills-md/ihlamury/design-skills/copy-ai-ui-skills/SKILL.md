---
name: copy-ai-ui-skills
description: Copy Ai's UI design system. Use when building interfaces inspired by Copy Ai's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://copy.ai
---

# Copy Ai UI Skills

Opinionated constraints for building Copy Ai-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Copy Ai-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#FEFEFE` as page background (`surface-base`)
- MUST use `#5227BD` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 18 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #FEFEFE | rgb(254,254,254) | Page background |
| `surface-raised` | #111111 | rgb(17,17,17) | Cards, modals, raised surfaces |
| `surface-overlay` | #541ED7 | rgb(84,30,215) | Overlays, tooltips, dropdowns |
| `text-primary` | #525252 | rgb(82,82,82) | Headings, body text |
| `text-secondary` | #737C83 | rgb(115,124,131) | Secondary, muted text |
| `text-tertiary` | #5F6A72 | rgb(95,106,114) | Additional text |
| `border-default` | #F9FCFC | rgb(249,252,252) | Subtle borders, dividers |
| `accent` | #5227BD | rgb(82,39,189) | Primary actions, links, focus |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `66px` / `700` for primary headings
- MUST use `38px` / `700` for body text
- SHOULD reduce font weights (currently 4 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 66px | 700 | #1D1E1E | 1 |
| `body` | Inter | 38px | 700 | #1D2021 | 1 |
| `text-30px` | Inter | 30px | 400 | #7F868A | 1 |
| `text-30px` | Inter | 30px | 700 | #2E2E2E | 1 |
| `text-25px` | Inter | 25px | semi_bold | #5B686F | 1 |
| `text-24px` | Inter | 24px | 500 | #767E82 | 1 |
| `text-24px` | Inter | 24px | 500 | #636E73 | 1 |
| `text-24px` | Inter | 24px | semi_bold | #5B686F | 1 |
| `text-20px` | Inter | 20px | semi_bold | #5F6A72 | 1 |
| `text-20px` | Inter | 20px | semi_bold | #5B676F | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 33x)

**Font Sizes:** 9px, 12px, 13px, 15px, 16px, 17px, 18px, 19px, 20px, 24px, 25px, 30px, 38px, 66px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 8px, 9px, 14px
- SHOULD use 4px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 33px
- SHOULD use 33px+ radius for pill-shaped elements
- SHOULD limit border widths to: 1px, 2px
- SHOULD use 33px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 33px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 10px, 113px, 8px, 9px, 1400px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 1039px
- **Main Content**: width: 1399px, height: 696px
- **Main Content**: width: 1410px, height: 659px
- **Header**: height: 48px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #BEBEBE | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#5227BD`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#111111` background
- List items: use `#111111` background

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
