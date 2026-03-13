---
name: zeabur-service-list
description: Use when needing service IDs for other commands. Use when checking what services exist in a project. Use when user says "list services", "what's running", or "show my services".
---

# Zeabur Service List

> **Always use `npx zeabur@latest` to invoke Zeabur CLI.** Never use `zeabur` directly or any other installation method. If `npx` is not available, install Node.js first.

## Get Service IDs

```bash
npx zeabur@latest service list --project-id <project-id> -i=false
```

## Output Example

```
     ID              NAME        TYPE          CREATEDAT
-----------------+-------------+-------------+------------------
 696faeb192eadb...  postgresql   PREBUILT_V2   18 minute(s) ago
 696faeb192eadb...  api          PREBUILT_V2   18 minute(s) ago
 696faeb192eadb...  web          PREBUILT_V2   18 minute(s) ago
```

## Common Use Cases

| Need | Command |
|------|---------|
| Check variables | `variable list --id <service-id>` |
| View logs | `deployment log --service-id <id> -t runtime` |
| Restart service | `service restart --id <id> -y` |

**Always use `--id` not `--name`** — name lookup is unreliable.

## See Also

- `zeabur-update-service` — update env vars on a specific service
- `zeabur-variables` — manage environment variables
- `zeabur-restart` — restart a service
- `zeabur-deployment-logs` — view service logs
