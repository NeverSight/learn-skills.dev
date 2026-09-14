---
name: codex
description: >
  codex when launching the local Codex CLI (`codex`) for a first-run
  install, interactive TUI, one-shot exec, stream, worktree, review,
  resume, login, MCP, or plugin command.
---

# Codex CLI

Default run is `codex exec -C <abs-dir> "<prompt>"`. Omit `--sandbox`.
`--sandbox workspace-write` is not auto-approve. Closest read-only match
is `--sandbox read-only`, which only constrains model-generated shell.
Review is `codex review`, a branch, not a `--plan` flag.

## Flags

| Flag                      | Default | Effect                                                                 |
| ------------------------- | ------- | ---------------------------------------------------------------------- |
| `exec`                    | yes     | Noninteractive one-shot                                                |
| `-C, --cd <DIR>`          | required when cwd is not the target | Working root                          |
| `--sandbox <mode>`        | omit    | User-named only. `read-only`, `workspace-write`, `danger-full-access`  |
| `-m, --model <model>`     | CLI     | Use that model. Only if the user named one                             |
| `--worktree`              | off     | Boolean. No name. Managed Git worktree                                 |
| `--wall-clock <duration>` | `15m`   | Parent wait before kill. Not a Codex flag                              |

No flags mean `codex exec -C <abs-dir>` and omit `--sandbox`. Bare `codex`
is the TUI.

## Iron laws

1. Default is `codex exec`. Bare `codex` is the TUI. `--sandbox workspace-write` is not auto-approve.
2. `--full-auto` is `BLOCKED`. `--search` or `--ask-for-approval` after `exec` is `BLOCKED`.
3. Gated flags need a named user waiver: `--dangerously-bypass-approvals-and-sandbox`, `--dangerously-bypass-hook-trust`, `--sandbox danger-full-access`, `--approve-for-me`, `--ask-for-approval never`, `--ignore-rules`. If `--sandbox` is rejected or a bypass is requested, follow `./references/sandbox.md`.
4. `--skip-git-repo-check` only when the user names it. Do not `git init` in `/tmp` to dodge the default check.

## 1. Resolve

Confirm `codex` is on PATH. If missing, follow First-run in
`./references/cli-surface.md`. Record workspace, prompt, mode, session,
worktree, sandbox, and `--wall-clock`. Check auth with `codex login status`.
Do not print secrets. Missing login is `BLOCKED`. Record:
`cmd | workspace | mode | session | worktree | gated | verified | terminal | wall-clock`.

Done when binary, workspace, mode, auth state, and wall-clock are recorded.

## 2. Authorize

Do not add `--sandbox` unless the user named one. Do not add a gated flag
without a named waiver. If `--sandbox` is rejected or a bypass is requested,
follow `./references/sandbox.md`.

Done when sandbox is omitted or authorized, gated flags are recorded or
absent, or the run is `BLOCKED` / `AWAITING_USER`.

## 3. Build the command

Construct argv from the Flags table. Quote the prompt. Pass `-C` when cwd
is not the target. No gated flag without a named waiver. If the user asked
to install, run the TUI, review, stream JSON, resume, log in, or manage
MCP or plugins, follow that recipe in `./references/cli-surface.md`.

Done when argv is recorded.

## 4. Run

Follow the matching recipe in `./references/orchestration.md` for one-shot,
streaming, worktrees, parallelism, or failures. Wait for exit or
`--wall-clock`. Do not kill a still-working process.

Done when the process exits or a named failure recipe applies.

## 5. Verify

Treat CLI text as unverified. Inspect `git status` and the diff. Run the
narrowest covering tests for edited executable code. `--sandbox read-only`
only constrains model-generated shell. It is not a tree-unchanged
guarantee. For parallel or worktree runs, verify each tree from
Parallelism in `./references/orchestration.md`.

Done when each requested outcome is observed or `BLOCKED` with evidence.

## 6. Report

Lead with terminal state. Restate cmd, mode, session, worktree, gated
waiver, wall-clock, and verification evidence.

Terminal values are `SUCCESS`, `BLOCKED`, `NO_CHANGES`, and `AWAITING_USER`.
