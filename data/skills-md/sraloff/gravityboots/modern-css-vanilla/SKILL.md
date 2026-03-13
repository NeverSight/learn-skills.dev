---
name: modern-css-vanilla
description: Modern CSS features like container queries, :has(), and cascade layers.
---

# Modern CSS Vanilla

## When to use this skill
- Writing custom CSS/SCSS (not utilizing Tailwind).
- Refactoring legacy stylesheets.
- Implementing complex layouts.

## 1. New Selectors
- **:has()**: The parent selector. `div:has(> img)` selects divs containing an image.
- **:is() / :where()**: For grouping selectors. `:where()` has 0 specificity (useful for resets).

## 2. Layouts
- **Container Queries**:
  ```css
  .card-container { container-type: inline-size; }
  @container (min-width: 500px) { ... }
  ```
- **Grid**: Use `display: grid` for 2D layouts; `flex` for 1D.

## 3. Architecture
- **Layers**: Use `@layer` to control cascade order explicitly (e.g., `@layer reset, base, theme, utilities`).
- **Variables**: Use Custom Properties (`--brand-color`) for theming.
