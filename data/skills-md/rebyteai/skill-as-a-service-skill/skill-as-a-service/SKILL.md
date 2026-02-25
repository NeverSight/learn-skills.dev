---
name: skill-as-a-service
description: |
  Run coding agents (Claude Code, Gemini, Codex) with skills in the cloud via API.
  Each task gets its own isolated VM. Use when you need to spawn sub-tasks,
  delegate work to other agents, or run tasks with specific skills.
  Requires REBYTE_API_KEY environment variable.
---

# Skill-as-a-Service API

Spawn coding agent tasks in the cloud via API. Each task gets its own isolated VM with skills pre-installed.

## Before You Start

Check that `REBYTE_API_KEY` is set:

```bash
echo "$REBYTE_API_KEY"
```

If empty, ask the user for their API key (get one at https://app.rebyte.ai/settings/api-keys), then:

```bash
export REBYTE_API_KEY="rbk_..."
```

## Create a Task

```bash
curl -s -X POST https://api.rebyte.ai/v1/tasks \
  -H "API_KEY: $REBYTE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Your task description here",
    "skills": ["deep-research"]
  }'
```

Response:
```json
{
  "id": "550e8400-...",
  "workspaceId": "660e8400-...",
  "url": "https://app.rebyte.ai/run/550e8400-...",
  "status": "running",
  "createdAt": "2026-02-09T10:30:00.000Z"
}
```

The `url` is live immediately. Give it to the user — they watch the agent work in real time. You do NOT need to poll or wait.

## Create a Task with Files

If the agent needs to work on files (PDFs, CSVs, images, etc.):

```bash
# 1. Get a signed upload URL
FILE_RESP=$(curl -s -X POST https://api.rebyte.ai/v1/files \
  -H "API_KEY: $REBYTE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"filename": "data.csv"}')

UPLOAD_URL=$(echo "$FILE_RESP" | jq -r '.uploadUrl')
FILE_ID=$(echo "$FILE_RESP" | jq -r '.id')
FILE_NAME=$(echo "$FILE_RESP" | jq -r '.filename')

# 2. Upload the file content
curl -s -X PUT "$UPLOAD_URL" \
  -H "Content-Type: application/octet-stream" \
  --data-binary @data.csv

# 3. Create a task with the file attached
curl -s -X POST https://api.rebyte.ai/v1/tasks \
  -H "API_KEY: $REBYTE_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"prompt\": \"Analyze this CSV and summarize findings\",
    \"skills\": [\"data-analysis\"],
    \"files\": [{\"id\": \"$FILE_ID\", \"filename\": \"$FILE_NAME\"}]
  }"
```

The file is copied into the task's VM at `/code/{filename}` before the agent starts.

## Create a Task with a GitHub Repo

```bash
curl -s -X POST https://api.rebyte.ai/v1/tasks \
  -H "API_KEY: $REBYTE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Add unit tests for the auth module",
    "skills": ["deep-research"],
    "githubUrl": "owner/repo",
    "branchName": "main"
  }'
```

## Share Results Publicly

By default, tasks are visible only to org members. To share with anyone (no login required):

```bash
TASK_ID="the-task-id-from-create"
curl -s -X PATCH "https://api.rebyte.ai/v1/tasks/$TASK_ID/visibility" \
  -H "API_KEY: $REBYTE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"visibility": "public"}'
```

Response includes `shareUrl` — give this to anyone:
```json
{
  "visibility": "public",
  "shareUrl": "https://app.rebyte.ai/share/550e8400-..."
}
```

## Check Task Status (Optional)

You don't need to poll — the URL is live. But if you need to wait for completion:

```bash
curl -s "https://api.rebyte.ai/v1/tasks/$TASK_ID" \
  -H "API_KEY: $REBYTE_API_KEY" | jq '{status, url}'
```

Statuses: `running`, `completed`, `failed`, `canceled`

## Follow Up on a Task (Optional)

Send additional instructions to a running or completed task:

```bash
curl -s -X POST "https://api.rebyte.ai/v1/tasks/$TASK_ID/prompts" \
  -H "API_KEY: $REBYTE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Now fix the issues you found"}'
```

## Reuse a Workspace (Optional)

Pass `workspaceId` from a previous task to skip VM provisioning (much faster):

```bash
# First task creates a new VM
TASK1=$(curl -s -X POST https://api.rebyte.ai/v1/tasks \
  -H "API_KEY: $REBYTE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Set up the project", "githubUrl": "owner/repo"}')
WS_ID=$(echo "$TASK1" | jq -r '.workspaceId')

# Second task reuses the same VM
curl -s -X POST https://api.rebyte.ai/v1/tasks \
  -H "API_KEY: $REBYTE_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"prompt\": \"Now add tests\", \"workspaceId\": \"$WS_ID\"}"
```

## Delete a Task

```bash
curl -s -X DELETE "https://api.rebyte.ai/v1/tasks/$TASK_ID" \
  -H "API_KEY: $REBYTE_API_KEY"
```

Returns HTTP 204 (no content).

## Create Task Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| prompt | string | Yes | Task description (max 100,000 chars) |
| executor | string | No | `opencode` (default), `claude`, `gemini`, `codex` |
| model | string | No | Model tier (default: `lite`) |
| files | object[] | No | Files from POST /v1/files. Each: `{"id": "...", "filename": "..."}` |
| skills | string[] | No | Skill slugs: `["deep-research", "pdf", "data-analysis"]` |
| githubUrl | string | No | GitHub repo (`owner/repo`) |
| branchName | string | No | Branch (default: `main`) |
| workspaceId | string | No | Reuse a workspace from a previous task |

## All Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /v1/files | Get signed upload URL for a file |
| POST | /v1/tasks | Create a task |
| GET | /v1/tasks | List tasks |
| GET | /v1/tasks/:id | Get task with status and prompts |
| POST | /v1/tasks/:id/prompts | Send a follow-up prompt |
| PATCH | /v1/tasks/:id/visibility | Set private/shared/public |
| DELETE | /v1/tasks/:id | Delete task |

## Bundled Python Client

This skill includes a Python client and CLI at `scripts/`. To use them:

```bash
# Find the skill directory
SKILL_DIR=$(find ~/.skills -maxdepth 1 -name '*skill-as-a-service*' -type d | head -1)

# Use the CLI
python3 "$SKILL_DIR/scripts/rebyte_cli.py" create --prompt "Hello world"
python3 "$SKILL_DIR/scripts/rebyte_cli.py" get TASK_ID
python3 "$SKILL_DIR/scripts/rebyte_cli.py" list

# Or use the client in Python
python3 -c "
import sys; sys.path.insert(0, '$SKILL_DIR/scripts')
from rebyte_client import RebyteClient
client = RebyteClient()
task = client.create_task(prompt='Hello world')
print(task['url'])
"
```

See [references/api.md](references/api.md) for full API details and [references/examples.md](references/examples.md) for more examples.
