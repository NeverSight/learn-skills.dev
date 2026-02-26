---
name: visionary-ethos-keeper
description: Ensures decisions and proposals align with company mission, values, and ethical guidelines. Checks for bias, privacy, and fairness concerns.
status: implemented
arguments:
  - name: input
    short: i
    type: string
    required: true
    description: Path to proposal/decision document or JSON
  - name: values
    short: v
    type: string
    description: Path to company values/mission JSON
  - name: out
    short: o
    type: string
    description: Output file path
category: Utilities
last_updated: '2026-02-13'
tags:
  - gemini-skill
---

# Visionary Ethos Keeper

This skill ensures that engineering and business decisions align with company values and ethical principles.

## Capabilities

### 1. Value Alignment Check

- Scores proposals against core company values (User First, Transparency, Innovation, etc.)
- Identifies unaddressed values and gaps.

### 2. Ethical Review

- Checks for dark patterns, bias amplification, environmental waste, and labor concerns.
- Generates recommendations for ethical compliance.

## Usage

- "Check if this product proposal aligns with our company mission and values."
- "Review this AI system design for ethical concerns."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`.
