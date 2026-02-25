---
name: borumi-project
description: Edit Borumi video project files (.bmprojbundle) using sqlite3
---

# Borumi Project Editing

This skill enables editing Borumi video project files using sqlite3.

## Project Structure

A Borumi project is a directory with the `.bmprojbundle` extension containing:
- `project.bmproj` - SQLite 3 database with project metadata

## Database Schema

### Key Tables

| Table | Purpose |
|-------|---------|
| `projects` | Main project info (id, name, render_target, active_tool) |
| `scenes` | Scenes with scripts (id, project_id, seq, name, script) |
| `takes` | Recording takes within scenes |
| `clips` | Media clips with timing info |
| `medias` | Media files with metadata |
| `project_sources` | Input sources for the project |
| `scene_timeline_segments` | Timeline segments |
| `project_timeline` | Timeline settings |

### Script JSON Schema

The `script` field in the `scenes` table contains JSON with rich text:

```json
{
  "selection": {"start": N, "end": N} | null,
  "content": [<block>, ...]
}
```

#### Block Types

**Paragraph:**
```json
{
  "type": "paragraph",
  "content": [<text-node>, ...]
}
```

**Bullet List:**
```json
{
  "type": "bullet-list",
  "content": [
    {"content": [<block>, ...]},
    ...
  ]
}
```

**Ordered List:**
```json
{
  "type": "ordered-list",
  "start": 1,
  "content": [
    {"content": [<block>, ...]},
    ...
  ]
}
```

#### Text Node

```json
{
  "type": "text",
  "text": "Your text here",
  "bold": false,
  "italic": false,
  "code": false,
  "strike": false
}
```

## Common Operations

### List all scenes in a project

```bash
sqlite3 "path/to/project.bmprojbundle/project.bmproj" \
  "SELECT id, name FROM scenes ORDER BY seq;"
```

### View a scene's script (formatted)

```bash
sqlite3 "path/to/project.bmprojbundle/project.bmproj" \
  "SELECT script FROM scenes WHERE name = 'Scene Name';" | jq .
```

### Update a scene's script with plain text

To set a simple plain text script:

```bash
sqlite3 "path/to/project.bmprojbundle/project.bmproj" \
  "UPDATE scenes SET script = '{\"selection\":null,\"content\":[{\"type\":\"paragraph\",\"content\":[{\"type\":\"text\",\"text\":\"Your new script text here\",\"bold\":false,\"italic\":false,\"code\":false,\"strike\":false}]}]}' WHERE name = 'Scene Name';"
```

### Update script with multiple paragraphs

Each paragraph is a separate object in the content array:

```bash
sqlite3 "path/to/project.bmprojbundle/project.bmproj" \
  "UPDATE scenes SET script = '{\"selection\":null,\"content\":[{\"type\":\"paragraph\",\"content\":[{\"type\":\"text\",\"text\":\"First paragraph\",\"bold\":false,\"italic\":false,\"code\":false,\"strike\":false}]},{\"type\":\"paragraph\",\"content\":[{\"type\":\"text\",\"text\":\"Second paragraph\",\"bold\":false,\"italic\":false,\"code\":false,\"strike\":false}]}]}' WHERE id = 'scene-uuid';"
```

### Rename a scene

```bash
sqlite3 "path/to/project.bmprojbundle/project.bmproj" \
  "UPDATE scenes SET name = 'New Scene Name' WHERE id = 'scene-uuid';"
```

### Add a new scene

```bash
sqlite3 "path/to/project.bmprojbundle/project.bmproj" \
  "INSERT INTO scenes (id, project_id, seq, name, script) VALUES (
    lower(hex(randomblob(4)) || '-' || hex(randomblob(2)) || '-4' || substr(hex(randomblob(2)),2) || '-' || substr('89ab',abs(random()) % 4 + 1, 1) || substr(hex(randomblob(2)),2) || '-' || hex(randomblob(6))),
    (SELECT id FROM projects LIMIT 1),
    'Z',
    'New Scene',
    '{\"selection\":null,\"content\":[{\"type\":\"paragraph\",\"content\":[{\"type\":\"text\",\"text\":\"Script content\",\"bold\":false,\"italic\":false,\"code\":false,\"strike\":false}]}]}'
  );"
```

Note: The `seq` field controls scene ordering. Use a value that sorts appropriately.

## Tips

- Always back up the `.bmprojbundle` folder before making changes
- Use `jq` to format and validate JSON when constructing complex scripts
- Scene IDs are UUIDs - use the `id` field for precise updates
- The `seq` field is a string used for ordering scenes (lexicographic sort)
- Close Borumi before editing the database to avoid conflicts
