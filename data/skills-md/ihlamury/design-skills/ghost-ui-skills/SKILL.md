---
name: ghost-ui-skills
description: Ghost's UI design system. Use when building interfaces inspired by Ghost's aesthetic - dark mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://ghost.org
---

# Ghost UI Skills

Opinionated constraints for building Ghost-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building dark-mode interfaces
- Creating Ghost-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- MUST use dark backgrounds (lightness < 20) for primary surfaces - detected lightness: 8
- MUST use `#FFFFFF` as page background (`surface-base`)
- SHOULD reduce color palette (currently 18 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #FFFFFF | rgb(255,255,255) | Page background |
| `surface-raised` | #DAE1EC | rgb(218,225,236) | Cards, modals, raised surfaces |
| `surface-overlay` | #0D0E10 | rgb(13,14,16) | Overlays, tooltips, dropdowns |
| `text-primary` | #D8D9DC | rgb(216,217,220) | Headings, body text |
| `text-secondary` | #333437 | rgb(51,52,55) | Secondary, muted text |
| `text-tertiary` | #4C4E53 | rgb(76,78,83) | Additional text |
| `border-default` | #DBE0E8 | rgb(219,224,232) | Subtle borders, dividers |
| `warning` | #FAB429 | rgb(250,180,41) | Warning states, cautions |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `73px` / `700` for primary headings
- MUST use `26px` / `500` for body text
- SHOULD reduce font weights (currently 5 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 73px | 700 | #1E2826 | 1 |
| `body` | Inter | 26px | 500 | #2F2F2F | 1 |
| `body-secondary` | Inter | 24px | semi_bold | #D8D9DC | 2 |
| `body-secondary` | Inter | 23px | semi_bold | #E5E6E9 | 1 |
| `text-18px` | Inter | 18px | semi_bold | #C2C3C4 | 1 |
| `text-14px` | Inter | 14px | 400 | #7B7B7B | 1 |
| `text-14px` | Inter | 14px | 400 | #7C7C7C | 1 |
| `text-14px` | Inter | 14px | 400 | #787878 | 1 |
| `text-13px` | Inter | 13px | 400 | #313234 | 1 |
| `text-13px` | Inter | 13px | 400 | #333438 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 42x)

**Font Sizes:** 9px, 10px, 11px, 12px, 13px, 14px, 18px, 23px, 24px, 26px, 73px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 6px, 7px, 8px
- SHOULD use 65px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 3px, 4px, 7px, 13px, 16px
- SHOULD limit border widths to: 1px, 6px
- SHOULD use 13px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 3px, 4px, 7px, 13px, 16px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 260px, 10px, 8px, 13px, 35px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1635px, height: 1080px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #757678 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#5E6AD2`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#DAE1EC` background
- List items: use `#DAE1EC` background

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
