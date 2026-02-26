---
name: log-to-requirement-bridge
description: Analyzes runtime errors and logs to draft improvement requirements. Bridges the gap between Operations and Development.
status: implemented
arguments:
  - name: input
    short: i
    type: string
    required: true
    description: Path to the log file to analyze
category: Utilities
last_updated: '2026-02-13'
tags:
  - gemini-skill
---

# Log-to-Requirement Bridge

This skill turns "problems" found in logs into "tasks" for developers. It analyzes recurring issues and suggests requirement updates.

## Capabilities

### 1. Error Correlation

- Aggregates similar log errors.
- Identifies root causes (e.g., "Frequent timeouts at API X").

### 2. Requirement Drafting

- Automatically drafts "Improvement Requirements" using the `requirements-wizard` format.
- Links logs as evidence for new requirements.

## Usage

- "Analyze the last 1000 lines of `app.log` and draft a requirement to fix the most frequent issue."
- "Bridge the gap: based on these error logs, what should we add to our Non-Functional Requirements?"

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
