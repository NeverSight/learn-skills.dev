---
name: list-integrations
description: List the alert-contact integrations configured on the UptimeRobot account so you can attach them to new or existing monitors.
tags: [integrations, alert-contacts, notifications, list, uptimerobot]
---

# List integrations

> **Preflight — read first.** If you cannot see any `uptimerobot:*` MCP tools in your tool list, invoke the `uptimerobot:setup` skill before doing anything else. Do not tell the user the MCP is misconfigured — `setup`'s Step 0 detects the common case (server connected, tools loaded after session start) and resolves it without re-keying.

Wraps the `list-integrations` MCP tool. Returns every alert-contact integration on the account — the destinations that can be attached to a monitor via `assignedAlertContacts`.

Use this whenever the user says "alert me on Slack", "page on-call", "email the team", etc. — you need the integration's numeric `id` before `create-monitor` or `update-monitor` will accept it.

## Minimal call

```json
{ "limit": 25 }
```

All parameters are optional:

- `limit` — page size (clamped server-side).
- `cursor` — numeric cursor from the previous page's `nextCursor`.

Paginated. Follow the `instructions` field verbatim for the next call.

## Response shape

```json
{
  "integrations": [
    {
      "id": 10,
      "friendlyName": "Ops Slack",
      "type": "Slack",
      "status": "Active",
      "enableNotificationsFor": "UpAndDown",
      "sslExpirationReminder": true,
      "value": "https://hooks.slack.com/services/..."
    }
  ],
  "currentPageCount": 1,
  "totalCount": 1,
  "nextCursor": null,
  "hasMore": false,
  "instructions": "This page contains 1 integrations. Total: 1. No more pages available"
}
```

### Fields

- `id` — numeric. Pass as a **string** to `assignedAlertContacts[].alertContactId` on `create-monitor` / `update-monitor`.
- `friendlyName` — user-defined label. Use this when talking to the user; don't surface the raw `value`.
- `type` — one of `EmailToSms`, `Email`, `Webhook`, `PushBullet`, `Zapier`, `ProSms`, `Pushover`, `Slack`, `MobileAppOld`, `MobileApp`, `Voice`, `Splunk`, `PagerDuty`, `OpsGenie`, `Telegram`, `MSTeams`, `GoogleChat`, `Discord`, `Mattermost`.
- `status` — `NotActivated`, `Paused`, `Active`, `ToMigrate`. Only `Active` integrations will actually deliver alerts.
- `enableNotificationsFor` — `UpAndDown`, `Down`, `Up`, or `None`. If `None`, attaching it to a monitor won't produce alerts.
- `value` — the delivery target (email address, webhook URL, phone number). Treat as sensitive — don't echo it to the user unless they ask.

## Attaching to a monitor

```json
{
  "friendlyName": "Prod API",
  "type": "HTTP",
  "url": "https://api.example.com/health",
  "assignedAlertContacts": [
    { "alertContactId": "10", "threshold": 0, "recurrence": 0 },
    { "alertContactId": "20", "threshold": 5, "recurrence": 30 }
  ]
}
```

- `alertContactId` is a **string** here even though `list-integrations` returns a number.
- `threshold` — minutes of consecutive downtime before this contact fires (`0` = immediate).
- `recurrence` — minutes between repeat notifications while still down (`0` = don't repeat).

## Common mistakes

- Calling `create-monitor` / `update-monitor` with invented `alertContactId`s. Always source them from `list-integrations`.
- Passing `alertContactId` as a number — it must be a string.
- Attaching a `status: NotActivated` or `Paused` integration and expecting alerts. Surface the status to the user first.
- Attaching an integration whose `enableNotificationsFor` is `None` — it silently won't deliver.
- Echoing `value` (webhook URL, email, phone) in chat output. Prefer `friendlyName`.

## Related

- `update-monitor` — attach or swap alert contacts on an existing monitor using the IDs from `list-integrations`.
- `create-*-monitor` — every create skill accepts `assignedAlertContacts`.
- `errors` — `-30003 resource_not_found` when the alert contact doesn't exist.
