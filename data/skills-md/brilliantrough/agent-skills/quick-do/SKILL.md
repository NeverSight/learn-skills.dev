---
name: quick-do
description: Execute small, well-understood changes directly in the current session with minimal ceremony and ponytail taste. Use when explicitly requested, or automatically for localized fixes, mechanical edits, config tweaks, and short scripts with clear behavior and a known verification path. No plan documents or grilling; do not add tests by default. Prefer steady-do when design, compatibility, or acceptance decisions remain; prefer plan-brief when planning and execution need a separate-session handoff.
---

# Quick Do: understand → do → verify

## When this skill applies

- Small, well-understood changes with a known verification path: localized fixes, mechanical edits, config tweaks, short scripts.
- The user's explicit choice wins — never switch workflows silently; if the chosen one cannot fit the task, say why and ask. Stuck on design, compatibility, or acceptance decisions → stop and propose `steady-do` (if unsure between quick and steady, use steady); a handoff to a separate session → propose `plan-brief`.
- These workflows govern requested development work, not every explanation or read-only question. Skill instructions are in English; replies and deliverables follow the user's language (Chinese by default).

## Do the work

- Read the request, applicable project rules, and affected files before editing. Inspect relevant callers when changing shared behavior; avoid unrelated exploration.
- **Look at the live site first (seconds, no approval):** env active, deps actually importable, files and callers as expected — one glance that prevents a whole round of avoidable errors. Skipping ceremony is the point here; skipping this look is not.
- Fix the root cause, not the reported symptom: grep the callers of what you touch and fix where all of them route through — a guard repeated in every caller is a bigger diff and leaves siblings broken.
- Prefer the obvious interpretation for ordinary implementation details. Ask at most one focused clarification in the normal quick path; if investigation reveals substantial ambiguity or risk, stop and propose `steady-do` rather than guessing to satisfy the question limit.
- No plan documents, grilling sessions, or sub-agents. Use a todo only when the work or host instructions warrant it; do not create a planning ceremony.
- Keep the smallest working change: reuse existing code, then stdlib/native features, then installed dependencies. No over-encapsulation, speculative abstractions, defensive boilerplate, redundant checks, or unrelated cleanup. Preserve necessary trust-boundary validation, security, accessibility, and data protection.
- Before destructive or irreversible actions, show the impact and obtain explicit authorization. A quick workflow does not permit overwriting secrets or changing unrelated environments.

## Verify and finish

- Default to the smallest real execution path plus a reread of the change; check the requested behavior, not merely the absence of errors. For documentation-only changes, inspect content and applicable format checks.
- Do not add tests, TDD, or verification scripts by default. Follow explicit user requests and mandatory project checks; those are not waived by this workflow.
- Report only what actually ran. A static check, successful load, or injected input is not proof of end-to-end behavior. If execution is unavailable, state what remains unverified and the concrete user check.
- **Blocked is a legitimate outcome:** say so, name what is left and the exact check the user must run; never fake completion and never silently skip a step.
- Finish in one short line stating the change and verification status, including a blocker or required user check when present. No separate report or summary essay; required product docs and project memory still apply.
