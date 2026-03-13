---
name: mill
description: "Write mill orchestration programs for parallel/sequential agent workflows, iterative Ralph Loop execution, and worktree-isolated development."
---

# mill

Use this skill whenever you are writing or reviewing a mill-based orchestration program (including pi-mill extension flows).

## Core rules

1. Keep `systemPrompt` (WHO/how) separate from `prompt` (WHAT/task).
2. Use `await` for sequential steps and `Promise.all` for independent parallel work.
3. Always pass an explicit `model` in `provider/model-id` format.
4. Check `exitCode`, `stopReason`, and `errorMessage` before trusting results.
5. Use `mill.observe.log(...)` for progress and diagnostics.

## Available patterns

- General orchestration patterns: `./references/patterns.md`
- Iterative Ralph Loop pattern: `./references/ralph-loop.md`
- Worktree-isolated parallel development: `./references/worktree.md`

Prefer these patterns before inventing new orchestration scaffolding.
