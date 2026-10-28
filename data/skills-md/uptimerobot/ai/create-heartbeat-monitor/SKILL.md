---
name: create-heartbeat-monitor
description: Create a HEARTBEAT monitor (cron/job monitor) that expects the target to ping a generated URL on a schedule; alerts when expected pings stop arriving.
tags: [monitoring, heartbeat, cron, job-monitoring, create, uptimerobot]
---

# Create a HEARTBEAT monitor

> **Preflight — read first.** If you cannot see any `uptimerobot:*` MCP tools in your tool list, invoke the `uptimerobot:setup` skill before doing anything else. Do not tell the user the MCP is misconfigured — `setup`'s Step 0 detects the common case (server connected, tools loaded after session start) and resolves it without re-keying.

Use when the user wants to monitor a scheduled job / cron / background worker / backup script. The target system must send periodic HTTP requests to a URL that UptimeRobot generates. If pings stop arriving for longer than the interval (plus optional grace period), the monitor goes down.

This is the **inverse** of the other monitor types: UptimeRobot does not probe anything, it waits for incoming pings.

**Tool:** `create-monitor`
**Required params:** `friendlyName`, `type: "HEARTBEAT"`.
**Do not send `url`.** The server generates it.

## Minimal call

```json
{
  "friendlyName": "Nightly DB backup",
  "type": "HEARTBEAT",
  "interval": 86400,
  "gracePeriod": 1800
}
```

The response includes the generated URL, shaped like:

```
https://heartbeat.uptimerobot.com/m<id>-<hash>
```

Show that URL to the user so they can wire it into their cron / job.

## Common optional params

- `interval` — how often the job is expected to ping (seconds, 30–86400). Required for this monitor to be useful; without it, defaults apply but may not match the user's schedule.
- `gracePeriod` — seconds of tolerance past `interval` before marking down (0–86400). Use this for jobs with variable duration.
- `assignedAlertContacts`, `tagNames`, `maintenanceWindowsIds` — same as other types.

## Example: hourly job with 5-minute grace

```json
{
  "friendlyName": "Hourly cache warmer",
  "type": "HEARTBEAT",
  "interval": 3600,
  "gracePeriod": 300,
  "assignedAlertContacts": [
    { "alertContactId": "10", "threshold": 0, "recurrence": 60 }
  ],
  "tagNames": ["jobs", "backend"]
}
```

## Using the generated URL

The target job must hit the URL to signal "I ran successfully". Shell example:

```bash
curl -fsS --retry 3 "https://heartbeat.uptimerobot.com/m800123456-abcd1234" > /dev/null
```

Trigger on success only — if the job fails, skip the ping and UptimeRobot will raise an incident after `interval + gracePeriod`.

## Common mistakes

- Sending `url` — HEARTBEAT rejects it (`-29001`). The server generates the URL.
- Sending `timeout`, `port`, `httpMethodType`, or any type-specific HTTP/KEYWORD fields — all rejected as forbidden fields.
- Setting `interval` shorter than the job's actual runtime, causing false downtime. Use `gracePeriod` to absorb normal variance.
- Forgetting to show the generated URL to the user. Without it they cannot wire up the job.

## After creation

Call `get-monitor-details` to confirm. The details response exposes the heartbeat URL as well.

## Related

- `create-api-monitor` — if the job also exposes a health endpoint you can probe.
- `manage-monitors` — for pausing during planned maintenance.
