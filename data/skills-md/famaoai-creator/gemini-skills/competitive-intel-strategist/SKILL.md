---
name: competitive-intel-strategist
description: Analyzes competitor releases and market trends to propose technical differentiation strategies. Ensures our products stay ahead by leveraging our unique code assets.
status: implemented
arguments:
  - name: input
    short: i
    type: string
    required: true
    description: Path to JSON file with competitive data
  - name: out
    short: o
    type: string
    description: Output file path
category: Strategy & Leadership
last_updated: '2026-02-13'
tags:
  - gemini-skill
---

# Competitive Intelligence Strategist

This skill helps the CEO win in the market by identifying technical "blue oceans."

## Capabilities

### 1. Competitive Gap Analysis

- Monitors competitor announcements and maps them against our current project capabilities (using `codebase-mapper`).
- Identifies where we are lagging or where we have a unique technical advantage.

### 2. Differentiation Strategy

- Proposes "Killer Features" by combining our internal IP with emerging technologies found by `innovation-scout`.

## Usage

- "Analyze Competitor X's latest API update and suggest how we can offer a superior developer experience."
- "What is our unique technical value proposition compared to the current market trend?"

## Knowledge Protocol

- Adheres to `knowledge/orchestration/knowledge-protocol.md`.
