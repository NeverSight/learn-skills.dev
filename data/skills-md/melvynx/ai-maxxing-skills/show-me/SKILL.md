---
name: show-me
description: Explain the current topic visually with the smallest diagram, sketch, or HTML artifact that makes the point. Use when the user wants to see, diagram, sketch, or visualize structure, flow, or change.
---

Show the current topic visually. Skip preamble. Pick the smallest view that makes the point, place it next to the short text it supports, and stop.

- Logic or algorithm → indented pseudocode
- Runtime control flow → call tree
- UI structure → component tree with file paths, state, and module boundaries that matter
- File responsibility or refactor → shallow annotated file tree
- Component, control, or data flow → Mermaid
- What changed, surrounding shape already exists → a `diff` in the same shape as the topic
- Most of it is new, omitted context hides ownership, or the user needs a copyable target → the whole block
- Visual UI, layout, state comparison, or a concept too dense for Mermaid → one focused HTML file matching the product's colors, type, spacing, and real labels; then `open` `show-me-{description}.html`

Keep only the calls, files, props, states, and boundaries needed for the current question. Use one or a few of these, never all of them.
