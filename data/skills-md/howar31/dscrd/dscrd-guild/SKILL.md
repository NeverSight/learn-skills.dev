---
name: dscrd-guild
description: "Inspect the servers the bot is in"
metadata:
  version: 0.2.0
  openclaw:
    category: "productivity"
    requires:
      bins:
        - dscrd
    cliHelp: "dscrd guild --help"
---

# dscrd guild

Inspect the servers the bot is in

> **PREREQUISITE:** Read `../dscrd-shared/SKILL.md` for auth, global flags, security rules, and exit codes. If missing, run `dscrd generate-skills`.

| Command | Description |
|---------|-------------|
| `dscrd guild info` | Show server details (member counts, owner, description) |
| `dscrd guild list` | List servers the bot has been invited to |

## dscrd guild info

Show server details (member counts, owner, description)

**Discord API:** `GET /guilds/{guild.id}`

```bash
dscrd guild info
```

## dscrd guild list

List servers the bot has been invited to

**Discord API:** `GET /users/@me/guilds`

```bash
dscrd guild list
```


