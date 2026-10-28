---
name: web-search
description: "MUST USE when the user needs current, online, or web-derived information — news, latest releases, vendor docs, real-world examples, recent changes, or anything not in the model's training set. LLM-neutral skill that exposes a unified web search CLI behind a single command. Runs single or multi-provider in parallel, saves raw + normalized JSON to a temp directory, prints the path so callers can pipe through rg / jq / grep. Zero-config out of the box. Works identically on macOS, Linux, WSL, Git Bash for Windows, and any environment with Python 3.8+. Triggers: 'search the web', 'look up online', 'google this', 'find current information', 'latest news', 'recent docs', 'check the internet', 'web search', 'browser search', 'research this', 'what is the latest', 'who is X', 'find examples of', 'is there documentation for', 'how do people solve', 'web-search', 'web_search'."
---

# Web Search

Run a search across one or many providers, get a JSON file you can pipe through `rg`, `jq`, or any other tool. Use this **whenever the answer depends on current information that may not be in your training data** — recent releases, today's news, a specific vendor's API as of this week, real-world example usage of a library, security advisories, etc.

## Decision: should I use this skill?

| Question matches | Use web-search? | Why |
|---|---|---|
| "What is the current X?" / "What's the latest Y?" | yes | Time-sensitive |
| "Find examples of how people use library Z" | yes | Real-world code corpus |
| "What did vendor announce about A this month?" | yes | Recent vendor announcements |
| "Look up the docs for command-line flag B" | yes | Authoritative reference |
| "What's the syntax for X?" (well-known language feature) | no | Use training knowledge |
| "Explain the difference between concept C and D" | maybe | Use training first; confirm with search if user wants citations |
| "Find the file in this codebase that does X" | no | Use grep / explore; not web search |

If you decide to search, choose the right invocation pattern below.

## How to invoke

Three patterns, in order of complexity:

### Pattern 1: single provider (most common)

```bash
python3 scripts/web-search "<your query>"
```

Uses the configured default provider (DuckDuckGo if no API keys are set up). Reads stdout for a human-readable preview AND a machine footer that names the result file:

```
=== duckduckgo (10 results, 393ms) ===
  [1] Python (programming language)
      https://en.wikipedia.org/wiki/Python_(programming_language)
      Python is a high-level, general-purpose programming language...
  [2] ...

--- WEBSEARCH ---
RESULT_FILE: /tmp/web-search/20260501T073731Z/combined.json
RUN_DIR:     /tmp/web-search/20260501T073731Z
PROVIDERS:   duckduckgo
TOTAL_RESULTS: 10
```

### Pattern 2: specific provider

```bash
python3 scripts/web-search --provider tavily "<query>"
python3 scripts/web-search --provider perplexity "<query>" --max-results 5
python3 scripts/web-search --provider anthropic "<query>"
```

Use a specific provider when you want a known feature — Perplexity for recency-filtered queries, Tavily for clean LLM snippets, Anthropic/OpenAI/xAI for model-mediated synthesis.

### Pattern 3: parallel multi-provider

```bash
# Subset of providers in parallel:
python3 scripts/web-search --providers tavily,brave,perplexity "<query>"

# Every configured provider in parallel:
python3 scripts/web-search --all "<query>"
```

Use multi-provider when:
- the topic is novel and you want diverse indexes triangulating
- a single provider returned thin or unrelated results on the first try
- the user asked for "thorough research" or "from multiple sources"

The skill saves each provider's output independently, so partial failures still produce useful data.

### Pattern 4: sequential fallback chain (config-driven)

Add a `fallback` field to your config and the skill runs providers **sequentially**, stopping at the first one that returns results:

```json
{
  "default": "brave",
  "fallback": ["openai", "duckduckgo", "mwmbl"]
}
```

Now `python3 scripts/web-search "<query>"` (no `--provider` flag) tries `brave` first; if it errors out OR returns 0 results, it falls through to `openai`; missing credentials silently skip a slot, so the chain proceeds to `duckduckgo`, etc. Footer reports `MODE: fallback` and `FALLBACK_TRIED: <providers that failed>`.

Use a fallback chain when:
- you want resilience against rate limits / outages on a paid provider
- you want a free safety net under a paid primary
- you're future-proofing — list `openai` in the chain today and it activates the moment you add an `apiKey`

`--provider`, `--providers`, `--all` all override the chain — use those when you want a specific behavior for one call.

## Reading the results

Every run writes to `<TMP_ROOT>/<run-id>/`. The path appears in stdout as `RESULT_FILE:`. Default `<TMP_ROOT>` is `/tmp/web-search` on macOS/Linux and `<system-temp>/web-search` on Windows.

Three useful flags for downstream automation:

| Flag | Effect |
|---|---|
| `--print-path-only` | Print only the absolute `combined.json` path. Use inside `$(...)`. |
| `--json` | Print the full manifest JSON to stdout. Pipe straight into `jq`. |
| `--no-preview` | Skip the human preview, keep only the machine footer. |

## Pipelines (the point of this skill)

The whole point of dumping JSON to disk is so you can filter, transform, and combine results without re-running the search. Examples:

```bash
# Get every URL across all providers:
RESULT=$(python3 scripts/web-search --all --print-path-only "...")
jq -r '.manifests[].results[].url' "$RESULT"

# Filter results to lines mentioning "release":
rg -i "release" "$RESULT"

# Stream straight from --json without disk:
python3 scripts/web-search --json "..." | jq '.manifests[].results[0]'

# Top result per provider:
jq -r '.manifests[] | "\(.provider): \(.results[0].title) - \(.results[0].url)"' "$RESULT"

# Dedupe across providers, sorted by score:
jq '[.manifests[].results[]] | unique_by(.url) | sort_by(-(.score // 0)) | .[:10]' "$RESULT"
```

Many more recipes in [`references/pipelines.md`](references/pipelines.md).

## When the wrapper is not available

If the host has `curl` but no Python (some Windows machines, distroless containers, jailed CI), invoke the providers directly. Every provider's exact request shape is documented in [`references/curl-recipes.md`](references/curl-recipes.md). The output schema matches what the skill produces internally — same fields, same names.

## Configuration

The skill works **with zero configuration** — DuckDuckGo and MWMBL accept anonymous calls. Provider variety improves with credentials. Drop a config file in any of these locations:

| OS | Path |
|---|---|
| macOS / Linux | `~/.config/web-search/config.json` |
| Windows | `%APPDATA%\web-search\config.json` |
| Any (project-local) | `./web-search.json` |
| Any (env var) | `$WEBSEARCH_CONFIG` points to a file |

Or set the matching env var (`TAVILY_API_KEY`, `BRAVE_API_KEY`, etc.) and the skill picks it up. See [`references/setup.md`](references/setup.md) for per-provider key acquisition steps.

Validate your setup:

```bash
python3 scripts/web-search --check
python3 scripts/web-search --list-providers
```

## baseUrl override (every provider)

Every provider supports a `baseUrl` field that fully replaces the default endpoint:

```json
{
  "providers": {
    "tavily":    {"apiKey": "tvly-...", "baseUrl": "https://eu.api.tavily.com/search"},
    "anthropic": {"apiKey": "sk-ant-...", "baseUrl": "https://anthropic-gw.internal.example.com/v1/messages"},
    "openai":    {"apiKey": "sk-...", "baseUrl": "http://localhost:8787/openai/v1/responses"}
  }
}
```

Use it for self-hosted proxies, regional mirrors, corporate gateways, or local mocks. The override is complete — the skill does not concatenate with the default. See [`references/base-urls.md`](references/base-urls.md) for concrete patterns.

## Cross-platform behavior

Identical commands work on macOS, Linux, WSL, Git Bash, Windows native, and containers. The Python script uses only the standard library and `pathlib.Path` for path handling — no shell-isms, no `/`-vs-`\` issues.

Windows-specific notes:

```powershell
# PowerShell:
$env:TAVILY_API_KEY = "tvly-..."
python scripts\web-search "your query"

# cmd.exe:
set TAVILY_API_KEY=tvly-...
python scripts\web-search "your query"
```

The shebang `#!/usr/bin/env python3` is ignored on Windows — invoke `python` (or `py`) explicitly. Full guide in [`references/platform-notes.md`](references/platform-notes.md).

## Provider selection guide

| Provider | Auth | Best for |
|---|---|---|
| `duckduckgo` | none | Quick factual lookups; "what is X" |
| `mwmbl` | none | Free fallback for actual web links |
| `exa` | required | Semantic search; technical queries |
| `tavily` | required | LLM-friendly clean snippets |
| `brave` | required | Independent index; privacy-sensitive |
| `serper` | required | Google's organic results, cheap |
| `google-cse` | required + CSE id | Official Google with custom engine |
| `z-ai` | required | Chinese-language queries |
| `perplexity` | required | Recency-filtered; pure or with answer |
| `xai` | required | Grok web_search + x_search (X/Twitter posts) |
| `openai` | required | Web search synthesized by GPT |
| `anthropic` | required | Web search synthesized by Claude |

Full catalog with API shapes, server caps, and quirks: [`references/providers/index.md`](references/providers/index.md). Each provider has its own dedicated page (e.g. [`providers/tavily.md`](references/providers/tavily.md), [`providers/anthropic.md`](references/providers/anthropic.md)).

## Domain filtering

Restrict results to or away from specific domains:

```bash
python3 scripts/web-search "..." --include docs.python.org,python.org
python3 scripts/web-search "..." --exclude reddit.com,medium.com
```

Both `--include` and `--exclude` accept comma-separated lists. Some providers (z-ai, xAI) have stricter caps — see the per-provider pages under [`references/providers/`](references/providers/). Allowed and blocked are mutually exclusive at call time.

## Cost awareness

| Tier | Providers |
|---|---|
| Free, no key | duckduckgo, mwmbl |
| Free with key (small free tier) | tavily, serper, google-cse, perplexity (small) |
| Paid per call | brave, z-ai, perplexity (volume), xai, openai, anthropic |

Model-mediated providers (xai, openai, anthropic) charge per call AND per token. Set `maxUses` (Anthropic) or `max_tool_calls` (OpenAI) in config to cap runaway agentic loops. For broad sweeps prefer the cheaper non-model providers and reserve LLM-mediated search for synthesis.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `config error: No default provider configured` | No keys set, default unset | Run `--check`; configure at least one provider or use `--provider duckduckgo` |
| `[provider] HTTP 401` | Invalid or expired API key | Rotate the key; `--check` to verify |
| `[provider] HTTP 429` | Rate limit hit | Lower `--parallelism`, add delay between runs, or switch providers |
| `Failed to parse response: ...` | Upstream changed schema OR `baseUrl` points at wrong path | Inspect `<provider>-raw.json` in the run dir |
| Empty preview, 0 results | Query too narrow OR provider has no relevant index | Try `--all` or a different provider |

The raw upstream response is always saved at `<run-dir>/<provider>-raw.json` so you can inspect failures without re-querying.

## Reference index

| File | Contents |
|---|---|
| [`references/providers/index.md`](references/providers/index.md) + per-provider pages | Each of the 12 providers has its own page: endpoint, auth, request/response shape, setup, curl recipe, quirks, baseUrl pattern. The index has the comparison table and selection guide. |
| [`references/setup.md`](references/setup.md) | Step-by-step API key acquisition for each provider |
| [`references/pipelines.md`](references/pipelines.md) | rg / jq / awk recipes for filtering and combining results |
| [`references/curl-recipes.md`](references/curl-recipes.md) | Direct curl invocations per provider — Python-less fallback |
| [`references/multi-provider.md`](references/multi-provider.md) | Parallel fan-out strategies, consensus ranking, failure isolation |
| [`references/result-schema.md`](references/result-schema.md) | Canonical JSON output schema; per-provider field mappings |
| [`references/platform-notes.md`](references/platform-notes.md) | macOS / Linux / Windows / WSL / containers gotchas |
| [`references/base-urls.md`](references/base-urls.md) | `baseUrl` override patterns for proxies, gateways, mocks, mirrors |

## Quick reference

```
python3 scripts/web-search [OPTIONS] "<query>"

  --provider NAME         Single provider (overrides default)
  --providers a,b,c       Comma-separated subset, run in parallel
  --all                   Run every configured provider in parallel
  --max-results N         Cap per provider (default 10)
  --include DOMAIN[,...]  Allow-list domains
  --exclude DOMAIN[,...]  Block-list domains
  --config PATH           Override config file
  --tmp-dir PATH          Override output directory
  --json                  Print full manifest to stdout
  --print-path-only       Print only the result file path
  --raw                   Print raw upstream JSON
  --list-providers        Show configured providers and exit
  --check                 Validate config, exit 0 if any provider works
```

When in doubt:

```bash
python3 scripts/web-search --provider duckduckgo "<query>"   # always works, no key needed
```
