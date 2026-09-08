---
name: layout
description: Layout practices.
---

# Layout

## Structure

- Make the structure reflect the content and its relationships.
- Add containers only when they serve meaning, layout, or behavior.
- Keep related content together; avoid nesting that adds no meaningful grouping.
- Remove redundant containers and superseded layout rules instead of adding compensating layers.

## Arrangement

- Give each layout responsibility one owner.
- Let parents arrange children; let children arrange their own contents.
- Define repeated spacing and alignment rules once.
- Express layout through flow, alignment, spacing, and sizing constraints.
- Define how elements grow, shrink, and wrap as available space changes.
- Avoid manual offsets and spacer elements used to compensate for layout structure.

## Abstraction

- Extract repeated structures when they represent the same concept and should evolve together.
- Keep simple structures inline; avoid abstractions that merely relocate markup.
- Keep conditional structure readable; separate meaningful variants when branching obscures the layout.
