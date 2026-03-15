---
name: jira-cli
version: 0.1.0
description: Interact with Jira Server/Data Center — read issues, create/update issues,
  transition status, link issues, and manage comments via a safe CLI wrapper.
---

# Jira CLI

Use `jira-cli` to interact with a self-hosted Jira Server/Data Center instance via the Jira REST API v2.

## Platform Support

- `scripts/jira-cli` is a launcher script.
- Prebuilt binaries are expected in `scripts/bin/` for:
  - macOS arm64 (`jira-cli-darwin-arm64`)
  - Linux x86_64 (`jira-cli-linux-x86_64`)
- If no compatible binary exists and source + Cargo are available, launcher falls back to `cargo run --release`.

## When To Use

- The user asks to read, search, or inspect Jira issues.
- The user asks to create or update a Jira issue.
- The user asks to transition an issue to a different status.
- The user asks to link two Jira issues.
- The user asks to add or read comments on an issue.
- The user asks to validate Jira config or debug connectivity.

## Setup

Read [Setup Guide](references/SETUP.md).

## Command Contract

Global flags (before subcommand):

- `--project-root <path>` (optional; default cwd)
- `--format <json|text>` (default `json`)
- `--output <path>` (optional output file)

Subcommands:

- `get-issue <KEY>` — fetch a single issue
  - `--fields <comma-separated>` (optional)
- `search` — search with JQL
  - `--jql "<query>"` (required)
  - `--max-results N` (default 50)
  - `--fields <comma-separated>` (optional)
- `create-issue` — create a new issue
  - `--project <KEY>` (required)
  - `--type <Bug|Task|Story|...>` (required)
  - `--title <summary>` (required)
  - `--description <text>` (optional)
  - `--assignee <username>` (optional)
  - `--priority <High|Medium|Low>` (optional)
- `update-issue <KEY>` — update an existing issue
  - `--title`, `--description`, `--assignee`, `--priority` (at least one required)
- `transition <KEY>` — transition issue to a new status
  - `--transition-id <id>` or `--status-name <name>` (exactly one required)
- `list-transitions <KEY>` — list available transitions for an issue
- `link-issue <KEY>` — link two issues
  - `--link-type <name>` (required, e.g. "blocks", "relates to")
  - `--target <KEY>` (required)
- `list-link-types` — list all available issue link type names
- `add-comment <KEY>` — add a comment to an issue
  - `--body "<text>"` (required)
- `list-comments <KEY>` — list all comments on an issue
- `config validate` — test connectivity and print authenticated user

## Output Envelope

All commands return a JSON envelope:

```json
{
  "version": "0.1.0",
  "ok": true,
  "command": "get-issue",
  "data": { ... },
  "meta": { "duration_ms": 42 }
}
```

On error:

```json
{
  "version": "0.1.0",
  "ok": false,
  "command": "get-issue",
  "error": { "code": "JIRA_API_ERROR", "message": "..." }
}
```

## Operational Guardrails

- MUST use `scripts/jira-cli` for all Jira interactions.
- MUST NOT call the Jira API directly (curl, fetch, reqwest, etc.).
- MUST NOT read `.agents/jira-cli/jira.toml` or `.env` files directly.

## Command Patterns

Validate config:

```bash
scripts/jira-cli --project-root /path/to/repo config validate
```

Get an issue:

```bash
scripts/jira-cli --project-root /path/to/repo get-issue PROJ-123
```

Search by JQL:

```bash
scripts/jira-cli --project-root /path/to/repo search --jql "project = PROJ AND status = 'In Progress'" --max-results 10
```

Create an issue:

```bash
scripts/jira-cli --project-root /path/to/repo create-issue --project PROJ --type Bug --title "Login fails on Safari" --description "Steps to reproduce..." --priority High
```

Update an issue:

```bash
scripts/jira-cli --project-root /path/to/repo update-issue PROJ-123 --title "Updated title" --assignee jsmith
```

List and apply a transition:

```bash
scripts/jira-cli --project-root /path/to/repo list-transitions PROJ-123
scripts/jira-cli --project-root /path/to/repo transition PROJ-123 --status-name "In Progress"
```

Link issues:

```bash
scripts/jira-cli --project-root /path/to/repo list-link-types
scripts/jira-cli --project-root /path/to/repo link-issue PROJ-123 --link-type "blocks" --target PROJ-456
```

Add and read comments:

```bash
scripts/jira-cli --project-root /path/to/repo add-comment PROJ-123 --body "Investigating root cause."
scripts/jira-cli --project-root /path/to/repo list-comments PROJ-123
```

## Agent Guidelines

- Default to `--format json` for machine parsing.
- Use `list-transitions` before `transition` when the transition ID is unknown.
- Use `list-link-types` before `link-issue` when the link type name is uncertain.
- Use `config validate` when debugging connectivity issues.
- Pass `--project-root` explicitly to avoid working-directory ambiguity.
