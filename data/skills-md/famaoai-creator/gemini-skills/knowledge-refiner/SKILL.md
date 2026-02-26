---
name: knowledge-refiner
description: Maintains and consolidates the knowledge base. Cleans up unstructured data and merges it into structured glossaries or patterns.
status: implemented
arguments:
  - name: dir
    short: d
    type: string
    description: Knowledge base directory
  - name: action
    short: a
    type: string
    description: Refinement action
  - name: out
    short: o
    type: string
    description: Output file path
category: Utilities
last_updated: '2026-02-13'
tags:
  - data-engineering
  - gemini-skill
---

# Knowledge Refiner

This skill keeps the `knowledge/` directory clean and useful.

## Capabilities

### 1. Knowledge Consolidation

- Merges multiple markdown notes into a single structured JSON/YAML glossary.
- Removes duplicate entries and resolves conflicts.

### 2. Pattern Extraction

- Analyzes unstructured text in `work/` or `knowledge/` to extract new reusable patterns for `security-scanner` or `iac-analyzer`.

## Usage

- "Refine the requirements knowledge base by merging all notes into `ipa_best_practices.md`."
- "Extract common error patterns from these logs and save them to `knowledge/security/scan-patterns.yaml`."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
