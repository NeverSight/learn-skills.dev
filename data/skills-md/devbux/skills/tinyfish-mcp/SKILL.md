---
name: tinyfish-mcp
license: MIT
description: >
  Live web search, webpage extraction, browser automation, monitors, and deep research
  using the TinyFish MCP server (search, fetch_content, run_web_automation,
  start_deep_research, monitors, wallet). Search and fetch are free; automation,
  browser sessions, monitors, and deep research beyond the daily free allowance
  draw from the wallet, so know the rates before calling them. Completely
  standalone and works with any AI coding assistant or harness.
---

# Web Search, Fetching, Automation & Research with TinyFish MCP

The **TinyFish MCP** server (`https://agent.tinyfish.ai/mcp`) connects AI coding
agents to live web search, full-browser page extraction, multi-step web
automation, recurring monitors, and cited deep research. It is a hosted remote
MCP server over Streamable HTTP, authenticated with **OAuth 2.1** — no API-key
header in the MCP config; the client opens a browser sign-in on first connect
(sign in to your TinyFish account in your default browser first).

---

## 1. Pick the lightest tool that does the job

**Search is the focus of this skill** — TinyFish's search is its strongest
capability, and the depth below goes there. The other capabilities are
covered compactly so you know they exist and what they cost, without paying
their full documentation in tokens on every read.

| Situation | Tool |
| --- | --- |
| No URL yet, need information or URLs | `search` (§2A, the detailed section) |
| URL in hand, need only its content | `fetch_content` (§2B, compact) |
| Need to click, log in, fill forms, or interact | `run_web_automation` (§2C, compact) |
| Need raw programmatic browser control (Playwright/Puppeteer/Selenium) | `create_browser_session` (§2D, compact) |
| Need to watch a topic or page on a schedule | `create_monitor` (§2D, compact) |
| Need an explicit multi-source cited report, not a quick answer | `start_deep_research` (§2D, compact) |

Quick questions stay on `search` / `fetch_content`. Do not reach for automation,
browser sessions, or deep research when a search and a fetch answer the question.

---

## 2. Core tools

### A. `search` (Live Web Search) — free, $0.00 per request

```json
{
  "query": "TypeScript 5.8 satisfies operator type narrowing",
  "domain_type": "web",
  "location": "US",
  "language": "en",
  "purpose": "finding the canonical docs page for a migration guide"
}
```

| Parameter | Required | Notes |
| --- | --- | --- |
| `query` | Yes | Concise, keyword-focused. |
| `domain_type` | No | `"web"` (default) \| `"news"` \| `"research_paper"`. |
| `recency_minutes`, `after_date`, `before_date` | No | Time bounds. Not supported when `domain_type` is `"research_paper"` — use `pub_year_min` / `pub_year_max` instead (inclusive integers, `0`–`9999`, min ≤ max). |
| `location` | No | Country code, e.g. `"US"`. |
| `language` | No | Language code, e.g. `"en"`. |
| `include_domains` / `exclude_domains` | No | Comma-separated domain allow/deny lists, combined length capped. |
| `page` | No | 0-indexed pagination, `0`–`10`. |
| `purpose` | No | A short statement of why you are searching; gives the search extra intent signal. |

Returns structured results with titles, snippets, and URLs. Use `get_search_usage`
(date range / status filters) to check allowance consumption instead of guessing.

### B. `fetch_content` (Content Extraction) — free, $0.00 per URL, compact

Fetches pages, renders JavaScript-heavy pages when needed, and extracts clean,
structured content. **Up to 10 URLs in a single request** — batch instead of
calling once per URL. Parameters: `format` (`"markdown"` default | `"html"` |
`"json"`), `links` / `image_links` (extract outbound / image URLs), `ttl`
(cache freshness tolerance, seconds), `per_url_timeout_ms`, `include_selectors`
/ `exclude_selectors` (1–20 CSS selectors each), conditional
`if_none_match` / `if_modified_since` (single URL only, with
`include_etag_and_last_modified` to get the validators back), and `purpose`.
Use `list_fetch_usage` (date range / status filters) to review past fetches;
it returns metadata only.

### C. Beyond search and fetch (compact — know they exist and what they cost)

- **Web automation — $0.016 per step.** `run_web_automation` executes
  multi-step automation from a URL and a natural-language goal, streaming
  progress; use only when interaction is required (clicking, forms, logins).
  `run_web_automation_async` returns a `run_id` immediately for long runs;
  poll with `get_run`, or check up to 8 runs at once with `batch_status`
  (every 30–60 seconds until `all_terminal` is true). `batch_cancel` and
  `cancel_run` are idempotent. For authenticated or recurring workflows,
  prefer a saved Browser Context Profile: `use_profile: true`, plus
  `profile_id` to select one (requires `use_profile: true`), paired with
  `use_vault: true` to repair stale sessions with saved credentials.
  Profiles must be created via the API or dashboard first.
- **Deep research — first 2 completed runs per UTC day free, then $2 (Deep) /
  $3 (Max).** `start_deep_research` takes `query` and optional `mode`
  (`"deep"` default | `"max"`); it returns a `research_run_id` immediately.
  Poll `get_deep_research` (waits about 25 seconds) through `QUEUED` /
  `RUNNING` until `COMPLETED` (report + citations), `FAILED`, `CANCELLED`, or
  `TIMED_OUT`. Runs take several minutes, at most 5 at once.
  `cancel_deep_research` stops one. For quick questions, stay on search/fetch.
- **Monitors — $0.005 per completed run (failed runs free), plus its
  search/fetch.** `create_monitor` with `type: "search"` + `config.query` or
  `type: "fetch"` + `config.url`; `schedule_cron` is a 5-field cron, UTC
  unless prefixed with `CRON_TZ=<zone>`. Creation returns a baseline result
  immediately. Manage with `list_monitors`, `get_monitor`, `pause_monitor`,
  `resume_monitor`, `run_monitor` (run once now), `cancel_monitor` (deletes
  it). Optional: `name`, `webhook_url`, `purpose`.
- **Browser sessions — $0.002 per browser-minute.**
  `create_browser_session` returns CDP details for Playwright, Puppeteer, or
  Selenium; `list_browser_sessions` filters by session ID, time range, and
  status; `close_browser_session` releases early (idempotent).
- **Legacy credit plans.** Accounts on legacy credit plans bill 1 credit per
  step and 1 credit per 4 browser-minutes instead of the dollar rates above.
- **Wallet.** `get_wallet` is read-only (balance, auto-reload state, contract
  rates, in-flight top-up; auto-reload changes happen in the dashboard).
  `top_up_wallet` adds money over the Machine Payments Protocol (two-call
  flow: challenge, then paid credential); accounts outside the rollout do not
  see it, and calling it returns `Unknown tool: top_up_wallet`.

Full inventory (26 tools): Web Automation: `run_web_automation`,
`run_web_automation_async`, `get_run`, `list_runs`, `cancel_run`. Batch:
`batch_status`, `batch_cancel`. Search: `search`, `get_search_usage`.
Extraction: `fetch_content`, `list_fetch_usage`. Deep Research:
`start_deep_research`, `get_deep_research`, `cancel_deep_research`. Monitors:
`create_monitor`, `list_monitors`, `get_monitor`, `pause_monitor`,
`resume_monitor`, `run_monitor`, `cancel_monitor`. Browser Sessions:
`create_browser_session`, `list_browser_sessions`, `close_browser_session`.
Wallet: `get_wallet`, `top_up_wallet`.

---

## 3. Rules that save money and tokens

- **Free vs. metered is the first decision.** `search` and `fetch_content`
  cost nothing; everything in §2C draws from the wallet (except the daily
  deep-research allowance and free failed monitor runs). Never call a metered
  tool when a free one answers the question, and check `get_wallet` before a
  long automation or research run.
- **Batch, don't serialize.** One `fetch_content` call takes up to 10 URLs;
  `batch_status` covers up to 8 runs. There is no official sequential-only
  rule — batching is the documented pattern.
- **Scope searches with filters, not extra calls.** `domain_type`,
  `recency_minutes`, date bounds, `include_domains` / `exclude_domains`, and
  `page` beat re-querying. For papers, use `pub_year_min` / `pub_year_max`.
- **Never put secrets in queries or fetch private/internal URLs.** Search
  queries and fetched URLs go to external infrastructure; public endpoints only.

---

## 4. Setup & Client Configuration

- **Endpoint URL**: `https://agent.tinyfish.ai/mcp`
- **Authentication**: OAuth 2.1. On first connect the client opens a browser
  sign-in; sign in to your TinyFish account in your default browser first.
  There is no Bearer header and no unauthenticated MCP mode. (Command Code is
  the exception: it connects by API key only, via its CLI.)

### Quick install (any client)

```bash
npx -y install-mcp@latest https://agent.tinyfish.ai/mcp --client <claude-code|cursor|windsurf|...>
```

### Manual configuration

Claude Code CLI:

```bash
claude mcp add --transport http tinyfish https://agent.tinyfish.ai/mcp
```

Cursor (`mcpServers`):

```json
{
  "mcpServers": {
    "tinyfish": {
      "url": "https://agent.tinyfish.ai/mcp"
    }
  }
}
```

VS Code (`.vscode/mcp.json`): the same JSON under `"servers"` with
`"type": "http"` added. No headers block in any of these — OAuth is completed
in the browser, not in the config.
