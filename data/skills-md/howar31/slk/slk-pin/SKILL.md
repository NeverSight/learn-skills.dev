---
name: slk-pin
description: "Pin and unpin items"
metadata:
  version: 0.8.1
  openclaw:
    category: "productivity"
    requires:
      bins:
        - slk
    cliHelp: "slk pin --help"
---

# slk pin

Pin and unpin items

> **PREREQUISITE:** Read `../slk-shared/SKILL.md` for auth, global flags, security rules, and exit codes. If missing, run `slk generate-skills`.

| Command | Description |
|---------|-------------|
| `slk pin add` | Pin a message to a channel |
| `slk pin list` | List pinned items in a channel |
| `slk pin remove` | Unpin a message from a channel |

## slk pin add

Pin a message to a channel

**Slack API:** `pins.add`

```bash
slk pin add [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel ID |
| `--ts` | ✓ | — | message timestamp |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk pin list

List pinned items in a channel

**Slack API:** `pins.list`

```bash
slk pin list [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel ID |

## slk pin remove

Unpin a message from a channel

**Slack API:** `pins.remove`

```bash
slk pin remove [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel ID |
| `--ts` | ✓ | — | message timestamp |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.


