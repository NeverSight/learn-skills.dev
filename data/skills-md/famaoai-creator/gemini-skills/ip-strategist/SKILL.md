---
name: ip-strategist
description: Identifies and protects intellectual property within the codebase. Drafts initial patent applications and IP reports for innovative algorithms or designs.
status: implemented
arguments:
  - name: dir
    short: d
    type: string
    description: Project directory to analyze
  - name: out
    short: o
    type: string
    description: Output file path
category: Governance & Security
last_updated: '2026-02-13'
tags:
  - gemini-skill
---

# IP Strategist

This skill helps protect the innovative value of your engineering efforts.

## Capabilities

### 1. Novelty Detection

- Analyzes the codebase to identify unique algorithms, architectural patterns, or data structures.
- Compares against general industry knowledge to find patentable "Novelty."

### 2. IP Drafting

- Drafts initial technical reports and patent application outlines to be reviewed by legal experts.

## Usage

- "Analyze the core processing engine for patentable innovations and draft an IP report."
- "What parts of our new scaling logic are unique enough to be protected as intellectual property?"

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
