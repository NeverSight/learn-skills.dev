---
name: memory-read
description: "精准读取 .memory/ 中某个桶的某个文件"
tools: ["Bash"]
---

## Purpose

Read a specific knowledge file from a bucket in `.memory/`.

## Input

- `bucket`: pm | architect | dev | qa
- `file`: filename within the bucket
- `anchor` (optional): check if a heading anchor exists

## Required Flow

```bash
memory-hub read <bucket> <file> [--anchor <anchor>]
```

## Output

JSON envelope with `data.content` containing the file content.

If `--anchor` is provided and invalid, `repair_triggered: true` and repair results are included.

## Error Handling

- `INVALID_BUCKET` → invalid bucket name
- `FILE_NOT_FOUND` → file does not exist in the bucket
