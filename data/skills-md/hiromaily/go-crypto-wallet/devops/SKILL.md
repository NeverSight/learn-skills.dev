---
name: devops
description: CI/CD and DevOps workflow. Use when modifying GitHub Actions, Docker configurations, or compose files.
---

# DevOps Workflow

Workflow for CI/CD and infrastructure changes.

## Prerequisites

**Use `git-workflow` Skill** for branch, commit, and PR workflow.

## Applicable Files

| Path | Description |
|------|-------------|
| `.github/workflows/` | GitHub Actions |
| `docker/` | Docker configurations |
| `compose.*.yaml` | Docker Compose files |
| `Dockerfile` | Container definitions |

## GitHub Actions

### Workflow Files

| File | Purpose |
|------|---------|
| `lint-test.yml` | Linting and testing |

### Testing Locally

```bash
# Use act for local testing (if installed)
act -l                    # List workflows
act push                  # Simulate push event
act pull_request          # Simulate PR event
```

### Syntax Validation

```bash
# Check YAML syntax
yamllint .github/workflows/
```

## Docker

### Compose Files

| File | Purpose |
|------|---------|
| `compose.yaml` | Base configuration |
| `compose.btc.yaml` | Bitcoin services |
| `compose.eth.yaml` | Ethereum services |
| `compose.xrp.yaml` | XRP services |
| `compose.bch.yaml` | Bitcoin Cash services |

### Testing

```bash
# Validate compose files
docker compose config

# Test specific compose
docker compose -f compose.yaml -f compose.btc.yaml config
```

## Verification Checklist

- [ ] YAML syntax is valid
- [ ] Workflow triggers are correct
- [ ] Secrets are not exposed
- [ ] Actions use pinned versions
- [ ] Docker images use specific tags

## Commit Format

```
ci: {brief description}

- {change 1}
- {change 2}

Closes #{issue_number}
```

## Related Skills

- `git-workflow` - Branch, commit, PR workflow
