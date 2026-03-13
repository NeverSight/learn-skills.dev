---
name: searxng-search
description: "Search the web using a self-hosted SearXNG instance. Use when users ask to search with SearXNG, or when web search is needed and a SearXNG instance is configured. Supports categories, engines, time range, and language filters."
allowed-tools:
  - Bash(python3:*)
---

# SearXNG Search Skill

Search the web using a SearXNG instance via its API.

## Configuration

The config file is read from `$XDG_CONFIG_HOME/agents/searxng.json` (defaults to `~/.config/agents/searxng.json`).

### Config fields

| Field | Type | Required | Description |
|---|---|---|---|
| `base_url` | `string` | **Yes** | SearXNG instance URL (no trailing slash) |
| `auth` | `object` | No | Auth config object (see below) |
| `auth.type` | `string` | If auth | `"bearer"` or `"basic"` |
| `auth.token` | `string` | If bearer | Bearer token value (supports `$ENV_VAR`) |
| `auth.user` | `string` | If basic | Basic auth username |
| `auth.pass` | `string` | If basic | Basic auth password |
| `headers` | `object` | No | Key-value pairs of additional HTTP headers |
| `default_language` | `string` | No | Default language code (e.g. `"en"`, `"zh-CN"`) |
| `default_categories` | `string[]` | No | Default categories (e.g. `["general", "news"]`) |
| `default_engines` | `string[]` | No | Default engines (e.g. `["google", "duckduckgo"]`) |
| `default_safesearch` | `number` | No | Default safe search level: `0`, `1`, `2` |
| `default_time_range` | `string` | No | Default time range: `"day"`, `"month"`, `"year"` |
| `default_max_results` | `number` | No | Max results to display (default: `5`) |
| `timeout` | `number` | No | Request timeout in seconds (default: `30`) |

### Example config (Bearer auth)

```json
{
  "base_url": "https://searx.example.com",
  "auth": {
    "type": "bearer",
    "token": "your-token-here"
  },
  "default_categories": ["general"],
  "default_engines": ["google", "duckduckgo", "brave"],
  "default_max_results": 10,
  "headers": {
    "X-Custom-Header": "value"
  }
}
```

### Example config (Basic auth)

```json
{
  "base_url": "https://searx.example.com",
  "auth": {
    "type": "basic",
    "user": "admin",
    "pass": "password"
  },
  "default_safesearch": 1
}
```

## Usage

Run the search script:

```bash
python3 scripts/search.py [OPTIONS] <query>
```

### Options

| Flag | Description |
|---|---|
| `-c, --categories` | Comma-separated categories (`general`, `news`, `images`, `videos`, `music`, `files`, `it`, `science`, `social media`) |
| `-e, --engines` | Comma-separated engines (`google`, `duckduckgo`, `bing`, etc.) |
| `-l, --language` | Language code (`en`, `zh-CN`, `ja`, etc.) |
| `-p, --page` | Page number (default: 1) |
| `-t, --time-range` | Time range: `day`, `month`, `year` |
| `-n, --max-results` | Max results to show (overrides config default) |
| `-s, --safesearch` | Safe search: `0` (off), `1` (moderate), `2` (strict) |

### Examples

```bash
# Basic search
python3 scripts/search.py "SearXNG documentation"

# Search news from the last day
python3 scripts/search.py -c news -t day "latest tech news"

# Search with specific engines, page 2
python3 scripts/search.py -e google,duckduckgo -p 2 "rust programming"

# Search in Chinese with more results
python3 scripts/search.py -l zh-CN -n 10 "开源搜索引擎"
```

## Workflow

1. User asks to search for something
2. Run `scripts/search.py` with the query and any relevant filters
3. Present results to the user in a readable format
4. If user wants more results, use `-p` for pagination or `-n` for more per page
