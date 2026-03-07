---
name: ticktick-ui-skills
description: Ticktick's UI design system. Use when building interfaces inspired by Ticktick's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://ticktick.com
---

# Ticktick UI Skills

Opinionated constraints for building Ticktick-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Ticktick-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#FEFEFE` as page background (`surface-base`)
- MUST use `#6E85D9` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 18 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #FEFEFE | rgb(254,254,254) | Page background |
| `surface-raised` | #D8EDF7 | rgb(216,237,247) | Cards, modals, raised surfaces |
| `surface-overlay` | #3656F8 | rgb(54,86,248) | Overlays, tooltips, dropdowns |
| `text-primary` | #CACACA | rgb(202,202,202) | Headings, body text |
| `text-secondary` | #8D8D8D | rgb(141,141,141) | Secondary, muted text |
| `text-tertiary` | #B7C0DE | rgb(183,192,222) | Additional text |
| `border-default` | #9AAFD4 | rgb(154,175,212) | Subtle borders, dividers |
| `accent` | #6E85D9 | rgb(110,133,217) | Primary actions, links, focus |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `51px` / `700` for primary headings
- MUST use `13px` / `400` for body text
- SHOULD reduce font weights (currently 4 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 51px | 700 | #282B2C | 1 |
| `text-20px` | Inter | 20px | 400 | #7D8CD9 | 1 |
| `text-19px` | Inter | 19px | 500 | #7C7C7C | 1 |
| `text-19px` | Inter | 19px | 400 | #525F66 | 1 |
| `text-18px` | Inter | 18px | 500 | #797979 | 1 |
| `text-16px` | Inter | 16px | 400 | #A0A0A0 | 1 |
| `text-16px` | Inter | 16px | 400 | #999999 | 1 |
| `text-16px` | Inter | 16px | 400 | #6E85D9 | 1 |
| `text-15px` | Inter | 15px | 400 | #9A9A9A | 1 |
| `text-15px` | Inter | 15px | 400 | #9C9C9C | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 62x)

**Font Sizes:** 9px, 10px, 11px, 12px, 13px, 14px, 15px, 16px, 18px, 19px, 20px, 51px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 2px, 4px, 5px, 6px, 9px, 14px, 15px, 20px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 3px, 16px, 22px, 23px, 25px
- SHOULD use 22px+ radius for pill-shaped elements
- MUST use 1px border width consistently
- SHOULD use 3px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 3px, 16px, 22px, 23px, 25px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 16px, 15px, 14px, 13px, 8px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 1080px
- **Main Content**: width: 1920px, height: 1038px
- **Main Content**: width: 1001px, height: 583px
- **Header**: height: 76px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #C3C2D0 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#6E85D9`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#D8EDF7` background
- List items: use `#D8EDF7` background

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
