---
name: mrscraper-fetch
description: Retrieve a known public URL with MrScraper's Scraper API as HTML, Markdown, a screenshot, or a combination. Use for reading, summarizing, archiving, or analyzing a page and before local extraction; supports browser rendering, real-device routing, proxies, and retries. Use web search when no URL is known.
---

# Retrieve Page Content with MrScraper

Use `mrscraper scraper-api` whenever the user already has a public URL. Keep
using the saved response for summarization, comparison, transformation, and
structured output. Use [mrscraper](../mrscraper/SKILL.md) for installation,
authentication, account status, or command routing, and
[mrscraper-serp](../mrscraper-serp/SKILL.md) when discovery must happen first.

## Page Retrieval Context

The Scraper API retrieves public pages through MrScraper's
[page-fetching service](https://docs.mrscraper.com/docs/features/unblocker).
Browser rendering executes page JavaScript, geographic routing selects the
proxy country, selector waits let delayed content appear, and homepage
navigation visits the site root before the target.

Use it only for content the user is authorized to access and in accordance
with the site's access requirements.

Plan-token usage is based on runtime and bandwidth: one token per 30 seconds
and one token per 0.25 MB, rounded up per component. Resource blocking can
reduce bandwidth for text-focused pages. Retries stop when the request
succeeds, the retry limit is reached, or the running token total reaches the
token cap; the initial request always runs. See the
[Token Plan](https://docs.mrscraper.com/docs/getting-started/api-token) for the
complete calculation.

## Step 1 — Define the Outcome

Confirm the target URL and what the user wants from it:

- Read, summarize, cite, or inspect the page;
- Check whether specific text appears;
- Archive the page or capture a screenshot;
- Produce fields, JSON, tables, or other structured output with local logic;
- Load JavaScript-rendered or geo-sensitive content.

For many pages that share a layout, retrieve representative pages, define one
local extractor, retrieve the remaining pages, and run the extractor across
the saved responses.

## Step 2 — Retrieve the Page

The command sends `POST https://api.mrscraper.com/` with the target URL, retry
budget, and page-loading options. It requests HTML by default.

Save substantial responses inside the user's current project:

```bash
mkdir -p ./.mrscraper
mrscraper scraper-api "https://www.scrapethissite.com/pages/simple/" \
  > ./.mrscraper/scrapethissite-simple.json
```

Stdout contains a JSON envelope. Page content is in `data`:

```json
{
  "status_code": 200,
  "data": {
    "html": "<!DOCTYPE html>...",
    "markdown": null,
    "screenshot": null,
    "token_usage": 3,
    "runtime": 18.02,
    "retry_count": 0
  },
  "headers": {
    "x-status-code": "200",
    "token_usage": "3"
  }
}
```

`headers["x-status-code"]` is the target page's status. Extract one field when
only that representation is needed:

```bash
jq -r '.data.html' ./.mrscraper/scrapethissite-simple.json
```

Request Markdown instead of HTML for readable text:

```bash
mrscraper scraper-api "https://www.scrapethissite.com/pages/simple/" \
  --markdown --no-html | jq -r '.data.markdown'
```

A screenshot is a base64 JPEG and can be large. Write it to a file rather than
reading it into the conversation:

```bash
mrscraper scraper-api "https://www.scrapethissite.com/pages/simple/" \
  --screenshot --no-html > ./.mrscraper/simple-screenshot.json
jq -r '.data.screenshot' ./.mrscraper/simple-screenshot.json \
  | base64 --decode > ./.mrscraper/simple.jpg
```

Check the exit code before using the result. Progress and diagnostics appear on
stderr, so redirected stdout remains machine-readable.

## Step 3 — Choose Page-Loading Options

Omit both rendering flags to let the service choose: it falls back to a browser
automatically when needed. `--browser-rendering` forces a browser and
`--no-browser-rendering` disables it. `--screenshot` always uses a browser.

Real-device routing is independent of browser rendering. Use `--super` when
routing may be the problem:

```bash
mrscraper scraper-api "https://www.scrapethissite.com/pages/simple/" --super
```

Wait for a CSS selector when the required content appears later:

```bash
mrscraper scraper-api "https://www.scrapethissite.com/pages/ajax-javascript/#2015" \
  --browser-rendering \
  --wait-for-selector ".film"
```

Use geographic routing or homepage navigation when the target requires it:

```bash
mrscraper scraper-api "https://www.scrapethissite.com/pages/simple/" \
  --geo-code ID \
  --home-page
```

Bound resource use:

```bash
mrscraper scraper-api "https://www.scrapethissite.com/pages/ajax-javascript/#2015" \
  --block-resources \
  --max-retries 1 \
  --token-cap 10 \
  --timeout 60
```

### Parameters

| CLI parameter | Default | Request mapping | Use |
| --- | --- | --- | --- |
| `<url>` | required | Body `url` | Target page URL. |
| `--no-html` | HTML requested | Query `html=false` | Skip HTML content. |
| `--markdown` | off | Query `markdown=true` | Request Markdown content. |
| `--screenshot` | off | Query `screenshot=true` | Capture a base64 JPEG; forces browser rendering. |
| `--browser-rendering` / `--no-browser-rendering` | automatic | Query `browserRendering` | Force or disable browser rendering. |
| `--super` | off | Query `super=true` | Real-device routing, independent of browser rendering. |
| `--geo-code <code>` | `US` | Query `geoCode` | Proxy country, such as `US`, `ID`, or `SG`. |
| `--proxy-country <code>` | omitted | Query `proxyCountry` | Compatibility country option. |
| `--no-use-proxy` | proxy allowed | Query `useProxy=false` | Do not use the service's configured proxy. |
| `--proxy <proxy>` | omitted | Query `proxy` | Custom proxy as `username:password@host:port`. |
| `--wait-for-selector <selector>` | omitted | Query `waitForSelector` | CSS selector to wait for. |
| `--home-page` | off | Query `warmStart=true` | Visit the site root before the target. |
| `--block-resources` | off | Query `blockResources=true` | Block images, CSS, and fonts. |
| `--bypass-proxy` | off | Query `bypassProxy=true` | Enable the proxy-bypass behavior. |
| `--cookie-jar <config>` | omitted | Query `cookieJar` | Cookie configuration, such as `domain=example.org&country=us`. |
| `--headers <json>` | omitted | Query `headers` | Target page request headers as a JSON object. |
| `--max-retries <n>` | `3` | Body `maxRetries` | Maximum retries; zero disables retries. |
| `--token-cap <n>` | omitted | Body `tokenCap` | Running token total that stops further retries. |
| `--timeout <seconds>` | `120` | Query `timeout` | Page timeout from 1 to 300 seconds; the CLI waits 30 seconds more. |
| `--stream` | off | Query `stream=true` | Ask the API to stream; the CLI still prints one JSON response. |
| `--discard-token-secret <secret>` | omitted | Header `x-discard-token-secret` | Optional upstream header value. |
| `--token <key>` | configured credential | Request headers | Override authentication for this command. |

## Step 4 — Inspect and Retry Deliberately

Start with the default request unless the task already establishes a
requirement. If the response fails, is blocked, incomplete, or missing dynamic
content:

1. Inspect `status_code`, `data.error`, `headers["x-status-code"]`, and the
   returned content;
2. Change one axis at a time: force or disable browser rendering, or add
   `--super` when routing may be the problem;
3. Add `--wait-for-selector`, `--geo-code`, or `--home-page` only when evidence
   shows that the target requires it; and
4. Do not repeat an identical request. Stop after a usable response unless the
   user requests a comparison.

Browser rendering loads a page; it does not click controls, submit forms, or
provide an authenticated interactive browser session.

## Step 5 — Deliver the Result

Answer the user's request from the retrieved page and report any saved
artifact. Keep the full envelope when headers or diagnostics matter.

Keep retrieved content available as the source of truth for later steps. Build
summaries, tables, JSON transformations, and extraction scripts from it, and
retrieve the page again when a follow-up needs details that an earlier
transformation did not preserve.
