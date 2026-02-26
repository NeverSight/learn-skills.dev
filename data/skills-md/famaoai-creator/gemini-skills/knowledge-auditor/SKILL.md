---
name: knowledge-auditor
description: Audits the 3-tier knowledge base for consistency, freshness, and cross-tier contradictions. Ensures that proprietary standards align with (or intentionally override) public ones.
status: implemented
category: Governance & Security
last_updated: '2026-02-13'
tags:
  - compliance
  - gemini-skill
---

# Knowledge Auditor

This skill maintains the health and accuracy of the global knowledge base.

## Capabilities

### 1. Multi-Tier Consistency Check

- Scans `Public`, `Confidential`, and `Personal` tiers for conflicting instructions on the same topic.
- Reports where a `Confidential` standard is missing a required override for a new `Public` update.

### 2. Freshness Verification

- Compares knowledge entries against recently fetched research (e.g., from `innovation-scout` or `google_web_search`).
- Flags "Knowledge Decay" in entries that haven't been updated despite significant industry shifts.

### 3. Structural Integrity

- Checks for dead links between documents.
- Verifies that all `Client-Specific` tiers follow the `theme_design_guide.md`.

## Usage

- "Audit all FISC-related knowledge for contradictions with the latest AWS blog updates."
- "Perform a full consistency check across all 3 tiers of the knowledge base."
- "Identify any outdated project standards in the confidential tier."
