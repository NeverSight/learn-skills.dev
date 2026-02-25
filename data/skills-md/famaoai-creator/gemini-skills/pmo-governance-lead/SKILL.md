---
name: pmo-governance-lead
description: Fulfills the role of a PMO by overseeing project quality gates, risks, and cross-skill alignment. Enforces IPA and industry standards across the lifecycle.
status: implemented
arguments:
  - name: dir
    short: d
    type: string
    description: Project directory to audit
  - name: phase
    short: p
    type: string
    description: SDLC phase to check
  - name: out
    short: o
    type: string
    description: Output file path
category: Utilities
last_updated: '2026-02-13'
tags:
  - gemini-skill
---

# PMO Governance Lead

This skill acts as the project's internal regulator and strategic advisor.

## Capabilities

### 1. Quality Gate Enforcement

- Audits if a phase (e.g., Design) is truly complete before implementation begins.
- Checks for required evidence logs (Review feedbacks, Test results).

### 2. Risk Orchestration

- Analyzes logs from all other skills to detect "hidden" project risks (e.g., tech debt spikes, compliance gaps).
- Refers to `knowledge/pmo/standards/governance.md`.

## Usage

- "Perform a PMO audit on the current project status and identify any missing quality gates."
- "Are we ready to move from Design to Implementation? Review all design review logs."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`.
