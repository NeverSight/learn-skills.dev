---
name: email-imap-fetch
description: Listen for one or more IMAP inboxes with the IDLE command, fetch unread email metadata plus text previews, and forward each message to OpenClaw webhooks. Use when tasks need near-real-time mailbox monitoring, multi-account inbox ingestion via environment variables, and automatic trigger delivery into OpenClaw automation.
---

# Email IMAP Fetch

## Core Goal
- Wait for new mail with IMAP IDLE.
- Fetch unread messages after each wake-up.
- Support multiple mailbox accounts configured with env.
- Control IDLE support strictly with env mode (`idle` or `poll`) without runtime probing.
- Forward each fetched email to OpenClaw webhooks.
- Emit machine-readable JSON lines for downstream steps.

## Workflow
1. Configure account env variables and OpenClaw webhook env variables (see `references/env.md` and `assets/config.example.env`).
2. Validate configuration:

```bash
python3 scripts/imap_idle_fetch.py check-config
```

3. Run one IDLE cycle per account (smoke test):

```bash
python3 scripts/imap_idle_fetch.py listen --cycles 1 --idle-seconds 120 --max-messages 10
```

4. Run continuously (default resident mode):

```bash
python3 scripts/imap_idle_fetch.py listen
```

## Runtime Model
- Skill files are installed locally, but the listener is not auto-started.
- In `idle` mode, IMAP IDLE receives push events only while listener process and IMAP connection are alive.
- In `poll` mode, listener sleeps for poll interval and then fetches unread messages.
- If the process exits, push events are missed; next run can still fetch existing unread emails with `UNSEEN`.
- Default runtime is resident mode (`IMAP_CYCLES=0` by default).
- Default IDLE mode is `poll` (safe for servers without IDLE support).
- In production, always-on deployment must run under `systemd`, `launchd`, `supervisor`, or an equivalent daemon manager.
- Do not run the listener as a foreground process bound to an interactive exec session; once that session exits, the listener will stop.

## Output Contract
- Output format is JSONL (one JSON object per line).
- `type=status` for lifecycle events.
- `type=message` for fetched emails with:
  - `account`, `mailbox`, `seq`, `uid`
  - `subject`, `from`, `to`, `date`, `message_id`
  - `snippet` (plain-text preview)
- `wait_mode` is `idle` or `poll` in cycle status output.
- `wait_events` records the active wait strategy details.
- `event=webhook_delivered` status events when OpenClaw webhook POST succeeds.
- `type=error` for account-level failures.
- `event=webhook_failed` error events when OpenClaw webhook POST fails.

## Parameters
- `--cycles`: IDLE cycles per account (`0` means forever).
- `--idle-seconds`: max wait time for each IDLE call.
- `--poll-seconds`: interval used when polling mode is active.
- `--idle-mode`: `idle` or `poll`.
- `--max-messages`: max unread emails fetched each cycle.
- `--mark-seen` / `--no-mark-seen`: control unread state updates.
- `--snippet-chars`: preview length limit.
- `--connect-timeout`: connection timeout seconds.
- `--retry-seconds`: retry delay after failure.

Environment defaults:
- `IMAP_CYCLES`
- `IMAP_IDLE_MODE`
- `IMAP_IDLE_SECONDS`
- `IMAP_POLL_SECONDS`
- `IMAP_MAX_MESSAGES`
- `IMAP_MARK_SEEN`
- `IMAP_SNIPPET_CHARS`
- `IMAP_CONNECT_TIMEOUT`
- `IMAP_RETRY_SECONDS`

OpenClaw webhooks forwarding:
- `OPENCLAW_WEBHOOKS_ENABLED`
- `OPENCLAW_WEBHOOKS_TOKEN`
- `OPENCLAW_WEBHOOKS_BASE_URL`
- `OPENCLAW_WEBHOOKS_MODE` (`agent` or `wake`)
- `OPENCLAW_WEBHOOKS_ENDPOINT` (optional endpoint override)
- `OPENCLAW_WEBHOOKS_PATH`
- `OPENCLAW_WEBHOOKS_WAKE_MODE`
- `OPENCLAW_WEBHOOKS_DELIVER`
- `OPENCLAW_WEBHOOKS_TIMEOUT`
- `OPENCLAW_WEBHOOKS_NAME`
- `OPENCLAW_WEBHOOKS_AGENT_ID`
- `OPENCLAW_WEBHOOKS_CHANNEL`
- `OPENCLAW_WEBHOOKS_TO`
- `OPENCLAW_WEBHOOKS_MODEL`
- `OPENCLAW_WEBHOOKS_THINKING`
- `OPENCLAW_WEBHOOKS_AGENT_TIMEOUT_SECONDS`
- `OPENCLAW_WEBHOOKS_SESSION_KEY_PREFIX`

## Error Handling
- Invalid env configuration exits with code `2`.
- In `idle` mode, unsupported IDLE returns explicit error and suggests `IMAP_IDLE_MODE=poll`.
- Runtime failures are emitted as `type=error`.
- Command exits non-zero when account processing errors occur.

## References
- `references/env.md`

## Assets
- `assets/config.example.env`

## Scripts
- `scripts/imap_idle_fetch.py`
