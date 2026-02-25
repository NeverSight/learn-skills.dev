---
name: exa.ai-websearch-api
description: A skill that equips you with real-time, source-grounded web search and content retrieval using the Exa API—optimized for balanced relevance and speed (type="auto") and full-text extraction for downstream reasoning, RAG, and code assistance. Powering agents with fast, high-quality web search by Exa.AI.
---

# Exa API Setup Guide

Exa | Web Search API, AI Search Engine, & Website Crawler

## Your Configuration

| Setting | Value |
|---------|-------|
| Coding Tool | Other |
| Framework | cURL |
| Use Case | Coding agent, Agetnic AI, Open Claw |
| Search Type | Auto - Balanced relevance and speed (~1 second) |
| Content | Full text |

## Keywords
ai search engine,serp api,best ai search engine,search api,deep research api,web search api,web search ai,ai search api,deepresearch api,web crawling api,website crawler,metaphor,exa,api,search,ai,llms

---

## API Key Setup

### Environment Variable

```bash
export EXA_API_KEY="YOUR_API_KEY"
```

### .env File

```env
EXA_API_KEY=YOUR_API_KEY
```

---

## 🔌 Exa MCP Server

Give your AI coding assistant real-time web search with Exa MCP.

**Remote MCP URL:**
```
https://mcp.exa.ai/mcp?exaApiKey=YOUR_API_KEY
```

**Available tools:** `web_search_exa`, `get_code_context_exa`, `company_research_exa`, `crawling_exa`, `linkedin_search_exa`, `deep_researcher_start`

**HTTP config (Cursor, Claude Code, Codex):**
```json
{
  "mcpServers": {
    "exa": {
      "type": "http",
      "url": "https://mcp.exa.ai/mcp?exaApiKey=YOUR_API_KEY",
      "headers": {}
    }
  }
}
```

**Local install (Claude Desktop):**
```json
{
  "mcpServers": {
    "exa": {
      "command": "npx",
      "args": ["-y", "exa-mcp-server"],
      "env": { "EXA_API_KEY": "YOUR_API_KEY" }
    }
  }
}
```

📖 Full docs: [docs.exa.ai/reference/exa-mcp](https://docs.exa.ai/reference/exa-mcp)

---

## Quick Start (cURL)

### cURL

```bash
curl -X POST 'https://api.exa.ai/search' \
  -H 'x-api-key: YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "React hooks best practices 2024",
  "type": "auto",
  "num_results": 10,
  "contents": {
    "text": {
      "max_characters": 20000
    }
  }
}'
```

---

## Function Calling / Tool Use

Function calling (also known as tool use) allows your AI agent to dynamically decide when to search the web based on the conversation context. Instead of searching on every request, the LLM intelligently determines when real-time information would improve its response—making your agent more efficient and accurate.

**Why use function calling with Exa?**
- Your agent can ground responses in current, factual information
- Reduces hallucinations by fetching real sources when needed
- Enables multi-step reasoning where the agent searches, analyzes, and responds

📚 **Full documentation**: https://docs.exa.ai/reference/openai-tool-calling

### OpenAI Function Calling

```python
import json
from openai import OpenAI
from exa_py import Exa

openai = OpenAI()
exa = Exa()

tools = [{
    "type": "function",
    "function": {
        "name": "exa_search",
        "description": "Search the web for current information.",
        "parameters": {
            "type": "object",
            "properties": {"query": {"type": "string", "description": "Search query"}},
            "required": ["query"]
        }
    }
}]

def exa_search(query: str) -> str:
    results = exa.search(query=query, type="auto", num_results=10, contents={"text": {"max_characters": 20000}})
    return "\n".join([f"{r.title}: {r.url}" for r in results.results])

messages = [{"role": "user", "content": "What's the latest in AI safety?"}]
response = openai.chat.completions.create(model="gpt-4o", messages=messages, tools=tools)

if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    search_results = exa_search(json.loads(tool_call.function.arguments)["query"])
    messages.append(response.choices[0].message)
    messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": search_results})
    final = openai.chat.completions.create(model="gpt-4o", messages=messages)
    print(final.choices[0].message.content)
```

### Anthropic Tool Use

```python
import anthropic
from exa_py import Exa

client = anthropic.Anthropic()
exa = Exa()

tools = [{
    "name": "exa_search",
    "description": "Search the web for current information.",
    "input_schema": {
        "type": "object",
        "properties": {"query": {"type": "string", "description": "Search query"}},
        "required": ["query"]
    }
}]

def exa_search(query: str) -> str:
    results = exa.search(query=query, type="auto", num_results=10, contents={"text": {"max_characters": 20000}})
    return "\n".join([f"{r.title}: {r.url}" for r in results.results])

messages = [{"role": "user", "content": "Latest quantum computing developments?"}]
response = client.messages.create(model="claude-sonnet-4-20250514", max_tokens=4096, tools=tools, messages=messages)

if response.stop_reason == "tool_use":
    tool_use = next(b for b in response.content if b.type == "tool_use")
    tool_result = exa_search(tool_use.input["query"])
    messages.append({"role": "assistant", "content": response.content})
    messages.append({"role": "user", "content": [{"type": "tool_result", "tool_use_id": tool_use.id, "content": tool_result}]})
    final = client.messages.create(model="claude-sonnet-4-20250514", max_tokens=4096, tools=tools, messages=messages)
    print(final.content[0].text)
```

---

## Search Type Reference

| Type | Best For | Speed | Depth |
|------|----------|-------|-------|
| `fast` | Real-time apps, autocomplete, quick lookups | Fastest | Basic |
| `auto` | Most queries - balanced relevance & speed | Medium | Smart | ← your selection

**Tip:** `type="auto"` works well for most queries. It provides balanced relevance and speed.

---

## Content Configuration

Choose ONE content type per request (not both):

| Type | Config | Best For |
|------|--------|----------|
| Text | `"text": {"max_characters": 20000}` | Full content extraction, RAG | ← your selection
| Highlights | `"highlights": {"max_characters": 2000}` | Snippets, summaries, lower cost |

**⚠️ Token usage warning:** Using `text: true` (full page text) can significantly increase token count, leading to slower and more expensive LLM calls. To mitigate:
- Add `max_characters` limit: `"text": {"max_characters": 10000}`
- Use `highlights` instead if you don't need contiguous text

**When to use text vs highlights:**
- **Text** - When you need untruncated, contiguous content (e.g., code snippets, full articles, documentation)
- **Highlights** - When you need key excerpts and don't need the full context (e.g., summaries, Q&A, general research)

---

## Domain Filtering (Optional)

Usually not needed - Exa's neural search finds relevant results without domain restrictions.

**When to use:**
- Targeting specific authoritative sources
- Excluding low-quality domains from results

**Example:**
```json
{
  "includeDomains": ["arxiv.org", "github.com"],
  "excludeDomains": ["pinterest.com"]
}
```

**Note:** `includeDomains` and `excludeDomains` cannot be used together.

---

## Coding Agent

Use `category: "null"` to search for null content.

```json
{
  "query": "React hooks best practices 2024",
  "category": null,
  "num_results": 10,
  "contents": {
    "text": {
      "max_characters": 20000
    }
  }
}
```

**Tips:**
- Use `type: "auto"` for balanced results
- Great for documentation lookup, API references, code examples

### SDK Examples



---

## Category Examples

Use category filters to search dedicated indexes. Each category returns only that content type.

**Note:** Categories can be restrictive. If you're not getting enough results, try searching without a category first, then add one if needed.

### People Search (`category: "people"`)
Find people by role, expertise, or what they work on

```bash
curl -X POST 'https://api.exa.ai/search' \
  -H 'x-api-key: YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "software engineer distributed systems",
  "category": "people",
  "type": "auto",
  "num_results": 10
}'
```

**Tips:**
  - Use SINGULAR form
  - Describe what they work on
  - No date/text filters supported

### Company Search (`category: "company"`)
Find companies by industry, criteria, or attributes

```bash
curl -X POST 'https://api.exa.ai/search' \
  -H 'x-api-key: YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "AI startup healthcare",
  "category": "company",
  "type": "auto",
  "num_results": 10
}'
```

**Tips:**
  - Use SINGULAR form
  - Simple entity queries
  - Returns company objects, not articles

### News Search (`category: "news"`)
News articles

```bash
curl -X POST 'https://api.exa.ai/search' \
  -H 'x-api-key: YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "OpenAI announcements",
  "category": "news",
  "type": "auto",
  "num_results": 10,
  "contents": {
    "text": {
      "max_characters": 20000
    }
  }
}'
```

**Tips:**
  - Use livecrawl: "preferred" for breaking news
  - Avoid date filters unless required

### Research Papers (`category: "research paper"`)
Academic papers

```bash
curl -X POST 'https://api.exa.ai/search' \
  -H 'x-api-key: YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "transformer architecture improvements",
  "category": "research paper",
  "type": "auto",
  "num_results": 10,
  "contents": {
    "text": {
      "max_characters": 20000
    }
  }
}'
```

**Tips:**
  - Use type: "auto" for most queries
  - Includes arxiv.org, paperswithcode.com, and other academic sources

### Tweet Search (`category: "tweet"`)
Twitter/X posts

```bash
curl -X POST 'https://api.exa.ai/search' \
  -H 'x-api-key: YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "AI safety discussion",
  "category": "tweet",
  "type": "auto",
  "num_results": 10,
  "contents": {
    "text": {
      "max_characters": 20000
    }
  }
}'
```

**Tips:**
  - Good for real-time discussions
  - Captures public sentiment

---

## Content Freshness (maxAgeHours)

`maxAgeHours` sets the maximum acceptable age (in hours) for cached content. If the cached version is older than this threshold, Exa will livecrawl the page to get fresh content.

| Value | Behavior | Best For |
|-------|----------|----------|
| 24 | Use cache if less than 24 hours old, otherwise livecrawl | Daily-fresh content |
| 1 | Use cache if less than 1 hour old, otherwise livecrawl | Near real-time data |
| 0 | Always livecrawl (ignore cache entirely) | Real-time data where cached content is unusable |
| -1 | Never livecrawl (cache only) | Maximum speed, historical/static content |
| *(omit)* | Default behavior (livecrawl as fallback if no cache exists) | **Recommended** — balanced speed and freshness |

**When LiveCrawl Isn't Necessary:**
Cached data is sufficient for many queries, especially for historical topics or educational content. These subjects rarely change, so reliable cached results can provide accurate information quickly.

See [maxAgeHours docs](https://exa.ai/docs/reference/livecrawling-contents#maxAgeHours) for more details.

---

## Other Endpoints

Beyond `/search`, Exa offers these endpoints:

| Endpoint | Description | Docs |
|----------|-------------|------|
| `/contents` | Get contents for known URLs | [Docs](https://exa.ai/docs/reference/get-contents) |
| `/answer` | Q&A with citations from web search | [Docs](https://exa.ai/docs/reference/answer) |

**Example - Get contents for URLs:**
```json
POST /contents
{
  "urls": ["https://example.com/article"],
  "text": { "max_characters": 20000 }
}
```

---

## Troubleshooting

**Results not relevant?**
1. Try `type: "auto"` - most balanced option
2. Refine query - use singular form, be specific
3. Check category matches your use case

**Results too slow?**
1. Use `type: "fast"`
2. Reduce `num_results`
3. Skip contents if you only need URLs

**No results?**
1. Remove filters (date, domain restrictions)
2. Simplify query
3. Try `type: "auto"` - has fallback mechanisms

---

## Resources

- Docs: https://exa.ai/docs
- Dashboard: https://dashboard.exa.ai
- API Status: https://status.exa.ai