---
name: academic-outline-builder
description: "Use to create a detailed table of contents and chapter-by-chapter plan for Indonesian academic books (buku ajar, buku referensi, or monograf)."
metadata:
  short-description: Build academic book outlines and chapter plans
---

# Academic Outline Builder

Use this specialist to turn a project brief and book architecture into a usable manuscript plan.

## Agent Contract

Input:

- project brief,
- source analysis,
- selected book type,
- chapter map or constraints,
- desired number of chapters if any.

Output:

- `status`.
- `table_of_contents`.
- `chapter_plan`: title, purpose, key topics, expected sources, tables/figures, learning/research function.
- `front_matter`.
- `back_matter`.
- `citation_gaps`.
- `assumptions`.

## Process

1. Confirm book type and reader progression.
2. Build logical chapter order.
3. Assign each chapter a clear role.
4. Add pedagogy fields for buku ajar.
5. Add synthesis/state-of-the-art fields for buku referensi or monograf.
6. List missing sources and figures/tables.

## Rules

- Prefer coherent chapter grouping over mechanical one-source-one-chapter mapping.
- Use Indonesian academic headings.
- Mark placeholder references as `[sumber perlu dilengkapi]`.
