---
name: slk-channel
description: "List and manage channels"
metadata:
  version: 0.8.1
  openclaw:
    category: "productivity"
    requires:
      bins:
        - slk
    cliHelp: "slk channel --help"
---

# slk channel

List and manage channels

> **PREREQUISITE:** Read `../slk-shared/SKILL.md` for auth, global flags, security rules, and exit codes. If missing, run `slk generate-skills`.

| Command | Description |
|---------|-------------|
| `slk channel archive` | Archive a channel |
| `slk channel close` | Close a direct/group message channel |
| `slk channel create` | Create a channel |
| `slk channel info` | Show channel details |
| `slk channel invite` | Invite users to a channel |
| `slk channel join` | Join a channel |
| `slk channel kick` | Remove a user from a channel |
| `slk channel leave` | Leave a channel |
| `slk channel list` | List channels |
| `slk channel mark` | Move the read cursor in a channel |
| `slk channel members` | List channel members |
| `slk channel open` | Open or create a direct/group message channel |
| `slk channel purpose` | Set a channel's purpose |
| `slk channel rename` | Rename a channel |
| `slk channel topic` | Set a channel's topic |
| `slk channel unarchive` | Unarchive a channel |

## slk channel archive

Archive a channel

**Slack API:** `conversations.archive`

```bash
slk channel archive [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel ID |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk channel close

Close a direct/group message channel

**Slack API:** `conversations.close`

```bash
slk channel close [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel ID |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk channel create

Create a channel

**Slack API:** `conversations.create`

```bash
slk channel create [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--name` | ✓ | — | channel name |
| `--private` | — | — | create a private channel |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk channel info

Show channel details

**Slack API:** `conversations.info`

```bash
slk channel info [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel ID |

## slk channel invite

Invite users to a channel

**Slack API:** `conversations.invite`

```bash
slk channel invite [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel ID |
| `--users` | ✓ | — | comma-separated user IDs |

**Tips:** Invite users to a channel. Cannot invite a channel's creator or an existing member (Slack returns cant_invite_self / already_in_channel).

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk channel join

Join a channel

**Slack API:** `conversations.join`

```bash
slk channel join [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel ID |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk channel kick

Remove a user from a channel

**Slack API:** `conversations.kick`

```bash
slk channel kick [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel ID |
| `--user` | ✓ | — | user ID to remove |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk channel leave

Leave a channel

**Slack API:** `conversations.leave`

```bash
slk channel leave [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel ID |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk channel list

List channels

**Slack API:** `conversations.list`

```bash
slk channel list [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--cursor` | — | — | initial pagination cursor |
| `--limit` | — | `0` | max channels to return (0 = no client-side cap) |
| `--types` | — | `public_channel,private_channel` | conversations.list types param |

## slk channel mark

Move the read cursor in a channel

**Slack API:** `conversations.mark`

```bash
slk channel mark [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel ID |
| `--ts` | ✓ | — | timestamp to mark as read |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk channel members

List channel members

**Slack API:** `conversations.members`

```bash
slk channel members [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel ID |

## slk channel open

Open or create a direct/group message channel

**Slack API:** `conversations.open`

```bash
slk channel open [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--users` | ✓ | — | comma-separated user IDs |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk channel purpose

Set a channel's purpose

**Slack API:** `conversations.setPurpose`

```bash
slk channel purpose [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel ID |
| `--purpose` | ✓ | — | new purpose |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk channel rename

Rename a channel

**Slack API:** `conversations.rename`

```bash
slk channel rename [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel ID |
| `--name` | ✓ | — | new channel name |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk channel topic

Set a channel's topic

**Slack API:** `conversations.setTopic`

```bash
slk channel topic [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel ID |
| `--topic` | ✓ | — | new topic |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk channel unarchive

Unarchive a channel

**Slack API:** `conversations.unarchive`

```bash
slk channel unarchive [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel ID |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.


