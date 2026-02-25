---
name: metengine-data-agent
description: Real-time smart money analytics for Polymarket, Hyperliquid, and Meteora via MetEngine x402 pay-per-request API. Use when tasks require wallet scoring, insider detection, position analysis, market flow, or LP/AMM analytics across these platforms, especially when access requires Solana USDC payment signing instead of API keys.
---

# MetEngine Data Agent

Keep this file small. Load detailed docs only when needed.

## Non-Negotiable Rule

- Never truncate addresses or IDs. Always return full values (EVM hex, Solana base58, condition IDs, token IDs, pool addresses, tx hashes).

## Runtime Workflow

1. Confirm service and pricing:
```bash
curl -sS https://agent.metengine.xyz/health
curl -sS https://agent.metengine.xyz/api/v1/pricing
```
2. Select one platform (`polymarket`, `hyperliquid`, or `meteora`) and load only that platform doc.
3. If payment flow details are needed, load `references/core-runtime.md`.
4. Execute x402 handshake using local Solana wallet (USDC + SOL required).
5. Return results with full IDs and endpoint provenance.

## Progressive Loading Map

Load order (stop as soon as enough context exists):

1. `references/docs-index.json`
2. `references/core-runtime.md` (payment, pricing, errors)
3. One platform file:
- `references/polymarket-endpoints.md`
- `references/hyperliquid-endpoints.md`
- `references/meteora-endpoints.md`

Do not load all platform files unless user explicitly asks for cross-platform aggregation.
Load `references/core-extended.md` only for deep debugging or policy details.

## Remote LLM-Friendly Docs (for hosted usage)

Use raw GitHub URLs when the skill is installed remotely:

- `https://raw.githubusercontent.com/MetEngine/skill/main/references/docs-index.json`
- `https://raw.githubusercontent.com/MetEngine/skill/main/references/core-runtime.md`
- `https://raw.githubusercontent.com/MetEngine/skill/main/references/core-extended.md`
- `https://raw.githubusercontent.com/MetEngine/skill/main/references/polymarket-endpoints.md`
- `https://raw.githubusercontent.com/MetEngine/skill/main/references/hyperliquid-endpoints.md`
- `https://raw.githubusercontent.com/MetEngine/skill/main/references/meteora-endpoints.md`

Example selective fetch:
```bash
curl -sS https://raw.githubusercontent.com/MetEngine/skill/main/references/docs-index.json
curl -sS https://raw.githubusercontent.com/MetEngine/skill/main/references/hyperliquid-endpoints.md
```

## Token Discipline

- Prefer endpoint lookup via `rg`/targeted section reads over loading full files.
- Keep working context to: core + one platform.
- Only pull multi-platform docs if user asks for comparisons, arb, or blended flows.
