---
name: slk-team
description: "Inspect the workspace"
metadata:
  version: 0.8.1
  openclaw:
    category: "productivity"
    requires:
      bins:
        - slk
    cliHelp: "slk team --help"
---

# slk team

Inspect the workspace

> **PREREQUISITE:** Read `../slk-shared/SKILL.md` for auth, global flags, security rules, and exit codes. If missing, run `slk generate-skills`.

| Command | Description |
|---------|-------------|
| `slk team info` | Show workspace info |
| `slk team profile` | List workspace profile fields |

## slk team info

Show workspace info

**Slack API:** `team.info`

```bash
slk team info [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--team` | — | — | team ID (defaults to the token's workspace) |

## slk team profile

List workspace profile fields

**Slack API:** `team.profile.get`

```bash
slk team profile
```


