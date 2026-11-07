---
name: veer-cli
description: >-
  Operate Veer-managed worktrees, folder contexts, terminals, repos, automations, artifacts,
  skill sharing, worktree comments, and Veer's embedded browser through the `veer` CLI. Use
  when the user says "$veer-cli", "Veer worktree", "child worktree", "spawn codex/claude in a
  worktree", "read/wait/send Veer terminal", "handoff" / "handover" / "give this to another
  agent", "Veer browser", "orca artifacts", or "share skills". Prefer it over raw git
  worktree, ad hoc PTYs, or Computer Use when Veer state is involved. Use Computer Use only
  when a visible window needs GUI control that a CLI, filesystem, or API cannot do.
---

# Veer CLI

This discovery stub loads the version-matched guide from the Orca executable used for this session.

## Resolve the CLI for this session

Choose the executable once and reuse it for every later command:

- If `VEER_CLI_COMMAND` is set, use its value. Otherwise use `ORCA_CLI_COMMAND`
  when set; Veer exports that compatibility variable in managed sessions.
- Otherwise, in a dev checkout whose session exposes `VEER_DEV_REPO_ROOT` or
  `ORCA_DEV_REPO_ROOT`, use `veer-dev`.
- Otherwise, on Linux outside a Veer-managed terminal, use `orca-ide`. Never run bare
  `orca` there — it normally resolves to the GNOME Orca screen reader (`/usr/bin/orca`).
- Otherwise, use the packaged `orca` compatibility CLI.

Below, `ORCA` is a placeholder for the executable you resolved. Substitute it before
running anything; do not create a shell variable or run `ORCA` literally. This works the
same way in POSIX shells, PowerShell, and cmd.exe.

If the selected executable cannot run, report its exact error and stop. Do not fall through
to another executable, which could silently target a different Veer build.

## Load the version-matched guide before running Orca commands

```text
ORCA skills get veer-cli
```

Prefer `--json`. Use the selected executable's `--help` for commands or flags the guide does
not cover. If a command reports that Veer is not running, start it with `ORCA open --json`
and retry. If it fails with `runtime_access_denied`, your sandbox blocked the connection:
re-run it with escalated permissions, and do not run `ORCA open` or restart Veer. If
`skills get` is unknown, explain that updating Veer restores the guide; use `--help` for
read-only discovery and do not guess unsupported commands.
