---
name: oodle-cli
description: Core Oodle CLI usage — auth, output formats, time flags, file input, and common patterns for all oodle commands.
metadata:
  version: "1.0.0"
  author: oodle-ai
  repository: https://github.com/oodle-ai/agent-skills
  tags: oodle,cli,observability
  globs: ""
  alwaysApply: "false"
---

# Oodle CLI — Core Usage

This skill teaches the agent to invoke the `oodle` CLI safely, with the right flags, time formats, and authentication for any subcommand.

## Prerequisites

Install the CLI before running any other command in this repo:

```bash
# Install via Homebrew (macOS / Linux)
brew install oodle-ai/oodle/oodle

# Or via Go (any platform with Go 1.21+)
go install github.com/oodle-ai/oodle-cli@latest

# Configure auth (interactive — writes ~/.oodle/config.yaml)
oodle configure

# Or set env vars (preferred for CI / containers)
export OODLE_API_KEY=<your-api-key>
export OODLE_INSTANCE=<your-instance-id>
export OODLE_DEPLOYMENT=<your-deployment-url>   # e.g. https://app.oodle.ai
```

Verify the CLI works before issuing any other command:

```bash
oodle version
oodle monitors list -o json | head
```

## Command Execution Order

Before running any oodle command:
1. Check whether the required resource ID or name is already in context.
2. If not, run the discovery command (e.g., `oodle <resource> list -o json`).
3. If the result is ambiguous, ask the user to confirm before proceeding.
4. Run the target command with the resolved ID.
5. Do not run speculative commands (e.g., do not `delete` without first `get`-ing the resource).

## Quick Reference

| Command | Purpose |
|---------|---------|
| `oodle monitors` | Manage metric monitors |
| `oodle dashboards` | Manage dashboards |
| `oodle folders` | Manage dashboard folders |
| `oodle notifiers` | Manage notification channels |
| `oodle notification-policies` | Manage routing of alerts to notifiers |
| `oodle muting-rules` | Silence alerts during maintenance |
| `oodle metrics query` | Run PromQL instant query |
| `oodle metrics query-range` | Run PromQL range query |
| `oodle logs index-patterns` | List available log index patterns |
| `oodle logs query` | Search logs using OpenSearch Query DSL |
| `oodle metrics` | Query metric names, labels, label values |
| `oodle traces` | Search and fetch traces |
| `oodle log-metrics` | Manage log-derived metric rules |
| `oodle synthetic-monitors` | Manage HTTP/TCP synthetic checks |
| `oodle drop-rules` | Manage metric drop / sample rules |
| `oodle api-keys` | Manage API keys |
| `oodle users` | Manage users |
| `oodle configure` | Interactive auth setup |
| `oodle skills` | Install and manage agent skills (this repo) |

## Common Operations

### Output formats

`-o` selects the output format. Default is `table` (human-readable). Use `json` whenever a result is consumed by another tool.

```bash
# ✅ CORRECT — JSON for scripting; jq can parse it
oodle monitors list -o json | jq '.[].id'

# ✅ CORRECT — table for humans skimming a list
oodle monitors list -o table

# ✅ CORRECT — yaml when round-tripping into a `-f` input file
oodle monitors get mon_123 -o yaml > monitor.yaml

# ✅ CORRECT — csv for spreadsheets / quick grep
oodle metrics list --match http_ -o csv

# ❌ WRONG — parsing the default table format with awk/grep is fragile
oodle monitors list | awk '{print $1}'
```

### Non-interactive flags

```bash
# ✅ CORRECT — --force skips destructive-action confirmation in CI
oodle monitors delete mon_123 --force

# ❌ WRONG — running a destructive command without --force in a non-TTY pipeline
oodle monitors delete mon_123
```

### Retries on transient failures

```bash
# ✅ CORRECT — retry transient 5xx / network errors up to 3 times
oodle monitors list -o json --retries 3

# ❌ WRONG — wrapping the command in a custom shell loop instead of using --retries
until oodle monitors list -o json; do sleep 5; done
```

### Time flags

`--from` and `--to` accept three formats:

| Format | Example | Meaning |
|--------|---------|---------|
| Epoch seconds | `1731628800` | absolute unix timestamp |
| `now` | `now` | current server time |
| Relative duration | `-1h`, `-30m`, `-7d` | now minus the duration |

```bash
# ✅ CORRECT — relative duration is timezone-safe and readable
oodle traces list --service api --from -1h --to now -o json

# ✅ CORRECT — epoch when the caller has an exact timestamp
oodle traces list --service api --from 1731628800 --to 1731632400 -o json

# ❌ WRONG — human strings are not parsed
oodle traces list --service api --from "1 hour ago"
```

### File input (`-f`)

`create` and `update` commands accept `-f <file>` and detect JSON or YAML from the file extension or the leading byte.

```bash
# ✅ CORRECT — JSON file
oodle monitors create -f monitor.json

# ✅ CORRECT — YAML file
oodle monitors create -f monitor.yaml

# ✅ CORRECT — round-trip through yaml for in-place edits
oodle monitors get mon_123 -o yaml > monitor.yaml
$EDITOR monitor.yaml
oodle monitors update mon_123 -f monitor.yaml

# ❌ WRONG — passing JSON inline as a flag value (no -f)
oodle monitors create --body '{"name":"x"}'
```

## Best Practices

### Use `-o json` whenever output is consumed by another tool

If the next step in the workflow is a `jq` filter, a script, or another `oodle` command, request JSON. Table output is for humans only.

```bash
# ✅ CORRECT
ID=$(oodle monitors list -o json | jq -r '.[] | select(.name=="High CPU") | .id')

# ❌ WRONG — column positions in table output can change between releases
ID=$(oodle monitors list | grep "High CPU" | awk '{print $1}')
```

### Use `--force` in CI, never in interactive sessions you don't own

`--force` skips the destructive-action confirmation prompt. Always pair it with a prior `get` for safety.

```bash
# ✅ CORRECT — in CI: confirm the resource exists, then delete
oodle monitors get mon_123 -o json > /dev/null && oodle monitors delete mon_123 --force

# ❌ WRONG — blanket --force on a name match without verifying the ID
oodle monitors delete $(oodle monitors list | grep CPU | head -1 | awk '{print $1}') --force
```

### Use environment variables for credentials in CI

Never hardcode the API key or write it into shell history.

```bash
# ✅ CORRECT — credentials come from the CI secret store
export OODLE_API_KEY="$CI_OODLE_API_KEY"
export OODLE_INSTANCE="$CI_OODLE_INSTANCE"
oodle monitors list -o json

# ❌ WRONG — credential in plain text on the command line
OODLE_API_KEY=sk_live_abc123 oodle monitors list -o json
```

### Pin command sequences to discovered IDs

When a workflow modifies a resource, capture the ID once and reuse it.

```bash
# ✅ CORRECT
ID=$(oodle monitors list -o json | jq -r '.[] | select(.name=="High CPU") | .id')
oodle monitors get "$ID" -o json
oodle monitors update "$ID" -f monitor.json

# ❌ WRONG — re-resolving the name on every step (race conditions, extra latency)
oodle monitors get $(oodle monitors list -o json | jq -r '.[] | select(.name=="High CPU") | .id')
oodle monitors update $(oodle monitors list -o json | jq -r '.[] | select(.name=="High CPU") | .id') -f monitor.json
```

## Failure Handling

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Invalid or missing API key | Run `oodle configure` or set `OODLE_API_KEY` |
| 404 Not Found | Resource ID does not exist | Verify with `oodle <resource> list -o json` |
| connection refused | Wrong `OODLE_DEPLOYMENT` URL | Check `OODLE_DEPLOYMENT` env var, ensure no trailing slash, confirm network egress |
| 429 Too Many Requests | Rate limited | Add `--retries 3`, back off 5–10s, batch fewer requests per minute |
| `unknown command` | CLI version too old | Upgrade with `brew upgrade oodle` or `go install ...@latest` |
| `error parsing -f file` | File is not valid JSON/YAML | Validate with `python3 -m json.tool` or `yq .` before retrying |

## References

- [Oodle CLI repo](https://github.com/oodle-ai/oodle-cli)
- [Oodle docs](https://docs.oodle.ai)
