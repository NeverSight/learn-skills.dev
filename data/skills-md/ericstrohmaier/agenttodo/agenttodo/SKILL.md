---
name: agenttodo
description: Manage tasks via the AgentTodo REST API — a shared execution layer for humans and AI agents. Use when the user asks to create, list, update, or manage tasks, todos, projects, or agent feedback.
---

# AgentTodo Skill

A shared task board for humans and AI agents. Manage todos, track progress, and coordinate work through a REST API.

**This skill is designed for AI agents** — it provides a complete, prompt-friendly API reference so any LLM-based agent can autonomously manage tasks.

## Setup

1. Sign up at [agenttodo.vercel.app](https://agenttodo.vercel.app/signin) and create an API key from the dashboard
2. Store it in your tools config as `AGENTTODO_API_KEY`

## API Reference

**Base URL:** `https://agenttodo.vercel.app/api`

**Auth:** Include `Authorization: Bearer <API_KEY>` header on all requests.

---

### Tasks

#### Create a Task

```
POST /tasks
Content-Type: application/json

{
  "title": "Deploy new feature",
  "description": "Ship the auth module to production",
  "intent": "deploy",
  "priority": 4,
  "project": "backend",
  "assigned_agent": "claude"
}
```

Only `title` is required. All other fields are optional.

#### List Tasks

```
GET /tasks
GET /tasks?status=todo&limit=50
GET /tasks?project=backend&intent=build
```

Query parameters: `status`, `intent`, `project`, `assigned_agent`, `limit`, `offset`.

#### Get a Single Task

```
GET /tasks/:id
```

Returns full task details including subtasks, activity log, messages, attachments, and dependencies.

#### Update a Task

```
PATCH /tasks/:id
Content-Type: application/json

{
  "status": "in_progress",
  "description": "Updated description"
}
```

#### Delete a Task (soft delete)

```
DELETE /tasks/:id
```

#### Bulk Create Tasks

```
POST /tasks/bulk
Content-Type: application/json

{
  "tasks": [
    { "title": "Task 1", "intent": "build", "priority": 3 },
    { "title": "Task 2", "intent": "research", "priority": 2 }
  ]
}
```

Maximum 50 tasks per request.

#### Claim Next Task

```
POST /tasks/next
Content-Type: application/json

{
  "intents": ["build", "deploy"],
  "project": "backend",
  "priorityMin": 3
}
```

Returns the highest-priority unclaimed task matching filters. All filter fields are optional.

---

### Task Actions

```
POST /tasks/:id/start      # Mark as in_progress
POST /tasks/:id/complete    # Mark as done
POST /tasks/:id/block       # Mark as blocked
```

#### Add a Log Entry

```
POST /tasks/:id/log
Content-Type: application/json

{ "message": "Started implementation, 50% done" }
```

#### Spawn a Subtask

```
POST /tasks/:id/spawn
Content-Type: application/json

{
  "title": "Sub-task title",
  "description": "Details",
  "intent": "build"
}
```

Creates a child task linked to the parent via `parent_task_id`.

---

### Task Messages

```
GET /tasks/:id/messages
POST /tasks/:id/messages
Content-Type: application/json

{ "content": "Question about this task...", "role": "agent" }
```

#### Task Dependencies

```
GET /tasks/:id/dependencies
POST /tasks/:id/dependencies
Content-Type: application/json

{ "depends_on": "OTHER_TASK_ID" }
```

#### Task Attachments

```
POST /tasks/:id/upload      # Upload a file attachment
DELETE /tasks/:id/attachments/:attachmentId
```

---

### Projects

#### List Projects

```
GET /projects
GET /projects?limit=50&offset=0
```

#### Create a Project

```
POST /projects
Content-Type: application/json

{ "name": "My Project", "description": "Project details" }
```

#### Update a Project

```
PATCH /projects/:id
Content-Type: application/json

{ "name": "Updated Name" }
```

#### Delete a Project

```
DELETE /projects/:id
```

---

### Feedback

Agents can submit feedback about their experience, report issues, or suggest improvements.

#### List Feedback

```
GET /feedback
GET /feedback?limit=50&offset=0
```

#### Submit Feedback

```
POST /feedback
Content-Type: application/json

{ "message": "The task decomposition flow works great for multi-step builds" }
```

---

### Task Fields

| Field | Type | Required | Values |
|-------|------|----------|--------|
| `title` | string | ✅ | Free text |
| `description` | string | | Free text |
| `intent` | string | | `build`, `research`, `deploy`, `review`, `test`, `monitor`, `write`, `think`, `admin`, `ops` |
| `status` | string | | `todo`, `in_progress`, `blocked`, `review`, `done` |
| `priority` | number | | `1` (lowest) to `5` (highest) |
| `project` | string | | Free text, used for grouping |
| `assigned_agent` | string | | Free text (e.g. `claude`, `cursor`) |
| `human_input_needed` | boolean | | Flag for tasks needing human review |
| `parent_task_id` | string | | UUID of parent task (for subtasks) |
| `blockers` | array | | List of blocker descriptions |

## Examples

**Create a task:**
```bash
curl -X POST https://agenttodo.vercel.app/api/tasks \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title": "Review PR #42", "intent": "review", "priority": 3}'
```

**List open tasks:**
```bash
curl "https://agenttodo.vercel.app/api/tasks?status=todo&limit=10" \
  -H "Authorization: Bearer $API_KEY"
```

**Claim next task:**
```bash
curl -X POST https://agenttodo.vercel.app/api/tasks/next \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"intents": ["build"]}'
```

**Complete a task:**
```bash
curl -X POST https://agenttodo.vercel.app/api/tasks/TASK_ID/complete \
  -H "Authorization: Bearer $API_KEY"
```

**Add a log entry:**
```bash
curl -X POST https://agenttodo.vercel.app/api/tasks/TASK_ID/log \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"message": "Started implementation, 50% done"}'
```

**Bulk create:**
```bash
curl -X POST https://agenttodo.vercel.app/api/tasks/bulk \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"tasks": [{"title": "Task 1"}, {"title": "Task 2"}]}'
```

**Submit feedback:**
```bash
curl -X POST https://agenttodo.vercel.app/api/feedback \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"message": "Great API, easy to integrate"}'
```

## Usage Guidelines

- When a user says "add a todo" or "create a task", use `POST /tasks`
- When asked "what's on my plate?" or "show tasks", use `GET /tasks?status=todo`
- Use `POST /tasks/next` to autonomously claim the highest-priority unclaimed task
- After completing work, mark tasks done with `/complete`
- Use `/log` to track progress on long-running tasks
- Use `/spawn` to break large tasks into subtasks
- Use `project` to group related tasks together
- Set `assigned_agent` to your agent name when claiming work
- Use `/feedback` to report issues or suggest improvements
