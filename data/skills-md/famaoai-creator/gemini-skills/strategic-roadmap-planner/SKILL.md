---
name: strategic-roadmap-planner
description: Analyzes code complexity, technical debt, and industry trends to propose a 3-month strategic roadmap. Aligns engineering effort with business ROI.
status: implemented
arguments:
  - name: dir
    short: d
    type: string
    description: Project directory to analyze
  - name: months
    short: m
    type: number
    description: Planning horizon in months
  - name: out
    short: o
    type: string
    description: Output file path
category: Strategy & Leadership
last_updated: '2026-02-13'
tags:
  - gemini-skill
---

# Strategic Roadmap Planner

This skill helps engineering leaders prioritize high-impact architectural and feature work.

## Capabilities

### 1. Technical Debt Valuation

- Calculates the "Interest Rate" of current legacy code.
- Uses **ECC Architect Principles** (`knowledge/external-wisdom/everything-claude/agents/architect.md`) to evaluate system design against SOLID/DRY standards.

### 2. Roadmap Generation

- Proposes a 3-month strategic plan (Gantt Chart).

## Usage

- "Based on our current technical debt and modern trends, generate a 3-month engineering roadmap."
- "What should be our top 3 technical priorities for the next quarter?"

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
