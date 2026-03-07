---
name: asciinema-streaming-backup
description: Real-time asciinema backup to GitHub orphan branch. TRIGGERS - streaming backup, asciinema backup, session backup, recording backup.
allowed-tools: Read, Bash, Glob, Write, Edit, AskUserQuestion
---

# asciinema-streaming-backup

Complete system for streaming asciinema recordings to GitHub with automatic brotli archival. Uses idle-detection for intelligent chunking, zstd for concatenatable streaming compression, and GitHub Actions for final brotli recompression.

## When to Use This Skill

Use this skill when:

- Setting up real-time backup of asciinema recordings to GitHub
- Configuring idle-detection chunking for recordings
- Creating orphan branch infrastructure for recording storage
- Integrating GitHub Actions for brotli recompression

> **Platform**: macOS, Linux
> **Isolation**: Uses Git orphan branch (separate history, cannot pollute main)

---

## Architecture Overview

```
┌─────────────────┐     zstd chunks      ┌─────────────────┐     Actions      ┌─────────────────┐
│  asciinema rec  │ ──────────────────▶  │  GitHub Orphan  │ ───────────────▶ │  brotli archive │
│  + idle-chunker │   (concatenatable)   │  gh-recordings  │                  │  (300x compress)│
└─────────────────┘                      └─────────────────┘                  └─────────────────┘
         │                                        │
         │ Idle ≥30s triggers chunk               │ Separate history
         ▼                                        │ Cannot PR to main
    ~/asciinema_recordings/                                 ▼
    └── repo-name/                          .github/workflows/
        └── chunks/*.zst                    └── recompress.yml
```

---

## Requirements

| Component         | Required | Installation             | Version       |
| ----------------- | -------- | ------------------------ | ------------- |
| **asciinema CLI** | Yes      | `brew install asciinema` | 3.0+ (Rust)   |
| **zstd**          | Yes      | `brew install zstd`      | Any           |
| **brotli**        | Yes      | `brew install brotli`    | Any           |
| **git**           | Yes      | Pre-installed            | 2.20+         |
| **gh CLI**        | Yes      | `brew install gh`        | Any           |
| **fswatch**       | Optional | `brew install fswatch`   | For real-time |

---

## Workflow Phases

### Phase 0: Preflight Validation

Verify all tools installed, offer self-correction if missing. Run the preflight check script, then AskUserQuestion to offer installation for missing tools.

See [Setup Scripts](./references/setup-scripts.md) for the complete `preflight-check.sh` script.

**Self-Correction**: If tools are missing, generate installation command and offer to run it.

---

### Phase 1: GitHub Account Detection

Detect available GitHub accounts from 5 sources (SSH config, SSH keys, gh CLI, mise env, git config) and let user choose which to use.

See [Account & Repository Detection](./references/account-detection.md) for the detection script, scoring logic, and AskUserQuestion flow.

---

### Phase 1.5: Current Repository Detection

Detect current git repository context (`CURRENT_REPO_OWNER`, `CURRENT_REPO_NAME`, `DETECTED_FROM`) to provide intelligent defaults for Phase 2.

See [Account & Repository Detection](./references/account-detection.md#phase-15-current-repository-detection) for the detection script.

---

### Phase 2: Core Configuration

Gather essential configuration: repository URL (with auto-detection from Phase 1.5), recording directory, and branch name.

See [Configuration Reference](./references/configuration-reference.md#phase-2-core-configuration) for all AskUserQuestion sequences and URL normalization logic.

---

### Phase 3: Advanced Configuration

Allow customization of compression and behavior parameters:

| Parameter      | Default | Range       |
| -------------- | ------- | ----------- |
| Idle threshold | 30s     | 5-300s      |
| zstd level     | 3       | 1-22        |
| Brotli level   | 9       | 1-11        |
| Auto-push      | Yes     | Yes/No      |
| Poll interval  | 5s      | 2s, 5s, 10s |

See [Configuration Reference](./references/configuration-reference.md#phase-3-advanced-configuration) for all AskUserQuestion sequences.

---

### Phase 4: Orphan Branch Setup

Create or configure the orphan branch with GitHub Actions workflow. Checks for existing branch first and offers clone/reset/verify options.

Key actions:

1. Check if branch exists on remote via `git ls-remote`
2. If exists: AskUserQuestion for clone/reset/verify
3. If new: Create orphan branch, add workflow + directory structure, push

See [Setup Scripts](./references/setup-scripts.md#setup-orphan-branchsh) for the complete `setup-orphan-branch.sh` script.
See [GitHub Workflow](./references/github-workflow.md) for the full `recompress.yml` Actions workflow.

---

### Phase 5: Local Environment Setup

Configure local directory and generate customized `idle-chunker.sh` with user parameters embedded from Phase 3.

Key actions:

1. Clone orphan branch to `~/asciinema_recordings/<repo>/`
2. Generate `idle-chunker.sh` with embedded configuration
3. Display configuration summary and usage instructions

See [Setup Scripts](./references/setup-scripts.md) for local setup scripts.
See [Idle Chunker](./references/idle-chunker.md) for the complete chunker implementation.

---

### Phase 6: Autonomous Validation

Claude executes 8 tests autonomously, displaying formatted results. Only 2 tests require user action (recording test, chunker live test).

| Test Category          | Count | Autonomous? |
| ---------------------- | ----- | ----------- |
| Tool preflight         | 5     | Yes         |
| Compression round-trip | 3     | Yes         |
| Repository validation  | 4     | Yes         |
| GitHub Actions trigger | 1     | Yes         |
| Recording test         | 1     | No (USER)   |
| Chunker live test      | 1     | No (USER)   |

See [Autonomous Validation](./references/autonomous-validation.md) for the complete validation script, user-required test flows, and troubleshooting table.

---

## Quick Start

### First-Time Setup

```bash
/usr/bin/env bash << 'PREFLIGHT_EOF'
# 1. Check requirements
for tool in asciinema zstd brotli git gh; do
  command -v "$tool" &>/dev/null && echo "$tool: OK" || echo "$tool: MISSING"
done

# 2. Create orphan branch (replace with your repo)
REPO="git@github.com:YOUR/REPO.git"
./setup-orphan-branch.sh "$REPO"

# 3. Validate setup
./validate-setup.sh "$HOME/asciinema_recordings/REPO"
PREFLIGHT_EOF
```

### Recording Session

```bash
/usr/bin/env bash << 'SKILL_SCRIPT_EOF'
# Terminal 1: Start recording
WORKSPACE=$(basename "$PWD")
asciinema rec $PWD/tmp/${WORKSPACE}_$(date +%Y-%m-%d_%H-%M).cast

# Terminal 2: Start idle-chunker
~/asciinema_recordings/REPO/idle-chunker.sh $PWD/tmp/${WORKSPACE}_*.cast
SKILL_SCRIPT_EOF
```

---

## Key Design Decisions

| Decision                | Rationale                                          |
| ----------------------- | -------------------------------------------------- |
| **zstd for streaming**  | Supports frame concatenation (brotli doesn't)      |
| **brotli for archival** | Best compression ratio (~300x for .cast files)     |
| **Orphan branch**       | Complete isolation, can't pollute main history     |
| **Idle-based chunking** | Semantic breakpoints, not mid-output splits        |
| **Shallow clone**       | Minimal disk usage, can't accidentally access main |
| **30s idle threshold**  | Balances chunk frequency vs semantic completeness  |

---

## Troubleshooting

See [Troubleshooting Guide](./references/troubleshooting.md) for common issues and fixes.

---

## Post-Change Checklist

After modifying this skill:

1. [ ] Orphan branch creation scripts use heredoc wrapper
2. [ ] All bash blocks compatible with zsh (no declare -A, no grep -P)
3. [ ] GitHub Actions workflow validates brotli recompression
4. [ ] Idle chunker handles both macOS and Linux stat syntax
5. [ ] Detection flow outputs parseable key=value format
6. [ ] References validate links to external documentation

---

## Reference Documentation

- [Account & Repository Detection](./references/account-detection.md) - GitHub account detection + repo context
- [Configuration Reference](./references/configuration-reference.md) - AskUserQuestion sequences + task templates
- [Idle Chunker Script](./references/idle-chunker.md) - Complete chunker implementation
- [GitHub Workflow](./references/github-workflow.md) - Full Actions workflow
- [Setup Scripts](./references/setup-scripts.md) - All setup and validation scripts
- [Autonomous Validation](./references/autonomous-validation.md) - Validation script and user-required tests
- [Troubleshooting Guide](./references/troubleshooting.md) - Common issues and fixes
- [asciinema 3.0 Docs](https://docs.asciinema.org/)
- [zstd Frame Format](https://github.com/facebook/zstd)
- [Git Orphan Branches](https://graphite.dev/guides/git-orphan-branches)
