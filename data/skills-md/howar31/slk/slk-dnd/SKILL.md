---
name: slk-dnd
description: "Do-Not-Disturb status and snooze"
metadata:
  version: 0.8.1
  openclaw:
    category: "productivity"
    requires:
      bins:
        - slk
    cliHelp: "slk dnd --help"
---

# slk dnd

Do-Not-Disturb status and snooze

> **PREREQUISITE:** Read `../slk-shared/SKILL.md` for auth, global flags, security rules, and exit codes. If missing, run `slk generate-skills`.

| Command | Description |
|---------|-------------|
| `slk dnd end` | End the active DND period |
| `slk dnd end-snooze` | End the active DND snooze |
| `slk dnd info` | Show DND status for a user (or the caller) |
| `slk dnd snooze` | Start a DND snooze for the given number of minutes |
| `slk dnd team` | Show DND status for a comma-separated list of users |

## slk dnd end

End the active DND period

**Slack API:** `dnd.endDnd`

```bash
slk dnd end
```

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk dnd end-snooze

End the active DND snooze

**Slack API:** `dnd.endSnooze`

```bash
slk dnd end-snooze
```

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk dnd info

Show DND status for a user (or the caller)

**Slack API:** `dnd.info`

```bash
slk dnd info [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--user` | — | — | user ID (omit for the calling user) |

## slk dnd snooze

Start a DND snooze for the given number of minutes

**Slack API:** `dnd.setSnooze`

```bash
slk dnd snooze [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--minutes` | ✓ | `0` | number of minutes to snooze |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk dnd team

Show DND status for a comma-separated list of users

**Slack API:** `dnd.teamInfo`

```bash
slk dnd team [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--users` | ✓ | — | comma-separated user IDs |


