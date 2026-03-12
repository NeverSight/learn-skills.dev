---
name: obsidian-canvas-architect
description: "Programmatically create and manipulate Obsidian Canvas (.canvas) files using JSON Canvas Spec 1.0. Enables agents to generate visual flowcharts, architecture diagrams, and planning boards. Use when creating or editing visual canvas files."
allowed-tools: Bash, Read, Write
---
# Obsidian Canvas Architect

**Status:** Active
**Author:** Richard Fremmerlid
**Domain:** Obsidian Integration
**Depends On:** `obsidian-vault-crud` (WP06)

## Purpose

Obsidian Canvas files (`.canvas`) use the JSON Canvas Spec 1.0 to define visual
boards with nodes (text, file references, URLs) connected by directional edges.
This skill lets agents programmatically generate visual planning boards, architecture
diagrams, and execution flowcharts.

## JSON Canvas Spec 1.0 Overview

A `.canvas` file is JSON with two top-level arrays:

```json
{
  "nodes": [
    {"id": "1", "type": "text", "text": "Hello", "x": 0, "y": 0, "width": 250, "height": 60},
    {"id": "2", "type": "file", "file": "path/to/note.md", "x": 300, "y": 0, "width": 250, "height": 60}
  ],
  "edges": [
    {"id": "e1", "fromNode": "1", "toNode": "2", "fromSide": "right", "toSide": "left"}
  ]
}
```

### Node Types
| Type | Required Fields | Purpose |
|:-----|:---------------|:--------|
| `text` | `text`, `x`, `y`, `width`, `height` | Inline text content |
| `file` | `file`, `x`, `y`, `width`, `height` | Reference to a vault note |
| `link` | `url`, `x`, `y`, `width`, `height` | External URL |
| `group` | `label`, `x`, `y`, `width`, `height` | Visual grouping container |

### Edge Properties
| Field | Required | Description |
|:------|:---------|:------------|
| `fromNode` | Yes | Source node ID |
| `toNode` | Yes | Target node ID |
| `fromSide` | No | `top`, `right`, `bottom`, `left` |
| `toSide` | No | `top`, `right`, `bottom`, `left` |
| `label` | No | Edge label text |

## Available Commands

### Create a Canvas
```bash
python ./scripts/canvas_ops.py create --file <path.canvas>
```

### Add a Node
```bash
python ./scripts/canvas_ops.py add-node \
  --file <path.canvas> --type text --text "My Node" --x 100 --y 200
```

### Add an Edge
```bash
python ./scripts/canvas_ops.py add-edge \
  --file <path.canvas> --from-node id1 --to-node id2
```

### Read a Canvas
```bash
python ./scripts/canvas_ops.py read --file <path.canvas>
```

## Safety Guarantees
- All writes go through `obsidian-vault-crud` atomic write protocol
- Malformed JSON triggers a clean error report, never a crash
- Node IDs are auto-generated (UUID) to prevent collisions
- Schema validation ensures all required fields are present before write
