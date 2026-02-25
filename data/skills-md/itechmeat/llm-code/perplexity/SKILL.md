---
name: perplexity
description: "Integrate Perplexity API for web-grounded AI responses and search. Covers Sonar models, Search API, SDK usage (Python/TypeScript), streaming, structured outputs, filters, media attachments, Pro Search, and prompting. Keywords: Perplexity, Sonar, sonar-pro, sonar-reasoning-pro, sonar-deep-research, web search API, grounded LLM, chat completions, perplexityai SDK, image attachments, PDF analysis."
version: "0.30.0"
release_date: "2026-02-23"
---

# Perplexity API

Build AI applications with real-time web search and grounded responses.

## Quick Navigation

- Models & pricing: `references/models.md`
- Search API patterns: `references/search-api.md`
- Chat completions guide: `references/chat-completions.md`
- Browser sessions API: `references/browser.md`
- Embeddings API: `references/embeddings.md`
- Structured outputs: `references/structured-outputs.md`
- Filters (domain/language/date/location): `references/filters.md`
- Media (images/videos/attachments): `references/media.md`
- Pro Search: `references/pro-search.md`
- Prompting best practices: `references/prompting.md`

## When to Use

- Need AI responses grounded in current web data
- Building search-powered applications
- Research tools requiring citations
- Real-time Q&A with source verification
- Document/image analysis with web context

## Installation

Install: `pip install perplexityai` (Python) or `npm install @perplexityai/perplexity` (TypeScript/JavaScript).

## Authentication

```bash
# macOS/Linux
export PERPLEXITY_API_KEY="your_api_key_here"

# Windows
setx PERPLEXITY_API_KEY "your_api_key_here"
```

SDK auto-reads `PERPLEXITY_API_KEY` environment variable.

## Quick Start — Chat Completion

```python
from perplexity import Perplexity

client = Perplexity()

completion = client.chat.completions.create(
    model="sonar-pro",
    messages=[{"role": "user", "content": "What is the latest news on AI?"}]
)

print(completion.choices[0].message.content)
```

**Note (v0.28.0):** The Python client includes a custom JSON encoder to support additional types in request payloads.

## Quick Start — Search API

```python
from perplexity import Perplexity

client = Perplexity()

search = client.search.create(
    query="artificial intelligence trends 2024",
    max_results=5
)

for result in search.results:
    print(f"{result.title}: {result.url}")
```

## Model Selection Guide

| Model                 | Use Case                       | Cost    |
| --------------------- | ------------------------------ | ------- |
| `sonar`               | Quick facts, simple Q&A        | Lowest  |
| `sonar-pro`           | Complex queries, research      | Medium  |
| `sonar-reasoning-pro` | Multi-step reasoning, analysis | Medium  |
| `sonar-deep-research` | Exhaustive research, reports   | Highest |

## Key Patterns

### Streaming Responses

```python
stream = client.chat.completions.create(
    messages=[{"role": "user", "content": "Explain quantum computing"}],
    model="sonar",
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

### Multi-Turn Conversation

```python
messages = [
    {"role": "system", "content": "You are a research assistant."},
    {"role": "user", "content": "What causes climate change?"},
    {"role": "assistant", "content": "Climate change is caused by..."},
    {"role": "user", "content": "What are the solutions?"}
]

completion = client.chat.completions.create(messages=messages, model="sonar")
```

### Web Search Options

```python
completion = client.chat.completions.create(
    messages=[{"role": "user", "content": "Latest renewable energy news"}],
    model="sonar",
    web_search_options={
        "search_recency_filter": "week",
        "search_domain_filter": ["energy.gov", "iea.org"]
    }
)
```

### Pro Search (Multi-Step Research)

```python
# REQUIRES stream=True
completion = client.chat.completions.create(
    model="sonar-pro",
    messages=[{"role": "user", "content": "Research solar panel ROI"}],
    search_type="pro",
    stream=True
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")
```

### Image Attachment

```python
completion = client.chat.completions.create(
    model="sonar-pro",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Describe this image"},
            {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}}
        ]
    }]
)
```

### File Attachment (PDF Analysis)

```python
completion = client.chat.completions.create(
    model="sonar-pro",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Summarize this document"},
            {"type": "file_url", "file_url": {"url": "https://example.com/report.pdf"}}
        ]
    }]
)
```

### Return Images in Response

```python
completion = client.chat.completions.create(
    model="sonar",
    messages=[{"role": "user", "content": "Mount Everest photos"}],
    return_images=True,
    image_format_filter=["jpg", "png"]
)
```

### Domain Filtering (Search API)

```python
# Allowlist: include only these domains
search = client.search.create(
    query="climate research",
    search_domain_filter=["science.org", "nature.com"]
)

# Denylist: exclude these domains
search = client.search.create(
    query="tech news",
    search_domain_filter=["-reddit.com", "-pinterest.com"]
)
```

### Multi-Query Search

```python
search = client.search.create(
    query=[
        "AI trends 2024",
        "machine learning healthcare",
        "neural networks applications"
    ],
    max_results=5
)

for i, query_results in enumerate(search.results):
    print(f"Query {i+1} results:")
    for result in query_results:
        print(f"  {result.title}")
```

### Structured Outputs (JSON Schema)

```python
from pydantic import BaseModel

class ContactInfo(BaseModel):
    email: str
    phone: str

completion = client.chat.completions.create(
    model="sonar-pro",
    messages=[{"role": "user", "content": "Find contact for Tesla IR"}],
    response_format={
        "type": "json_schema",
        "json_schema": {"schema": ContactInfo.model_json_schema()}
    }
)

contact = ContactInfo.model_validate_json(completion.choices[0].message.content)
```

### Async Operations

```python
import asyncio
from perplexity import AsyncPerplexity

async def main():
    async with AsyncPerplexity() as client:
        tasks = [
            client.search.create(query="AI news"),
            client.search.create(query="tech trends")
        ]
        results = await asyncio.gather(*tasks)

asyncio.run(main())
```

### Rate Limit Handling

```python
import time
from perplexity import RateLimitError

def search_with_retry(client, query, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.search.create(query=query)
        except RateLimitError:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                raise
```

## Response Parameters

| Parameter           | Default | Description                     |
| ------------------- | ------- | ------------------------------- |
| `temperature`       | 0.7     | Creativity (0-2)                |
| `max_tokens`        | varies  | Response length limit           |
| `top_p`             | 0.9     | Nucleus sampling                |
| `presence_penalty`  | 0       | Reduce repetition (-2 to 2)     |
| `frequency_penalty` | 0       | Reduce word frequency (-2 to 2) |

## Search API Parameters

| Parameter                | Description                             |
| ------------------------ | --------------------------------------- |
| `max_results`            | 1-20 results per query                  |
| `max_tokens_per_page`    | Content extraction depth (default 2048) |
| `country`                | ISO country code for regional results   |
| `search_domain_filter`   | Domain allowlist/denylist (max 20)      |
| `search_language_filter` | ISO 639-1 language codes (max 10)       |

## Pricing Quick Reference

**Search API:** $5/1K requests (no token costs)

**Sonar Models (per 1M tokens):**
| Model | Input | Output |
|-------|-------|--------|
| sonar | $1 | $1 |
| sonar-pro | $3 | $15 |
| sonar-reasoning-pro | $2 | $8 |

**Request fees** (per 1K requests): $5-$14 depending on search context size.

## Critical Prohibitions

- Do NOT request links/URLs in prompts (use `citations` field instead — model will hallucinate URLs)
- Do NOT use recursive JSON schemas (not supported)
- Do NOT use `dict[str, Any]` in Pydantic models for structured outputs
- Do NOT mix allowlist and denylist in `search_domain_filter`
- Do NOT exceed 5 queries in multi-query search
- Do NOT expect first request with new JSON schema to be fast (10-30s warmup)
- Do NOT use Pro Search without `stream=True` (will fail)
- Do NOT send images to `sonar-deep-research` (not supported)
- Do NOT include `data:` prefix for file attachments base64 (only for images)
- Do NOT try to control search via prompts (use API parameters instead)

## Error Handling

```python
import perplexity

try:
    completion = client.chat.completions.create(...)
except perplexity.BadRequestError as e:
    print(f"Invalid parameters: {e}")
except perplexity.RateLimitError:
    print("Rate limited, retry later")
except perplexity.APIStatusError as e:
    print(f"API error: {e.status_code}")
```

## OpenAI SDK Compatibility

Perplexity supports OpenAI Chat Completions format. Use OpenAI client by pointing to Perplexity endpoint.

## Links

- [API Portal](https://www.perplexity.ai/settings/api)
- [Documentation](https://docs.perplexity.ai/)
- [Python SDK (PyPI)](https://pypi.org/project/perplexityai/)
- [TypeScript SDK (npm)](https://www.npmjs.com/package/@perplexityai/perplexity)
