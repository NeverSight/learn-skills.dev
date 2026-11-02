---
name: atlas-implement
description: "Test-driven and source-driven implementation. Use when building features or fixing bugs test-first, using red-green-refactor, or writing integration tests; checking an approach against official framework or library documentation before implementing; or designing interfaces, ownership and module boundaries."
disable-model-invocation: false
metadata:
  short-description: Design first, test first or implement from official documentation.
---

# Atlas Implement

Select from the requested outcome and implementation context, honoring an explicit method choice. Read and follow each selected method before editing; combine methods when their needs apply.

Treat requests for `architect`, `tdd` or `source-driven-development` as requests for the corresponding bundled method, and load it through the links below.

| Method | When it applies | Read and follow |
| --- | --- | --- |
| Architect | An explicit Architect/design-first request, or a selected architectural decision about interfaces, ownership or module shape | [Architect](references/architect/architect.md) |
| TDD | Test-first feature or bug work, red-green-refactor, integration tests, or behavior with an agreed public Test Seam | [TDD](references/tdd/tdd.md) |
| Source-Driven Development | Implementation whose correctness depends on framework, library or API versions and their official documentation | [Source-Driven](references/source-driven/source-driven.md) |

Architect is selective; routine implementation does not require design exploration. For combined work, use Source-Driven to establish version-specific constraints, Architect to choose the implementation shape, and TDD to prove behavior through the agreed seam. Mechanical edits and version-independent work use normal project validation when no selected method applies.
