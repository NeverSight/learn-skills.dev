---
name: rustxng
description: "Web search and page-text grounding through a local RustXNG server (keyless, self-hosted SearXNG port), driven with curl and jq. Use when a task needs current facts from the web and a `rustxng` binary is on PATH: searching, pulling page text to ground an answer, restricting a lookup to certain domains, or running a multi-query `/research` sweep. Also covers crawling a corpus into a local BM25 index with `rustxng-index`."
---

# rustxng

`rustxng` is a local metasearch server: it fans a query out to many upstream engines and answers over HTTP, with no API key. One request can return ranked results and the text of the top pages, so an answer can be grounded on what the pages say. `rustxng --help` lists the CLI flags and most environment variables.

Examples use the default address `127.0.0.1:8888`. Change the port in every URL when you start on another one.

## 1. Get a server

Probe first, since one may already be running:

```bash
curl -fsS -m 2 http://127.0.0.1:8888/healthz
```

`OK` means reuse it, and leave it running afterwards because it is not yours to stop. If nothing answers, start one that cleans up after itself, then wait for it:

```bash
log=$(mktemp)
RUSTXNG_IDLE_TIMEOUT=600 rustxng >"$log" 2>&1 &
pid=$!
ready=
for i in $(seq 50); do
  curl -fsS -m 1 http://127.0.0.1:8888/healthz 2>/dev/null && { ready=1; break; }
  kill -0 "$pid" 2>/dev/null || break
  sleep 0.2
done
[ -n "$ready" ] || { kill "$pid" 2>/dev/null; tail -n 20 "$log"; false; }
```

This step is done when the block prints `OK` and exits 0. A non-zero exit means the server did not come up, and the output is the end of its log, so act on the `error:` line there. `Address already in use` means another program holds the port (Jupyter also defaults to 8888), which `--port <other>` solves. Any other error, such as an unreadable settings file, needs its own fix because a new port will fail the same way.

- `RUSTXNG_IDLE_TIMEOUT` is in seconds. The server exits with status 0 once that long passes with no requests, checked every 5 seconds. Any request resets the clock, `/healthz` included, so a health-polling loop keeps the server alive forever.
- With no settings file it boots from embedded defaults and needs no secret. A `./settings.toml` in the working directory is not read.

## 2. Search

Keep output small from the first call. An uncapped response is 110 to 180 KB (130 to 225 results), so set `max_results` and project with `jq`:

```bash
curl -fsS -G http://127.0.0.1:8888/search \
  --data-urlencode 'q=tokio runtime' -d format=json -d max_results=5 \
  | jq -r '.results[] | "\(.title)\n\(.url)\n\(.content)\n"'
```

`format=json` is required on every call, because the default is HTML. `-f` makes curl exit non-zero on an HTTP error, which matters because errors are never JSON: they come back as an HTML page (missing `q`, unknown `format`) or plain text (non-numeric `pageno`), with status 400.

### Grounding on page text

Add `include_raw_content=1`, and pick how many pages to read with `max_results`, which applies before the pages are fetched:

```bash
curl -fsS -G http://127.0.0.1:8888/search \
  --data-urlencode 'q=tokio runtime' -d format=json \
  -d include_raw_content=1 -d max_results=3 \
  | jq '.results[] | {url, title, raw_content}'
```

- Only the top 5 results get page text, however high `max_results` goes. No request parameter changes that.
- Each `raw_content` is cut at 8000 characters, and a trailing `…` marks the cut: the page continues beyond what you can see.
- A failed fetch leaves the key absent, so `jq` above prints `null`. In testing reddit.com pages came back this way every time, and one run lost all 3 tokio.rs pages that a repeat then returned in full. When every result is missing, retry once. Treat a result that stays missing as snippet-only and cite it only for what `content` says, or read the next result instead.

### Parameters

Accepted on `/search`, by GET or POST:

| Parameter | Values | Notes |
| --- | --- | --- |
| `q` | text | Required. Parsed for SearXNG syntax, so `!!gh rust` answers 303 to the external site instead of JSON. |
| `format` | `json`, `csv`, `rss`, `html` | Page text is emitted only in `json`. |
| `max_results` | 1 to 200 | No cap when omitted. |
| `include_raw_content` | `1` | See above. |
| `include_domains`, `exclude_domains` | comma list | Subdomains match. |
| `categories` | comma list | Default `general`. Tried: `it`, `science`, `news`. |
| `time_range` | `day`, `week`, `month`, `year` | Any other value is silently ignored. `publishedDate` is often null, so this cannot be checked from the output. |
| `timeout_limit` | seconds | Default 3. |
| `pageno` | integer | Default 1. |
| `locale` | e.g. `ja`, `de` | Default `en`. |
| `safesearch` | 0 to 2 | Default 0. |
| `engines` | comma list | Replaces `categories`. See below. |
| `full` | `1` | Adds `number_of_results`, `timings`, `pageno`, `paging` and more to the response. |

Response keys are `query`, `results`, `answers`, `corrections`, `infoboxes`, `suggestions` and `unresponsive_engines`. Each result carries `url`, `title`, `content`, `engine`, `engines`, `score`, `publishedDate` and `raw_content` when fetched, plus others most tasks can ignore.

### How results behave

- **Latency tracks `timeout_limit`.** A cold query waits for slow engines up to the limit, so it measured 1.3 to 3.0 s at the default and 1.0 s with `timeout_limit=1`. Successful upstream responses are cached for 300 s. A repeat measured 0.03 to 0.3 s when everything was cached, yet could still take the full limit while stalled engines were retried.
- **A long `unresponsive_engines` list is normal.** It holds `[engine, reason]` pairs such as `Access denied` and `Too many requests`, and a request succeeds without those engines. Read it when `results` comes back empty, since the status is still 200.
- **Domain filters narrow what upstream already returned.** They do not make engines search that site, so put topic words in `q`. With `include_domains=doc.rust-lang.org`, `async await` returned nothing while `rust async await` returned 3 pages.
- **Reach for `categories` and `include_domains` before `engines`.** A single named engine turns off relevance ranking and has no fallback when that engine blocks you: in testing `duckduckgo` answered `CAPTCHA` and `wikipedia` answered `Too many requests` on some runs, while `github` and `arxiv` worked. A name it does not recognize silently falls back to the default category with status 200, so when you name an engine, confirm it in `.results[].engine`.
- **Write the query in the language you want results in.** Japanese queries returned Japanese pages under every `locale`, and `locale=ja` left the results for `mercury` unchanged. Pass `locale`, since `language` is read only for HTML paging links.
- **Calling in parallel is fine locally.** The bot limiter is off by default, and 8 concurrent requests all returned 200. The limit you will meet is upstream engines throttling you. Under a settings file that enables the limiter, expect 429 with `Retry-After`.

## 3. Sweep a broad question

`/research` runs several searches in sequence and returns deduplicated sources in one call. A successful response is always JSON, so it takes no `format`:

```bash
curl -fsS -G http://127.0.0.1:8888/research \
  --data-urlencode 'q=tokio runtime' -d max_queries=2 -d max_sources=3 \
  | jq '{queries, sources: [.sources[] | {url, title, content}]}'
```

`max_queries` is 1 to 10 (default 5) and `max_sources` is 1 to 50 (default 10). Each source's `content` is page text when the fetch worked and the search snippet when it did not, with nothing marking which, and length does not tell them apart. So treat `/research` as discovery. To ground on what it found, re-run the sub-query through `/search` with `include_raw_content=1`, adding `include_domains=<host>` to target a source, because there a failed fetch shows as an absent key.

Without an LLM configured, which is the default, the sub-queries are just `q` plus the fixed suffixes `overview`, `best practices` and `examples`. That means at most 4 searches, at most 20 sources (each sub-query keeps 5), and a null `report`. Budget about 4 s per sub-query: fresh runs took 7.6 to 7.9 s for 2 and 13.7 s for 4. For a question with a known shape, your own targeted `/search` calls will do better than these suffixes.

## 4. Inspect the server

- `/stats/errors` is JSON per engine, including `suspended` and `suspension_reason`. Check it when results get thin during a long session.
- `/config` is JSON with the engine list and `default_locale`.
- `/autocompleter?q=rust` is a JSON array of suggested queries. It is empty when the default backend is unreachable, which `backend=wikipedia` worked around in testing.

## 5. Settings files and the local index

Before passing `-c` or `SEARXNG_SETTINGS_PATH`, or when asked to crawl with `rustxng-index`, read [references/config-and-index.md](references/config-and-index.md). A hand-written settings file silently changes defaults, and the index takes a settings file to be used at all.
