---
name: readwise-ui-skills
description: Readwise's UI design system. Use when building interfaces inspired by Readwise's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://readwise.io
---

# Readwise UI Skills

Opinionated constraints for building Readwise-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Readwise-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#FFFFFF` as page background (`surface-base`)
- MUST use `#3C78C1` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 24 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #FFFFFF | rgb(255,255,255) | Page background |
| `surface-raised` | #3C78C1 | rgb(60,120,193) | Cards, modals, raised surfaces |
| `surface-overlay` | #F7EFA0 | rgb(247,239,160) | Overlays, tooltips, dropdowns |
| `text-primary` | #323232 | rgb(50,50,50) | Headings, body text |
| `text-secondary` | #83B2E7 | rgb(131,178,231) | Secondary, muted text |
| `text-tertiary` | #A3995D | rgb(163,153,93) | Additional text |
| `border-default` | #2165BC | rgb(33,101,188) | Subtle borders, dividers |
| `accent` | #3C78C1 | rgb(60,120,193) | Primary actions, links, focus |
| `warning` | #F4CF8F | rgb(244,207,143) | Warning states, cautions |
| `destructive` | #F0791E | rgb(240,121,30) | Error states, delete actions |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `48px` / `700` for primary headings
- MUST use `28px` / `semi_bold` for body text
- SHOULD reduce font weights (currently 5 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 48px | 700 | #383938 | 1 |
| `text-38px` | Inter | 38px | extra_bold | #303030 | 1 |
| `body` | Inter | 28px | semi_bold | #313131 | 1 |
| `text-22px` | Inter | 22px | semi_bold | #323232 | 1 |
| `text-22px` | Inter | 22px | semi_bold | #383838 | 1 |
| `text-22px` | Inter | 22px | 400 | #4C4C4C | 1 |
| `text-21px` | Inter | 21px | 400 | #635A37 | 1 |
| `text-18px` | Inter | 18px | semi_bold | #D5D5D5 | 1 |
| `text-16px` | Inter | 16px | 400 | #9D9D9C | 1 |
| `text-14px` | Inter | 14px | 400 | #BDD8EF | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 49x)

**Font Sizes:** 5px, 6px, 7px, 8px, 9px, 10px, 11px, 12px, 13px, 14px, 16px, 18px, 21px, 22px, 28px, 38px, 48px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 6px, 7px, 8px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 2px, 5px, 7px, 9px
- SHOULD limit border widths to: 1px, 2px
- SHOULD use 5px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 2px, 5px, 7px, 9px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 6px, 9px, 64px, 5px, 160px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 1080px
- **Main Content**: width: 1364px, height: 913px
- **Main Content**: width: 1364px, height: 903px
- **Main Content**: width: 963px, height: 569px
- **Header**: height: 66px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #83B2E7 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#3C78C1`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#3C78C1` background
- List items: use `#3C78C1` background

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
