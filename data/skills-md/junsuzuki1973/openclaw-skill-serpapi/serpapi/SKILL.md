---
name: serpapi
description: Google Search API via SerpAPI for real-time search results with high freshness.
---

# SerpAPI - Google Search API

Google Search API via SerpAPI for accessing real-time Google search results with high freshness. Perfect for tracking the latest LLM versions, tech trends, and competitive research.

## Configuration

API credentials are stored in `~/.clawdbot/serpapi-config.json`:
```json
{
  "apiKey": "your_serpapi_key_here"
}
```

## API Endpoints

### Google Search

**Basic Search**
```bash
curl -s "https://serpapi.com/search?q={query}&api_key={apiKey}&type=search"
```

**Parameters:**
- `q` - Search query (required)
- `type` - Search type: `search` (default), `news`, `images`, `videos`
- `engine` - Search engine: `google` (default), `bing`, `yahoo`, `duckduckgo`
- `google_domain` - Google domain: `google.com`, `google.co.jp`, etc.
- `gl` - Country: `us`, `jp`, `uk`, `de`, etc.
- `hl` - Language: `en`, `ja`, `de`, `fr`, etc.
- `num` - Number of results (default: 10)
- `start` - Pagination offset (default: 0)
- `safe` - Safe search: `active`, `off`
- `filter` - Filter results: `0` (all), `1` (filter similar)
- `tbm` - Specific search: `isch` (images), `vid` (videos), `nws` (news)
- `tbs` - Advanced search operators (date range, etc.)

### News Search

**Google News**
```bash
curl -s "https://serpapi.com/search?q={query}&api_key={apiKey}&type=search&tbm=nws"
```

**Time-Based News:**
```bash
# Past hour
curl -s "https://serpapi.com/search?q={query}&api_key={apiKey}&tbm=nws&tbs=qdr:h"

# Past 24 hours
curl -s "https://serpapi.com/search?q={query}&api_key={apiKey}&tbm=nws&tbs=qdr:d"

# Past week
curl -s "https://serpapi.com/search?q={query}&api_key={apiKey}&tbm=nws&tbs=qdr:w"

# Past month
curl -s "https://serpapi.com/search?q={query}&api_key={apiKey}&tbm=nws&tbs=qdr:m"

# Past year
curl -s "https://serpapi.com/search?q={query}&api_key={apiKey}&tbm=nws&tbs=qdr:y"
```

### Advanced Search

**Date Range Search:**
```bash
# Specific date range (CDATE: YYYY-MM-DD)
curl -s "https://serpapi.com/search?q={query}&api_key={apiKey}&tbs=cdr:1,cd_min:2025-01-01,cd_max:2025-12-31"
```

**File Type Search:**
```bash
# PDF files
curl -s "https://serpapi.com/search?q={query}&api_key={apiKey}&tbs=ift:pdf"

# Specific site
curl -s "https://serpapi.com/search?q={query}+site:docs.anthropic.com&api_key={apiKey}"
```

**Exact Phrase:**
```bash
curl -s "https://serpapi.com/search?q=\"exact phrase\"&api_key={apiKey}"
```

**Exclude Words:**
```bash
curl -s "https://serpapi.com/search?q={query}+-{exclude}&api_key={apiKey}"
```

**OR Search:**
```bash
curl -s "https://serpapi.com/search?q={term1}+OR+{term2}&api_key={apiKey}"
```

## Response Format

```json
{
  "search_metadata": {
    "id": "search_id",
    "status": "Success",
    "created_at": "2026-02-01 00:00:00 UTC",
    "total_time_taken": 1.23,
    "request_url": "https://...",
    "google_url": "https://..."
  },
  "search_parameters": {
    "q": "search query",
    "engine": "google",
    "google_domain": "google.com"
  },
  "search_information": {
    "total_results": 1000000,
    "time_taken": 0.45
  },
  "organic_results": [
    {
      "position": 1,
      "title": "Page Title",
      "link": "https://example.com",
      "snippet": "Page description...",
      "date": "Feb 1, 2026"
    }
  ],
  "answer_box": {...},
  "people_also_ask": [...],
  "related_questions": [...],
  "knowledge_graph": {...}
}
```

## Usage Examples

### Search for Latest LLM Versions
```bash
# Claude latest version
curl -s "https://serpapi.com/search?q=Claude+4+latest+version+2026&api_key={apiKey}&gl=us&hl=en" | jq '.organic_results[:5]'

# GPT-5 release date
curl -s "https://serpapi.com/search?q=GPT-5+release+date&api_key={apiKey}" | jq '.organic_results[:5]'

# Gemini 2 Pro updates
curl -s "https://serpapi.com/search?q=Gemini+2+Pro+updates+2026&api_key={apiKey}" | jq '.organic_results[:5]'
```

### Tech Trends & Libraries
```bash
# Latest Python features
curl -s "https://serpapi.com/search?q=Python+3.14+new+features&api_key={apiKey}" | jq '.organic_results[:5]'

# React 19 changes
curl -s "https://serpapi.com/search?q=React+19+changes+2026&api_key={apiKey}" | jq '.organic_results[:5]'

# OpenAI API changelog
curl -s "https://serpapi.com/search?q=OpenAI+API+changelog+2026&api_key={apiKey}&tbm=nws&tbs=qdr:w" | jq '.organic_results[:5]'
```

### Japanese Search
```bash
# Japanese results
curl -s "https://serpapi.com/search?q=AIエージェント最新情報&api_key={apiKey}&gl=jp&hl=ja&google_domain=google.co.jp" | jq '.organic_results[:5]'
```

### Competitive Research
```bash
# Search specific company
curl -s "https://serpapi.com/search?q=OpenAI+competitors+2026&api_key={apiKey}" | jq '.organic_results[:5]'

# AI industry news (past week)
curl -s "https://serpapi.com/search?q=AI+industry&api_key={apiKey}&tbm=nws&tbs=qdr:w" | jq '.organic_results[:5]'
```

## Helper Scripts

### Quick Search
```bash
#!/bin/bash
# ~/.openclaw/workspace/skills/serpapi/scripts/search.sh

API_KEY=$(cat ~/.clawdbot/serpapi-config.json | jq -r '.apiKey')
QUERY="${1:-AI news}"

curl -s "https://serpapi.com/search?q=$(printf '%s' "$QUERY" | jq -sRr @uri)&api_key=$API_KEY&num=10" \
  | jq '.organic_results[] | {position, title, link, snippet}'
```

### News Search (Past 24h)
```bash
#!/bin/bash
# ~/.openclaw/workspace/skills/serpapi/scripts/search_news_24h.sh

API_KEY=$(cat ~/.clawdbot/serpapi-config.json | jq -r '.apiKey')
QUERY="${1:-AI}"

curl -s "https://serpapi.com/search?q=$(printf '%s' "$QUERY" | jq -sRr @uri)&api_key=$API_KEY&tbm=nws&tbs=qdr:d&num=10" \
  | jq '.organic_results[] | {position, title, link, date, snippet}'
```

### Japanese Search
```bash
#!/bin/bash
# ~/.openclaw/workspace/skills/serpapi/scripts/search_ja.sh

API_KEY=$(cat ~/.clawdbot/serpapi-config.json | jq -r '.apiKey')
QUERY="${1:-AI}"

curl -s "https://serpapi.com/search?q=$(printf '%s' "$QUERY" | jq -sRr @uri)&api_key=$API_KEY&gl=jp&hl=ja&google_domain=google.co.jp&num=10" \
  | jq '.organic_results[]'
```

### Latest LLM Info
```bash
#!/bin/bash
# ~/.openclaw/workspace/skills/serpapi/scripts/search_llm.sh

API_KEY=$(cat ~/.clawdbot/serpapi-config.json | jq -r '.apiKey')
QUERY="${1:-Claude 4}"

curl -s "https://serpapi.com/search?q=$(printf '%s' "$QUERY" | jq -sRr @uri)+latest+version+2026&api_key=$API_KEY&gl=us&hl=en&num=5" \
  | jq '.organic_results[] | {title, link, snippet}'
```

## Country & Language Codes

### Google Domains
- `google.com` - US (default)
- `google.co.jp` - Japan
- `google.co.uk` - United Kingdom
- `google.de` - Germany
- `google.fr` - France

### Country Codes (gl)
- `us` - United States
- `jp` - Japan
- `uk` - United Kingdom
- `de` - Germany
- `fr` - France

### Language Codes (hl)
- `en` - English
- `ja` - Japanese
- `de` - German
- `fr` - French
- `es` - Spanish

## Time-Based Search Operators (tbs)

- `qdr:h` - Past hour
- `qdr:d` - Past 24 hours
- `qdr:w` - Past week
- `qdr:m` - Past month
- `qdr:y` - Past year
- `cdr:1,cd_min:YYYY-MM-DD,cd_max:YYYY-MM-DD` - Custom date range

## Use Cases for OpenClaw

### Real-Time Information Gathering
```bash
# Check latest LLM API pricing
~/.openclaw/workspace/skills/serpapi/scripts/search.sh "OpenAI API pricing 2026"

# Check if a library version is outdated
~/.openclaw/workspace/skills/serpapi/scripts/search.sh "React 19 release date"

# Verify breaking changes
~/.openclaw/workspace/skills/serpapi/scripts/search.sh "Python 3.14 breaking changes"
```

### Competitive Intelligence
```bash
# Latest AI startup funding
~/.openclaw/workspace/skills/serpapi/scripts/search_news_24h.sh "AI startup funding"

# New AI tools released
~/.openclaw/workspace/skills/serpapi/scripts/search_news_24h.sh "new AI tool launch"
```

### Technical Problem Solving
```bash
# Find recent solutions
~/.openclaw/workspace/skills/serpapi/scripts/search.sh "Node.js memory leak 2026"

# Check if others have the same issue
~/.openclaw/workspace/skills/serpapi/scripts/search.sh "error code 0x80070005 Windows 11"
```

## Rate Limits

Check your SerpAPI plan for specific limits:
- Free plan: 100 searches/month
- Paid plans: Higher limits available

## Notes

- SerpAPI provides real-time Google search results
- Results are always fresh (no caching by default)
- Supports multiple search engines (Google, Bing, Yahoo, DuckDuckGo)
- Can extract structured data (knowledge graph, answer boxes, etc.)
- Useful for LLMs to access current web information

## Comparison with Brave Search API

| Feature | SerpAPI | Brave Search API |
|---------|---------|------------------|
| Source | Google results | Brave index |
| Freshness | Real-time | Real-time |
| Privacy | Standard Google | Privacy-focused |
| Coverage | Google's index | Brave's independent index |
| Cost | Free tier available | Free tier available |
| Use case | Latest trends, Google-specific results | Privacy-focused search |

Both APIs complement each other - use SerpAPI for Google-specific results and maximum coverage, use Brave Search for privacy-focused alternative search.
