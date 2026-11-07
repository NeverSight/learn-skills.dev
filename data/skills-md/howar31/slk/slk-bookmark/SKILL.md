---
name: slk-bookmark
description: "Manage channel bookmarks"
metadata:
  version: 0.8.1
  openclaw:
    category: "productivity"
    requires:
      bins:
        - slk
    cliHelp: "slk bookmark --help"
---

# slk bookmark

Manage channel bookmarks

> **PREREQUISITE:** Read `../slk-shared/SKILL.md` for auth, global flags, security rules, and exit codes. If missing, run `slk generate-skills`.

| Command | Description |
|---------|-------------|
| `slk bookmark add` | Add a bookmark to a channel |
| `slk bookmark edit` | Edit an existing channel bookmark |
| `slk bookmark list` | List bookmarks in a channel |
| `slk bookmark remove` | Remove a bookmark from a channel |

## slk bookmark add

Add a bookmark to a channel

**Slack API:** `bookmarks.add`

```bash
slk bookmark add [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel ID |
| `--link` | ✓ | — | bookmark URL |
| `--title` | ✓ | — | bookmark title |
| `--type` | — | `link` | bookmark type |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk bookmark edit

Edit an existing channel bookmark

**Slack API:** `bookmarks.edit`

```bash
slk bookmark edit [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel ID |
| `--id` | ✓ | — | bookmark ID |
| `--link` | — | — | new bookmark URL |
| `--title` | — | — | new bookmark title |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk bookmark list

List bookmarks in a channel

**Slack API:** `bookmarks.list`

```bash
slk bookmark list [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel ID |

## slk bookmark remove

Remove a bookmark from a channel

**Slack API:** `bookmarks.remove`

```bash
slk bookmark remove [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel ID |
| `--id` | ✓ | — | bookmark ID |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.


