---
name: apify-ultimate-scraper
description: >-
  Universal AI-powered web scraper for any platform. Scrape data from Instagram,
  Facebook, TikTok, YouTube, LinkedIn, X/Twitter, Google Maps, Google Search,
  Google Trends, Reddit, Airbnb, Yelp, and 15+ more platforms. Use for lead
  generation, brand monitoring, competitor analysis, influencer discovery, trend
  research, content analytics, audience analysis, review analysis, SEO
  intelligence, recruitment, or any data extraction task.
user-invocable: false
---
# Universal web scraper

AI-driven data extraction from ~100 Actors across 15+ platforms via the Apify CLI.

**Rule: Pass `--json` and redirect stderr with `2>/dev/null` on data-returning commands** (`actors call`, `actors start`, `actors info`, `actors search`, `datasets get-items`, `runs info`). JSON output is stable across CLI versions. stderr contains progress messages and version warnings that break JSON parsers if not redirected.

This rule does **not** apply to status/auth commands (`apify info`, `apify --version`, `apify login`). For those, use `2>&1` so authentication and version errors are visible.

**Exception:** if `--input` returns no data, re-run with `2>&1` to confirm whether the cause is a missing schema vs. a network/auth error.

**Rule: pass `--user-agent apify-claude-code-plugin/apify-ultimate-scraper` only on actor start and actor run commands (`apify actors start`, `apify actors call`). Do not add it to login, info, search, or other CLI commands.**

## Prerequisites

- Apify CLI v1.5.0+ (`npm install -g apify-cli`) — older versions reject the user-agent flag
- Authenticated session (see below)

## Authentication

If a CLI command fails with an auth error, authenticate using one of these methods:

1. **OAuth (interactive):** `apify login` (opens browser)
2. **Environment variable:** `export APIFY_TOKEN=your_token_here`
3. **From .env file:** `source .env` (if the file contains `APIFY_TOKEN=...`)

Generate token: https://console.apify.com/settings/integrations

## Workflow

### Step 0: Verify CLI readiness before doing anything else

Before using the Apify CLI, always verify the local environment:

1. Check that the CLI is installed and is v1.5.0 or newer:
```bash
    apify --help
    apify --version
```
If this fails, install the CLI first:
```bash
       npm install -g apify-cli
```
2. Check that the CLI is authenticated:

```bash
    # Auth check — do NOT pipe to /dev/null, you need to see errors
    apify info 2>&1
```
   If this shows the user is not logged in, instruct them to authenticate with a token:

```bash
    apify login --token TOKEN
```

3. Authenticated Apify CLI commands need file access to `~/.apify/`, where the CLI keeps its credentials. A host that sandboxes file access can deny this even when the login is valid; that is a sandbox problem, not a login problem.

4. Assume many Apify commands block with zero output until completion, so allow at least 60 seconds before treating one as stuck. If your shell tool takes a timeout, raise it accordingly.

5. For long or unknown-duration runs, prefer the async pattern:

```bash
    apify actors start "ACTOR_ID" -i 'JSON_INPUT' --user-agent apify-claude-code-plugin/apify-ultimate-scraper --json 2>/dev/null
```

   Then poll the run status:

```bash
    apify runs info RUN_ID --json
```

   Check `.status` for `SUCCEEDED` or `FAILED`.

### Step 1: Understand goal and select Actor

Identify the target platform and use case. Read `references/actor-index.md` to find the right Actor.
Prefer `apify`-tier actors; use `community`-tier only when no `apify` actor covers the task.
For input schemas, fetch dynamically: `apify actors info "ACTOR_ID" --input --json 2>/dev/null`
If the output is empty, re-run without the redirect (`2>&1`) to surface auth or network errors before proceeding.

If the task involves a multi-step pipeline, also read the matching workflow guide:

| Task involves... | Read |
|-----------------|------|
| leads, contacts, emails, B2B | `references/workflows/lead-generation.md` |
| competitor, ads, pricing | `references/workflows/competitive-intel.md` |
| influencer, creator | `references/workflows/influencer-vetting.md` |
| brand, mentions, sentiment | `references/workflows/brand-monitoring.md` |
| reviews, ratings, reputation | `references/workflows/review-analysis.md` |
| SEO, SERP, crawl, content, RAG | `references/workflows/content-and-seo.md` |
| analytics, engagement, performance | `references/workflows/social-media-analytics.md` |
| trends, keywords, hashtags | `references/workflows/trend-research.md` |
| jobs, recruiting, candidates | `references/workflows/job-market-and-recruitment.md` |
| real estate, listings, hotels | `references/workflows/real-estate-and-hospitality.md` |
| price monitoring, e-commerce, products | `references/workflows/ecommerce-price-monitoring.md` |
| contact enrichment, email extraction | `references/workflows/contact-enrichment.md` |
| knowledge base, RAG, LLM data feed | `references/workflows/knowledge-base-and-rag.md` |
| company research, due diligence | `references/workflows/company-research.md` |

If no Actor matches in the index, search dynamically:

    apify actors search "KEYWORDS" --json --limit 10 2>/dev/null

From results: `items[].username`/`items[].name` (Actor ID), `items[].title`, `items[].stats.totalUsers30Days`, `items[].currentPricingInfo.pricingModel`.

### Step 2: Fetch Actor schema and check gotchas

Some Actors don't register an input schema with the platform (their schema lives in code). Try schema sources in this order — fall through on empty/error:

1. **Input schema (human-readable):**
```bash
    apify actors info "ACTOR_ID" --input 2>/dev/null
```
   If output is `Error: No input schema found for this Actor`, skip to source 2.

2. **Input schema (JSON keys only):**
```bash
    apify actors info "ACTOR_ID" --input --json 2>/dev/null | jq '.input.schema.properties // empty | keys'
```
   Empty result means no registered schema — fall through to source 3. To drill into a specific field:
```bash
    apify actors info "ACTOR_ID" --input --json 2>/dev/null | jq '.input.schema.properties.FIELD_NAME'
```

3. **README fallback** (always works, contains usage examples):
```bash
    apify actors info "ACTOR_ID" --readme 2>/dev/null
```
   Grep the README for an "Input" / "Example input" section to copy the JSON shape.

4. **Last resort — call with minimal known input** (e.g. `{"startUrls":[{"url":"..."}]}` for crawlers) and let the Actor surface validation errors that reveal required fields. See `references/gotchas.md` for known-good minimal inputs for common Actors.

Also read `references/gotchas.md` to check for common pitfalls and cost guardrails for the selected Actor.

### Step 3: Configure and run

**Skip user preferences** for simple lookups (e.g., "Nike's follower count"). Go straight to running with quick answer mode.

For larger tasks, confirm output format (quick answer / CSV / JSON) and result count.

Before starting the run, double-check whether the task is short enough for a blocking call or should use the async pattern from Step 0.

**Standard run (blocking):**
```bash
    apify actors call "ACTOR_ID" -i 'JSON_INPUT' --user-agent apify-claude-code-plugin/apify-ultimate-scraper --json 2>/dev/null
```
From output: `.id` (run ID), `.status`, `.defaultDatasetId`, `.stats.durationMillis`

**Fetch results:**
```bash
    apify datasets get-items DATASET_ID --format json
```
For CSV: `apify datasets get-items DATASET_ID --format csv`

**Quick answer mode:** Fetch results as JSON, pick top 5, present formatted in chat.

**Save to file:** Fetch results, use Write tool to save as `YYYY-MM-DD_descriptive-name.csv` or `.json`.

**Large/long-running scrapes:**
```bash
    apify actors start "ACTOR_ID" -i 'JSON_INPUT' --user-agent apify-claude-code-plugin/apify-ultimate-scraper --json 2>/dev/null
```
Poll: `apify runs info RUN_ID --json` (check `.status` for `SUCCEEDED` or `FAILED`).

### Step 4: Deliver results

Report: result count, file location (if saved), key data fields, and links:
- Dataset: `https://console.apify.com/storage/datasets/DATASET_ID`
- Run: `https://console.apify.com/actors/runs/RUN_ID`

For multi-step workflows: suggest the next pipeline step from the workflow guide.

## Troubleshooting

Common errors and pitfalls are documented in `references/gotchas.md`. Read it before running PPE (pay-per-event) Actors.
