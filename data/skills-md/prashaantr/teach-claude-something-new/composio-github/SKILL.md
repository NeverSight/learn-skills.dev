---
name: composio-github
description: |
  GitHub via Composio API. Use when:
  (1) Reading repository contents, README, or downloading repos
  (2) Creating, updating, or listing issues
  (3) Creating, listing, or merging pull requests
  (4) Listing repositories or branches
  DO NOT use `gh` CLI - it will fail with auth errors. Use Composio HTTP API only.
---

# GitHub via Composio

> **DO NOT** use `gh` CLI - it will fail with "gh auth login" error.
> Use the Composio HTTP API (curl commands) below instead.

## Environment

```bash
COMPOSIO_API_KEY      # API key
COMPOSIO_USER_ID      # Entity ID (required for all requests)
COMPOSIO_CONNECTIONS  # JSON with .github connection ID
```

## Core Pattern

```bash
CONNECTION_ID=$(echo $COMPOSIO_CONNECTIONS | jq -r '.github')

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
# List your repositories (public + private)
curl -s "https://backend.composio.dev/api/v3/tools/execute/GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER" \
  -H "x-api-key: $COMPOSIO_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "connected_account_id": "'$CONNECTION_ID'",
    "entity_id": "'$COMPOSIO_USER_ID'",
    "arguments": {"visibility": "all", "affiliation": "owner,collaborator,organization_member"}
  }' | jq '.data.repositories'

# List repository issues
curl -s "https://backend.composio.dev/api/v3/tools/execute/GITHUB_LIST_REPOSITORY_ISSUES" \
  -H "x-api-key: $COMPOSIO_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "connected_account_id": "'$CONNECTION_ID'",
    "entity_id": "'$COMPOSIO_USER_ID'",
    "arguments": {"owner": "OWNER", "repo": "REPO", "state": "open"}
  }' | jq
```

## All Actions

See [references/actions.md](references/actions.md) for complete API reference including:
- Repository contents: get files, README, download ZIP
- Issues: list, create, update, comment
- Pull requests: list, create, merge
- Repositories: list, get info
- Branches: list

## Discover Actions

```bash
curl -s "https://backend.composio.dev/api/v2/actions?apps=github" \
  -H "x-api-key: $COMPOSIO_API_KEY" | jq '.items[] | {name, description}'
```
