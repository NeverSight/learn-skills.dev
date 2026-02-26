---
name: lang-detector
description: Detect natural language of text (ja, en, etc.).
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

# Lang Detector

Detect natural language of text (ja, en, etc.).

## Usage

node lang-detector/scripts/detect.cjs [options]

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
