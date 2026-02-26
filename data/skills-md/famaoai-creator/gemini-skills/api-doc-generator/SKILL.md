---
name: api-doc-generator
description: Generate API documentation from OpenAPI specs or code.
status: implemented
category: Utilities
last_updated: '2026-02-13'
tags:
  - automation
  - documentation
  - gemini-skill
  - integration
related_skills:
  - word-artisan
---

# Api Doc Generator

Generate API documentation from OpenAPI specs or code.

## Usage

node api-doc-generator/scripts/generate.cjs [options]

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
