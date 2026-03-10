---
name: free-search-aggregator
description: Quota-aware multi-provider web search for OpenClaw. Supports 12 search providers with automatic failover, task-level deep search (@dual/@deep), real quota checks, and managed result storage under memory/.
---

# Free Search Aggregator

Reliable, provider-diverse web search for OpenClaw with **high uptime + low operator overhead**.

## Why use this skill

- **12 search providers**, 6 requiring no API key at all
- Automatic failover: if one provider fails, the next is tried instantly
- Quota-aware: tracks daily usage, warns at 80%, skips exhausted providers
- Task search mode for multi-angle research queries
- Built-in storage lifecycle (cache / index / report), no workspace clutter
- **Self-healing**: health-based smart routing automatically promotes reliable providers
- **Quality optimization**: relevance scoring, fuzzy dedup, domain diversity, re-ranking
- **Auto-discovery**: probes candidate search engines and SearXNG instances for new sources
- **Self-diagnostic**: `doctor` and `setup` commands for zero-friction onboarding

---

## Provider Overview

| Provider       | Key Required | Free Quota        | Index Source          | Notes                           |
|----------------|-------------|-------------------|-----------------------|---------------------------------|
| `brave`        | BRAVE_API_KEY | 2000/day         | Brave independent     | High quality, privacy-friendly  |
| `exa`          | EXA_API_KEY   | ~33/day (1k/mo)  | Neural + web          | Semantic search, unique finds   |
| `tavily`       | TAVILY_API_KEY | 1000/day        | Web (AI-optimized)    | Designed for AI agents          |
| `duckduckgo`   | None          | ~500/day          | Bing + own            | No key, privacy-focused         |
| `bing_html`    | None          | ~300/day          | Microsoft Bing RSS    | No key, stable XML feed         |
| `mojeek`       | None (or MOJEEK_API_KEY) | 200/day | Mojeek independent | Non-Google/Bing index  |
| `serper`       | SERPER_API_KEY | 2500/day         | Google                | High quota free tier            |
| `searchapi`    | SEARCHAPI_API_KEY | 100/mo        | Google / Bing         | Multi-engine                    |
| `google_cse`   | GOOGLE_API_KEY + GOOGLE_CX | 100/day | Google        | Official Google API             |
| `baidu`        | BAIDU_API_KEY | 200/day           | Baidu                 | Best for Chinese content        |
| `wikipedia`    | None          | 1000/day          | Wikipedia             | Factual/encyclopedic queries    |
| `searxng`      | None          | unlimited (self-hosted) | Meta (all engines) | Requires own instance      |

**Total daily quota (all keys configured): 8400+ requests/day**

---

## Credential model (important)

- **No mandatory API key** — DuckDuckGo + Bing RSS + Mojeek + Wikipedia work out of the box.
- API-key providers fail gracefully if key is missing (AuthError → skip, no quota consumed, no latency):
  - `BRAVE_API_KEY`
  - `EXA_API_KEY`
  - `TAVILY_API_KEY`
  - `SERPER_API_KEY`
  - `SEARCHAPI_API_KEY`
  - `GOOGLE_API_KEY` + `GOOGLE_CX`
  - `BAIDU_API_KEY`
  - `MOJEEK_API_KEY` (optional — without it uses HTML scraping)

---

## Core capabilities

### 1. Search failover
Default provider order:
```
brave → exa → tavily → duckduckgo → bing_html → mojeek → serper → searchapi → google_cse → baidu → wikipedia
```
First successful non-empty result returns immediately.

### 2. Task-level multi-query search
- Expands one goal into multiple targeted queries
- Aggregates + deduplicates results
- Prefix presets:
  - default: `workers=1`
  - `@dual ...` → `workers=2`
  - `@deep ...` → `workers=3` + deeper query coverage

### 3. Quota intelligence
- Per-provider daily tracking
- Real quota retrieval where supported (Tavily, SearchAPI, Brave via probe)
- Auto concurrency reduction at 80% quota saturation

### 4. Provider health monitoring
- Tracks success rate, latency, and error types per provider over time
- Computes health scores (success 50%, latency 30%, freshness 20%)
- **Smart ordering**: auto-promotes healthy providers, demotes degraded ones
- View dashboard: `python -m free_search health`

### 5. Result quality optimization
- Relevance scoring (query-title-snippet token overlap)
- Enhanced dedup: URL + title similarity (Jaccard threshold)
- Domain diversity: limits same-domain results (default max 3)
- Automatic filtering of low-quality results (short titles, missing URLs)

### 6. Source auto-discovery
- Probes all configured providers for availability
- Scans candidate search engines (Marginalia, Wiby, public SearXNG instances)
- Validates response format, latency, and result quality
- Generates recommendations for new sources to integrate
- Run: `python -m free_search discover`

### 7. Managed persistence
- `memory/search-cache/YYYY-MM-DD/*.json`
- `memory/search-index/search-index.jsonl`
- `memory/search-reports/YYYY-MM-DD/*.md`

---

## Quick commands

```bash
# Normal search
scripts/search "latest AI agent frameworks 2026" --max-results 5

# Task search (multi-query, parallel)
scripts/search task "@dual Compare Claude vs GPT-4 for code generation" --max-results 5

# Deep research mode
scripts/search task "@deep autonomous vehicle safety 2026" --max-results 8 --max-queries 10

# Quota status
scripts/status

# Real quota from provider APIs
scripts/remaining --real

# Cleanup cache
python3 -m free_search gc --cache-days 14

# Provider health dashboard
python3 -m free_search health

# Discover new search sources
python3 -m free_search discover

# System diagnostics
python3 -m free_search doctor

# Setup status & recommendations
python3 -m free_search setup
```

---

## Provider setup guides

### Bing RSS (`bing_html`) — No key needed
Uses Bing's built-in RSS endpoint (`format=rss`) — bypasses bot detection. Works out of the box.

### Mojeek — No key needed (API key optional)
Out-of-the-box HTML scraping. For higher quotas/stability:
1. Register at https://www.mojeek.com/services/search/api/
2. Set `MOJEEK_API_KEY` → automatically switches to JSON API mode

### Wikipedia — No key needed
Multilingual support — change `lang` in `providers.yaml`:
```yaml
wikipedia:
  lang: it   # en | zh | it | de | fr | ja ...
```

### Exa.ai — API key required
1. Register at https://exa.ai/
2. Set `EXA_API_KEY`
3. Free tier: 1000 searches/month (~33/day)

### Google Custom Search — API key + CX required
1. Get API key: https://developers.google.com/custom-search/v1/introduction
2. Create search engine: https://programmablesearchengine.google.com/
3. Set `GOOGLE_API_KEY` and `GOOGLE_CX`
4. Free tier: 100 queries/day

### Baidu Qianfan — API key required
1. Register at https://cloud.baidu.com/
2. Set `BAIDU_API_KEY`
3. Best for Chinese-language content

### SearXNG — Self-hosted instance required
Public instances rate-limit server-to-server requests. Use your own:
```bash
docker run -d -p 8080:8080 searxng/searxng
```
Then in `providers.yaml`:
```yaml
searxng:
  endpoint: http://localhost:8080
  enabled: true
```

---

## Post-install self-check

```bash
# 1) Confirm provider load
scripts/status --compact

# 2) Smoke test (uses duckduckgo/bing/mojeek out of the box)
scripts/search "openclaw" --max-results 3 --compact

# 3) Verify storage paths
ls -la /home/openclaw/.openclaw/workspace/memory/search-cache/ | tail -n 5

# 4) Check real quota (optional)
scripts/remaining --real --compact
```

---

## Output contract (stable)

- **Search**: `query`, `provider`, `results[]`, `meta.attempted`, `meta.quota`
- **Task search**: `task`, `queries[]`, `grouped_results[]`, `merged_results[]`, `meta`
- **Quota**: `date`, `providers[]`, `totals`; with `--real`: `real_quota.providers[]`

---

## Operator notes

- Default mode: `workers=1` — conservative for cost control
- Use `@dual` / `@deep` only for research tasks
- `SearXNG` and `YaCy` are `enabled: false` by default (self-hosted only)
- `MOJEEK_API_KEY` is optional — provider gracefully falls back to HTML scraping
- Provider health data stored in `memory/provider-health/health.jsonl`
- Discovery results stored in `memory/provider-discovery/discovery.jsonl`
- Run `python -m free_search doctor` after setup to verify everything works
- Run `python -m free_search discover` periodically to find new search sources
