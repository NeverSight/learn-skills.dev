---
name: dscrd-automod
description: "Manage auto-moderation rules"
metadata:
  version: 0.2.0
  openclaw:
    category: "productivity"
    requires:
      bins:
        - dscrd
    cliHelp: "dscrd automod --help"
---

# dscrd automod

Manage auto-moderation rules

> **PREREQUISITE:** Read `../dscrd-shared/SKILL.md` for auth, global flags, security rules, and exit codes. If missing, run `dscrd generate-skills`.

| Command | Description |
|---------|-------------|
| `dscrd automod create` | Create a keyword-blocking rule |
| `dscrd automod delete` | Delete an auto-moderation rule |
| `dscrd automod info` | Show one auto-moderation rule (raw JSON) |
| `dscrd automod list` | List auto-moderation rules |

## dscrd automod create

Create a keyword-blocking rule

**Discord API:** `POST /guilds/{guild.id}/auto-moderation/rules`

**Bot permissions:** `MANAGE_GUILD`

```bash
dscrd automod create [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--keyword` | — | `[]` | keyword to block (repeatable, * wildcards allowed) |
| `--name` | ✓ | — | rule name |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## dscrd automod delete

Delete an auto-moderation rule

**Discord API:** `DELETE /guilds/{guild.id}/auto-moderation/rules/{rule.id}`

**Bot permissions:** `MANAGE_GUILD`

```bash
dscrd automod delete [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--id` | ✓ | — | rule ID |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## dscrd automod info

Show one auto-moderation rule (raw JSON)

**Discord API:** `GET /guilds/{guild.id}/auto-moderation/rules/{rule.id}`

**Bot permissions:** `MANAGE_GUILD`

```bash
dscrd automod info [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--id` | ✓ | — | rule ID |

## dscrd automod list

List auto-moderation rules

**Discord API:** `GET /guilds/{guild.id}/auto-moderation/rules`

**Bot permissions:** `MANAGE_GUILD`

```bash
dscrd automod list
```


