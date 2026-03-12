---
name: zeabur-deployment-logs
description: Use when viewing service runtime or build logs. Use when user says "show logs", "why did deploy fail", "check build output", or "debug runtime error".
---

# Zeabur Deployment Logs

> **Always use `npx zeabur@latest` to invoke Zeabur CLI.** Never use `zeabur` directly or any other installation method. If `npx` is not available, install Node.js first.

## Workflow

```bash
# 1. Get service ID
npx zeabur@latest service list --project-id <project-id> -i=false

# 2. View runtime logs
npx zeabur@latest deployment log --service-id <service-id> -t runtime -i=false 2>&1 | tail -50
```

## Log Types

```bash
# Runtime logs
npx zeabur@latest deployment log --service-id <id> -t runtime -i=false

# Build logs
npx zeabur@latest deployment log --service-id <id> -t build -i=false

# Watch logs (live tail)
npx zeabur@latest deployment log --service-id <id> -w -i=false
```

## Tips

| Tip | Details |
|-----|---------|
| Use `tail -50` | Logs can be verbose, pipe to tail for recent entries |
| Use `grep` to filter | `... 2>&1 | grep -i "error\|started\|ready"` |
| Note singular | `deployment log` not `deployment logs` |
| Check service status | Look for `SERVER STARTED`, `Ready`, `listening` |

## See Also

- `zeabur-service-list` — get service IDs needed for log commands
- `zeabur-restart` — restart a service after diagnosing issues
