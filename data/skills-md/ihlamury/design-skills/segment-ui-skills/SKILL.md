---
name: segment-ui-skills
description: Segment's UI design system. Use when building interfaces inspired by Segment's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://segment.com
---

# Segment UI Skills

Opinionated constraints for building Segment-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Segment-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#0748D8` as page background (`surface-base`)
- MUST use `#94C2F0` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 14 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #0748D8 | rgb(7,72,216) | Page background |
| `surface-raised` | #000000 | rgb(0,0,0) | Cards, modals, raised surfaces |
| `surface-overlay` | #0F1423 | rgb(15,20,35) | Overlays, tooltips, dropdowns |
| `text-primary` | #2F3239 | rgb(47,50,57) | Headings, body text |
| `text-2` | #424856 | rgb(66,72,86) | Additional text |
| `text-secondary` | #94C2F0 | rgb(148,194,240) | Secondary, muted text |
| `border-default` | #1148C1 | rgb(17,72,193) | Subtle borders, dividers |
| `accent` | #94C2F0 | rgb(148,194,240) | Primary actions, links, focus |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `50px` / `700` for primary headings
- MUST use `31px` / `500` for body text
- SHOULD reduce font weights (currently 5 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 50px | 700 | #E1E4E6 | 1 |
| `heading-2` | Inter | 46px | semi_bold | #2F3239 | 1 |
| `heading-3` | Inter | 46px | 700 | #222730 | 1 |
| `body` | Inter | 31px | 500 | #2D2C41 | 1 |
| `text-21px` | Inter | 21px | 400 | #B1B7C2 | 1 |
| `text-18px` | Inter | 18px | 400 | #54575E | 1 |
| `text-16px` | Inter | 16px | 300 | #87A1D0 | 1 |
| `text-15px` | Inter | 15px | 400 | #5F6165 | 1 |
| `text-15px` | Inter | 15px | 400 | #484A50 | 1 |
| `text-15px` | Inter | 15px | 400 | #52545B | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 20x)

**Font Sizes:** 5px, 10px, 13px, 14px, 15px, 16px, 18px, 21px, 31px, 46px, 50px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 16px, 18px, 78px
- SHOULD use 2px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 6px, 7px
- MUST use 1px border width consistently
- SHOULD use 6px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 6px, 7px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 8px, 248px, 11px, 476px, 96px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 545px
- **Main Content**: width: 1920px, height: 543px
- **Header**: height: 44px
- **Header**: height: 55px
- **Header**: height: 53px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #94C2F0 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#94C2F0`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#000000` background
- List items: use `#000000` background

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
