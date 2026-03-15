---
name: memory
description: Read long-term memory files to get historical context, code references, and error fix records. Use when user wants to read memory, get context, check history, avoid repeating errors.
---

# Memory - Long-term Context

Read the current session's long-term memory files to access historical context preserved across compacts.

## Background

Claude Code's `/compact` compresses conversations to save context. Repeated compaction causes "memory decay" - important early details gradually get lost.

Max's memory system automatically saves accumulated content to files during each compact, ensuring important information is never lost.

## Memory Files

| File | Content | Priority |
|------|---------|----------|
| `errors.md` | Error fix records | **Highest** - Avoid repeating mistakes |
| `context.md` | User messages + technical concepts | Medium - Full background |
| `files.md` | Code file references | Low - Only when needed |

## Instructions

Use the memory.py script to read files with automatic truncation (large files are trimmed to last ~15000 chars to save context):

```bash
# Read errors.md only (default, recommended)
cd /path/to/skills/memory && uv run memory.py errors.md

# Read specific files
cd /path/to/skills/memory && uv run memory.py errors.md context.md

# Read all files
cd /path/to/skills/memory && uv run memory.py all
```

The script automatically:
- Reads from `~/.claude/projects/$MAX_PROJECT_ID/max/$MAX_SESSION_ID/memory/`
- Truncates files > 15000 chars (keeps most recent content)
- Skips non-existent files

## When to Read Memory

**After compact** - When you see "Earlier details saved to..." in the summary:
- Always read `errors.md` first - Critical to avoid repeating past mistakes

**On demand** - Read specific files based on the situation:

| Situation | Command |
|-----------|---------|
| Encountering errors / Tests failing | `uv run memory.py errors.md` |
| Need to recall previous discussions | `uv run memory.py context.md` |
| Reusing code patterns / Finding files | `uv run memory.py files.md` |

## Notes

- Memory files are automatically updated during each `/compact`
- Files are appended with timestamps, newest content at the bottom
- Large files are truncated to ~15000 chars (≈3% of context) to prevent context overflow
