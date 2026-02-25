---
name: composio-exa
description: |
  Exa AI-native semantic search via Composio API. Use when:
  (1) Searching the web with natural language queries
  (2) Getting citation-backed answers to research questions
  (3) Finding pages similar to a given URL
  (4) Retrieving full content from search results
  Exa understands meaning - queries don't need exact keyword matches.
---

# Exa Search via Composio

Exa is an AI-native search engine that understands meaning. Unlike keyword search, Exa finds what you're looking for even if your query doesn't match exact words on the page.

## Environment

```bash
COMPOSIO_API_KEY      # API key
COMPOSIO_USER_ID      # Entity ID (required for all requests)
COMPOSIO_CONNECTIONS  # JSON with .exa connection ID
```

## Core Pattern

```bash
CONNECTION_ID=$(echo $COMPOSIO_CONNECTIONS | jq -r '.exa')

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
# Semantic search
curl -s "https://backend.composio.dev/api/v3/tools/execute/EXA_SEARCH" \
  -H "x-api-key: $COMPOSIO_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "connected_account_id": "'$CONNECTION_ID'",
    "entity_id": "'$COMPOSIO_USER_ID'",
    "arguments": {
      "query": "best practices for building AI agents",
      "numResults": 10,
      "type": "auto"
    }
  }' | jq

# Get citation-backed answer
curl -s "https://backend.composio.dev/api/v3/tools/execute/EXA_ANSWER" \
  -H "x-api-key: $COMPOSIO_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "connected_account_id": "'$CONNECTION_ID'",
    "entity_id": "'$COMPOSIO_USER_ID'",
    "arguments": {
      "query": "What are the key differences between RAG and fine-tuning?"
    }
  }' | jq
```

## Query Tips

Exa understands natural language. Write queries as if asking a knowledgeable person:

| Instead of | Try |
|------------|-----|
| `"LLM fine tuning"` | `"tutorials on how to fine-tune large language models"` |
| `"react hooks"` | `"best practices for using React hooks in production"` |
| `"startup funding"` | `"guides for raising seed funding for AI startups"` |

## Best Practices

1. **Use EXA_ANSWER for questions**: When you need a direct answer with citations
2. **Use EXA_SEARCH for exploration**: When you need multiple results to analyze
3. **Be specific**: "Python libraries for PDF text extraction" > "PDF Python"
4. **Use filters**: Narrow by domain or date for recent/authoritative sources

## All Actions

See [references/actions.md](references/actions.md) for complete API reference including:
- EXA_SEARCH: Semantic web search with filtering
- EXA_ANSWER: Citation-backed answers to questions
- EXA_FIND_SIMILAR: Find pages similar to a URL
- EXA_GET_CONTENTS_ACTION: Get full content from results

## Discover Actions

```bash
curl -s "https://backend.composio.dev/api/v2/actions?apps=exa" \
  -H "x-api-key: $COMPOSIO_API_KEY" | jq '.items[] | {name, description}'
```
