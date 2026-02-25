---
name: prompt-optimizer
description: Self-improves agent instructions and context handling. Analyzes failed or suboptimal responses to refine system prompts and prompt templates.
status: implemented
arguments:
  - name: input
    short: i
    type: string
    required: true
    description: Path to SKILL.md file to analyze
  - name: out
    short: o
    type: string
    description: Optional output file path
category: Utilities
last_updated: '2026-02-13'
tags:
  - gemini-skill
  - performance
---

# Prompt Optimizer

This skill enables the AI to self-evolve by refining its own instructions based on performance analysis.

## Capabilities

### 1. Instruction Refinement

- Analyzes existing `SKILL.md` files for ambiguity or contradictions.
- Suggests optimized wording to improve accuracy and reduce hallucinations.

### 2. Context Optimization

- Evaluates how data is passed to the AI (e.g., file contents, logs).
- Recommends more efficient ways to structure the prompt context for complex tasks.

## Usage

- "Analyze why the `security-scanner` gave a false positive and optimize its prompt instructions."
- "Optimize the system prompt in `requirements-wizard/SKILL.md` for better clarity."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
