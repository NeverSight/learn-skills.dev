---
name: FarmDash Supply Master
description: "Use when comparing lending and yield pools by net expected APY, TVL depth, stablecoin and impermanent-loss risk. Read-only; deposits need user-signed approval."
tags: ["defi","defi-yield","yield-farming","yield-aggregator","apy-comparison","aave","lido","curve","stablecoin-yield","liquidity-pools","defi-analytics","yield-optimization","impermanent-loss","tvl-analysis","reward-token-risk","openclaw","ai-agent","mcp","web3","farmdash"]
author: FarmDash Pioneers (@Parmasanandgarlic)
homepage: https://www.farmdash.one/agents
version: "1.1.2"
icon: vault
env:
  FARMDASH_API_KEY:
    description: "Optional Bearer token for higher FarmDash limits."
    required: false
metadata: {"openclaw":{"homepage":"https://www.farmdash.one/agents","skillKey":"farmdash-supply-master","primaryEnv":"FARMDASH_API_KEY","execution":"read-only-yield-selection"}}
---

# FarmDash Supply Master

> Use this skill when parking capital: comparing yield pools by net expected return, not headline APY — including stables, LP risk, and data quality.

Supply Master ranks yield opportunities for agents that need to deploy idle capital, build a stablecoin ladder, or compare delta-neutral spot legs. It is intentionally read-only.

## Tool

### `compare_yields`

Inputs:

- `chains`: optional chain filter.
- `assets`: optional symbols such as `USDC`, `ETH`, `SOL`.
- `projects`: optional protocol filter.
- `riskPreference`: `conservative`, `balanced`, or `aggressive`.
- `minTvlUsd`: minimum pool depth.
- `stableOnly`: restrict to stablecoin pools.
- `limit`: max results.

The tool uses the DeFiLlama yield dataset at runtime. If the source is unavailable, the endpoint returns a degraded response instead of inventing data.

## Ranking Logic

Supply Master does not rank by APY alone. `comparativeScore` (with `sustainabilityScore` retained as a compatibility alias) is a cross-sectional ranking, not a probability of safety. Version `yield_quality_v2` considers:

- TVL depth.
- APY range and whether APY looks unusually high.
- stablecoin exposure.
- impermanent-loss risk.
- exposure category.
- the user's risk preference.
- base APY versus reward-token APY and the share dependent on incentives.
- available 1-day, 7-day, and 30-day APY changes, historical sigma, and observation count.
- explicit penalties when history or data quality is unavailable.

Agent rules:

- Rank net expected yield, not headline APY. Subtract execution, bridge, withdrawal, hedging, and monitoring costs over the intended holding period.
- Treat reward-heavy APY as decay-prone and mark-to-market the reward token separately.
- Treat stablecoin pools as credit/depeg exposure, not cash equivalents.
- Do not infer protocol safety from TVL. Review contract, oracle, admin, bridge, redemption, liquidity, and incident risk separately.
- Missing history, underlying-token identity, exit terms, or reward composition lowers confidence; it never becomes zero risk.

### History Gate Before Ranking
Before comparing base/reward APY, require 1-day, 7-day, and 30-day APY changes, historical sigma, and observation count. When history, token identity, exit terms, or reward composition is missing, lower confidence, apply the explicit data-quality penalty, and never promote the pool to the core rung.
- When APY is high but TVL is thin, history is short, reward share is high, or IL risk is present, describe it as speculative rather than core deployment.

### Ladder Position Sizing Rule
Place only `conservative`-passing pools in the core rung. Pools flagged speculative by thin TVL, short history, high reward-token share, or IL risk go only in the outer rung at a reduced size, with the reward token marked-to-market separately and a downside case computed with reward APY at zero plus withdrawal friction.

## Standard Flow

### Stablecoin Ladder Recipe
For idle stables found via Wagon Steward: run `compare_yields` three times with `stableOnly: true` and `riskPreference` set to `conservative`, then `balanced`, then `aggressive`, holding `chains`, `assets`, and `minTvlUsd` constant. Assign one rung per preference; rank each rung by net expected yield after execution, bridge, withdrawal, hedging, and monitoring costs over the intended holding period. Treat every rung as credit/depeg exposure, never cash. Discard any rung with unresolved critical data before Camp Guard review.

1. Use Wagon Steward to find idle assets.
2. Call `compare_yields` with the user's chain, asset, TVL, and risk filters.
3. Compare base/reward APY, APY stability, data depth, TVL, IL, and exit constraints; discard pools with unresolved critical data.
4. Filter out pools that conflict with the user's protocol, chain, asset, stablecoin, bridge, or jurisdiction limits.
5. Compute holding-period net edge and a downside case (reward APY to zero, stablecoin depeg, and withdrawal friction where applicable).
6. Use Camp Guard before any approval or deposit route.

### Deposit Handoff Checklist
Hand every selected pool to Camp Guard with its chain, protocol, asset, bridge, and jurisdiction limits already filtered, plus the holding-period net edge and downside case (reward APY to zero, stablecoin depeg, withdrawal friction). Proceed only to Signal Architect `resolve_defi_intent` when a supported adapter can produce real calldata.
7. Use Signal Architect's `resolve_defi_intent` only when a supported adapter can produce real calldata.

## Disclaimers

Yield changes constantly. APY is not guaranteed, rewards may dilute, smart contracts can fail, and stablecoins can depeg. Supply Master provides ranking data, not financial advice.

**Install:** Copy this file into your OpenClaw workspace, or fetch `https://www.farmdash.one/openclaw-skills/farmdash-supply-master/SKILL.md`.

**Companion skills:** FarmDash Wagon Steward, FarmDash Camp Guard, FarmDash Signal Architect, FarmDash Trail Marshal.

**Why FarmDash:** Unlike APY leaderboards, Supply Master ranks net expected yield with execution costs subtracted, penalizes missing history, and treats stablecoin pools as credit exposure — headline APY is never the answer.

**FarmDash:** [DeFi yield farming intelligence](https://www.farmdash.one/)
**Agent Hub:** [FarmDash DeFi yield intelligence for agents](https://www.farmdash.one/agents)
**OpenAPI Spec:** [FarmDash API Schema](https://www.farmdash.one/agents/openapi.yaml)
**MCP Config:** [FarmDash MCP Server](https://www.farmdash.one/.well-known/mcp.json)

<!-- farmdash-canonical-links:start -->

## Official FarmDash Links

- [FarmDash DeFi intelligence website](https://www.farmdash.one/)
- [FarmDash Agent Hub](https://www.farmdash.one/agents)
- [Canonical FarmDash Supply Master skill manual](https://www.farmdash.one/openclaw-skills/farmdash-supply-master/SKILL.md)
- [Agent integration documentation](https://www.farmdash.one/docs)
- [Live agent capability status](https://www.farmdash.one/api/v1/agent/status)
- [OpenAPI contract](https://www.farmdash.one/agents/openapi.yaml)
- [MCP discovery manifest](https://www.farmdash.one/.well-known/mcp.json)
- [Fees and commercial terms](https://www.farmdash.one/fees)
- [Security and authority boundaries](https://www.farmdash.one/security)

<!-- farmdash-canonical-links:end -->
