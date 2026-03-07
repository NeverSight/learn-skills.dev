---
name: posthog-ui-skills
description: Posthog's UI design system. Use when building interfaces inspired by Posthog's aesthetic - dark mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://posthog.com
---

# Posthog UI Skills

Opinionated constraints for building Posthog-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building dark-mode interfaces
- Creating Posthog-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- MUST use dark backgrounds (lightness < 20) for primary surfaces - detected lightness: 0
- MUST use `#000000` as page background (`surface-base`)
- SHOULD limit color palette to 5 distinct colors
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #000000 | rgb(0,0,0) | Page background |
| `surface-raised` | #E38B20 | rgb(227,139,32) | Cards, modals, raised surfaces |
| `text-primary` | #52290C | rgb(82,41,12) | Headings, body text |
| `text-secondary` | #55554A | rgb(85,85,74) | Secondary, muted text |
| `border-default` | #C17C25 | rgb(193,124,37) | Subtle borders, dividers |
| `destructive` | #52290C | rgb(82,41,12) | Error states, delete actions |
| `warning` | #C17C25 | rgb(193,124,37) | Warning states, cautions |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `14px` / `400` for primary headings
- MUST limit font weights to: regular, light
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 14px | 400 | #626257 | 1 |
| `heading-2` | Inter | 13px | 300 | #545449 | 1 |
| `heading-3` | Inter | 12px | 400 | #5B5B50 | 1 |
| `caption` | Inter | 11px | 400 | #58584D | 1 |
| `label` | Inter | 10px | 400 | #52290C | 1 |
| `label` | Inter | 10px | 400 | #55554A | 1 |
| `label` | Inter | 10px | 400 | #56564B | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 7x)

**Font Sizes:** 10px, 11px, 12px, 13px, 14px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 3px, 4px, 9px, 10px
- SHOULD use 4px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 3px
- MUST use 1px border width consistently
- SHOULD use 3px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 3px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 41px, 24px, 43px, 857px, 12px
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Header**: height: 39px
- **Main Content**: width: 1920px, height: 1050px
- **Main Content**: width: 1920px, height: 1043px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #52290C | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#5E6AD2`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#E38B20` background
- List items: use `#E38B20` background

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
