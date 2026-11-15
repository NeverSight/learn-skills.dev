---
name: crontap-status-page-incidents
description: >
  Open, update and resolve incidents on a Crontap status page, schedule
  maintenance windows, and mark the monitors or heartbeats they affect. Use
  when a user wants to tell customers about an outage, post progress updates,
  or announce planned maintenance on their public status page.
license: MIT
metadata:
  version: "1.0.0"
  group: main
  order: 7
  title: Run status page incidents
  summary: Tell customers what is happening during an outage with clear updates, affected components and a resolution, or announce maintenance ahead of time.
  bestFor: Outage communication and planned maintenance notices
  guide: https://crontap.com/status-pages
  guideTitle: Status pages
  tools: get_status_page,list_incidents,create_incident,post_incident_update,resolve_incident,schedule_maintenance
---

# Run status page incidents

A Crontap status page shows monitors and heartbeats as items. Incidents and
maintenance windows are written by people (or their agents) on top of that
automatic history. On a published page every change is public within about a
minute, so write for customers: plain language, no internal hostnames, no
blame.

## Prerequisites

Before using the required tools, check whether they are available. If any are
missing, stop and offer the user exactly two choices:

1. Connect Crontap MCP at `https://mcp.crontap.com/mcp`. MCP access works on
   every Crontap tier.
2. Configure `$CRONTAP_CLIENT_ID` and `$CRONTAP_API_KEY` for the raw API. Raw
   API access requires Ultra.

Do not silently choose a path or continue until the user selects one.

- The account needs a status page. Pages are created and designed in the
  Crontap dashboard; the tools manage incidents on existing pages.
- Confirm the wording with the user before opening an incident on a published
  page. Customers read it.

## Impact and status

- `impact` sets the page state: `none` leaves it alone, `minor` shows it as
  degraded, `major` and `critical` show a major outage.
- `status` moves through `investigating`, `identified`, `monitoring` and
  `resolved`. Post an update with each move so visitors see why.
- Maintenance shows as upcoming before `scheduledStart` and in progress until
  `scheduledEnd` or until it is resolved.

## Workflow

1. Find the page with `list_status_pages`, then read its items with
   `get_status_page`. Each item shows a monitor or heartbeat.
2. Check `list_incidents` so you do not open a duplicate of an open incident.
3. Open the incident with a short title and impact. Name affected items by
   `monitorIds` or `heartbeatIds` (or item ids). Set `startedAt` when the
   outage began earlier, up to 7 days back.
4. Post updates with `post_incident_update` as the situation changes, moving
   `status` in the same call.
5. Resolve with `resolve_incident` and a closing update once the fix holds.
6. For planned work, use `schedule_maintenance` with a start and end.

## MCP examples

Find the page and its items:

```json
{
  "tool": "get_status_page",
  "arguments": { "statusPageId": "<status-page-id>" }
}
```

Check for an incident that is already open:

```json
{
  "tool": "list_incidents",
  "arguments": { "statusPageId": "<status-page-id>", "state": "open" }
}
```

Open an incident for a failing monitor:

```json
{
  "tool": "create_incident",
  "arguments": {
    "statusPageId": "<status-page-id>",
    "title": "Elevated API error rates",
    "impact": "major",
    "bodyMd": "Some API requests fail with 502. We are investigating.",
    "monitorIds": ["<monitor-id>"],
    "startedAt": "2026-11-12T09:14:00Z"
  }
}
```

Post progress and move the status:

```json
{
  "tool": "post_incident_update",
  "arguments": {
    "statusPageId": "<status-page-id>",
    "incidentId": "<incident-id>",
    "bodyMd": "We found the cause and are rolling out a fix.",
    "status": "identified"
  }
}
```

Resolve with a closing note:

```json
{
  "tool": "resolve_incident",
  "arguments": {
    "statusPageId": "<status-page-id>",
    "incidentId": "<incident-id>",
    "bodyMd": "Error rates are back to normal. Sorry for the disruption."
  }
}
```

Announce maintenance:

```json
{
  "tool": "schedule_maintenance",
  "arguments": {
    "statusPageId": "<status-page-id>",
    "title": "Database upgrade",
    "scheduledStart": "2026-11-15T02:00:00Z",
    "scheduledEnd": "2026-11-15T03:00:00Z",
    "bodyMd": "The dashboard may be read-only for a few minutes."
  }
}
```

## REST fallback

Use REST only with Ultra API access:

```bash
curl --fail-with-body \
  "https://api.crontap.com/v1/status-page/<status-page-id>/incident" \
  -X POST \
  -H "ClientId: $CRONTAP_CLIENT_ID" \
  -H "ApiKey: $CRONTAP_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
    "title": "Elevated API error rates",
    "impact": "major",
    "monitorIds": ["<monitor-id>"]
  }'
```

Post updates to `.../incident/<incident-id>/updates` with
`{"bodyMd": "...", "status": "identified"}` and resolve with POST to
`.../incident/<incident-id>/resolve`. Maintenance uses the incident route with
`"isMaintenance": true`, `scheduledStart` and `scheduledEnd`.

## Verification

- Read the result: it says whether the page is published and where it is
  public. On an unpublished page nothing is visible yet.
- Use `get_incident` to confirm the status, affected item ids and timeline.
- Open the public URL a minute later to check the page state matches the
  impact.

## Safety and limits

- Never put credentials, internal URLs or customer data in titles or updates.
- Prefer `resolve_incident` over `delete_incident`. Deleting removes history
  customers may already have seen.
- A page holds 50 open incidents and maintenance windows, an incident holds 50
  updates, and an account can post 60 incidents and updates per hour. Error
  results name the limit and the next step.
- A monitor or heartbeat that is not on the page is rejected; add it to the
  page in the dashboard first.

## Troubleshooting

- `Not on this status page`: call `get_status_page` and use the ids it lists.
- `startedAt must not be in the future`: send a time from the last 7 days.
- The page still shows operational: impact `none` never changes the page
  state, and the public page refreshes within about a minute.

## References

- [Crontap Agent Skills catalogue](https://crontap.com/skills)
- [Crontap status pages](https://crontap.com/status-pages)
- [Crontap MCP](https://crontap.com/mcp)
- [Live REST API reference](https://api.crontap.com/docs/)
