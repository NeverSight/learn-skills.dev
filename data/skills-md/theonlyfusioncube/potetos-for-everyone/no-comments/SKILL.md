---
name: no-comments
description: Remove redundant comments, dead workaround explanations, and AI tells from code while preserving necessary constraints. Use when cleaning up code or diffs.
---
# No Comments

1. Identify comments that explain obvious code, restate syntax, or explain temporary workarounds that should be deleted.
2. Distinguish legitimate constraints (hard external requirements, regulatory/spec references, non-obvious invariants) from redundant explanations.
3. Convert valid constraint comments into types, tests, assertions, or lints whenever possible.
4. Delete redundant commentary, commented-out dead code, and speculative notes.
5. Verify that code remains readable and self-documenting through clear naming and small, focused functions.
