---
name: lemonsqueezy-ui-skills
description: Lemonsqueezy's UI design system. Use when building interfaces inspired by Lemonsqueezy's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://lemonsqueezy.com
---

# Lemonsqueezy UI Skills

Opinionated constraints for building Lemonsqueezy-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Lemonsqueezy-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#FEFEFE` as page background (`surface-base`)
- MUST use `#9368E3` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 12 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #FEFEFE | rgb(254,254,254) | Page background |
| `surface-raised` | #3F01DF | rgb(63,1,223) | Cards, modals, raised surfaces |
| `text-primary` | #D0B4F4 | rgb(208,180,244) | Headings, body text |
| `text-2` | #4F4F50 | rgb(79,79,80) | Additional text |
| `text-secondary` | #8550F5 | rgb(133,80,245) | Secondary, muted text |
| `border-default` | #9368E3 | rgb(147,104,227) | Subtle borders, dividers |
| `accent` | #9368E3 | rgb(147,104,227) | Primary actions, links, focus |
| `warning` | #FCD995 | rgb(252,217,149) | Warning states, cautions |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `74px` / `700` for primary headings
- MUST use `31px` / `semi_bold` for body text
- SHOULD reduce font weights (currently 4 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 74px | 700 | #F1E8F9 | 1 |
| `body` | Inter | 31px | semi_bold | #E2D2F8 | 1 |
| `text-25px` | Inter | 25px | semi_bold | #E0CDF6 | 1 |
| `text-25px` | Inter | 25px | semi_bold | #E2D1F8 | 1 |
| `text-25px` | Inter | 25px | semi_bold | #DAC6F6 | 1 |
| `text-22px` | Inter | 22px | 500 | #D0B4F4 | 1 |
| `text-18px` | Inter | 18px | 400 | #8A59F2 | 1 |
| `text-15px` | Inter | 15px | 400 | #8A56F5 | 1 |
| `text-15px` | Inter | 15px | 400 | #8955F5 | 1 |
| `text-15px` | Inter | 15px | 400 | #794D14 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 18x)

**Font Sizes:** 11px, 12px, 13px, 14px, 15px, 18px, 22px, 25px, 31px, 74px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 2px, 3px, 4px, 5px, 6px, 15px, 16px, 17px
- SHOULD use 4px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 17px, 21px, 29px
- SHOULD use 21px+ radius for pill-shaped elements
- SHOULD limit border widths to: 1px, 2px
- SHOULD use 29px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 17px, 21px, 29px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 30px, 12px, 145px, 88px, 8px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 1002px
- **Main Content**: width: 1920px, height: 998px
- **Header**: height: 69px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #D0B4F4 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#9368E3`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#3F01DF` background
- List items: use `#3F01DF` background

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
