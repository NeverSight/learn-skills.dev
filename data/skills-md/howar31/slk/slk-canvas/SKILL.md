---
name: slk-canvas
description: "Create, read, update, list canvases"
metadata:
  version: 0.8.1
  openclaw:
    category: "productivity"
    requires:
      bins:
        - slk
    cliHelp: "slk canvas --help"
---

# slk canvas

Create, read, update, list canvases

> **PREREQUISITE:** Read `../slk-shared/SKILL.md` for auth, global flags, security rules, and exit codes. If missing, run `slk generate-skills`.

| Command | Description |
|---------|-------------|
| `slk canvas create` | Create a standalone canvas |
| `slk canvas delete` | Delete a canvas |
| `slk canvas list` | List canvases via search.files |
| `slk canvas read` | Read a canvas as markdown (HTML-converted) |
| `slk canvas share` | Set access on a canvas for users or channels |
| `slk canvas unshare` | Remove access on a canvas for users or channels |
| `slk canvas update` | Update a canvas's content |

## slk canvas create

Create a standalone canvas

**Slack API:** `canvases.create`

```bash
slk canvas create [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--markdown` | — | — | canvas body in markdown |
| `--markdown-file` | — | — | path to markdown file (use - for stdin) |
| `--title` | ✓ | — | canvas title |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk canvas delete

Delete a canvas

**Slack API:** `canvases.delete`

```bash
slk canvas delete [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--id` | ✓ | — | canvas ID |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk canvas list

List canvases via search.files

**Slack API:** `search.files`

```bash
slk canvas list [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--limit` | — | `20` | max results (1-100) |
| `--query` | — | — | extra search terms prepended to type:canvases |

## slk canvas read

Read a canvas as markdown (HTML-converted)

**Slack API:** `files.info`

```bash
slk canvas read [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--id` | ✓ | — | canvas ID |
| `--with-sections` | — | — | also emit the section_id mapping (JSON output) |

## slk canvas share

Set access on a canvas for users or channels

**Slack API:** `canvases.access.set`

```bash
slk canvas share [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--access-level` | ✓ | — | access level: read, write, or owner |
| `--channels` | — | — | comma-separated channel IDs to grant access |
| `--id` | ✓ | — | canvas ID |
| `--users` | — | — | comma-separated user IDs to grant access |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk canvas unshare

Remove access on a canvas for users or channels

**Slack API:** `canvases.access.delete`

```bash
slk canvas unshare [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channels` | — | — | comma-separated channel IDs to remove access |
| `--id` | ✓ | — | canvas ID |
| `--users` | — | — | comma-separated user IDs to remove access |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.

## slk canvas update

Update a canvas's content

**Slack API:** `canvases.edit`

```bash
slk canvas update [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--action` | — | `replace` | edit action: replace (default), prepend, append |
| `--id` | ✓ | — | canvas ID |
| `--markdown` | — | — | new canvas body in markdown |
| `--markdown-file` | — | — | path to markdown file (use - for stdin) |
| `--section-id` | — | — | optional section ID to target |

> [!CAUTION]
> Write command — confirm with the user before executing; preview with `--dry-run`.


