---
name: sunset-architect
description: Manages the graceful decommissioning of underused or high-maintenance features. Plans deprecation cycles, handles data archiving, and generates migration paths for legacy users.
status: implemented
arguments:
  - name: input
    short: i
    type: string
    required: true
    description: Path to JSON with feature/service data to sunset
  - name: out
    short: o
    type: string
    description: Output file path
category: Strategy & Leadership
last_updated: '2026-02-13'
tags:
  - automation
  - data-engineering
  - gemini-skill
---

# Sunset Architect

This skill ensures that the codebase stays lean by elegantly removing parts of the system that are no longer valuable.

## Capabilities

### 1. Legacy Identification

- Identifies "Zombie Features" with low utilization and high maintenance/error rates.
- Calculates the cost-savings of removing specific legacy components.

### 2. Graceful Sunsetting

- Generates step-by-step "Retirement Plans" including deprecation warnings, data migration/archiving scripts, and user communication drafts.

## Usage

- "Identify the top 3 candidates for sunsetting in our current codebase."
- "Create a graceful decommissioning plan for the legacy v1 API."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
