---
name: api-evolution-manager
description: Governs the evolution of public APIs. Detects breaking changes, manages deprecation cycles, and generates migration guides for clients.
status: implemented
arguments:
  - name: current
    short: c
    type: string
    required: true
    description: Path to current API spec (OpenAPI JSON/YAML)
  - name: previous
    short: p
    type: string
    description: Path to previous API spec for diff
  - name: out
    short: o
    type: string
    description: Output file path
category: Utilities
last_updated: '2026-02-13'
tags:
  - automation
  - gemini-skill
  - integration
---

# API Evolution Manager

This skill ensures that your API grows gracefully without breaking downstream consumers.

## Capabilities

### 1. Breaking Change Detection

- Compares current API schemas (OpenAPI, GraphQL) with previous versions.
- Flags any changes that would break backward compatibility.

### 2. Lifecycle Management

- Manages deprecation notices and sunsetting schedules.
- Automatically generates "Migration Guides" for developers using the API.

## Usage

- "Audit the latest API changes for breaking changes and update the versioning plan."
- "Generate a migration guide for clients moving from v1.0 to v2.0."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
