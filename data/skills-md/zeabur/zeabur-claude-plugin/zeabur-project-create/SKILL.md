---
name: zeabur-project-create
description: Use when creating a new Zeabur project. Use when deploying templates to a new project. Use when user says "create project", "new project", or "set up a new environment".
---

# Zeabur Project Create

> **Always use `npx zeabur@latest` to invoke Zeabur CLI.** Never use `zeabur` directly or any other installation method. If `npx` is not available, install Node.js first.

## Choosing a Region

**Do NOT hardcode or guess region codes.** Old region codes like `hnd1`, `tpe1` are deprecated. The region must always be derived from the user's server list.

**Step 1 — List the user's servers:**

```bash
npx zeabur@latest server list -i=false --json
```

**Step 2 — Ask the user which server to use:**

Present the server list to the user (show name, provider, and region for each) and **ask them to pick one**. Do NOT choose a server on the user's behalf. Also offer the option to rent a new server if none of the existing ones are suitable.

- If the user has **no servers**, guide them to rent one first using the `zeabur-server-rent` skill (or `zeabur-server-catalog` to browse options).

**Step 3 — Use the selected server ID with `server-` prefix as the region:**

The region code format is `server-<server-id>`, where `<server-id>` comes from the server list output.

> Some templates (e.g. with `REQUIRE_DEDICATED_SERVER`) can only be deployed on dedicated servers. If you get `Unsupported template (code: REQUIRE_DEDICATED_SERVER)`, rent a dedicated server and recreate the project with its region.

## Create Project

```bash
# Create project with name and region (region must be server-<server-id>)
npx zeabur@latest project create -n "<project-name>" -r "server-<server-id>" -i=false --json
```

## Get Project ID

```bash
# List projects as JSON and extract project ID by name
PROJECT_ID=$(npx zeabur@latest project list -i=false --json | jq -r '.[] | select(.name == "<project-name>") | ._id')
```

## Deploy Template to Project

```bash
# Deploy template file to specific project (non-interactive)
npx zeabur@latest template deploy -i=false --json \
  -f <template-file> \
  --project-id <project-id> \
  --var PUBLIC_DOMAIN=myapp \
  --var KEY=value
```

## Workflow

```bash
# 1. Find server ID
npx zeabur@latest server list -i=false --json

# 2. Create project (use server-<id> from step 1)
npx zeabur@latest project create -n "wrenai-prod" -r "server-<server-id>" -i=false --json

# 3. Get project ID
PROJECT_ID=$(npx zeabur@latest project list -i=false --json | jq -r '.[] | select(.name == "wrenai-prod") | ._id')
echo "Project ID: $PROJECT_ID"
echo "Dashboard: https://zeabur.com/projects/$PROJECT_ID"

# 4. Deploy template (non-interactive)
npx zeabur@latest template deploy -i=false --json -f template.yml --project-id $PROJECT_ID --var PUBLIC_DOMAIN=myapp
```

## See Also

- `zeabur-template-deploy` — detailed template deployment flags and troubleshooting
- `zeabur-server-rent` — rent a dedicated server before creating a project on it
