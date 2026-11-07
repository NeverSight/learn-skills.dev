---
name: dscrd-dm
description: "Direct messages (sent as the bot; requires a mutual server)"
metadata:
  version: 0.2.0
  openclaw:
    category: "productivity"
    requires:
      bins:
        - dscrd
    cliHelp: "dscrd dm --help"
---

# dscrd dm

Direct messages (sent as the bot; requires a mutual server)

> **PREREQUISITE:** Read `../dscrd-shared/SKILL.md` for auth, global flags, security rules, and exit codes. If missing, run `dscrd generate-skills`.

| Command | Description |
|---------|-------------|
| `dscrd dm read` | Read the bot's DM history with a user |
| `dscrd dm send` | Send a DM to a user (as the bot) |

## dscrd dm read

Read the bot's DM history with a user

**Discord API:** `POST /users/@me/channels + GET /channels/{dm.id}/messages`

```bash
dscrd dm read [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--limit` | — | `5` | max messages |
| `--user` | ✓ | — | user ID |

## dscrd dm send

Send a DM to a user (as the bot)

**Discord API:** `POST /users/@me/channels + POST /channels/{dm.id}/messages`

```bash
dscrd dm send [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--text` | — | — | message text |
| `--text-file` | — | — | path to text file (use - for stdin) |
| `--user` | ✓ | — | recipient user ID |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.


