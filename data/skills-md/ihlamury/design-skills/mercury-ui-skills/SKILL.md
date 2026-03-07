---
name: mercury-ui-skills
description: Mercury's UI design system. Use when building interfaces inspired by Mercury's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://mercury.com
---

# Mercury UI Skills

Opinionated constraints for building Mercury-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Mercury-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#000000` as page background (`surface-base`)
- MUST use `#8B9CEC` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 23 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #000000 | rgb(0,0,0) | Page background |
| `surface-raised` | #FFFFFF | rgb(255,255,255) | Cards, modals, raised surfaces |
| `surface-overlay` | #ECEDEE | rgb(236,237,238) | Overlays, tooltips, dropdowns |
| `text-primary` | #C2C2C2 | rgb(194,194,194) | Headings, body text |
| `text-secondary` | #B0B0B0 | rgb(176,176,176) | Secondary, muted text |
| `text-tertiary` | #D0D0D7 | rgb(208,208,215) | Additional text |
| `border-default` | #FDFEFE | rgb(253,254,254) | Subtle borders, dividers |
| `accent` | #8B9CEC | rgb(139,156,236) | Primary actions, links, focus |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `69px` / `700` for primary headings
- MUST use `16px` / `700` for body text
- SHOULD reduce font weights (currently 5 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 69px | 700 | #32312D | 1 |
| `text-26px` | Inter | 26px | 500 | #4C4E4D | 1 |
| `text-25px` | Inter | 25px | 400 | #5C5B5E | 1 |
| `text-21px` | Inter | 21px | 400 | #726F69 | 1 |
| `body` | Inter | 16px | 700 | #BBBCBF | 1 |
| `body-secondary` | Inter | 15px | 400 | #A9A9A9 | 1 |
| `body-secondary` | Inter | 15px | 400 | #A8A8A8 | 1 |
| `body-secondary` | Inter | 15px | 400 | #AAAAAA | 1 |
| `body-secondary` | Inter | 15px | 400 | #C4C6C5 | 1 |
| `body-secondary` | Inter | 15px | 400 | #B1BBF3 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 56x)

**Font Sizes:** 9px, 11px, 12px, 13px, 14px, 15px, 16px, 21px, 25px, 26px, 69px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 2px, 4px, 5px, 6px, 7px, 10px, 11px, 12px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 3px, 4px, 10px, 13px, 16px, 18px, 21px
- SHOULD use 21px+ radius for pill-shaped elements
- SHOULD limit border widths to: 1px, 2px, 5px, 7px
- SHOULD use 13px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 3px, 4px, 10px, 13px, 16px, 18px, 21px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 11px, 8px, 12px, 9px, 13px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 563px
- **Main Content**: width: 1920px, height: 625px
- **Main Content**: width: 1352px, height: 605px
- **Main Content**: width: 1139px, height: 595px
- **Header**: height: 67px

## Components

- MUST use `0px` height for input fields

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #8E9090 | none | - | - |

### Inputs

- Height: `0px`

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#8B9CEC`)
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
