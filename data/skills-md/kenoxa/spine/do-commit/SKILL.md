---
name: do-commit
description: >
  Safe, scoped commit workflow.
  Use when ready to commit changes. Do NOT use mid-implementation —
  finish the current task first.
disable-model-invocation: true
argument-hint: "[message]"
---

Stage only in-scope files, draft a Conventional Commits message, confirm with user, commit.

## Workflow

1. **Inspect** — run `git status` and `git diff --stat` to see dirty files.
2. **Scope files** — determine committable files in this order:
   - User-specified files (highest priority)
   - Files clearly attributable to the current task/session
   - Best-guess selection from dirty files — include the proposed list in the confirmation step
3. **Draft message** — `<type>[optional scope][!]: <description>` (imperative, specific, ≤72 chars).
   For non-trivial or multi-file changes, add a concise body (1–3 bullets) explaining why,
   key constraints, and impact. Do not restate the diff.
4. **Confirm** — display the proposed commit message as a fenced code block and list staged
   file paths. Ask one concise question (e.g., "Commit these changes?"). Never commit without
   explicit user approval.
5. **Commit** — stage only confirmed paths and commit. If committed paths differ from staged
   (e.g., hooks modified content), report the deltas.
6. **Report** — show commit hash and summary.

## Scoped Staging

Never auto-stage all dirty files (`git add -A` / `git add .`). Stage only confirmed in-scope
paths. Pre-commit hooks may add or modify content during commit — this is expected.

## Message Format

Conventional Commits. Types: `feat`, `fix`, `refactor`, `chore`, `docs`, `test`, `perf`, `ci`, `build`.

- Subject: imperative mood, specific, no vague summaries (`update stuff`, `fix things`)
- Body (when present): explains *why*, not *what* — the diff shows what changed
- Breaking changes: `!` suffix on type or `BREAKING CHANGE:` footer

## Constraints

- Push only when explicitly requested.
- Amend only when explicitly requested.
- If no in-scope committable files exist, report and stop.
- Never strip or modify commit trailers added by the platform or user.

## Anti-Patterns

- Auto-staging all dirty files without scoping
- Committing without explicit user confirmation
- Vague commit messages that don't describe the actual change
- Pushing without being asked
- Amending without being asked
