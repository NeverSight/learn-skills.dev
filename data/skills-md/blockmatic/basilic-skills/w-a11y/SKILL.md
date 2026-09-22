---
name: w-a11y
description: Audit UI against repository a11y docs and tests; do not invent a WCAG level.
disable-model-invocation: true
---

Audit the specified UI against accessibility docs and existing a11y tests. Stay report-only unless the user asked to fix.

1. Read testing and frontend docs for the named a11y gate. If none exists, report that and run only existing repo tests.
2. Inspect semantic structure, keyboard access, names, and focus on changed UI.
3. Run the repository's a11y or component tests. Do not declare WCAG A/AA/AAA unless the repository docs name that level.
4. If fixes are authorized, apply the smallest semantic/ARIA change that meets the documented gate.
5. Docs: `/w-docs` if behavior or commands changed.
