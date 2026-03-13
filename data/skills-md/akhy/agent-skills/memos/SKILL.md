---
name: memos
description: Manage memos using a self-hosted Memos instance — create, list, update, delete memos, post comments, manage reactions, attachments, and relations via the Memos REST API.
compatibility: Requires curl and jq in PATH. Set MEMOS_URL and MEMOS_ACCESS_TOKEN env vars before use.
metadata:
  {
    "author": "akhy",
    "version": "1.0.0",
    "upstream": "https://usememos.com",
    "openclaw":
      {
        "emoji": "📝",
        "homepage": "https://usememos.com",
        "requires": { "bins": ["curl", "jq"], "env": ["MEMOS_URL", "MEMOS_ACCESS_TOKEN"] },
        "primaryEnv": "MEMOS_ACCESS_TOKEN",
        "install":
          [
            {
              "id": "brew-jq",
              "kind": "brew",
              "formula": "jq",
              "bins": ["jq"],
              "label": "Install jq (brew)",
            },
          ],
      },
  }
---

# Memos Skill

Interact with a [Memos](https://usememos.com) instance via its REST API (`/api/v1/memos`).

## Prerequisites

Set these env vars before using this skill:

```bash
export MEMOS_URL="https://memos.example.com"
export MEMOS_ACCESS_TOKEN="your_access_token"  # from Memos account settings
```

All requests use `Authorization: Bearer $MEMOS_ACCESS_TOKEN`.

## Script

All operations go through `scripts/memos.sh`. Run it with `bash memos/scripts/memos.sh <command> [options]`.

Run without arguments to see full usage:

```bash
bash memos/scripts/memos.sh --help
```

## Operations

### List memos

```bash
# All memos
bash memos/scripts/memos.sh list

# With filter (AIP-160 syntax)
bash memos/scripts/memos.sh list --filter 'state == "NORMAL"' --page-size 20

# Include deleted
bash memos/scripts/memos.sh list --show-deleted
```

### Create a memo

```bash
bash memos/scripts/memos.sh create --content "Hello, world!" --visibility PUBLIC

# Pinned private memo
bash memos/scripts/memos.sh create --content "Important note" --pinned
```

`--visibility`: `PUBLIC` | `PROTECTED` | `PRIVATE` (default: `PRIVATE`)

### Get a memo

```bash
bash memos/scripts/memos.sh get memos/123
```

Memo resource names follow the format `memos/{id}`.

### Update a memo

```bash
bash memos/scripts/memos.sh update memos/123 --content "Updated content"
bash memos/scripts/memos.sh update memos/123 --visibility PUBLIC --pinned true
bash memos/scripts/memos.sh update memos/123 --state ARCHIVED
```

Only specified fields are sent in `updateMask`.

### Delete a memo

```bash
# Soft delete
bash memos/scripts/memos.sh delete memos/123

# Hard delete
bash memos/scripts/memos.sh delete memos/123 --force
```

### Comments

```bash
# List comments
bash memos/scripts/memos.sh comments memos/123

# Post a comment
bash memos/scripts/memos.sh comment memos/123 --content "Great memo!"
```

### Reactions

```bash
# List reactions
bash memos/scripts/memos.sh reactions memos/123

# Add a reaction
bash memos/scripts/memos.sh react memos/123 --reaction "👍"

# Remove a reaction (reaction ID from list response)
bash memos/scripts/memos.sh delete-reaction memos/123 reactions/456
```

### Attachments

```bash
# List attachments
bash memos/scripts/memos.sh attachments memos/123

# Set attachments (replaces existing)
bash memos/scripts/memos.sh set-attachments memos/123 --names "attachments/1,attachments/2"
```

### Relations

```bash
# List relations
bash memos/scripts/memos.sh relations memos/123

# Set relations (replaces existing)
bash memos/scripts/memos.sh set-relations memos/123 --relations '[{"memo":"memos/123","relatedMemo":"memos/456","type":"REFERENCE"}]'
```

## Pagination

List commands support `--page-size N` and `--page-token TOKEN`. The response includes `nextPageToken` when more results are available:

```bash
result=$(bash memos/scripts/memos.sh list --page-size 10)
next=$(echo "$result" | jq -r '.nextPageToken // empty')

# Fetch next page
bash memos/scripts/memos.sh list --page-size 10 --page-token "$next"
```

## Filtering

Use AIP-160 filter expressions with `--filter`:

```bash
bash memos/scripts/memos.sh list --filter 'state == "NORMAL"'
bash memos/scripts/memos.sh list --filter 'visibility == "PUBLIC"'
```

## Response Format

All responses are JSON. Pipe through `jq` to extract fields:

```bash
# Get all memo names and snippets
bash memos/scripts/memos.sh list | jq '.memos[] | {name, snippet}'

# Get a single field
bash memos/scripts/memos.sh get memos/123 | jq '.content'
```
