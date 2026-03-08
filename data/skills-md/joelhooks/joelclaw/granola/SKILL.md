---
name: granola
displayName: Granola Meeting Intelligence
description: Access and process Granola meeting notes and transcripts via the granola CLI (MCP-backed). Use when pulling meeting data, analyzing transcripts, backfilling meetings, or any task involving Granola meeting content.
version: 0.1.0
author: joel
tags:
  - granola
  - meetings
  - transcripts
  - mcp
---

# Granola Meeting Intelligence

Access Joel's Granola meeting notes via the `granola` CLI, which wraps the Granola MCP server through `mcporter`.

## Setup

- **Binary**: `~/.local/bin/granola`
- **Source**: `~/Code/joelhooks/granola-cli`
- **Config**: `~/.config/granola-cli/mcporter.json`
- **Transport**: MCP via mcporter (NOT direct API, NOT npm package)
- **Auth**: Uses Granola's local credentials automatically

## CLI Commands

### List meetings
```bash
granola meetings [--range this_week|last_week|last_30_days|custom] [--start YYYY-MM-DD] [--end YYYY-MM-DD]
```

### Get meeting details (summary, participants)
```bash
granola meeting <meeting-id>
```

### Get full transcript
```bash
granola meeting <meeting-id> --transcript
```

### Search meetings
```bash
granola search "<query>"
```

### Check auth/connection
```bash
granola --help
```
Returns `"connected": true` if MCP transport is working.

## Output Format

All commands return agent-first JSON with HATEOAS `next_actions`:
```json
{
  "ok": true,
  "command": "granola meetings",
  "result": { ... },
  "next_actions": [
    { "command": "granola meeting <id>", "description": "Get details" }
  ]
}
```

## Important Notes

- **Timestamps are UTC.** Granola returns all dates in UTC. A meeting showing "5:01 PM" on Feb 26 is actually 9:01 AM PST. Always convert when displaying to Joel or writing to Vault files.
- **Codex cannot run Granola.** The MCP transport (mcporter) requires a local socket that Codex sandboxes can't open (`EPERM`). Always pull transcripts from pi/gateway sessions, not codex tasks.

## Known Limitations

- **Rate limiting**: `get_meeting_transcript` endpoint rate-limits aggressively. Don't batch transcript pulls — space them out.
- **Concurrency**: Keep concurrency at 1 for transcript fetches. Original concurrency of 3 overwhelmed the API.
- **Granola app not required locally**: The MCP server handles auth via stored creds, Granola desktop app does NOT need to be running.

## MCP Tools (underlying)

The granola CLI wraps these MCP tools:
1. `query_granola_meetings` — NL search with citations
2. `list_meetings` — by time range
3. `get_meetings` — details by ID array
4. `get_meeting_transcript` — verbatim transcript by ID

## Pipeline Integration

When a new meeting is detected, fire an Inngest event:
```bash
curl -X POST "http://localhost:8288/e/$EVENT_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "meeting/noted",
    "data": {
      "meeting_id": "<id>",
      "title": "<title>",
      "date": "<YYYY-MM-DD>",
      "source": "granola",
      "participants": ["Person A", "Person B"]
    }
  }'
```

Inngest functions that process meetings:
- `check/granola-meetings` — event-triggered check for new meetings
- `granola-check-cron` — hourly cron (`7 * * * *`) polling for new meetings
- `granola-backfill` — bulk backfill all meetings

## Related

- ADR-0055: Granola Meeting Intelligence Pipeline
- Source repo: `~/Code/joelhooks/granola-cli`
- Inngest functions: `packages/system-bus/src/inngest/functions/check-granola.ts`
- Meeting analysis: `packages/system-bus/src/inngest/functions/meeting-analyze.ts`
- Transcript indexing: `packages/system-bus/src/inngest/functions/meeting-transcript-index.ts`
