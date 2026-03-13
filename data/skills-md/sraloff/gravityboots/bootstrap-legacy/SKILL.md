---
name: bootstrap-legacy
description: Patterns for maintaining or migrating Bootstrap 3/4/5 projects.
---

# Bootstrap Legacy Patterns

## When to use this skill
- Maintaining sites built with Bootstrap.
- Migrating from Bootstrap to Tailwind.
- Using Bootstrap components.

## 1. Grid System
- **Classes**: `container`, `row`, `col-{breakpoint}-{size}`.
- **Nesting**: Rows must be direct children of containers or columns.

## 2. Utilities vs Components
- **Components**: Bootstrap relies heavily on pre-built components (`.card`, `.navbar`, `.modal`).
- **Utilities**: Bootstrap 5 introduced more utility classes (`.d-flex`, `.mb-3`), similar to Tailwind. Prefer these over custom CSS when editing.

## 3. Migration
- **To Tailwind**: Map concepts (e.g., `d-none` -> `hidden`, `text-center` -> `text-center`, `btn-primary` -> custom component).
- **Coexistence**: Avoid loading both if possible, but if needed, scope Bootstrap to a wrapper (namespace).
