---
name: web-scraper
description: "Fetch any URL and extract clean readable content as text or markdown. Use this skill when the user asks to scrape a webpage, extract text from a URL, fetch website content, read an article from a link, or download webpage content."
tags: [web, scraper, url, fetch, extract, article, html, utility]
version: 0.1.0
---

# Skill: web-scraper

## When to Use

Use this skill when the user asks to:

- Scrape or fetch content from a URL
- Extract text from a webpage
- Read an article from a link
- Get the content of a website
- Download and convert a webpage to text/markdown
- Summarize a web page

## Input Parameters

| Parameter | Required | Description                                         | Example                     |
| --------- | -------- | --------------------------------------------------- | --------------------------- |
| `url`     | Yes      | URL to scrape                                       | https://example.com/article |
| `format`  | No       | Output format: `markdown` (default), `text`, `html` | markdown                    |
| `output`  | No       | Save output to file path                            | article.md                  |

## Procedure

1. Get the URL from the user's request
2. Run the bundled script:

   ```bash
   # Fetch and extract as markdown (default)
   python3 skills/web-scraper/scripts/scrape.py "https://example.com/article"

   # Extract as plain text
   python3 skills/web-scraper/scripts/scrape.py "https://example.com" --format text

   # Save to file
   python3 skills/web-scraper/scripts/scrape.py "https://example.com" --output article.md
   ```

3. The script auto-installs `trafilatura` and `requests` if needed
4. Present the extracted content to the user

## Bundled Scripts

| Script              | Type   | Description                         |
| ------------------- | ------ | ----------------------------------- |
| `scripts/scrape.py` | Python | Fetch URL and extract clean content |

### Script Usage

```bash
# Extract article content as markdown
python3 scripts/scrape.py "https://example.com/blog-post"

# Extract as plain text
python3 scripts/scrape.py "https://example.com" --format text

# Keep raw HTML
python3 scripts/scrape.py "https://example.com" --format html

# Save to file
python3 scripts/scrape.py "https://example.com" --output page.md

# Include metadata (title, author, date)
python3 scripts/scrape.py "https://example.com/article" --metadata
```

## Example

```
scrape this URL: https://example.com/article
extract the text from this webpage
fetch the content of this link and save it
read this article: https://blog.example.com/post-1
get the content from this website
```
