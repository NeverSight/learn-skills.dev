---
name: keyword-planner
description: Get keyword ideas, average monthly search volume, competition, and bid ranges from the local Google Ads Keyword Planner CLI. Use when Codex needs live keyword demand data from Google Keyword Planner for seed keywords or a seed URL, needs JSON keyword idea exports for SEO prioritization, needs country/language-specific demand checks, or needs to exclude already-covered content from keyword research.
---

# Keyword Planner

## Overview

Use the local `keyword-planner` command to pull Google Keyword Planner ideas and search-volume metrics directly from the Google Ads API. The CLI calls Google's `KeywordPlanIdeaService.GenerateKeywordIdeas`, which is the API equivalent of the Keyword Planner flow in the Google Ads UI. Prefer this skill when the user asks for keyword volume, keyword ideas, demand validation, CPC/bid ranges, or a keyword list grounded in Keyword Planner rather than SERP estimates or memory.

Google does not charge a separate per-call fee for normal Google Ads API usage, but calls are governed by the developer token's access level and daily operation limits. The user still needs an eligible Google Ads account and approved API access.

## Quick Start

Use JSON output by default so results can be filtered, sorted, and summarized reliably:

```bash
keyword-planner --keywords "seo tools" "keyword research" --output json
```

Use a URL seed when the user wants ideas from an existing page or competitor page:

```bash
keyword-planner --url "https://example.com/page" --output json
```

If sandbox policy requires approval for network/API access, request escalation before running the command. The command calls the Google Ads API.

## Inputs

Collect or infer:

- Seed keywords with `--keywords`, or one seed URL with `--url`.
- Optional `--customer-id` if `GOOGLE_ADS_CUSTOMER_ID` is not already configured.
- Optional `--location-ids`; default is `2840` for the United States.
- Optional `--language-id`; default is `1000` for English.
- Optional existing-content spreadsheet path for exclusion.

Ask for missing seeds if the user provides neither keywords nor a URL. Do not ask for credentials unless the command fails or the user has not configured a Google Ads customer ID.

## Access and Credentials

There is no simple "Keyword Planner API key." The required access credential is a Google Ads API developer token, plus authentication credentials for the Google Ads account the CLI should query.

To get access:

1. Create or choose a Google Ads manager account. The API Center is available from manager accounts, not ordinary client accounts.
2. Open the Google Ads API Center at `https://ads.google.com/aw/apicenter` while signed in to that manager account.
3. Complete the API Access form and accept the terms.
4. Copy the developer token shown in API Center after Google grants access. New tokens may start with Explorer or Test access before Basic or Standard access is approved.
5. Create authentication credentials for the CLI. This local wrapper is written for service-account JSON credentials, so place `google-key.json` where the CLI can find it or pass `--key-file`.
6. Set the customer ID and developer token:

```bash
GOOGLE_ADS_CUSTOMER_ID=1234567890
GOOGLE_ADS_DEVELOPER_TOKEN=your-developer-token
```

The CLI expects:

- Google Ads API access with service-account credentials.
- `GOOGLE_ADS_CUSTOMER_ID` in `.env` or `--customer-id`.
- Developer token in `GOOGLE_ADS_DEVELOPER_TOKEN` or as `developer_token` inside `google-key.json`.
- `google-key.json`, unless a different path is passed with `--key-file`.

If credentials fail, report the exact missing item or Google Ads API error. Do not fabricate volume, CPC, or competition data as a fallback.

## Existing-Content Exclusion

By default, the CLI excludes matching ideas when `outputs/lindy_titles.csv` exists. This is useful for net-new content planning but can hide keywords the site already covers.

Use explicit exclusion when the user provides an inventory of existing pages:

```bash
keyword-planner --keywords "crm software" --exclude-existing-content exports/pages.csv --output json
```

Disable exclusion when the user wants the full Keyword Planner universe, including ideas already covered:

```bash
keyword-planner --keywords "crm software" --no-exclude-existing-content --output json
```

## Location and Language

The defaults are United States and English. Override location when the user names a country or market:

```bash
keyword-planner --keywords "accounting software" --location-ids 2826 --language-id 1000 --output json
```

Common location IDs:

- `2840`: United States
- `2826`: United Kingdom
- `2124`: Canada
- `2036`: Australia

If the requested market is not one of these, look up the Google Ads geo target constant ID or ask the user for it.

## Workflow

1. Decide whether the request needs live Keyword Planner data. If yes, run the CLI instead of relying on memory.
2. Use `--output json` unless the user explicitly asks for a table.
3. Include `--no-exclude-existing-content` when the user asks for all ideas or volume checks for known terms.
4. Sort and group results according to the user goal:
   - Demand validation: preserve the exact seed and closest variants first.
   - Content planning: prioritize relevant, higher-volume, lower-competition ideas.
   - Paid-search or commercial research: include competition and top-of-page bid ranges.
5. Report the filters used: seed type, location IDs, language ID, and whether existing-content exclusion was on.

## Output Fields

The JSON output contains:

- `keyword`
- `avg_monthly_searches`
- `competition`
- `competition_index`
- `low_top_of_page_bid_micros`
- `high_top_of_page_bid_micros`

Convert bid micros to currency units when presenting CPC-style ranges: `1,000,000` micros equals `1.00`.

## Final Answer

Lead with the actionable read, not the raw dump. Include a compact table with keyword, volume, competition, and bid range when useful. Mention any failed API calls, missing credentials, unavailable markets, or filters that may have removed results.
