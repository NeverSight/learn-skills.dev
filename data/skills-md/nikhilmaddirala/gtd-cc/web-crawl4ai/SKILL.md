---
name: web-crawl4ai
description: Complete Crawl4AI SDK reference and implementation guide. Use when users need to scrape websites, extract structured data, handle JavaScript-heavy pages, crawl multiple URLs, or build automated web data pipelines. Includes optimized extraction patterns, error handling, and comprehensive code examples.
version: 0.7.4
crawl4ai_version: ">=0.7.4"
last_updated: 2025-01-26
---

# Crawl4AI Toolkit

## Overview

This skill provides comprehensive support for web crawling and data extraction using Crawl4AI library, including complete SDK reference, ready-to-use scripts, error handling patterns, and optimized workflows for efficient data extraction.


## Context

User needs programmatic web crawling capabilities. This skill is appropriate when:
- Scraping websites with JavaScript rendering requirements
- Extracting structured data using CSS selectors or LLM extraction
- Building automated web data pipelines
- Handling login-protected or dynamic content


## Process

1. Verify crawl4ai installation with `crawl4ai-doctor`
2. Configure browser and crawler settings based on target site
3. Execute crawl using appropriate method (basic, batch, or advanced)
4. Process results (markdown, extracted data, links)
5. Handle errors with retry logic and exponential backoff
6. Verification: Confirm extracted content meets quality requirements


## Quick Start

### Installation Check
```bash
# Verify installation
crawl4ai-doctor

# If issues, run setup
crawl4ai-setup
```

### Basic First Crawl
```python
import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun("https://example.com")
        print(result.markdown[:500])  # First 500 chars

asyncio.run(main())
```

### Using Provided Scripts
```bash
# Simple markdown extraction
python scripts/basic_crawler.py https://example.com

# Batch processing
python scripts/batch_crawler.py urls.txt

# Data extraction
python scripts/extraction_pipeline.py --generate-schema https://shop.com "extract products"
```

## Core Crawling Fundamentals

### 1. Basic Crawling

Understanding of core components for any crawl:

```python
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

# Browser configuration (controls browser behavior)
browser_config = BrowserConfig(
    headless=True,  # Run without GUI
    viewport_width=1920,
    viewport_height=1080,
    user_agent="custom-agent"  # Optional custom user agent
)

# Crawler configuration (controls crawl behavior)
crawler_config = CrawlerRunConfig(
    page_timeout=30000,  # 30 seconds timeout
    screenshot=True,  # Take screenshot
    remove_overlay_elements=True  # Remove popups/overlays
)

# Execute crawl with arun()
async with AsyncWebCrawler(config=browser_config) as crawler:
    result = await crawler.arun(
        url="https://example.com",
        config=crawler_config
    )

    # CrawlResult contains everything
    print(f"Success: {result.success}")
    print(f"HTML length: {len(result.html)}")
    print(f"Markdown length: {len(result.markdown)}")
    print(f"Links found: {len(result.links)}")
```

### 2. Configuration Deep Dive

**BrowserConfig** - Controls browser instance:
- `headless`: Run with/without GUI
- `viewport_width/height`: Browser dimensions
- `user_agent`: Custom user agent string
- `cookies`: Pre-set cookies
- `headers`: Custom HTTP headers

**CrawlerRunConfig** - Controls each crawl:
- `page_timeout`: Maximum page load/JS execution time (ms)
- `wait_for`: CSS selector or JS condition to wait for (optional)
- `cache_mode`: Control caching behavior
- `js_code`: Execute custom JavaScript
- `screenshot`: Capture page screenshot
- `session_id`: Persist session across crawls

### 3. Content Processing

Basic content operations available in every crawl:

```python
result = await crawler.arun(url)

# Access extracted content
markdown = result.markdown  # Clean markdown
html = result.html  # Raw HTML
text = result.cleaned_html  # Cleaned HTML

# Media and links
images = result.media["images"]
videos = result.media["videos"]
internal_links = result.links["internal"]
external_links = result.links["external"]

# Metadata
title = result.metadata["title"]
description = result.metadata["description"]
```

## JavaScript-Heavy Content Handling

For sites that rely on JavaScript for content rendering:

```python
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

# Configure for JavaScript-heavy sites
browser_config = BrowserConfig(
    headless=True,
    viewport_width=1920,
    viewport_height=1080,
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
)

crawler_config = CrawlerRunConfig(
    page_timeout=60000,  # 60 seconds for JS loading
    wait_for="css:.main-content",  # Wait for specific element
    js_code="""
    // Scroll to trigger lazy loading
    window.scrollTo(0, document.body.scrollHeight);
    // Wait for any async content
    await new Promise(resolve => setTimeout(resolve, 2000));
    """,
    remove_overlay_elements=True
)

async def crawl_dynamic_content(url):
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url, config=crawler_config)
        return result.markdown
```

## Content Filtering

Focus on relevant content while ignoring navigation and footers:

```python
from crawl4ai.content_filter_strategy import BM25ContentFilter, PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

# Option 1: Relevance-based filtering
bm25_filter = BM25ContentFilter(
    user_query="product features documentation",
    bm25_threshold=1.0
)

# Option 2: Quality-based filtering
pruning_filter = PruningContentFilter(threshold=0.4, threshold_type="fixed")

md_generator = DefaultMarkdownGenerator(content_filter=bm25_filter)
config = CrawlerRunConfig(markdown_generator=md_generator)

async def extract_focused_content(url, query):
    # Update filter with user query
    bm25_filter.user_query = query
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url, config=config)
        return {
            "raw_content": str(result.markdown.raw_markdown),
            "focused_content": str(result.markdown.fit_markdown),
            "metadata": result.metadata
        }
```

## Markdown Generation

### Basic Markdown Extraction

Crawl4AI excels at generating clean, well-formatted markdown:

```python
# Simple markdown extraction
async with AsyncWebCrawler() as crawler:
    result = await crawler.arun("https://docs.example.com")

    # High-quality markdown ready for LLMs
    with open("documentation.md", "w") as f:
        f.write(result.markdown)
```

### Fit Markdown (Content Filtering)

Use content filters to get only relevant content:

```python
from crawl4ai.content_filter_strategy import PruningContentFilter, BM25ContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

# Option 1: Pruning filter (removes low-quality content)
pruning_filter = PruningContentFilter(threshold=0.4, threshold_type="fixed")

# Option 2: BM25 filter (relevance-based filtering)
bm25_filter = BM25ContentFilter(user_query="machine learning tutorials", bm25_threshold=1.0)

md_generator = DefaultMarkdownGenerator(content_filter=bm25_filter)

config = CrawlerRunConfig(markdown_generator=md_generator)

result = await crawler.arun(url, config=config)
# Access filtered content
print(result.markdown.fit_markdown)  # Filtered markdown
print(result.markdown.raw_markdown)  # Original markdown
```

### Markdown Customization

Control markdown generation with options:

```python
config = CrawlerRunConfig(
    # Exclude elements from markdown
    excluded_tags=["nav", "footer", "aside"],

    # Focus on specific CSS selector
    css_selector=".main-content",

    # Clean up formatting
    remove_forms=True,
    remove_overlay_elements=True,

    # Control link handling
    exclude_external_links=True,
    exclude_internal_links=False
)

# Custom markdown generation
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

generator = DefaultMarkdownGenerator(
    options={
        "ignore_links": False,
        "ignore_images": False,
        "image_alt_text": True
    }
)
```

## Data Extraction

### Schema-Based Extraction (Most Efficient)

For repetitive patterns, generate schema once and reuse:

```bash
# Step 1: Generate schema with LLM (one-time)
python scripts/extraction_pipeline.py --generate-schema https://shop.com "extract products"

# Step 2: Use schema for fast extraction (no LLM)
python scripts/extraction_pipeline.py --use-schema https://shop.com generated_schema.json
```

### Manual CSS/JSON Extraction

When you know the structure:

```python
schema = {
    "name": "articles",
    "baseSelector": "article.post",
    "fields": [
        {"name": "title", "selector": "h2", "type": "text"},
        {"name": "date", "selector": ".date", "type": "text"},
        {"name": "content", "selector": ".content", "type": "text"}
    ]
}

extraction_strategy = JsonCssExtractionStrategy(schema=schema)
config = CrawlerRunConfig(extraction_strategy=extraction_strategy)
```

### LLM-Based Extraction

For complex or irregular content:

```python
extraction_strategy = LLMExtractionStrategy(
    provider="openai/gpt-4o-mini",
    instruction="Extract key financial metrics and quarterly trends"
)
```

## Advanced Patterns

### Deep Crawling

Discover and crawl links from a page:

```python
# Basic link discovery
async with AsyncWebCrawler() as crawler:
    result = await crawler.arun(url)

    # Extract and process discovered links
    internal_links = result.links.get("internal", [])
    external_links = result.links.get("external", [])

    # Crawl discovered internal links
    for link in internal_links:
        if "/blog/" in link and "/tag/" not in link:  # Filter links
            sub_result = await crawler.arun(link)
            # Process sub-page

    # For advanced deep crawling, consider using URL seeding patterns
    # or custom crawl strategies (see complete-sdk-reference.md)
```

### Batch & Multi-URL Processing

Efficiently crawl multiple URLs:

```python
urls = ["https://site1.com", "https://site2.com", "https://site3.com"]

async with AsyncWebCrawler() as crawler:
    # Concurrent crawling with arun_many()
    results = await crawler.arun_many(
        urls=urls,
        config=crawler_config,
        max_concurrent=5  # Control concurrency
    )

    for result in results:
        if result.success:
            print(f"✅ {result.url}: {len(result.markdown)} chars")
```

### Session & Authentication

Handle login-required content:

```python
# First crawl - establish session and login
login_config = CrawlerRunConfig(
    session_id="user_session",
    js_code="""
    document.querySelector('#username').value = 'myuser';
    document.querySelector('#password').value = 'mypass';
    document.querySelector('#submit').click();
    """,
    wait_for="css:.dashboard"  # Wait for post-login element
)

await crawler.arun("https://site.com/login", config=login_config)

# Subsequent crawls - reuse session
config = CrawlerRunConfig(session_id="user_session")
await crawler.arun("https://site.com/protected-content", config=config)
```

### Dynamic Content Handling

For JavaScript-heavy sites:

```python
config = CrawlerRunConfig(
    # Wait for dynamic content
    wait_for="css:.ajax-content",

    # Execute JavaScript
    js_code="""
    // Scroll to load content
    window.scrollTo(0, document.body.scrollHeight);

    // Click load more button
    document.querySelector('.load-more')?.click();
    """,

    # Note: For virtual scrolling (Twitter/Instagram-style),
    # use virtual_scroll_config parameter (see docs)

    # Extended timeout for slow loading
    page_timeout=60000
)
```

### Anti-Detection & Proxies

Avoid bot detection:

```python
# Proxy configuration
browser_config = BrowserConfig(
    headless=True,
    proxy_config={
        "server": "http://proxy.server:8080",
        "username": "user",
        "password": "pass"
    }
)

# For stealth/undetected browsing, consider:
# - Rotating user agents via user_agent parameter
# - Using different viewport sizes
# - Adding delays between requests

# Rate limiting
import asyncio
for url in urls:
    result = await crawler.arun(url)
    await asyncio.sleep(2)  # Delay between requests
```

## Robust Crawling Template

```python
import asyncio
import random
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.content_filter_strategy import BM25ContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

async def robust_crawl(url, query=None, max_retries=3):
    """Robust crawling with retries and error handling"""

    for attempt in range(max_retries):
        try:
            # Randomize configuration for each attempt
            browser_config = BrowserConfig(
                headless=True,
                viewport_width=random.choice([1920, 1366, 1440]),
                viewport_height=random.choice([1080, 768, 900]),
                user_agent=random.choice([
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
                ])
            )

            # Add content filtering if query provided
            config = CrawlerRunConfig(
                page_timeout=45000,
                remove_overlay_elements=True
            )

            if query:
                bm25_filter = BM25ContentFilter(user_query=query, bm25_threshold=1.0)
                md_generator = DefaultMarkdownGenerator(content_filter=bm25_filter)
                config.markdown_generator = md_generator

            async with AsyncWebCrawler(config=browser_config) as crawler:
                result = await crawler.arun(url, config=config)

                if result.success and len(str(result.markdown)) > 100:
                    return {
                        "content": str(result.markdown),
                        "metadata": result.metadata,
                        "links": result.links,
                        "attempt": attempt + 1
                    }
                else:
                    print(f"Attempt {attempt + 1}: Insufficient content extracted")

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")

        # Exponential backoff
        if attempt < max_retries - 1:
            await asyncio.sleep(2 ** attempt)

    raise Exception(f"Failed to extract content after {max_retries} attempts")
```

## Common Use Cases

### Documentation to Markdown
```python
# Convert entire documentation site to clean markdown
async with AsyncWebCrawler() as crawler:
    result = await crawler.arun("https://docs.example.com")

    # Save as markdown for LLM consumption
    with open("docs.md", "w") as f:
        f.write(result.markdown)
```

### E-commerce Product Monitoring
```python
# Generate schema once for product pages
# Then monitor prices/availability without LLM costs
schema = load_json("product_schema.json")
products = await crawler.arun_many(product_urls,
    config=CrawlerRunConfig(extraction_strategy=JsonCssExtractionStrategy(schema)))
```

### News Aggregation
```python
# Crawl multiple news sources concurrently
news_urls = ["https://news1.com", "https://news2.com", "https://news3.com"]
results = await crawler.arun_many(news_urls, max_concurrent=5)

# Extract articles with Fit Markdown
for result in results:
    if result.success:
        # Get only relevant content
        article = result.fit_markdown
```

### Research & Data Collection
```python
# Academic paper collection with focused extraction
config = CrawlerRunConfig(
    fit_markdown=True,
    fit_markdown_options={
        "query": "machine learning transformers",
        "max_tokens": 10000
    }
)
```

## Performance Optimization

### Concurrent Crawling
For multiple URLs:

```python
urls = ["https://site1.com", "https://site2.com", "https://site3.com"]

async def crawl_multiple(urls, max_concurrent=3):
    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun_many(
            urls=urls,
            config=CrawlerRunConfig(page_timeout=30000),
            max_concurrent=max_concurrent
        )

        return [
            {"url": r.url, "content": str(r.markdown), "success": r.success}
            for r in results if r.success
        ]

results = asyncio.run(crawl_multiple(urls))
```

### Caching Strategy
Enable caching during development:

```python
from crawl4ai import CacheMode

config = CrawlerRunConfig(
    cache_mode=CacheMode.ENABLED,  # Cache successful requests
    excluded_tags=["script", "style"]  # Exclude unnecessary elements
)
```

## Error Handling & Troubleshooting

### Common Issues and Solutions

**1. Timeout Errors**
```python
# Increase timeout for slow sites
config = CrawlerRunConfig(
    page_timeout=90000,  # 90 seconds
    wait_for="js:document.readyState === 'complete'"
)
```

**2. Bot Detection**
```python
# Rotate user agents and add delays
import random
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
]

browser_config = BrowserConfig(
    headless=True,
    user_agent=random.choice(user_agents),
    viewport_width=f"{random.choice([1920, 1366, 1440])}",
    viewport_height=f"{random.choice([1080, 768, 900])}"
)

# Add delay between requests
await asyncio.sleep(random.uniform(1, 3))
```

**3. Content Not Loading**
```python
# Wait for specific content
config = CrawlerRunConfig(
    wait_for=[
        "css:.article-content",  # Wait for main content
        "js:window.mainContentLoaded"  # Wait for JS flag
    ],
    js_code="""
    // Trigger any lazy loading
    window.dispatchEvent(new Event('load'));
    """
)
```

**JavaScript not loading:**
```python
config = CrawlerRunConfig(
    wait_for="css:.dynamic-content",  # Wait for specific element
    page_timeout=60000  # Increase timeout
)
```

**Bot detection issues:**
```python
browser_config = BrowserConfig(
    headless=False,  # Sometimes visible browsing helps
    viewport_width=1920,
    viewport_height=1080,
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
)
# Add delays between requests
await asyncio.sleep(random.uniform(2, 5))
```

**Content extraction problems:**
```python
# Debug what's being extracted
result = await crawler.arun(url)
print(f"HTML length: {len(result.html)}")
print(f"Markdown length: {len(result.markdown)}")
print(f"Links found: {len(result.links)}")

# Try different wait strategies
config = CrawlerRunConfig(
    wait_for="js:document.querySelector('.content') !== null"
)
```

**Session/auth issues:**
```python
# Verify session is maintained
config = CrawlerRunConfig(session_id="test_session")
result = await crawler.arun(url, config=config)
print(f"Session ID: {result.session_id}")
print(f"Cookies: {result.cookies}")
```

## Guidelines

- Always check `result.success` before processing content
- Start with basic crawling - understand BrowserConfig, CrawlerRunConfig, and arun() before moving to advanced features
- Use markdown generation for documentation and content - Crawl4AI excels at clean markdown extraction
- Try schema generation first for structured data - 10-100x more efficient than LLM extraction
- Use appropriate timeouts - 30s for normal sites, 60s+ for JavaScript-heavy sites
- Enable caching during development with `cache_mode=CacheMode.ENABLED` to avoid repeated requests
- Implement retry logic with exponential backoff
- Add delays between requests to respect rate limits
- Filter content aggressively to focus on relevant information
- Reuse sessions for authenticated content instead of re-logging

## Resources

### scripts/
- **extraction_pipeline.py** - Three extraction approaches with schema generation
- **basic_crawler.py** - Simple markdown extraction with screenshots
- **batch_crawler.py** - Multi-URL concurrent processing

### examples/
- **basic-scraping.py** - Core scraping patterns
- **structured-data-extraction.py** - JSON extraction with CSS selectors

### references/
- **complete-sdk-reference.md** - Complete SDK documentation (23K words) with all parameters, methods, and advanced features

### tests/
- **test_basic_crawling.py** - Basic crawling patterns
- **test_advanced_patterns.py** - Advanced crawling scenarios
- **test_data_extraction.py** - Data extraction strategies
- **test_markdown_generation.py** - Markdown generation tests

---

For more details on any topic, refer to `references/complete-sdk-reference.md` which contains comprehensive documentation of all features, parameters, and advanced usage patterns.
