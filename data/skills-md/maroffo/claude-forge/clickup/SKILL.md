---
name: clickup
description: "ClickUp task management via MCP. Use for task updates, comments, time tracking, workspace navigation. Always interact in English."
allowed-tools: [mcp__clickup__*]
compatibility: "Requires ClickUp MCP server connected and authenticated."
---

# ABOUTME: ClickUp MCP integration for task management and workflow automation
# ABOUTME: Task CRUD, comments, time tracking, workspace hierarchy, search

# ClickUp MCP Integration

## Critical Rules

1. **ALL content in English** - task names, descriptions, comments
2. **Never guess IDs** - always search or ask
3. **Read before update** - understand current state
4. **Check comments** - automation adds branch names, CI links

---

## Quick Reference

```
# Search → Get → Update flow
clickup_search → keywords: "task name"
clickup_get_task → task_id: "abc123"
clickup_update_task → task_id, status: "in progress"
clickup_get_task_comments → task_id (check for branch name)
clickup_create_task_comment → task_id, comment_text: "..."
```

---

All tools available via MCP: `clickup_*` prefix. See tool schemas for parameters.

**Key:** Always search before creating. Never guess IDs. `create_task` requires `list_id` - ask user.

---

## Workflow: Starting a Task

1. **Search:** `clickup_search` → keywords
2. **Get details:** `clickup_get_task` → task_id
3. **Check comments:** `clickup_get_task_comments` → find branch name
4. **Update status:** `clickup_update_task` → status: "in progress"
5. **Create branch** using name from comment

## Workflow: Completing a Task

1. **Add comment:** `clickup_create_task_comment` → "Completed. MR: https://..."
2. **Update status:** `clickup_update_task` → status: "ready for review"

---

## Git Integration

Branch format from automation: `<type>/<task-name>_CU-<task-id>`

Example: `feature/user-auth_CU-abc123`

1. Task created → automation adds branch comment
2. Read comment → get branch name
3. Work & commit → reference task ID
4. Create MR → link to task
5. Update status → "ready for review" → "complete"
