---
name: chaos-monkey-orchestrator
description: Injects managed chaos into environments to test system resilience. Validates that self-healing and monitoring systems work as expected under stress.
status: implemented
arguments:
  - name: dir
    short: d
    type: string
    description: Project directory
  - name: intensity
    short: 'n'
    type: string
    description: Chaos intensity level
  - name: dry-run
    type: boolean
    description: Only simulate, do not execute
  - name: out
    short: o
    type: string
    description: Output file path
category: Utilities
last_updated: '2026-02-13'
tags:
  - gemini-skill
  - observability
  - qa
---

# Chaos Monkey Orchestrator

This skill validates system resilience by intentionally introducing controlled failures.

## Capabilities

### 1. Chaos Injection

- Injects network latency, terminates random service pods, or fills disk space in staging environments.
- Simulates API timeouts and database master failures.

### 2. Resilience Validation

- Verifies that `self-healing-orchestrator` and `crisis-manager` respond correctly to the injected chaos.
- Adheres to the "Fire Drill" protocols defined in [Modern SRE Best Practices](../knowledge/operations/modern_sre_best_practices.md).

## Usage

- "Run a chaos drill on the staging environment: simulate a 50% network packet loss."
- "Terminate a random pod every hour for the next 4 hours and monitor the recovery time."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
- References [Modern SRE Best Practices](../knowledge/operations/modern_sre_best_practices.md) for resilience testing and fault injection standards.
