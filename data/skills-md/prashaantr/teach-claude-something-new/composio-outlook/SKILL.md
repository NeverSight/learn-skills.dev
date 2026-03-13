---
name: composio-outlook
description: |
  Outlook/Microsoft 365 email via Composio API. Use when:
  (1) Sending emails via Outlook/Microsoft 365
  (2) Listing, searching, or reading Outlook inbox messages
  (3) Replying to Outlook emails
  (4) Creating drafts or managing folders
  Use Composio HTTP API only.
---

# Outlook via Composio

## Environment

```bash
COMPOSIO_API_KEY      # API key
COMPOSIO_USER_ID      # Entity ID (required for all requests)
COMPOSIO_CONNECTIONS  # JSON with .outlook connection ID
```

## Core Pattern

```bash
CONNECTION_ID=$(echo $COMPOSIO_CONNECTIONS | jq -r '.outlook')

curl -s "https://backend.composio.dev/api/v3/tools/execute/ACTION_NAME" \
  -H "x-api-key: $COMPOSIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "connected_account_id": "'$CONNECTION_ID'",
    "entity_id": "'$COMPOSIO_USER_ID'",
    "arguments": {}
  }' | jq '.data'
```

## Quick Start

**IMPORTANT: Choose the right action!**
- User says "draft" or "prepare" → Use `OUTLOOK_CREATE_DRAFT` (saves to Drafts folder)
- User says "send" → Use `OUTLOOK_SEND_EMAIL` (sends immediately)

```bash
# SEND EMAIL (sends immediately - always include agent tag)
curl -s "https://backend.composio.dev/api/v3/tools/execute/OUTLOOK_SEND_EMAIL" \
  -H "x-api-key: $COMPOSIO_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "connected_account_id": "'$CONNECTION_ID'",
    "entity_id": "'$COMPOSIO_USER_ID'",
    "arguments": {
      "to": "recipient@example.com",
      "subject": "Subject line",
      "body": "Email body text\n\n--\nSent by '"$AGENT_NAME"'"
    }
  }' | jq

# List recent messages
curl -s "https://backend.composio.dev/api/v3/tools/execute/OUTLOOK_LIST_MESSAGES" \
  -H "x-api-key: $COMPOSIO_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "connected_account_id": "'$CONNECTION_ID'",
    "entity_id": "'$COMPOSIO_USER_ID'",
    "arguments": {"max_results": 10}
  }' | jq

# Get specific message by ID
curl -s "https://backend.composio.dev/api/v3/tools/execute/OUTLOOK_GET_MESSAGE" \
  -H "x-api-key: $COMPOSIO_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "connected_account_id": "'$CONNECTION_ID'",
    "entity_id": "'$COMPOSIO_USER_ID'",
    "arguments": {"message_id": "MESSAGE_ID_HERE"}
  }' | jq

# Search messages
curl -s "https://backend.composio.dev/api/v3/tools/execute/OUTLOOK_SEARCH_MESSAGES" \
  -H "x-api-key: $COMPOSIO_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "connected_account_id": "'$CONNECTION_ID'",
    "entity_id": "'$COMPOSIO_USER_ID'",
    "arguments": {"query": "from:someone@example.com"}
  }' | jq
```

## Common Actions

| Action | Description |
|--------|-------------|
| `OUTLOOK_SEND_EMAIL` | Send email immediately |
| `OUTLOOK_CREATE_DRAFT` | Save draft without sending |
| `OUTLOOK_LIST_MESSAGES` | List inbox messages |
| `OUTLOOK_GET_MESSAGE` | Get message by ID |
| `OUTLOOK_SEARCH_MESSAGES` | Search messages |
| `OUTLOOK_REPLY_TO_MESSAGE` | Reply to a message |
| `OUTLOOK_LIST_FOLDERS` | List mail folders |

## Discover All Actions

```bash
curl -s "https://backend.composio.dev/api/v2/actions?apps=outlook" \
  -H "x-api-key: $COMPOSIO_API_KEY" | jq '.items[] | {name, description}'
```
