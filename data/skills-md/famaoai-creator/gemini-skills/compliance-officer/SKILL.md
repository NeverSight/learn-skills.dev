---
name: compliance-officer
description: Maps technical state to regulatory standards (SOC2, ISO27001, etc.). Generates real-time compliance scores and audit-ready evidence reports.
status: implemented
arguments:
  - name: dir
    short: d
    type: string
    description: Project directory
  - name: standard
    short: s
    type: string
    description: Compliance standard
  - name: out
    short: o
    type: string
    description: Output file path
category: Governance & Security
last_updated: '2026-02-13'
tags:
  - automation
  - compliance
  - gemini-skill
---

# Compliance Officer

This skill automates the painful process of preparing for security and regulatory audits.

## Capabilities

### 1. Standard Mapping

- Maps code, IaC, and logs to specific controls in standards like SOC2, ISO27001, or HIPAA.
- Provides a "Compliance Dashboard" in Markdown format.

### 2. Evidence Generation

- Automatically collects and packages evidence (e.g., IAM roles, encryption settings, PR review logs) for auditors.

## Usage

- "How do we stand against SOC2 Type II requirements? Generate a gap analysis."
- "Collect all necessary evidence for the upcoming ISO27001 audit."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
