---
name: dscrd-emoji
description: "Inspect custom emoji"
metadata:
  version: 0.2.0
  openclaw:
    category: "productivity"
    requires:
      bins:
        - dscrd
    cliHelp: "dscrd emoji --help"
---

# dscrd emoji

Inspect custom emoji

> **PREREQUISITE:** Read `../dscrd-shared/SKILL.md` for auth, global flags, security rules, and exit codes. If missing, run `dscrd generate-skills`.

| Command | Description |
|---------|-------------|
| `dscrd emoji info` | Show one custom emoji |
| `dscrd emoji list` | List the server's custom emoji |

## dscrd emoji info

Show one custom emoji

**Discord API:** `GET /guilds/{guild.id}/emojis/{emoji.id}`

```bash
dscrd emoji info [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--id` | ✓ | — | emoji ID |

## dscrd emoji list

List the server's custom emoji

**Discord API:** `GET /guilds/{guild.id}/emojis`

```bash
dscrd emoji list
```


