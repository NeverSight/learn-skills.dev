---
name: slk-search
description: "Search messages, channels, users"
metadata:
  version: 0.8.1
  openclaw:
    category: "productivity"
    requires:
      bins:
        - slk
    cliHelp: "slk search --help"
---

# slk search

Search messages, channels, users

> **PREREQUISITE:** Read `../slk-shared/SKILL.md` for auth, global flags, security rules, and exit codes. If missing, run `slk generate-skills`.

| Command | Description |
|---------|-------------|
| `slk search all` | Search messages and files combined (requires a user token) |
| `slk search channels` | List/search channels (client-side filter) |
| `slk search files` | Search files (requires a user token) |
| `slk search messages` | Search messages (requires a user token) |
| `slk search users` | List/search workspace users (client-side filter) |

## slk search all

Search messages and files combined (requires a user token)

**Slack API:** `search.all`

```bash
slk search all [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--query` | ✓ | — | search query |

## slk search channels

List/search channels (client-side filter)

**Slack API:** `conversations.list`

```bash
slk search channels [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--channel-types` | — | `public_channel,private_channel` | comma-separated channel types: public_channel,private_channel |
| `--include-archived` | — | — | include archived channels |
| `--query` | — | — | filter channels whose name contains this substring (case-insensitive) |

## slk search files

Search files (requires a user token)

**Slack API:** `search.files`

```bash
slk search files [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--query` | ✓ | — | search query |

## slk search messages

Search messages (requires a user token)

**Slack API:** `search.messages`

```bash
slk search messages [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--public` | — | — | restrict the search to public channels (appends in:public to the query) |
| `--query` | ✓ | — | search query |

## slk search users

List/search workspace users (client-side filter)

**Slack API:** `users.list`

```bash
slk search users [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--query` | — | — | filter users whose name/real_name contains this substring (case-insensitive) |


