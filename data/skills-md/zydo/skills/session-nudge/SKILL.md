---
name: session-nudge
description: >-
  Turn a periodic or one-time keepalive nudge on or off for the current coding-agent session (Claude Code,
  Codex CLI or Grok Build), set its pace, or show whether it is on. The nudge is a "[HH:MM:SS] Automated nudge:
  continue working ..." message that a background OS job (launchd / systemd timer / cron / Windows
  Task Scheduler) types into opted-in agent terminals, every 61 minutes by default. Use for
  "/session-nudge on|off|enable|disable|status", "nudge every 20 minutes", "nudge once at 2:01 AM", "turn the nudge off
  here", "别给这个 session 发 nudge", "每半小时 nudge 一次", "给那个 codex 窗口开 nudge", "nudge my grok window too", and when setting the nudge
  up or testing it on a new machine. Sessions are off by default.
---

# Session nudge

One helper does everything; run it with the Python 3.9+ on PATH:

```sh
python3 <this skill's directory>/scripts/nudge.py <action> [options]
```

## Map the request to an action

| User says | Run |
|---|---|
| `on`, `enable`, "turn nudges on here" | `on` |
| `off`, `disable`, "stop nudging this session" | `off` |
| nothing, `status`, "is the nudge on?" | `status` |
| a pace: "nudge every 20 minutes", "每半小时", "hourly", "every 1.5h" | `on --every N` |
| "nudge once at 2:01 AM local time" | `once --at 02:01` |
| a different terminal (e.g. a Codex or Grok Build window) | add `--pid N` |
| "test the nudge", or first use on a machine | `test` |
| change the default pace for new opt-ins | `install --interval N` |
| remove the background job | `uninstall` |

A pace turns the nudge on (or changes the pace of an already-enabled session).
Convert it to whole minutes yourself: "half an hour" -> 30, "every 2 hours"
-> 120, "1.5h" -> 90; anything under one minute becomes 1. With no pace,
`on` keeps the session's existing pace, else the default (61). The pace is per
session: other sessions keep theirs.

`once --at HH:MM` schedules the next local occurrence, or tomorrow if today's time has passed. The scheduler delivers it once and removes the entry. `off` also cancels a scheduled one-time nudge.

Report the helper's one-line result. Do not edit the scheduler job, the state
files or the templates by hand; the helper is the interface.

## First run on a machine: ask, then test

`status`, `on`, `once`, `install` and `test` first make sure the background job
exists and matches this skill's location, creating it from `templates/` for
the current OS if not (`off` never installs anything). Until an end-to-end
`test` has passed on this machine, their output also contains setup
questions:

```
ASK-USER [Header]: question
    - Option label: what to do if chosen
```

For each one, ask the user with your question tool (AskUserQuestion in Claude
Code: the bracketed word as header, the listed options as options; in agents without
one, ask in plain text). Do what the chosen option says. Then run `test`, and if it
fails, handle the `ASK-USER` lines it prints the same way and run `test` again
until it passes or the user stops. The `on` that printed the questions has
already taken effect, so there is no need to repeat it after the test; tell
the user the session's state plus one sentence on the test result. No
`ASK-USER` lines means this machine is already set up: skip `test`. Typical
questions:

- macOS: allow python3 to control iTerm2 (Automation permission; the first
  test triggers the system prompt).
- Linux: enable systemd lingering so the timer runs while logged out; start a
  cron daemon if only the cron fallback is available.
- Windows: register the task with highest privileges when agents run in an
  elevated terminal.
- Any OS: this terminal cannot be typed into -> run agent sessions in tmux,
  WezTerm (or iTerm2 on macOS).

`test` opens a throwaway terminal (tmux, WezTerm, iTerm2 window or Windows
console), has the real scheduler job fire at it, and checks the message
arrived and was submitted. `test --pid N` targets an existing agent terminal
instead (the nudge text really lands in that session).

## How it works

- Scheduler: launchd agent `local.session-nudge` (macOS), systemd user timer
  `session-nudge.timer` or a crontab line when there is no systemd user
  session (Linux), Task Scheduler task `session-nudge` (Windows). It runs
  `nudge.py fire` every minute; each tick nudges only sessions whose own
  interval has elapsed.
- Opt-ins live in the state directory (`~/.local/state/session-nudge/`, or
  `%LOCALAPPDATA%\session-nudge\` on Windows; `$SESSION_NUDGE_HOME`
  overrides), file `include`: one line per agent TUI PID with its pace and
  last nudge time. Keyed by PID, so an opt-in ends with its process and never
  sticks to a terminal a later session reuses. `nudge.log` there records every
  delivery and skip; `config.json` holds the default pace and the message
  (`{now}` and `{next}` are filled in).
- Delivery: tmux `send-keys`, WezTerm `cli send-text`, iTerm2 AppleScript
  (macOS), console input injection (Windows). Text first, then CR after 0.5s
  and again after 1s: Claude Code treats a CR in the same burst as pasted
  text, and the second CR is a no-op on an empty composer. Other terminals
  (Terminal.app, GNOME Terminal, VS Code's terminal without tmux) cannot be
  typed into and are logged as skipped. A session sitting at a permission
  prompt consumes the text there.

## Finding this session's terminal

- Claude Code: `CLAUDE_PID` is the TUI. Codex or anything else: the nearest
  ancestor process named `claude`, `codex` or `grok` that has a terminal.
- A Claude Code background session (`kind: bg` in
  `~/.claude/sessions/<pid>.json`) is shown through an attached TUI that the
  session files do not name; the helper takes the single interactive TUI in
  the same working directory. With several it lists them and changes nothing
  -- ask the user which window shows this session and rerun with `--pid N`.
- Find a PID by hand with `ps axww -o pid=,tty=,command= | grep -E 'claude|codex|grok'`
  (Windows: `Get-Process claude,codex,grok,node`). Headless processes (`claude -p`,
  `codex exec`, the codex app-server) have no terminal and are never nudged.
- The opt-in follows the TUI process, not the conversation: if that window is
  switched to another session, that session is nudged too.
