---
name: format-detector
description: Detect text format (JSON, YAML, CSV, etc.) and confidence.
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

# Format Detector

Detect text format (JSON, YAML, CSV, etc.) and confidence.

## Usage

node format-detector/scripts/detect.cjs [options]

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
