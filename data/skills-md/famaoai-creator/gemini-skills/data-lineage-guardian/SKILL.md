---
name: data-lineage-guardian
description: Tracks the flow and integrity of data across the entire stack. Monitors data quality, ensures "Right to be Forgotten" compliance, and visualizes data lineage.
status: implemented
arguments:
  - name: dir
    short: d
    type: string
    description: Project directory
  - name: out
    short: o
    type: string
    description: Output file path
category: Utilities
last_updated: '2026-02-13'
tags:
  - data-engineering
  - gemini-skill
  - observability
---

# Data Lineage Guardian

This skill ensures that your data remains clean, compliant, and traceable from source to sink.

## Capabilities

### 1. Lineage Mapping

- Automatically maps how data moves through databases, APIs, and frontend components.
- Visualizes "Data Provenance" to identify where a specific piece of information originated.

### 2. Quality & Compliance Monitoring

- Detects data drifts or corruption in the pipeline.
- Ensures PII (Personal Identifiable Information) is correctly handled or deleted across all systems to comply with privacy laws.

## Usage

- "Map the lineage of the 'Customer Billing' data from the main DB to the frontend dashboard."
- "Verify if our data deletion process correctly clears all traces of a user in compliance with GDPR."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
