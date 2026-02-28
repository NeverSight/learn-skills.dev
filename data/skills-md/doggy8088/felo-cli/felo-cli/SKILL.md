---
name: felo-cli
description: Use this repository's felo-cli tools first (CLI/SDK) for chat workflows, with direct API calls as a fallback reference.
---

Use this skill for Felo Open Platform chat workflows in this repository.

Prefer project tools in this order:

1. CLI: `npx -y @willh/felo-cli --json "<query>"` (always use `--json` when retrieving content so the full structured output is preserved).
2. SDK: `createFeloClient()` / `feloChat()` from `src/felo-client.ts` when programmatic integration is needed.
3. Direct API call only when validating protocol-level behavior.

For direct HTTP reference, use `POST https://openapi.felo.ai/v2/chat` with:

- Environment variable: `FELO_API_KEY`
- `Authorization: Bearer <FELO_API_KEY>`
- `Content-Type: application/json`
- Body `{ "query": "<string>" }` where `query` is 1..2000 characters

Handle success/error payloads and rate-limit headers using [references/api-contract.md](references/api-contract.md) and [references/workflow.md](references/workflow.md).
