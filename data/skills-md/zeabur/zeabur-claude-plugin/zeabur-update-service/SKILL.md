---
name: zeabur-update-service
description: Use when modifying service config without full redeploy. Use when updating env vars and restarting single service. Use when user says "change env var", "update config", or "fix variable without redeploying".
---

# Zeabur Update Service Without Redeploy

> **Always use `npx zeabur@latest` to invoke Zeabur CLI.** Never use `zeabur` directly or any other installation method. If `npx` is not available, install Node.js first.

## Workflow

```bash
# 1. Get service ID
npx zeabur@latest service list --project-id <project-id> -i=false

# 2. Check current variables
npx zeabur@latest variable list --id <service-id> -i=false

# 3. Add/update variables
npx zeabur@latest variable create --id <service-id> \
  --key "KEY1=value1" \
  --key "KEY2=value2" \
  -i=false -y

# 4. Restart service
npx zeabur@latest service restart --id <service-id> -y -i=false
```

## Caveats

| Issue | Solution |
|-------|----------|
| `${VAR}` references | Set in Dashboard, not CLI (shell expands to empty) |
| `variable update` clears vars | Use `variable create` instead |

## When to Use

- Fix environment variable typos
- Add missing config
- Change ports, URLs, credentials
- **No need to redeploy entire template**

## See Also

- `zeabur-service-list` — get service IDs needed for updates
- `zeabur-variables` — detailed guide on variable management
- `zeabur-restart` — restart service after config changes
