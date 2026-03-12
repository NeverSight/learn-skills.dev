---
name: zeabur-variables
description: Use when managing Zeabur environment variables via CLI. Use when variables are empty or SERVICE_NOT_FOUND errors. Use when user says "set env var", "add variable", or "why is my variable empty".
---

# Zeabur Variables Management

> **Always use `npx zeabur@latest` to invoke Zeabur CLI.** Never use `zeabur` directly or any other installation method. If `npx` is not available, install Node.js first.

## Known Issues

1. **Use `--id` not `--name`** - name lookup unreliable
2. **`${VAR}` gets empty** - shell expands before CLI receives
3. **`variable update` may clear all vars** - bug in CLI

## Create Variables

```bash
# ✅ Use service ID
npx zeabur@latest variable create --id <service-id> \
  --key "KEY1=value1" \
  --key "KEY2=value2" \
  -y -i=false
```

## Variable References

```bash
# ❌ FAILS - shell expands ${VAR} to empty
--key "REDIS_URL=${REDIS_URI_INTERNAL}"

# ✅ Set references in Dashboard instead
```

## List Variables

```bash
npx zeabur@latest variable list --id <service-id> -i=false
```

**For `${VAR}` references → Use Zeabur Dashboard, not CLI.**

## See Also

- `zeabur-service-list` — get service IDs needed for variable commands
- `zeabur-update-service` — update variables and restart in one workflow
