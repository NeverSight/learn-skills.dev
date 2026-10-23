---
name: dscrd-channel
description: "Manage channels"
metadata:
  version: 0.2.0
  openclaw:
    category: "productivity"
    requires:
      bins:
        - dscrd
    cliHelp: "dscrd channel --help"
---

# dscrd channel

Manage channels

> **PREREQUISITE:** Read `../dscrd-shared/SKILL.md` for auth, global flags, security rules, and exit codes. If missing, run `dscrd generate-skills`.

| Command | Description |
|---------|-------------|
| `dscrd channel create` | Create a channel |
| `dscrd channel delete` | Delete a channel |
| `dscrd channel edit` | Edit a channel's name or topic |
| `dscrd channel info` | Show channel details |
| `dscrd channel list` | List channels in the server |
| `dscrd channel topic` | Set a channel's topic |

## dscrd channel create

Create a channel

**Discord API:** `POST /guilds/{guild.id}/channels`

**Bot permissions:** `MANAGE_CHANNELS`

```bash
dscrd channel create [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--name` | ✓ | — | channel name |
| `--parent` | — | — | parent category ID |
| `--topic` | — | — | channel topic |
| `--type` | — | `text` | channel type: text\|voice\|category\|announcement\|stage\|forum\|media |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## dscrd channel delete

Delete a channel

**Discord API:** `DELETE /channels/{channel.id}`

**Bot permissions:** `MANAGE_CHANNELS`

```bash
dscrd channel delete [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel ID or name |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## dscrd channel edit

Edit a channel's name or topic

**Discord API:** `PATCH /channels/{channel.id}`

**Bot permissions:** `MANAGE_CHANNELS`

```bash
dscrd channel edit [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel ID or name |
| `--name` | — | — | new channel name |
| `--topic` | — | — | new channel topic |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## dscrd channel info

Show channel details

**Discord API:** `GET /channels/{channel.id}`

```bash
dscrd channel info [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel ID or name |

## dscrd channel list

List channels in the server

**Discord API:** `GET /guilds/{guild.id}/channels`

```bash
dscrd channel list
```

## dscrd channel topic

Set a channel's topic

**Discord API:** `PATCH /channels/{channel.id}`

**Bot permissions:** `MANAGE_CHANNELS`

```bash
dscrd channel topic [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel ID or name |
| `--topic` | ✓ | — | new topic |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.


