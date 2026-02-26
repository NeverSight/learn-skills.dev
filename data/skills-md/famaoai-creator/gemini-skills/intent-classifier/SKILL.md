---
name: intent-classifier
description: Classify intent of text (request, question, report).
status: implemented
arguments:
  - name: input
    short: i
    type: string
    required: true
category: Utilities
last_updated: '2026-02-13'
tags:
  - gemini-skill
---

# intent-classifier

Classify intent of text (request, question, report).

## Usage

```bash
node intent-classifier/scripts/classify.cjs --input <file>
```

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
