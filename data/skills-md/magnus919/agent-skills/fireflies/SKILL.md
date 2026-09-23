---
name: fireflies
description: >-
  Query Fireflies.ai meeting transcripts, meeting notes, summaries, contacts, channels,
  AI meeting analytics, AskFred, audio uploads, and webhook signatures through its GraphQL API.
  Use when a user mentions Fireflies, Fireflies.ai, meeting transcripts or notes stored in
  Fireflies, AskFred, or Fireflies webhooks. Do not use for local audio transcription, calendar
  management, or meetings that are not Fireflies data.
license: MIT
compatibility: Requires Python 3.9+, network access for API calls, and FIREFLIES_API_KEY for non-dry-run API requests.
metadata:
  service: fireflies.ai
  api: graphql
allowed-tools: Bash Read
---

# Fireflies.ai

Use `scripts/fireflies` from this skill directory. It uses the Fireflies GraphQL endpoint directly
and emits the API response as JSON. Read-only discovery is safe. Before any state change, confirm
the target, scope, and rollback path; then route the change through the CLI's literal `--confirm`.
`--dry-run` previews a payload only and never authorizes a write.

## First Use

1. Check the command schema: `scripts/fireflies --help` and the relevant subcommand help.
2. Set `FIREFLIES_API_KEY` only for an actual API request. Do not expose or persist it.
3. Start with read-only discovery, such as `scripts/fireflies transcripts list --limit 10 --json`.
4. Use `--dry-run --json` before each mutation to inspect the exact GraphQL payload.

## Command Map

| Need | Command |
|---|---|
| Find transcript metadata | `scripts/fireflies transcripts list --keyword TEXT --limit 10 --json` |
| Read a meeting, summary, sentences, analytics, and recording links | `scripts/fireflies transcripts get ID --json` |
| People, channels, groups, contacts, apps | `users`, `channels`, `groups`, `contacts`, `apps` |
| Meeting analytics or live meetings | `analytics --start DATE --end DATE`, `meetings active` |
| Ask a transcript question | `askfred create --question TEXT --transcript-id ID --confirm` |
| Read one AskFred thread | `askfred get THREAD_ID` |
| Assign an admin/user role | `users set-role --user-id ID --role admin --confirm` |
| Move meetings into a channel | `meetings update-channel --channel-id ID --transcript-ids A,B,C --confirm` |
| Add a live meeting by link | `live add-to --meeting-link URL --confirm` |
| Create a soundbite clip | `live soundbite --meeting-id ID --prompt TEXT --confirm` |
| Two-phase file upload | `audio create-upload ... --confirm` then `audio confirm-upload --meeting-id ID --confirm` |
| Run an exact current/future API operation | `query --document GRAPHQL --variables JSON` |
| Verify a delivered webhook locally | `webhook verify --secret SECRET --signature sha256=... --body FILE` |

## Safe Mutation Workflow

1. Identify the Fireflies object ID and present the intended change.
2. Confirm target, scope, and rollback path with the user. Deletion may not be reversible.
3. Preview the exact document using `--dry-run`; this makes no HTTP request.
4. Run exactly the approved mutation with `--confirm`.
5. Return the response without printing credentials.

Examples:

```bash
scripts/fireflies meetings rename transcript-id --title "Weekly product review" --dry-run --json
scripts/fireflies meetings rename transcript-id --title "Weekly product review" --confirm --json
scripts/fireflies transcripts delete transcript-id --confirm --json
```

## Reference Routing

- Read [references/cli-reference.md](references/cli-reference.md) for syntax, output, exit codes, or generic GraphQL execution.
- Read [references/api-reference.md](references/api-reference.md) for the API model, exact documented operation families, limits, permissions, and source links.
- Read [references/workflows.md](references/workflows.md) for transcript, analytics, upload, AskFred, and generic-operation recipes.
- Read [references/webhook-security.md](references/webhook-security.md) when receiving or implementing Webhooks V2.
- Read [references/troubleshooting.md](references/troubleshooting.md) after an auth, GraphQL, limit, permission, pagination, or webhook failure.
- Read [references/source-index.md](references/source-index.md) when validating source scope or documentation freshness.

## Boundaries

The CLI never starts a webhook server, stores API keys, or guesses undocumented GraphQL fields.
If an ergonomic command does not cover the needed current operation, use `query` or `mutation`
with a documented GraphQL document. The generic mutation command still requires `--confirm`.
