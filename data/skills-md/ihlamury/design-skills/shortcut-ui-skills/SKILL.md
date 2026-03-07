---
name: shortcut-ui-skills
description: Shortcut's UI design system. Use when building interfaces inspired by Shortcut's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://shortcut.com
---

# Shortcut UI Skills

Opinionated constraints for building Shortcut-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Shortcut-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#FFFFFF` as page background (`surface-base`)
- MUST use `#3831BF` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 26 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #FFFFFF | rgb(255,255,255) | Page background |
| `surface-raised` | #EBECF0 | rgb(235,236,240) | Cards, modals, raised surfaces |
| `surface-overlay` | #D7EAF5 | rgb(215,234,245) | Overlays, tooltips, dropdowns |
| `text-primary` | #949494 | rgb(148,148,148) | Headings, body text |
| `text-2` | #545454 | rgb(84,84,84) | Additional text |
| `text-secondary` | #A0A1A6 | rgb(160,161,166) | Secondary, muted text |
| `border-default` | #E3E0D5 | rgb(227,224,213) | Subtle borders, dividers |
| `warning` | #523F1D | rgb(82,63,29) | Warning states, cautions |
| `accent` | #3831BF | rgb(56,49,191) | Primary actions, links, focus |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `50px` / `700` for primary headings
- MUST use `21px` / `400` for body text
- SHOULD reduce font weights (currently 5 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 50px | 700 | #433CB7 | 1 |
| `heading-2` | Inter | 50px | 700 | #121212 | 1 |
| `text-25px` | Inter | 25px | semi_bold | #1F1F1F | 1 |
| `body` | Inter | 21px | 400 | #747379 | 1 |
| `body-secondary` | Inter | 20px | 400 | #949494 | 1 |
| `body-secondary` | Inter | 20px | 400 | #999999 | 1 |
| `body-secondary` | Inter | 19px | 400 | #919191 | 2 |
| `body-secondary` | Inter | 19px | 400 | #8E8E8E | 1 |
| `body-secondary` | Inter | 18px | 400 | #979797 | 1 |
| `body-secondary` | Inter | 18px | 400 | #949494 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 62x)

**Font Sizes:** 6px, 8px, 9px, 10px, 11px, 12px, 13px, 14px, 15px, 16px, 17px, 18px, 19px, 20px, 21px, 25px, 50px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 6px, 8px, 9px
- SHOULD use 2px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 1px, 2px, 3px, 4px, 6px, 7px, 21px
- SHOULD use 21px+ radius for pill-shaped elements
- SHOULD limit border widths to: 1px, 2px, 3px
- SHOULD use 3px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 1px, 2px, 3px, 4px, 6px, 7px, 21px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 16px, 9px, 10px, 15px, 185px
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1496px, height: 589px
- **Main Content**: width: 1491px, height: 556px
- **Main Content**: width: 1853px, height: 1053px

## Components

- MUST use `0px` height for input fields

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #76858F | none | - | - |

### Inputs

- Height: `0px`

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#3831BF`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#EBECF0` background
- List items: use `#EBECF0` background

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
