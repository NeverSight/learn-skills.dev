---
name: memory-search
description: "跨桶全文检索 .memory/ 中的知识文件"
tools: ["Bash"]
---

## Purpose

Full-text search across all knowledge buckets (pm, architect, dev, qa).

## Input

- `query`: search string (substring or regex)
- `context` (optional): lines of context around matches, default 1

## Required Flow

```bash
memory-hub search "<query>" [--context N]
```

## Output

JSON envelope with `data.matches` array: `{file, line_number, line_content, context}`.

## Error Handling

- `NOT_INITIALIZED` → `.memory/` does not exist
