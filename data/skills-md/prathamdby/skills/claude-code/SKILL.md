---
name: claude-code
description: >
  claude-code when launching the local Claude Code CLI (`claude`) for a
  first-run install, interactive session, one-shot, stream, resume, worktree,
  or auth, MCP, or plugin command.
---

# Claude Code CLI

Default run is `claude --print --output-format text "<prompt>"` from the
target directory. Read-only is `--permission-mode plan`. `--print` writes
unless plan is set. Wrong cwd is `BLOCKED`.

## Flags

| Flag                     | Default | Effect                                              |
| ------------------------ | ------- | --------------------------------------------------- |
| `--print`                | yes     | Noninteractive. Writes unless plan is set           |
| `--permission-mode plan` | off     | Read-only                                           |
| `--model`                | CLI     | User-named only. Aliases: `fable`, `opus`, `sonnet` |
| `--resume <id>`          | off     | Resume that session. No picker under `--print`      |
| `--continue`             | off     | Continue the previous session in this directory     |
| `--worktree [name]`      | off     | Isolated worktree. Do not invent a path             |
| `--output-format`        | `text`  | With `--print`: `text`, `json`, or `stream-json`    |
| `--wall-clock`           | `15m`   | Parent wait before kill. Not a Claude flag          |

`--resume` conflicts with `--continue`. Conflict is `BLOCKED`. No flags mean
`--print`, omit permission mode, `text` output, from the target directory.

## Iron laws

1. `--print` can write. `--permission-mode plan` is read-only. Omit `--print`
   only for an asked-for TUI.
2. A skipped trust dialog is not skipped permissions. Never add
   `--dangerously-skip-permissions` or `--permission-mode bypassPermissions`
   to recover a prompt.
3. Gated, named waiver only: `--dangerously-skip-permissions`,
   `--allow-dangerously-skip-permissions`, and `--permission-mode` values
   `bypassPermissions`, `dontAsk`, and `auto`. Follow the gated table in
   `./references/permissions.md`.
4. `claude help` is `BLOCKED`. `claude remote-control` is not a help command.

## 1. Resolve

Confirm `claude` is on PATH. If missing, follow First-run in
`./references/cli-surface.md`. Record workspace, prompt, permission mode,
session, worktree, output format, and `--wall-clock`. Check auth with
`claude auth status --text`. Do not print secrets. Missing login is
`BLOCKED`. Record:
`cmd | workspace | mode | session | worktree | gated | verified | terminal | wall-clock`.

Done when binary, workspace, mode, auth state, and wall-clock are recorded.

## 2. Authorize

No gated flag without a named waiver. On a permission prompt under `--print`,
follow Print-mode prompts in `./references/permissions.md`. Do not add
`--dangerously-skip-permissions` because `--print` skipped a trust dialog.

Done when gated state is recorded, or the run is `BLOCKED` / `AWAITING_USER`.

## 3. Build the command

Construct argv from the Flags table. Add `--permission-mode plan` for
read-only work. Quote the prompt. Run from the target directory. If
`--output-format` is `json` or `stream-json`, follow `--print` output in
`./references/cli-surface.md`. If the user asked to install, update, or
run the interactive TUI, follow that recipe in `./references/cli-surface.md`.

Done when argv is recorded.

## 4. Run

Follow the matching recipe in `./references/orchestration.md` for one-shot,
streaming, sessions, worktrees, parallelism, cleanup, or failures. Wait for
exit or `--wall-clock`. Do not kill a still-working process.

Done when the process exits, a live handle is the intended outcome, or a
named failure recipe applies.

## 5. Verify

Treat CLI text as unverified. Inspect `git status` and the diff. Run the
narrowest covering tests for edited executable code. Read-only
`--permission-mode plan` must leave the tree unchanged. For parallel or
worktree runs, verify each tree from Parallelism in
`./references/orchestration.md`.

Done when each requested outcome is observed or `BLOCKED` with evidence.

## 6. Report

Lead with terminal state. Restate cmd, mode, session, worktree, gated
waiver, wall-clock, and verification evidence.

Terminal values are `SUCCESS`, `BLOCKED`, `NO_CHANGES`, and `AWAITING_USER`.
