---
name: spec-authoring
description: Create/iterate requirements docs with REQ-IDs following specs/requirements.md (root or specs/features/<slug>/ scope).
argument-hint: "[root|<slug>] [short goal]"
user-invocable: true
---

# spec-authoring

## Purpose
Write or refine `requirements.md` so it is clear, testable, and scoped, using REQ IDs and the repository template.

## Inputs
- `PROJECT.md`
- `specs/requirements.md` OR `specs/features/<slug>/requirements.md` (scope)
- If present: existing `design.md` / `tasks.md` for the same scope (read-only context; do not advance phases)

## Steps
1. Resolve scope:
   - If `<slug>` provided: use `specs/features/<slug>/requirements.md`
   - Else: use `specs/requirements.md`
2. Read the target requirements file and keep its template structure.
3. Fill/iterate:
   - Introduction (what/why, not how)
   - Glossary (only domain terms; consistent naming)
   - Requirements list using REQ IDs: `REQ-001`, `REQ-002`, ...
4. For each requirement:
   - Keep it single-purpose.
   - Make it testable and unambiguous.
   - Avoid implementation details.
   - Add acceptance criteria only if it improves testability (SHALL statements).
5. Detect missing info and ask only the minimum blocking questions.
6. Stop and request explicit approval when the requirements are coherent and complete.

## Output
- Updated requirements file for the resolved scope
- 3–5 bullets summarizing what changed
- Blocking questions (only if required to proceed)
