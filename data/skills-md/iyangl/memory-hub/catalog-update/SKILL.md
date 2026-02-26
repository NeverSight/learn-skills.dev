---
name: catalog-update
description: "更新代码模块索引（catalog/modules/* 和 topics.md 代码模块部分）"
tools: ["Bash", "Write"]
---

## Purpose

Update the code module index from AI-generated JSON. Only touches the code modules section of topics.md, not the knowledge files section.

## Input

JSON file with schema:

```json
{
  "modules": [
    {
      "name": "module-name",
      "summary": "One-line description",
      "files": [
        {"path": "src/file.py", "description": "What this file does"}
      ]
    }
  ]
}
```

## Required Flow

### Step 1: Write JSON to a temporary file

Use the file write tool to create a JSON file (e.g. `/tmp/modules.json`).

### Step 2: Run catalog-update

```bash
memory-hub catalog-update --file /tmp/modules.json
```

Automatically triggers `catalog.repair` after completion.

## Output

JSON envelope with `data.modules_written`, `data.modules_deleted`, and repair results.

## Error Handling

- `FILE_NOT_FOUND` → JSON file not found
- `INVALID_JSON` → file is not valid JSON
- `INVALID_SCHEMA` → `modules` is not an array
