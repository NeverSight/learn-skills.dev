---
name: deslop
description: Remove AI-generated code slop from a diff
---

# Remove AI code slop

Remove AI-generated slop introduced in the change. Use the caller's diff, or otherwise the diff against the base branch, including staged, unstaged, and untracked files. Finish when you have removed each focus-area instance in the change or kept it because a guardrail requires it.

## Focus areas

- Defensive checks, try/catch blocks, or fallback defaults that are abnormal for trusted code paths or hide failures
- Casts to `any` (or similar language-specific overly broad type) used only to bypass type issues, and subtler dodges that do the same (`as unknown as T`, suppression comments)
- Deeply nested code that should be simplified with early returns
- Speculative generality: an interface with one implementation, an option nobody sets, a parameter always passed the same value, a wrapper that only forwards
- A second name for something the codebase already names

## Guardrails

- Keep behavior unchanged unless fixing a clear bug.
- Remove a guard only when it is provably redundant or removing it fixes a bug. Keep validation at trust boundaries and error handling that prevents data loss.
- Prefer minimal, focused edits over broad rewrites.
- Run the project's type check and tests after editing.
- Keep the final summary concise (1-3 sentences).
