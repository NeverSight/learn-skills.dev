---
name: tech-dd-analyst
description: Performs Technical Due Diligence on startups. Analyzes code (if available) or evaluates public signals (hiring, blogs) to assess technical risk and team maturity.
status: implemented
arguments:
  - name: dir
    short: d
    type: string
    description: Project directory to analyze
  - name: out
    short: o
    type: string
    description: Output file path
category: Utilities
last_updated: '2026-02-13'
tags:
  - gemini-skill
---

# Tech DD Analyst

This skill acts as your "Technical Investigator" for investment decisions.

## Capabilities

### 1. Repository Analysis (Whitebox)

- If GitHub access is provided:
  - Calculates "Bus Factor" (dependency on key individuals).
  - Identifies "Spaghetti Code" and lack of tests using `cognitive-load-auditor`.

### 2. Public Signal Analysis (Blackbox)

- Analyzes Job Descriptions (JD) to infer the tech stack and "Technical Debt" (e.g., hiring for "PHP migration").
- Evaluates the CTO's technical blog posts for depth and thought leadership.

### 3. Interview Strategy

- Generates a customized "CTO Interview Script" based on the startup's stage and domain.
- Example: "Ask about their disaster recovery plan for the 'Single-Master DB' risk identified in their architecture diagram."

## Usage

- "Perform a Tech DD on 'Startup X'. Here is their GitHub URL."
- "I don't have code access for 'Startup Y'. Generate a list of technical questions to ask their CTO."

## Knowledge Protocol

- Adheres to `knowledge/ceo/investment/tech_dd_standard.md`.
