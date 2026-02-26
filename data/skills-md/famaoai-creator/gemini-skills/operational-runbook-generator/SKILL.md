---
name: operational-runbook-generator
description: Generates detailed, step-by-step operational runbooks for day-to-day tasks (scaling, patching, updates). Ensures consistency and safety with built-in rollback procedures.
status: implemented
arguments:
  - name: service
    short: s
    type: string
    required: true
    description: Service name
  - name: type
    short: t
    type: string
    description: Runbook type
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

# Operational Runbook Generator

This skill ensures that every operational task is documented with professional rigor to prevent human error.

## Capabilities

### 1. Runbook Synthesis

- Translates high-level requests (e.g., "Rotate the DB keys") into a structured Markdown runbook.
- Follows the AI-native guidelines in [Runbook Best Practices](../knowledge/operations/runbook_best_practices.md) (e.g., code blocks, validation steps).

### 2. Risk & Rollback Planning

- Automatically identifies risks associated with the task.
- Generates specific rollback commands for each step as required by the best practices.

## Usage

- "Generate an operational runbook for upgrading our RDS instance from t3.medium to t3.large."
- "Create a procedure for annual SSL certificate rotation."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`.
- References [Runbook Best Practices](../knowledge/operations/runbook_best_practices.md) for generating machine-readable and executable operational procedures.
