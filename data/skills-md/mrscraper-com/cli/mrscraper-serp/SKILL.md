---
name: mrscraper-serp
description: Discover public URLs through Google with the MrScraper CLI's web-search command. Use when a task begins with a query, topic, product, company, or question rather than a known target URL; retrieve selected pages with the Scraper API for reading and analysis.
---

# Discover Pages with MrScraper Web Search

Use `mrscraper web-search` when the task begins with a search query rather than
a known target URL. Use [mrscraper](../mrscraper/SKILL.md) for installation,
authentication, account status, or command routing.

The command sends
`POST https://sync.scraper.mrscraper.com/api/google/serp/v2/sync`.

## Step 1 — Build the Query

Include the important entity, attribute, location, or date in the query. Quote
the query so the shell preserves spaces:

```bash
mkdir -p ./.mrscraper
mrscraper web-search "web scraping best practices" \
  > ./.mrscraper/web-scraping-search.json
```

The input can also be a complete Google search URL:

```bash
mrscraper web-search \
  "https://www.google.com/search?q=web+scraping&gl=us&hl=en&start=20" \
  > ./.mrscraper/web-scraping-search.json
```

For a Google URL, the command reads `q`, `gl`, `hl`, and `start`. Explicit
`--region`, `--language`, and `--page` values take precedence. Always quote
URLs so the shell does not interpret `?` or `&`.

## Step 2 — Set Locale and Pagination

Set both country and language when results must match a locale:

```bash
mrscraper web-search "running shoes" \
  --region id \
  --language id \
  --page 2 \
  > ./.mrscraper/running-shoes-id.json
```

Start with the first page unless the user requests broader coverage. Inspect
each page before requesting another.

## Step 3 — Choose the Output

Parsed JSON is the default. Organic results are in `data.data.organic`, with
related sections such as `people_also_ask` and `pagination` beside them:

```bash
mrscraper web-search "iphone 17" | jq '.data.data.organic'
```

Request result-page HTML when the page itself is needed:

```bash
mrscraper web-search "iphone 17" --format html \
  > ./.mrscraper/iphone-17-search-html.json
```

Use JavaScript rendering for features such as AI Overview:

```bash
mrscraper web-search "what is web scraping" --render-js \
  > ./.mrscraper/web-scraping-rendered.json
```

### Parameters

| CLI parameter | Default | Request mapping | Use |
| --- | --- | --- | --- |
| `<query-or-url>` | required | Body `query` | Search query or complete Google search URL. |
| `--region <code>` | from URL or omitted | Body `region` | Google result country, such as `us` or `id`. |
| `--language <code>` | from URL or omitted | Body `language` | Google result language, such as `en` or `id`. |
| `--page <n>` | from URL or omitted | Body `page` | Positive, 1-based result page. |
| `--format <json\|html>` | `json` | Body `format` | Return parsed JSON or result-page HTML. |
| `--render-js` | off | Body `renderJs=true` | Render JavaScript-dependent result features. |
| `--timeout <seconds>` | `600` | Command request | Set the HTTP request deadline. |
| `--token <key>` | configured credential | Request headers | Override authentication for this command. |

## Step 4 — Inspect the Results

Stdout contains a JSON response envelope. Check the exit code and save
substantial output under `./.mrscraper/`. Progress and diagnostics appear on
stderr.

## Step 5 — Continue with Relevant URLs

Select only URLs relevant to the user's goal, then:

- Load [mrscraper-fetch](../mrscraper-fetch/SKILL.md) for every selected page
  whose content will inform the answer, preserving the raw responses; and
- Analyze or transform those responses locally, using one reusable extraction
  implementation when pages share a structure.

If the user only requested URL discovery, stop after the search. For broad
result sets, retrieve the pages selected for analysis with coverage
proportional to the request, in parallel when the environment supports safe
parallel execution.

## Step 6 — Handle Weak or Missing Results

- Set both `--region` and `--language` when the locale is wrong.
- Rewrite noisy queries with the important entity, attribute, and location.
- Request another result page only after checking the current page.
- Retry once with `--render-js` when a JavaScript-rendered result feature is
  required.
- Increase `--timeout` when the request deadline is too short.
- Use the [mrscraper](../mrscraper/SKILL.md) skill when authentication fails.

Web search is for public Google discovery, not for discovering URLs within one
known site.
