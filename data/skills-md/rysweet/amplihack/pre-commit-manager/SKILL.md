---
name: pre-commit-manager
version: 1.0.0
description: |
  Manage pre-commit hooks with preference memory and template-based configuration.
  Use when installing, configuring, enabling/disabling, or checking status of pre-commit hooks.
  Supports templates for python, javascript, typescript, go, rust, and generic projects.
auto_activates:
  - "Install pre-commit hooks"
  - "Configure pre-commit"
  - "Enable pre-commit auto-install"
  - "Disable pre-commit auto-install"
  - "Show pre-commit status"
  - "Check pre-commit status"
  - "Generate secrets baseline"
  - "Create detect-secrets baseline"
  - "Set up pre-commit"
priority_score: 38.0
---

# Pre-Commit Manager Skill

Manage pre-commit hooks with preference memory and template-based configuration.

## Operations

### 1. Install

Install pre-commit hooks in current repository.

**Usage:**

```
Install pre-commit hooks now
```

**What it does:**

- Checks if `.pre-commit-config.yaml` exists
- Verifies pre-commit binary is available
- Runs `pre-commit install`
- Reports success/failure

### 2. Configure

Generate `.pre-commit-config.yaml` from templates.

**Usage:**

```
Configure pre-commit with python template
Configure pre-commit with javascript template
Configure pre-commit with generic template
```

**Templates:**

- `python` - Python projects (black, ruff, mypy)
- `javascript` - JS/TS projects (prettier, eslint)
- `typescript` - TypeScript projects
- `generic` - Language-agnostic (trailing whitespace, file size, detect-secrets)

### 3. Enable

Set preference to "always" auto-install.

**Usage:**

```
Enable pre-commit auto-install
```

### 4. Disable

Set preference to "never" auto-install.

**Usage:**

```
Disable pre-commit auto-install
```

### 5. Status

Show current pre-commit status.

**Usage:**

```
Show pre-commit status
Check pre-commit status
```

**Shows:**

- Git repository status
- Config file existence
- Hooks installation status
- Current preference setting
- Pre-commit binary availability

### 6. Baseline

Generate `.secrets.baseline` for detect-secrets.

**Usage:**

```
Generate secrets baseline
Create detect-secrets baseline
```

## Implementation

This skill interfaces with:

- `.claude/tools/amplihack/hooks/precommit_prefs.py` - Preference management
- `.claude/tools/amplihack/hooks/precommit_installer.py` - Hook installation
- Templates in `templates/` directory

## Security

- Path traversal prevention
- Template whitelist validation
- No `shell=True` in subprocess calls
- Subprocess timeouts enforced

## Reference

Based on: https://gist.github.com/MangaD/6a85ee73dd19c833270524269159ed6e#4-installing-and-setting-up-pre-commit
