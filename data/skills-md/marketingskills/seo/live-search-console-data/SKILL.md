---
name: live-search-console-data
description: Get live Google Search Console and GA4 data in your agent in 30 seconds. No Google Cloud project, no API keys, no OAuth setup. One sign-in, and your agent can query real GSC clicks, impressions, rankings, and GA4 sessions. Use when Codex needs authenticated access to live Google search and analytics data for any SEO analysis.
---

# Live Search Console Data

## Overview

Get live Google Search Console and GA4 data in your agent in 30 seconds. No Google Cloud project to create, no API keys to request, no OAuth consent screen to configure. One Google sign-in and your agent can query real clicks, impressions, rankings, sessions, and conversions. Uses RefreshAgent as an authenticated proxy — keep secrets out of prompts and repositories. Prefer the bundled helper because it can authenticate, save, and reuse the user's local key without exposing it in chat.

## First-Use Login

Before doing any SEO analysis, check whether the user already has a saved RefreshAgent key by running exactly one lightweight helper command first. Expect this first command to open a browser login if `~/.config/refreshagent/.env` does not exist yet:

```bash
python3 /home/dunc/.codex/skills/live-search-console-data/scripts/refreshagent_api.py \
  GET /api/v1/clients --login
```

If the helper opens a browser, tell the user that RefreshAgent needs one Google sign-in on first use, then wait for the command to finish. Do not investigate missing output as a data/API problem while the login is pending. Do not start Search Console and GA4 discovery in parallel until this first command has completed and saved the key.

After the first command succeeds, continue with resource discovery (`/api/v1/sc/sites`, `/api/v1/ga4/properties`) and the user's requested analysis. Later runs should reuse the saved key and should not open a browser.

## Authentication

Send the API key in the `X-API-Key` header.

Do not save API keys in skill files, repositories, shell history, examples, or final answers. Prefer:

```bash
export REFRESHAGENT_API_KEY="..."
```

The helper also checks `~/.config/refreshagent/.env`. If no key exists, it opens `https://refreshagent.com/auth/cli` with a localhost callback, waits for Google login, saves the returned key to `~/.config/refreshagent/.env`, and then continues the original API request.

When running commands from an agent, use the helper directly. If it starts login, tell the user to complete the browser sign-in and return to the agent. Do not ask the user to manually paste a key unless browser login is unavailable.

## Quick Start

Use `scripts/refreshagent_api.py` for authenticated REST calls:

```bash
python3 /home/dunc/.codex/skills/live-search-console-data/scripts/refreshagent_api.py \
  GET /api/v1/sc/sites
```

To force setup without making an API request:

```bash
python3 /home/dunc/.codex/skills/live-search-console-data/scripts/refreshagent_api.py \
  GET /api/v1/clients --login
```

Examples:

```bash
python3 /home/dunc/.codex/skills/live-search-console-data/scripts/refreshagent_api.py \
  GET /api/v1/sc/summary --param site_url=https://example.com/

python3 /home/dunc/.codex/skills/live-search-console-data/scripts/refreshagent_api.py \
  GET /api/v1/sc/query --param site_url=sc-domain:example.com --param date_range=30d

python3 /home/dunc/.codex/skills/live-search-console-data/scripts/refreshagent_api.py \
  GET /api/v1/sc/keyword-position --param site_url=sc-domain:example.com --param keyword="example keyword"

python3 /home/dunc/.codex/skills/live-search-console-data/scripts/refreshagent_api.py \
  POST /api/v1/proposals/build/start --json '{"site":"https://example.com","audience":"agency"}'
```

Use `--base-url` only when targeting a non-production RefreshAgent host.

## Workflow

1. Run the first-use login/setup command above and wait for it to finish if no saved key is present.
2. Identify the metric source: Search Console (`/api/v1/sc/...`), GA4 (`/api/v1/ga4/...`), clients (`/api/v1/clients`), or proposals (`/api/v1/proposals/...`).
3. If the site or property identifier is unknown, list available resources first with `/api/v1/sc/sites`, `/api/v1/ga4/properties`, or `/api/v1/clients`.
4. Use explicit dates when the user asks for a time period. GSC data can lag by 2-3 days; mention that when interpreting "today" or very recent windows.
5. Inspect `cache.cached` and `cache.age_seconds` before presenting results as fresh.
6. Preserve raw metric meaning: GSC `position` is average search position where lower is better; `position_change` is positive when rank improved.
7. Summarize results in business language, but keep enough raw numbers for auditability.

## Common Endpoints

- `GET /api/v1/sc/sites`: list Search Console sites available to the API key.
- `GET /api/v1/sc/summary`: clicks and impressions for 30d/7d versus previous periods.
- `GET /api/v1/sc/query`: top queries, optional exact `keyword`, date range, and device filter.
- `GET /api/v1/sc/pages`: top pages by clicks.
- `GET /api/v1/sc/keyword-analysis`: top 50 queries for deeper analysis.
- `GET /api/v1/sc/keyword-position`: exact keyword current/previous metrics.
- `GET /api/v1/sc/cannibalization`: query+page conflict check.
- `GET /api/v1/sc/sitemaps`: submitted sitemap status and index counts.
- `GET /api/v1/ga4/properties`: list GA4 properties.
- `GET /api/v1/ga4/summary`: organic active users and sessions.
- `GET /api/v1/ga4/organic-sessions`: organic sessions with date and path filters.
- `GET /api/v1/ga4/landing-pages`: landing pages with conversions.
- `GET /api/v1/ga4/top-events`: top events with conversions.
- `GET/POST /api/v1/clients`: list or create client site mappings.
- `POST /api/v1/proposals/build/start`: start async proposal build; poll returned job URL.
- `POST /api/v1/proposals/build`: synchronous proposal build; prefer async for agents.

For full request/response schemas, read `references/openapi.yaml`.

## GraphQL

RefreshAgent also exposes GraphQL:

- Endpoint: `POST https://refreshagent.com/graphql`
- Header: `X-API-Key: <key>`
- Schema: `GET https://refreshagent.com/graphql/schema`

Prefer REST unless the user specifically asks for GraphQL or a REST endpoint cannot express the needed query.
