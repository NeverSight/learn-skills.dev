---
name: memory-list
description: "列出 .memory/ 中某个桶的所有文件"
tools: ["Bash"]
---

## Purpose

List all `.md` files in a knowledge bucket.

## Input

- `bucket`: pm | architect | dev | qa

## Required Flow

```bash
memory-hub list <bucket>
```

## Output

JSON envelope with `data.files` array of filenames.

## Error Handling

- `INVALID_BUCKET` → invalid bucket name
- `BUCKET_NOT_FOUND` → bucket directory does not exist
