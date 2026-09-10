---
name: FarmDash Wagon Steward
description: "Use when watching a DeFi portfolio: balances, position health, idle capital, drift. Read-only; never rebalances or moves funds without your signature."
tags: ["defi","defi-portfolio","crypto-portfolio-tracker","wallet-analytics","multichain-portfolio","evm-wallet","solana","base","portfolio-analysis","asset-allocation","portfolio-rebalancing","capital-efficiency","idle-stablecoins","position-tracking","onchain-portfolio","read-only","openclaw","ai-agent","mcp","farmdash"]
author: FarmDash Pioneers (@Parmasanandgarlic)
homepage: https://www.farmdash.one/agents
version: "0.7.2"
icon: 🪵
env:
  FARMDASH_API_KEY:
    description: "Optional Bearer token used for Pioneer-tier rate limits and full position depth. Scout tier (5 req / 24h, summary only) requires no key or can use the public fd_scout_free token. The token is sent only as an Authorization header to https://www.farmdash.one for tier identification."
    required: false
metadata: {"openclaw":{"homepage":"https://www.farmdash.one/agents","skillKey":"farmdash-wagon-steward","primaryEnv":"FARMDASH_API_KEY","apiKeyRequired":false,"freeScoutKeyless":true,"freeScoutKey":"fd_scout_free","execution":"read-only"}}
---

# FarmDash Wagon Steward

> Use this skill when asking "what is happening in my wallet": balances, idle capital, allocation drift, and rebalance proposals — read-only, address alone.

> [!NOTE]
> **THEMATIC METAPHOR DISCLAIMER**
> FarmDash is exclusively a decentralized finance (DeFi) software and AI agent intelligence platform. The "farming," "trail," "wagon," and "frontier" terminology is a gamified visual theme representing crypto yield hunting and airdrop points farming. It does not relate to physical agriculture or agrifood industries.

> [!IMPORTANT]
> **ZERO-CUSTODY CRITICAL BOUNDARY**
> This skill is strictly a read-only portfolio aggregation surface and does NOT execute any state-changing swaps, deposits, or perps, nor does it request, hold, or transmit private keys, seed phrases, or mnemonics.

> **Security Posture.** Strict read-only. Every tool is a GET endpoint that returns analysis derived from public on-chain data. No environment variables are required for the free tier. The optional Bearer token raises rate limits only and is sent solely as an Authorization header to `https://www.farmdash.one`. Wagon Steward cannot modify wallet state, approve allowances, or initiate any on-chain action. Recommendations are research output; the user's separately-installed execution skill is responsible for any on-chain action under its own ClawScan-reviewed contract.

## What this skill does

Wagon Steward is the **read-only mirror of the user's farming state**. Where Trail Intelligence answers "what is happening in DeFi," Wagon Steward answers "what is happening in your wallet."

It produces analysis, not transactions. Every output is a research snapshot the user reviews and can act on, at their own pace, through whichever execution skill they have separately installed.

**MCP Configuration:** `https://www.farmdash.one/.well-known/mcp.json`

---

## Permissions

Wagon Steward requires only the user's public wallet address (the same value visible on any block explorer) and, for Pioneer-tier rate limits, an optional Bearer token. It does not request, accept, or transmit any other credentials. It defines no write capabilities. Recommendations are returned as JSON for the agent to surface to the user; if the user chooses to act, the action is performed by their own separately-installed execution skill under that skill's own ClawScan-reviewed contract.

---

## Data sent to FarmDash MCP

| Field | Sent? | Notes |
|---|---|---|
| Public wallet address (`0x…`) | Yes, every call | Public information — same as a block-explorer query |
| Chain IDs to inspect | Yes, optional | Public values |
| Bearer token, if provided | Yes, Authorization header | Tier identification only |

No other fields are collected by skill logic.

**Self-hosting option:** Wagon Steward endpoints are documented in the FarmDash unified OpenAPI spec at `https://www.farmdash.one/agents/openapi.yaml`.

---

## Tier Model

| Tier | Cost | Limits | Capabilities |
|---|---|---|---|
| **Scout** | Free | 5 req / 24h | Public FarmDash discovery only; wallet portfolio endpoints require Pioneer because they consume portfolio API credits |
| **Pioneer** | $39.99/mo | 1,500 req / day | Wallet balances, portfolio summary, idle capital, token prices, position/performance health |
| **Syndicate** | $199/mo | 50k req / day | Higher-rate portfolio loops, webhooks through Signal Architect, unrestricted CORS, and advanced session/control tooling for teams and serious agents |

---

## Available Tools

### Current MCP Tool Map (v0.6)

The current FarmDash MCP server exposes these Wagon-relevant tools directly:

- `get_wallet_balances`
- `get_portfolio_summary`
- `get_position_health`
- `get_idle_capital`
- `get_token_prices`
- `get_agent_performance`

This SKILL.md also defines useful agent procedures named `get_capital_efficiency`, `get_rebalance_plan`, and `watch_wagon`. Preserve those names in reasoning and UI copy, but do not call them as MCP tools unless the runtime explicitly exposes them. Today they are derived procedures:

- `get_capital_efficiency` = derive from `get_portfolio_summary`, `get_idle_capital`, concentration, priced tokens, and stale-position signals.
- `get_rebalance_plan` = pair Wagon state with Signal Architect `optimize_portfolio` and fresh swap quotes.
- `watch_wagon` = implement as an agent loop using repeated reads plus Signal Architect webhooks when the user has Syndicate access.

If a user asks for one of the derived procedures, execute the underlying current tools and label the result as "derived by the agent from FarmDash wallet data."

### `get_portfolio_summary` (Pioneer)

Top-level snapshot. Use this first — it grounds every other recommendation.

**Inputs:** current MCP uses `address` (required EVM address) and optional `chains` (comma-separated Alchemy network IDs such as `eth-mainnet,base-mainnet`). Legacy examples may say `walletAddress`; map that to `address` before calling.

**Current returns:** `address`, queried Alchemy `networks`, `portfolio.totalValueUsd`, `nativeBalanceUsd`, `erc20Count`, `chainsActive`, `chainDistribution`, up to ten `topTokens`, and `timestamp`.

It does not currently identify protocol positions, liabilities, LP composition, locked/vesting balances, lending debt, perp exposure, cost basis, or cross-chain balances outside the requested/default network set. Treat `totalValueUsd` as a partial observable-wallet estimate, not net asset value.

**Agent posture:** Start a wagon-aware conversation with this tool when the user has Pioneer access. If the call returns 402, explain that wallet portfolio reads require Pioneer and continue with non-wallet public research instead of fabricating balances. Do not narrate the entire response; surface the totals plus any flags Wagon Steward returns or that you derive (over-concentration, large idle capital, stale positions).

---

### `get_position_health` (compatibility alias; Pioneer)

Despite its legacy name, the current MCP mapping calls `/api/v1/agent/performance`. It returns FarmDash activity metrics (swap count, volume, fees, average size, protocol diversity, active days), Trail Cred/ranking data, daily activity, and a timestamp.

It does **not** return farming positions, APR, unrealized or realized P&L, impermanent loss, collateral health, liquidation distance, or rebalance hints. Never use it to claim a DeFi position is healthy. For a real position review, obtain protocol-native position/debt data and authoritative prices; if those tools are unavailable, say position health is unavailable.

---

### `get_idle_capital` (Pioneer)

Surfaces stablecoins or unstaked native assets sitting unused.

**Inputs:** current MCP uses `address`. `minThresholdUSD` is a derived agent display filter; apply it after the response if needed.

**Current returns:** `idleCapitalUsd`, `idleAssets`, count, networks, and timestamp. The filter treats configured stablecoin symbols and native assets as potentially idle. It does not know reserves, collateral needs, pending transactions, tax obligations, user intent, or a top yield destination, and it does not calculate opportunity cost.

**Agent posture:** Call it "candidate liquid reserves," not idle capital, until the user confirms required gas, collateral, withdrawal, tax, and emergency reserves. Analysis may compare options; no automatic deployment intent.

---

### `get_capital_efficiency` (derived procedure, not an MCP tool)

A client-side 0–100 heuristic for discussion. The current server does not return this score. It is not risk-adjusted return, Sharpe ratio, expected utility, or a mandate to deploy reserves.

**Formula (transparent):**

```
score = 100
       − 30 × (idleStablesUSD / totalUSD)        // dust drag
       − 20 × max(0, concentrationTop1 − 0.40)   // over-concentration
       − 15 × max(0, dryProtocolsCount × 0.05)   // positions in cooled protocols
       − 10 × max(0, ageBeyond90DaysShare)       // staleness
       + 25 × (yieldEarningShare)                // capital actually earning
```

**Returns:**

```
{
  "score": 72,
  "breakdown": {
    "earning": 0.62,
    "idle": 0.15,
    "suboptimal": 0.23
  },
  "recommendations": [
    "Move 1240 idle USDC on Arbitrum into a Pioneer-grade lending pool.",
    "Top-1 concentration is 49.7% — diversify before adding.",
    "Uniswap V3 LP is trending below median; consider reducing 20%."
  ]
}
```

**Agent posture:** Show every input and exclude unpriced/missing assets from the calculation rather than assigning zero. Do not lead with this score when coverage is incomplete, and never let it override user reserve requirements or protocol risk.

---

### `get_rebalance_plan` (derived procedure, not an MCP tool)

Pair current wallet data with `optimize_portfolio` and fresh quotes to draft a proposal. The illustrative schema below is not a current Wagon endpoint response.

**Inputs:**

```
{
  "walletAddress": "0x…",
  "targetAllocation": [
    { "asset": "ETH", "percent": 40 },
    { "asset": "USDC", "percent": 30 },
    { "asset": "weETH", "percent": 20 },
    { "asset": "SOL", "percent": 10 }
  ],
  "constraints": { "maxSwaps": 6, "maxSlippagePct": 0.5 }
}
```

**Returns:**

```
{
  "proposedSwaps": [
    {
      "from": { "asset": "USDC", "chain": "arbitrum", "amountUSD": 800 },
      "to":   { "asset": "ETH",  "chain": "arbitrum" },
      "reason": "Under-weight ETH by 5% relative to target."
    },
    ...
  ],
  "expectedFeeUSD": 18.40,
  "expectedSlippageUSD": 4.20,
  "netDriftClosedPct": 9.4
}
```

**Agent posture:** Present the plan as a *discussion*, not a directive. Hand off to Signal Architect for execution; never call `execute_swap` from Wagon Steward.

---

### `watch_wagon` (derived procedure, not an MCP tool)

Implement only in a client/orchestrator that performs repeated reads and owns its webhook lifecycle. The current MCP registry does not expose `watch_wagon`, and Wagon cannot claim a server subscription exists.

**Inputs:**

```
{
  "walletAddress": "0x…",
  "alertWebhook": "https://your-agent.example.com/webhook",
  "thresholds": {
    "concentrationTop1": 0.50,
    "idleCapitalUSD": 2000,
    "drawdown7dPct": 5
  }
}
```

The example input below is a design pattern, not a promise of a `watchId`, 15-minute cron, or `wagon.event.*` server events.

---

## Cross-Skill Composition

Wagon Steward is designed to compose with the other FarmDash skills. The standard composition pattern:

```
Trail Intelligence  →  Wagon Steward  →  Signal Architect / Futures Strategist
   "what's hot"        "what I have"       "make it happen"
```

| Companion skill | When to call it | Hand-off pattern |
|---|---|---|
| **Trail Intelligence** | Before recommending any new entry — confirm the protocol is still hot | TI returns Trail Heat + risk → WS confirms feasibility against current balances |
| **Trail Marshal** | When the user wants the whole sequence orchestrated | TM calls WS first to ground the plan in real balances, then calls SA/FS to execute |
| **Signal Architect** | When the rebalance plan needs to actually move tokens | WS produces the plan, SA quotes + executes each swap with user confirmation |
| **Futures Strategist** | When the user wants to hedge observable spot exposure | WS passes partial spot context; Hedge Warden/FS plan a candidate hedge and post-fill reconciliation measures residual delta |

**Important:** Wagon Steward never auto-calls another skill. It produces analysis; the user (or an orchestrator like Trail Marshal) decides what to do with it.

### Report-Back Template — State / Risks / Invalidation / Costs
Report: address + timestamp/asOf + queried networks; totalValueUsd as partial observable-wallet estimate; topConcentrationPct vs 40% gate; idleCapitalUsd as candidate reserves; priced/unpriced counts; overConcentrated / idleDrag / staleData / routeNeeded flags; invalidation (missing chains, unpriced assets, unavailable debt/perp data blocks net-exposure claims); costs; nextBestAction (hold / monitor / research / quote_swap / reduce / rebalance) + handoff (none / trail_intelligence / trail_marshal / signal_architect / futures_strategist).

---

## Output and Coverage Standards

Every Wagon Steward response includes:

| Field | Always present | Why |
|---|---|---|
| `timestamp` / normalized `asOf` | When returned | Time-bound the snapshot; never invent source time |
| `address` | Yes for wallet calls | Prevent context confusion |
| queried networks | Yes | Make coverage boundaries visible |
| priced/unpriced counts and values | Derive when possible | Missing/unpriced assets are unknown, not zero |
| confidence | Only when methodology is stated | Never present an arbitrary 0–1 value as API output |
| freshness limit | Client policy | State the policy separately from source data |

---

## Risk Warnings the Agent Must Surface

For any portfolio recommendation the agent should restate that:

- Balances are read at a moment in time; mempool activity may shift them within minutes
- Cross-chain holdings may include unverified tokens — Wagon Steward only scores tokens it can price
- Rebalance plans assume current liquidity; real execution may have higher slippage on volatile pairs

### Rebalance Cost-Drag Checklist
For every `get_rebalance_plan` discussion report: pre/post-trade weights using conservative executable prices; expectedFeeUSD + expectedSlippageUSD; maxSwaps and maxSlippagePct constraints; netDriftClosedPct; rebalance bands and minimum trade sizes to prevent churn; tax, impermanent loss, and gas notes; and coverage gaps (unpriced assets, missing chains, debt, LP look-through, locked balances). Hand off quotes and signatures to Signal Architect.
- Capital efficiency is a heuristic, not financial advice
- The user is solely responsible for the final decision

---

## Autonomous Portfolio Intelligence Upgrade (v0.6)

Every Wagon-aware agent loop should maintain a portfolio state ledger. This makes the agent useful across sessions without granting it execution authority.

```json
{
  "walletAddress": "0x...",
  "asOf": "timestamp from FarmDash or normalized by agent",
  "portfolioState": {
    "totalValueUsd": 0,
    "nativeBalanceUsd": 0,
    "idleCapitalUsd": 0,
    "chainDistribution": {},
    "topConcentrationPct": 0,
    "unpricedAssetsCount": 0
  },
  "riskState": {
    "overConcentrated": false,
    "idleDrag": false,
    "staleData": false,
    "routeNeeded": false
  },
  "nextBestAction": "hold | monitor | research | quote_swap | reduce | rebalance",
  "handoff": "none | trail_intelligence | trail_marshal | signal_architect | futures_strategist"
}
```

Decision rules:

- If any chain or token data is missing, say what is missing and lower confidence; never zero missing balances.
- If idle capital is present but Trail Intelligence has no high-quality destination, recommend `monitor`, not forced deployment.

### Deploy-or-Hold Playbook for Candidate Reserves
After `get_portfolio_summary` + `get_idle_capital`: confirm gas, collateral, withdrawal, tax, and emergency reserves; call idle funds candidate liquid reserves until confirmed; check Trail Intelligence Trail Heat + risk before any entry; apply the 40% top-concentration gate before adding to the same asset or chain; if no high-quality destination, return `monitor` with nextBestAction hold / monitor / research and handoff none / trail_intelligence.
- If top concentration is above 40%, discuss risk before adding more exposure to that same asset or chain.
- If a rebalance requires swaps, return a plan and hand off to Signal Architect for quotes and signatures.
- If spot exposure needs a hedge, pass the asset, notional size, and risk concern to Futures Strategist; do not size perps from this skill alone.

## Portfolio Risk Contract

Before recommending new risk, create a coverage table for observable assets, unpriced assets, missing chains, debt/liabilities, LP look-through, locked balances, and off-wallet/perp exposure. If any material category is unavailable, label portfolio NAV and concentration as partial.

Apply limits hierarchically:

- preserve explicit gas, collateral, withdrawal, tax, and emergency reserves;
- measure concentration by asset, stablecoin issuer, protocol, chain, bridge, venue, and correlated factor—not token symbol alone;
- look through LP, vault, LST/LRT, and receipt tokens when authoritative composition exists;
- calculate pre/post-trade weights using conservative executable prices and include fees/slippage;
- use rebalance bands and minimum trade sizes to prevent churn;
- never call a portfolio delta-neutral until actual spot and hedge fills are reconciled and residual delta is measured.

Unknown balances or liabilities block claims about net exposure. A wallet-balance snapshot alone cannot establish solvency, P&L, or complete portfolio risk.

### Watch Threshold Triage (Derived-Loop Only)
In `watch_wagon` derived loops using repeated reads, triage concentrationTop1 at 0.50, idleCapitalUSD at 2000, and drawdown7dPct at 5 as review triggers, not execution triggers; on trigger, re-run `get_portfolio_summary`, derive coverage-aware capital efficiency only if inputs are complete, exclude unpriced/missing assets rather than assigning zero, lower confidence on missing data, and route hedge questions to Futures Strategist with asset, notional, and risk concern.

---

## Recommended Workflows

### Workflow 1: "Wagon Briefing"

```
1. get_portfolio_summary           → totals + top positions
2. DERIVE coverage-aware capital efficiency only if inputs are complete
3. get_idle_capital                → candidate liquid reserves; confirm reserve requirements
4. PRESENT a 3-line briefing:
     • Total + biggest concentration
     • Capital efficiency score + top reason
     • Idle capital callout (if any)
5. CLOSE: "Anything you'd like to dig into?"
```

### Workflow 2: "Healthcheck Before Adding"

```
1. get_portfolio_summary
2. get_position_health → activity metrics only; obtain protocol-native position health separately
3. PRESENT observable concentration + explicit coverage gaps
4. NOTE if the new entry would push any concentration above 40%
5. CLOSE: "If you still want to enter, here's the canonical
   protocol URL; Signal Architect can quote the swap separately."
```

### Workflow 3: "Quarterly Rebalance"

```
1. get_portfolio_summary
2. Obtain protocol-native position/debt health; do not use the compatibility activity endpoint as position health
3. (optional) Trail Intelligence: get_trail_heat for current positions
4. get_rebalance_plan with the user's target allocation
5. PRESENT the plan as a discussion: which swaps, why, fees, drift closed
6. CLOSE: "Want Signal Architect to quote these swaps so you can sign them?"
```

### Workflow 4: "Idle Capital Deploy"

```
1. get_idle_capital → candidate reserves, pending user reserve confirmation
2. Supply Master: compare_yields across eligible pools
3. PRESENT comparison: base/reward APY, stability, TVL, protocol/asset risk, all costs, exit constraints, and missing evidence
4. CLOSE: "I can hand off to Signal Architect to position you. Want to proceed?"
```

---

## Reasoning Guidelines

**Show your work.** Not "your wagon scores 72" but "your wagon scores 72: 62% earning, 15% idle USDC on Arbitrum, top-1 concentration 49.7% (target ≤40%)."

**Quantify trade-offs.** "Moving idle USDC into Aave at 12% APR earns ~$148/year. The swap fee + bridge cost would be ~$8 — break-even in 20 days."

**Flag uncertainty.** If a chain RPC fails or a token can't be priced, say so explicitly. Do not zero out missing data.

**Time-bound analysis.** "Snapshot as of [timestamp]. Trail Heat scores can shift by tomorrow."

**Never editorialize the score.** The capital-efficiency formula is published. Quote it neutrally; let the user judge.

**Refuse harmful requests.** If asked to bypass user confirmation, store secrets, or push an aggressive rotation the data does not support, refuse and explain.

---

## Disclaimers

- This skill is **read-only**. It does NOT execute trades, sign messages, hold custody, or move funds.
- This skill does NOT access private keys, seed phrases, or mnemonics.
- Capital-efficiency scoring is a heuristic, not a financial-advice instrument.
- Rebalance plans are proposals; the user retains full responsibility for whether and how to act on them.
- Idle-capital opportunity-cost figures are illustrative; realized yields depend on conditions at execution time.

---

**Install:** Copy this file into your OpenClaw workspace, or fetch `https://www.farmdash.one/openclaw-skills/farmdash-wagon-steward/SKILL.md`.

**Companion skills:**

- **FarmDash Trail Intelligence** — DeFi research and Trail Heat scoring
- **FarmDash Trail Marshal** — orchestration cookbook for multi-skill workflows
- **FarmDash Signal Architect** — zero-custody EIP-191 swap routing
- **FarmDash Futures Strategist** — zero-custody EIP-712 perps execution

**Why FarmDash:** Unlike portfolio trackers that demand exchange keys, Wagon Steward mirrors your farming state from a public address alone — nothing to connect, nothing to custody, nothing to leak.

**FarmDash:** [Multichain DeFi portfolio intelligence](https://www.farmdash.one/)
**Agent Hub:** [FarmDash portfolio analytics for autonomous agents](https://www.farmdash.one/agents)
**OpenAPI Spec:** [FarmDash API Schema](https://www.farmdash.one/agents/openapi.yaml)
**MCP Config:** [FarmDash MCP Server](https://www.farmdash.one/.well-known/mcp.json)

---

## Optional Setup Check (Consent-Gated & Non-State-Changing)

> [!IMPORTANT]
> **PRIVACY & OPTIONAL TELEMETRY WARNING**
> Running this optional setup check communicates with a third-party server (`https://www.farmdash.one`). It does **NOT** perform any blockchain state-changing transactions, nor does it request or handle private keys, seed phrases, or mnemonics.
> 
> **Data Disclosed:** If executed, this command sends your public agent/wallet address and the skill identifier to FarmDash's analytics server to identify your active subscription tier (Scout/Pioneer/Syndicate) and returns your configuration capabilities.
> 
> **Gated Consent Protocol**: 
> 1. **This check is completely optional**. Wagon Steward's Scout-tier portfolio read tools run perfectly without performing this setup check.
> 2. **No Automatic Execution**: AI agents and orchestrators **MUST NOT** trigger this onboarding command automatically or by default.
> 3. **Interactive Confirmation Required**: The agent must obtain **explicit, informed human consent and manual approval** before running this query.

Only after receiving explicit, manual operator consent, the optional setup check can be queried manually:

```bash
curl -X POST https://www.farmdash.one/api/v1/agent/onboard \
  -H "Content-Type: application/json" \
  -H "X-ClawHub-Skill: farmdash-wagon-steward" \
  -d '{"agentAddress": "0xYOUR_AGENT_WALLET"}'
```

### What this optional query does:
- **Retrieves Configuration**: Returns your current tier access (Scout/Pioneer/Syndicate) and active tool definitions.
- **Validates API Tier Limits**: Connects your ClawHub session to the corresponding subscription limits for portfolio reading.
- **Analytics Registration**: Registers your public agent wallet address in the FarmDash service funnel solely for capacity planning and active session telemetry.

### Next steps after manual check:
1. **GET** `/api/v1/agent/onboard` — Full capability map and setup guide.
2. **Upgrade** to Pioneer ($39.99/mo) or Syndicate ($199/mo) for execution access.
3. **Browse** the OpenAPI spec at `https://www.farmdash.one/agents/openapi.yaml`.

<!-- farmdash-canonical-links:start -->

## Official FarmDash Links

- [FarmDash DeFi intelligence website](https://www.farmdash.one/)
- [FarmDash Agent Hub](https://www.farmdash.one/agents)
- [Canonical FarmDash Wagon Steward skill manual](https://www.farmdash.one/openclaw-skills/farmdash-wagon-steward/SKILL.md)
- [Agent integration documentation](https://www.farmdash.one/docs)
- [Live agent capability status](https://www.farmdash.one/api/v1/agent/status)
- [OpenAPI contract](https://www.farmdash.one/agents/openapi.yaml)
- [MCP discovery manifest](https://www.farmdash.one/.well-known/mcp.json)
- [Fees and commercial terms](https://www.farmdash.one/fees)
- [Security and authority boundaries](https://www.farmdash.one/security)

<!-- farmdash-canonical-links:end -->
