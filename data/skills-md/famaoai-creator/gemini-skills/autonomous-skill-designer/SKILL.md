---
name: autonomous-skill-designer
description: The ultimate "self-generation" skill. Autonomously designs and implements new Gemini skills to solve novel problems that current skills cannot address.
status: implemented
category: Utilities
last_updated: '2026-02-13'
tags:
  - gemini-skill
---

# Autonomous Skill Designer

This is the final key to the ecosystem. It allows the monorepo to expand its own capabilities without human intervention.

## Capabilities

### 1. Gap Identification

- Works with `mission-control` to identify when a user's high-level goal cannot be met by existing skills.
- Defines the requirements for a new, necessary skill.

### 2. Autonomous Implementation

- Drafts the new `SKILL.md` instructions.
- Implements the necessary Node.js/Python scripts.
- Installs and tests the new skill within the monorepo.

## Usage

- "We need a way to integrate with our internal proprietary CI system. Use `autonomous-skill-designer` to build a skill for it."
- "The monorepo is missing a way to handle legacy COBOL files. Design and implement a `cobol-analyzer` skill."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
