---
name: workspace-tools
description: Utilities for inspecting the local project workspace (list files, spot large folders, and determine where to focus).
license: MIT
---

# Tools

## list-directory

- Purpose: Print a depth-limited directory tree as JSON for the current working directory or a target path.
- Usage:
  - `./scripts/list-directory/list-directory` (defaults to current directory, depth 2)
  - `./scripts/list-directory/list-directory --path ./src --depth 3`
- Flags:
  - `--path <path>`: Directory to scan (default: `.`, relative paths are resolved from cwd)
  - `--depth <number>`: How deep to recurse (default: 2)
  - `--json`: Emit compact JSON instead of pretty output
