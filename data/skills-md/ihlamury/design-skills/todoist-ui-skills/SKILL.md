---
name: todoist-ui-skills
description: Todoist's UI design system. Use when building interfaces inspired by Todoist's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://todoist.com
---

# Todoist UI Skills

Opinionated constraints for building Todoist-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Todoist-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#FDFCFA` as page background (`surface-base`)
- SHOULD reduce color palette (currently 20 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #FDFCFA | rgb(253,252,250) | Page background |
| `surface-raised` | #FDDECF | rgb(253,222,207) | Cards, modals, raised surfaces |
| `surface-overlay` | #FDF3EA | rgb(253,243,234) | Overlays, tooltips, dropdowns |
| `text-primary` | #A6A6A6 | rgb(166,166,166) | Headings, body text |
| `text-2` | #515250 | rgb(81,82,80) | Additional text |
| `text-secondary` | #6B6A6A | rgb(107,106,106) | Secondary, muted text |
| `border-default` | #F6F1EF | rgb(246,241,239) | Subtle borders, dividers |
| `destructive` | #FDF3EA | rgb(253,243,234) | Error states, delete actions |
| `warning` | #FDFCFA | rgb(253,252,250) | Warning states, cautions |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `55px` / `700` for primary headings
- MUST use `13px` / `400` for body text
- SHOULD reduce font weights (currently 5 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 55px | 700 | #2B2A26 | 1 |
| `text-22px` | Inter | 22px | 400 | #606159 | 1 |
| `text-21px` | Inter | 21px | 500 | #C95958 | 1 |
| `text-20px` | Inter | 20px | 400 | #66675E | 1 |
| `text-19px` | Inter | 19px | 400 | #777674 | 1 |
| `text-18px` | Inter | 18px | 500 | #969591 | 1 |
| `text-18px` | Inter | 18px | 400 | #A4A3A1 | 1 |
| `text-18px` | Inter | 18px | extra_bold | #8B8C86 | 1 |
| `text-16px` | Inter | 16px | 500 | #F1BCAF | 1 |
| `text-16px` | Inter | 16px | 400 | #52534D | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 75x)

**Font Sizes:** 5px, 6px, 7px, 8px, 9px, 10px, 11px, 12px, 13px, 14px, 15px, 16px, 18px, 19px, 20px, 21px, 22px, 55px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 6px, 7px, 10px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 1px, 2px, 3px, 4px, 9px, 10px
- MUST use 1px border width consistently
- SHOULD use 3px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 1px, 2px, 3px, 4px, 9px, 10px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 7px, 8px, 10px, 11px, 5px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 938px
- **Header**: height: 76px

## Components

- MUST use `0px` height for input fields

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #515250 | none | - | - |

### Inputs

- Height: `0px`

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#5E6AD2`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#FDDECF` background
- List items: use `#FDDECF` background

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
