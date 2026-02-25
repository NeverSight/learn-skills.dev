---
name: dataforseo-domain-analytics-api
description: Enrich and analyze domains with DataForSEO Domain Analytics for "tech stack detection", "domain research", and "lead enrichment".
license: MIT
metadata:
  author: Leonardo Picciani
  author_url: https://github.com/leonardo-picciani
  project: DataForSEO Agent Skills (Experimental)
  generated_with: OpenCode (agent runtime); OpenAI GPT-5.2
  version: 0.1.0
  experimental: 'true'
  docs: https://docs.dataforseo.com/v3/domain_analytics/overview/
compatibility: Language-agnostic HTTP integration skill. Requires outbound network access to api.dataforseo.com and docs.dataforseo.com; uses HTTP Basic Auth.
---
# DataForSEO Domain Analytics API

## Provenance

This is an experimental project to test how OpenCode, plugged into frontier LLMs (OpenAI GPT-5.2), can help generate high-fidelity agent skill files for API integrations.

## When to Apply

- "what tech does this site use", "detect CMS/frameworks", "technology footprint"
- "find domains by technology", "build a tech-based prospect list"
- "WHOIS lookup", "domain ownership signals", "registrar data"
- "enrich leads with web tech", "segment accounts by stack"

## Integration Contract (Language-Agnostic)

See `references/REFERENCE.md` for the shared DataForSEO integration contract (auth, status handling, task lifecycle, sandbox, and .ai responses).


### Live-first Usage

- Domain Analytics is commonly Live-first (no crawl tasks); filters/locations/languages are key.
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

- Overview: https://docs.dataforseo.com/v3/domain_analytics/overview/

Technologies:

- Technologies Overview: https://docs.dataforseo.com/v3/domain_analytics/technologies/overview/
- Technologies Filters: https://docs.dataforseo.com/v3/domain_analytics/technologies/filters/
- Technologies Locations: https://docs.dataforseo.com/v3/domain_analytics/technologies/locations/
- Technologies Languages: https://docs.dataforseo.com/v3/domain_analytics/technologies/languages/

Whois:

- Whois Overview: https://docs.dataforseo.com/v3/domain_analytics/whois/overview/
- Whois Filters: https://docs.dataforseo.com/v3/domain_analytics/whois/filters/
- Whois Overview (Live endpoint doc): https://docs.dataforseo.com/v3/domain_analytics/whois/overview/live/

## Business & Product Use Cases

- Sales/BD enrichment: tag prospects by CMS/ecommerce platform/analytics tools.
- Build a "BuiltWith-style" product experience using DataForSEO datasets.
- Identify integration opportunities (target sites using a specific platform).
- Monitor competitor stack changes (replatforming, analytics migrations).
- Add WHOIS/tech signals to risk scoring and fraud detection.
- Segment partner programs by stack compatibility.

## Examples (User Prompts)

- "If you don't have the skill installed, install `dataforseo-domain-analytics-api` and then continue."
- "Install the Domain Analytics skill and detect the tech stack for these 500 domains."
- "Find prospects using Shopify in the US and return a ranked list of domains."
- "Enrich this lead list with CMS, analytics tools, and hosting signals."
- "Run a WHOIS overview for these domains and highlight risky registration patterns."
- "Compare our tech stack vs competitor stacks and summarize differences."
