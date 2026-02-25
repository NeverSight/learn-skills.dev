---
name: exa-search
description: Search the web using Exa's AI-powered search API. Supports semantic search, content extraction, direct answers, and deep research with structured output.
license: MIT
metadata:
  author: Nicolai Schmid
  version: 1.0.0
  requires:
    - curl
    - jq
---

# Exa Web Search

Search the web using Exa's AI-powered search API. Exa provides semantic search capabilities optimized for AI applications.

## Configuration

Config file: `~/.config/exa-search/config.json`

```json
{
  "api_key": "your-exa-api-key-here"
}
```

### Getting an API key

1. Go to https://dashboard.exa.ai/api-keys
2. Sign up or log in to your Exa account
3. Create a new API key

### Troubleshooting config

If requests fail, verify the config:

```bash
# Check config exists and is valid JSON
cat ~/.config/exa-search/config.json | jq .

# Test connection
curl -s -X POST "https://api.exa.ai/search" \
  -H "x-api-key: $(jq -r .api_key ~/.config/exa-search/config.json)" \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "numResults": 1}' | jq '.results | length'
```

**Common issues:**

- `401 Unauthorized`: API key is invalid → get a new key from dashboard
- `Connection refused`: Network issue or API is down
- `null` or parse error: Config file is missing or malformed

If config is broken, guide the user to provide their Exa API key, then create/update the config:

```bash
mkdir -p ~/.config/exa-search
cat > ~/.config/exa-search/config.json << 'EOF'
{
  "api_key": "USER_PROVIDED_API_KEY"
}
EOF
```

## Endpoint Selection Guide

Choose the appropriate endpoint based on user intent:

| Endpoint | Use When |
|----------|----------|
| `/search` | Need to find web pages, research topics, or get content from multiple sources |
| `/contents` | Have specific URLs and need to extract their full content |
| `/answer` | Need a direct, concise answer to a factual question |
| `/research/v1` | Need in-depth research with structured output, multi-step analysis, or comprehensive reports |

## API Examples

### Load API key

```bash
EXA_API_KEY=$(jq -r .api_key ~/.config/exa-search/config.json)
```

### 1. Search (`/search`)

Semantic search with optional content extraction. Returns results with their contents.

```bash
# Basic search
curl -s -X POST "https://api.exa.ai/search" \
  -H "x-api-key: $EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "latest developments in AI agents",
    "numResults": 10
  }' | jq '.results[] | {title, url, publishedDate}'

# Search with content extraction
curl -s -X POST "https://api.exa.ai/search" \
  -H "x-api-key: $EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "best practices for RAG systems",
    "numResults": 5,
    "contents": {
      "text": true,
      "highlights": {
        "numSentences": 3,
        "highlightsPerUrl": 2
      },
      "summary": {}
    }
  }' | jq '.results[] | {title, url, summary, highlights}'

# Search with date filters and domain restrictions
curl -s -X POST "https://api.exa.ai/search" \
  -H "x-api-key: $EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "OpenAI announcements",
    "numResults": 10,
    "startPublishedDate": "2024-01-01T00:00:00.000Z",
    "includeDomains": ["openai.com", "techcrunch.com", "theverge.com"],
    "contents": {
      "text": {"maxCharacters": 1000},
      "summary": {}
    }
  }' | jq

# Search with category filter
curl -s -X POST "https://api.exa.ai/search" \
  -H "x-api-key: $EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "transformer architecture papers",
    "numResults": 10,
    "category": "research paper",
    "contents": {
      "text": true,
      "summary": {}
    }
  }' | jq

# Deep search for comprehensive results
curl -s -X POST "https://api.exa.ai/search" \
  -H "x-api-key: $EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "climate change mitigation strategies",
    "type": "deep",
    "numResults": 20,
    "contents": {
      "text": true,
      "summary": {}
    }
  }' | jq
```

**Search types:**
- `auto` (default): Intelligently combines neural and other methods
- `neural`: Pure semantic/embeddings-based search
- `fast`: Quick keyword-based search
- `deep`: Comprehensive search with query expansion

**Categories:** `company`, `research paper`, `news`, `pdf`, `github`, `tweet`, `personal site`, `financial report`, `people`

### 2. Contents (`/contents`)

Extract content from specific URLs.

```bash
# Get content from URLs
curl -s -X POST "https://api.exa.ai/contents" \
  -H "x-api-key: $EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": [
      "https://arxiv.org/abs/2307.06435",
      "https://example.com/article"
    ],
    "text": true,
    "summary": {},
    "highlights": {
      "numSentences": 2,
      "highlightsPerUrl": 3
    }
  }' | jq '.results[] | {url, title, summary, highlights}'

# Get content with livecrawl for fresh data
curl -s -X POST "https://api.exa.ai/contents" \
  -H "x-api-key: $EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["https://example.com/news"],
    "text": {"maxCharacters": 5000},
    "livecrawl": "preferred"
  }' | jq
```

**Livecrawl options:**
- `never`: Only use cache
- `fallback`: Livecrawl when cache is empty (default)
- `preferred`: Try livecrawl first, fall back to cache
- `always`: Always livecrawl, never use cache

### 3. Answer (`/answer`)

Get direct answers to questions, grounded in web search results.

```bash
# Get a direct answer
curl -s -X POST "https://api.exa.ai/answer" \
  -H "x-api-key: $EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the current population of Tokyo?"
  }' | jq '{answer, citations: [.citations[] | {title, url}]}'

# Answer with full source text
curl -s -X POST "https://api.exa.ai/answer" \
  -H "x-api-key: $EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the main features of GPT-4?",
    "text": true
  }' | jq
```

### 4. Research (`/research/v1`)

Long-running research tasks with structured output. This is asynchronous - you create a task and poll for results.

```bash
# Create a research task with structured output
RESEARCH_RESPONSE=$(curl -s -X POST "https://api.exa.ai/research/v1" \
  -H "x-api-key: $EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "exa-research",
    "instructions": "Compare the top 3 cloud providers (AWS, Azure, GCP) on pricing for compute instances. Return structured data.",
    "outputSchema": {
      "type": "object",
      "required": ["providers"],
      "properties": {
        "providers": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["name", "computePricing", "strengths"],
            "properties": {
              "name": {"type": "string"},
              "computePricing": {"type": "string"},
              "strengths": {"type": "array", "items": {"type": "string"}}
            }
          }
        }
      }
    }
  }')

RESEARCH_ID=$(echo "$RESEARCH_RESPONSE" | jq -r '.researchId')
echo "Research ID: $RESEARCH_ID"

# Poll for results (repeat until status is "completed" or "failed")
curl -s "https://api.exa.ai/research/v1/$RESEARCH_ID" \
  -H "x-api-key: $EXA_API_KEY" | jq '{status, output}'

# Simple research without schema (returns markdown report)
curl -s -X POST "https://api.exa.ai/research/v1" \
  -H "x-api-key: $EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "exa-research",
    "instructions": "Summarize the latest developments in quantum computing from the past 6 months."
  }' | jq
```

**Research models:**
- `exa-research` (default): Balanced speed and quality, adapts to task difficulty
- `exa-research-pro`: Maximum quality, more thorough analysis (slower)

**Best practices for research:**
- Be explicit about what information you want
- Describe how the agent should find information
- Specify the desired output format
- Keep schemas small (1-5 root fields)
- Use enums in schemas for better accuracy

## API Reference

### Search Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | string | The search query (required) |
| `numResults` | integer | Number of results (max 100, default 10) |
| `type` | string | Search type: `auto`, `neural`, `fast`, `deep` |
| `category` | string | Filter by content type |
| `includeDomains` | array | Only include results from these domains |
| `excludeDomains` | array | Exclude results from these domains |
| `startPublishedDate` | string | Only results published after (ISO 8601) |
| `endPublishedDate` | string | Only results published before (ISO 8601) |
| `includeText` | array | Must contain this text (max 1 string, 5 words) |
| `excludeText` | array | Must not contain this text |
| `contents` | object | Content extraction options |

### Contents Options

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | boolean/object | Extract full page text |
| `highlights` | object | Extract relevant snippets |
| `summary` | object | Generate page summary |
| `livecrawl` | string | Crawl freshness: `never`, `fallback`, `preferred`, `always` |

### Response Fields

| Field | Description |
|-------|-------------|
| `requestId` | Unique request identifier |
| `results` | Array of search results |
| `results[].id` | Document ID (use with /contents) |
| `results[].url` | Page URL |
| `results[].title` | Page title |
| `results[].publishedDate` | Publication date |
| `results[].author` | Author if available |
| `results[].text` | Full page content (if requested) |
| `results[].highlights` | Relevant snippets (if requested) |
| `results[].summary` | Page summary (if requested) |
| `costDollars` | Request cost breakdown |

## Pricing Notes

- **Search:** $0.005 per request (1-25 results), $0.025 (26-100 results)
- **Deep Search:** $0.015 per request (1-25 results), $0.075 (26-100 results)
- **Contents:** $0.001 per page for text/highlights/summary
- **Answer:** Variable based on search and LLM usage
- **Research:** Variable usage-based (searches + pages read + reasoning tokens)
