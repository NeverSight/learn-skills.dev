---
name: codeium-ui-skills
description: Codeium's UI design system. Use when building interfaces inspired by Codeium's aesthetic - dark mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://codeium.com
---

# Codeium UI Skills

Opinionated constraints for building Codeium-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building dark-mode interfaces
- Creating Codeium-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- MUST use dark backgrounds (lightness < 20) for primary surfaces - detected lightness: 17
- MUST use `#152443` as page background (`surface-base`)
- MUST use `#32E5AD` for primary actions and focus states (`accent`)
- SHOULD limit color palette to 7 distinct colors
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #152443 | rgb(21,36,67) | Page background |
| `surface-raised` | #32E5AD | rgb(50,229,173) | Cards, modals, raised surfaces |
| `text-primary` | #ACB9C8 | rgb(172,185,200) | Headings, body text |
| `text-secondary` | #136045 | rgb(19,96,69) | Secondary, muted text |
| `text-tertiary` | #CED5DB | rgb(206,213,219) | Additional text |
| `border-default` | #253453 | rgb(37,52,83) | Subtle borders, dividers |
| `accent` | #32E5AD | rgb(50,229,173) | Primary actions, links, focus |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `77px` / `700` for primary headings
- MUST use `20px` / `400` for body text
- MUST limit font weights to: regular, bold
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 77px | 700 | #CED5DB | 1 |
| `body` | Inter | 20px | 400 | #ACB9C8 | 1 |
| `body-secondary` | Inter | 20px | 400 | #B4BEC9 | 1 |
| `text-17px` | Inter | 17px | 400 | #B2BDCB | 1 |
| `text-14px` | Inter | 14px | 400 | #136045 | 1 |
| `text-13px` | Inter | 13px | 400 | #A0ACBE | 1 |
| `caption` | Inter | 10px | 400 | #146F50 | 1 |
| `label` | Inter | 10px | 400 | #A7B3C2 | 1 |
| `label` | Inter | 10px | 400 | #A1ADBD | 1 |
| `label` | Inter | 10px | 400 | #A9B6C4 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 13x)

**Font Sizes:** 10px, 13px, 14px, 17px, 20px, 77px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 5px, 6px, 16px, 29px, 42px
- SHOULD use 6px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use 1px border width consistently
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 6px, 157px, 74px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 1080px
- **Main Content**: width: 1920px, height: 802px
- **Header**: height: 84px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #B2BDCB | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#32E5AD`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#32E5AD` background
- List items: use `#32E5AD` background

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
