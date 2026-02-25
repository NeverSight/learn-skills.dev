---
name: composio-linear
description: |
  Linear project management via Composio API. Use when:
  (1) Listing, creating, or updating Linear issues
  (2) Getting teams, users, or workflow states
  (3) Managing projects or adding comments
  (4) Creating custom views with label/assignee filters
  (5) Running custom GraphQL queries/mutations
  DO NOT use `linear` CLI - use Composio HTTP API only.
---

# Linear via Composio

> **DO NOT** use `linear` CLI. Use Composio HTTP API commands below.

## Environment

```bash
COMPOSIO_API_KEY      # API key
COMPOSIO_USER_ID      # Entity ID (required for all requests)
COMPOSIO_CONNECTIONS  # JSON with .linear connection ID
```

## Core Pattern

```bash
CONNECTION_ID=$(echo $COMPOSIO_CONNECTIONS | jq -r '.linear')

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
# List issues
curl -s "https://backend.composio.dev/api/v3/tools/execute/LINEAR_LIST_LINEAR_ISSUES" \
  -H "x-api-key: $COMPOSIO_API_KEY" -H "Content-Type: application/json" \
  -d '{"connected_account_id": "'$CONNECTION_ID'", "entity_id": "'$COMPOSIO_USER_ID'", "arguments": {}}' | jq

# Get teams
curl -s "https://backend.composio.dev/api/v3/tools/execute/LINEAR_GET_ALL_LINEAR_TEAMS" \
  -H "x-api-key: $COMPOSIO_API_KEY" -H "Content-Type: application/json" \
  -d '{"connected_account_id": "'$CONNECTION_ID'", "entity_id": "'$COMPOSIO_USER_ID'", "arguments": {}}' | jq
```

## All Actions

See [references/actions.md](references/actions.md) for complete API reference including:
- Issues: list, get, create, update, search, archive
- Teams & Users: list teams, list users, get current user
- Projects: list, create
- Comments: create
- Custom Views: create views with label/assignee filters (via GraphQL)
- Labels: list all labels (via GraphQL)
- GraphQL: run any query or mutation

## Discover Actions

```bash
curl -s "https://backend.composio.dev/api/v2/actions?apps=linear" \
  -H "x-api-key: $COMPOSIO_API_KEY" | jq '.items[] | {name, description}'
```
