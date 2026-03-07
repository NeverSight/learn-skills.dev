---
name: github-ui-skills
description: GitHub's UI design system. Use when building interfaces inspired by GitHub's aesthetic - dark mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://github.com
---

# GitHub UI Skills

Opinionated constraints for building GitHub-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building dark-mode interfaces
- Creating GitHub-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- MUST use dark backgrounds (lightness < 20) for primary surfaces - detected lightness: 12
- MUST use `#10131A` as page background (`surface-base`)
- MUST use `#030036` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 23 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #10131A | rgb(16,19,26) | Page background |
| `surface-raised` | #11122F | rgb(17,18,47) | Cards, modals, raised surfaces |
| `surface-overlay` | #186D29 | rgb(24,109,41) | Overlays, tooltips, dropdowns |
| `text-primary` | #878A91 | rgb(135,138,145) | Headings, body text |
| `text-secondary` | #74777E | rgb(116,119,126) | Secondary, muted text |
| `text-tertiary` | #525C71 | rgb(82,92,113) | Additional text |
| `border-default` | #1A1835 | rgb(26,24,53) | Subtle borders, dividers |
| `success` | #A3D4AD | rgb(163,212,173) | Success states, confirmations |
| `accent` | #030036 | rgb(3,0,54) | Primary actions, links, focus |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `53px` / `700` for primary headings
- MUST use `29px` / `400` for body text
- MUST limit font weights to: regular, bold, light
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 53px | 700 | #E3E4EA | 1 |
| `body` | Inter | 29px | 400 | #606A7A | 1 |
| `text-18px` | Inter | 18px | 400 | #A7A8BF | 1 |
| `text-16px` | Inter | 16px | 300 | #989BA2 | 1 |
| `text-15px` | Inter | 15px | 300 | #3F4249 | 1 |
| `text-15px` | Inter | 15px | 400 | #7F848A | 1 |
| `text-15px` | Inter | 15px | 400 | #B5B6C4 | 1 |
| `text-15px` | Inter | 15px | 400 | #A3D4AD | 1 |
| `text-15px` | Inter | 15px | 400 | #6B6B71 | 1 |
| `text-15px` | Inter | 15px | 400 | #9796B1 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 54x)

**Font Sizes:** 4px, 5px, 9px, 10px, 11px, 12px, 13px, 14px, 15px, 16px, 18px, 29px, 53px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 2px, 3px, 4px, 5px, 6px, 8px, 11px, 14px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 3px, 4px, 5px, 9px, 15px, 22px, 29px
- SHOULD use 22px+ radius for pill-shaped elements
- SHOULD limit border widths to: 1px, 2px, 3px, 4px
- SHOULD use 3px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 3px, 4px, 5px, 9px, 15px, 22px, 29px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 10px, 9px, 11px, 28px, 21px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 1080px
- **Main Content**: width: 1920px, height: 1004px
- **Header**: height: 64px

## Components

- MUST use `0px` height for input fields

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #B5B6C4 | none | - | - |

### Inputs

- Height: `0px`

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#030036`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#11122F` background
- List items: use `#11122F` background

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
