---
name: deepsource
description: >
  Retrieve code review results from DeepSource — issues, vulnerabilities, report cards,
  and analysis runs. Use when asked about code quality, security findings, dependency
  CVEs, coverage metrics, or analysis status.
---

# DeepSource CLI

## Authentication

```bash
deepsource auth login
```

## Goals

### Get code review issues

```bash
deepsource issues --output json
```

Narrow by severity, category, or path:
```bash
deepsource issues --severity critical,major --output json
deepsource issues --category security,bug-risk --output json
deepsource issues --path src/auth --output json
deepsource issues --severity critical --category security --limit 20 --output json
```

Scope to a PR or branch:
```bash
deepsource issues --pr 42 --output json
deepsource issues --default-branch --output json
```

### Get report card

```bash
deepsource report-card --output json
```

Returns grades (A-F) and scores for security, reliability, complexity, hygiene, coverage, and an aggregate.

Scope to a PR or commit:
```bash
deepsource report-card --pr 42 --output json
deepsource report-card --commit abc123 --output json
```

### Get vulnerabilities

```bash
deepsource vulnerabilities --output json
```

Filter by severity:

```bash
deepsource vulnerabilities --severity critical,high --output json
```

Scope to a PR or branch:

```bash
deepsource vulnerabilities --pr 42 --output json
deepsource vulnerabilities --default-branch --output json
```

### Check analysis status

```bash
deepsource repo status --output json
deepsource runs --output json
deepsource runs --commit abc123 --output json
```

`repo status` shows activation and configured analyzers. `runs` shows recent analysis run history.

## Key patterns

- **Auto-detection:** Inside a git repo the CLI auto-detects the repo and current branch. Use `--repo` when outside the repo or targeting a different one. Use scope flags (`--pr`, `--commit`, `--default-branch`) to override the auto-detected branch.
- **Always use `--output json`** for machine-readable output.
- **Repo format:** `--repo provider/owner/name` — providers: `gh`, `gl`, `bb`, `ads`.
- **Scope flags are mutually exclusive:** `--commit`, `--pr`, and `--default-branch` cannot be combined. Omit all three to use auto-detection.

## Documentation

Full CLI docs: https://deepsource.com/docs/developers/cli/installation

Run `deepsource <command> --help` for detailed flag reference.
