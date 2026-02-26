---
name: nonfunctional-architect
description: Interactive guide for defining non-functional requirements based on IPA "Non-Functional Requirements Grade 2018". Helps users select appropriate service levels (Availability, Performance, Security, etc.) and generates a requirements definition document.
status: implemented
category: Strategy & Leadership
last_updated: '2026-02-13'
tags:
  - automation
  - documentation
  - gemini-skill
  - security
---

# Non-Functional Architect

## Overview

This skill assists in the **Non-Functional Requirements Definition** phase of system development. It uses the IPA "Non-Functional Requirements Grade 2018" as a knowledge base to interview the user and determine the necessary system service levels.

## Capabilities

1.  **Model-Based Assessment**:
    - Recommends requirement levels based on system impact (Low/Mid/High).
    - Utilizes [Availability Best Practices](../knowledge/operations/availability_best_practices.md) for tier classification.
2.  **Interactive Selection**:
    - Guides the user through key categories (Availability, Performance, Security, etc.) to select specific levels.
3.  **Document Generation**:
    - Exports the agreed requirements as a Markdown report (`nonfunctional_requirements.md`).

## Usage

```bash
# Start the interactive assessment
node scripts/assess.cjs
```

## Resources

- **Knowledge Base**: `assets/requirements.yaml` (Converted from IPA Excel sheet)

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
- References [Availability Best Practices](../knowledge/operations/availability_best_practices.md) for standardizing availability levels and disaster recovery goals.
