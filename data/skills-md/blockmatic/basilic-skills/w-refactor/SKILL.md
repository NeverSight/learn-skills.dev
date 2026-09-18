---
name: w-refactor
description: Refactor selected code while preserving behavior, then verify.
disable-model-invocation: true
---

Use the selected files or a named concern. Capture current behavior with tests, types, or a manual scenario before editing. Refactor does not authorize commit, push, or PR.

1. Record a baseline: what callers depend on, which checks prove it, and what must not change.
2. Improve structure in the smallest useful diff: extract duplication, clarify names, reduce nesting. Reuse existing packages. Do not add comments that restate the code.
3. Change algorithms or data structures only with measured evidence from the repository's profiler, tests, or traces.
4. Run the affected checks from the baseline. Restore behavior if they fail. Never the full pre-push suite.
5. Docs: `/w-docs` if behavior or commands changed.
