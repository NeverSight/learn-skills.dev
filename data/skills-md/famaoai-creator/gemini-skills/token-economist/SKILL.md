---
name: token-economist
description: Minimizes token consumption and costs by optimizing data input. Performs smart summarization and chunking of large files without losing critical context.
status: implemented
arguments:
  - name: input
    short: i
    type: string
    description: Path to a file to analyze
  - name: text
    short: t
    type: string
    description: Raw text string to analyze
category: Utilities
last_updated: '2026-02-13'
tags:
  - data-engineering
  - finops
  - gemini-skill
---

# Token Economist

This skill focuses on cost-efficiency and precision when dealing with large-scale data in LLMs.

## Capabilities

### 1. Smart Summarization

- Condenses large log files or documentation into "information-dense" summaries.
- Strips redundant or boilerplate text before sending to the model.

### 2. Intelligent Chunking

- Splits large files based on logical boundaries (e.g., function blocks, sections) rather than raw character counts.
- Maintains cross-chunk context through small overlaps or "context headers."

## Usage

- "Summarize this 10MB log file for analysis, keeping only the error patterns and stack traces."
- "The codebase is too large; use `token-economist` to prepare a dense overview for the AI."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
