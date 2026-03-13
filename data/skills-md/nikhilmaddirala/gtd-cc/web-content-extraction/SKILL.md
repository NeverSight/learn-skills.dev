---
name: web-content-extraction
description: Extract documentation and content from websites. Supports Mintlify, Starlight/Astro, Docusaurus, GitBook, ReadTheDocs, Sphinx, and generic sites. Uses a tiered approach - try the simplest method first (direct curl, Jina AI Reader) before falling back to Crawl4AI for JS-heavy sites.
version: 0.3.0
last_updated: 2025-02-01
---

# Content extraction

## Overview

This skill extracts documentation and website content as markdown files. It uses a tiered approach: try the simplest method first, fall back to heavier tools only when needed.


## Context

User provides a URL to extract content from. This skill is appropriate when:
- Extracting documentation sites (API docs, tutorials, reference guides)
- Crawling entire websites to markdown for offline reference
- Archiving websites or generating sitemaps
- Converting multi-page documentation to organized markdown


## Process

1. Discover all pages (llms.txt, sitemap XML, nav link extraction, or progressive crawling)
2. Detect platform to choose extraction method
3. Batch extract content using the simplest working method
4. Organize output and verify results


## Page discovery (ordered by preference)

Before extracting content, discover all pages on the site. Try these methods in order:

### Method 1: llms.txt

Some documentation platforms (notably Mintlify) serve an `llms.txt` file listing all pages:

```bash
# Check for llms.txt
curl -sL "https://example.com/docs/llms.txt" -o /tmp/llms.txt
head -20 /tmp/llms.txt

# Extract all URLs
grep -oE 'https://[^\s]+\.md' /tmp/llms.txt
```

This is the most reliable method when available. It gives you every page URL immediately.

### Method 2: sitemap XML

Most documentation sites have a sitemap:

```bash
# Check common sitemap locations
curl -sL "https://example.com/sitemap.xml" | head -20
curl -sL "https://example.com/sitemap-index.xml" | head -20
curl -sL "https://example.com/docs/sitemap-index.xml" | head -20
curl -sL "https://example.com/docs/sitemap-0.xml" | head -20

# Extract all URLs from sitemap
curl -sL "https://example.com/sitemap-0.xml" | grep -oE 'https://[^<]+' | sort
```

Starlight/Astro sites reliably have sitemaps. Look for `<link rel="sitemap">` in the HTML source.

### Method 3: Jina AI Reader nav extraction

Use Jina to render the page and extract sidebar/nav links:

```bash
curl -sL "https://r.jina.ai/https://example.com/docs/" -o /tmp/nav.md
grep -oE '/docs/[a-z0-9/-]+' /tmp/nav.md | sort -u
```

### Method 4: progressive crawling (Crawl4AI)

For sites where the above methods fail, use Crawl4AI to discover pages by following links. See the "Advanced: Crawl4AI" section below.


## Platform detection and extraction

### Mintlify sites (Anthropic, Stripe, many API docs)

Mintlify serves raw markdown when you append `.md` to any page URL. This is the ideal case: zero dependencies, clean output, no nav/footer noise.

**Detection:**
- `llms.txt` exists
- Appending `.md` to a URL returns markdown (not HTML)

**Extraction:**
```bash
# Test: does the .md URL return markdown?
curl -sL "https://example.com/docs/en/overview.md" | head -5

# If it starts with markdown (# heading, etc.), use direct curl for all pages:
OUT="./output"
mkdir -p "$OUT"

pages=(overview quickstart setup cli-reference)  # from llms.txt

for page in "${pages[@]}"; do
  curl -sL "https://example.com/docs/en/${page}.md" -o "${OUT}/${page}.md" &
done
wait

# Verify
ls -1 "$OUT" | wc -l
find "$OUT" -name "*.md" -size 0  # check for empty files
du -sh "$OUT"
```

### Starlight/Astro sites (OpenCode, many OSS projects)

Starlight renders HTML server-side. Use Jina AI Reader to convert to markdown.

**Detection:**
- HTML contains `Starlight` or `astro` in meta tags / generator
- Has `sitemap-index.xml`

**Extraction:**
```bash
# Discover pages via sitemap
curl -sL "https://example.com/docs/sitemap-0.xml" | grep -oE 'https://[^<]+' > /tmp/urls.txt

OUT="./output"
mkdir -p "$OUT"

# Batch download via Jina (rate limit: max 5 concurrent)
while read url; do
  slug=$(echo "$url" | sed 's|.*/docs/||; s|/$||; s|/|-|g')
  [ -z "$slug" ] && slug="index"
  curl -sL "https://r.jina.ai/${url}" -o "${OUT}/${slug}.md" &

  running=$(jobs -r | wc -l)
  if [ "$running" -ge 5 ]; then
    wait -n
  fi
done < /tmp/urls.txt
wait
```

Note: Jina output includes nav/sidebar noise. For reference docs this is acceptable. For cleaner output, use Crawl4AI with CSS selectors.

### Docusaurus, GitBook, ReadTheDocs, Sphinx

These platforms render HTML. Use Jina as the first attempt; fall back to Crawl4AI if Jina output is too noisy.

**Platform-specific CSS selectors (for Crawl4AI fallback):**

| Platform | Content selector | Exclude |
|----------|-----------------|---------|
| Docusaurus | `article, .markdown, .theme-doc-markdown` | `nav, footer, .pagination, .table-of-contents` |
| GitBook | `.gitbook-root, .page-body, .theme-doc` | `nav, header, .sidebar, .navigation` |
| ReadTheDocs | `.document, .role-content, .bd-content` | `nav, .sidebar, .toctree, .related-topics` |
| Sphinx | `.document, .body, .section` | `nav, .related, .sphinxsidebar, .toctree-wrapper` |

### Generic sites

Try methods in this order:
1. Check for `llms.txt` or `.md` URL suffix
2. Check for sitemap XML
3. Use Jina AI Reader
4. Fall back to Crawl4AI


## Complete workflow examples

### Example 1: Mintlify docs (simplest case)

```bash
# 1. Discover pages
curl -sL "https://code.claude.com/docs/llms.txt" -o /tmp/llms.txt
grep -oE 'https://[^\s]+\.md' /tmp/llms.txt > /tmp/urls.txt

# 2. Extract page names
sed 's|.*/en/||; s|\.md||' /tmp/urls.txt > /tmp/pages.txt

# 3. Batch download
OUT="./claude-code-docs"
mkdir -p "$OUT"

while read page; do
  curl -sL "https://code.claude.com/docs/en/${page}.md" -o "${OUT}/${page}.md" &
done < /tmp/pages.txt
wait

# 4. Verify
echo "$(ls -1 "$OUT"/*.md | wc -l) files, $(du -sh "$OUT" | cut -f1)"
find "$OUT" -name "*.md" -size 0 -exec echo "EMPTY: {}" \;
```

### Example 2: Starlight/Astro docs (Jina approach)

```bash
# 1. Discover pages via sitemap
curl -sL "https://opencode.ai/docs/sitemap-index.xml"  # find sitemap URL
curl -sL "https://opencode.ai/docs/sitemap-0.xml" | grep -oE 'https://[^<]+' > /tmp/urls.txt

# 2. Batch download via Jina (throttled)
OUT="./opencode-docs"
mkdir -p "$OUT"

while read url; do
  slug=$(echo "$url" | sed 's|.*/docs/||; s|/$||; s|/|-|g')
  [ -z "$slug" ] && slug="index"
  curl -sL "https://r.jina.ai/${url}" -o "${OUT}/${slug}.md" &
  running=$(jobs -r | wc -l)
  [ "$running" -ge 5 ] && wait -n
done < /tmp/urls.txt
wait

# 3. Verify
echo "$(ls -1 "$OUT"/*.md | wc -l) files, $(du -sh "$OUT" | cut -f1)"
```

### Example 3: full site crawl to markdown (Crawl4AI)

For sites that need JavaScript rendering or where simpler methods fail:

```bash
# Quick CLI approach
uvx crawl4ai crawl \
  --url "https://example.com" \
  --output-dir "output/example-com-$(date +%Y%m%d-%H%M%S)" \
  --max-depth 3 \
  --format markdown
```

Python implementation for more control:

```python
import asyncio
import os
from pathlib import Path
from datetime import datetime
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from urllib.parse import urljoin, urlparse

async def crawl_to_markdown(base_url, output_dir, max_depth=3):
    """Crawl entire website and save as markdown files"""

    base_domain = urlparse(base_url).netloc
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    crawl_dir = Path(output_dir) / f"{base_domain}-{timestamp}"
    crawl_dir.mkdir(parents=True, exist_ok=True)

    visited = set()
    queue = [(base_url, 0)]

    async with AsyncWebCrawler() as crawler:
        while queue and len(visited) < 100:
            url, depth = queue.pop(0)

            if url in visited or depth > max_depth:
                continue

            try:
                result = await crawler.arun(
                    url,
                    config=CrawlerRunConfig(
                        page_timeout=30000,
                        remove_overlay_elements=True
                    )
                )

                if result.success:
                    path = urlparse(url).path
                    if path.endswith('/') or path == '':
                        path = path + 'index.md'
                    else:
                        path = path + '.md' if not path.endswith('.md') else path

                    output_file = crawl_dir / path.lstrip('/')
                    output_file.parent.mkdir(parents=True, exist_ok=True)

                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(f"# {result.metadata.get('title', 'Page')}\n\n")
                        f.write(str(result.markdown))

                    visited.add(url)

                    for link_info in result.links.get("internal", []):
                        href = link_info.get("href", "")
                        absolute_url = urljoin(base_url, href)
                        if (absolute_url not in visited and
                            not absolute_url.startswith('#') and
                            absolute_url.startswith(base_url)):
                            queue.append((absolute_url, depth + 1))

            except Exception as e:
                print(f"Failed: {url}: {e}")

    print(f"Done: {len(visited)} pages saved to {crawl_dir}")
    return crawl_dir
```


## Advanced: Crawl4AI patterns

### Universal documentation extraction

For sites where simple methods fail, use Crawl4AI with platform-aware selectors:

```python
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig

async def extract_documentation(url):
    """Universal documentation extractor with platform detection"""

    content_selectors = [
        "article", ".markdown", ".theme-doc-markdown",
        ".gitbook-root", ".document", ".bd-content",
        ".page-body", ".role-content", ".section",
        ".main-content", "[role='main']"
    ]

    config = CrawlerRunConfig(
        css_selector=", ".join(content_selectors),
        wait_for="css:article, .markdown, .document, [role='main']",
        remove_overlay_elements=True,
        exclude_tags=[
            "nav", "header", "footer",
            ".sidebar", ".navigation", ".menu",
            ".table-of-contents", ".toc",
            ".pagination", ".breadcrumbs",
            "script", "style", "noscript"
        ],
        page_timeout=45000
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url, config=config)
        if result.success:
            return str(result.markdown)
```

### Relevance-based filtering

```python
from crawl4ai.content_filter_strategy import BM25ContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

async def extract_relevant_docs(url, focus_area):
    """Extract documentation focused on specific topics"""

    bm25_filter = BM25ContentFilter(
        user_query=focus_area,
        bm25_threshold=1.2,
        include_tables=True,
        include_code=True
    )

    md_generator = DefaultMarkdownGenerator(
        content_filter=bm25_filter,
        options={
            "ignore_links": False,
            "ignore_images": False,
            "code_block_format": "fenced"
        }
    )

    config = CrawlerRunConfig(
        css_selector="article, .document, .markdown",
        markdown_generator=md_generator
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url, config=config)
        return str(result.markdown.fit_markdown)
```

### Batch extraction with concurrency

```python
async def extract_complete_docs(urls, max_concurrent=3):
    """Extract multiple pages concurrently"""

    config = CrawlerRunConfig(
        css_selector="article, .document, .markdown",
        remove_overlay_elements=True,
        page_timeout=30000
    )

    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun_many(
            urls=urls,
            config=config,
            max_concurrent=max_concurrent
        )

        extracted = {}
        for result in results:
            if result.success:
                extracted[result.url] = str(result.markdown)

        return extracted
```

### API documentation extraction

```python
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

schema = {
    "name": "api_endpoints",
    "baseSelector": ".api-endpoint, .method, .endpoint",
    "fields": [
        {"name": "method", "selector": ".http-method, .verb", "type": "text"},
        {"name": "path", "selector": ".path, .route", "type": "text"},
        {"name": "description", "selector": ".description", "type": "text"},
        {"name": "parameters", "selector": ".parameters", "type": "text"},
        {"name": "example", "selector": ".example, .code-example", "type": "text"}
    ]
}

async def extract_api_docs(url):
    extraction_strategy = JsonCssExtractionStrategy(schema=schema)
    config = CrawlerRunConfig(
        css_selector=".api-reference, .endpoints, .methods",
        extraction_strategy=extraction_strategy
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url, config=config)
        return result.extracted_content
```


## Advanced: intelligent crawling

For sites that require link-following discovery (no sitemap, no llms.txt):

```python
class IntelligentCrawler:
    def __init__(self, base_url, max_depth=5, max_pages=100):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.visited = set()
        self.queue = [(base_url, 0)]

    async def crawl(self):
        """Crawl with intelligent depth control and link prioritization"""

        async with AsyncWebCrawler() as crawler:
            while self.queue and len(self.visited) < self.max_pages:
                url, depth = self.queue.pop(0)

                if url in self.visited or depth > self.max_depth:
                    continue

                config = CrawlerRunConfig(
                    page_timeout=30000,
                    remove_overlay_elements=True,
                    exclude_tags=["script", "style", "nav", "footer"]
                )

                try:
                    result = await crawler.arun(url, config=config)
                    if result.success:
                        self.visited.add(url)
                        yield url, str(result.markdown), result.metadata

                        for link_info in result.links.get("internal", []):
                            href = link_info.get("href", "")
                            if self._is_valid(href):
                                absolute = urljoin(self.base_url, href)
                                if absolute not in self.visited:
                                    priority = self._priority(href, link_info)
                                    self.queue.append((absolute, depth + 1))

                except Exception as e:
                    print(f"Failed: {url}: {e}")

                await asyncio.sleep(1)

    def _is_valid(self, href):
        if href.startswith(('#', 'mailto:', 'tel:', 'javascript:')):
            return False
        skip = ['.pdf', '.jpg', '.png', '.gif', '.zip', '.exe']
        return not any(href.lower().endswith(ext) for ext in skip)

    def _priority(self, href, link_info):
        text = (href + link_info.get("text", "")).lower()
        if any(kw in text for kw in ["docs", "guide", "tutorial", "api"]):
            return 10
        return 5
```


## Sitemap generation

After crawling, generate a sitemap for navigation:

```python
def create_markdown_sitemap(pages, base_url):
    """Generate markdown sitemap from crawled pages"""
    lines = [f"# Sitemap for {base_url}\n"]
    for url, title in sorted(pages.items()):
        depth = url.replace(base_url, '').count('/')
        indent = "  " * depth
        lines.append(f"{indent}- [{title or url}]({url})")
    return "\n".join(lines)
```


## Guidelines

- Always try the simplest extraction method first (direct curl > Jina > Crawl4AI)
- Check for `llms.txt` and sitemap XML before crawling
- Use parallel `curl` with `&` + `wait` for batch downloads (no tokens wasted in agent context)
- Throttle Jina requests to max 5 concurrent
- For Crawl4AI, use `arun_many()` with `max_concurrent=3` for multi-page docs
- Add delays between requests when crawling large sites
- Always verify downloads: check file count, empty files, and total size
- Maintain heading hierarchy and code block formatting
