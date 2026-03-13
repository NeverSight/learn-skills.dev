---
name: markdown-task-manager
description: Use when managing tasks, the system is a Kanban task manager based on local Markdown files (`kanban.md` and `archive.md`). It follows a strict format compatible with the task-manager.html web application.
---

# 📋 Markdown Task Manager Skill

## When to Use This Skill

- Create tasks to document work to be done
- Plan complex features
- Track project progress
- Archive completed tasks
- Generate status reports

## 📋 STRICT Task Format

### Mandatory Template

```markdown
### TASK-XXX | Task title

**Priority**: [Critical|High|Medium|Low] | **Category**: [Value] | **Assigned**: @user1, @user2
**Created**: YYYY-MM-DD | **Started**: YYYY-MM-DD | **Due**: YYYY-MM-DD | **Finished**: YYYY-MM-DD
**Tags**: #tag1 #tag2 #tag3

Free text description. **NO `##` or `###` headings allowed**.

**Subtasks**:
- [ ] First subtask
- [x] Completed subtask

**Notes**:
Additional notes with subsections `**Title**:`.

**Result**:
What was done.

**Modified files**:
- file.js (lines 42-58)
```

### ❌ FORBIDDEN

- `## Title` or `### Title` inside a task
- `**Subtasks**` or `**Notes**` without `:`
- Automatic archiving (only on user request)

**Why?** The HTML parser of the application does not recognize `##` inside tasks.

## 🔄 Workflow

### 1. New Request
1. Read `kanban.md` to get the last task ID
2. Create task in `kanban.md` → "📝 To Do" section
3. Unique ID (TASK-XXX) auto-incremented
4. Break down into subtasks if needed
5. Increment counter in `<!-- Config: Last Task ID: XXX -->`

### 2. Start Work
1. Move task → "🚀 In Progress" section
2. Add `**Started**: YYYY-MM-DD`
3. Check off subtasks progressively

### 3. Finish Work
1. Move → "✅ Done" section
2. Add `**Finished**: YYYY-MM-DD`
3. Document in `**Notes**:`:
   - `**Result**:` - What was done
   - `**Modified files**:` - List with line numbers
   - `**Technical decisions**:` - Choices made
   - `**Tests performed**:` - Validated tests

### 4. Archiving

**⚠️ Tasks are NOT archived immediately!**

- Completed tasks remain in "✅ Done"
- **Only on user request** → move to `archive.md`
- **Never archive directly at end of work**

## 📁 File Structure

### kanban.md

```markdown
# Kanban Board

<!-- Config: Last Task ID: 42 -->

## ⚙️ Configuration

**Columns**: 📝 To Do | 🚀 In Progress | 👀 Review | ✅ Done
**Categories**: Frontend, Backend, DevOps
**Users**: @alice, @bob
**Tags**: #bug, #feature, #docs

---

## 📝 To Do

### TASK-001 | Title
[...]

## 🚀 In Progress

## 👀 Review

## ✅ Done

### TASK-003 | Completed task
[...]
```

### archive.md

```markdown
# Task Archive

> Archived tasks

## ✅ Archives

### TASK-001 | Archived task
[... full content ...]

---

### TASK-002 | Another archived task
[... full content ...]
```

## 🎯 Golden Rules

### ✅ ALWAYS

1. Create task BEFORE coding
2. Strict format (no `##` inside tasks)
3. Break down if complex (3+ steps)
4. Update in real-time
5. Document result in `**Notes**:`
6. Reference tasks in commits (`TASK-XXX`)
7. Leave in "Done" (archive only on user request)

### ❌ NEVER

1. `## Title` inside a task
2. Code without creating task
3. Forget to check off subtasks
4. Archive immediately (stay in "Done")
5. Forget to document the result

## 🔧 User Commands

### Planning
- "Plan [feature]"
- "Create roadmap for 3 months"

### Execution
- "Do TASK-XXX"
- "Continue TASK-XXX"

### Tracking
- "Where are we?"
- "Weekly status"

### Modifications
- "Break down TASK-XXX"
- "Add subtask to TASK-XXX"

### Search
- "Search in archives: [keyword]"

### Maintenance
- "Archive completed tasks"

## 📝 Complete Examples

### Simple Task

```markdown
### TASK-001 | Fix login bug

**Priority**: Critical | **Category**: Backend | **Assigned**: @bob
**Created**: 2025-01-20 | **Due**: 2025-01-21
**Tags**: #bug #urgent

Users cannot log in. Error 500 in logs.

**Notes**:
Check Redis, related to yesterday's deployment.
```

### Complete Task with Result

```markdown
### TASK-042 | Notification system

**Priority**: High | **Category**: Backend | **Assigned**: @alice
**Created**: 2025-01-15 | **Started**: 2025-01-18 | **Finished**: 2025-01-22
**Tags**: #feature

Real-time notifications with WebSockets.

**Subtasks**:
- [x] Setup WebSocket server
- [x] REST API
- [x] Email sending
- [x] Notifications UI
- [x] E2E tests

**Notes**:

**Result**:
✅ Functional system with WebSocket, REST API and emails.

**Modified files**:
- src/websocket/server.js (lines 1-150)
- src/api/notifications.js (lines 20-85)

**Technical decisions**:
- Socket.io for WebSockets
- SendGrid for emails
- 30-day history in MongoDB

**Tests performed**:
- ✅ 100 simultaneous connections
- ✅ Auto-reconnection
- ✅ Emails < 2s
```

## 🛠️ Skill Functions

When using this skill, you must:

1. **Read kanban.md** to understand current state and get last ID
2. **Create tasks** following strict format
3. **Update tasks** by moving between sections
4. **Check off subtasks** progressively
5. **Document result** in Notes before marking Done
6. **Increment Last Task ID** in config comment
7. **Never archive** unless explicitly requested

## 📘 Git Integration

```bash
# Commits with reference
git commit -m "feat: Add feature (TASK-042 - 3/5)"
git commit -m "fix: Bug fix (TASK-001)"

# Branches
git checkout -b feature/TASK-042-notifications
```

## ⚠️ Critical Points of Attention

1. **Markdown Format**: Strictly respect format (no `##` inside tasks)
2. **ID Increment**: Always increment `<!-- Config: Last Task ID: XXX -->`
3. **Columns**: Use exact column names defined in Configuration
4. **Archiving**: NEVER archive automatically, only on request
5. **Documentation**: Always fill `**Notes**:` with Result, Modified files, etc.

## 🎓 Usage

### Initialization

Before using the skill, verify the project contains:
- `kanban.md` (required)
- `archive.md` (required)
- `AI_WORKFLOW.md` (optional but recommended)

### First Use

```
"Use the markdown-task-manager skill to create a task for [feature]"
```

### Invocation Examples

```
"Skill markdown-task-manager: create a task to implement authentication"
"Skill markdown-task-manager: update TASK-007 with results"
"Skill markdown-task-manager: list all tasks in progress"
"Skill markdown-task-manager: archive completed tasks"
```

## 🔍 Implementation Details

### Reading kanban.md

Always start by reading `kanban.md` to:
- Get the last task ID from `<!-- Config: Last Task ID: XXX -->`
- Understand existing columns structure
- Check current tasks in each column

### Creating a New Task

1. Calculate new ID: `last_id + 1`
2. Format as `TASK-XXX` (3 digits with leading zeros)
3. Add to "📝 To Do" section
4. Update `<!-- Config: Last Task ID: XXX -->` comment
5. Use today's date for `**Created**:`

### Moving Tasks Between Columns

When moving a task:
1. Copy entire task content (from `### TASK-XXX` to blank line before next task)
2. Paste in target column section
3. Delete from original location
4. Update dates accordingly (`**Started**:` or `**Finished**:`)

### Completing Tasks

Before moving to "✅ Done":
1. Ensure all subtasks are checked `[x]`
2. Add `**Finished**: YYYY-MM-DD`
3. Fill in `**Notes**:` section with:
   - `**Result**:` describing what was accomplished
   - `**Modified files**:` listing changed files with line ranges
   - `**Technical decisions**:` if any choices were made
   - `**Tests performed**:` if tests were run

### Archiving Tasks

Only when user explicitly requests archiving:
1. Read task from "✅ Done" section in `kanban.md`
2. Append task to "## ✅ Archives" section in `archive.md`
3. Add separator `---` between archived tasks
4. Remove task from `kanban.md`

---

**This skill ensures complete traceability and total transparency of work done by AI.**
