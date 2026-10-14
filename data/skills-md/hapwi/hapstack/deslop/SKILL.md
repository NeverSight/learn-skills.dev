---
name: deslop
description: Remove AI-generated code slop and clean up code style
license: MIT
---

## Host integration

Read [the Hapstack runtime contract](../hap-mode/references/runtime.md) once per task before model selection, delegation, external actions, or scheduling. Its host mappings and authorization rules govern the host-specific steps below.


# Remove AI code slop

Resolve the requested diff base or actual remote default branch, then check the scoped diff against it and remove AI-generated slop introduced in the branch.

## Focus Areas

- Extra comments that are unnecessary or inconsistent with local style
- Defensive checks or try/catch blocks that are abnormal for trusted code paths
- Casts to `any` used only to bypass type issues
- Deeply nested code that should be simplified with early returns
- Other patterns inconsistent with the file and surrounding codebase

## Guardrails

- Keep behavior unchanged unless fixing a clear bug.
- Prefer minimal, focused edits over broad rewrites.
- Keep the final summary concise (1-3 sentences).
