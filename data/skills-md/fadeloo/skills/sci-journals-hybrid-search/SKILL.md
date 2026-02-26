---
name: sci-journals-hybrid-search
description: Supabase edge function sci_search for hybrid search over scientific journal chunks with optional journal/date filters, chunk expansion (extK), and metadata retrieval. Use when integrating or debugging sci_search requests, filters, or result shaping.
---

# SCI Journals Hybrid Search

## Prepare required inputs
- Provide `data` as JSON with `query` and optional `topK`, `extK`, `filter`, `datefilter`, `getMeta`.
- Set `TIANGONG_AI_APIKEY` and send `x-api-key: <TIANGONG_AI_APIKEY>`.

## Send request
- Endpoint: `https://qyyqlnwqwgvzxnccnbgm.supabase.co/functions/v1/sci_search`
- Headers:
  - `Content-Type: application/json`
  - `x-region: us-east-1`
  - `x-api-key: <TIANGONG_AI_APIKEY>`
- Use `assets/example-request.json` as a base payload.

```bash
curl -sS --location --request POST "https://qyyqlnwqwgvzxnccnbgm.supabase.co/functions/v1/sci_search" \
  --header 'Content-Type: application/json' \
  --header 'x-region: us-east-1' \
  --header "x-api-key: $TIANGONG_AI_APIKEY" \
  --data @assets/example-request.json
```

## Interpret response
- Request shape: `{ "query": string, "topK"?: number, "extK"?: number, "filter"?: object, "datefilter"?: object, "getMeta"?: boolean }`
- `extK` expands each `topK` hit by adjacent chunks before/after and merges the context.
- `filter` constrains journal scope; `datefilter` constrains UNIX-second date bounds.
- Success and error shapes:
  - 200 with `{ "data": [...] }` or `[]`
  - 400 when `query` is missing
  - 500 on backend errors

## Troubleshoot quickly
- If unauthorized, verify `TIANGONG_AI_APIKEY` and `x-api-key`.
- If filtering looks wrong, confirm journal names and UNIX-second boundaries.
- If 500 occurs, treat it as backend failure and inspect Supabase function logs.

## References
- `references/env.md`
- `references/request-response.md`
- `references/testing.md`

## Assets
- `assets/example-request.json`
