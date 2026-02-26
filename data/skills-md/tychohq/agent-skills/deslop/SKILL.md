---
name: deslop
version: 1.0.0
description: Remove AI-style code slop from a branch by reviewing diffs, deleting inconsistent defensive noise, and preserving behavior and local style.
allowed-tools: [Bash]
---

## When to use this skill

Use when asked to:
- "remove AI slop"
- "clean up generated code style"
- "review branch diff for weird comments/defensive checks/casts"

## Workflow

1. Set comparison base (default `main`) and inspect `git diff <base>...HEAD`.
2. Build a candidate list using `rg` over added lines (comments, catches, casts, lint ignores, placeholders, debug leftovers).
3. Review each candidate in full file context and compare with nearby local patterns.
4. Remove only inconsistent slop; keep behavior and domain-valid guards.
5. Re-run project checks (`bun check`, `bun typecheck`) and fix regressions.
6. Report exact files changed and what slop was removed vs intentionally kept.

## Slop checklist

Read and apply: [`references/slop-heuristics.md`](references/slop-heuristics.md)

## Guardrails

- Do not remove protections at trust boundaries (user input, auth, network, db, file I/O).
- Do not replace real typing with weaker typing.
- Prefer minimal edits over broad rewrites.
- Keep project conventions (hooks/query style, component patterns, naming).
