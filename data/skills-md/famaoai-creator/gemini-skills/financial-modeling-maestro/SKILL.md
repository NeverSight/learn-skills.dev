---
name: financial-modeling-maestro
description: Generates and analyzes financial models, P&L forecasts, and cash flow projections. Transforms business assumptions into multi-year financial statements.
status: implemented
arguments:
  - name: input
    short: i
    type: string
    required: true
    description: Path to JSON file with financial assumptions
  - name: years
    short: 'y'
    type: number
    description: Number of years to project
  - name: out
    short: o
    type: string
    description: Output file path
category: Strategy & Leadership
last_updated: '2026-02-13'
tags:
  - automation
  - gemini-skill
---

# Financial Modeling Maestro

This skill provides the CEO with a "Financial Simulator" for the company.

## Capabilities

### 1. P&L & Cash Flow Simulation

- Generates 3-5 year financial forecasts based on revenue growth, hiring plans, and server costs.
- Calculates "Runway" and "Breakeven" points automatically.

### 2. Scenario Analysis (What-If)

- Simulates different scenarios (e.g., "What if we double our engineering team?", "What if our churn rate increases to 5%?").

## Usage

- "Build a 3-year P&L forecast assuming a 15% monthly growth in SaaS subscribers."
- "Analyze our current burn rate and tell me how many months of runway we have left."

## Knowledge Protocol

- Adheres to `knowledge/orchestration/knowledge-protocol.md`.
