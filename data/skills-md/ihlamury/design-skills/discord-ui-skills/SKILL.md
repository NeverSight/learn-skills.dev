---
name: discord-ui-skills
description: Discord's UI design system. Use when building interfaces inspired by Discord's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://discord.com
---

# Discord UI Skills

Opinionated constraints for building Discord-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Discord-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#4548ED` as page background (`surface-base`)
- MUST use `#4548ED` for primary actions and focus states (`accent`)
- SHOULD limit color palette to 9 distinct colors
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #4548ED | rgb(69,72,237) | Page background |
| `surface-raised` | #FEFEFE | rgb(254,254,254) | Cards, modals, raised surfaces |
| `text-primary` | #C8D0F9 | rgb(200,208,249) | Headings, body text |
| `text-2` | #494A4B | rgb(73,74,75) | Additional text |
| `text-tertiary` | #36383C | rgb(54,56,60) | Additional text |
| `border-default` | #4848E2 | rgb(72,72,226) | Subtle borders, dividers |
| `accent` | #4548ED | rgb(69,72,237) | Primary actions, links, focus |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `52px` / `700` for primary headings
- MUST use `20px` / `400` for body text
- MUST limit font weights to: regular, medium, bold
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 52px | 700 | #F4F4F6 | 1 |
| `body` | Inter | 20px | 400 | #C8D0F9 | 1 |
| `body-secondary` | Inter | 18px | 400 | #C8C8DF | 1 |
| `text-17px` | Inter | 17px | 500 | #CFCFD1 | 1 |
| `text-15px` | Inter | 15px | 400 | #414141 | 1 |
| `text-14px` | Inter | 14px | 400 | #494A4B | 1 |
| `text-14px` | Inter | 14px | 400 | #B3B3C2 | 1 |
| `text-14px` | Inter | 14px | 400 | #B7B6C4 | 1 |
| `text-14px` | Inter | 14px | 400 | #BDBCC9 | 1 |
| `text-14px` | Inter | 14px | 400 | #B1B0BC | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 16x)

**Font Sizes:** 11px, 12px, 13px, 14px, 15px, 17px, 18px, 20px, 52px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 5px, 6px, 13px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 9px
- MUST use 1px border width consistently
- SHOULD use 9px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 9px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 10px, 11px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 1080px
- **Main Content**: width: 1920px, height: 1034px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #C8D0F9 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#4548ED`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#FEFEFE` background
- List items: use `#FEFEFE` background

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
