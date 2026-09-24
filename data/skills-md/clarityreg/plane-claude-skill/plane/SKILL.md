---
name: plane
description: Manage Plane.so projects, work items, cycles, and modules. Use when creating/updating issues, managing sprints, organizing work, or querying project status. Supports all Plane API operations without heavy MCP token overhead.
---

# Plane Project Management

Interact with Plane.so for project management tasks. This skill provides direct API access to Plane without the token overhead of MCP tool schemas.

## Quick Start

```bash
# Set environment variables first
export PLANE_API_KEY="your-api-key"
export PLANE_WORKSPACE_SLUG="your-workspace"
export PLANE_BASE_URL="https://api.plane.so"  # or your self-hosted URL
```

## Available Operations

### Projects
```bash
python ~/.claude/skills/plane/scripts/projects.py list
python ~/.claude/skills/plane/scripts/projects.py get <project_id>
python ~/.claude/skills/plane/scripts/projects.py create --name "Project Name" --description "Description"
python ~/.claude/skills/plane/scripts/projects.py update <project_id> --name "New Name"
python ~/.claude/skills/plane/scripts/projects.py delete <project_id>
python ~/.claude/skills/plane/scripts/projects.py members <project_id>
```

### Work Items (Issues)
```bash
python ~/.claude/skills/plane/scripts/work_items.py list <project_id>
python ~/.claude/skills/plane/scripts/work_items.py get <project_id> <item_id>
python ~/.claude/skills/plane/scripts/work_items.py create <project_id> --name "Task name" --priority "high"
python ~/.claude/skills/plane/scripts/work_items.py update <project_id> <item_id> --state "done"
python ~/.claude/skills/plane/scripts/work_items.py search <query>
```

### Cycles (Sprints)
```bash
python ~/.claude/skills/plane/scripts/cycles.py list <project_id>
python ~/.claude/skills/plane/scripts/cycles.py create <project_id> --name "Sprint 1" --start "2025-01-01" --end "2025-01-14"
python ~/.claude/skills/plane/scripts/cycles.py add-items <project_id> <cycle_id> --items "item1,item2"
python ~/.claude/skills/plane/scripts/cycles.py transfer <project_id> <from_cycle> <to_cycle>
```

### Modules
```bash
python ~/.claude/skills/plane/scripts/modules.py list <project_id>
python ~/.claude/skills/plane/scripts/modules.py create <project_id> --name "Feature Module"
python ~/.claude/skills/plane/scripts/modules.py add-items <project_id> <module_id> --items "item1,item2"
```

### Initiatives
```bash
python ~/.claude/skills/plane/scripts/initiatives.py list
python ~/.claude/skills/plane/scripts/initiatives.py create --name "Q1 Goals" --description "Quarterly objectives"
```

## Configuration

The skill reads configuration from `.claude/skills/plane/.env` or environment variables:

**Option 1:** Create `.env` in the skill directory:
```bash
cp .claude/skills/plane/.env.example .claude/skills/plane/.env
# Edit .claude/skills/plane/.env with your credentials
```

```env
PLANE_API_KEY=your-api-key
PLANE_WORKSPACE_SLUG=your-workspace
PLANE_BASE_URL=https://api.plane.so
```

**Option 2:** Set shell environment variables:
- `PLANE_API_KEY` - Your Plane API key (required)
- `PLANE_WORKSPACE_SLUG` - Your workspace slug (required)
- `PLANE_BASE_URL` - API base URL (default: https://api.plane.so)

Environment variables take precedence over `.env` file values.

## Token Efficiency

This skill replaces 55+ MCP tool schemas with on-demand script execution:
- **MCP approach**: All tool schemas loaded every request (~50k tokens)
- **Skill approach**: Only load what's needed (<500 tokens per operation)

## Detailed References

For full API schemas and advanced usage:
- [Tool Reference](references/tools.md) - Complete list of all operations
- [Schemas](references/schemas.md) - Request/response data structures
- [Workflows](references/workflows.md) - Common task patterns

## Examples

See [examples/](examples/) for common workflows:
- Creating a new project with initial issues
- Setting up a sprint cycle
- Bulk updating work items
- Generating project reports
