---
name: polylane-cli
description: Drive Polylane from the terminal with the `polylane` CLI — investigate production issues, incidents, and alerts; search logs and query metrics; explore cloud resources, services, and dependency graphs; check what's deployed; search code; save memories; run automations from a catalog; connect observability tools and cloud accounts; and drive threads with the Polylane agent. Use when the work happens in a shell or script, when the user asks for the CLI, or when the Polylane MCP tools are not connected — to debug prod, look up a service or resource, search the codebase, manage integrations, connect a cloud provider, or talk to the Polylane agent. Retrieve (`--help`, `polylane api describe`) — never guess commands or flags.
---

# Polylane CLI — Agent Skill Guide

`polylane` wraps the Polylane platform with agent-friendly commands. Top-level commands map to tasks an agent actually performs; the full API surface is available under `polylane api` as an escape hatch.

This file teaches the contracts and workflows; it deliberately lists no command inventory. **Help is authoritative** — it reflects the installed version:

```bash
polylane --help                                  # resource list
polylane <resource> --help                       # verbs for a resource
polylane <resource> <verb> --help                # flags + examples for one command
```

For anything not a first-class command:

```bash
polylane api list [--tag <Tag>] [--query <q>]    # every operation
polylane api describe <operation-id>             # its shape
polylane api call <operation-id> [--body '{...}' | --body-file path]
```

Concepts, schemas, and limits: <https://docs.polylane.com> (model-readable, no auth; index at `/llms.txt`).

## Prerequisites

```bash
# Install (pick one)
npm install -g @coreplane/polylane
# curl -fsSL https://polylane.com/install.sh | bash        # macOS / Linux
# irm https://polylane.com/install.ps1 | iex               # Windows

# Auth — OAuth is the default; API key where a browser is impossible
polylane auth login                                    # OAuth browser (PKCE)
polylane auth login --no-browser                       # device code (SSH / headless)
polylane auth login --api-key sk_xxxxx                 # scripts / CI
polylane auth signup --email <email> --password <pw>   # new account (emails a 6-digit code)
polylane auth status                                   # verify

# Workspace — set once, then forget
polylane workspace use <workspace-id-or-slug>
polylane workspace create --name "My Workspace"        # new + makes default
```

API keys persist to `~/.polylane/config.json`; OAuth credentials to `~/.polylane/credentials.json` (auto-refresh). For long-lived agent access after signup, create an API key and switch to it. Account lifecycle beyond signup/login lives in the web console.

Config precedence: **flags > env vars (`POLYLANE_API_KEY`, `POLYLANE_WORKSPACE_ID`, `POLYLANE_OUTPUT`, …) > `~/.polylane/config.json` > defaults**. Full variable list: <https://docs.polylane.com/coding-agents/cli/configuration>. Telemetry: `polylane telemetry status` / `disable`, or `DO_NOT_TRACK=1`.

## Agent Flags

Combine for non-interactive (agent / CI) contexts:

| Flag | Purpose |
|---|---|
| `--non-interactive` | Fail fast on missing args instead of prompting |
| `--quiet` | Suppress spinners — stdout stays pure data |
| `--output json` | Force JSON regardless of TTY state |
| `--full` | Disable narrow projection on list commands |
| `--no-wait` / `--stream` | Fire-and-forget / stream tokens on `thread ask` / `continue` |
| `--yes` | Skip destructive-action confirmation prompts |
| `--dry-run` / `--verbose` | Preview the request / log HTTP traffic |
| `--api-key` / `--workspace` / `--timeout` | Per-call overrides |

## Contracts

**stdout is pure data** (JSON, table rows, streamed tokens, URLs — safe to pipe); **stderr** carries progress, hints, and errors. Errors print `Error: <message>` + `Hint: <the exact command that fixes it>`; in JSON mode: `{"error": {"code", "message", "hint"}}` on stderr.

**Exit codes** (stable — branch on `$?`): 0 success · 1 general · 2 usage · 3 auth · 4 rate limit / plan upgrade · 5 timeout · 6 network · 130 interrupted.

**Every API response** carries `_html_url` (console deep link) and `_links` (next-step operations) — rendered as a `Console:` / `Next:` footer on single objects, kept raw in JSON mode.

## Core Workflows

### Investigating an issue

```bash
polylane issue list --active                      # what's currently flagged
polylane issue show <issue-id>                    # full body + linked investigation
polylane feed list --category change --since 24h  # what changed recently
polylane service find "<query>"                   # locate the service
polylane service logs <service-id> --since 1h --grep error
polylane service metrics <service-id> --since 1h
polylane service graph <service-id> --direction both --depth 1
polylane repo grep <owner/repo> "<pattern>"       # correlate with code
polylane issue note <issue-id> "<what you did>"   # record as you go
polylane memory save "<confirmed finding>"        # teach future runs
```

### Onboarding

```bash
polylane integration catalog                      # discover what can connect
polylane integration connect --type <type>        # per-type flags: see --help
polylane cloud connect --provider <provider>      # per-provider flags: see --help
polylane automation catalog && polylane automation from-template <slug>
polylane integration list && polylane cloud list && polylane service list   # verify
```

### Running agent tools directly

The same tools Polylane's own agent uses — telemetry queries across every connected provider, graph traversal, code search — without opening a thread:

```bash
polylane tools search "<capability>" [--full]      # discover (+ JSON schemas)
polylane tools run <name> --params '{...}'
polylane tools code 'async () => { return await tools.findNodes({ query: "api" }); }'
```

Read-only by default; writes need a credential with the `agent_tools:write` scope plus `--write`.

### Talking to the agent

```bash
polylane thread ask "<prompt>" [--context <ids>]   # blocking; ids typed by prefix (repo_, acc_, …)
polylane thread ask "<prompt>" --stream            # tokens to stdout
TID=$(polylane thread ask "<prompt>" --no-wait --output json --quiet | jq -r '.id')
polylane thread continue "$TID" "<follow-up>"
```

### Automations

Load the `polylane-automations` skill for the model and authoring checklist. Quick surface: `automation catalog` / `from-template <slug>` / `create` / `trigger <id>` / `executions <id>`. Schema: `polylane api describe automations.post`.

### Wiring coding agents

`polylane setup [--agent claude|cursor|opencode|codex|…] [--project]` installs this skill and registers the MCP server (`https://mcp.polylane.com/mcp`) in each agent's config. Idempotent.

## Gotchas No Help Text Confesses

- **Browser-flow commands** (`auth login`, `integration connect`, `cloud connect` for OAuth-style providers) exit 0 when the URL is *generated*, not when the install completes upstream — re-query with `list` / `show` to confirm.
- **Partial success still exits 0**: connect-style operations can return `{ accounts: [...], failures: [...] }` — inspect `failures`.
- **`--since` means two things**: a duration string (`1h`, `7d`) on `service logs` / `service metrics` / `feed`, but **unix milliseconds** on `issue list` (as are `--from` / `--to` everywhere).
- **Destructive commands** need `--yes` when non-interactive (else exit 2); a cancelled confirmation exits 0 with `Cancelled` on stderr.
- **`auth signup` is idempotent** for an existing user with a matching password — safe to re-run to renew a session.
- **Streaming** (`--stream`): WebSocket upgrade 401/403 exits 3; other socket failures exit 6.
