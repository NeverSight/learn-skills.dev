---
name: polaris-cli
description: >
  Query and manage BlackDuck Coverity static analysis issues via the Polaris CLI.
  Use when the user asks about Coverity issues, code analysis findings, static analysis
  results, Polaris projects/branches, triage status, dismissing findings, or any
  BlackDuck/Polaris-related task. Trigger phrases include "check coverity", "show issues",
  "list projects", "triage issue", "dismiss finding", "polaris", "static analysis",
  "code analysis findings", "coverity issues", "security findings".
---

# Polaris CLI

CLI for querying BlackDuck Coverity on Polaris.

## Setup

First, resolve the absolute path to this skill's directory (the directory containing
this SKILL.md file). Use `POLARIS` as shorthand for `<skill-dir>/scripts/polaris` in
all commands. For example if this SKILL.md is at `~/.agents/skills/polaris-cli/SKILL.md`,
then `POLARIS=~/.agents/skills/polaris-cli/scripts/polaris`.

If the binary is not yet installed (first run), run:
```bash
<skill-dir>/scripts/install.sh
```
This downloads the correct platform binary from GitHub Releases (requires `gh` CLI).

## Output Format

**Always use `--toon` flag** on every command. TOON is a token-efficient format
optimized for LLM context windows. Never use `--format pretty` or omit the flag.

```bash
$POLARIS --toon <command> [options]
```

## Configuration

The base URL can be persisted in `~/.config/polaris/config.toml` so `--base-url` is not
needed on every invocation:

```toml
base_url = "https://visma.cop.blackduck.com"
```

Resolution order: `--base-url` flag > `POLARIS_BASE_URL` env > config file > default.

## Authentication

Before any command will work, an API token must be available. Resolution order:
1. `--api-token` flag
2. `POLARIS_API_TOKEN` environment variable
3. OS keychain (macOS Keychain, Linux Secret Service, Windows Credential Manager)

**First-time setup:** Get an API token from the Polaris web UI (user settings > API tokens),
then store it in the OS keychain so it persists across sessions:
```bash
$POLARIS auth login --token <TOKEN>
```
The token is verified before being stored. If login fails, the token is invalid.

**If auth errors occur**, check the current state:
```bash
$POLARIS auth status --toon
```
This shows which sources have a token and which one is active.

**Remove stored token:**
```bash
$POLARIS auth logout
```

## Commands

### List projects

```bash
$POLARIS projects --toon
$POLARIS projects --toon --name "exact-project-name"
```

### List branches

```bash
$POLARIS branches --toon --project-id <PROJECT_UUID>
```

### List issues

```bash
# Uses main branch automatically when --branch-id omitted
$POLARIS issues --toon --project-id <PROJECT_UUID>
$POLARIS issues --toon --project-id <PROJECT_UUID> --branch-id <BRANCH_UUID>
```

### Show issue detail

```bash
$POLARIS issue --toon --issue-id <ISSUE_UUID> --project-id <PROJECT_UUID>
```

Returns full detail including severity, checker, file path, event summary, and web URL.

### Show event tree

```bash
$POLARIS events --toon --finding-key <FINDING_KEY> --run-id <RUN_ID>
$POLARIS events --toon --finding-key <KEY> --run-id <ID> --max-depth 3
```

Get `finding-key` and `run-id` from issue detail output. Shows full Coverity event tree
with source code context.

### Triage

Get current triage status:
```bash
$POLARIS triage get --toon --project-id <PROJECT_UUID> --issue-key <ISSUE_KEY>
```

Update triage (at least one of `--dismiss`, `--owner`, `--comment` required):
```bash
$POLARIS triage update --toon --project-id <PID> --issue-keys <KEY1>,<KEY2> \
  --dismiss DISMISSED_FALSE_POSITIVE --comment "False positive: checked manually"
```

Dismiss values: `NOT_DISMISSED`, `DISMISSED_FALSE_POSITIVE`, `DISMISSED_INTENTIONAL`, `DISMISSED_OTHER`, `TO_BE_FIXED`.

View triage history:
```bash
$POLARIS triage history --toon --project-id <PROJECT_UUID> --issue-key <ISSUE_KEY> --limit 20
```

### Counts & Metrics

Roll-up counts of issues. Auto-resolves main branch when `--branch-id` is omitted.
The `--group-by` value must be a discovery value (see Discovery below), not a plain name.
```bash
# Total counts (no grouping)
$POLARIS counts --toon --project-id <PROJECT_UUID>
# Grouped by severity (use the value from `discovery --type group-bys`)
$POLARIS counts --toon --project-id <PID> --group-by '[issue][taxonomy][id][011dfe05-00e5-4d8c-8746-a81fe44a120b]'
# With explicit branch
$POLARIS counts --toon --project-id <PID> --branch-id <BID>
```

Issue trends over time. Auto-resolves main branch when `--branch-id` is omitted.
```bash
$POLARIS trends --toon --project-id <PROJECT_UUID>
$POLARIS trends --toon --project-id <PID> --granularity month --start-date 2025-01-01 --end-date 2025-12-31
$POLARIS trends --toon --project-id <PID> --group-by '[issue][status]'
```

Issue age metrics:
```bash
# Auto-resolves main branch when --branch-id is omitted
$POLARIS age --toon --project-id <PROJECT_UUID>
$POLARIS age --toon --project-id <PID> --branch-id <BID> --metric resolved
```

Metric options: `outstanding` (default), `resolved`.

Discovery — query available group-by values and filter keys. **Run this first** to get
valid `--group-by` values for `counts` and `trends` commands.
```bash
$POLARIS discovery --toon --type group-bys
$POLARIS discovery --toon --type filter-keys
```

## Typical Workflow

1. Find the project: `$POLARIS projects --toon --name "my-project"`
2. List issues on main branch: `$POLARIS issues --toon --project-id <PID>`
3. Inspect a specific issue: `$POLARIS issue --toon --issue-id <IID> --project-id <PID>`
4. View full event tree if needed: `$POLARIS events --toon --finding-key <FK> --run-id <RID>`
5. Triage: `$POLARIS triage update --toon --project-id <PID> --issue-keys <IK> --dismiss DISMISSED_FALSE_POSITIVE`

## Global Options

| Flag | Env Var | Default |
|---|---|---|
| `--base-url` | `POLARIS_BASE_URL` | `https://your-instance.polaris.blackduck.com` |
| `--api-token` | `POLARIS_API_TOKEN` | (keychain) |
| `--toon` | - | Use this always |
