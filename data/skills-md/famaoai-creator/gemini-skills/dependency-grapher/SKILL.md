---
name: dependency-grapher
description: Generate dependency graphs (Mermaid/DOT) from project files.
status: implemented
category: Engineering & DevOps
last_updated: '2026-02-13'
tags:
  - automation
  - gemini-skill
---

# Dependency Grapher

Generate dependency graphs (Mermaid/DOT) from project files.

## Usage

node dependency-grapher/scripts/graph.cjs [options]

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
