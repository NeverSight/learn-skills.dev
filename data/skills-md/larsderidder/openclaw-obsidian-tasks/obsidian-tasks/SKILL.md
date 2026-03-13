---
name: obsidian-tasks
description: Set up and manage an Obsidian task board with Kanban + Dataview. Creates a Tasks/Board.md pipeline (Backlog/Todo/In Progress/Review/Done), per-task notes with YAML frontmatter (status/priority/category/due), and dashboards via Dataview queries. Use for task tracking, moving cards between columns, keeping board + frontmatter in sync, and linking tasks to supporting notes/research.
---

# obsidian-tasks

Task management in Obsidian vaults using Kanban boards, Dataview dashboards, and structured task notes.

## Setup

Run the setup script to initialize a task board in an Obsidian vault:

```bash
python3 scripts/setup.py <vault-path> [--folder <name>] [--columns <col1,col2,...>]
```

- `vault-path`: Path to the Obsidian vault root
- `--folder`: Subfolder to create (default: `Tasks`)
- `--columns`: Kanban columns (default: `Backlog,Todo,In Progress,Review,Done`)

This creates:
- `<folder>/Board.md` - Kanban board (requires Kanban community plugin)
- `<folder>/Dashboard.md` - Dataview dashboard (requires Dataview community plugin)

Tell the user to install **Kanban** and **Dataview** community plugins if not already installed.

## Task Note Format

Each task is a separate markdown file with YAML frontmatter:

```markdown
---
status: todo
priority: P1
category: revenue
created: 2026-02-03
due: 2026-02-07
---

# Task Title

Description and notes here.

## References
- [[linked-document|Display Name]]

## Status
- [x] Step completed
- [ ] Step pending
```

### Frontmatter Fields

| Field | Values | Required |
|-------|--------|----------|
| status | backlog, todo, in-progress, review, done | yes |
| priority | P1, P2, P3 | yes |
| category | free text (revenue, content, research, setup, project) | yes |
| created | YYYY-MM-DD | yes |
| due | YYYY-MM-DD | no |
| parked_until | YYYY-MM-DD | no |

### Priority Labels on Board

Use emoji prefixes on the Kanban board for visual priority:
- 🔴 P1 (urgent)
- 🟡 P2 (normal)
- 🟢 P3 (backlog/parked)

## Managing Tasks

### Create a Task

1. Create a markdown file in the tasks folder with frontmatter
2. Add a card to Board.md in the appropriate column:
```
- [ ] [[Task Name]] 🔴 P1 @{2026-02-07}
```

### Move a Task

1. Update `status` in the task note's frontmatter
2. Move the card line in Board.md to the target column

### Complete a Task

1. Set `status: done` in frontmatter
2. Move to Done column and mark checkbox:
```
- [x] [[Task Name]] ✅ 2026-02-03
```

### Always update both Board.md AND the task note frontmatter to keep them in sync.

## Linking Documents

Use Obsidian `[[wikilinks]]` to connect tasks to supporting documents:

```markdown
## References
- [[2026-02-03-research-report|Research Report]]
- [[meeting-notes-jan|Meeting Notes]]
```

Store referenced documents in a sibling folder (e.g., `Research/` next to `Tasks/`).

## Dashboard Queries

The setup script creates a Dataview dashboard. Core queries:

**Tasks by priority:**
```dataview
TABLE status, category, due
FROM "<tasks-folder>"
WHERE priority = "P1" AND status != "done"
SORT due ASC
```

**Overdue tasks:**
```dataview
TABLE priority, category
FROM "<tasks-folder>"
WHERE due AND due < date(today) AND status != "done"
SORT due ASC
```

**Recently completed:**
```dataview
TABLE category
FROM "<tasks-folder>"
WHERE status = "done"
SORT file.mtime DESC
LIMIT 10
```
