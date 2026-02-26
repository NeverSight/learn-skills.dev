---
name: business-impact-analyzer
description: Translates engineering metrics (DORA, error rates, technical debt) into business KPIs and financial impact. Helps justify technical investments to stakeholders.
status: implemented
arguments:
  - name: input
    short: i
    type: string
    required: true
    description: Path to JSON file with engineering metrics
  - name: out
    short: o
    type: string
    description: Output file path
category: Utilities
last_updated: '2026-02-13'
tags:
  - gemini-skill
---

# Business Impact Analyzer

This skill connects the machine room to the boardroom by quantifying technical work in business terms.

## Capabilities

### 1. ROI Modeling

- Correlates DORA metrics (Deployment Frequency, Lead Time) with business agility and cost savings.
- Estimates the "Cost of Inaction" for critical technical debt.

### 2. Executive Insight

- Generates "Business Impact Reports" that explain how technical improvements (e.g., refactoring, better testing) directly affect revenue, churn, or operating margins.

## Usage

- "Analyze our recent performance improvements and estimate the impact on infrastructure costs and user retention."
- "Translate our technical debt reduction plan into a business value proposition for the CEO."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
