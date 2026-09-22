---
name: rail-pass
description: Compact the current conversation into a pass document for a fresh agent session.
disable-model-invocation: true
---

# Rail Pass

Write a pass document so a fresh agent can continue. Save under the OS temp directory **or** `docs/monorail/<feature>/pass-<date>.md` if a feature slug is active and the user prefers repo-local — ask once if unclear. Find active efforts with the shell (`ls docs/monorail/`); search tools skip gitignored paths.

## Include

- Goal of the next session
- Decisions already made (pointers under `docs/monorail/` — `CONTEXT.md`, ADRs, feature paths — do not duplicate)
- If light align finished decisions but `align.md` is not written yet: say so explicitly and make writing `align.md` the next-session goal (do not start `/rail-spec` until it exists)
- If `align.md` or a cleared map exists but `spec.md` / tasks are not done: next-session goal is continue the **planning chain** (`/rail-spec`; it stops for your go/no-go before `/rail-slice`) — do not ask the user to type each stage separately
- Open questions
- Suggested skills (`/rail-align`, `/rail-spec`, `/rail-build`, …) — planning-chain skills auto-continue downstream (`/rail-spec` stops once for your go/no-go before slice); `/rail-build` runs tasks serially in one session (use this pass doc only when a run's context genuinely degrades; concurrent builds need separate worktrees)
- Exact file paths to read first (`align.md`, `map.md`, `spec.md`, task file, …)

## Rules

- Redact secrets and PII
- If the user passed arguments, treat them as the next session focus
- Do not continue implementing in this session after writing the pass document
