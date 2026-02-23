---
name: "gitlab-ci"
description: "GitLab CI/CD pipeline operations. ALWAYS use this skill when user wants to: (1) view pipeline status, (2) run/trigger pipelines, (3) view/retry jobs, (4) trace job logs, (5) download artifacts, (6) lint CI config."
version: "1.0.0"
author: "GitLab-Assistant-Skills"
license: "MIT"
allowed-tools: ["Bash", "Read", "Glob", "Grep"]
---

# CI/CD Pipeline Skill

CI/CD pipeline operations for GitLab using the `glab` CLI.

## Quick Reference

| Operation | Command | Risk |
|-----------|---------|:----:|
| View status | `glab ci status` | - |
| View pipeline | `glab ci view` | - |
| List pipelines | `glab ci list` | - |
| Run pipeline | `glab ci run` | ⚠️ |
| Get pipeline JSON | `glab ci get` | - |
| Retry job | `glab ci retry <job-id>` | ⚠️ |
| Trace job | `glab ci trace <job-id>` | - |
| Download artifacts | `glab ci artifact` | - |
| Lint CI config | `glab ci lint` | - |
| Delete pipeline | `glab ci delete <id>` | ⚠️⚠️ |

**Risk Legend**: - Safe | ⚠️ Caution | ⚠️⚠️ Warning | ⚠️⚠️⚠️ Danger

## When to Use This Skill

**ALWAYS use when:**
- User wants to check pipeline/build status
- User mentions "CI", "CD", "pipeline", "build", "job", "deploy"
- User wants to trigger or retry builds
- User wants to view job logs

**NEVER use when:**
- User wants to manage CI/CD variables (use gitlab-variable instead)
- User wants to manage schedules (use gitlab-schedule skill)

## Available Commands

### View Pipeline Status

```bash
glab ci status [options]
```

**Options:**
| Flag | Description |
|------|-------------|
| `-b, --branch=<branch>` | Check status for specific branch |
| `-l, --live` | Show status in real-time (updates automatically) |
| `-c, --compact` | Show compact view |

**Examples:**
```bash
# View current branch pipeline status
glab ci status

# View status for specific branch
glab ci status --branch=main

# Watch status live (updates in real-time)
glab ci status --live

# Compact view
glab ci status --compact
```

### Interactive Pipeline View

```bash
glab ci view [options]
```

**Options:**
| Flag | Description |
|------|-------------|
| `-b, --branch=<branch>` | View pipeline for specific branch/tag |
| `-p, --pipeline-id=<id>` | View specific pipeline by ID |
| `-w, --web` | Open pipeline in browser |

**Keyboard shortcuts in view mode:**
| Key | Action |
|-----|--------|
| `Esc` or `q` | Close logs or return to pipeline |
| `Ctrl+R` or `Ctrl+P` | Run, retry, or play a job |
| `Tab` / Arrow keys | Navigate |
| `Enter` | Confirm selection |
| `Ctrl+D` | Cancel job / Quit view |

**Examples:**
```bash
# Interactive view for current branch
glab ci view

# View specific branch pipeline
glab ci view --branch=feature/new

# View specific pipeline ID
glab ci view --pipeline-id=12345

# Open in browser
glab ci view --web
```

### List Pipelines

```bash
glab ci list [options]
```

**Options:**
| Flag | Description |
|------|-------------|
| `-b, --branch=<branch>` | Filter by branch |
| `--status=<status>` | Filter by status: running, pending, success, failed, canceled, skipped |
| `--all` | List all pipelines (not just default page) |
| `-P, --per-page=<n>` | Items per page |

**Examples:**
```bash
# List recent pipelines
glab ci list

# List pipelines for branch
glab ci list --branch=main

# List failed pipelines
glab ci list --status=failed

# List all running pipelines
glab ci list --status=running --all
```

### Run/Trigger Pipeline

```bash
glab ci run [options]
```

**Options:**
| Flag | Description |
|------|-------------|
| `-b, --branch=<ref>` | Branch or tag to run pipeline on |
| `--variables=<vars>` | CI variables as key=value pairs (comma-separated) |

**Examples:**
```bash
# Run pipeline for current branch
glab ci run

# Run pipeline for specific branch
glab ci run --branch=main

# Run with CI variables
glab ci run --variables="DEPLOY_ENV=staging,DEBUG=true"

# Run for a tag
glab ci run --branch=v1.2.3
```

### Get Pipeline JSON

```bash
glab ci get [options]
```

Get JSON representation of a pipeline.

**Options:**
| Flag | Description |
|------|-------------|
| `-b, --branch=<branch>` | Get pipeline for specific branch |
| `-p, --pipeline-id=<id>` | Get specific pipeline by ID |

**Examples:**
```bash
# Get current branch pipeline
glab ci get

# Get specific pipeline
glab ci get --pipeline-id=12345

# Pipe to jq for processing
glab ci get | jq '.status'
```

### Retry Job

```bash
glab ci retry <job-id>
```

Retry a failed CI job.

**Examples:**
```bash
# Retry specific job
glab ci retry 456789
```

### Trace Job Logs

```bash
glab ci trace <job-id> [options]
```

View job logs in real-time.

**Examples:**
```bash
# Trace job output
glab ci trace 456789
```

### Download Artifacts

```bash
glab ci artifact [options]
```

Download artifacts from the last pipeline.

**Options:**
| Flag | Description |
|------|-------------|
| `-b, --branch=<branch>` | Download from specific branch |
| `-j, --job=<job-name>` | Download from specific job |
| `-p, --path=<path>` | Download to specific path |

**Examples:**
```bash
# Download all artifacts from last pipeline
glab ci artifact

# Download from specific job
glab ci artifact --job=build

# Download to specific directory
glab ci artifact --path=./artifacts/
```

### Lint CI Configuration

```bash
glab ci lint [file]
```

Validate .gitlab-ci.yml file.

**Examples:**
```bash
# Lint default .gitlab-ci.yml
glab ci lint

# Lint specific file
glab ci lint path/to/.gitlab-ci.yml
```

### Delete Pipeline

```bash
glab ci delete <pipeline-id>
```

**Warning:** This permanently deletes the pipeline and its jobs.

## Common Workflows

### Workflow 1: Check and Fix Failed Pipeline

```bash
# 1. Check current status
glab ci status

# 2. View failed pipeline interactively
glab ci view

# 3. Find failed job and view logs (in interactive view)
# Press arrow keys to select job, Enter to view logs

# 4. Retry the failed job
glab ci retry <job-id>

# 5. Watch the retry
glab ci status --live
```

### Workflow 2: Trigger Deployment

```bash
# 1. Ensure tests pass
glab ci status --branch=main

# 2. Trigger deployment pipeline with variables
glab ci run --branch=main --variables="DEPLOY_ENV=production"

# 3. Monitor deployment
glab ci status --live
```

### Workflow 3: Debug CI Configuration

```bash
# 1. Lint your CI config
glab ci lint

# 2. If valid, run a test pipeline
glab ci run

# 3. Watch the results
glab ci view
```

### Workflow 4: Download Build Artifacts

```bash
# 1. Check pipeline succeeded
glab ci status --branch=release

# 2. Download artifacts from build job
glab ci artifact --branch=release --job=build --path=./dist/
```

## Pipeline Status Reference

| Status | Meaning |
|--------|---------|
| `running` | Pipeline is currently executing |
| `pending` | Pipeline is waiting to run |
| `success` | All jobs passed |
| `failed` | One or more jobs failed |
| `canceled` | Pipeline was manually canceled |
| `skipped` | Pipeline was skipped |
| `manual` | Waiting for manual trigger |
| `scheduled` | Scheduled to run later |

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Authentication failed | Invalid/expired token | Run `glab auth login` |
| Pipeline not found | No pipeline for branch | Check branch name or run `glab ci run` |
| Job stuck pending | No runners available | Check runner configuration |
| Lint fails | Invalid YAML syntax | Fix syntax errors in .gitlab-ci.yml |
| Cannot retry | Job not in retryable state | Wait for current run or cancel first |

## Related Documentation

- [Safeguards](../shared/docs/SAFEGUARDS.md)
- [Quick Reference](../shared/docs/QUICK_REFERENCE.md)
