---
name: word-artisan
description: Generate Word documents (.docx) from Markdown.
status: implemented
category: Data & Content
last_updated: '2026-02-13'
tags:
  - automation
  - documentation
  - gemini-skill
related_skills:
  - api-doc-generator
---

# Word Artisan

Generate professional, comprehensive Word documents (.docx) from Markdown.

## Documentation Fidelity Modes

1.  **Executive Summary**: Focus on high-level goals, budget, and impact.
2.  **Standard Specification**: Balanced view of functional and non-functional requirements.
3.  **Comprehensive Deep-Dive**: Exhaustive technical documentation including every parameter, CLI command, and edge case. Essential for NFR definitions and security audits.

## High-Fidelity Documentation Workflow

1.  **Standard Alignment**: Choose the appropriate standard (e.g., IPA Grade) based on the target fidelity.
2.  **Detail-Oriented Writing**: For Deep-Dive mode, expand sections with specific technical configurations.
3.  **Visual Styling**: Apply professional templates consistently.

## Usage

node word-artisan/scripts/convert.cjs [options]

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
