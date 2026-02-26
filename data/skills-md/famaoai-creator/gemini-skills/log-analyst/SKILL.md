---
name: log-analyst
description: Reads the tail of a log file to help analyze recent errors or behavior.
status: implemented
arguments:
  - name: file
    type: string
    positional: true
    required: true
    description: Path to log file
  - name: lines
    type: number
    positional: true
    default: 100
    description: Number of lines to read
category: Utilities
last_updated: '2026-02-13'
tags:
  - gemini-skill
---

# Log Analyst Skill

Reads the tail (end) of a log file to help analyze recent errors or runtime behavior.

## Usage

```bash
node log-analyst/scripts/tail.cjs <path_to_log_file> [num_lines]
```

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
