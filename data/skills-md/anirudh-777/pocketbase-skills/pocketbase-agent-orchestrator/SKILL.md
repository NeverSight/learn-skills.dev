---
name: pocketbase-agent-orchestrator
description: Use when managing PocketBase work end-to-end and you want one default skill for setup, schema, auth, API, logs, and operations
---

# PocketBase Agent Orchestrator

## Overview
This is the default PocketBase skill. Start here for almost all requests.

## Default Flow
1. Run quick actions first for immediate operations.
2. Use advanced domain skills only when a task is deep in one area.
3. Before completion, run health and relevant log checks.

## Credentials
If credentials are missing, prompt the user to run secure setup first:

```bash
./skills/pocketbase-operations/scripts/pb_creds_setup.sh
set -a; source .env.pocketbase.local; set +a
```

Manual setup (if needed):

```bash
export PB_URL="https://your-pocketbase.example.com"
export PB_ADMIN_EMAIL="admin@example.com"
export PB_ADMIN_PASSWORD="replace-me"
```

Supported aliases in scripts:
- URL: `PB_URL` or `NEXT_PUBLIC_POCKETBASE_URL`
- identity: `PB_ADMIN_EMAIL` or `PB_SUPERUSER_EMAIL` or `POCKETBASE_SERVICE_EMAIL`
- password: `PB_ADMIN_PASSWORD` or `PB_SUPERUSER_PASSWORD` or `POCKETBASE_SERVICE_PASSWORD`

Secure handling rules:
- Never ask users to paste passwords into code files or committed docs.
- Keep secrets in ignored local env files or a secret manager.
- In production/CI, inject creds from platform secrets, not shell history.

## Quick Actions

### 1) Create collection

```bash
./skills/pocketbase-operations/scripts/pb_request.sh POST /api/collections '{
  "name": "tasks",
  "type": "base",
  "schema": [
    { "name": "title", "type": "text", "required": true },
    { "name": "done", "type": "bool" }
  ]
}'
```

### 2) List/update records

```bash
./skills/pocketbase-operations/scripts/pb_request.sh GET "/api/collections/tasks/records?page=1&perPage=20"
./skills/pocketbase-operations/scripts/pb_request.sh PATCH /api/collections/tasks/records/RECORD_ID '{"done": true}'
```

### 3) Fix rules

```bash
COLL_ID=$(./skills/pocketbase-operations/scripts/pb_request.sh GET "/api/collections?filter=name%3D%22tasks%22" | sed -n 's/.*"id":"\([^"]*\)".*/\1/p' | head -n 1)
./skills/pocketbase-operations/scripts/pb_request.sh PATCH "/api/collections/$COLL_ID" '{
  "listRule": "@request.auth.id != \"\"",
  "viewRule": "@request.auth.id != \"\"",
  "createRule": "@request.auth.id != \"\"",
  "updateRule": "@request.auth.id != \"\"",
  "deleteRule": "@request.auth.id != \"\""
}'
```

### 4) Health + API logs + backup

```bash
./skills/pocketbase-operations/scripts/pb_healthcheck.sh
./skills/pocketbase-operations/scripts/pb_api_logs.sh --status-gte 400 --match "candidates,applications,starred,resumes,candidate_activity_log,whatsapp_messages" --limit 80

tar -czf "pocketbase-backup-$(date +%Y%m%d-%H%M%S).tar.gz" /var/lib/pocketbase
```

## Optional Runtime Logs
Use only when you need service/container/file runtime logs:

```bash
./skills/pocketbase-operations/scripts/pb_logs.sh --lines 300 --since 1h
./skills/pocketbase-operations/scripts/pb_logs.sh --follow
```

## Advanced Skills (Use Only When Needed)
- `pocketbase-foundations`
- `pocketbase-data-modeling`
- `pocketbase-auth-and-access`
- `pocketbase-api-and-sdk`
- `pocketbase-automation-and-hooks`
- `pocketbase-operations`
