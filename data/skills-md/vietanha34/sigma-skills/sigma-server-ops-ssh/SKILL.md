---
name: sigma-server-ops-ssh
description: SSH-first diagnostics for sigma-media-server. Collect bounded logs/status safely, run reusable troubleshooting workflows, and produce structured incident summaries.
---

# Sigma Server Ops (SSH)

Use this skill to diagnose `sigma-media-server` on remote hosts over SSH before investing in a full MCP implementation.

## Trigger Phrases
- "check sigma-media-server status"
- "analyze sigma server errors"
- "collect logs from prod server"
- "triage incident on sigma host"

## Tools
- Local shell with `ssh` access from client machine.
- Optional helper script: `scripts/collect_sigma_diagnostics.sh`.

## Preconditions
- SSH key-based auth is configured (`BatchMode=yes`, no interactive password prompt).
- Remote user has least-privilege read access to service status and logs.
- Target host is explicitly provided by user (or selected from approved aliases).
- If SSH is not ready, load `references/templates/ssh-prerequisites.md` and guide setup first.

## Guardrails
- Read-only diagnostics only.
- Never run restart/kill/write operations unless user explicitly asks in a separate step.
- Always bound collection by time and line count.
- Redact secrets/tokens from output.

## Workflow Router
1. Resolve inputs: `host`, `service` (default `sigma-media-server`), `since` (default `30m`).
2. Choose workflow:
   - Quick health check: load `references/workflows/01-quick-health-check.md`.
   - Error triage: load `references/workflows/02-error-triage.md`.
   - Incident write-up: load `references/workflows/03-incident-summary.md`.
3. Use `scripts/collect_sigma_diagnostics.sh` for deterministic collection when possible.
4. Render final answer using `references/templates/incident-report-template.md`.

## Minimal Response Contract
Always return:
- `Current status`: healthy/degraded/down
- `Evidence`: 3-10 key log lines/events with timestamps
- `Likely cause`: top hypothesis + confidence (low/med/high)
- `Next actions`: safe, ordered, and explicit

## Failure Handling
- SSH unreachable: classify `network/auth` and stop.
- Permission denied: report exact command that failed and required scope.
- No logs: verify service name and widen `since` once.
