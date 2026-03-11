---
name: web-scraper
description: "Extract structured data from websites. Use when: collecting competitor pricing; scraping product listings; extracting contact information; gathering research data; monitoring website changes"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Web Scraper

> Extract structured data from websites using BeautifulSoup and requests - turn any webpage into usable data.

## When to Use This Skill

- **Competitor research** - Scrape pricing, features, positioning
- **Lead generation** - Extract contact info from directories
- **Content audit** - Pull headings, links, meta data
- **Price monitoring** - Track competitor pricing changes
- **Data collection** - Gather research data from multiple sources


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures analysis frameworks | Strategic priorities |
| Synthesizes market data | Competitive positioning |
| Identifies opportunities | Resource allocation |
| Creates strategic options | Final strategy selection |
| Suggests implementation approaches | Execution decisions |

## Dependencies

```bash
pip install beautifulsoup4 requests pandas click lxml
```

## Commands

### Scrape Elements
```bash
python scripts/main.py scrape https://example.com --selector "h1,h2,p"
python scripts/main.py scrape https://example.com --selector ".product-price"
```

### Extract Links
```bash
python scripts/main.py links https://example.com
python scripts/main.py links https://example.com --internal-only
```

### Extract Emails
```bash
python scripts/main.py emails https://example.com
python scripts/main.py emails https://example.com --depth 2
```

### Extract Structured Data
```bash
python scripts/main.py structured https://example.com/article --schema article
python scripts/main.py structured https://example.com/product --schema product
```

## Examples

### Example 1: Scrape Competitor Pricing
```bash
python scripts/main.py scrape https://competitor.com/pricing --selector ".price,.plan-name"

# Output:
# Extracted 6 elements
# 1. Starter - $29/mo
# 2. Pro - $99/mo
# 3. Enterprise - Contact us
```

### Example 2: Extract Article Content
```bash
python scripts/main.py structured https://blog.example.com/post --schema article

# Output: article_data.json
# {
#   "title": "How to Scale Your Startup",
#   "author": "Jane Doe",
#   "date": "2024-01-15",
#   "content": "...",
#   "word_count": 1523
# }
```

## CSS Selector Reference

| Selector | Description | Example |
|----------|-------------|---------|
| `tag` | Element type | `h1`, `p`, `div` |
| `.class` | Class name | `.price`, `.title` |
| `#id` | Element ID | `#main-content` |
| `tag.class` | Tag with class | `div.product` |
| `tag[attr]` | Has attribute | `a[href]` |
| `parent > child` | Direct child | `ul > li` |
| `tag1, tag2` | Multiple | `h1, h2, h3` |

## Ethical Scraping Guidelines

1. **Check robots.txt** - Respect site's scraping policy
2. **Rate limit** - Don't overload servers (1-2 req/sec)
3. **Identify yourself** - Use descriptive User-Agent
4. **Cache requests** - Don't re-scrape unchanged pages
5. **Terms of Service** - Check if scraping is allowed

## Skill Boundaries

### What This Skill Does Well
- Structuring strategic analysis
- Identifying market opportunities
- Creating strategic frameworks
- Synthesizing competitive data

### What This Skill Cannot Do
- Replace market research
- Guarantee strategic success
- Know proprietary competitor info
- Make executive decisions

## Related Skills

- [competitor-monitor](../competitor-monitor/) - Monitor competitor changes
- [pdf-extractor](../pdf-extractor/) - Extract from PDFs

## Skill Metadata


- **Mode**: centaur
```yaml
category: automation
subcategory: data-extraction
dependencies: [beautifulsoup4, requests, pandas]
difficulty: intermediate
time_saved: 5+ hours/week
```
