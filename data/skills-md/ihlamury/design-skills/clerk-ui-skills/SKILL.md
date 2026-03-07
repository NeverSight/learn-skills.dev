---
name: clerk-ui-skills
description: Clerk's UI design system. Use when building interfaces inspired by Clerk's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://clerk.com
---

# Clerk UI Skills

Opinionated constraints for building Clerk-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Clerk-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#FEFEFE` as page background (`surface-base`)
- MUST use `#C4A9F3` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 12 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #FEFEFE | rgb(254,254,254) | Page background |
| `surface-raised` | #090909 | rgb(9,9,9) | Cards, modals, raised surfaces |
| `text-primary` | #5C5C5C | rgb(92,92,92) | Headings, body text |
| `text-secondary` | #98979D | rgb(152,151,157) | Secondary, muted text |
| `text-tertiary` | #2F2F2F | rgb(47,47,47) | Additional text |
| `border-default` | #E4E4E1 | rgb(228,228,225) | Subtle borders, dividers |
| `accent` | #C4A9F3 | rgb(196,169,243) | Primary actions, links, focus |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `66px` / `700` for primary headings
- MUST use `26px` / `700` for body text
- SHOULD reduce font weights (currently 4 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 66px | 700 | #262628 | 1 |
| `body` | Inter | 26px | 700 | #292929 | 1 |
| `text-19px` | Inter | 19px | 500 | #4D4D4D | 1 |
| `text-18px` | Inter | 18px | 500 | #303030 | 1 |
| `text-18px` | Inter | 18px | 400 | #525252 | 1 |
| `text-17px` | Inter | 17px | 500 | #E9E9E9 | 1 |
| `text-17px` | Inter | 17px | 400 | #838285 | 1 |
| `text-16px` | Inter | 16px | 500 | #2F2F2F | 1 |
| `text-16px` | Inter | 16px | 300 | #F5F5F5 | 1 |
| `text-15px` | Inter | 15px | 400 | #BDBDBD | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 28x)

**Font Sizes:** 9px, 11px, 12px, 14px, 15px, 16px, 17px, 18px, 19px, 26px, 66px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 4px, 5px, 16px, 37px, 49px, 51px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 4px, 6px, 7px
- MUST use 1px border width consistently
- SHOULD use 6px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 4px, 6px, 7px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 8px, 52px, 44px, 363px, 71px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 584px

## Components

- MUST use `0px` height for input fields

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #BDBDBD | none | - | - |

### Inputs

- Height: `0px`

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#C4A9F3`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#090909` background
- List items: use `#090909` background

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
