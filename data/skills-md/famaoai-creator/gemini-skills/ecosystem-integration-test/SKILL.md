---
name: ecosystem-integration-test
description: Validates the interoperability between skills. Ensures that output formats (JSON/Markdown) from one skill are correctly consumed by the next in a chain.
status: implemented
arguments:
  - name: dir
    short: d
    type: string
    description: Root directory of the skill ecosystem
  - name: out
    short: o
    type: string
    description: Output file path
category: Utilities
last_updated: '2026-02-13'
tags:
  - gemini-skill
  - qa
---

# Ecosystem Integration Test

This skill ensures the "Digital Nervous System" is intact.

## Capabilities

### 1. Handover Verification

- Simulates common skill chains (e.g., `RD -> Code`).
- Checks if the JSON output of Skill A matches the input schema of Skill B.

### 2. Protocol Adherence Check

- Verifies that all skills are correctly using `scripts/lib/core.cjs` and following the 3-Tier Knowledge Protocol.

## Usage

- "Run a full integration test on the 'Business Launchpad' meta-skill chain."
- "Verify that `requirements-wizard` outputs can be parsed by `test-suite-architect`."
