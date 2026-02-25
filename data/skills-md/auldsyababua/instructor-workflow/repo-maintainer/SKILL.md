---
name: repo-maintainer
description: Audits and reorganizes messy repositories into clean, LLM-friendly structures. It uses a non-destructive "Migration Manifest" process to safely consolidate scripts, establish documentation, and create AI context zones.
---

# Repository Maintainer

## Overview

This skill turns disorganized codebases ("polluted roots," "orphan scripts") into structured, readable repositories. It prioritizes **LLM-Readability** (creating explicit context maps) and **Safety** (using a reversible migration manifest).

Use this skill when:
- A repository has too many files in the root directory.
- Documentation is missing, outdated, or scattered.
- An LLM struggles to find relevant context due to noise.
- You need to "refactor" the file structure without breaking git history.

## Workflow

### 1. The Audit (Discovery)
First, analyze the repository to understand "Hot" (frequently changed) vs "Cold" (stale) zones.
- Run `scripts/scaffold_manifest.py` to generate a draft manifest.
- Identify the "blood flow" (dependencies): Does `main.py` import that messy script?
- **Output:** A mental model of the current chaos.

### 2. The Manifest (Planning)
Do not move files immediately. Create a `migration_manifest.yaml` that defines the desired state.
- Run `scripts/scaffold_manifest.py` to generate a draft manifest if you haven't already.
- Categorize files into:
    - **Core:** Application logic (`src/`)
    - **Scaffolding:** Configs (`.env`, `docker-compose`)
    - **Artifacts:** One-off scripts (Move to `archive/`)
    - **Knowledge:** Docs (Move to `docs/`)
- Review the YAML file. It is the "Contract of Changes."

### 3. Execution (Safe Move)
Apply the changes using the manifest.
- Run `scripts/apply_migration.py`.
- **Safety Rule:** This script uses `git mv` to preserve history.
- **Quarantine:** Unknown scripts go to `archive/quarantine/` rather than being deleted.

### 4. LLM Optimization (Contextualizing)
Once files are moved, establish the `.ai/` directory.
- Copy `assets/CONTEXT_TEMPLATE.md` to `.ai/CONTEXT.md`.
- Fill it with a high-level summary of the architecture.
- This ensures future agents understand *why* the code exists, not just what it does.

## Directory Structure Standards

When planning the migration, aim for this specific structure (The "LLM-First" Architecture):

```text
/ (Root)
├── .ai/                 # Context specifically for LLMs
│   ├── CONTEXT.md       # Architecture & Business Logic
│   └── GUIDELINES.md    # Coding standards
├── src/                 # Source code
├── scripts/             # DevOps/Maintenance scripts
├── docs/                # Human documentation
├── archive/             # Deprecated/Quarantine
└── README.md            # The Map
```
