---
name: slk-msg
description: "Read and send messages"
metadata:
  version: 0.8.1
  openclaw:
    category: "productivity"
    requires:
      bins:
        - slk
    cliHelp: "slk msg --help"
---

# slk msg

Read and send messages

> **PREREQUISITE:** Read `../slk-shared/SKILL.md` for auth, global flags, security rules, and exit codes. If missing, run `slk generate-skills`.

| Command | Description |
|---------|-------------|
| `slk msg delete` | delete a message |
| `slk msg draft` | Create a message draft via drafts.create |
| `slk msg ephemeral` | Send an ephemeral message visible only to the target user |
| `slk msg me` | Send a /me message (italicized action text) |
| `slk msg permalink` | Get the permalink for a message |
| `slk msg react` | Add an emoji reaction to a message |
| `slk msg reacted` | List items the user has reacted to |
| `slk msg reactions` | List reactions on a message |
| `slk msg read` | Read messages from a channel or DM |
| `slk msg schedule` | Schedule a message for a future time |
| `slk msg scheduled` | List scheduled messages |
| `slk msg send` | Send a message to a channel or DM |
| `slk msg unreact` | Remove an emoji reaction from a message |
| `slk msg unschedule` | Cancel a scheduled message |
| `slk msg update` | update a message |

## slk msg delete

delete a message

**Slack API:** `chat.delete`

```bash
slk msg delete [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel value |
| `--ts` | ✓ | — | ts value |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk msg draft

Create a message draft via drafts.create

**Slack API:** `drafts.create`

```bash
slk msg draft [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | destination channel or user ID |
| `--text` | — | — | draft message text |
| `--text-file` | — | — | path to text file (use - for stdin) |
| `--thread` | — | — | optional thread_ts for a draft reply |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk msg ephemeral

Send an ephemeral message visible only to the target user

**Slack API:** `chat.postEphemeral`

```bash
slk msg ephemeral [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel ID |
| `--text` | — | — | message text |
| `--text-file` | — | — | path to text file (use - for stdin) |
| `--user` | ✓ | — | user ID of the recipient |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk msg me

Send a /me message (italicized action text)

**Slack API:** `chat.meMessage`

```bash
slk msg me [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel ID |
| `--text` | ✓ | — | action text |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk msg permalink

Get the permalink for a message

**Slack API:** `chat.getPermalink`

```bash
slk msg permalink [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel ID |
| `--ts` | ✓ | — | message timestamp |

## slk msg react

Add an emoji reaction to a message

**Slack API:** `reactions.add`

```bash
slk msg react [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel ID |
| `--emoji` | ✓ | — | emoji name without colons |
| `--ts` | ✓ | — | message timestamp |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk msg reacted

List items the user has reacted to

**Slack API:** `reactions.list`

```bash
slk msg reacted [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--user` | — | — | user ID (defaults to the authed user when empty) |

## slk msg reactions

List reactions on a message

**Slack API:** `reactions.get`

```bash
slk msg reactions [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel ID |
| `--ts` | ✓ | — | message timestamp |

## slk msg read

Read messages from a channel or DM

**Slack API:** `conversations.history`

```bash
slk msg read [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel ID or user ID for a DM |
| `--cursor` | — | — | pagination cursor |
| `--latest` | — | — | end of time range (ts) |
| `--limit` | — | `50` | max messages |
| `--oldest` | — | — | start of time range (ts) |

## slk msg schedule

Schedule a message for a future time

**Slack API:** `chat.scheduleMessage`

```bash
slk msg schedule [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--at` | ✓ | — | Unix timestamp to post at |
| `--channel` | ✓ | — | channel ID |
| `--reply-broadcast` | — | — | also broadcast a threaded reply to the channel (requires --thread) |
| `--text` | — | — | message text |
| `--text-file` | — | — | path to text file (use - for stdin) |
| `--thread` | — | — | optional thread parent ts |

**Tips:** Schedule a message. chat.deleteScheduledMessage may return ok=true for schedules within ~5 minutes of post_at yet the message still posts.

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk msg scheduled

List scheduled messages

**Slack API:** `chat.scheduledMessages.list`

```bash
slk msg scheduled [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | — | — | filter by channel ID (optional) |

## slk msg send

Send a message to a channel or DM

**Slack API:** `chat.postMessage`

```bash
slk msg send [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel ID or user ID |
| `--reply-broadcast` | — | — | also broadcast a threaded reply to the channel (requires --thread) |
| `--text` | — | — | message text |
| `--text-file` | — | — | path to text file (use - for stdin) |
| `--thread` | — | — | reply in this thread ts |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk msg unreact

Remove an emoji reaction from a message

**Slack API:** `reactions.remove`

```bash
slk msg unreact [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel ID |
| `--emoji` | ✓ | — | emoji name without colons |
| `--ts` | ✓ | — | message timestamp |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk msg unschedule

Cancel a scheduled message

**Slack API:** `chat.deleteScheduledMessage`

```bash
slk msg unschedule [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel ID |
| `--id` | ✓ | — | scheduled message ID |

**Tips:** Cancel a scheduled message. chat.deleteScheduledMessage may return ok=true for schedules within ~5 minutes of post_at yet the message still posts.

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk msg update

update a message

**Slack API:** `chat.update`

```bash
slk msg update [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel ID |
| `--text` | — | — | new message text |
| `--text-file` | — | — | path to text file (use - for stdin) |
| `--ts` | ✓ | — | message timestamp |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.


