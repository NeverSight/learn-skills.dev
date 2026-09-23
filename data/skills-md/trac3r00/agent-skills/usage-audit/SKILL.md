---
name: usage-audit
description: Cross-client token and session accounting. Every AI agent client records what it consumed — Claude Code per-message usage JSONL, Codex token_count events, OpenCode per-session token columns — but none shows the cross-client total. Reads the same local stores as session-handoff (read-only, nothing uploaded) and reports tokens by model, client, and project, with an optional budget gate.
when_to_use: You run multiple agent clients and want to know where tokens actually go — which model, which project, which client — or want a cron/CI tripwire when consumption exceeds a budget. NOT a billing tool; token counts are what clients recorded locally, and cache tokens are reported separately.
version: 1.0.0
license: MIT
metadata:
  agentskills:
    tags: [usage, tokens, cost, accounting, multi-agent]
---

# Usage Audit

You cannot manage what no client will show you: cross-client, cross-project
token consumption, from the logs already on your disk.

## Commands

```bash
python3 scripts/usage_audit.py                        # last 30 days, by model
python3 scripts/usage_audit.py --by project           # where tokens go
python3 scripts/usage_audit.py --by client --since 7  # which client burns most
python3 scripts/usage_audit.py --budget-tokens 50000000 || notify  # tripwire
python3 scripts/usage_audit.py --json                 # full report, all groupings
```

## Stores read (read-only, local)

| Client | Source |
|---|---|
| Claude Code | `~/.claude/projects/*/*.jsonl` per-message `usage` blocks |
| Codex | `~/.codex/sessions/**/rollout-*.jsonl` final `token_count` totals |
| OpenCode / OMO | `opencode.db` session token columns |

Missing stores are skipped silently. Cache tokens are tracked separately from
input/output so cached-heavy workflows read honestly.

## Pairs with

`context-budget` (why is per-turn cost high) answers the static question;
`usage-audit` answers the historical one (where did tokens actually go).
`session-handoff` shares the same store-reading conventions.
