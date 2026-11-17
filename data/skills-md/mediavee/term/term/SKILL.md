---
name: term
description: Open and drive persistent terminal sessions (tmux-backed) whose shell state — cwd, env, sudo, an open SSH connection, a REPL — survives across commands. Use when a task needs a shell kept alive between commands instead of one-shot shells, e.g. running several commands over a single SSH connection.
license: MIT
compatibility: Requires tmux
metadata:
  author: mediavee
  version: "1.0"
---

Persistent terminals via the bundled CLI at `scripts/term`. Invoke it as `${CLAUDE_SKILL_DIR}/scripts/term` on Claude Code, or `scripts/term` relative to this skill on other agents (shown below as `term`). Run `term` with no args for the full help.

- `term open <name> [command...]` — start a session; optional first command (e.g. `ssh host`)
- `term run <name> [-t SECS] <command>` — run a command, wait, return output + exit code (works through SSH; exits with the command's code)
- `term wait <name> [-t SECS] <pattern>` — wait until a regex appears on screen (REPL prompts, "ready" lines, login prompts)
- `term send <name> <text...>` — type a line + Enter (interactive prompts, passwords)
- `term key <name> <key...>` — raw keys (C-c, Up, C-d)
- `term read <name> [lines]` — show recent output
- `term attach <name>` — attach to a session (human, needs a TTY)
- `term list` / `term close <name>` / `term reset`

`run` expects a POSIX shell and one logical command (chain with `&&`, `;`, `|`). For a prompt that blocks (sudo/ssh password) or a REPL/TUI, use `send` + `read` instead of `run`. If `run` times out, the command keeps running — poll with `read`, don't re-send.
