---
name: convertkit-ui-skills
description: Convertkit's UI design system. Use when building interfaces inspired by Convertkit's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://convertkit.com
---

# Convertkit UI Skills

Opinionated constraints for building Convertkit-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Convertkit-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#FFFFFF` as page background (`surface-base`)
- MUST use `#194775` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 18 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #FFFFFF | rgb(255,255,255) | Page background |
| `surface-raised` | #EEE9E4 | rgb(238,233,228) | Cards, modals, raised surfaces |
| `surface-overlay` | #379EFD | rgb(55,158,253) | Overlays, tooltips, dropdowns |
| `text-primary` | #6C6C6C | rgb(108,108,108) | Headings, body text |
| `text-secondary` | #8C8B91 | rgb(140,139,145) | Secondary, muted text |
| `text-tertiary` | #4B4855 | rgb(75,72,85) | Additional text |
| `border-default` | #EFFEFE | rgb(239,254,254) | Subtle borders, dividers |
| `accent` | #194775 | rgb(25,71,117) | Primary actions, links, focus |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `75px` / `700` for primary headings
- MUST use `29px` / `semi_bold` for body text
- SHOULD reduce font weights (currently 5 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 75px | 700 | #242221 | 1 |
| `body` | Inter | 29px | semi_bold | #4B4855 | 1 |
| `text-24px` | Inter | 24px | 700 | #292929 | 1 |
| `text-17px` | Inter | 17px | 400 | #6D6864 | 1 |
| `text-16px` | Inter | 16px | 400 | #66625E | 1 |
| `text-15px` | Inter | 15px | 400 | #9DA1A5 | 1 |
| `text-15px` | Inter | 15px | 500 | #CED2D4 | 1 |
| `text-15px` | Inter | 15px | 500 | #4A4744 | 1 |
| `text-15px` | Inter | 15px | 500 | #4D4A47 | 1 |
| `text-14px` | Inter | 14px | 400 | #8C8B91 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 35x)

**Font Sizes:** 11px, 12px, 13px, 14px, 15px, 16px, 17px, 24px, 29px, 75px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 6px, 7px, 8px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 3px, 4px, 6px, 7px, 9px, 10px
- SHOULD limit border widths to: 1px, 2px
- SHOULD use 7px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 3px, 4px, 6px, 7px, 9px, 10px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 44px, 10px, 335px, 107px, 142px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Header**: height: 58px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #5B5B5B | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#194775`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#EEE9E4` background
- List items: use `#EEE9E4` background

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
