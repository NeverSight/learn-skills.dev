---
name: doc-type-classifier
description: Classify document type (meeting-notes, spec, etc).
status: implemented
category: Utilities
last_updated: '2026-02-13'
tags:
  - documentation
  - gemini-skill
---

# doc-type-classifier

Classify document type (meeting-notes, spec, etc).

## Usage

```bash
node doc-type-classifier/scripts/classify.cjs --input <file>
```

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
