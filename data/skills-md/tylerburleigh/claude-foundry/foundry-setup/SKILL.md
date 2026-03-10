---
name: foundry-setup
description: First-time setup for the foundry plugin (plugin:foundry@claude-foundry)
disable-model-invocation: true
---

# Foundry Setup Skill

First-time setup for the foundry plugin. This skill is idempotent and safe to run multiple times.

## Argument Handling

Check if `$ARGUMENTS` contains `--check` or `--preflight`:
- **If flag present:** Run only Phase 1 (Pre-flight Checks), display results, then stop
- **If no flag:** Run all phases (full setup)

## Execution

**MANDATORY:** Read `references/setup.md` before proceeding. It contains the detailed phase instructions.

### Flow

```
- **Entry** → Read `references/setup.md` (MANDATORY) → Ensure Full Mode → Preflight: MCP, Python, Git
  - [--check?] → **Exit**
  - [else] → Permissions → Workspace
    - [toml created?] → FeatureFlags → Providers → Research → TestConfig
    - [else] → Create TOML → FeatureFlags → Providers → Research → TestConfig
    - CLAUDE.md Configuration → Summary → **Exit**
```
