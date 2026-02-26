---
name: dependency-lifeline
description: Proactively monitors and plans library updates. Assesses the risk of breaking changes and proposes safe update paths.
status: implemented
arguments:
  - name: dir
    short: d
    type: string
    description: Project directory containing package.json
  - name: out
    short: o
    type: string
    description: Output file path
category: Utilities
last_updated: '2026-02-13'
tags:
  - gemini-skill
  - observability
---

# Dependency Lifeline

This skill moves from reactive vulnerability scanning to proactive dependency management.

## Capabilities

### 1. Update Strategy

- Monitors for new versions of project dependencies.
- Analyzes changelogs and issues to predict the risk of "Breaking Changes."

### 2. Automated Migration

- Proposes code changes required to support a newer library version.
- Validates updates by running existing tests via `test-genie`.

## Usage

- "What libraries in this project are out of date, and what is the risk of updating them?"
- "Propose an update plan for `package.json` to move to the next major version of React."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
