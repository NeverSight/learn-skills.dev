---
name: web-search
description: Web search capability using DuckDuckGo API by default, with Tavily API fallback when TRAVILY_TOKEN is provided. Use when you need to search the web for current information, research topics, find URLs, or gather data from online sources. Supports queries for news, technical information, research papers, company data, and general web content.
---

# Web Search

## Quick Start

Search the web using the included script:

```bash
python3 /skills/web-search/scripts/web_search.py "your search query" [max_results]
```

**Example:**
```bash
python3 /skills/web-search/scripts/web_search.py "latest AI research" 5
```

## Search Methods

### DuckDuckGo API (Default)
- **No setup required** - works out of the box
- Uses DuckDuckGo's Instant Answer API
- Returns structured results with titles and URLs
- Good for general searches and research

### Tavily API (Premium)
- **Setup required** - set `TRAVILY_TOKEN` environment variable
- Higher quality results with direct answers
- Better for complex queries and research
- Structured JSON response with content snippets

**To use Tavily:**
```bash
export TRAVILY_TOKEN="your-tavily-api-token"
python3 /skills/web-search/scripts/web_search.py "your query"
```

## Output Format

Both methods return JSON:
```json
[
  {
    "title": "Result Title",
    "url": "https://example.com",
    "content": "Optional content (Tavily only)"
  }
]
```

## Use Cases

- **Research**: Find current information on topics
- **URL Discovery**: Find relevant websites and resources
- **Fact Checking**: Verify information from multiple sources
- **Technical Documentation**: Find official docs and references
- **News & Updates**: Get current events and developments

## Integration with Scripts

The web search can be integrated into other scripts:

```python
import subprocess
import json

def search_and_extract(query, max_results=5):
    result = subprocess.run(
        ['python3', '/skills/web-search/scripts/web_search.py', query, str(max_results)],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)
```

## Resources

- **Script**: `/skills/web-search/scripts/web_search.py` - Main search script
- **Reference**: `/skills/web-search/references/search_methods.md` - Detailed method documentation
