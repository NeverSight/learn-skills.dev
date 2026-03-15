---
name: ui-refactor
description: Tactical user interface design guide for fixing layouts, selecting colors/fonts, and creating professional UIs. Use when the user asks to "make this look better," needs help with CSS/styling decisions, wants to create a design system, or needs to fix a cluttered interface.
---

# UI Refactoring and Design

This skill applies tactical, logical rules to user interface design. It prioritizes clarity, hierarchy, and systems over "artistic talent."

## Core Workflow

1.  **Feature First**: Do not start by designing a "shell" (nav bars, sidebars). Start with the specific functionality (e.g., the search form, the contact card).
2.  **Low Fidelity**: Ignore color, shadows, and fonts initially. Design in grayscale using a thick marker or basic wireframes to solve layout and spacing first.
3.  **Define Systems**: Do not use arbitrary values. establishing restrictive systems for spacing, type, and color immediately.
4.  **Refine**: Apply specific tactics for hierarchy, depth, and polish.

## Domain-Specific Tactics

Consult these references for specific implementation rules:

- **Making elements stand out/fit in**: See [hierarchy.md](references/hierarchy.md) (Size, weight, contrast, semantics).
- **Whitespace and alignment**: See [layout-spacing.md](references/layout-spacing.md) (Grids, spacing scales, density).
- **Text and fonts**: See [typography.md](references/typography.md) (Type scales, line-height, fonts).
- **Colors and palettes**: See [color.md](references/color.md) (HSL, saturation, accessible contrast).
- **Images, shadows, and polish**: See [depth-and-polish.md](references/depth-and-polish.md) (Light sources, assets, finishing touches).

## Quick Heuristics

- **Limit Choices**: If you can't decide between two options, you have too many choices. constrain your inputs (colors, font sizes, spacing) to a pre-defined scale.
- **Personality**:
    - *Serious/Elegant*: Serif fonts, sharp corners, gold/blue colors, formal language.
    - *Playful/Friendly*: Rounded sans-serifs, large border-radius, pink/orange, casual language.
- **Complexity**: Do not design for edge cases first. Design the "happy path" (simple version), then iterate for complexity.