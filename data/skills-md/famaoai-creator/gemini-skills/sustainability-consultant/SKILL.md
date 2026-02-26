---
name: sustainability-consultant
description: Estimates the environmental impact (Carbon Footprint) of code and infrastructure. Recommends optimizations for energy efficiency and "GreenOps".
status: implemented
arguments:
  - name: dir
    short: d
    type: string
    description: Project directory
  - name: out
    short: o
    type: string
    description: Output file path
category: Utilities
last_updated: '2026-02-13'
tags:
  - gemini-skill
---

# Sustainability Consultant (GreenOps)

This skill helps you build eco-friendly software by monitoring and reducing carbon emissions.

## Capabilities

### 1. Carbon Footprint Estimation

- Estimates CO2 emissions based on cloud resource types, regions (grid intensity), and runtime profiling.
- Correlates energy consumption with specific code modules.

### 2. Green Refactoring

- Suggests energy-efficient alternatives (e.g., "Move this cron job to a cleaner grid region", "Optimize this high-CPU loop").

## Usage

- "What is the estimated monthly carbon footprint of our current AWS setup?"
- "Analyze this profile and suggest code changes to reduce energy consumption."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
