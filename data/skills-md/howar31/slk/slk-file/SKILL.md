---
name: slk-file
description: "List and manage files"
metadata:
  version: 0.8.1
  openclaw:
    category: "productivity"
    requires:
      bins:
        - slk
    cliHelp: "slk file --help"
---

# slk file

List and manage files

> **PREREQUISITE:** Read `../slk-shared/SKILL.md` for auth, global flags, security rules, and exit codes. If missing, run `slk generate-skills`.

| Command | Description |
|---------|-------------|
| `slk file delete` | Delete a file |
| `slk file info` | Show file details |
| `slk file list` | List files |
| `slk file public` | Make a file publicly accessible |
| `slk file revoke-public` | Revoke a file's public link |
| `slk file upload` | Upload a file |

## slk file delete

Delete a file

**Slack API:** `files.delete`

```bash
slk file delete [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--file` | ✓ | — | file ID |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk file info

Show file details

**Slack API:** `files.info`

```bash
slk file info [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--file` | ✓ | — | file ID |

## slk file list

List files

**Slack API:** `files.list`

```bash
slk file list [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | — | — | filter by channel ID (optional) |
| `--types` | — | — | filter by file types, comma-separated (optional) |
| `--user` | — | — | filter by user ID (optional) |

## slk file public

Make a file publicly accessible

**Slack API:** `files.sharedPublicURL`

```bash
slk file public [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--file` | ✓ | — | file ID |

**Tips:** Makes the file accessible to anyone with the link.

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk file revoke-public

Revoke a file's public link

**Slack API:** `files.revokePublicURL`

```bash
slk file revoke-public [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--file` | ✓ | — | file ID |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk file upload

Upload a file

**Slack API:** `files.getUploadURLExternal`

```bash
slk file upload [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel` | — | — | channel ID to share the file into (optional) |
| `--file` | ✓ | — | path to file to upload |
| `--title` | — | — | file title (defaults to filename) |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.


