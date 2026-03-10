---
name: nocobase-api-call
description: Execute authenticated NocoBase API requests via a reusable shell script. Use when users ask to call NocoBase endpoints directly (GET/POST/PUT/PATCH/DELETE), inspect raw API responses, or run collection/field operations with a specific endpoint and payload.
argument-hint: "[method] [endpoint] [data-json-or-file]"
allowed-tools: Bash, Read
---

# Goal

Run direct NocoBase API requests in a deterministic, low-dependency way for reusable automation and distribution.

# Workflow

1. Confirm request inputs: HTTP method, endpoint, and optional JSON payload or file.
2. Ensure authentication config is available:
   - Preferred: read `NOCOBASE_URL` and `NOCOBASE_API_TOKEN` from environment variables.
   - Optional fallback: read `./.env` in user's current working directory.
   - If token is still missing and `./.env` does not exist, create `./.env` template first, then ask user to edit token.
   - Continue after user confirms token is set.
3. Execute `scripts/nocobase-api.sh`.
4. Return response JSON and HTTP status; if it fails, show the endpoint/method and the error message.

# Mandatory Auth Gate

- If `NOCOBASE_API_TOKEN` is missing, do not provide offline substitutes.
- You must guide the user to configure auth first, then resume the API task.
- Do not switch to "design doc only", "manual JSON only", or "one-click later" fallback outputs.
- Do not attempt to obtain token on behalf of user by calling login APIs or creating API keys automatically.
- If auth is not ready, stop API execution and ask user to complete token configuration manually.

# Missing-Token Response Template

When auth is missing, respond with short actionable instructions:

1. Explain token is required to proceed with API execution.
2. If `./.env` is missing, create it with template keys and ask user to edit `NOCOBASE_API_TOKEN`.
3. Ask user to confirm after setting token, then continue immediately.

# Environment Setup

Use this skill as the single source of truth for API environment config:

```bash
# preferred: export environment variables
export NOCOBASE_URL="http://localhost:13000"
export NOCOBASE_API_TOKEN="<your-token>"

# after token is ready:
skills/nocobase-api-call/scripts/nocobase-api.sh GET /collections:list
```

Alternative (temporary session):

```bash
export NOCOBASE_URL="http://localhost:13000"
export NOCOBASE_API_TOKEN="<your-token>"
```

# Resources

- `scripts/nocobase-api.sh` - Generic authenticated NocoBase API caller (`curl` based)
- `.env.example` - Reference template
- `.gitignore` - Excludes local `.env`

# Usage

```bash
# List collections
./scripts/nocobase-api.sh GET /collections:list

# Create collection from inline JSON
./scripts/nocobase-api.sh POST /collections:create '{"name":"products","title":"Products"}'

# Create from file
./scripts/nocobase-api.sh POST /collections:create ./payload.json

# Response body only (for script chaining)
./scripts/nocobase-api.sh --raw GET '/swagger:get?ns=plugins%2Fdata-source-main'
```
