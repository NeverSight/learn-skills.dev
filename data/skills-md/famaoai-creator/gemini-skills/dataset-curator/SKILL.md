---
name: dataset-curator
description: Prepares and audits high-quality datasets for AI/RAG applications. Cleans noise, structure data, and ensures privacy compliance in knowledge bases.
status: implemented
arguments:
  - name: input
    short: i
    type: string
    required: true
    description: Path to data file (JSON/CSV/text)
  - name: out
    short: o
    type: string
    description: Output file path
  - name: format
    short: f
    type: string
    description: Data format
category: Data & Content
last_updated: '2026-02-13'
tags:
  - compliance
  - data-engineering
  - gemini-skill
---

# Dataset Curator

This skill ensures that the data you feed to your AI is clean, accurate, and safe.

## Capabilities

### 1. Data Cleaning & Structuring

- Removes duplicates, boilerplate, and noisy text from knowledge bases.
- Converts unstructured documents into clean Markdown or JSON/Vector-friendly formats.

### 2. Privacy Audit

- Scans datasets for PII (Personal Identifiable Information) before they are sent to LLMs or vector databases.

## Usage

- "Clean up the `knowledge/` directory and structure it for better RAG performance."
- "Audit this customer feedback dataset for sensitive info before we use it for AI training."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
