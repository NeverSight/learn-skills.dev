---
name: agent-fetch
description: "Fetch web pages as clean Markdown via the agent-fetch CLI. Handles cases that built-in web-fetch tools may not cover well: JavaScript-rendered pages (headless browser), authenticated endpoints (custom headers), batch fetching multiple URLs concurrently, and content output without AI summarization. Also works standalone when no built-in fetch tool is available."
---

# Agent Fetch

Fetch web pages as clean Markdown for agent workflows. Uses a fallback pipeline: native Markdown -> static HTML extraction -> headless browser rendering.

## When to use agent-fetch

Use agent-fetch instead of (or in addition to) a built-in web-fetch tool when:

- The page is a **JavaScript-rendered SPA** -- use `--mode browser` or let `auto` mode fall back to headless Chrome
- You need **custom headers** (authentication, cookies) -- use `--header` (prefer environment variable references such as `--header "Authorization: Bearer $TOKEN"` to avoid exposing secrets in logs)
- You want the **extracted content without AI summarization** -- agent-fetch outputs the readability-extracted body directly, subject to `--max-body-bytes` (default 8 MiB)
- You need to **batch fetch multiple URLs** concurrently -- pass multiple URLs with `--concurrency`
- You need to **wait for specific content** to appear -- use `--wait-selector`
- **No built-in web-fetch tool** is available in your environment

## Ensure the CLI exists

Require `agent-fetch` in `PATH`. If not installed, install it:

Preferred method (no Go required):

1. Download a release artifact from `https://github.com/firede/agent-fetch/releases`
2. Extract the archive, make the binary executable, and place it on `PATH`.

macOS note: if Gatekeeper blocks execution, run `xattr -dr com.apple.quarantine /path/to/agent-fetch`

Alternative method (requires Go):

```bash
go install github.com/firede/agent-fetch/cmd/agent-fetch@latest
```

Verify: `agent-fetch --help`

## Modes

| Mode | When to use | Browser needed |
|------|-------------|----------------|
| `auto` (default) | General pages -- tries markdown, then static, then browser | Only if static quality is low |
| `static` | When browser is unavailable or unnecessary | No |
| `browser` | JavaScript-heavy or dynamic pages | Yes (Chrome/Chromium) |
| `raw` | When you need the exact HTTP response body | No |

## Command patterns

Default (auto mode):

```bash
agent-fetch https://example.com
```

JavaScript-heavy page:

```bash
agent-fetch --mode browser --wait-selector "article" https://example.com
```

Authenticated endpoint:

```bash
agent-fetch --header "Authorization: Bearer $TOKEN" https://example.com
```

Batch fetch:

```bash
agent-fetch --concurrency 4 https://example.com https://example.org
```

Static-only (no browser dependency):

```bash
agent-fetch --mode static https://example.com
```

Without front matter:

```bash
agent-fetch --meta=false https://example.com
```

Diagnose browser readiness:

```bash
agent-fetch doctor
```

Use a custom browser path (useful in containers):

```bash
agent-fetch doctor --browser-path /usr/bin/chromium
```

Structured JSONL output:

```bash
agent-fetch --format jsonl https://example.com
```

## Output contract

- Fetched content is written to `stdout` in the selected format (`markdown` or `jsonl`).
- In `markdown` mode with multiple URLs, output uses task markers:

```text
<!-- count: N, succeeded: X, failed: Y -->
<!-- task[1]: <input-url> -->
...markdown...
<!-- /task[1] -->
<!-- task[2](failed): <input-url> -->
<!-- error[2]: <error text> -->
```

- In `jsonl` mode, each task emits one JSON line:

```json
{"seq":1,"url":"https://example.com","resolved_mode":"static","content":"...","meta":{"title":"...","description":"..."}}
{"seq":2,"url":"https://bad.example","error":"http request failed: timeout"}
```

- Exit code `0`: all succeeded. `1`: any task failed. `2`: argument/usage error.

## Error handling

| Symptom | Likely cause | Remedy |
|---------|-------------|--------|
| Empty or very short output in `auto` mode | Static extraction yielded low quality, browser not available | Install Chrome/Chromium, or use `--mode browser` explicitly |
| Browser not found or startup crash | Chrome/Chromium missing or misconfigured | Run `agent-fetch doctor` for guided diagnosis; use `--browser-path` for non-default locations |
| Timeout error | Page loads slowly | Increase `--timeout` (for static) or `--browser-timeout` (for browser) |
| Content missing dynamic elements | Page requires JS rendering | Use `--mode browser`, optionally with `--wait-selector` |
| Auth/403 errors | Endpoint requires credentials | Add `--header "Authorization: Bearer $TOKEN"` or `--header 'Cookie: ...'` |
| Gatekeeper blocks on macOS | Binary not notarized | Run `xattr -dr com.apple.quarantine /path/to/agent-fetch` |
