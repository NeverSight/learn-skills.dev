---
name: dify-knowledge-base-search
description: Dify dataset retrieve API for knowledge base chunk search/testing. Use when integrating or debugging Dify knowledge base retrieval requests, retrieval_model options, or response shaping.
---

# Dify Knowledge Base Search

## Prepare required inputs
- Provide `data` as JSON containing `query` and optional `retrieval_model.top_k`.
- Read these env vars:
  - `DIFY_API_BASE_URL`: base API URL and include `/v1` (example: `https://api.dify.ai/v1`).
  - `DIFY_DATASET_ID`: target dataset ID.
  - `DIFY_API_KEY`: send as `Authorization: Bearer <DIFY_API_KEY>`.

## Send request
- Endpoint: `${DIFY_API_BASE_URL}/datasets/${DIFY_DATASET_ID}/retrieve`
- Headers:
  - `Content-Type: application/json`
  - `Authorization: Bearer <DIFY_API_KEY>`
- Use `assets/example-request.json` as the payload template.

```bash
curl -sS --location --request POST "$DIFY_API_BASE_URL/datasets/$DIFY_DATASET_ID/retrieve" \
  --header 'Content-Type: application/json' \
  --header "Authorization: Bearer $DIFY_API_KEY" \
  --data @assets/example-request.json
```

## Interpret response
- Request shape: `{ "query": string, "retrieval_model"?: { "top_k": number } }`
- Success shape: 200 with `{ query, records: [...] }`
- If `records` is empty, increase `retrieval_model.top_k` moderately and retry.

## Troubleshoot quickly
- If auth fails, verify `DIFY_API_KEY` and `Authorization` header format.
- If route fails, verify `DIFY_API_BASE_URL` includes `/v1`.
- If results are low quality, refine `query` and tune `top_k`.

## References
- `references/env.md`
- `references/request-response.md`
- `references/testing.md`

## Assets
- `assets/example-request.json`
