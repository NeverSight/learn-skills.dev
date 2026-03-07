---
name: tldraw-ui-skills
description: Tldraw's UI design system. Use when building interfaces inspired by Tldraw's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://tldraw.com
---

# Tldraw UI Skills

Opinionated constraints for building Tldraw-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Tldraw-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#E7EBEE` as page background (`surface-base`)
- MUST use `#0E54F0` for primary actions and focus states (`accent`)
- SHOULD limit color palette to 9 distinct colors
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #E7EBEE | rgb(231,235,238) | Page background |
| `surface-raised` | #F8F9FB | rgb(248,249,251) | Cards, modals, raised surfaces |
| `surface-overlay` | #0E54F0 | rgb(14,84,240) | Overlays, tooltips, dropdowns |
| `text-primary` | #A3A4A6 | rgb(163,164,166) | Headings, body text |
| `text-secondary` | #64686B | rgb(100,104,107) | Secondary, muted text |
| `text-tertiary` | #535353 | rgb(83,83,83) | Additional text |
| `border-default` | #CBCCCE | rgb(203,204,206) | Subtle borders, dividers |
| `accent` | #0E54F0 | rgb(14,84,240) | Primary actions, links, focus |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `14px` / `500` for primary headings
- MUST use `12px` / `400` for body text
- MUST limit font weights to: regular, medium
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 14px | 500 | #5C5C5C | 1 |
| `heading-2` | Inter | 13px | 500 | #4E4F51 | 1 |
| `heading-3` | Inter | 12px | 500 | #6A6A6A | 1 |
| `body` | Inter | 12px | 400 | #535353 | 1 |
| `body-secondary` | Inter | 12px | 400 | #616161 | 1 |
| `body-secondary` | Inter | 12px | 400 | #96C4F4 | 1 |
| `text-10px` | Inter | 10px | 400 | #A3A4A6 | 1 |
| `caption` | Inter | 9px | 400 | #64686B | 1 |
| `label` | Inter | 7px | 400 | #A6A7A9 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 9x)

**Font Sizes:** 7px, 9px, 10px, 12px, 13px, 14px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 3px, 4px, 5px, 6px, 18px, 22px
- SHOULD use 2px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 0px, 3px, 4px, 6px, 7px, 9px
- MUST use 1px border width consistently
- SHOULD use 6px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 0px, 3px, 4px, 6px, 7px, 9px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 16px, 12px, 96px, 13px, 32px
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 965px
- **Main Content**: width: 1920px, height: 593px

## Components

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #A3A4A6 | none | - | - |

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#0E54F0`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#F8F9FB` background
- List items: use `#F8F9FB` background

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
