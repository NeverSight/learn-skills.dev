---
name: anthropic-ui-skills
description: Anthropic's UI design system. Use when building interfaces inspired by Anthropic's aesthetic - light mode, Inter font, 4px grid.
license: MIT
metadata:
  author: design-skills
  version: "1.0.0"
  source: https://www.anthropic.com
---

# Anthropic UI Skills

Opinionated constraints for building Anthropic-style interfaces with AI agents.

## When to Apply

Reference these guidelines when:
- Building light-mode interfaces
- Creating Anthropic-inspired design systems
- Implementing UIs with Inter font and 4px grid

## Colors

- SHOULD use light backgrounds for primary surfaces
- MUST use `#ECE9E0` as page background (`surface-base`)
- SHOULD limit color palette to 8 distinct colors
- MUST maintain text contrast ratio of at least 4.5:1 for accessibility

### Semantic Tokens

| Token | HEX | RGB | Usage |
|-------|-----|-----|-------|
| `surface-base` | #ECE9E0 | rgb(236,233,224) | Page background |
| `surface-raised` | #DBD1C0 | rgb(219,209,192) | Cards, modals, raised surfaces |
| `surface-overlay` | #0F0F10 | rgb(15,15,16) | Overlays, tooltips, dropdowns |
| `text-primary` | #625F59 | rgb(98,95,89) | Headings, body text |
| `text-secondary` | #9F9F9C | rgb(159,159,156) | Secondary, muted text |
| `text-tertiary` | #454036 | rgb(69,64,54) | Additional text |

## Typography

- MUST use `Inter` as primary font family
- SHOULD use single font family for consistency
- MUST use `68px` / `700` for primary headings
- MUST use `33px` / `semi_bold` for body text
- SHOULD reduce font weights (currently 5 detected)
- MUST use `text-balance` for headings and `text-pretty` for body text
- SHOULD use `tabular-nums` for numeric data
- NEVER modify letter-spacing unless explicitly requested

### Text Styles

| Style | Font | Size | Weight | Color | Count |
|-------|------|------|--------|-------|-------|
| `heading-1` | Inter | 68px | 700 | #201F1D | 1 |
| `body` | Inter | 33px | semi_bold | #35312A | 1 |
| `text-23px` | Inter | 23px | 500 | #403D37 | 1 |
| `text-21px` | Inter | 21px | 400 | #3D362C | 1 |
| `text-21px` | Inter | 21px | 400 | #3B352B | 1 |
| `text-20px` | Inter | 20px | 400 | #494237 | 1 |
| `text-17px` | Inter | 17px | 500 | #423F3B | 1 |
| `text-16px` | Inter | 16px | 400 | #454036 | 1 |
| `text-14px` | Inter | 14px | 500 | #3F3931 | 1 |
| `text-14px` | Inter | 14px | 400 | #A2A3A0 | 1 |

### Typography Reference

**Font Families:**
- `Inter` (used 16x)

**Font Sizes:** 10px, 11px, 14px, 16px, 17px, 20px, 21px, 23px, 33px, 68px

## Spacing

- MUST use 4px grid for spacing
- SHOULD use spacing from scale: 3px, 4px, 5px, 6px
- SHOULD use 5px as default gap between elements
- NEVER use arbitrary spacing values (use design scale)
- SHOULD maintain consistent padding within containers

## Borders

- MUST use border-radius from scale: 3px, 15px
- SHOULD use 3px as default border-radius
- NEVER use arbitrary border-radius values (use design scale)
- SHOULD use subtle borders (1px) for element separation

### Border Radius Reference

**Scale:** 3px, 15px

## Layout

- MUST design for 1920px base viewport width
- SHOULD use consistent element widths: 10px, 18px, 146px, 579px
- SHOULD maintain text-heavy layout with clear hierarchy
- NEVER use `h-screen`, use `h-dvh` for full viewport height
- MUST respect `safe-area-inset` for fixed elements
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

### Detected Layout Patterns

- **Main Content**: width: 1920px, height: 1004px
- **Main Content**: width: 1920px, height: 673px

## Components

- MUST use `0px` height for input fields

### Buttons

| Variant | Background | Text | Border | Height | Radius |
|---------|------------|------|--------|--------|--------|
| Ghost | transparent | #9F9F9C | none | - | - |

### Inputs

- Height: `0px`

## Interactive States

### Focus

- MUST use `2px` outline with accent color (`#5E6AD2`)
- MUST use `2px` outline-offset
- NEVER remove focus indicators

### Hover

- Buttons (primary): lighten background by 10%
- Buttons (secondary): use `#DBD1C0` background
- List items: use `#DBD1C0` background

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
