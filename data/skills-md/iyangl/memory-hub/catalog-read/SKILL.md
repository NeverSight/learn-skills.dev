---
name: catalog-read
description: "读取 catalog 轻量目录或功能域详细索引"
tools: ["Bash"]
---

## Purpose

Read the catalog index: either the top-level `topics.md` or a specific module's detailed index.

## Input

- `target`: `topics` (default) or a module name

## Required Flow

```bash
memory-hub catalog-read [topics|<module>]
```

## Output

JSON envelope with `data.content` containing the file content.

## Error Handling

- `CATALOG_NOT_FOUND` → requested catalog file does not exist
