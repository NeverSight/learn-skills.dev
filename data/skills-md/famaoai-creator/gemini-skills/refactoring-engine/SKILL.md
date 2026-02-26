---
name: refactoring-engine
description: Executes large-scale architectural refactoring and technical debt reduction across the entire codebase. Ensures consistency with modern design patterns.
status: implemented
arguments:
  - name: input
    short: i
    type: string
    required: true
    description: Path to source file to analyze
  - name: out
    short: o
    type: string
    description: Optional output file path
category: Engineering & DevOps
last_updated: '2026-02-13'
tags:
  - gemini-skill
---

# Refactoring Engine

This skill moves beyond line-by-line changes to perform systemic improvements to the code architecture.

## Capabilities

### 1. Pattern Migration

- Migrates components to new design systems (e.g., from CSS modules to Tailwind, or to Atomic Design).
- Converts legacy syntax to modern standards (e.g., Class components to Functional components in React).

### 2. Dependency Decoupling

- Identifies and breaks circular dependencies.
- Extracts shared logic into centralized services or utilities.

## Workflow

1.  **Pinning Tests (Mandatory)**: Before changing any code, create tests that capture the _current_ behavior (even if it's messy). This ensures no regression occurs.
2.  **Architectural Analysis**: Use `cognitive-load-auditor` to identify high-complexity hotspots.
3.  **Pattern Migration**: Apply clean code patterns (Guard Clauses, Strategy, etc.).

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
