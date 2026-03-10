---
name: exa-search
description: >-
  Searches the web via Exa’s Search API and returns source URLs (optionally with highlights, full text, summaries, and subpages).
  Use when the user asks to “search with Exa”, “use Exa”, “find sources/URLs”, “do web research”, “retrieve webpage text”,
  “get highlights/summaries”, “filter by domain/date/category”, or needs fresh results (news, real-time lookups).
metadata:
  author: "generated-by-chatgpt"
  version: "1.0.0"
  upstream_docs:
    - "https://exa.ai/docs/reference/search"
    - "https://exa.ai/docs/reference/search-quickstart"
    - "https://exa.ai/docs/reference/search-best-practices"
---

# Searching with Exa (Search API)

This skill is a **recipe for consistent web research** using Exa’s Search API: you choose the right search mode, apply the right filters, request only the content you need (highlights/text/summary), and return clean citations.

## Quick start (default path)

1) Ensure an API key is available as an environment variable:

- `EXA_API_KEY` (preferred)
- or pass `--api-key` to the scripts.

2) Run a search (JSON response to stdout):

```bash
python {baseDir}/scripts/exa_search.py   --query "latest research in LLMs"   --type auto   --category "research paper"   --num-results 5   --highlights   --highlights-per-url 3   --num-sentences 2
```

## Operating principles (always follow)

- **Always return URLs**. Prefer also returning title + a 1–2 sentence “why this source” note.
- **Prefer `highlights` first** for agentic workflows. Escalate to full `text` only when necessary.
- **Use filters aggressively**: domain allowlists, date windows, and `category` improve relevance and reduce noise.
- **Freshness is explicit**: if the user asks for “latest”, “today”, “current”, etc., set a freshness policy (see below).
- **Don’t overfetch**: cap content length with `maxCharacters` when requesting `text`.
- **If the user needs hard evidence** (numbers, quotes), fetch full text for the top 1–3 pages and verify.

## Workflow

### Step 1 — Translate the user task into a search plan

Decide:

1. **Search type**
   - `auto` (default): best general quality.
   - `instant`: lowest latency, for autocomplete / live suggestions.
   - `deep`: more comprehensive; can use `additionalQueries`.
   - `fast` / `neural`: streamlined alternatives.

2. **Category** (when appropriate)
   - `news`, `research paper`, `company`, `people`, `tweet`, `personal site`, `financial report`, etc.

3. **Freshness**
   - If “real-time / latest”: consider live crawling via `maxAgeHours` (see *Freshness*).
   - If “historical/static”: use cache only (e.g., `maxAgeHours: -1`).

4. **Content mode**
   - `highlights`: token-efficient evidence snippets.
   - `text`: deep reading (cap via `maxCharacters`).
   - `summary`: quick structured overviews (optionally with a guiding `query`).

### Step 2 — Build the request payload

Start from this template and fill only what you need:

```json
{
  "query": "...",
  "type": "auto",
  "category": "news",
  "numResults": 10,
  "includeDomains": ["..."],
  "excludeDomains": ["..."],
  "startPublishedDate": "2025-01-01T00:00:00.000Z",
  "endPublishedDate": "2025-12-31T23:59:59.999Z",
  "includeText": ["must contain phrase"],
  "excludeText": ["must not contain phrase"],
  "contents": {
    "highlights": true,
    "text": { "maxCharacters": 8000, "includeHtmlTags": false },
    "summary": { "query": "..." },
    "subpages": 0,
    "extras": { "links": 0, "imageLinks": 0 },
    "maxAgeHours": 24
  }
}
```

Notes:
- `contents` is optional. If omitted, you’ll only get metadata (`title`, `url`, etc.).
- `maxAgeHours` controls when Exa should live-crawl vs use cached content (see below).
- `context` is deprecated; use `highlights` or `text` instead.

### Step 3 — Execute the request

**Option A (recommended):** use the bundled script so requests are consistent and validated.

```bash
python {baseDir}/scripts/exa_search.py --query "..." --highlights --num-results 10
```

**Option B:** call the HTTP endpoint directly.

```bash
curl --request POST   --url https://api.exa.ai/search   --header "content-type: application/json"   --header "x-api-key: $EXA_API_KEY"   --data '{"query":"...","type":"auto","numResults":5}'
```

### Step 4 — Post-process results into an answer with citations

1. **De-duplicate** near-identical domains/pages when the user wants breadth.
2. **Select the top sources** (usually 3–7) that jointly cover the claim space.
3. For each selected result, extract:
   - title, url
   - key highlight(s) or a short quote from `text`
   - published date (if available)
4. **Write the response** with inline citations (URLs) and clear uncertainty where needed.
5. If the user wants a deliverable (report, memo), preserve a “Sources” section listing all URLs.

## Freshness policy (use this when “latest/current/today” appears)

Use `contents.maxAgeHours` (or the `maxAgeHours` top-level alias if the API accepts it):

- `24`: daily-fresh content (use cache if <24h else livecrawl)
- `1`: near-real-time (cache if <1h else livecrawl)
- `0`: always livecrawl (slowest, most current)
- `-1`: never livecrawl (fastest; cache only)
- omit: default behaviour (livecrawl only when cache missing)

## Common patterns

### Pattern A — “Give me sources for X” (fast + token efficient)
- `type: auto`, `numResults: 5–10`
- `contents.highlights: true`
- Optional: `category` and `includeDomains`

### Pattern B — “Do deep research on X” (read a few pages thoroughly)
- Start with highlights on 10–20 results.
- Then fetch full `text` for the top 3–5 URLs with a `maxCharacters` cap.
- Summarise with citations.

### Pattern C — “Latest news about X”
- `category: news`
- Apply a date window (`startPublishedDate`) if the question is time-bound.
- Use a freshness setting (often `maxAgeHours: 1–24`).

### Pattern D — “Find a company / person page”
- `category: company` or `people`
- If using `people`, allowlist LinkedIn domains when needed.
- IMPORTANT: some filters are unsupported for `company`/`people`; see troubleshooting.

## Troubleshooting

### 401 / 403 (auth)
- Confirm `x-api-key` header is present and valid.
- Confirm you aren’t accidentally using a placeholder like `YOUR-EXA-API-KEY`.

### 400 (invalid parameters)
- `company` and `people` categories support a limited set of filters; unsupported parameters can trigger 400 errors.
- If in doubt, remove date and text filters first, then re-add one-by-one.

### Too much content / token blow-ups
- Prefer `highlights` over `text`.
- Cap `text.maxCharacters`.
- Reduce `numResults`.

## Bundled references

- API + parameter cheat sheet: `references/exa-search-api.md`
- Best-practice recipes: `references/exa-search-best-practices.md`
- Quickstart snippets (SDK + curl): `references/exa-search-quickstart.md`
