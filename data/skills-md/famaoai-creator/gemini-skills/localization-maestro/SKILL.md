---
name: localization-maestro
description: Manages global expansion by automating i18n workflows and auditing for cultural/regional appropriateness. Handles formats, currency, and sensitive localized expressions.
status: implemented
arguments:
  - name: dir
    short: d
    type: string
    description: Project directory
  - name: locale
    short: l
    type: string
    description: Target locale (e.g., ja, fr, de)
  - name: out
    short: o
    type: string
    description: Output file path
category: Strategy & Leadership
last_updated: '2026-02-13'
tags:
  - compliance
  - gemini-skill
---

# Localization Maestro

This skill ensures your application is truly global, not just translated.

## Capabilities

### 1. i18n Automation

- Synchronizes translation files across multiple languages.
- Detects hardcoded strings and migrates them to resource files.

### 2. Cultural & Regional Audit

- **Visual Verification**: Uses `browser-navigator` to capture screenshots after language switching. Checks for layout breaks caused by long strings (e.g., German) or bidirectional text.
- **Regional Compliance**: Checks for appropriate date/time formats and currency symbols.

## Usage

- "Audit the `i18n/` files for completeness and check for culturally sensitive content in the Japanese version."
- "Extract all hardcoded strings in `src/pages` and move them to `en.json`."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
