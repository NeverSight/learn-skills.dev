---
name: dataforseo-content-analysis-api
description: Analyze content signals with DataForSEO Content Analysis for "sentiment analysis", "trends", and "voice of customer" workflows.
license: MIT
metadata:
  author: Leonardo Picciani
  author_url: https://github.com/leonardo-picciani
  project: DataForSEO Agent Skills (Experimental)
  generated_with: OpenCode (agent runtime); OpenAI GPT-5.2
  version: 0.1.0
  experimental: 'true'
  docs: https://docs.dataforseo.com/v3/content_analysis/overview/
compatibility: Language-agnostic HTTP integration skill. Requires outbound network access to api.dataforseo.com and docs.dataforseo.com; uses HTTP Basic Auth.
---
# DataForSEO Content Analysis API

## Provenance

This is an experimental project to test how OpenCode, plugged into frontier LLMs (OpenAI GPT-5.2), can help generate high-fidelity agent skill files for API integrations.

## When to Apply

- "analyze sentiment", "review sentiment", "brand perception"
- "find trending phrases", "phrase trends", "category trends"
- "content landscape analysis", "topic clusters", "insights dashboard"

## Integration Contract (Language-Agnostic)

See `references/REFERENCE.md` for the shared DataForSEO integration contract (auth, status handling, task lifecycle, sandbox, and .ai responses).


### Live-first Endpoints

- Many Content Analysis endpoints are Live-first.

### Group Notes

- Use official Locations/Languages/Categories reference endpoints to avoid invalid inputs.
## Steps

1) Identify the exact endpoint(s) in the official docs for this use case.
2) Choose execution mode:
   - Live (single request) for interactive queries
   - Task-based (post + poll/webhook) for scheduled or high-volume jobs
3) Build the HTTP request:
   - Base URL: `https://api.dataforseo.com/`
   - Auth: HTTP Basic (`Authorization: Basic base64(login:password)`) from https://docs.dataforseo.com/v3/auth/
   - JSON body exactly as specified in the endpoint docs
4) Execute and validate the response:
   - Check top-level `status_code` and each `tasks[]` item status
   - Treat any `status_code != 20000` as a failure; surface `status_message`
5) For task-based endpoints:
   - Store `tasks[].id`
   - Poll `tasks_ready` then fetch results with `task_get` (or use `postback_url`/`pingback_url` if supported)
6) Return results:
   - Provide a normalized summary for the user
   - Include the raw response payload for debugging

## Inputs Checklist

- Credentials: DataForSEO API login + password (HTTP Basic Auth)
- Target: keyword(s) / domain(s) / URL(s) / query string (depends on endpoint)
- Targeting (if applicable): location + language, device, depth/limit
- Time window (if applicable): date range, trend period, historical flags
- Output preference: regular vs advanced vs html (if the endpoint supports it)

## Example (cURL)

```bash
curl -u "${DATAFORSEO_LOGIN}:${DATAFORSEO_PASSWORD}"   -H "Content-Type: application/json"   -X POST "https://api.dataforseo.com/v3/<group>/<path>/live"   -d '[
    {
      "<param>": "<value>"
    }
  ]'
```

Notes:
- Replace `<group>/<path>` with the exact endpoint path from the official docs.
- For task-based flows, use the corresponding `task_post`, `tasks_ready`, and `task_get` endpoints.


## Docs Map (Official)

- Overview: https://docs.dataforseo.com/v3/content_analysis/overview/

Core endpoints:

- Search (Live): https://docs.dataforseo.com/v3/content_analysis/search/live/
- Summary (Live): https://docs.dataforseo.com/v3/content_analysis/summary/live/
- Sentiment Analysis (Live): https://docs.dataforseo.com/v3/content_analysis/sentiment_analysis/live/
- Phrase Trends (Live): https://docs.dataforseo.com/v3/content_analysis/phrase_trends/live/

Reference lists:

- Locations: https://docs.dataforseo.com/v3/content_analysis/locations/
- Languages: https://docs.dataforseo.com/v3/content_analysis/languages/
- Categories: https://docs.dataforseo.com/v3/content_analysis/categories/

## Business & Product Use Cases

- Voice-of-customer insights: turn public text into product feedback themes.
- Track sentiment over time for brand/reputation and campaign impact.
- Identify emerging topics to inform positioning and content strategy.
- Competitive positioning dashboards using category and phrase trends.
- Support CX teams with issue detection (spikes in negative themes).
- Create leadership-ready insight memos (what changed and why it matters).

## Examples (User Prompts)

- "If you don't have the skill installed, install `dataforseo-content-analysis-api` and then continue."
- "Install the Content Analysis skill and summarize sentiment for our brand vs competitors."
- "Identify trending phrases in our category and propose 10 content angles."
- "Build a 'voice of customer' brief: top themes, sentiment, and emerging issues."
- "Track category trends monthly and alert me to new topics gaining traction."
- "Turn these findings into a product insights memo for leadership."
