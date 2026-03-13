---
name: json-canvas
description: Create and edit JSON Canvas files (.canvas) with nodes, edges, groups, and connections. Use when working with .canvas files, creating visual canvases, mind maps, flowcharts, or when the user mentions Canvas files in Obsidian.
allowed-tools:
  - Read
  - Write
  - Edit
---

# JSON Canvas Skill

This skill enables Claude Code to create and edit valid JSON Canvas files (`.canvas`) used in Obsidian and other applications.

## Overview

JSON Canvas is an open file format for infinite canvas data. Canvas files use the `.canvas` extension and contain valid JSON following the [JSON Canvas Spec 1.0](https://jsoncanvas.org/spec/1.0/).

## File Structure

```json
{
  "nodes": [],
  "edges": []
}
```

- `nodes`: Array of node objects (optional)
- `edges`: Array of edge objects (optional)

## Node Types

### Text Node

```json
{
  "id": "unique-id",
  "type": "text",
  "x": 0,
  "y": 0,
  "width": 250,
  "height": 100,
  "text": "# Heading\n\nMarkdown **content**"
}
```

### File Node

```json
{
  "id": "unique-id",
  "type": "file",
  "x": 300,
  "y": 0,
  "width": 250,
  "height": 100,
  "file": "path/to/file.md",
  "subpath": "#Heading"  // Optional
}
```

### Link Node

```json
{
  "id": "unique-id",
  "type": "link",
  "x": 600,
  "y": 0,
  "width": 250,
  "height": 100,
  "url": "https://example.com"
}
```

### Group Node

```json
{
  "id": "unique-id",
  "type": "group",
  "x": -50,
  "y": -50,
  "width": 1000,
  "height": 300,
  "label": "Group Label",
  "color": "4"
}
```

## Edges

Edges connect nodes with arrows or lines.

```json
{
  "id": "unique-id",
  "from": "node-id-1",
  "to": "node-id-2",
  "fromEnd": "arrow",
  "toEnd": "none",
  "color": "5"
}
```

### End Shapes

- `none` - No arrow
- `arrow` - Arrowhead

### Side Values

- `top`, `right`, `bottom`, `left`, `none`

## Colors

Preset colors: `"1"` through `"6"` (red, orange, yellow, green, blue, purple)

## Quick Example

```json
{
  "nodes": [
    {
      "id": "1",
      "type": "text",
      "x": 0,
      "y": 0,
      "width": 250,
      "height": 100,
      "text": "# Start\n\nBeginning of flow"
    },
    {
      "id": "2",
      "type": "text",
      "x": 400,
      "y": 0,
      "width": 250,
      "height": 100,
      "text": "# End\n\nConclusion"
    }
  ],
  "edges": [
    {
      "id": "e1",
      "from": "1",
      "to": "2",
      "fromEnd": "arrow",
      "toEnd": "arrow"
    }
  ]
}
```

## ID Generation

- Use 16-character hexadecimal IDs: `a1b2c3d4e5f6g7h8`
- Or use UUID v4: `xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx`
- Must be unique within the canvas

## Layout Guidelines

### Positioning
- Start at (0, 0) for first node
- Space nodes: 400px horizontal, 200px vertical
- Center text nodes: width 250-300px

### Recommended Sizes
- Text nodes: 250x100 to 400x300
- File nodes: 300x200
- Link nodes: 250x100
- Groups: Large enough to contain children + 50px padding

### Spacing
- 50px between connected nodes
- 100px between unconnected nodes

## Validation Rules

### Required Fields
- All nodes must have: `id`, `type`, `x`, `y`, `width`, `height`
- Text nodes: must have `text`
- File nodes: must have `file`
- Link nodes: must have `url`

### Edge Requirements
- `from` and `to` must reference existing node IDs
- `id` must be unique across all edges

### Common Mistakes
- ❌ Using `label` for text nodes (use `text` field)
- ❌ Missing `type` field
- ❌ Invalid node IDs in edges
- ❌ Negative width/height

## Important Notes

1. **Z-index**: Node order in array determines layering (last = top)
2. **Text vs label**: Text nodes use `text` field, groups use `label` field
3. **Edge directions**: `fromEnd` is at the source node, `toEnd` is at the target
4. **File paths**: Use forward slashes, relative to vault root

## Detailed Documentation

For complete examples and advanced patterns, see [REFERENCE.md](REFERENCE.md):
- Complete canvas examples (mind maps, flowcharts, project boards)
- Advanced node configurations
- Edge styling and routing
- Group nesting and layouts
