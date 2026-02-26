---
name: investor-readiness-audit
description: Prepares documents and audits for fundraising or board meetings. Ensures financial, technical, and compliance data is boardroom-ready.
status: implemented
arguments:
  - name: dir
    short: d
    type: string
    description: Project directory to audit
  - name: stage
    short: s
    type: string
    description: Fundraising stage
  - name: out
    short: o
    type: string
    description: Output file path
category: Utilities
last_updated: '2026-02-13'
tags:
  - compliance
  - data-engineering
  - documentation
  - gemini-skill
---

# Investor Readiness Audit

This skill helps the CEO prepare for the "Moment of Truth" (Fundraising or IPO).

## Capabilities

### 1. Data Room Pre-check

- Audits the project for critical documentation: `RD`, `Audit Reports`, `Notice Files`, `SBoMs`.
- Validates that the "Technical Health" matches the "Business Narrative."

### 2. Pitch Deck Logic

- Ensures that financial claims are backed by raw data in the monorepo (e.g., actual server costs, delivery velocity).

## Usage

- "Are we ready for a Series B technical due diligence? Perform an audit."
- "Gather all technical and financial evidence needed for the quarterly board meeting."

## Knowledge Protocol

- Adheres to `knowledge/orchestration/knowledge-protocol.md`.
