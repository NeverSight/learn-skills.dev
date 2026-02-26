---
name: talent-requirement-generator
description: Identifies the ideal human skills needed for the project's next phase. Analyzes technical debt, roadmap, and current team gaps to generate job descriptions and coding challenges.
status: implemented
arguments:
  - name: dir
    short: d
    type: string
    description: Project directory
  - name: role
    short: r
    type: string
    description: Role type
  - name: out
    short: o
    type: string
    description: Output file path
category: Utilities
last_updated: '2026-02-13'
tags:
  - automation
  - gemini-skill
---

# Talent Requirement Generator

This skill helps project leaders build the right human team to complement the AI ecosystem.

## Capabilities

### 1. Gap Analysis

- Evaluates the current codebase and `strategic-roadmap-planner` outputs to find missing technical expertise (e.g., "Need a Rust performance expert").

### 2. Hiring Asset Creation

- Generates tailored Job Descriptions (JDs) focused on the specific needs of the repo.
- Creates relevant coding challenges that mirror actual problems found in the project.

## Usage

- "What kind of engineer should we hire next to accelerate the 3-month roadmap?"
- "Generate a coding challenge for a senior backend candidate based on our recent architectural bottlenecks."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
