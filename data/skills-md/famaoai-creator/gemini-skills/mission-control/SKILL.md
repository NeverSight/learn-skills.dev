---
name: mission-control
description: Orchestrates multiple skills to achieve high-level goals. Acts as the brain of the ecosystem to coordinate complex workflows across the SDLC.
status: implemented
arguments:
  - name: pipeline
    short: p
    type: string
  - name: skills
    short: s
    type: string
  - name: dir
    short: d
    type: string
category: Utilities
last_updated: '2026-02-13'
tags:
  - gemini-skill
---

# Mission Control (Orchestrator)

This is the "Brain" of the Gemini Skills ecosystem. It knows how to combine 100+ specialized skills to fulfill abstract, high-level requests.

## Capabilities

### 1. Workflow Orchestration

- **Intent-Driven Execution**: Parses abstract user requests against `knowledge/orchestration/meta-skills/intent_mapping.yaml` to trigger pre-defined skill chains (Meta-Skills).
- **Credential Verification**: Automatically invokes `connection-manager` before any task requiring external tools (Slack, Jira, AWS) to ensure secrets are loaded.
- **Proposer Branding**: Orchestrates all visual skills to adopt the "Proposer Brand" (e.g., logos, colors) defined in `knowledge/templates/themes/proposer/`.
- **Global Skill Lookup**: Prioritizes `knowledge/orchestration/global_skill_index.json` to instantly identify the best skills for a task without reading all definition files.
- **Parallel Audit Pipeline**: Can trigger `security-scanner`, `ux-auditor`, and `license-auditor` in parallel, aggregating results for a 3x speedup in quality gates.
- **3-Tier Sovereign Protocol**: Orchestrates all skills to use Public, Confidential (Skill/Client-specific), and Personal knowledge tiers.
- **Client Context Switching**: Can set a specific client context (e.g., "Act as lead for Client A") to prioritize `knowledge/confidential/clients/ClientA/`.
- **Key Patterns**:
  - **Hybrid AI-Native Flow**: Optimal balance of TDD for core logic and AI-direct generation for speed. Target 90%+ coverage. See `knowledge/orchestration/hybrid-development-flow.md`.
  - **Safe Git Flow**: Enforces "Branch -> PR -> Review" sequence. Direct push to main is prohibited. See `knowledge/orchestration/git-flow-standards.md`.
  - **Advanced Development Flow**: The gold standard for autonomous engineering (Full TDD). See `knowledge/orchestration/advanced-development-flow.md`.
  - **Professional Proposal Pipeline**: See `knowledge/orchestration/proposal-pipeline.md` for the full research-to-production sequence.
  - **Production Readiness Audit**: Coordinates `security-scanner` -> `ux-auditor` -> `license-auditor` -> `project-health-check`.
  - **Enterprise Quality Cycle**: Follows `knowledge/orchestration/quality-management-flow.md` to review, report, and improve artifacts.
  - **Self-Healing Loop**: Applies `knowledge/orchestration/autonomous-debug-loop.md` to automatically recover from execution failures.
  - **Knowledge Integrity Audit**: Periodically triggers `knowledge-auditor` to maintain consistency across 3 tiers.
  - **Autonomous Troubleshooting**: Links `log-analyst` -> `crisis-manager` -> `self-healing-orchestrator`.

### 2. Executive Reporting

- Summarizes the results of multiple skill executions into a single, high-level status report for stakeholders.

## Usage

- "Execute a full production-readiness audit and report the results."
- "Create a business proposal for [Target Client] regarding [Solution/Technology]."
- "I want to release a new version. Coordinate all necessary checks and documentation."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
