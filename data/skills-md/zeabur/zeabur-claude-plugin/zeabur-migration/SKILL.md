---
name: zeabur-migration
description: Use when services stuck on Waiting for database migrations to complete. Use when app expects separate migrator service.
---

# Zeabur Migration Issues

> **Always use `npx zeabur@latest` to invoke Zeabur CLI.** Never use `zeabur` directly or any other installation method. If `npx` is not available, install Node.js first.

## Symptom

```
Waiting for database migrations to complete...
Waiting for database migrations to complete...
(repeating forever)
```

## Cause

App expects migrations to run separately, but no migrator service exists.

## Solutions

### Option A: Add migration to API startup

```yaml
# In api service — command MUST be inside source
spec:
  source:
    image: myapp:latest
    command:
      - /bin/sh
      - -c
      - "python manage.py wait_for_db && python manage.py migrate && exec ./entrypoint.sh"
```

### Option B: Add migrator service

```yaml
- name: migrator
  spec:
    source:
      image: same-backend-image
      command:
        - ./bin/docker-entrypoint-migrator.sh
    env:
      DATABASE_URL: ...
```

**Option A is simpler** - migrations run on API startup and are idempotent (safe to repeat).

## See Also

- `zeabur-template` — template YAML reference for command placement
- `zeabur-deployment-logs` — check migration logs for errors
- `zeabur-startup-order` — similar issue where services start before dependencies are ready
