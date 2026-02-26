---
name: nanoserp
description: "Free web search and page scraping via DuckDuckGo. Use when the agent needs to search the web for information, fetch and read webpage contents, or gather links from a page. Triggers on tasks requiring web search, web scraping, URL fetching, or internet research. No API keys or accounts needed."
---

# nanoserp

A zero-config CLI and Python library for web search and page scraping via DuckDuckGo. No API keys required.

## Setup

Install with pip (requires Python 3.11+):

```bash
pip install nanoserp
```

Or run directly without installing via `uvx`:

```bash
uvx nanoserp search "query"
```

## CLI Usage

The CLI is invoked with `nanoserp` (or `uvx nanoserp` if not installed).

### Search

```bash
nanoserp search "query"
nanoserp search "query" --date-filter w      # d=day, w=week, m=month, y=year
nanoserp search "query" --offset 10          # pagination
```

Output: numbered list of results with title, URL, date (if available), and snippet.

### Scrape

```bash
nanoserp scrape "https://example.com"
```

Output: page content as markdown, followed by a list of extracted links.

## Python Library Usage

```python
from nanoserp import search, scrape, DateFilter

# Search
response = search("python web scraping")
for r in response.results:
    print(r.title, r.url, r.snippet)

# Search with date filter and pagination
page1 = search("query", date_filter=DateFilter.WEEK)
page2 = search("query", offset=len(page1.results), vqd=page1.vqd)

# Scrape
page = scrape("https://example.com")
print(page.markdown)
for link in page.links:
    print(link.text, link.url)
```

### Function Signatures

```python
search(query: str, *, offset: int = 0, date_filter: DateFilter | None = None,
       vqd: str | None = None, timeout: float = 10.0) -> SearchResponse

scrape(url: str, *, timeout: float = 10.0) -> ScrapeResponse
```

### Models

- **SearchResponse**: `query`, `results: list[SearchResult]`, `vqd: str | None`
- **SearchResult**: `title`, `url`, `snippet`, `date: datetime | None`
- **ScrapeResponse**: `url`, `markdown`, `links: list[ScrapeLink]`
- **ScrapeLink**: `text`, `url`
- **DateFilter**: `DAY`, `WEEK`, `MONTH`, `YEAR`

### Error Handling

All exceptions inherit from `NanoserpError` (with `.message` attribute). The most common is `RateLimitError` (HTTP 429) when DuckDuckGo throttles requests.

```python
from nanoserp.exceptions import RateLimitError, NanoserpError

try:
    result = search("test")
except RateLimitError:
    # back off and retry
except NanoserpError as e:
    print(e.message)
```

## When to Use

- **Web search**: finding documentation, current information, or researching a topic
- **Page scraping**: reading webpage content, extracting links, fetching reference material
- **Combining both**: search to find relevant URLs, then scrape to read their content

## Tips

- Pass `vqd` from a previous `SearchResponse` when paginating to avoid redundant token requests.
- DuckDuckGo may rate-limit heavy use. Catch `RateLimitError` and back off.
- Scrape returns markdown, which is compact and easy to parse or summarize.
- The `--date-filter` flag is useful for finding recent information.
