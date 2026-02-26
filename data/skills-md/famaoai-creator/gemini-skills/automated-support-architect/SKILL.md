---
name: automated-support-architect
description: Generates high-quality user support assets (FAQs, Troubleshooting Guides, Chatbot Knowledge) directly from source code and requirements. Bridges the gap between developers and end-users.
status: implemented
arguments:
  - name: dir
    short: d
    type: string
    description: Project directory
  - name: type
    short: t
    type: string
    description: Support asset type
  - name: out
    short: o
    type: string
    description: Output file path
category: Strategy & Leadership
last_updated: '2026-02-13'
tags:
  - automation
  - gemini-skill
---

# Automated Support Architect

This skill transforms technical implementation details into helpful resources for end-users.

## Capabilities

### 1. Support Asset Generation

- Analyzes requirements and code to generate "How-To" guides and FAQs.
- Creates structured knowledge bases for customer support chatbots.

### 2. Error Translation

- Translates technical error codes and stack traces into user-friendly troubleshooting steps.

## Usage

- "Generate a troubleshooting guide for the new mobile checkout feature."
- "Build a support FAQ based on the latest API documentation and known edge cases."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
