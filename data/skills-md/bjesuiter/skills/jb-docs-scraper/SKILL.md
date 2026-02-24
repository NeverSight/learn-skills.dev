---
name: jb-docs-scraper
description: Scrape documentation websites into local markdown files for AI context. Takes a base URL and crawls the documentation, storing results in ./docs (or custom path). Uses crawl4ai with BFS deep crawling.
---

# Documentation Scraper

Scrape any documentation website into local markdown files. Uses `crawl4ai` for async web crawling.

## Quick Start

```bash
# Scrape any documentation URL
uv run --with crawl4ai python ./references/scrape_docs.py <URL>

# Examples
uv run --with crawl4ai python ./references/scrape_docs.py https://mediasoup.org/documentation/v3/
uv run --with crawl4ai python ./references/scrape_docs.py https://docs.rombo.co/tailwind
```

Output goes to `./docs/<auto-detected-name>/` by default.

## Prerequisites (First Time Only)

```bash
uv run --with crawl4ai playwright install
```

## Usage

```bash
uv run --with crawl4ai python ./references/scrape_docs.py <URL> [OPTIONS]
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `-o, --output PATH` | Output directory | `./docs/<auto-detected-name>` |
| `--max-depth N` | Maximum link depth | `6` |
| `--max-pages N` | Maximum pages to scrape | `500` |
| `--url-pattern PATTERN` | URL filter (glob) | Auto-detected |
| `-q, --quiet` | Suppress verbose output | `False` |

### Examples

```bash
# Basic - scrape to ./docs/documentation_v3/
uv run --with crawl4ai python ./references/scrape_docs.py \
  https://mediasoup.org/documentation/v3/

# Custom output directory
uv run --with crawl4ai python ./references/scrape_docs.py \
  https://docs.rombo.co/tailwind \
  --output ./my-tailwind-docs

# Limit crawl scope
uv run --with crawl4ai python ./references/scrape_docs.py \
  https://tanstack.com/start/latest/docs/framework/react/overview \
  --max-pages 50 \
  --max-depth 3

# Custom URL pattern filter
uv run --with crawl4ai python ./references/scrape_docs.py \
  https://example.com/docs/api/v2/ \
  --url-pattern "*api/v2/*"
```

## How It Works

1. **Auto-detects** domain and URL pattern from the input URL
2. **Crawls** using BFS (breadth-first search) strategy
3. **Filters** to stay within the documentation section
4. **Converts** pages to clean markdown
5. **Saves** with directory structure mirroring the URL paths

## Output Structure

```
docs/<name>/
  index.md           # Root page
  getting-started.md
  api/
    overview.md
    client.md
  guides/
    installation.md
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `Playwright browser binaries are missing` | Run `uv run --with crawl4ai playwright install` |
| Empty output | Check if URL pattern matches actual doc URLs. Try `--url-pattern` |
| Missing pages | Increase `--max-depth` or `--max-pages` |
| Wrong pages scraped | Use stricter `--url-pattern` |

## Tips

1. **Test first** - Use `--max-pages 10` to verify config before full crawl
2. **Check output name** - Script auto-detects from URL path segments
3. **Rerun safe** - Files are overwritten, duplicates skipped
