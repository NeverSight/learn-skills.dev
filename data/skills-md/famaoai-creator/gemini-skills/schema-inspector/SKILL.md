---
name: schema-inspector
description: Automatically locates and displays schema definition files (SQL, Prisma, OpenAPI, etc.).
status: implemented
category: Utilities
last_updated: '2026-02-13'
tags:
  - gemini-skill
  - integration
---

# Schema Inspector Skill

Automatically locates and displays the content of schema definition files (SQL, Prisma, OpenAPI, etc.) to help the AI understand data models and APIs.

## Usage

```bash
node schema-inspector/scripts/inspect.cjs <project_root>
```

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
