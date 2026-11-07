---
name: acknowledge
description: Acknowledge user-made code changes without modifying anything.
disable-model-invocation: true
---

# Acknowledge User Changes

When invoked:

1. Read the user's description of the changes.
2. Inspect the relevant code to understand the current implementation, if needed.
3. Do not edit, create, delete, format, or revert any files.
4. Do not run commands or tools that modify the codebase, generate files, or change project state.
5. Acknowledge the changes and briefly summarize your understanding.
6. If anything is unclear, ask a question instead of guessing.

This is an acknowledgment-only task. Do not implement, improve, refactor, review, or suggest changes unless explicitly asked.

## Response

Briefly confirm:
- What changed.
- How you understand the current behavior or implementation.
- Any ambiguity that needs clarification.

Do not resume previous tasks automatically.