---
name: code-search
description: Use when you need to locate definitions of classes, functions, constants, types, or symbols in the application code. Before searching individual files, run Repomix with stdout output to capture a snapshot and base the search on that content.
---

# Repomix Code Search

## Overview

Generate a repository snapshot with Repomix to stdout and use it as the primary source to find symbol definitions before diving into individual files.

## Workflow

1. Run Repomix on this repository and send to stdout:

```bash
npx repomix --stdout
```

2. Analyze the snapshot to locate symbol definitions (classes, functions, constants, types).
3. If you need exact locations or extra context, use read/search tools on the real files.

## Notes

- Regenerate the snapshot if you changed relevant files in `src/`.
- If the repo is large, consider `--include` and `--ignore` to narrow the snapshot.
