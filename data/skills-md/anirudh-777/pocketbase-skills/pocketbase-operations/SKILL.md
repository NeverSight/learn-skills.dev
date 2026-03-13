---
name: pocketbase-operations
description: Use when you specifically need advanced PocketBase operational runbooks for backup, restore, incidents, and runtime diagnostics
---

# PocketBase Operations (Advanced)

## Overview
Use this for deeper production operations. Default to `pocketbase-agent-orchestrator` for quick management actions.

## Core Scripts
- `scripts/pb_creds_setup.sh`
- `scripts/pb_request.sh`
- `scripts/pb_api_logs.sh`
- `scripts/pb_healthcheck.sh`

## Optional Script
- `scripts/pb_logs.sh` (runtime logs from systemd/docker/file)

## Minimal Workflow
1. Validate health and critical endpoints.
2. Inspect API logs for failures and hot paths.
3. Verify backup posture and restore readiness.
4. Run incident response when degradation is detected.

## References
- [incident-runbook.md](references/incident-runbook.md)
- [backup-restore-checklist.md](references/backup-restore-checklist.md)
- [security-hardening.md](references/security-hardening.md)
