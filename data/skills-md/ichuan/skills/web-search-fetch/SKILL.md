---
name: web-search-fetch
description: Web search and URL fetch for AI agents. Use when the user asks to search the web, find URLs, research a topic, or read/fetch/summarize a webpage as clean Markdown. The search backend is configurable and invisible to the caller; fetching uses plain HTTP plus a local HTML-to-Markdown converter with zero dependencies.
---

# Web Search & Fetch

Requires Python 3; no package installation is needed. Resolve `scripts/web.py` relative to this `SKILL.md` file. Use its absolute path and keep the working directory at the user's project so the project's `.env` is loaded:

```bash
python3 /path/to/web-search-fetch/scripts/web.py search "python 3.13 release notes" --limit 5
```

On Windows, use the equivalent path syntax:

```powershell
py C:\path\to\web-search-fetch\scripts\web.py search "python 3.13 release notes" --limit 5
```

The relative-path examples below assume the working directory is the skill directory, which contains this file.

The script has two subcommands:

- `search <query>` — web search, prints one JSON result per line: `{"url", "title", "snippet"}`
- `fetch <url>` — fetch a URL and print the page as Markdown (title and warnings go to stderr)

The user never needs to know which search backend is in use; both subcommands take plain queries/URLs.

## Search

- Output is NDJSON; each line is one result with `url`, `title`, `snippet`.
- `--limit N` caps the number of results (default 8, values clamped to 1–20). Search requests have a 30-second timeout per backend.
- The script selects the backend and handles quota fallback automatically. Do not call both backends yourself or repeat the query to combine their results.
- Successful results go to stdout; warnings and errors go to stderr. A failure exits nonzero. An empty successful response means no results; do not treat it as a quota error.

## Fetch

```bash
python3 scripts/web.py fetch https://www.example.com/news/story
```
- By default only the **main content** is kept: the converter locates the article body and drops navigation, share links, related/popular lists, promos, cookie banners and hidden elements. Headings, paragraphs, lists, code blocks, links, images and tables are preserved, and relative URLs are resolved against the final page URL.
- `--full` converts the whole page instead. Main-content extraction assumes an article-style page; on list/index pages (homepages, category feeds, link directories) it can prune the headline list too. If the output looks too short or is missing what you came for, judge from the content and retry once with `--full`.
- `--raw` skips HTML-to-Markdown conversion and prints the response body decoded as text (useful for HTML/JSON/plain-text endpoints). It does not preserve the original bytes and is not suitable for binary downloads; use an appropriate download tool for your environment.
- `--timeout N` (default 30s) and `--max-bytes N` (default 5 MB) bound the request.
- Conversion is done by the local `scripts/html2markdown.py` module (stdlib only, no pip install).

## JavaScript-rendered pages

Plain HTTP cannot run JavaScript. When `fetch` extracts almost no text it prints a `[warn]` line telling you the page likely needs JS rendering (the line also suggests `--full`). Try `--full` once; if the full page is also nearly empty, do not retry further — switch to the **agent-browser** skill and load the URL in a real browser instead.

## Configuration

Read from environment variables, falling back to a `.env` file in the current working directory:

```bash
# Brave (takes priority when a key is set)
BRAVE_API_KEY=your-key

# RustXNG: used when Brave is unconfigured or quota-limited
RUSTXNG_URL=https://search.example.com
# Optional; omit for instances without authentication
RUSTXNG_TOKEN=your-token
```

- Brave is preferred, using `BRAVE_API_KEY` or its legacy alias `WEBSEARCH_API_KEY`. If neither key is set, use `RUSTXNG_URL` directly. Empty values are ignored. `WEBSEARCH_PROVIDER` is no longer used.
- If Brave returns HTTP `429` (rate/quota limit) or `402` (payment/quota required), try RustXNG once when `RUSTXNG_URL` is configured. Emit a warning to stderr and return only RustXNG's results. Without a configured fallback, report the Brave failure.
- Other Brave errors (including `401`, `403`, connection failures and server errors) and empty results do not trigger fallback. RustXNG errors are final; never loop between backends or combine their results.
- `RUSTXNG_URL` is the instance base URL, optionally including a path prefix, without `/search`, query parameters or embedded credentials. Requests use `/search` with `format=json`; results keep the same `url`, `title`, `snippet` output format.
- `RUSTXNG_TOKEN`, when set, is sent only as `Authorization: Bearer <token>`. Use HTTPS for remote instances. Redirects are rejected to avoid forwarding credentials to another destination.

Fetch needs no configuration.
