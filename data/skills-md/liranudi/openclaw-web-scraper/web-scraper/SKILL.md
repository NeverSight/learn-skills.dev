---
name: web-scraper
description: Search the web and read page contents without API keys. Use when you need to search via DuckDuckGo/Brave/Google (multi-page), extract readable text from URLs, browse interactively with a persistent visible browser (with tabs, click, screenshot, text search), download files/PDFs, or dismiss cookie banners. Supports JSON/markdown/text output. Powered by Playwright + Chromium.
---

# Web Scraper

Four scripts, zero API keys. All output is JSON by default.

**Dependencies:** `requests`, `beautifulsoup4`, `playwright` (with Chromium).
**Optional:** `pdfplumber` or `PyPDF2` for PDF text extraction.

Install: `pip install requests beautifulsoup4 playwright && playwright install chromium`

## 1. Search the Web

```bash
python3 scripts/google_search.py "query" --pages N --engine ENGINE
```

- `--engine` — `duckduckgo` (default), `brave`, or `google`
- Returns `[{title, url, snippet}, ...]`

## 2. Read a Page (one-shot)

```bash
python3 scripts/read_page.py "https://url" [--max-chars N] [--visible] [--format json|markdown|text] [--no-dismiss]
```

- `--format` — `json` (default), `markdown`, or `text`
- Auto-dismisses cookie consent banners (skip with `--no-dismiss`)

## 3. Persistent Browser Session

```bash
python3 scripts/browser_session.py open "https://url"              # Open + extract
python3 scripts/browser_session.py navigate "https://other"        # Go to new URL
python3 scripts/browser_session.py extract [--format FMT]          # Re-read page
python3 scripts/browser_session.py screenshot [path] [--full]      # Save screenshot
python3 scripts/browser_session.py click "Submit"                  # Click by text/selector
python3 scripts/browser_session.py search "keyword"                # Search text in page
python3 scripts/browser_session.py tab new "https://url"           # Open new tab
python3 scripts/browser_session.py tab list                        # List all tabs
python3 scripts/browser_session.py tab switch 1                    # Switch to tab index
python3 scripts/browser_session.py tab close [index]               # Close tab
python3 scripts/browser_session.py dismiss-cookies                 # Manually dismiss cookies
python3 scripts/browser_session.py close                           # Close browser
```

- Cookie consent auto-dismissed on open/navigate
- Multiple tabs supported — open, switch, close independently
- Search returns matching lines with line numbers
- Extract supports json/markdown/text output

## 4. Download Files

```bash
python3 scripts/download_file.py "https://example.com/doc.pdf" [--output DIR] [--filename NAME]
```

- Auto-detects filename from URL/headers
- PDFs: extracts text if pdfplumber/PyPDF2 installed
- Returns `{status, path, filename, size_bytes, content_type, extracted_text}`
