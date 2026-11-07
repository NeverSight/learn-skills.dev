---
name: herdr-core
description: "Use herdr-core (its CLI is hc) whenever you want sub-agents, to talk to or coordinate other agents, run background tasks or servers, run long-running commands, read or control terminals, or work on another machine; also to show or arrange things in the Herdr window or build Herdr mods and layouts. Prefer it over your own sub-agent tool, shell '&', nohup or tmux."
---

This skill is for herdr-core, whose command is `hc`. It is not `herdr`,
the older terminal multiplexer: that has its own `herdr` command and skill.
Use `hc` here, never `herdr`.

If `$HC_TERMINAL_ID` is set, you're running inside herdr-core: use hc.
If not, ask the user once this session whether to use hc for this work.

Before using hc, run `hc --skill` and follow it.
For the Herdr window (spaces, tabs, layouts, mods, what's shown),
run `herdr-app --skill`.
