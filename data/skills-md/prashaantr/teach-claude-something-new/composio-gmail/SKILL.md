---
name: composio-gmail
description: |
  Gmail via Composio API. Use when:
  (1) Sending emails with optional CC/BCC
  (2) Listing, searching, or reading inbox messages
  (3) Replying to messages
  (4) Creating drafts or managing labels
  Use Composio HTTP API only.
---

# Gmail via Composio

## Environment

```bash
COMPOSIO_API_KEY      # API key
COMPOSIO_USER_ID      # Entity ID (required for all requests)
COMPOSIO_CONNECTIONS  # JSON with .gmail connection ID
```

## Core Pattern

```bash
CONNECTION_ID=$(echo $COMPOSIO_CONNECTIONS | jq -r '.gmail')

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
- User says "draft" or "prepare" → Use `GMAIL_CREATE_DRAFT` (saves to Drafts folder)
- User says "send" → Use `GMAIL_SEND_EMAIL` (sends immediately)

```bash
# CREATE DRAFT (saves to Drafts folder for user to review/send)
curl -s "https://backend.composio.dev/api/v3/tools/execute/GMAIL_CREATE_DRAFT" \
  -H "x-api-key: $COMPOSIO_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "connected_account_id": "'$CONNECTION_ID'",
    "entity_id": "'$COMPOSIO_USER_ID'",
    "arguments": {
      "to": "recipient@example.com",
      "subject": "Subject line",
      "body": "Email body text"
    }
  }' | jq

# SEND EMAIL (sends immediately - always include agent tag)
curl -s "https://backend.composio.dev/api/v3/tools/execute/GMAIL_SEND_EMAIL" \
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
curl -s "https://backend.composio.dev/api/v3/tools/execute/GMAIL_LIST_MESSAGES" \
  -H "x-api-key: $COMPOSIO_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "connected_account_id": "'$CONNECTION_ID'",
    "entity_id": "'$COMPOSIO_USER_ID'",
    "arguments": {"max_results": 10}
  }' | jq
```

## All Actions

See [references/actions.md](references/actions.md) for complete API reference including:
- Messages: send, list, search, get, reply
- Labels: list, add/remove from messages
- Drafts: create

## Discover Actions

```bash
curl -s "https://backend.composio.dev/api/v2/actions?apps=gmail" \
  -H "x-api-key: $COMPOSIO_API_KEY" | jq '.items[] | {name, description}'
```
