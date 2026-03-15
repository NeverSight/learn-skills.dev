---
name: fathom
description: Use this skill whenever you need to list, filter, search, export, or retrieve transcripts and summaries from Fathom via the official API using the agent-first `fathom` CLI.
---

# Fathom (agent-first CLI)

Use this skill when the task is about Fathom meetings, transcripts, summaries, teams, team members, or official webhooks.

Default stance:

- Prefer the official API-backed CLI, not browser automation.
- Prefer `--json` for machine use.
- Prefer filtering before exporting.
- Use `meetings grep` when you need content search across summaries/transcripts.

## Default workflow

- Sanity check: `fathom doctor --json`
- Browse recent meetings: `fathom meetings list --limit 25 --json`
- Narrow by metadata: `fathom meetings list --team Operations --created-after 2026-03-01 --query "customer discovery" --json`
- Resolve one meeting: `fathom meetings get <recording_id_or_url> --with summary,transcript --json`
- Pull exact transcript or summary: `fathom recordings transcript <recording_id> --json` and `fathom recordings summary <recording_id> --json`

## Common tasks

- Search meeting content: `fathom meetings grep "renewal timeline" --limit 50 --json`
- Export a bundle: `fathom meetings export --all --zip`
- Export a filtered slice: `fathom meetings export --team Operations --created-after 2026-03-01 --format json,md,txt --json`
- Inspect teams: `fathom teams --json`
- Inspect team members: `fathom team-members --team Operations --json`
- Create a webhook: `fathom webhooks create --destination-url https://example.com/fathom-webhook --triggered-for my_recordings --include transcript,summary`

## Auth

If `fathom doctor --json` reports missing auth:

- Best ephemeral path: `FATHOM_API_KEY=... fathom doctor --json`
- Saved local config: `fathom auth set`
- Non-interactive automation: `printf '%s' "$FATHOM_API_KEY" | fathom auth set --stdin`

Avoid pasting full keys into logs or chat.

## Important constraints

- There is no official `whoami` endpoint.
- `meetings get` is a derived helper, because Fathom does not publish a single-meeting fetch endpoint.
- `recordings transcript` and `recordings summary` switch into callback mode when `--destination-url` is supplied.
- Webhook secrets only appear on creation. Capture them immediately if you need signature verification.

## Contract

Stable JSON behavior is documented in `docs/CONTRACT_V1.md`.
