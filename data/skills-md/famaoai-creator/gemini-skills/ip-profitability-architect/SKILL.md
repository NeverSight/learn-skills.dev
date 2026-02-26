---
name: ip-profitability-architect
description: Designs business and licensing models for internal intellectual property. Transforms IP from a protection cost into a revenue-generating asset.
status: implemented
arguments:
  - name: input
    short: i
    type: string
    required: true
    description: Path to JSON with IP portfolio data
  - name: out
    short: o
    type: string
    description: Output file path
category: Strategy & Leadership
last_updated: '2026-02-13'
tags:
  - finops
  - gemini-skill
---

# IP Profitability Architect

This skill turns your proprietary code into a strategic profit engine.

## Capabilities

### 1. Monetization Modeling

- Analyzes patentable code found by `ip-strategist` and proposes licensing models (SaaS, OEM, White-label).
- Estimates potential revenue from opening certain modules as "Commercial SDKs."

### 2. Open-Source Strategy

- Evaluates the business impact of open-sourcing parts of the codebase to build community trust vs. keeping them proprietary for competitive edge.

## Usage

- "How can we monetize our unique order validation algorithm?"
- "Draft a licensing model for our AI-native UI components."

## Knowledge Protocol

- Adheres to `knowledge/orchestration/knowledge-protocol.md`.
