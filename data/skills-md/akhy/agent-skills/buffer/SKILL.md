---
name: buffer
description: Manage Buffer social media posts and ideas — create and schedule posts to connected channels, manage the post queue, and create ideas in the Buffer Create space. Supports all Buffer-connected services (Instagram, Twitter/X, Facebook, LinkedIn, TikTok, Pinterest, YouTube, Mastodon, Bluesky, Threads, Google Business).
compatibility: Requires curl and jq in PATH. Set BUFFER_API_KEY env var before use.
metadata:
  upstream: https://buffer.com
---

# Buffer Skill

Interact with [Buffer](https://buffer.com) via its GraphQL API (`https://api.buffer.com`).

## Prerequisites

Set this env var before using this skill:

```bash
export BUFFER_API_KEY="your_api_key"  # from Buffer account settings
```

All requests use `Authorization: Bearer $BUFFER_API_KEY`.

## Script

All operations go through `scripts/buffer.sh`. Run from the repo root:

```bash
bash buffer/scripts/buffer.sh <command> [options]
```

Run without arguments or with `--help` to see full usage:

```bash
bash buffer/scripts/buffer.sh --help
```

## Workflow

Most operations need an **org ID** and a **channel ID**. Start here:

```bash
# 1. Get your organization ID
bash buffer/scripts/buffer.sh account | jq '.account.organizations[].id'

# 2. List channels to find channel IDs
bash buffer/scripts/buffer.sh channels --org-id <org-id> | jq '.channels[] | {id, name, service}'
```

## Operations

### Create a post

```bash
# Add to queue (default)
bash buffer/scripts/buffer.sh create-post \
  --channel-id <channel-id> \
  --text "Hello from the Buffer API!"

# Schedule at a specific time
bash buffer/scripts/buffer.sh create-post \
  --channel-id <channel-id> \
  --text "Scheduled post" \
  --mode customScheduled \
  --due-at "2026-04-01T09:00:00Z"

# Share immediately
bash buffer/scripts/buffer.sh create-post \
  --channel-id <channel-id> \
  --text "Posting now!" \
  --mode shareNow

# Save as draft
bash buffer/scripts/buffer.sh create-post \
  --channel-id <channel-id> \
  --text "Draft content" \
  --save-draft

# Post linked to an idea
bash buffer/scripts/buffer.sh create-post \
  --channel-id <channel-id> \
  --text "Content from my idea" \
  --idea-id <idea-id>
```

**`--mode` values:** `addToQueue` (default) | `shareNow` | `shareNext` | `customScheduled` | `recommendedTime`

**`--scheduling-type` values:** `automatic` (default) | `notification`

> **Note on editing posts:** Buffer's public GraphQL API does not expose an `updatePost` mutation. Use `update-post` to create a revised draft, or edit the post in the Buffer dashboard.

### Get and list posts

```bash
# Get a single post
bash buffer/scripts/buffer.sh get-post --id <post-id>

# List all posts
bash buffer/scripts/buffer.sh list-posts --org-id <org-id>

# Filter by status and channel
bash buffer/scripts/buffer.sh list-posts \
  --org-id <org-id> \
  --status scheduled \
  --channel-id <channel-id>

# Paginate
result=$(bash buffer/scripts/buffer.sh list-posts --org-id <org-id> --limit 10)
cursor=$(echo "$result" | jq -r '.posts.pageInfo.endCursor')
bash buffer/scripts/buffer.sh list-posts --org-id <org-id> --limit 10 --after "$cursor"
```

**`--status` values:** `draft` | `scheduled` | `sent` | `error` | `needs_approval`

### Create an idea

```bash
# Basic idea
bash buffer/scripts/buffer.sh create-idea \
  --org-id <org-id> \
  --title "Campaign concept" \
  --text "Details about the campaign..."

# With target date and tags
bash buffer/scripts/buffer.sh create-idea \
  --org-id <org-id> \
  --title "Spring promo" \
  --text "Spring sale announcement ideas" \
  --date "2026-04-01T00:00:00Z" \
  --tags '[{"id":"tag-id","name":"Marketing","color":"#FF5733"}]'
```

> **Note on editing ideas:** Buffer's public GraphQL API does not expose an `updateIdea` mutation. Use `update-idea` to create a revised idea.

### Channel info

```bash
# List all channels for an org
bash buffer/scripts/buffer.sh channels --org-id <org-id>

# Get a specific channel with posting schedule
bash buffer/scripts/buffer.sh channel --id <channel-id>
```

## Response Format

All responses are JSON. Use `jq` to extract fields:

```bash
# Get created post ID
bash buffer/scripts/buffer.sh create-post \
  --channel-id <channel-id> \
  --text "Hello!" | jq '.createPost.post.id'

# List scheduled post texts
bash buffer/scripts/buffer.sh list-posts \
  --org-id <org-id> \
  --status scheduled | jq '.posts.edges[].node | {id, text, dueAt}'

# Get idea ID after creation
bash buffer/scripts/buffer.sh create-idea \
  --org-id <org-id> \
  --title "My idea" | jq '.createIdea.id // .createIdea.idea.id'
```

## Supported Services

`instagram` · `twitter` · `facebook` · `linkedin` · `pinterest` · `tiktok` · `youtube` · `mastodon` · `bluesky` · `threads` · `googlebusiness` · `startPage`
