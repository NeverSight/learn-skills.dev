---
name: version-update
description: Update semantic versions across node/rust/python projects, then commit (and optionally push) in a safe release flow.
allowed-tools: Bash Read Edit
compatibility: Requires a git repository and scripts under skills/version-update/scripts.
---

# Version Update Skill

> Cross-stack semantic version update for node/rust/python.

<scripts>

## Available scripts

| Script | Purpose |
|------|------|
| `scripts/stack-detect.sh` | Detect stacks (`node`, `rust`, `python`) |
| `scripts/version-find.sh [--plain]` | Discover version-bearing files |
| `scripts/version-current.sh [file]` | Extract current semver (`file|version`) |
| `scripts/version-bump.sh <current> <type>` | Calculate next semver |
| `scripts/version-apply.sh <new> [files...]` | Apply version to discovered/selected files |
| `scripts/git-commit.sh "msg" [files]` | Commit changed files |
| `scripts/git-push.sh` | Push current branch safely |

</scripts>

<version_rules>

| Argument | Action | Example |
|------|------|------|
| `+1` / `+patch` | Patch +1 | `0.1.13 -> 0.1.14` |
| `+minor` | Minor +1 | `0.1.13 -> 0.2.0` |
| `+major` | Major +1 | `0.1.13 -> 1.0.0` |
| `x.y.z` | Explicit set | `0.1.13 -> 2.0.0` |

</version_rules>

<workflow>

## Workflow

```bash
# 1) detect stack(s)
scripts/stack-detect.sh

# 2) find version-bearing files
scripts/version-find.sh

# 3) read current version
scripts/version-current.sh
# output: <file>|<version>

# 4) compute next version
scripts/version-bump.sh 1.2.3 +minor
# -> 1.3.0

# 5) apply to all discovered files (or selected files)
scripts/version-apply.sh 1.3.0

# 6) commit
scripts/git-commit.sh "chore: bump version to 1.3.0"

# 7) optional push
scripts/git-push.sh
```

</workflow>

<stack_targets>

| Stack | Primary files | Additional patterns |
|------|------|------|
| Node | `package.json` | `.version('x.y.z')` in code |
| Rust | `Cargo.toml` (`[package].version`) | `.version('x.y.z')` in code |
| Python | `pyproject.toml`, `setup.py`, `__version__` in `.py` | `.version('x.y.z')` in code |

</stack_targets>

<required>

| Category | Required |
|------|------|
| Input | Parse ARGUMENT as bump rule or explicit semver |
| Discovery | Run `version-find.sh` before applying updates |
| Consistency | Keep all discovered version files synchronized |
| Safety | Use conventional commit message (`chore: bump version to x.y.z`) |
| Git | Keep git write operations sequential |

</required>

<validation>

Execution checklist:

- [ ] Current version identified with `version-current.sh`
- [ ] Target version computed via `version-bump.sh` (or explicit semver validated)
- [ ] `version-apply.sh` updated all intended files
- [ ] `git diff` reviewed
- [ ] Commit created with `scripts/git-commit.sh`
- [ ] Optional push executed only when requested

Forbidden:

- [ ] Starting updates without reading current version
- [ ] Updating only one file when multiple version files exist
- [ ] Force-pushing protected branches

</validation>
