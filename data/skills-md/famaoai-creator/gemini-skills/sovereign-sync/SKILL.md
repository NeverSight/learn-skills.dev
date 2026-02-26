---
name: sovereign-sync
description: Syncs specific knowledge tiers with external private repositories.
status: implemented
category: Utilities
last_updated: '2026-02-13'
tags:
  - gemini-skill
---

# Sovereign Sync

This skill enables the **External Knowledge Link** pattern. It allows specific tiers of the Sovereign Matrix (like L3 Confidential) to be managed as independent Git repositories, separate from the monorepo logic.

## Capabilities

### 1. Initialize Link

Link a knowledge tier to an external private repository.

- **Command**: \`node scripts/sync.cjs init <tier> <repo_url>\`

### 2. Import (Pull)

Fetch the latest maps, entity definitions, and shared analysis from the organization.

- **Command**: \`node scripts/sync.cjs pull <tier>\`

### 3. Share (Push)

Push local analysis results and updated mappings to the private organizational repository.

- **Command**: \`node scripts/sync.cjs push <tier>\`

## Default Configuration

- **L3 (Confidential)**: Intended to be synced with the organization's Private Engineering Repo.
- **L2 (Roles)**: Can optionally be synced with a restricted Executive Repo.

## Knowledge Protocol

- This skill MUST NOT be used on the \`public\` tier.
- It facilitates the "Sovereign Knowledge Sharing" required for multi-entity orchestration.
