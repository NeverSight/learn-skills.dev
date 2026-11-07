---
name: slk-usergroup
description: "Manage user groups"
metadata:
  version: 0.8.1
  openclaw:
    category: "productivity"
    requires:
      bins:
        - slk
    cliHelp: "slk usergroup --help"
---

# slk usergroup

Manage user groups

> **PREREQUISITE:** Read `../slk-shared/SKILL.md` for auth, global flags, security rules, and exit codes. If missing, run `slk generate-skills`.

| Command | Description |
|---------|-------------|
| `slk usergroup create` | Create a user group |
| `slk usergroup disable` | Disable a user group |
| `slk usergroup enable` | Enable a user group |
| `slk usergroup list` | List user groups |
| `slk usergroup set-users` | Set the members of a user group |
| `slk usergroup update` | Update a user group |
| `slk usergroup users` | List members of a user group |

## slk usergroup create

Create a user group

**Slack API:** `usergroups.create`

```bash
slk usergroup create [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--description` | — | — | user group description (optional) |
| `--handle` | — | — | user group handle (optional) |
| `--name` | ✓ | — | user group name |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk usergroup disable

Disable a user group

**Slack API:** `usergroups.disable`

```bash
slk usergroup disable [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--usergroup` | ✓ | — | user group ID |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk usergroup enable

Enable a user group

**Slack API:** `usergroups.enable`

```bash
slk usergroup enable [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--usergroup` | ✓ | — | user group ID |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk usergroup list

List user groups

**Slack API:** `usergroups.list`

```bash
slk usergroup list
```

## slk usergroup set-users

Set the members of a user group

**Slack API:** `usergroups.users.update`

```bash
slk usergroup set-users [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--usergroup` | ✓ | — | user group ID |
| `--users` | ✓ | — | comma-separated user IDs |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk usergroup update

Update a user group

**Slack API:** `usergroups.update`

```bash
slk usergroup update [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--handle` | — | — | new user group handle (optional) |
| `--name` | — | — | new user group name (optional) |
| `--usergroup` | ✓ | — | user group ID |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk usergroup users

List members of a user group

**Slack API:** `usergroups.users.list`

```bash
slk usergroup users [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--usergroup` | ✓ | — | user group ID |


