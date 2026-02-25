---
name: gms-mcp
description: GameMaker MCP workflow skills and command reference
metadata:
  openclaw:
    requires:
      anyBins:
        - gms
---

# GMS-MCP Skills

Task-oriented workflows and comprehensive command reference for GameMaker development.

## Workflows

Task-focused guides for common GameMaker development tasks.

### Creating Things
| Workflow | Task |
|----------|------|
| [setup-object](workflows/setup-object.md) | Create object with sprite and events |
| [setup-script](workflows/setup-script.md) | Create script with JSDoc |
| [setup-room](workflows/setup-room.md) | Create room with layers and instances |
| [orchestrate-macro](workflows/orchestrate-macro.md) | Create multi-asset systems |

### Modifying Things
| Workflow | Task |
|----------|------|
| [smart-refactor](workflows/smart-refactor.md) | Rename asset with reference updates |
| [duplicate-asset](workflows/duplicate-asset.md) | Copy asset to create variant |
| [update-art](workflows/update-art.md) | Replace sprite images |
| [manage-events](workflows/manage-events.md) | Add, remove, validate events |

### Deleting Things
| Workflow | Task |
|----------|------|
| [safe-delete](workflows/safe-delete.md) | Check dependencies before deletion |

### Understanding Code
| Workflow | Task |
|----------|------|
| [find-code](workflows/find-code.md) | Find definitions and references |
| [lookup-docs](workflows/lookup-docs.md) | Look up GML function documentation |
| [analyze-logic](workflows/analyze-logic.md) | Understand script behavior |
| [generate-jsdoc](workflows/generate-jsdoc.md) | Document functions |

### Running & Debugging
| Workflow | Task |
|----------|------|
| [run-game](workflows/run-game.md) | Compile and run the game |
| [debug-live](workflows/debug-live.md) | Send commands to running game |

### Project Health
| Workflow | Task |
|----------|------|
| [check-health](workflows/check-health.md) | Quick project validation |
| [check-quality](workflows/check-quality.md) | Detect code anti-patterns |
| [cleanup-project](workflows/cleanup-project.md) | Fix orphans and sync issues |
| [pre-commit](workflows/pre-commit.md) | Validate before committing |

---

## Reference

Comprehensive command documentation for when you need syntax details.

| Reference | Contents |
|-----------|----------|
| [asset-types](reference/asset-types.md) | All 14 asset types, options, naming conventions |
| [event-types](reference/event-types.md) | Event specifications, key codes |
| [room-commands](reference/room-commands.md) | Room, layer, instance operations |
| [workflow-commands](reference/workflow-commands.md) | Duplicate, rename, delete, swap |
| [maintenance-commands](reference/maintenance-commands.md) | All maintenance operations |
| [runtime-options](reference/runtime-options.md) | Platforms, VM/YYC, bridge |
| [symbol-commands](reference/symbol-commands.md) | Index, find, list operations |
| [doc-commands](reference/doc-commands.md) | GML documentation lookup, search, cache |

---

## Quick Commands

```bash
# Create
gms asset create object o_name --parent-path "folders/Objects.yy"
gms asset create script scr_name --parent-path "folders/Scripts.yy"
gms event add o_name create

# Run
gms run start
gms run stop

# Find
gms symbol find-definition name
gms symbol find-references name

# Docs
gms doc lookup draw_sprite
gms doc search collision
gms doc list --category Drawing

# Health
gms diagnostics --depth quick
gms maintenance auto --fix

# Delete safely
gms symbol find-references name  # Check first!
gms asset delete type name
```

---

## Installation

```bash
gms skills install                       # Install to ~/.claude/skills/
gms skills install --project             # Install to ./.claude/skills/
gms skills install --openclaw            # Install to ~/.openclaw/skills/
gms skills install --openclaw --project  # Install to ./skills/
gms skills list                          # Show installed skills
```
