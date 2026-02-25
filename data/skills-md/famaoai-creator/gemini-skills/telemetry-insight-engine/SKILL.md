---
name: telemetry-insight-engine
description: Analyzes real-world telemetry and usage data to identify feature gaps and usability issues. Feeds insights back into the requirements phase.
status: implemented
arguments:
  - name: input
    short: i
    type: string
    required: true
    description: Path to telemetry data (JSON)
  - name: out
    short: o
    type: string
    description: Output file path
category: Engineering & DevOps
last_updated: '2026-02-13'
tags:
  - data-engineering
  - gemini-skill
---

# Telemetry Insight Engine

This skill closes the loop between production usage and new feature development.

## Capabilities

### 1. Usage Analysis

- Analyzes application logs and telemetry (e.g., event data) to identify underused features or common drop-off points.
- Correlates usage patterns with specific code modules.

### 2. Feedback Loop

- Automatically drafts new "Enhancement Requirements" for the `requirements-wizard` based on observed user behavior.

## Usage

- "Analyze our production telemetry and tell me which 3 features should be prioritized for improvement."
- "Are users struggling with the new checkout flow? Use `telemetry-insight-engine` to find out."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
