---
name: vibe-kanban-mcp
description: >
  Use this skill whenever the user wants to work with Vibe Kanban via MCPorter CLI.
  Covers any workflow that creates, updates, lists, assigns, tags, links, or manages
  Vibe Kanban issues, projects, repositories, workspaces, or workspace sessions by
   running `mcporter call vibe_kanban.<tool>` commands in the terminal. This skill
  is the reference and workflow guide for resolving org/project/workspace IDs,
  configuring MCPorter, managing repo scripts, and starting or linking workspace
  sessions. Trigger even when the user only says things like "vibe kanban",
  "kanban", "mcporter", "mcporter call vibe_kanban", "create issue",
  "assign this issue", "start workspace session", "link workspace", or asks how to
  wire an agent, Claude Code, Codex, Cursor, OpenCode, Gemini, Copilot, Amp, Droid,
  or Qwen into Vibe Kanban programmatically.
---

# Vibe Kanban via MCPorter — Skill

This skill teaches agents to operate Vibe Kanban entirely through **MCPorter CLI**
commands. MCPorter bridges MCP servers to the terminal so any agent with shell
access can drive Vibe Kanban without editor-integrated MCP support.

All tool calls follow the pattern:

```bash
mcporter call vibe_kanban.<tool_name> param=value ...
```

> Source: `crates/mcp/src/task_server/tools/`  
> Last updated: 2026-03-09

---

## Quick navigation

| What you need | Reference file |
|---|---|
| MCPorter setup, call syntax, executors, workflows | [`references/overview.md`](references/overview.md) |
| `list_organizations`, `list_org_members`, `list_projects` | [`references/organizations-projects.md`](references/organizations-projects.md) |
| Create / list / get / update / delete issues | [`references/issues.md`](references/issues.md) |
| Assignees, tags, issue relationships | [`references/issues.md`](references/issues.md) |
| Workspaces, `start_workspace_session`, `link_workspace` | [`references/workspaces-sessions.md`](references/workspaces-sessions.md) |
| Repositories and script management | [`references/repos.md`](references/repos.md) |

---

## Tool module summary

| Module | Tools | Description |
|---|---|---|
| `organizations` | 2 | Organisation & member listing |
| `remote_projects` | 1 | Project listing |
| `remote_issues` | 5 | Issue CRUD |
| `issue_assignees` | 3 | Assignee management |
| `issue_tags` | 4 | Tag management |
| `issue_relationships` | 2 | Issue relationships |
| `workspaces` | 3 | Local workspace CRUD |
| `repos` | 4+ | Repository & script management |
| `task_attempts` | 2 | Workspace session start & link |
| `context` | N | ID resolution and context-related guidance |

---

## How to use this skill

1. **Ensure MCPorter is available** — see
   [`references/overview.md`](references/overview.md) for installation and Vibe Kanban
   server registration.

2. **Identify what the user wants to do** — pick the closest workflow from the table
   above and read the matching reference file.

3. **Always pass IDs explicitly** — `project_id`, `organization_id`, and
   `workspace_id` must be provided in every call. Resolve them first by calling the
   corresponding list tools.

4. **Follow the workflow examples** — each reference file contains end-to-end
   MCPorter command sequences. Always resolve IDs by calling list tools before using
   them in create/update/delete calls.

5. **Pick the right executor** — when calling `start_workspace_session`, the executor
   string must match one of the supported values.  
   Full list: [`references/overview.md`](references/overview.md) → "Supported Executors".
