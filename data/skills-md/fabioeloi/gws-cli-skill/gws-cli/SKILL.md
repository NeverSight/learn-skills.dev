---
name: gws-cli
description: Use the Google Workspace CLI to inspect schemas, authenticate safely, and run Google Workspace API commands. Use when the user wants to work with Drive, Gmail, Sheets, Docs, Calendar, Chat, Tasks, or other Google Workspace APIs through the gws command.
license: MIT
compatibility: Requires the gws binary on PATH, network access to Google APIs, and an authenticated Google Workspace or Google Cloud context.
metadata:
  author: fabioeloi
  upstream: https://github.com/googleworkspace/cli
  distribution: https://skills.sh
---

# gws-cli

Use this skill when the task should be executed through the Google Workspace CLI instead of handwritten HTTP requests or ad hoc API wrappers.

## When to use this skill

- The user asks to interact with Google Drive, Gmail, Sheets, Docs, Slides, Calendar, Chat, Tasks, People, Meet, or Workspace Admin APIs.
- The user wants structured JSON output that is easy for an agent to inspect.
- The user needs to inspect Google API schemas before building a request.
- The user wants a repeatable CLI workflow that can run locally, in CI, or in a headless environment.

## Required operating model

1. Confirm that `gws` is installed and available on `PATH`.
2. Check authentication status before making API calls.
3. Inspect the target method with `gws schema` or `gws <service> --help` before composing flags.
4. Prefer read-only commands first.
5. For write, update, or delete operations, confirm intent with the user before execution.
6. Prefer `--dry-run` when the command supports local validation and the operation is risky.

## Quick start

```bash
# Install the CLI
npm install -g @googleworkspace/cli

# Check the binary and auth status
bash scripts/check-prereqs.sh

# Inspect command space
gws drive --help
gws schema drive.files.list

# Run a read-only command
gws drive files list --params '{"pageSize": 10}' --format json
```

## Authentication workflow

Choose the lightest auth flow that satisfies the task.

### Local interactive

```bash
gws auth setup
gws auth login
```

### Service account

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json
gws auth status
```

### CI or headless flows

- Prefer exported credentials or service-account based execution.
- Never echo secrets back to the user.
- If credentials are missing, stop and ask for the appropriate auth setup instead of guessing.

More detail is in [references/REFERENCE.md](references/REFERENCE.md).

## Command discovery workflow

Always inspect before executing.

```bash
# Browse resources and helper commands for a service
gws sheets --help

# Inspect a specific method schema
gws schema sheets.spreadsheets.values.get
```

Use schema output to determine:

- required `--params` values
- whether a request body is needed via `--json`
- whether pagination or file upload flags apply
- which field names and types the API expects

## Command patterns

### Read-only list or get

```bash
gws drive files list --params '{"pageSize": 10}' --format json
gws gmail users messages get --params '{"userId": "me", "id": "MESSAGE_ID"}' --format json
```

### Create or update with explicit confirmation

```bash
gws sheets spreadsheets create --json '{"properties": {"title": "Q1 Budget"}}' --format json
gws docs documents batchUpdate --params '{"documentId": "DOC_ID"}' --json '{"requests": [...]}' --format json
```

### Schema-driven request building

```bash
gws schema calendar.events.insert
gws calendar events insert --params '{"calendarId": "primary"}' --json '{"summary": "Standup", "start": {"dateTime": "2026-03-07T09:00:00Z"}, "end": {"dateTime": "2026-03-07T09:15:00Z"}}'
```

### Pagination

```bash
gws drive files list --params '{"pageSize": 100}' --page-all
```

### File upload or download

```bash
gws drive files create --json '{"name": "report.pdf"}' --upload ./report.pdf
gws drive files get --params '{"fileId": "FILE_ID", "alt": "media"}' --output ./download.bin
```

## Safety rules

- Treat `create`, `insert`, `update`, `patch`, `delete`, and helper commands that change state as write operations.
- Confirm the target resource, identity, and scope before executing a write operation.
- Never print tokens, OAuth client secrets, or service account JSON contents.
- Prefer `--format json` unless the user explicitly wants a human-oriented table.
- Use `--page-all` intentionally because it changes output shape to NDJSON.
- If the upstream API or CLI help is ambiguous, inspect the schema again instead of guessing flag names.

## Available support files

- [references/REFERENCE.md](references/REFERENCE.md) for installation, auth, and common command templates
- `scripts/check-prereqs.sh` for local environment checks

## Troubleshooting

- If `gws` is missing, install it from npm or a GitHub release, confirm it is on `PATH`, and rerun `bash scripts/check-prereqs.sh`.
- If `gws auth status` shows no credentials, run `gws auth setup` and `gws auth login`, or export `GOOGLE_APPLICATION_CREDENTIALS` for a service-account flow.
- If `gws auth login` fails due to OAuth client restrictions, prefer the upstream manual OAuth flow or a service account where appropriate.
- If a request returns `403 Forbidden` or insufficient permissions, confirm the active identity, API enablement, scopes, and resource sharing before retrying.
- If a method is unknown, confirm the service alias with `gws <service> --help` before assuming the REST method name maps directly.
- If a request fails schema validation, rerun `gws schema <service.resource.method>` and compare every required field name with the command you built.
- If `--page-all` changes the output shape unexpectedly, remember that pagination output becomes NDJSON and should be parsed line by line.
