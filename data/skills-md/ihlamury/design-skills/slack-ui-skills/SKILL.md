---
name: slack-ui-skills
description: Slack's UI design system. Use when building interfaces inspired by Slack's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://slack.com
---

# Slack UI Skills

Opinionated constraints for building Slack-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Slack-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#FFFFFF` as page background (`surface-base`)
- MUST use `#481652` for primary actions and focus states (`accent`)
- SHOULD reduce color palette (currently 31 colors detected)
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #FFFFFF | rgb(255,255,255) | Page background |
| `surface-raised` | #D9EDE7 | rgb(217,237,231) | Cards, modals, raised surfaces |
| `surface-overlay` | #3F1652 | rgb(63,22,82) | Overlays, tooltips, dropdowns |
| `text-primary` | #0F0F0F | rgb(15,15,15) | Headings, body text |
| `text-secondary` | #6B9389 | rgb(107,147,137) | Secondary, muted text |
| `text-tertiary` | #656A66 | rgb(101,106,102) | Additional text |
| `border-default` | #BDA6BE | rgb(189,166,190) | Subtle borders, dividers |
| `accent` | #481652 | rgb(72,22,82) | Primary actions, links, focus |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `61px` / `700` for primary headings
- MUST use `22px` / `500` for body text
- SHOULD reduce font weights (currently 5 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 61px | 700 | #141414 | 1 |
| `text-50px` | Inter | 50px | 700 | #0F0F0F | 1 |
| `text-49px` | Inter | 49px | 700 | #0F0F0F | 1 |
| `body` | Inter | 22px | 500 | #949494 | 1 |
| `body-secondary` | Inter | 22px | semi_bold | #262626 | 1 |
| `body-secondary` | Inter | 21px | semi_bold | #4A4F4B | 1 |
| `body-secondary` | Inter | 20px | 500 | #747474 | 1 |
| `body-secondary` | Inter | 20px | 400 | #4C4C4C | 1 |
| `text-18px` | Inter | 18px | 400 | #7A7A7A | 1 |
| `text-17px` | Inter | 17px | 400 | #6B9389 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 53x)

**Font Sizes:** 6px, 7px, 8px, 9px, 10px, 11px, 12px, 13px, 14px, 15px, 16px, 17px, 18px, 20px, 21px, 22px, 49px, 50px, 61px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 1px, 2px, 4px, 5px, 6px, 7px, 9px, 10px
- SHOULD use 2px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 1px, 3px, 4px, 8px, 9px, 16px
- SHOULD limit border widths to: 1px, 2px
- SHOULD use 4px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 1px, 3px, 4px, 8px, 9px, 16px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 15px, 67px, 13px, 16px, 17px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 619px

## Components

- MUST use `0px` height for input fields

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #5B887D | none | - | - |

### Inputs

- Height: `0px`

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#481652`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#D9EDE7` background
- List items: use `#D9EDE7` background

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
