---
name: test-genie
description: Executes the project's test suite and returns the output for AI analysis.
status: implemented
category: Engineering & DevOps
last_updated: '2026-02-13'
tags:
  - analytics
  - gemini-skill
  - qa
---

# Test Genie Skill

Executes the project's test suite and returns the output. It attempts to auto-detect the test command (npm, pytest, etc.).

## Usage

```bash
node test-genie/scripts/run.cjs <project_root> [custom_command]
```

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
