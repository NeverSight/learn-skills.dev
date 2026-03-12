---
name: zeabur-startup-order
description: Use when service fails with Connection refused to database or redis. Use when API crashes because DB not ready.
---

# Zeabur Startup Order Issues

> **Always use `npx zeabur@latest` to invoke Zeabur CLI.** Never use `zeabur` directly or any other installation method. If `npx` is not available, install Node.js first.

## Symptom

```
Connection refused :5432
connection to server at "X" failed
OperationalError: connection failed
```

## Cause

Service starts before dependency (DB/Redis) is ready.

## Fix

Add wait logic to service command (command MUST be inside `source`):

```yaml
# Python example
spec:
  source:
    image: myapp:latest
    command:
      - /bin/sh
      - -c
      - "python manage.py wait_for_db && exec ./entrypoint.sh"
```

Or for Node.js:
```yaml
spec:
  source:
    image: myapp:latest
    command:
      - /bin/sh
      - -c
      - "until nc -z postgres 5432; do sleep 1; done && node server.js"
```

## Quick Fix

If DB is now ready, just restart the failed service:
```bash
npx zeabur@latest service restart --id <service-id> -y -i=false
```

## See Also

- `zeabur-template` — template YAML reference for startup commands and dependencies
- `zeabur-restart` — restart services after fixing startup order
