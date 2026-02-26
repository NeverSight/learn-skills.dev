---
name: ai-model-orchestrator
description: Dynamically selects the optimal AI model based on task complexity, cost, and latency. Routes requests to Gemini, GPT-4, Claude, or local LLMs to maximize efficiency.
status: implemented
arguments:
  - name: input
    short: i
    type: string
    required: true
    description: Path to JSON task description or text prompt file
  - name: budget
    short: b
    type: string
    description: Cost tier preference
  - name: out
    short: o
    type: string
    description: Output file path
category: Utilities
last_updated: '2026-02-13'
tags:
  - finops
  - gemini-skill
---

# AI Model Orchestrator

This skill ensures that the most appropriate and cost-effective intelligence is used for every task.

## Capabilities

### 1. Task Triage

- Analyzes the "Hardness" of a prompt or code task.
- Routes simple tasks (e.g., translation, basic cleanup) to faster/cheaper models.
- Routes complex tasks (e.g., architectural design, deep debugging) to state-of-the-art models.

### 2. Multi-Provider Fallback

- Automatically switches providers if an API is down or throttled.
- Compares outputs from multiple models for critical tasks (consensus building).

## Usage

- "Execute the code review using the most cost-effective model that maintains high precision."
- "Orchestrate a multi-model evaluation of our new security architecture."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
