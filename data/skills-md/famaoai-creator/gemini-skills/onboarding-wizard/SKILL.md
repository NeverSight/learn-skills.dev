---
name: onboarding-wizard
description: Generates a personalized project guide for new members. Analyzes the codebase and skills to help someone get productive in day one.
status: implemented
arguments:
  - name: dir
    short: d
    type: string
    description: Project directory
category: Engineering & DevOps
last_updated: '2026-02-13'
tags:
  - automation
  - gemini-skill
---

# Onboarding Wizard

This skill reduces the "time-to-productivity" for new developers or contributors.

## Capabilities

### 1. Project Orientation

- Generates a "First Steps" guide including local setup, key directories, and architecture.
- Explains which Gemini skills are most relevant for the current project.

### 2. Contextual Learning

- Identifies "Good First Issues" or logical starting points in the codebase.
- Maps domain-specific glossaries to code modules.

## Usage

- "I'm new to this project. Run the `onboarding-wizard` to get me started."
- "Generate a day-one guide for a new frontend developer joining this repo."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
