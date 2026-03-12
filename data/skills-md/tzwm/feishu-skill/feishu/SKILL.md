---
name: feishu
description: Interact with Feishu (Lark) API to manage Docx, Wiki, Drive, and Permissions. Use when you need to read, write, create documentation or manage cloud space in Feishu.
---

# Feishu Skill

A skill for interacting with the Feishu (Lark) API for advanced management of Documents, Wiki, Drive, and Permissions.

## Setup

First time setup:
```bash
cd skills/feishu
pnpm install
```

Requires the following environment variables to be set in your terminal or `.env`:
- `LARK_APP_ID`
- `LARK_APP_SECRET`

## Usage

Use the `pnpm start` command with various subcommands.

### Documents (doc)

Read document:
```bash
cd skills/feishu
pnpm start doc read -t <doc_token_or_url>
```

Write to document (replaces all content with Markdown):
```bash
pnpm start doc write -t <doc_token> --content "# Title\nNew content"
```

List comments on a document:
```bash
pnpm start doc list-comments -t <doc_token>
```

### Wiki (wiki)

List accessible wiki spaces:
```bash
cd skills/feishu
pnpm start wiki spaces
```

Get details of a Wiki node (returns underlying obj_token for docs):
```bash
pnpm start wiki get -t <wiki_token_or_url>
```

### Drive (drive)

List folder contents:
```bash
cd skills/feishu
pnpm start drive list -f <folder_token>
```

### Permissions (perm)

List collaborators:
```bash
cd skills/feishu
pnpm start perm list -t <file_token> --type docx
```

### IM (instant message)

List messages from a chat or thread:
```bash
cd skills/feishu
pnpm start im messages -c <chat_id>
```

Use `--help` on any command for more options:
```bash
pnpm start im --help
```

