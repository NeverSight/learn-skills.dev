---
name: manage-caffeinate
description: "Turn macOS caffeinate sleep prevention on or off, check its status, or explain the launchd-backed setup. Use when the user says to enable, disable, start, stop, toggle, inspect, or troubleshoot caffeinate / coffee Nate / keep-awake behavior for local terminal, Codex, Claude Code, or other agent workflows."
---

# Manage Caffeinate

## Overview

Use this skill to manage a machine-level macOS `caffeinate` job. This is not Codex-specific; it keeps the Mac awake for any local terminal, Codex, Claude Code, browser, or agent process that depends on the machine staying awake.

The preferred mechanism is a launchd-managed job named `agentdesk-caffeinate`, which runs:

```bash
/usr/bin/caffeinate -dimsu
```

## Workflow

Run the bundled script from the installed skill:

```bash
bash "$HOME/.codex/skills/manage-caffeinate/scripts/manage-caffeinate.sh" status
bash "$HOME/.codex/skills/manage-caffeinate/scripts/manage-caffeinate.sh" on
bash "$HOME/.codex/skills/manage-caffeinate/scripts/manage-caffeinate.sh" off
```

If the skill is being run from a cloned AgentDesk checkout instead of an installed Codex skill, run:

```bash
bash "skills/manage-caffeinate/scripts/manage-caffeinate.sh" status
```

## Commands

- `on`: create or refresh the launchd job. Also removes the legacy `codex-caffeinate` label if present.
- `off`: remove the launchd job and clean up matching managed `/usr/bin/caffeinate -dimsu` processes.
- `status`: show launchd status and `pmset -g assertions` caffeinate lines.
- `restart`: remove and recreate the launchd job.

## Verification

After turning it on, verify `pmset -g assertions` lists `/usr/bin/caffeinate` or a `caffeinate command-line tool` assertion with `PreventUserIdleSystemSleep`, `PreventUserIdleDisplaySleep`, and `PreventSystemSleep`.

After turning it off, verify `launchctl list agentdesk-caffeinate` fails and `pmset -g assertions` no longer lists the caffeinate assertions.

## Reference

Read [references/setup.md](references/setup.md) when you need to explain how the launchd setup works, why launchd is used instead of a background shell process, or what was initially configured on Arthur's machine.

## Boundaries

`caffeinate` prevents idle sleep while macOS allows the assertion. Closing a MacBook lid can still force sleep unless the machine is in a supported clamshell setup, typically connected to power and external display/input.
