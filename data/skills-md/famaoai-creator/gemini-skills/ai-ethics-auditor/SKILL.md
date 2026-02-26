---
name: ai-ethics-auditor
description: Audits AI systems for bias, fairness, and privacy. Analyzes prompts and datasets to ensure ethical and safe AI implementation.
status: implemented
arguments:
  - name: input
    short: i
    type: string
    required: true
    description: Path to AI config, prompt, or dataset file
  - name: out
    short: o
    type: string
    description: Output file path
category: Governance & Security
last_updated: '2026-02-13'
tags:
  - compliance
  - data-engineering
  - gemini-skill
---

# AI Ethics Auditor

This skill protects your organization by ensuring AI implementations are fair, unbiased, and respect user privacy.

## Capabilities

### 1. Bias & Fairness Audit

- Analyzes prompts for stereotypical or discriminatory language.
- Checks if datasets contain historical biases that could lead to unfair AI decisions.

### 2. AI Safety Verification

- Verifies that PII (Personally Identifiable Information) is not leaked through AI responses.
- Audits for "dark patterns" in AI-driven user interactions.

## Usage

- "Audit our RAG prompt for potential gender or racial bias."
- "Perform an ethics check on this customer support chatbot dataset."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
