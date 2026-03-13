---
name: "portpilot-assistant"
description: "Use when users ask in Chinese or English to manage local dev ports via natural language (for example: pick an available port, inspect who uses port 3000, free a port, run port conflict doctor, or initialize .portmanrc). Route to PortPilot CLI commands; run read-only actions automatically and require detailed confirmation for write actions."
---

# PortPilot Assistant

Translate natural language into `portpilot` commands with safe defaults.

## Workflow

1. Classify intent into one of: `scan`, `who`, `pick`, `doctor`, `free`, `init`, `config`.
2. Resolve target port/range/path from user text; if absent, apply defaults.
3. For the first `portpilot` call in a new session, run one permission bootstrap to avoid repeated prompts (details below).
4. Execute read actions directly (`scan`, `who`, `pick`, `doctor`).
5. For write actions (`free`, `init --force`, `config migrate`), require explicit confirmation and show details.
6. Return concise conclusion first, then command output details.

## Intent mapping

- 帮我选个端口 / pick a port:
  - `portpilot pick --range 3000-3999 --count 1 --lease-ms 20000 --json`
- 扫描当前端口 / scan current used ports:
  - `portpilot scan --protocol both --json`
- 查看 3000 端口 / check port 3000:
  - `portpilot who 3000 --json`
- 释放 3000 端口 / free port 3000:
  - First `portpilot who 3000 --json`, then confirm, then `portpilot free 3000 --yes --json`
- 扫描冲突 / run doctor:
  - `portpilot doctor --json`
- 初始化配置 / init port config:
  - `portpilot init --dry-run --json` (default preview)

## Safety policy

- Read actions run automatically.
- Write actions require confirmation.
- Confirmation payload must include: `port`, `pid`, `command`, `cwd`, `startTime`, `action`.
- If dependency failure occurs, run `portpilot doctor --preflight --json` and return install/fix commands.

## Permission bootstrap (one-time)

- On the first `portpilot` action in a new session, proactively run one lightweight bootstrap command (`portpilot doctor --json`) with escalation.
- Resolve bundled CLI absolute path first (path-independent):
  - Preferred: `$CODEX_HOME/skills/portpilot-assistant/assets/portpilot/bin/portpilot.js`
  - Fallback for repo-local usage: `<repo>/.claude/skills/portpilot-assistant/assets/portpilot/bin/portpilot.js`
- In that one-time escalation request, set:
  - `sandbox_permissions: require_escalated`
  - `prefix_rule: ["node", "<resolved-portpilot-cli-absolute-path>"]`
- Explain that this is a one-time approval to avoid repeated prompts for future `portpilot` commands.
- After approval, run requested commands normally without escalation.
- If bootstrap was not done (or approval was denied), and a read action fails with permission errors (`Operation not permitted` / netlink denied / `lsof` denied), rerun once with escalation.
- Write actions still require explicit user confirmation before execution.

## Execution notes

- Run bundled CLI from this skill first: `assets/portpilot/bin/portpilot.js`.
- Fallback to npx only if bundled CLI is missing: `npx -y portpilot-cli@1 ...`.
- Always pass `--json` for machine-readable parsing in skill scripts.
