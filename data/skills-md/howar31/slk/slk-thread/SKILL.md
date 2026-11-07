---
name: slk-thread
description: "Read and reply to threads"
metadata:
  version: 0.8.1
  openclaw:
    category: "productivity"
    requires:
      bins:
        - slk
    cliHelp: "slk thread --help"
---

# slk thread

Read and reply to threads

> **PREREQUISITE:** Read `../slk-shared/SKILL.md` for auth, global flags, security rules, and exit codes. If missing, run `slk generate-skills`.

| Command | Description |
|---------|-------------|
| `slk thread read` | Read replies in a thread |
| `slk thread reply` | Reply within a thread |

## slk thread read

Read replies in a thread

**Slack API:** `conversations.replies`

```bash
slk thread read [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel ID |
| `--cursor` | — | — | pagination cursor |
| `--latest` | — | — | end of time range (ts) |
| `--limit` | — | `100` | max replies |
| `--oldest` | — | — | start of time range (ts) |
| `--thread` | ✓ | — | parent message ts |

## slk thread reply

Reply within a thread

**Slack API:** `chat.postMessage`

```bash
slk thread reply [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | ✓ | — | channel ID |
| `--text` | — | — | reply text |
| `--text-file` | — | — | path to text file (use - for stdin) |
| `--thread` | ✓ | — | parent message ts |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.


