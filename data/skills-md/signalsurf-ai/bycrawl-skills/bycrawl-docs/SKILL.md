---
name: bycrawl-docs
description: "Fetch the latest ByCrawl API documentation from bycrawl.com. Use when working with ByCrawl API, Python SDK, or needing API reference for Threads, Instagram, Facebook, X/Twitter, Reddit, TikTok, LinkedIn, YouTube, Dcard, Job104."
allowed-tools: ["WebFetch"]
user-invocable: true
argument-hint: "<section> e.g. threads, python-sdk, getting-started"
---

# ByCrawl Documentation Fetcher

Fetch the latest documentation from bycrawl.com to ensure you have up-to-date API information.

## Documentation Pages

Base URL: `https://bycrawl.com/en/docs`

| Section | Path | Description |
|---------|------|-------------|
| Introduction | `/en/docs` | Overview, base URL, auth, quick examples |
| Getting Started | `/en/docs/getting-started` | Setup guide, API key, first request |
| Python SDK | `/en/docs/python-sdk` | SDK installation, methods, async, pagination |
| API Overview | `/en/docs/api-reference` | Endpoint patterns, common parameters |
| Threads | `/en/docs/api-reference/threads` | Threads API endpoints |
| Facebook | `/en/docs/api-reference/facebook` | Facebook API endpoints |
| X / Twitter | `/en/docs/api-reference/x` | X/Twitter API endpoints |
| Reddit | `/en/docs/api-reference/reddit` | Reddit API endpoints |
| Instagram | `/en/docs/api-reference/instagram` | Instagram API endpoints |
| TikTok | `/en/docs/api-reference/tiktok` | TikTok API endpoints |
| YouTube | `/en/docs/api-reference/youtube` | YouTube API endpoints |
| LinkedIn | `/en/docs/api-reference/linkedin` | LinkedIn API endpoints |
| Dcard | `/en/docs/api-reference/dcard` | Dcard API endpoints |
| Job104 | `/en/docs/api-reference/job104` | Job104 API endpoints |
| Error Codes | `/en/docs/error-codes` | Error codes and troubleshooting |
| Limitations | `/en/docs/limitations` | Rate limits and constraints |
| Changelog | `/en/docs/changelog` | Version history and updates |

## Workflow

1. **Determine which page(s) to fetch based on the user's question:**
   - If user asks about a specific platform (e.g. "threads API") → fetch that platform's API reference page
   - If user asks about SDK usage → fetch the Python SDK page
   - If user asks about setup/auth → fetch Getting Started
   - If user asks about errors → fetch Error Codes
   - If unclear → fetch Introduction + the most relevant section
   - If user provides `$ARGUMENTS`, map it to the correct page path

2. **Fetch the docs page(s):**
   - Use `WebFetch` with URL `https://bycrawl.com/en/docs/{section}`
   - Extract all content including code examples, endpoint definitions, parameters, and response formats
   - Fetch up to 3 pages if the question spans multiple topics

3. **Present the documentation:**
   - Show the full API content with all code examples
   - Preserve parameter tables, response schemas, and example payloads
   - Note any version info, deprecations, or recent changes
   - Highlight information directly relevant to the user's question

## Output Format

```
# ByCrawl Docs - [Section Name]
Source: https://bycrawl.com/en/docs/[path]

[Full documentation content with code examples]
```

## Quick Reference

- Base API URL: `https://api.bycrawl.com`
- Auth header: `x-api-key: sk_byc_...`
- Python SDK: `pip install bycrawl`
- MCP package: `@bycrawl/mcp`
- Common endpoint pattern: `GET /{platform}/users/{username}`, `GET /{platform}/posts/search?q=keyword`
