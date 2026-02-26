---
name: feishu-tasks
description: Create, read, and manage Feishu tasks with automatic user authorization. Use when you need to create tasks that your user can directly edit, read task lists, manage task details, or check calendar events. Supports automatic token refresh and persistence across sessions. All operations are performed with user identity, ensuring proper permissions.
---

# Feishu Tasks

Manage Feishu tasks with automatic user authorization. This skill handles OAuth token refresh and creates tasks that your user owns and can edit directly.

## Quick Start

### Create a task for your user

```bash
bash scripts/create_task.sh "Task Name" "Task Description"
```

Returns task ID, GUID, and link.

### List tasks

```bash
bash scripts/list_tasks.sh
```

### Get task details

```bash
bash scripts/get_task.sh <task_guid>
```

### Update a task

```bash
bash scripts/update_task.sh <task_guid> "New Summary" "New Description"
```

### Complete a task

```bash
bash scripts/complete_task.sh <task_guid>
```

## Workflow Example

```bash
# 1. Create a task
TASK_ID=$(bash scripts/create_task.sh "Learn 10 IELTS phrases" "Master common phrases")

# 2. List all tasks to verify
bash scripts/list_tasks.sh

# 3. Complete the task when done
bash scripts/complete_task.sh "<task_guid>"
```

## Setup

### Prerequisites

- User must authorize with Feishu OAuth (one-time setup)
- Credentials stored at `~/.feishu-credentials.json`
- Required permissions: `offline_access task:task:read task:task:write`

### Verify Setup

```bash
bash scripts/verify_setup.sh
```

## Important Notes

### Token Management

- **Automatic refresh**: `refresh_token` is automatically refreshed when `user_access_token` expires
- **Long-term access**: `offline_access` permission enables indefinite token refresh
- **User identity**: All operations use your user token, not app token → tasks you create are yours to edit

### Task Ownership

- Tasks created with this skill are owned by **your user account**
- You have full editing permissions in Feishu UI
- No permission issues like app-created tasks

### Credential Storage

Credentials are stored in `~/.feishu-credentials.json`:

```json
{
  "app_id": "cli_...",
  "app_secret": "...",
  "user_access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "scope": "offline_access task:task:read ..."
}
```

This file contains sensitive tokens. Keep it secure.

## Troubleshooting

### "Unauthorized" Error

Usually means `user_access_token` has expired and `refresh_token` refresh failed:

```bash
bash scripts/verify_setup.sh
```

If tokens are invalid, you'll need to re-authorize through OAuth flow.

### "Task not found"

Verify the task GUID is correct. List tasks to check:

```bash
bash scripts/list_tasks.sh
```

### Token Refresh Issues

The skill attempts automatic refresh. If it fails:

1. Check network connectivity
2. Verify credentials file exists and is valid
3. Run `verify_setup.sh` for diagnostics

## Scripts Reference

See [references/scripts.md](references/scripts.md) for complete script documentation and API endpoints.

## API Reference

See [references/api.md](references/api.md) for Feishu Task API details and response formats.

## Tips

- **Batch operations**: Create multiple tasks in a loop using `create_task.sh`
- **Task templates**: Store common task descriptions as environment variables for quick creation
- **Integration**: These scripts can be called from cron jobs or other automation
