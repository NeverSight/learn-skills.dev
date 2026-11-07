---
name: dscrd-event
description: "Manage scheduled events"
metadata:
  version: 0.2.0
  openclaw:
    category: "productivity"
    requires:
      bins:
        - dscrd
    cliHelp: "dscrd event --help"
---

# dscrd event

Manage scheduled events

> **PREREQUISITE:** Read `../dscrd-shared/SKILL.md` for auth, global flags, security rules, and exit codes. If missing, run `dscrd generate-skills`.

| Command | Description |
|---------|-------------|
| `dscrd event create` | Create a scheduled event (external with --location, or voice with --channel) |
| `dscrd event delete` | Delete a scheduled event |
| `dscrd event edit` | Edit a scheduled event |
| `dscrd event list` | List scheduled events |

## dscrd event create

Create a scheduled event (external with --location, or voice with --channel)

**Discord API:** `POST /guilds/{guild.id}/scheduled-events`

**Bot permissions:** `MANAGE_EVENTS`

```bash
dscrd event create [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | — | — | voice channel ID |
| `--description` | — | — | event description |
| `--end` | — | — | end time (ISO8601; required for --location events) |
| `--location` | — | — | external location text |
| `--name` | ✓ | — | event name |
| `--start` | ✓ | — | start time (ISO8601, e.g. 2026-08-01T19:00:00+08:00) |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## dscrd event delete

Delete a scheduled event

**Discord API:** `DELETE /guilds/{guild.id}/scheduled-events/{event.id}`

**Bot permissions:** `MANAGE_EVENTS`

```bash
dscrd event delete [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--id` | ✓ | — | event ID |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## dscrd event edit

Edit a scheduled event

**Discord API:** `PATCH /guilds/{guild.id}/scheduled-events/{event.id}`

**Bot permissions:** `MANAGE_EVENTS`

```bash
dscrd event edit [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--description` | — | — | new description |
| `--id` | ✓ | — | event ID |
| `--name` | — | — | new name |
| `--start` | — | — | new start time (ISO8601) |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## dscrd event list

List scheduled events

**Discord API:** `GET /guilds/{guild.id}/scheduled-events`

```bash
dscrd event list
```


