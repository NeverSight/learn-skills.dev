---
name: defuddle
description: >-
  Fetch readable text content from any URL using the defuddle.md service.
  Use this skill whenever you need to extract content from URLs that are
  difficult to fetch directly — such as x.com/twitter posts, pages behind
  JavaScript rendering, or sites that block standard fetchers. Also use it
  as a general fallback when WebFetch fails or returns unusable results.
  Trigger on: reading tweets/X posts, fetching article content from tricky
  domains, "grab the text from this link", or any URL where direct fetching
  is unreliable.
---

# Defuddle

Fetch readable web content as Markdown via the defuddle.md service.

## When to use

- **Hard-to-fetch domains**: x.com, twitter.com, sites with heavy JS rendering, anti-scraping protections, or paywalls
- **WebFetch fallback**: when WebFetch returns errors, empty content, or garbled output
- **General content extraction**: whenever you need clean, readable text from a URL

## How it works

defuddle.md is a public service that extracts the main content from a webpage and returns it as Markdown with YAML frontmatter.

```bash
curl -sL "defuddle.md/<url>"
```

The `<url>` is the target URL **without the protocol** (no `https://`).

## Examples

Fetch an article:
```bash
curl -sL "defuddle.md/example.com/blog/some-post"
```

Fetch a tweet / X post:
```bash
curl -sL "defuddle.md/x.com/username/status/123456789"
```

## Usage notes

- Always use `-sL` flags (silent mode + follow redirects)
- Strip `https://` or `http://` from the target URL before appending
- The response is Markdown text — you can use it directly or extract specific sections
- If the response is empty or an error page, the target site may not be supported; fall back to WebFetch or inform the user
