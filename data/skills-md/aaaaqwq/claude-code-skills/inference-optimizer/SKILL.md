---
name: inference-optimizer
description: Audit OpenClaw token usage, purge stale sessions, and optimize inference speed. Use when the user sends /optimize, /audit, asks to purge sessions, or wants a token/workspace audit.
license: MIT
metadata:
  author: clawdbot
  version: "0.1.0"
---

# Inference Optimizer

Optimize OpenClaw for maximum inference speed and minimum token usage. When user sends `/optimize` or `/audit`, exec the audit script and return raw output. When user approves purge, exec the purge script.

## Triggers

- `/optimize` — run audit
- `/audit` — same as /optimize
- "purge sessions", "purge stale", "clean up sessions" — after audit, if user approves

## Workflow

1. **Audit:** Exec `bash <skill_dir>/scripts/openclaw-audit.sh`, return raw output. Do NOT ask what to optimize. Do NOT list options.
2. **Purge:** If user approves purge after audit, exec `bash <skill_dir>/scripts/purge-stale-sessions.sh`, return raw output.
3. **Full optimization:** For Task 1–5 (workspace rewrite, heartbeat, deploy), read `optimization-agent.md` and follow its flow.

## Path Resolution

Scripts live at `~/clawd/skills/public/inference-optimizer/scripts/` (or wherever the skill is installed). Use that path when exec-ing.

## Allowlist

Purge script needs: `find`, `find *`, `find **`, `rm`, `rm *`, `rm **`, `bash`, `bash *`, `bash **`. Add to `exec-approvals.json` for the agent if purge is blocked.
