---
name: tgcli
description: >
  Use when user wants to read/search/send/analyze Telegram messages via tgcli CLI.
  Trigger on requests about channel/chat history, digests/news, mentions, files, topics,
  contacts, groups, tags, media downloads, and archive/sync status.
  Also covers group admin (rename, members, invite links, join/leave).
  For edit/delete/reactions/inline buttons, use telegram-mcp instead.
---

# tgcli

Telegram CLI skill for AI agents.

## Install

Install this skill from GitHub:

```bash
npx skills add dapi/tgcli --skill tgcli --agent '*' -g -y
```

Install CLI:

```bash
npm install -g @dapi/tgcli
```

Authenticate once:

```bash
tgcli auth
```

## Tool Boundary: tgcli vs telegram-mcp

| Use tgcli for | Use telegram-mcp for |
|-|-|
| Read/search/archive messages | edit/delete/forward |
| Send text/files and topic posts | reactions |
| | Send photo with preview (image as cover) via `send_file` |
| Forum topics listing/search | inline bot buttons |
| Download media from messages | advanced interactive actions |
| Group admin (rename, members, invite, join/leave) | ban/kick/promote with granular permissions |
| Channel/contact tags and metadata | |
| Sync jobs and archive monitoring | |
| JSON output for automation | |

## Execution Rules

- If `tgcli` is not found, install it: `npm install -g @dapi/tgcli` then run `tgcli auth` for first-time login.
- Always add `--json` for agent workflows.
- Add `--timeout 30s` by default; use `--timeout 90s` for heavy archive fallback reads.
- Prefer explicit `--source archive|live|both` instead of relying on defaults.
- For sending format control:
  - `--parse-mode markdown|html|none` (case-insensitive)
  - for `send file`, `--parse-mode` requires `--caption`
  - `--reply-to <messageId>` replies to a specific message; if both `--reply-to` and `--topic` are passed, `--reply-to` wins
- Never delete lock files (`LOCK`, `database is locked`): wait and retry.

## Core Command Patterns

### Read

```bash
tgcli messages list --chat <id|@username> --limit 50 --source archive --json --timeout 30s
tgcli messages list --chat <id|@username> --chat <id2> --limit 50 --source archive --json --timeout 30s
tgcli messages list --chat <id|@username> --topic <topicId> --after 2025-01-01T00:00:00Z --limit 100 --source archive --json --timeout 30s
tgcli messages show --chat <id|@username> --id <msgId> --source archive --json --timeout 30s
tgcli messages context --chat <id|@username> --id <msgId> --before 5 --after 5 --source archive --json --timeout 30s
```

### Search

```bash
tgcli messages search "Claude Code" --chat <id|@username> --source archive --json --timeout 30s
tgcli messages search --query "Claude Code" --chat <id|@username> --source archive --json --timeout 30s
tgcli messages search --regex "claude\\s+(code|agent)" --chat <id|@username> --source archive --json --timeout 30s
tgcli messages search --tag ai --chat <id|@username> --source archive --json --timeout 30s
tgcli messages search --tags "ai,dev" --chat <id|@username> --source archive --json --timeout 30s
tgcli messages search "release" --chat <id|@username> --after 2025-06-01T00:00:00Z --before 2025-06-30T00:00:00Z --source archive --json --timeout 30s
tgcli messages search "Release" --case-sensitive --chat <id|@username> --source archive --json --timeout 30s
```

Both positional query and `--query` flag work. `--chat` accepts multiple values. Use `--regex` for pattern matching, `--tag`/`--tags` to filter by channel tags, `--after`/`--before` for date range, `--case-sensitive` to disable case-insensitive search.

### Send Text/File

```bash
tgcli send text --to <id|@username> --message "Hello" --json --timeout 30s
tgcli send text --to <id|@username> --topic <topicId> --message "**Hello**" --parse-mode markdown --json --timeout 30s
tgcli send text --to <id|@username> --message "Done" --reply-to <messageId> --json --timeout 30s

tgcli send file --to <id|@username> --file /path/to/file --caption "Report" --json --timeout 30s
tgcli send file --to <id|@username> --file /path/to/file --caption "<b>Report</b>" --parse-mode html --json --timeout 30s
tgcli send file --to <id|@username> --file /path/to/file --filename custom-name.pdf --json --timeout 30s
tgcli send file --to <id|@username> --file /path/to/file --reply-to <messageId> --json --timeout 30s
```

### Post with Cover Image (Photo + Caption)

tgcli `send file` sends images as **documents** (no preview). To post an image as a photo with caption (cover-style), use **telegram-mcp** `send_file`:

Workflow:
1. Download or prepare image locally
2. Send via telegram-mcp:
   - `mcp__telegram-mcp__send_file(chat_id=<id>, file_path="/tmp/image.jpg", caption="Post text")`
3. Caption limit: 1024 characters. For longer posts — send photo first, then follow up with `send text`.

For draft/approval flow:
1. Send to Saved Messages first (use own user ID, not `me`)
2. Review in Telegram
3. If approved — resend to target channel

Note: telegram-mcp `send_file` auto-detects .jpg/.png as photos with preview. tgcli `send file` always sends as document attachment.

### Media Download

```bash
tgcli media download --chat <id|@username> --id <msgId> --json --timeout 30s
tgcli media download --chat <id|@username> --id <msgId> --output /path/to/save --json --timeout 30s
```

### Channels

```bash
tgcli channels list --query "ai" --limit 20 --json --timeout 30s
tgcli channels show --chat <id|@username> --json --timeout 30s
tgcli channels sync --chat <id|@username> --enable --json --timeout 30s
tgcli channels sync --chat <id|@username> --disable --json --timeout 30s
```

### Topics

```bash
tgcli topics list --chat <id|@username> --limit 50 --json --timeout 30s
tgcli topics search --chat <id|@username> --query "release" --limit 20 --json --timeout 30s
```

### Contacts

```bash
tgcli contacts search "alex" --limit 20 --json --timeout 30s
tgcli contacts show --user <id> --json --timeout 30s
tgcli contacts alias set --user <id> --alias "Alex" --json --timeout 30s
tgcli contacts alias rm --user <id> --json --timeout 30s
tgcli contacts tags add --user <id> --tag coworker --tag ai --json --timeout 30s
tgcli contacts tags rm --user <id> --tag ai --json --timeout 30s
tgcli contacts notes set --user <id> --notes "Met at meetup" --json --timeout 30s
```

### Groups

```bash
tgcli groups list --query "dev" --limit 20 --json --timeout 30s
tgcli groups info --chat <id|@username> --json --timeout 30s
tgcli groups rename --chat <id|@username> --name "New Name" --json --timeout 30s
tgcli groups members add --chat <id|@username> --user <userId> --user <userId2> --json --timeout 30s
tgcli groups members remove --chat <id|@username> --user <userId> --json --timeout 30s
tgcli groups invite get --chat <id|@username> --json --timeout 30s
tgcli groups invite revoke --chat <id|@username> --json --timeout 30s
tgcli groups join --code <invite-code> --json --timeout 30s
tgcli groups leave --chat <id|@username> --json --timeout 30s
```

### Tags (Channel Classification)

```bash
tgcli tags list --chat <id|@username> --json --timeout 30s
tgcli tags set --chat <id|@username> --tag ai --tag dev --json --timeout 30s
tgcli tags search --tag ai --limit 20 --json --timeout 30s
tgcli tags auto --limit 50 --json --timeout 90s            # AI-powered: generates tags from channel metadata/content
tgcli tags auto --chat <id|@username> --source manual --json --timeout 90s
tgcli tags auto --limit 50 --no-refresh-metadata --json --timeout 90s
```

### Metadata (Channel Cache)

```bash
tgcli metadata get --chat <id|@username> --json --timeout 30s
tgcli metadata refresh --chat <id|@username> --force --json --timeout 30s
tgcli metadata refresh --only-missing --limit 50 --json --timeout 90s
```

### Sync Jobs

```bash
tgcli sync status --json --timeout 30s
tgcli sync jobs list --json --timeout 30s
tgcli sync jobs list --status error --json --timeout 30s
tgcli sync jobs list --channel <id|@username> --json --timeout 30s
tgcli sync jobs add --chat <id|@username> --depth 500 --json --timeout 30s
tgcli sync jobs add --chat <id|@username> --min-date 2025-01-01T00:00:00Z --json --timeout 30s
tgcli sync jobs retry --all-errors --json --timeout 30s
tgcli sync jobs retry --job-id <id> --json --timeout 30s
tgcli sync jobs retry --channel <id|@username> --json --timeout 30s
tgcli sync jobs cancel --job-id <id> --json --timeout 30s
tgcli sync jobs cancel --channel <id|@username> --json --timeout 30s
```

### Service (Background Sync Daemon)

```bash
tgcli service status --json --timeout 30s
tgcli service install --json --timeout 30s
tgcli service start --json --timeout 30s
tgcli service stop --json --timeout 30s
tgcli service logs --json --timeout 30s
```

### Config & Auth

```bash
tgcli auth --qr --json --timeout 30s
tgcli auth status --json --timeout 30s
tgcli auth logout --json --timeout 30s
tgcli config list --json --timeout 30s
tgcli config get <key> --json --timeout 30s
tgcli config set <key> <value> --json --timeout 30s
tgcli config unset <key> --json --timeout 30s
tgcli doctor --json --timeout 30s
tgcli doctor --connect --json --timeout 30s
```

## Archive + Analysis Workflow

For tasks like "analyze chat history", "what happened this week", "digest/news":

1. Resolve chat:
   - `tgcli channels list --query "<name>" --json --timeout 30s`
   - optionally `tgcli groups list --query "<name>" --json --timeout 30s`
2. Ensure archive flow:
   - `tgcli channels sync --chat <id> --enable`
   - `tgcli sync jobs add --chat <id> --depth 500`
   - `tgcli service status --json --timeout 30s` — check if running
   - `tgcli service install --json --timeout 30s` — if not installed yet
   - `tgcli service start --json --timeout 30s` — start daemon
3. Read archive first:
   - `tgcli messages list --chat <id> --source archive --limit 500 --json --timeout 30s`
4. If archive is still empty, fallback to live:
   - `tgcli messages list --chat <id> --source live --limit 500 --json --timeout 90s`
5. Build digest/synthesis from JSON payload.

## Continuous Sync Workflow

For tasks like "monitor these channels", "keep syncing my subscriptions":

Architecture: `channels sync --enable` marks channels for watching → `sync jobs add` creates backfill tasks → `service start` runs a persistent daemon that processes jobs and pulls realtime updates.

1. Enable sync for each channel:
   - `tgcli channels sync --chat <id|@username> --enable --json --timeout 30s`
   - repeat for each channel to monitor
2. Add backfill jobs (optional, pulls history):
   - `tgcli sync jobs add --chat <id|@username> --depth 1000 --json --timeout 30s`
3. Start the background daemon:
   - `tgcli service install --json --timeout 30s` — first time only
   - `tgcli service start --json --timeout 30s`
4. Verify it's running:
   - `tgcli service status --json --timeout 30s`
   - `tgcli sync status --json --timeout 30s` — shows per-channel sync progress
5. Check for errors:
   - `tgcli sync jobs list --status error --json --timeout 30s`
   - `tgcli sync jobs retry --all-errors --json --timeout 30s`
6. Stop monitoring a channel:
   - `tgcli channels sync --chat <id|@username> --disable --json --timeout 30s`

Alternative without systemd service (one-shot or foreground):
- `tgcli sync --once` — run one sync pass and exit
- `tgcli sync --follow` — keep syncing in foreground (ctrl-c to stop)
- `tgcli sync --follow --idle-exit 5m` — auto-exit after 5 minutes idle

## Sync Semantics

- "My channels/subscriptions" -> `tgcli channels list ...`
- "Monitored/synced channels" -> `tgcli sync status --json --timeout 30s`

## Trigger Examples

### Should trigger

- "read messages in <channel>"
- "search telegram for <query>"
- "send this text/file to telegram"
- "download file from telegram message"
- "summarize what was discussed this week"
- "what's new in <chat>?"
- "show my mentions in <channel>"
- "tag channels by topic"
- "add user to telegram group"
- "get invite link for group"
- "reply to a specific telegram message"
- "start syncing this channel"
- "monitor my telegram channels"
- "прочитай сообщения в канале"
- "найди в телеграме про релиз"
- "отправь сообщение в канал"
- "дай сводку по чату"
- "скачай файл из сообщения"
- "опубликуй пост с картинкой"
- "отправь фото с подписью в канал"
- "post with cover image"

### Should not trigger

- "edit/delete/forward telegram message"
- "react with emoji to message"
- "click inline button in bot"
- "ban/kick/promote user with granular permissions"

Use `telegram-mcp` for those operations.
