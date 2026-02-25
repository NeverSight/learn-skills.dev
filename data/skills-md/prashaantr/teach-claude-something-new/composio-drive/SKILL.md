---
name: composio-drive
description: |
  Google Drive via Composio API. Use when:
  (1) Listing, searching, or downloading files
  (2) Uploading files or creating folders
  (3) Sharing files with users
  (4) Managing file metadata
  Use Composio HTTP API only.
---

# Google Drive via Composio

## Environment

```bash
COMPOSIO_API_KEY      # API key
COMPOSIO_USER_ID      # Entity ID (required for all requests)
COMPOSIO_CONNECTIONS  # JSON with .googledrive connection ID
```

## Core Pattern

```bash
CONNECTION_ID=$(echo $COMPOSIO_CONNECTIONS | jq -r '.googledrive')

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

```bash
# List files
curl -s "https://backend.composio.dev/api/v3/tools/execute/GOOGLEDRIVE_LIST_FILES" \
  -H "x-api-key: $COMPOSIO_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "connected_account_id": "'$CONNECTION_ID'",
    "entity_id": "'$COMPOSIO_USER_ID'",
    "arguments": {}
  }' | jq

# Search files
curl -s "https://backend.composio.dev/api/v3/tools/execute/GOOGLEDRIVE_SEARCH_FILES" \
  -H "x-api-key: $COMPOSIO_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "connected_account_id": "'$CONNECTION_ID'",
    "entity_id": "'$COMPOSIO_USER_ID'",
    "arguments": {"query": "name contains 'report'"}
  }' | jq
```

## All Actions

See [references/actions.md](references/actions.md) for complete API reference including:
- Files: list, search, get metadata, download, upload, delete
- Folders: create, list contents
- Sharing: share with users

## Discover Actions

```bash
curl -s "https://backend.composio.dev/api/v2/actions?apps=googledrive" \
  -H "x-api-key: $COMPOSIO_API_KEY" | jq '.items[] | {name, description}'
```
