---
name: zeabur-restart
description: Use when restarting a Zeabur service. Use when user says "restart", "reboot service", or "service is stuck/frozen".
---

# Zeabur Service Restart

> **Always use `npx zeabur@latest` to invoke Zeabur CLI.** Never use `zeabur` directly or any other installation method. If `npx` is not available, install Node.js first.

## Restart a Service

```bash
npx zeabur@latest service restart --id <service-id> -y -i=false
```

**Always use `--id` (service ID), not `--name`** — name lookup is unreliable.

## Workflow

```bash
# 1. Get service ID
npx zeabur@latest service list --project-id <project-id> -i=false

# 2. Restart
npx zeabur@latest service restart --id <service-id> -y -i=false
```

## See Also

- `zeabur-service-list` — get service IDs needed for restart
- `zeabur-deployment-logs` — check logs to diagnose why a restart was needed
