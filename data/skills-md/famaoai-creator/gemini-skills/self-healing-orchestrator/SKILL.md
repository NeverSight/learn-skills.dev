---
name: self-healing-orchestrator
description: Automatically repairs known production issues by applying patches, rollbacks, or config changes. The autonomous counterpart to crisis-manager.
status: implemented
arguments:
  - name: input
    short: i
    type: string
    required: true
    description: Path to error log or JSON error report
  - name: dry-run
    type: boolean
    description: Only propose fixes without applying them
  - name: out
    short: o
    type: string
    description: Output file path
category: Utilities
last_updated: '2026-02-13'
tags:
  - gemini-skill
---

# Self-Healing Orchestrator

This skill acts as an autonomous first-responder to production alerts.

## Capabilities

### 1. Pattern-Based Repair

- Matches incoming error patterns with established "Healing Runbooks."
- Can automatically restart services, scale resources, or rollback a specific deployment, ensuring **idempotency** as defined in [Runbook Best Practices](../knowledge/operations/runbook_best_practices.md).

### 2. Autonomous Patching

- For known minor bugs (e.g., edge-case NULL pointers), it can generate, test, and deploy a temporary hotfix.
- Follows strict **Safety & Error Handling** (e.g., Dry Run, Human-in-the-loop) protocols.

## Usage

- "Automate the response to 'Database Connection Timeout' alerts using `self-healing-orchestrator`."
- "A minor bug was detected in production; can the orchestrator apply a safe hotfix?"

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
- References [Runbook Best Practices](../knowledge/operations/runbook_best_practices.md) for executing machine-readable procedures safely and autonomously.
