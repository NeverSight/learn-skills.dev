---
name: codebase-mapper
description: Maps the directory structure of the project to help the AI understand the codebase layout.
status: implemented
arguments:
  - name: directory
    type: string
    positional: true
    default: .
    description: Root directory to map
  - name: depth
    type: number
    positional: true
    default: 3
    description: Max depth to traverse
category: Engineering & DevOps
last_updated: '2026-02-13'
tags:
  - gemini-skill
---

# Codebase Mapper Skill

Maps the directory structure of the project to help the AI understand the codebase layout.

## Usage

```bash
node codebase-mapper/scripts/map.cjs <directory_path> [max_depth]
```

- `<directory_path>`: Root directory to map (default: `.`)
- `[max_depth]`: How deep to traverse (default: `3`)

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
