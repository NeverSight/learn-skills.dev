---
name: issue-to-solution-bridge
description: Automates the entire lifecycle from issue detection to solution. Interprets bug reports or feature requests and orchestrates other skills to implement and test the fix.
status: implemented
arguments:
  - name: issue
    short: i
    type: string
    description: GitHub issue number or URL
  - name: description
    short: d
    type: string
    description: Issue description text
  - name: repo
    short: r
    type: string
    description: Repository (owner/repo)
  - name: dry-run
    type: boolean
    description: Analysis only, no changes
category: Utilities
last_updated: '2026-02-13'
tags:
  - gemini-skill
  - qa
---

# Issue-to-Solution Bridge

This skill acts as an autonomous agent that takes an Issue ID or description and drives it to completion.

## Capabilities

### 1. Issue Interpretation

- Analyzes GitHub/Jira issue descriptions to understand requirements and reproduction steps.
- Identifies relevant files and modules to be modified.

### 2. Full-Cycle Orchestration

- Coordinates `codebase-mapper`, `test-suite-architect`, and `mission-control` to implement the solution, verify it with tests, and prepare a PR.

## Usage

- "Solve GitHub Issue #123: 'Authentication fails on mobile devices'."
- "Interpret this feature request and implement the initial draft in a new branch."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
