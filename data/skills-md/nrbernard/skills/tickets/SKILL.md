---
name: tickets
description: Print a table of every open ticket (neither done nor wontfix) with its number, name, status and open blockers, or with `next [feature]` the one ticket to pick up.
disable-model-invocation: true
# status.mjs imports tickets.mjs, which the agent has no need to read.
argument-hint: "[next [feature]]"
allowed-tools: Bash(node */tickets/status.mjs), Bash(node */tickets/status.mjs *)
metadata:
  version: "0.2.0"
---

!`node ${CLAUDE_SKILL_DIR}/status.mjs $ARGUMENTS`

Reply with the output above, verbatim, and nothing else.
