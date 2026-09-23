---
name: forgejo-cli
description: >-
  Use when managing a Forgejo or Gitea server from the terminal: issues, pull requests,
  repositories, file contents, labels, milestones, releases, webhooks, user settings, or
  any /api/v1 endpoint through a safe generic API command. Do not use this skill for
  unrelated requests; route to the nearest named specialist.
license: MIT
compatibility: Python 3.8+; requests is required only for live API calls.
metadata:
  version: 2.0.0
  tags: forgejo, gitea, git, api, code-review
---

# Forgejo CLI v2

Run `python3 scripts/forgejo-cli`. `--agent` (default) uses `FORGEJO_AGENT_TOKEN`; `--user` uses `FORGEJO_USER_TOKEN`; `--server URL` selects an installation. Set `FORGEJO_SERVER` in your shell if your wrapper supplies it, otherwise pass `--server` explicitly.

## Safety

- Mutations require `--force`/`--yes`/`-y`, or `--dry-run`.
- `--dry-run --json` emits one plan with `method`, `path`, `query`, and `body`; it makes no network request.
- `--json` writes exactly one JSON value to stdout; diagnostics go to stderr.
- `--page` and `--limit` work for any list/search request. Add `--include-response` to receive the HTTP status plus `link` and `x-total-count` pagination headers.
- `--help` does not read credentials or contact a server. Path segments are encoded.

## Common workflows

```bash
python3 scripts/forgejo-cli issue list --owner acme --repo app --json
python3 scripts/forgejo-cli --dry-run --json repo create --name demo --private
python3 scripts/forgejo-cli --dry-run --json api --method POST \
  --path /api/v1/repos/acme/app/actions/variables --data '{"name":"KEY","value":"value"}'
```

First-class groups: `issue`, `pr`, `repo`, `content`, `label`, `milestone`, `release`, `hook`, and `user`. `content` expects base64 and update/delete require the current SHA. Use `api` for any other `/api/v1/` endpoint; it supports JSON, raw files, multipart uploads/forms, and custom headers. Consult `/api/swagger` or `/swagger.v1.json` on the selected server. See [command reference](references/command-reference.md).

## Choosing a command

Use a first-class command for its covered daily workflow. Use `api` when the operation is absent, requires version-specific fields, or needs a schema not represented by a simple flag. Before using `api`, read [endpoint routing](references/endpoint-routing.md); read [API usage](references/api-usage.md) for authentication, pagination, compatibility, and safe schema discovery. Read [troubleshooting](references/troubleshooting.md) for 401/403/422 responses and transport failures.
