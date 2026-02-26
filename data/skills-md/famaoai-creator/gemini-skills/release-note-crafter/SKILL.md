---
name: release-note-crafter
description: Generates business-value-focused release notes by correlating Git logs with requirements. Focuses on "what's new" for users and stakeholders.
status: implemented
arguments:
  - name: dir
    short: d
    type: string
    required: true
    description: Git repository path
  - name: since
    short: s
    type: string
    required: true
    description: Date or tag to start from
  - name: out
    short: o
    type: string
    description: Output file path for release notes
category: Utilities
last_updated: '2026-02-13'
tags:
  - automation
  - gemini-skill
---

# Release Note Crafter

This skill bridges the gap between technical commits and business value.

## Capabilities

### 1. Value-Based Synthesis

- Group technical commits into user-facing features and fixes.
- Translates "Refactored auth logic" into "Improved login security and speed."

### 2. Multi-Audience Output

- Generates high-level summaries for stakeholders.
- Generates detailed changelogs for developers/QA.

## Usage

- "Generate release notes for the `v1.2.0` release by analyzing commits since `v1.1.0`."
- "Craft a user-facing 'What's New' announcement based on these recent changes."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
