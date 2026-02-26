---
name: process-hybrid-search
description: Execute and troubleshoot Supabase edge function `process_hybrid_search`, which rewrites process descriptions and calls `hybrid_search_processes` with optional filters. Use when validating process query/filter behavior, tuning retrieval prompts, or debugging auth, embedding, and RPC failures.
---

# Process Hybrid Search

## Run Workflow
1. Set `TIANGONG_LCA_APIKEY` or pass `--token`.
2. Execute `scripts/run-process-hybrid-search.sh` with a request JSON file.
3. Confirm response shape, then debug with focused references.

## Commands
```bash
scripts/run-process-hybrid-search.sh --dry-run --token "$TIANGONG_LCA_APIKEY"
scripts/run-process-hybrid-search.sh --token "$TIANGONG_LCA_APIKEY"
scripts/run-process-hybrid-search.sh --data ./assets/example-request.json --token "$TIANGONG_LCA_APIKEY"
```

## Fast Triage
- `400`: missing or invalid `query`.
- `500`: embedding provider or `hybrid_search_processes` RPC failure.
- Empty `data`: query/filter mismatch; inspect generated retrieval query and filter structure.

## Load References On Demand
- `references/env.md`: auth, region, and endpoint overrides.
- `references/request-response.md`: payload contract and RPC expectations.
- `references/prompts.md`: query-rewrite prompt constraints.
- `references/testing.md`: smoke test checklist.
