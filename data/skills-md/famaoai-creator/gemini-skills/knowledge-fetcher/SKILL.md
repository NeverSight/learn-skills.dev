---
name: knowledge-fetcher
description: Fetch knowledge from both public and confidential directories. Bridges general best practices with proprietary internal standards.
status: implemented
arguments:
  - name: query
    short: q
    type: string
    required: true
  - name: type
    short: t
    type: string
category: Integration & API
last_updated: '2026-02-13'
tags:
  - gemini-skill
---

# Knowledge Fetcher (Hybrid Bridge)

This skill acts as the gateway to the monorepo's collective intelligence, supporting a tiered access model between public and confidential data.

## Capabilities

### 1. 3-Tier Sovereign Search

Automatically searches for relevant documentation across three tiers:

- **Public Tier**: `knowledge/` (Synced with Git).
- **Confidential Tier**: `knowledge/confidential/` (Company/Client-specific secrets).
- **Personal Tier**: `knowledge/personal/` (Strictly local, machine-specific secrets).

### 2. Multi-Source Consolidation & Precedence

- **Precedence**: Personal > Client-Confidential > General-Confidential > Public.
- Merges findings from both tiers to provide a complete context.
- Prioritizes confidential standards if a conflict exists with public ones (e.g., specific company policies overriding generic ones).

## Usage

- "Fetch all knowledge regarding [Topic], including any internal confidential standards."
- "What is our company's specific policy on [Security Method]? Check the confidential tier."

## Safety

- This skill NEVER outputs the full content of confidential files if it detects a public-facing task (like drafting an issue on GitHub). It provides summarized, safe insights instead.

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
