---
name: skill-evolution-engine
description: Enables skills to self-improve by analyzing execution logs and user feedback. Automatically refines SKILL.md and scripts to fix recurring failures.
status: implemented
arguments:
  - name: skill
    short: s
    type: string
    required: true
    description: Skill name to analyze for evolution
  - name: dir
    short: d
    type: string
    description: Project root
  - name: out
    short: o
    type: string
    description: Output file path
category: Engineering & DevOps
last_updated: '2026-02-13'
tags:
  - gemini-skill
---

# Skill Evolution Engine

This is the self-improvement core of the monorepo. It monitors other skills and updates them based on real-world performance.

## Capabilities

### 1. Failure Analysis

- Inspects `work/` logs to identify why a skill tool call failed or was suboptimal.
- Correlates errors with specific instructions in `SKILL.md`.

### 2. Autonomous Patching

- Generates and applies improvements to `SKILL.md` (instructions) and associated scripts to prevent future errors.
- Proposes architectural changes to skills if the current approach is fundamentally limited.

## Usage

- "Analyze the performance of all skills over the last week and evolve those with high failure rates."
- "The `browser-navigator` keeps failing on SPA sites. Use `skill-evolution-engine` to fix it."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
