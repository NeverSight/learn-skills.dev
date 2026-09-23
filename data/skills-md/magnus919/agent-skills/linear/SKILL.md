---
name: linear
description: >-
  Manage Linear teams, projects, cycles, issues, comments, workflow state, and documents from a terminal through
  Linear's public GraphQL API. Use when a user asks to list, search, inspect, create, update,
  move, or comment on Linear work, or to find Linear documents. Do not use to embed a live agent
  inside Linear or to build an MCP integration.
license: MIT
compatibility: Requires Python 3.8+; network access and a Linear personal API key or OAuth access token for live API requests.
metadata:
  service: Linear
  api: GraphQL
  graphql-docs: https://linear.app/developers/graphql
  oauth-docs: https://linear.app/developers/oauth-2-0-authentication
  rate-limit-docs: https://linear.app/developers/rate-limiting
  agent-interaction-docs: https://linear.app/developers/agent-interaction
allowed-tools: Bash Read
---

# Linear

Use `scripts/linear` from this skill directory. It is a small, dependency-free wrapper around
Linear's public GraphQL API, not an MCP server. Use command-specific `--help` rather than copying
the full command reference into a response.

## Setup

1. Inspect the available command and relevant noun: `scripts/linear --help` and `scripts/linear issue --help`.
2. For a live request, set exactly one credential in the process environment. Use `LINEAR_API_KEY`
   for a personal key or `LINEAR_ACCESS_TOKEN` for OAuth. Never print, persist, or place either in a command transcript.
3. Begin with bounded discovery. Reads default to `--limit 10`; the maximum is 100.
4. Output is always JSON: compact with `--json`, indented without it. `--dry-run` makes no network request and previews the operation.

## Command Map

| Need | Command |
|---|---|
| Confirm current identity | `scripts/linear whoami --json` |
| Discover teams | `scripts/linear team list --limit 20 --json` |
| List a team's workflow states | `scripts/linear state list --team ENG --json` |
| Narrow a known issue set | `scripts/linear issue list --team ENG --state "In Progress" --json` |
| Find an issue by words | `scripts/linear issue search "customer import" --json` |
| Read one known issue | `scripts/linear issue get ENG-42 --json` |
| Read an issue with its project, cycle, hierarchy, comments, and relations | `scripts/linear issue get ENG-42 --detail --json` |
| Create an issue with project, parent, assignee, labels, state, or due date | `scripts/linear issue create --team ENG --title "Fix login" --project "Platform" --parent ENG-1 --assignee "Ada Lovelace" --label bug --state "In Progress" --due 2026-08-31` |
| Update an issue's assignee, labels, due date, or project | `scripts/linear issue update ENG-42 --assignee "Ada Lovelace" --label bug --remove-label p2 --due 2026-08-31 --project "Platform"` |
| Archive or unarchive an issue | `scripts/linear issue archive ENG-42` or `scripts/linear issue unarchive ENG-42` |
| List or read projects | `scripts/linear project list --team ENG --json` or `scripts/linear project get "Roadmap" --json` |
| Update a project | `scripts/linear project update "Roadmap" --description "Q3 plan" --status started` |
| List or read cycles | `scripts/linear cycle list --team ENG --json` or `scripts/linear cycle get UUID --json` |
| Find documents by words | `scripts/linear document search roadmap --json` |
| Read a document by UUID, slug, or URL | `scripts/linear document get REF --json` |
| Use a documented unsupported GraphQL operation | `scripts/linear raw 'query { viewer { id } }' --json` |

## Choose the Smallest Read

| Situation | Use |
|---|---|
| You know an issue identifier or UUID | `issue get` |
| You have words but not an identifier | `issue search` or `document search` |
| You need a bounded set with filters | `issue list`, `document list`, `project list`, or `cycle list` |
| You need a team's workflow states | `state list --team ENG` |
| The task needs a documented operation outside this focused CLI | `raw` with an explicit GraphQL query |

`raw` is an escape hatch, not a replacement for normal commands. Keep its query narrow and use
the official GraphQL documentation to confirm field names and permissions.

## State Changes

Confirm the target, scope, and rollback path before acting. Read-only discovery may proceed without confirmation.

For `issue create`, `issue update`, `issue move`, `issue comment`, `issue archive`, `issue unarchive`,
`project update`, and raw GraphQL mutations:

1. Identify the issue/team/project/state using a read command.
2. State the exact intended change and recovery path to the user.
3. Run the same command with `--dry-run --json`; this has no credentials or network requirement.
4. After confirmation, rerun it with `--confirm --json`.
5. Report the returned identifier and outcome without exposing credentials.

The `--team` filters for issue, project, and cycle lists require an exact team key. `issue create`
resolves a team key or exact name before creation, resolves issue identifiers before comments,
updates, or archiving, resolves a project by UUID or exact name, an assignee by exact name or
email, labels within the issue's team, and a destination workflow state only within that issue's
team. `project update` resolves the project by UUID or exact name and the status by name or type.
It does not guess IDs, workflow states, labels, or project statuses. Load
`references/domain-and-workflows.md` for safe mutation recipes and Linear workflow semantics.

## Errors And Recovery

- Missing credentials: export one supported environment variable only for the command session, or use `--dry-run` to inspect the request.
- GraphQL error: the CLI writes Linear's first useful error message to stderr and exits nonzero, including when the HTTP status is 200. Check permissions, exact identifiers, and documented field availability.
- Team ambiguity: use `team list` to choose an exact key/name; do not retry by guessing an ID.
- State lookup failure: list the team's states first with `state list --team`, then use that exact name. The error also lists the available states for the issue's team.
- Label lookup failure: the error lists the available labels in the issue's team. Use that exact name.
- Project status lookup failure: the error lists the available statuses. Use an exact name or type (for example `planned`, `started`, `paused`, `completed`, `canceled`).
- Project description rejection: Linear's `projectUpdate` rejects descriptions longer than 255 characters. Keep project descriptions at 255 characters or fewer.
- Limit failure: choose a value from 1 through 100. The CLI deliberately does not paginate automatically.
- Rate limit or transport failure: wait and retry the same bounded read. Follow Linear's [rate limiting guidance](https://linear.app/developers/rate-limiting) rather than adding a retry loop.

## References

| When you need... | Load... |
|---|---|
| Linear's data model, workflow semantics, safe mutation recipes | `references/domain-and-workflows.md` |
| GraphQL endpoint, auth, filters, pagination, errors, rate limits | `references/graphql-contract.md` |
| CLI vs MCP vs raw GraphQL vs Agent Session decision | `references/integration-boundaries.md` |
| Source URLs, access dates, schema verification procedure | `references/sources.md` |

## Verification

Run the offline tests and repository validator after changes:

```bash
python3 -m unittest linear/tests/test_linear.py
ruby scripts/validate-skills.rb
```

## When Not To Use

Use Linear's native MCP or agent-session/webhook API when the task is to embed a live agent inside
Linear rather than operate Linear from a terminal.
