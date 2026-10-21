---
name: monitor
description: Create and manage recurring Exa searches or Firecrawl page, crawl, and web-search monitors through ArkSpace. Use when the user wants scheduled change checks, webhook delivery, a monitor paused or resumed, an immediate check triggered, history inspected, or a persistent monitor deleted.
compatibility: Requires a local filesystem-based host with shell and network access, Node.js 20+, the arks CLI, and Exa or Firecrawl credentials; intended for Claude Code and Codex CLI on macOS, Linux, and Windows.
---

# Monitor

Use the installed `arks` CLI or ArkSpace MCP tools. Use `web.search` for one-time discovery and `research.run` for one attached report.

## Choose the contract

Do not present Firecrawl Monitor as an interchangeable Exa Provider:

- Use `monitor.*` for Exa recurring search results. Its contract is a query, result count, interval, webhook, run history, and one-time signing secret.
- Use `monitor.site.*` for Firecrawl page, crawl, or web-search change checks. Its contract includes typed targets, a cron or natural-language schedule, retention, optional goal-based judging, page-level diffs, Firecrawl credit estimates, and optional webhook events.

Ask one focused question if the intended contract is unclear.

## Readiness and ownership

1. Run `arks --version`. If unavailable, explain that ArkSpace CLI is required and ask before changing the user's environment.
2. Run `arks doctor --json` when Provider readiness is unknown. If credentials are missing, direct the human to run `arks setup` in a trusted local terminal. Never ask for an API key in conversation or place one in a command argument.
3. Ask before changing configuration or the user's environment. Use only ArkSpace-owned monitor IDs; every resource is bound to the anonymous key ID that created it.

## Create an Exa recurring search

Before creation, present the monitor name, exact query, result count, cadence, public HTTPS webhook, new secret-file path, and continuing charges. Obtain explicit approval, then call `monitor.create` with `confirmed: true`.

The secret path must not already exist. ArkSpace creates it with restrictive permissions and never returns the secret. Configure the receiver to verify `Exa-Signature`. Do not copy the secret into chat.

## Create a Firecrawl site monitor

Before creation, present:

- the exact `scrape`, `crawl`, or `search` targets;
- the five-field cron or natural-language schedule and IANA timezone;
- retention from 1–365 days;
- the judging goal and whether judging is enabled;
- the public HTTPS webhook and selected `monitor.page` or `monitor.check.completed` events, if any;
- Firecrawl's estimate when available, and that each check bills underlying scrape, crawl, search, and optional judging work.

Obtain explicit approval, then call `monitor.site.create` with `confirmed: true`. Search targets require a non-empty goal unless judging is explicitly disabled. ArkSpace bounds targets and outputs, forces fresh monitored fetches, and does not expose arbitrary scrape code, webhook headers, or secret values.

For the CLI, place create fields in a JSON object and run:

```bash
arks monitor site create --input ./site-monitor.json --confirm --json
```

## Operate

Exa operations:

- `monitor.list`, `monitor.status`, `monitor.runs`, `monitor.run.get`
- confirmed mutations: `monitor.update`, `monitor.pause`, `monitor.resume`, `monitor.trigger`, `monitor.delete`

Firecrawl operations:

- `monitor.site.list`, `monitor.site.status`, `monitor.site.checks`, `monitor.site.check.get`
- confirmed mutations: `monitor.site.update`, `monitor.site.pause`, `monitor.site.resume`, `monitor.site.trigger`, `monitor.site.delete`

State the exact resource ID and effect before every mutation. Pausing retains configuration and history. Resuming restores scheduled work. Triggering queues paid work immediately. Deletion is irreversible at the Provider resource level.

## Failure and deletion

ArkSpace never rotates credentials or Providers for an owned monitor. Restore a missing owning environment-variable credential rather than creating a duplicate.

If create reports `acceptance-unknown`, check the correct Provider dashboard before retrying. If a mutation reports `safeToRetry: false`, refresh status or history before acting again. A successful delete confirms removal of the API resource only; do not claim physical erasure of retained artifacts, delivery records, logs, or backups.

Report the monitor ID, Provider, target or query, schedule, current state, and mutation outcome. Summarize run or check history instead of pasting raw Provider payloads, while preserving warnings and uncertain effects.
