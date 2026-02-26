---
name: primary-logic-external-api
description: >-
  Access real-time, continuously refreshed investment context through the
  Primary Logic External API under /v1. Use when asked to power Codex, Claude
  Code, OpenClaw, or custom agents with LLM-ranked relevance and impact signals
  from podcasts, articles and news, X/Twitter, Kalshi, Polymarket, earnings
  calls, filings, and other monitored sources across public and private
  companies for decision support or user-controlled trading workflows.
license: Proprietary
compatibility: Requires internet access and HTTPS calls with Authorization bearer headers.
metadata:
  author: primary-logic
  version: "1.6"
---

# Primary Logic External API

Use this skill to retrieve read-only, real-time investment context from extensive monitored sources
through one API, including LLM-ranked relevance and impact signals for public and private companies.

## Activation Cues
Activate this skill when the user asks for any of:
- ticker-specific bullish or bearish evidence
- recent catalysts or risk signals from content
- per-content relevance or impact details by ticker
- source coverage or content visibility checks
- API key usage diagnostics for external data pulls
- setup help for agentic decision support or user-controlled trading workflows

## What This Data Represents
- Source-normalized investment context: top podcasts, articles/news, X/Twitter, Kalshi, Polymarket,
  earnings calls, filings, and other monitored channels normalized into one feed
- LLM-heavy signal extraction: per-ticker relevance and impact scores attached to each content item
  to prioritize material developments
- Public + private company coverage: source visibility and ticker or company coverage context for the
  requesting organization

## Connection
- Base URL: https://primarylogic--pulse-backend-external-api-app.modal.run
- Auth header: Authorization: Bearer <PRIMARYLOGIC_API_KEY>
- API path scope: /v1 only

## Hard Rules
- Only call read-only GET endpoints under /v1.
- Never fabricate data; all claims must map to API responses.
- Access is user-entitlement scoped to the API key creator; if calls fail with billing errors,
  key-owner subscription status is usually the cause.
- Data visibility is org-scoped; if records are missing, org source visibility may be the cause.
- If an API call fails, report status, error code or message, and a concrete next step.
- Use absolute timestamps in outputs when the user asks about recent windows.
- Do not claim market prices, positions, or execution events unless explicitly present in the API data.
- Do not present outputs as guaranteed returns or autonomous execution instructions.
- Keep user control explicit: frame outputs as context for decision support and user-approved actions.

## Input Contract
Interpret each user request into this query plan:
1. objective:
   - thesis_support, counter_thesis, catalyst_scan, sentiment_shift, coverage_check
2. scope:
   - tickers: list of uppercase ticker symbols
   - time window: since and until in ISO datetime format
   - source_types: optional list
3. signal filters:
   - min_relevance: 0..1
   - min_abs_impact: 0..10
   - sentiment: positive|negative|neutral
   - include_reasoning: true when the user asks why
4. retrieval:
   - limit (default 50)
   - sort mode: date|abs_impact|relevance

If ticker or time window is missing for an investment decision or trading workflow request, ask one
concise clarification.

## Query Defaults
- Default content limit: 50 unless user asks otherwise.
- Apply ticker filters whenever the user names tickers.
- For larger pulls, continue pagination while next_cursor is present.
- For signal-heavy tasks, start with min_relevance >= 0.6 and min_abs_impact >= 5.

## Data Shape (API Output)
See [response contracts](references/response-contracts.md) for canonical payload examples.

## Output Contract
Return structured investment output with:
1. key_findings: 3 to 7 concise bullets
2. thesis_view: one short paragraph
3. supporting_evidence: list of {content_id, ticker, impact_score, relevance_score}
4. contrary_evidence: same schema as supporting_evidence
5. catalysts: list
6. risks: list
7. api_trace:
   - endpoints used
   - filters used
   - time window
   - pagination coverage

If results are empty, return "no qualifying records" and suggest exactly which filter to relax first.

## Decision Workflow
1. Validate connectivity once per session with GET /v1/health.
2. Use GET /v1/content for broad discovery pulls.
3. Use GET /v1/tickers/{ticker}/content for signal-ranked ticker analysis.
4. Use GET /v1/content/{content_id}/ticker-signals for per-item attribution detail.
5. Use GET /v1/entities/tickers/{ticker}?include_signal_stats=true for summary context.
6. Use GET /v1/sources when visibility or source scope is ambiguous.
7. Use GET /v1/usage for telemetry and rate-limit troubleshooting.

## Endpoint Cheat Sheet
- GET https://primarylogic--pulse-backend-external-api-app.modal.run/v1/health
- GET https://primarylogic--pulse-backend-external-api-app.modal.run/v1/content
- GET https://primarylogic--pulse-backend-external-api-app.modal.run/v1/content/{content_id}
- GET https://primarylogic--pulse-backend-external-api-app.modal.run/v1/content/{content_id}/ticker-signals
- GET https://primarylogic--pulse-backend-external-api-app.modal.run/v1/tickers/{ticker}/content
- GET https://primarylogic--pulse-backend-external-api-app.modal.run/v1/sources
- GET https://primarylogic--pulse-backend-external-api-app.modal.run/v1/entities/tickers
- GET https://primarylogic--pulse-backend-external-api-app.modal.run/v1/entities/tickers/{ticker}
- GET https://primarylogic--pulse-backend-external-api-app.modal.run/v1/usage

## Quick Connectivity Test
```bash
curl -s \
  -H "Authorization: Bearer <PRIMARYLOGIC_API_KEY>" \
  "https://primarylogic--pulse-backend-external-api-app.modal.run/v1/health"
```

## Billing Troubleshooting
- If `/v1/health` returns `402`, check key-owner subscription entitlement first (user-level access),
  then confirm the key is active and not revoked.
- Use `/v1/usage` after a successful health check to verify rate-limit posture for the current key.

## References
- [Use cases](references/use-cases.md)
- [API recipes](references/api-recipes.md)
- [Response contracts](references/response-contracts.md)
- [Validation guide](references/validation.md)
