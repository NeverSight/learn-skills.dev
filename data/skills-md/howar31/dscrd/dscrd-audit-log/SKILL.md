---
name: dscrd-audit-log
description: "Read the server audit log"
metadata:
  version: 0.2.0
  openclaw:
    category: "productivity"
    requires:
      bins:
        - dscrd
    cliHelp: "dscrd audit-log --help"
---

# dscrd audit-log

Read the server audit log

> **PREREQUISITE:** Read `../dscrd-shared/SKILL.md` for auth, global flags, security rules, and exit codes. If missing, run `dscrd generate-skills`.

| Command | Description |
|---------|-------------|
| `dscrd audit-log read` | Read recent audit-log entries |

## dscrd audit-log read

Read recent audit-log entries

**Discord API:** `GET /guilds/{guild.id}/audit-logs`

**Bot permissions:** `VIEW_AUDIT_LOG`

```bash
dscrd audit-log read [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--action` | — | — | filter by numeric action type |
| `--limit` | — | `25` | max entries (1-100) |
| `--user` | — | — | filter by acting user ID |


