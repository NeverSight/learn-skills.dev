---
name: openai-ui-skills
description: OpenAI's UI design system. Use when building interfaces inspired by OpenAI's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://openai.com
---

# OpenAI UI Skills

Opinionated constraints for building OpenAI-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating OpenAI-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#FFFFFF` as page background (`surface-base`)
- SHOULD limit color palette to 8 distinct colors
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #FFFFFF | rgb(255,255,255) | Page background |
| `text-primary` | #525252 | rgb(82,82,82) | Headings, body text |
| `text-secondary` | #747474 | rgb(116,116,116) | Secondary, muted text |
| `text-tertiary` | #8A8A8A | rgb(138,138,138) | Additional text |
| `border-default` | #C9C0BB | rgb(201,192,187) | Subtle borders, dividers |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `24px` / `semi_bold` for primary headings
- MUST use `14px` / `400` for body text
- MUST limit font weights to: regular, semi_bold, light
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 24px | semi_bold | #212121 | 1 |
| `heading-2` | Inter | 24px | semi_bold | #222222 | 1 |
| `body` | Inter | 14px | 400 | #8F8F8F | 1 |
| `body-secondary` | Inter | 13px | 400 | #525252 | 2 |
| `body-secondary` | Inter | 13px | 400 | #5B5B5B | 1 |
| `body-secondary` | Inter | 13px | 400 | #565656 | 1 |
| `body-secondary` | Inter | 11px | 400 | #8A8A8A | 1 |
| `body-secondary` | Inter | 11px | 400 | #8D8D8D | 1 |
| `text-10px` | Inter | 10px | 400 | #5C5C5C | 2 |
| `text-10px` | Inter | 10px | 400 | #575757 | 2 |

### Typography Reference

**Font Families:**
- `Inter` (used 19x)

**Font Sizes:** 7px, 10px, 11px, 13px, 14px, 24px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 4px, 5px, 6px, 7px, 10px, 11px, 31px, 32px
- SHOULD use 4px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 16px, 18px, 19px, 22px
- SHOULD use 22px+ radius for pill-shaped elements
- MUST use 1px border width consistently
- SHOULD use 19px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 16px, 18px, 19px, 22px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use 202px for sidebar width
- SHOULD use consistent element widths: 8px, 21px, 14px, 61px, 36px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Sidebar**: width: 202px, position: left

## Components

- MUST use `0px` height for input fields

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #8A8A8A | none | - | - |

### Inputs

- Height: `0px`

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#5E6AD2`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `surface-raised` background
- List items: use `surface-raised` background

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
