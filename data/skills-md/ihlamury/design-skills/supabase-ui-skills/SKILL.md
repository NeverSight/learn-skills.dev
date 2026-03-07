---
name: supabase-ui-skills
description: Supabase's UI design system. Use when building interfaces inspired by Supabase's aesthetic - dark mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://supabase.com
---

# Supabase UI Skills

Opinionated constraints for building Supabase-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building dark-mode interfaces
- Creating Supabase-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- MUST use dark backgrounds (lightness < 20) for primary surfaces - detected lightness: 7
- MUST use `#121212` as page background (`surface-base`)
- SHOULD reduce color palette (currently 16 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #121212 | rgb(18,18,18) | Page background |
| `surface-raised` | #000000 | rgb(0,0,0) | Cards, modals, raised surfaces |
| `surface-overlay` | #0A502B | rgb(10,80,43) | Overlays, tooltips, dropdowns |
| `text-primary` | #525252 | rgb(82,82,82) | Headings, body text |
| `text-2` | #9C9C9C | rgb(156,156,156) | Additional text |
| `text-secondary` | #323232 | rgb(50,50,50) | Secondary, muted text |
| `border-default` | #1A1A1A | rgb(26,26,26) | Subtle borders, dividers |
| `success` | #3DB576 | rgb(61,181,118) | Success states, confirmations |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `56px` / `700` for primary headings
- MUST use `15px` / `400` for body text
- SHOULD reduce font weights (currently 4 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 56px | 700 | #E9E9E9 | 1 |
| `heading-2` | Inter | 55px | 700 | #3DB576 | 1 |
| `text-21px` | Inter | 21px | 500 | #A2A2A2 | 1 |
| `text-16px` | Inter | 16px | 500 | #3C3C3C | 1 |
| `text-16px` | Inter | 16px | 500 | #383838 | 1 |
| `text-16px` | Inter | 16px | 500 | #393939 | 1 |
| `text-16px` | Inter | 16px | 400 | #AAAAAA | 1 |
| `body` | Inter | 15px | 400 | #9C9C9C | 1 |
| `body-secondary` | Inter | 15px | 400 | #444444 | 1 |
| `body-secondary` | Inter | 15px | 400 | #A8A8A8 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 38x)

**Font Sizes:** 9px, 10px, 11px, 12px, 13px, 14px, 15px, 16px, 21px, 55px, 56px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 3px, 4px, 5px, 6px, 16px, 40px, 61px
- SHOULD use 3px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 3px, 4px, 5px, 6px, 7px, 9px, 10px, 13px, 16px
- SHOULD limit border widths to: 1px, 2px
- SHOULD use 3px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 3px, 4px, 5px, 6px, 7px, 9px, 10px, 13px, 16px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 8px, 17px, 52px, 162px, 158px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Header**: height: 66px
- **Main Content**: width: 1920px, height: 1014px
- **Main Content**: width: 1920px, height: 1020px
- **Header**: height: 63px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #4B7D64 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#5E6AD2`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#000000` background
- List items: use `#000000` background

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
