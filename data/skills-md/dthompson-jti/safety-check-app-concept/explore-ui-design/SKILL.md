---
name: explore-ui-design
description: Visual design exploration (layout, color, typography, component composition). Use when exploring "how should this look?" or "what visual treatment should we use?"
---

# Explore UI Design

Explore visual design options including layout, color, typography, and component composition.

## When to Use
- Exploring layout options for a new feature
- Considering color palettes or theming
- Evaluating typography choices
- Exploring component visual treatments

## Approach

### Phase 1: Design Context
Clarify:
- What is the design system context? (Reference SPEC-CSS.md)
- What existing patterns should we align with?
- What mood/tone are we aiming for?

### Phase 2: Visual Options
Generate **3-4 distinct visual approaches** varying:
- Layout structure (grid, flex, composition)
- Visual hierarchy (size, weight, spacing)
- Color usage (accent, background, contrast)
- Component styling (borders, shadows, rounded corners)

Use ASCII wireframes with `var(--token-name)` syntax.

### Phase 3: Recommendation
Recommend with:
- Visual rationale
- Token usage
- Alignment with design system

## Constraints
- Use existing design tokens only — flag as "Hallucination" if token doesn't exist
- No code generation
- No interaction design — that's `explore/ux`
