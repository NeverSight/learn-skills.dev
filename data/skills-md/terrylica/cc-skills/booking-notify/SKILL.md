---
name: booking-notify
description: Dual-channel booking notifications via Telegram + Pushover. Scheduled sync, webhook relay, emergency alerts with custom sounds. TRIGGERS - booking sync, booking digest, booking notifications, upcoming bookings, calendar sync, booking reminder, pushover, webhook, dune alert.
allowed-tools: Read, Bash, Grep, Glob
---

# Booking Notifications (Dual-Channel)

Automated booking notifications via two channels:

| Channel  | Delivery  | Format     | Use Case                                   |
| -------- | --------- | ---------- | ------------------------------------------ |
| Telegram | Scheduled | HTML       | Interactive commands, daily digest, search |
| Pushover | Real-time | Plain text | Emergency alerts with custom sound (dune)  |

## Mandatory Preflight

### Step 1: Check Sync Script Exists

```bash
ls -la "$HOME/.claude/plugins/marketplaces/cc-skills/plugins/calcom-commander/scripts/sync.ts" 2>/dev/null || echo "SCRIPT_NOT_FOUND"
```

### Step 2: Verify Environment (Required)

```bash
echo "CALCOM_OP_UUID: ${CALCOM_OP_UUID:-NOT_SET}"
echo "TELEGRAM_BOT_TOKEN: ${TELEGRAM_BOT_TOKEN:+SET}"
echo "TELEGRAM_CHAT_ID: ${TELEGRAM_CHAT_ID:-NOT_SET}"
echo "HAIKU_MODEL: ${HAIKU_MODEL:-NOT_SET}"
```

**All must be SET.** If any are NOT_SET, run the setup command first.

### Step 3: Verify Pushover (Optional)

```bash
echo "PUSHOVER_APP_TOKEN: ${PUSHOVER_APP_TOKEN:+SET}"
echo "PUSHOVER_USER_KEY: ${PUSHOVER_USER_KEY:+SET}"
echo "PUSHOVER_SOUND: ${PUSHOVER_SOUND:-dune}"
echo "WEBHOOK_RELAY_URL: ${WEBHOOK_RELAY_URL:-NOT_SET}"
```

**If NOT_SET**: Pushover is optional. Telegram-only operation still works. To enable, see [pushover-setup.md](./references/pushover-setup.md).

### Step 4: Verify Cal.com CLI Binary

```bash
ls -la "$HOME/.claude/plugins/marketplaces/cc-skills/plugins/calcom-commander/scripts/calcom-cli/calcom" 2>/dev/null || echo "BINARY_NOT_FOUND"
```

**If BINARY_NOT_FOUND**: Build it:

```bash
cd "$HOME/.claude/plugins/marketplaces/cc-skills/plugins/calcom-commander/scripts/calcom-cli" && bun install && bun run build
```

## Notification Channels

### Telegram (Scheduled Sync)

6h polling via launchd. Sends HTML-formatted messages for:

| Category     | Examples                                         |
| ------------ | ------------------------------------------------ |
| NEW BOOKING  | New interview scheduled, new consultation booked |
| CANCELLATION | Booking cancelled by attendee, host cancelled    |
| UPCOMING     | Booking starting in 1 hour, today's schedule     |
| RESCHEDULED  | Booking moved to new time, date changed          |

### Pushover (Real-Time Webhook)

Instant notifications via Cloud Run webhook relay:

| Event       | Priority      | Sound | Must Acknowledge? |
| ----------- | ------------- | ----- | ----------------- |
| New booking | 2 (Emergency) | dune  | Yes               |
| Rescheduled | 2 (Emergency) | dune  | Yes               |
| Cancelled   | 0 (Normal)    | dune  | No                |

### Webhook Relay

The webhook relay is a lightweight Cloud Run service that bridges Cal.com webhooks to Pushover. See [webhook-relay.md](./references/webhook-relay.md) for deployment.

## Running Manually

```bash
cd ~/own/amonic && bun run "$HOME/.claude/plugins/marketplaces/cc-skills/plugins/calcom-commander/scripts/sync.ts"
```

## Sync Behavior

1. Fetches bookings from Cal.com API (last 6h window)
2. Compares against last-known state (file-based)
3. Detects new bookings, cancellations, and reschedules
4. Sends Telegram notification (HTML) for each change
5. Sends Pushover notification (plain text) if credentials configured
6. Updates state file for next sync cycle
7. Circuit breaker prevents cascade failures on API errors

## mise Configuration (Agnostic Wiring)

Any repository can adopt these notifications by adding to `.mise.local.toml`:

```toml
[env]
# Required (Telegram)
CALCOM_OP_UUID = "<1password-uuid>"
TELEGRAM_BOT_TOKEN = "<bot-token>"
TELEGRAM_CHAT_ID = "<chat-id>"

# Optional (Pushover dual-channel)
PUSHOVER_APP_TOKEN = "<pushover-app-token>"
PUSHOVER_USER_KEY = "<pushover-user-key>"
PUSHOVER_SOUND = "dune"
WEBHOOK_RELAY_URL = "https://calcom-pushover-webhook-XXXXX.us-central1.run.app/"
```

## References

- [notification-templates.md](./references/notification-templates.md) — Dual-channel message templates
- [pushover-setup.md](./references/pushover-setup.md) — Pushover credential setup guide
- [webhook-relay.md](./references/webhook-relay.md) — Webhook relay deployment + management
- [sync-config.md](./references/sync-config.md) — Sync interval and state management

## Post-Change Checklist

- [ ] YAML frontmatter valid (no colons in description)
- [ ] Trigger keywords current
- [ ] Path patterns use $HOME not hardcoded paths
- [ ] Pushover graceful degradation verified (works without Pushover creds)
