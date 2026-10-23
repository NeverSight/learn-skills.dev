---
name: slk-list
description: "Create and manage Slack Lists"
metadata:
  version: 0.8.1
  openclaw:
    category: "productivity"
    requires:
      bins:
        - slk
    cliHelp: "slk list --help"
---

# slk list

Create and manage Slack Lists

> **PREREQUISITE:** Read `../slk-shared/SKILL.md` for auth, global flags, security rules, and exit codes. If missing, run `slk generate-skills`.

| Command | Description |
|---------|-------------|
| `slk list add-item` | Add an item to a List |
| `slk list create` | Create a new List |
| `slk list delete-item` | Delete one item from a List |
| `slk list read` | Read items in a List |
| `slk list update` | Update metadata of a List |
| `slk list update-item` | Update an item in a List |

## slk list add-item

Add an item to a List

**Slack API:** `slackLists.items.create`

```bash
slk list add-item [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--fields` | — | `[]` | initial fields as JSON array (see Long help for shape) |
| `--id` | ✓ | — | list ID |

**Tips:** Add an item to a List.

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk list create

Create a new List

**Slack API:** `slackLists.create`

```bash
slk list create [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--title` | ✓ | — | list title |

**Tips:** Create a Slack List. Lists cannot be deleted via the public API (slackLists.delete does not exist) — remove them in the Slack UI.

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk list delete-item

Delete one item from a List

**Slack API:** `slackLists.items.delete`

```bash
slk list delete-item [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--id` | ✓ | — | list ID |
| `--row-id` | ✓ | — | row (item) ID to delete |

**Tips:** Deletes one List item. The whole-list delete API (slackLists.delete) does not exist — remove a List in the Slack UI.

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk list read

Read items in a List

**Slack API:** `slackLists.items.list`

```bash
slk list read [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--id` | ✓ | — | list ID |

## slk list update

Update metadata of a List

**Slack API:** `slackLists.update`

```bash
slk list update [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--description` | — | — | new description for the list |
| `--id` | ✓ | — | list ID |
| `--name` | — | — | new name for the list |
| `--todo-mode` | — | — | todo mode string (e.g. "on" or "off") |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk list update-item

Update an item in a List

**Slack API:** `slackLists.items.update`

```bash
slk list update-item [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--fields` | — | `[]` | updated cells as JSON array (see Long help for shape) |
| `--id` | ✓ | — | list ID |
| `--row-id` | — | — | row to update; injected as cells[].row_id when a cell omits it |

**Tips:** Update an item in a List.

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.


