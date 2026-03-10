---
name: collavre
description: Manage Collavre Creatives (hierarchical tasks/content blocks) via CLI. Use when creating, retrieving, updating, importing, or batch-operating on Creatives. Creatives are tree-structured items with automatic progress rollup — like a smart to-do list that doubles as a structured document.
---

# Collavre

CLI for managing Collavre Creatives via MCP protocol.

## Setup

```bash
# Configure (once)
collavre auth --url https://collavre.example.com --token <oauth_token>

# Verify
collavre list
```

The `collavre` script lives in `scripts/collavre`. Config is stored at `~/.config/collavre/config.json`.

## Commands

### List root creatives
```bash
collavre list
collavre list --level 5              # deeper tree
collavre list --format json          # structured output
```

### Get a creative subtree
```bash
collavre get 123
collavre get 123 --level 5 --comments
```

### Search
```bash
collavre search "project name"
collavre search "urgent" --tags "v2"
```

### Create
```bash
collavre create --parent 123 --desc "New task"
collavre create --parent 123 --desc "<h1>Rich content</h1>"
```

### Update
```bash
collavre update 456 --desc "Updated title"
collavre update 456 --progress 1.0        # mark complete (leaf only)
collavre update 456 --parent 789           # move
```

### Import markdown
```bash
collavre import --parent 123 --file plan.md
collavre import --parent 123 --stdin < plan.md
echo "# Quick\n## Plan" | collavre import --parent 123 --stdin
```

### Batch operations
```bash
collavre batch --file ops.json
```

ops.json format:
```json
[
  { "action": "create", "parent_id": 100, "description": "Task A" },
  { "action": "update", "id": 200, "progress": 1.0 },
  { "action": "delete", "id": 300 }
]
```

## Key Concepts

- **Tree structure**: Creatives nest via `parent_id`. Use `--level` to control depth.
- **Progress**: Leaf = manual (0.0 or 1.0). Parent = auto-calculated from children.
- **Import**: Markdown headings/bullets become nested Creatives.
- **Batch**: All-or-nothing transaction. Requires approval.
- **Description format**: Accepts HTML. Plain text auto-wraps in `<p>` tags.

For detailed MCP tool parameters, see [references/tool-reference.md](references/tool-reference.md).
