---
name: executive-reporting-maestro
description: Synthesizes technical data into professional external reports for PMOs and stakeholders. Focuses on ROI, milestones, and high-level project health.
status: implemented
arguments:
  - name: input
    short: i
    type: string
    required: true
    description: Path to a directory of JSON result files or a single JSON file
  - name: title
    short: t
    type: string
    description: Report title
  - name: out
    short: o
    type: string
    description: Output file path (JSON or .md)
category: Strategy & Leadership
last_updated: '2026-02-13'
tags:
  - data-engineering
  - gemini-skill
---

# Executive Reporting Maestro

This skill translates the complex internal state of the ecosystem into a polished, persuasive report for external audiences.

## Capabilities

### 1. External Status Reporting

- Generates high-level status updates based on `knowledge/pmo/templates/external_status_report.md`.
- Categorizes updates into "Executive Highlights" and "Technical Details."

### 2. Strategic Narrative

- Uses `ppt-artisan` and `stakeholder-communicator` logic to ensure reports focus on business outcomes and risk mitigation.

## Usage

- "Generate a bi-weekly status report for the external PMO team."
- "Create an executive summary of our security posture for the quarterly review."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`.
