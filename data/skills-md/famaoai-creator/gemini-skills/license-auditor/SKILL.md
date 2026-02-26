---
name: license-auditor
description: Scans project dependencies for license compliance risks. Identifies restrictive licenses (GPL, AGPL) and generates mandatory attribution (NOTICE) files.
status: implemented
arguments:
  - name: dir
    short: d
    type: string
    required: true
    description: Project directory to audit
  - name: out
    short: o
    type: string
    description: Output file path
category: Governance & Security
last_updated: '2026-02-13'
tags:
  - automation
  - compliance
  - gemini-skill
---

# License Auditor

This skill ensures your project is legally sound by auditing the licenses of all third-party libraries.

## Capabilities

### 1. Compliance Scan

- Lists all licenses found in `package.json`, `requirements.txt`, etc.
- Flags restrictive (copyleft) licenses that might conflict with commercial use.

### 2. Attribution Management

- Automatically generates a `NOTICE` or `THIRD-PARTY-LICENSES` file containing all required legal notices and copyrights.

## Usage

- "Audit the licenses in this project and generate a compliance report."
- "Create a NOTICE file for the upcoming release."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
