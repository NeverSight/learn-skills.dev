---
name: synthetic-user-persona
description: Generates diverse AI user personas to autonomously test applications. Simulates beginners, power users, and users with accessibility needs to discover hidden UI/UX flaws.
status: implemented
arguments:
  - name: count
    short: 'n'
    type: number
    description: Number of personas to generate
  - name: product
    short: p
    type: string
    description: Product description
  - name: out
    short: o
    type: string
    description: Output file path
category: Utilities
last_updated: '2026-02-13'
tags:
  - automation
  - cloud
  - gemini-skill
  - qa
---

# Synthetic User Persona

This skill takes browser automation to the next level by simulating human behavior and diverse user needs.

## Capabilities

### 1. Persona Generation

- Creates "Virtual Users" with specific goals, skill levels, and constraints.
- Includes personas for accessibility testing (e.g., screen reader users, users with motor impairments).

### 2. Exploratory Testing

- Instead of following a script, the AI "explores" the UI based on its persona's mental model.
- Discovers non-obvious bugs and usability friction points.

## Usage

- "Have a 'Novice User' persona try to complete our checkout flow and report any confusion."
- "Perform an exploratory accessibility audit using three different synthetic personas."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
