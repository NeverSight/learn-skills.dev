---
name: schema-validator
description: Validate JSON against schemas and identify best match.
status: implemented
arguments:
  - name: input
    short: i
    type: string
    required: true
    description: JSON data to validate
  - name: schema
    short: s
    type: string
    required: true
    description: JSON Schema file path
category: Utilities
last_updated: '2026-02-13'
tags:
  - gemini-skill
---

# Schema Validator

Validate JSON against schemas and identify best match.

## Usage

node schema-validator/scripts/validate.cjs [options]

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
