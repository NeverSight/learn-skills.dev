---
name: diff-visualizer
description: Generate a visual difference report between two texts.
status: implemented
arguments:
  - name: old
    short: a
    type: string
    required: true
  - name: new
    short: b
    type: string
    required: true
  - name: out
    short: o
    type: string
category: Utilities
last_updated: '2026-02-13'
tags:
  - automation
  - gemini-skill
---

# Diff Visualizer

Generate a visual difference report between two texts.

## Usage

node diff-visualizer/scripts/diff.cjs [options]

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
