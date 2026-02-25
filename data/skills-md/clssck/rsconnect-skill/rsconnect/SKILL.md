---
name: rsconnect
description: Posit Connect deployment workflows for R and Python. Use only for Connect/rsconnect/manifest.json/renv/requirements/uv deployment issues, git-backed content, version upgrades, and bundle errors.
license: MIT
compatibility: Requires R + renv + rsconnect (>= 0.8.15) for R content, or Python 3.10+ + uv + rsconnect-python for Python content.
metadata:
  author: clssck
  version: "2.0.0"
---

# Posit Connect Deployment Guide

In commands below, `$SKILL_DIR` means the directory containing this file. Replace it with the actual path when executing (e.g., `.claude/skills/rsconnect`, `.cursor/skills/rsconnect`).

## First-Time Setup: Gitignore

**On first use, ensure the agent skills directory is gitignored.** The skill folder (e.g., `.cursor/`, `.agents/`, `.claude/`) should not be committed to the project repository.

Check if `.gitignore` already contains the relevant entry. If not, add it:

```bash
# For Cursor-installed skills:
echo ".cursor/" >> .gitignore

# For .agents/ installed skills:
echo ".agents/" >> .gitignore

# For Claude Code skills:
echo ".claude/" >> .gitignore
```

> **Rule:** Only add the entry for the agent directory that is actually present in the project. Do not add entries for directories that don't exist.

## Before Proceeding

**Ask the user if not clear from context:**

1. **Is this R or Python content?**
   - **R** — Uses renv.lock, rsconnect R package → see [R sections](#quick-start-r) below
   - **Python** — Uses requirements.txt, uv, rsconnect-python → see [Python sections](#quick-start-python-uv) below

2. **How is this app deployed to Connect?**
   - **Git-backed** — Connect pulls from Git automatically (needs `manifest.json`) - *simplest for teams*
   - **RStudio IDE** — Click "Publish" button in IDE (R only)
   - **R console** — `rsconnect::deployApp()` (R only)
   - **Jupyter** — Publish from notebook interface
   - **Command line** — `rsconnect deploy manifest`
   - **Not sure** — Check Connect UI → Content → Your App → Info tab (shows deployment source)

3. **If Git-backed, what branch does Connect watch?**
   - Check Connect UI → Content → Your App → Info → "Git Repository" section
   - **Recommendation:** Use a dedicated deploy branch (e.g., `deploy`, `production`) so you control when changes go live

> Note: **This skill focuses on Git-backed deployment** (the default for this project). For push-button methods, the main difference is you don't need `manifest.json` — rsconnect generates the bundle on-the-fly.

---

## Windows Notes
- Prefer PowerShell or Git Bash/WSL for command execution.
- If `python` is not on PATH, use `py -3` (Python launcher).
- If `Rscript` is not on PATH, use `Rscript.exe`.
- Install uv with PowerShell: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`.


# R Deployment

## Quick Start (R)

```bash
# 1. Check if ready to deploy
Rscript $SKILL_DIR/scripts/pre_deploy_check.R

# 2. Fix any issues reported, then commit
git add manifest.json renv.lock && git commit -m "chore: update manifest"

# 3. Push (Connect auto-deploys from Git)
git push
```

## First Step: Gather R Project Status

Before doing anything else, run the pre-deploy check to understand the current state:

```bash
Rscript $SKILL_DIR/scripts/pre_deploy_check.R
```

This reports: R version, rsconnect version, manifest status, Source:unknown count, and library sync state. Use the output to inform your response.

---

## R Key Concepts

### renv.lock vs manifest.json

| File | Purpose | When to Update |
|------|---------|----------------|
| `renv.lock` | Records YOUR local package versions | After `renv::install()` or `renv::update()` |
| `manifest.json` | Tells Connect what to install | After changing `renv.lock` or app files |

**They can drift!** Always update both together:
```r
renv::snapshot()           # Update renv.lock
rsconnect::writeManifest() # Update manifest.json
```

### What is "Source: unknown"?

Connect needs to know WHERE to download each package. `Source: unknown` means Connect can't find it.

**Common causes:** Package installed from local file, missing repo in options, Bioconductor package without prefix.

**Fix:** `Rscript $SKILL_DIR/scripts/fix_unknown_sources.R --dry-run`

---

## R Helper Scripts

| Script | Purpose | Flags |
|--------|---------|-------|
| `pre_deploy_check.R` | Validate deployment readiness | |
| `diagnose.R` | Full diagnostics report | `--verbose` |
| `fix_unknown_sources.R` | Fix Source:unknown packages | `--dry-run`, `--help` |
| `regenerate_manifest.R` | Regenerate manifest.json | |
| `precommit_check.R` | Git pre-commit hook validation | |

```bash
# Run from project root
Rscript $SKILL_DIR/scripts/<script>.R
```

### Git Pre-commit Hook

Automatically validate deployment files before each commit:

```bash
# Install the pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
Rscript $SKILL_DIR/scripts/precommit_check.R
EOF
chmod +x .git/hooks/pre-commit
```

```powershell
# PowerShell (Windows)
# Replace $SKILL_DIR with your actual skill path
@'
#!/usr/bin/env pwsh
& Rscript $SKILL_DIR/scripts/precommit_check.R
exit $LASTEXITCODE
'@ | Set-Content .git/hooks/pre-commit
```
Note: Requires PowerShell 7+ (`pwsh`). If unavailable, run the bash snippet in Git Bash or WSL.

The hook checks:
- No `Source: unknown` packages in staged `renv.lock`
- Manifest freshness when `renv.lock` is staged
- Manifest exists when `renv.lock` is staged

To bypass (not recommended): `git commit --no-verify`

---

## R Common Workflows

### Deploy After Code Changes (R)

```bash
renv::snapshot()  # If dependencies changed
Rscript $SKILL_DIR/scripts/regenerate_manifest.R
git add renv.lock manifest.json
git commit -m "chore: update manifest"
git push
```

### Fix Source:unknown Error

```bash
# 1. See what would change (safe)
Rscript $SKILL_DIR/scripts/fix_unknown_sources.R --dry-run

# 2. Apply fixes (creates backup)
Rscript $SKILL_DIR/scripts/fix_unknown_sources.R

# 3. Regenerate manifest
Rscript $SKILL_DIR/scripts/regenerate_manifest.R
```

### Rollback a Bad Deployment

```bash
# Option 1: Revert to previous commit
git revert HEAD
git push

# Option 2: Restore from backup (if fix_unknown_sources.R was run)
cp renv.lock.backup.YYYYMMDD_HHMMSS renv.lock
Rscript $SKILL_DIR/scripts/regenerate_manifest.R
git add -A && git commit -m "fix: rollback deployment"
git push

# Option 3: In Connect UI
# Go to Content → Your App → History → Activate previous bundle
```

### R Version Upgrade

1. Install new R version
2. Back up: `cp renv.lock renv.lock.bak`
3. From new R session:
   ```r
   renv::init()  # Select option 2: re-initialize
   ```
4. Fix any Source:unknown issues
5. Regenerate manifest and deploy

See [references/troubleshooting.md](references/troubleshooting.md) for detailed migration steps.

---

# Python Deployment (uv)

## Quick Start (Python / uv)

```bash
# 1. Check if ready to deploy
python $SKILL_DIR/scripts/pre_deploy_check_py.py

# 2. Fix any issues reported, then commit
git add manifest.json requirements.txt && git commit -m "chore: update manifest"

# 3. Push (Connect auto-deploys from Git)
git push
```

## First Step: Gather Python Project Status

Before doing anything else, run the Python pre-deploy check:

```bash
python $SKILL_DIR/scripts/pre_deploy_check_py.py
```

This reports: Python version, uv/rsconnect status, pyproject.toml presence, manifest status, requirements.txt sync, and allow_uv setting. Use the output to inform your response.

---

## Python Key Concepts

### requirements.txt vs manifest.json

| File | Purpose | When to Update |
|------|---------|----------------|
| `requirements.txt` | Records YOUR Python package versions | After `uv add` or `uv remove` |
| `manifest.json` | Tells Connect what to install | After changing requirements.txt or app files |

**They can drift!** Always update both together:
```bash
uv export --no-hashes -o requirements.txt  # Update requirements.txt
rsconnect write-manifest <type> .           # Update manifest.json
```

### uv Workflow

[uv](https://docs.astral.sh/uv/) is a fast Python package manager. Key commands:

| Action | Command |
|--------|---------|
| Add a package | `uv add <pkg>` |
| Remove a package | `uv remove <pkg>` |
| Sync environment | `uv sync` |
| Export for Connect | `uv export --no-hashes -o requirements.txt` |
| Run a tool | `uvx <tool>` (e.g., `uvx rsconnect-python`) |

`uv export` requires `pyproject.toml`. If it's missing, `regenerate_manifest_py.py` can create a minimal one, but review it before committing.

### What is `allow_uv`?

As of Connect 2024.12.0, Connect can use `uv pip` instead of `pip` for faster Python package installs. Setting `allow_uv: true` in manifest.json's `python.package_manager` section opts in.

The `regenerate_manifest_py.py` script patches this automatically. Currently `rsconnect-python` CLI doesn't have a flag for it — the script patches `manifest.json` after generation.

---

## Python Helper Scripts

| Script | Purpose | Flags |
|--------|---------|-------|
| `pre_deploy_check_py.py` | Validate Python deployment readiness | |
| `diagnose_py.py` | Full Python diagnostics report | `--verbose`, `--help` |
| `regenerate_manifest_py.py` | Regenerate manifest for Python apps | `--type`, `--no-uv-export`, `--no-allow-uv` |

```bash
# Run from project root
python $SKILL_DIR/scripts/<script>.py
```

### Content Type Detection

The `regenerate_manifest_py.py` script auto-detects your framework:
It scans common entrypoints in the project root, `src/`, and importable package directories (plus pyproject entry points).

| Framework | Detected By | rsconnect Type |
|-----------|-------------|----------------|
| FastAPI | `from fastapi import` | `fastapi` |
| Flask | `from flask import` | `api` |
| Dash | `from dash import` | `dash` |
| Streamlit | `import streamlit` | `streamlit` |
| Bokeh | `import bokeh` | `bokeh` |
| Jupyter notebook | `.ipynb` files | `notebook` |
| Generic API | Default fallback | `api` |

Override with: `python $SKILL_DIR/scripts/regenerate_manifest_py.py --type fastapi`

---

## Python Common Workflows

### Deploy After Code Changes (Python)

```bash
uv export --no-hashes -o requirements.txt  # If dependencies changed
python $SKILL_DIR/scripts/regenerate_manifest_py.py
git add requirements.txt manifest.json
git commit -m "chore: update manifest"
git push
```

### Regenerate Manifest (Python)

```bash
# Auto-detect framework
python $SKILL_DIR/scripts/regenerate_manifest_py.py

# Specify framework explicitly
python $SKILL_DIR/scripts/regenerate_manifest_py.py --type fastapi

# Skip uv export (use existing requirements.txt)
python $SKILL_DIR/scripts/regenerate_manifest_py.py --no-uv-export
```

### Python Version Upgrade

1. Update `.python-version` with **exact** major.minor.patch (e.g. `3.13.6`, not `3.13`)
   — Posit Connect requires exact version pinning
2. Run: `uv sync`
3. Export: `uv export --no-hashes -o requirements.txt`
4. Regenerate manifest: `python $SKILL_DIR/scripts/regenerate_manifest_py.py`
5. Commit and push

### Rollback a Bad Deployment (Python)

```bash
# Option 1: Revert to previous commit
git revert HEAD
git push

# Option 2: In Connect UI
# Go to Content → Your App → History → Activate previous bundle
```

---

# Shared Concepts (R & Python)

## Deployment Methods

| Method | Language | Best For | Needs manifest.json? |
|--------|----------|----------|---------------------|
| **Git-backed** | R & Python | Teams, CI/CD, reproducibility | Yes |
| RStudio IDE | R | Quick one-off deploys | No (auto-generated) |
| R console | R | Scripted deploys | No |
| Jupyter | R & Python | Notebooks | No |
| CLI (`rsconnect deploy`) | R & Python | CI pipelines without Git integration | Yes |

### Git-backed (This Project)

**How it works:**
1. You generate `manifest.json` locally
2. You push to Git (with manifest.json + renv.lock/requirements.txt)
3. Connect polls your branch (configurable, default 15 min) and auto-deploys

**Why it's the easiest for teams:**
- No credentials needed on dev machines (just Git access)
- Deployment = `git push`
- Full audit trail in Git history
- Easy rollback (`git revert`)

**Requirements (R):** rsconnect ≥ 0.8.15, manifest.json committed to repo
**Requirements (Python):** rsconnect-python, manifest.json committed to repo

> **Note:** Once Git-backed, stay Git-backed. You can't switch to push-button without recreating the content in Connect.

---

## Branch Strategy

### Recommended: Deploy Branch

```
main (development)
  │
  └── deploy (Connect watches this branch)
```

**Workflow (R):**
```bash
git checkout deploy
git merge main
Rscript $SKILL_DIR/scripts/regenerate_manifest.R
git add manifest.json renv.lock
git commit -m "chore: update manifest for deploy"
git push origin deploy
```

**Workflow (Python):**
```bash
git checkout deploy
git merge main
python $SKILL_DIR/scripts/regenerate_manifest_py.py
git add manifest.json requirements.txt
git commit -m "chore: update manifest for deploy"
git push origin deploy
```

### Multi-environment Setup

```
main (development)
  ├── staging (Connect staging server watches)
  └── production (Connect prod server watches)
```

Each Connect server points to a different branch. Merge up through environments:
`main` → `staging` → `production`

---

## Pre-deploy Checklist

### R Projects
- [ ] Run `Rscript $SKILL_DIR/scripts/pre_deploy_check.R`
- [ ] No Source:unknown packages
- [ ] Manifest is up to date
- [ ] `.rscignore` excludes dev artifacts
- [ ] On correct branch for deployment
- [ ] Commit and push

### Python Projects
- [ ] Run `python $SKILL_DIR/scripts/pre_deploy_check_py.py`
- [ ] requirements.txt is up to date
- [ ] `pyproject.toml` exists (required for uv export)
- [ ] Manifest is up to date
- [ ] `allow_uv: true` in manifest (recommended)
- [ ] `.rscignore` excludes dev artifacts (`.venv/`, `__pycache__/`, etc.)
- [ ] On correct branch for deployment
- [ ] Commit and push

---

## Additional Resources

- **Script docs:** [scripts/README.md](scripts/README.md)
- **Troubleshooting:** [references/troubleshooting.md](references/troubleshooting.md)
- **Commands:** [references/commands.md](references/commands.md)

### External Links

- [Posit Connect Git-backed docs](https://docs.posit.co/connect/user/git-backed/)
- [renv documentation](https://rstudio.github.io/renv/)
- [rsconnect writeManifest](https://rstudio.github.io/rsconnect/reference/writeManifest.html)
- [uv documentation](https://docs.astral.sh/uv/)
- [rsconnect-python docs](https://docs.posit.co/rsconnect-python/)
