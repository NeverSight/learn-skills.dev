---
name: notion-ui-skills
description: Notion's UI design system. Use when building interfaces inspired by Notion's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://notion.so
---

# Notion UI Skills

Opinionated constraints for building Notion-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Notion-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#F6F6F6` as page background (`surface-base`)
- MUST use `#97CAEE` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 15 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #F6F6F6 | rgb(246,246,246) | Page background |
| `surface-raised` | #E5E5E4 | rgb(229,229,228) | Cards, modals, raised surfaces |
| `surface-overlay` | #DFEFFE | rgb(223,239,254) | Overlays, tooltips, dropdowns |
| `text-primary` | #5D686A | rgb(93,104,106) | Headings, body text |
| `text-2` | #3E3E3E | rgb(62,62,62) | Additional text |
| `text-tertiary` | #505050 | rgb(80,80,80) | Additional text |
| `border-default` | #EDEEEC | rgb(237,238,236) | Subtle borders, dividers |
| `accent` | #97CAEE | rgb(151,202,238) | Primary actions, links, focus |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `66px` / `700` for primary headings
- MUST use `16px` / `500` for body text
- SHOULD reduce font weights (currently 6 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 66px | 700 | #212121 | 1 |
| `text-29px` | Inter | 29px | extra_bold | #292929 | 1 |
| `text-27px` | Inter | 27px | 400 | #4D4D4D | 1 |
| `text-21px` | Inter | 21px | 500 | #252525 | 1 |
| `text-19px` | Inter | 19px | semi_bold | #333333 | 1 |
| `text-18px` | Inter | 18px | semi_bold | #383838 | 1 |
| `text-18px` | Inter | 18px | 400 | #4E4E4E | 1 |
| `body` | Inter | 16px | 500 | #545454 | 1 |
| `body-secondary` | Inter | 16px | 400 | #9B9B9B | 1 |
| `body-secondary` | Inter | 15px | 400 | #5F5F5F | 2 |

### Typography Reference

**Font Families:**
- `Inter` (used 33x)

**Font Sizes:** 8px, 10px, 11px, 12px, 13px, 14px, 15px, 16px, 18px, 19px, 21px, 27px, 29px, 66px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 4px, 5px, 6px, 11px, 14px, 18px
- SHOULD use 1px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 3px, 4px, 6px, 15px
- MUST use 1px border width consistently
- SHOULD use 4px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 3px, 4px, 6px, 15px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 16px, 13px, 17px, 18px, 10px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 1080px
- **Main Content**: width: 1822px, height: 1008px

## Components

- MUST use `0px` height for input fields

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #767674 | none | - | - |

### Inputs

- Height: `0px`

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#97CAEE`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#E5E5E4` background
- List items: use `#E5E5E4` background

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
