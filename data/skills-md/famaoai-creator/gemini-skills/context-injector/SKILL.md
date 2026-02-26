---
name: context-injector
description: Inject knowledge into JSON data context.
status: implemented
arguments:
  - name: data
    short: d
    type: string
    required: true
  - name: knowledge
    short: k
    type: string
    required: true
  - name: out
    short: o
    type: string
  - name: output-tier
    type: string
category: Utilities
last_updated: '2026-02-13'
tags:
  - data-engineering
  - gemini-skill
---

# context-injector

Inject knowledge into JSON data context.

## Usage

```bash
node context-injector/scripts/inject.cjs [options]
```

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
