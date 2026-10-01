---
name: aio-ade-cli
description: >-
  Use the public `aio-ade` CLI to operate AIO-ADE-managed worktrees, folder contexts,
  terminals, repos, automations, worktree comments, and the browser embedded
  inside the AIO-ADE app. Use when the user says "$aio-ade-cli", "use aio-ade cli",
  "AIO-ADE worktree", "child worktree", "cardStatus", "spawn codex/claude in a worktree",
  "read/wait/send AIO-ADE terminal", "terminal send", "full handoff", "handover",
  "give this to another agent", "another worktree", "AIO-ADE browser", or
  "control the browser inside AIO-ADE". Prefer this over raw `git worktree`, ad hoc
  PTYs, Playwright, or Computer Use when the task touches AIO-ADE-managed state.
  Use Computer Use for browser windows, webviews, or desktop UI outside AIO-ADE's
  embedded browser.
---

# AIO-ADE CLI

This file is a discovery stub, not the usage guide. The full, version-matched AIO-ADE CLI
reference is served by the `aio-ade` binary itself — kept out of this file on purpose so it
can never drift from the binary that will actually run your commands.

Engage AIO-ADE whenever its running editor/runtime is the source of truth: AIO-ADE-managed
worktrees, folder contexts, terminals, repos, automations, worktree comments, and the
browser embedded inside the AIO-ADE app. Triggers include "$aio-ade-cli", "AIO-ADE worktree",
"child worktree", "spawn codex/claude in a worktree", "read/wait/send AIO-ADE terminal",
"full handoff" / "handover" / "give this to another agent", and "control the browser
inside AIO-ADE". Use plain shell tools when AIO-ADE state does not matter.

## Resolve the CLI for this session

Choose the executable once and reuse it for every later command:

- If the `AIO_ADE_CLI_COMMAND` environment variable is set, use its value. AIO-ADE exports this
  for managed WSL sessions.
- Otherwise, in a dev checkout whose session exposes `AIO_ADE_DEV_REPO_ROOT`, use `aio-ade-dev`.
- Otherwise, use `aio-ade`. It is the same name on every platform: the pre-rebrand CLI needed a
  separate Linux name because a bare `orca` collided with the GNOME Orca screen reader
  (`/usr/bin/orca`), and `aio-ade` does not.
- Otherwise, use `aio-ade`.

Below, `AIO_ADE` is a placeholder for the executable you resolved. Substitute it before
running anything; do not create a shell variable or run `AIO_ADE` literally. This works the
same way in POSIX shells, PowerShell, and cmd.exe.

If the selected executable cannot run, report its exact error and stop. Do not fall through
to another executable, which could silently target a different AIO-ADE build.

## Load the full guide before running AIO-ADE commands

```text
AIO_ADE skills get aio-ade-cli
```

That prints the complete, version-matched guide for the exact binary that will handle your
next commands — worktrees, handoffs, terminals, automations, and the built-in browser.
Read it first, then run the specific command you need.

Don't guess subcommands or flags from memory or from a cached copy of this stub. They
change between AIO-ADE releases, and this file deliberately no longer lists them. Confirm the
app is up with `AIO_ADE status --json` (start it with `AIO_ADE open --json` if needed), and
prefer `--json` for agent-driven calls.

## If an older AIO-ADE does not recognize `skills get`

Use this fallback only when the selected binary explicitly reports that `skills get` is an
unknown command. Another failure is not proof of an older binary; report it rather than
guessing or changing executables. For a confirmed pre-guide binary, use only this bounded,
read-only bootstrap to orient. Do not dead-end and do not invent commands:

```text
AIO_ADE status --json
AIO_ADE worktree ps --json
AIO_ADE terminal list --json
```

Then tell the user that updating AIO-ADE restores the full, version-matched guide via
`AIO_ADE skills get aio-ade-cli`. Beyond these commands, ask the user rather than guessing a
command surface this older binary may not support.
