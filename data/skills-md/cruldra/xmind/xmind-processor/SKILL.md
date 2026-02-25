---
name: xmind-processor
description: Programmatically create, read, and modify XMind mind map files (.xmind). Provides Python utilities for parsing xmind files, inserting topics, setting background colors, and creating new mind maps from templates. Use when working with XMind files for automation, batch processing, or generating mind maps programmatically.
---

# XMind Processor

Programmatically work with XMind mind map files (.xmind format).

## Capabilities

This skill provides Python utilities to:

1. **Parse** existing .xmind files and extract content.json
2. **Create** new .xmind files from templates
3. **Insert** topics programmatically using JSONPath expressions
4. **Modify** background colors and other properties
5. **Batch process** multiple mind maps

## Core Scripts

All scripts are located in `scripts/` directory.

### xmind_utils.py - Core Utilities

```python
from scripts.xmind_utils import read_content, write_content, modify_content

# Read xmind file
content = read_content("file.xmind")

# Write modified content back
write_content("file.xmind", new_content, output_path="output.xmind")

# Modify with a function
modify_content("file.xmind", lambda c: do_something(c), output_path="output.xmind")
```

### create_xmind.py - Create New Files

```python
from scripts.create_xmind import create_xmind

# Create blank mind map
create_xmind("new.xmind")

# Create with custom titles
create_xmind(
    "new.xmind",
    sheet_title="My Canvas",
    root_topic_title="Central Topic"
)
```

Command line:
```bash
uv run scripts/create_xmind.py output.xmind --sheet-title "Project" --root-topic "Goals"
```

### insert_topic.py - Add Topics

```python
from scripts.insert_topic import insert_topic, insert_topics_batch

# Insert single topic
insert_topic(
    "file.xmind",
    parent_jsonpath="$[0].rootTopic",
    topic_title="New Child Topic",
    output_path="output.xmind"
)

# Batch insert
insert_topics_batch(
    "file.xmind",
    "$[0].rootTopic.children.attached[0]",
    ["Sub-topic 1", "Sub-topic 2", "Sub-topic 3"],
    output_path="output.xmind"
)
```

Command line:
```bash
# List available paths
uv run scripts/insert_topic.py file.xmind --list-topics

# Insert topic
uv run scripts/insert_topic.py file.xmind --parent '$[0].rootTopic' --title "New Topic"

# Batch insert
uv run scripts/insert_topic.py file.xmind --parent '$[0].rootTopic.children.attached[0]' --titles "A" "B" "C"
```

### set_background.py - Styling

```python
from scripts.set_background import set_sheet_background, set_all_sheets_background, list_sheets

# Set single sheet background
set_sheet_background("file.xmind", color="#000000FF", sheet_index=0)

# Set all sheets
set_all_sheets_background("file.xmind", color="#FF0000FF")

# List sheets
sheets = list_sheets("file.xmind")
```

Command line:
```bash
uv run scripts/set_background.py file.xmind --color "#000000FF"
uv run scripts/set_background.py file.xmind --color "#FF0000FF" --all
uv run scripts/set_background.py file.xmind --list
```

## File Structure

XMind files are ZIP archives containing:
- `content.json` - Main content (sheets, topics, structure)
- `metadata.json` - File metadata
- `manifest.json` - Package manifest
- `Thumbnails/thumbnail.png` - Preview image

### content.json Structure

```json
[
  {
    "id": "...",
    "title": "画布 1",
    "rootTopic": {
      "id": "...",
      "title": "中心主题",
      "children": {
        "attached": [
          {"id": "...", "title": "分支主题 1"},
          {"id": "...", "title": "分支主题 2"}
        ]
      }
    }
  }
]
```

## JSONPath Expressions

Use JSONPath to locate topics in the mind map:

- `$[0].rootTopic` - First sheet's central topic
- `$[0].rootTopic.children.attached[0]` - First branch topic
- `$[0].rootTopic.children.attached[?(@.title=="分支主题 1")]` - Find by title

## Dependencies

```bash
uv add jsonpath-ng
```

## Template

A blank template is available at `assets/demo.xmind`.

## Common Workflows

### 1. Create and Populate Mind Map

```python
from scripts.create_xmind import create_xmind
from scripts.insert_topic import insert_topics_batch

# Create new file
create_xmind("project.xmind", sheet_title="Q1 Planning", root_topic_title="Goals")

# Add branch topics
insert_topics_batch(
    "project.xmind",
    "$[0].rootTopic",
    ["Marketing", "Development", "Sales"]
)
```

### 2. Modify Existing File

```python
from scripts.xmind_utils import read_content, write_content

content = read_content("existing.xmind")
# Modify content directly
content[0]['title'] = "New Title"
write_content("existing.xmind", content, output_path="modified.xmind")
```

### 3. Batch Process Multiple Files

```python
from pathlib import Path
from scripts.set_background import set_all_sheets_background

for xmind_file in Path("mindmaps/").glob("*.xmind"):
    set_all_sheets_background(xmind_file, color="#000000FF")
```

## Topic Structure

When creating topics programmatically:

```python
{
    "id": "uuid-here",
    "title": "Topic Name",
    "titleUnedited": True,
    "children": {
        "attached": [
            # Child topics here
        ]
    }
}
```

## Best Practices

1. **Always use output_path** to avoid overwriting original files during development
2. **Validate JSONPath** expressions with --list-topics first
3. **Quote color values** in shell commands: `"#000000FF"` not `#000000FF`
4. **Use UUIDs** for new topic IDs (auto-generated by scripts)
5. **Keep backups** when batch processing

## Error Handling

Common errors and solutions:

- `FileNotFoundError`: Check file path exists
- `ValueError: 不是有效的xmind文件`: File is corrupted or not a ZIP
- `IndexError: sheet_index超出范围`: Requested sheet doesn't exist
- `ModuleNotFoundError: jsonpath_ng`: Run `uv add jsonpath-ng`
