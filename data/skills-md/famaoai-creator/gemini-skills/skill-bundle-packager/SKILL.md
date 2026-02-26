---
name: skill-bundle-packager
description: Dynamically bundles mission-specific skills into specialized subsets. Optimizes agent performance by focusing on relevant tools for specific high-level tasks.
status: implemented
category: Utilities
last_updated: '2026-02-13'
tags:
  - gemini-skill
  - performance
---

# Skill Bundle Packager

This skill optimizes operational focus by creating specialized "Strike Teams" of skills.

## Capabilities

### 1. Mission-Specific Bundling

- Identifies the required tools for a specific task (e.g., "Full Audit" = `security-scanner` + `license-auditor` + `ux-auditor`).
- Creates temporary execution contexts where only the necessary skills are prioritized.

### 2. Export & Deploy

- Prepares skill packages for deployment to specific project sub-directories or separate CI pipelines.

## Usage

- "Bundle all skills necessary for a 'Production Hand-off' mission."
- "Package a 'Security Strike Team' for our legacy binary audit."

## Commands

```bash
# Create a bundle for a specific mission
node skill-bundle-packager/scripts/bundle.cjs <mission-name> <skill-1> <skill-2> ...
```

## Knowledge Protocol

- Adheres to `knowledge/orchestration/optimization-standards.md`.
