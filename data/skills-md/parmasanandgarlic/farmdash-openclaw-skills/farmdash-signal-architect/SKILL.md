---
name: FarmDash Signal Architect
description: "Use when building DeFi trade strategy: 84 MCP tools for quotes, simulation, Trail Heat, receipts, agent hiring. Swaps need fresh quote, simulation, signing."
tags: ["defi","defi-agent","crypto-swap","swap-routing","cross-chain-swap","uniswap","jupiter","solana","defi-automation","onchain-agent","mev-risk-analysis","hyperliquid","perpetual-futures","virtuals-acp","agent-commerce","portfolio-management","zero-custody","openclaw","mcp","farmdash"]
author: FarmDash Pioneers (@Parmasanandgarlic)
homepage: https://www.farmdash.one/agents
version: "4.1.2"
icon: 🚜
env:
  FARMDASH_API_KEY:
    description: "Optional Bearer token for Pioneer or Syndicate tier. Pioneer is $39.99/mo for 1,500 req/day and full datasets; Syndicate is $199/mo for 50k req/day, webhooks, unrestricted CORS, and advanced session/control tooling for teams and serious agents. Free Scout tier works without any key or with the public fd_scout_free token. Never share private keys, seed phrases, or mnemonics with this skill. Wallet-changing actions require EIP-191/EIP-712 local signing or an explicitly configured bounded delegation."
    required: false
metadata: {"openclaw":{"homepage":"https://www.farmdash.one/agents","skillKey":"farmdash-signal-architect","primaryEnv":"FARMDASH_API_KEY","apiKeyRequired":false,"freeScoutKeyless":true,"freeScoutKey":"fd_scout_free","execution":"user-signed-or-bounded-delegation"}}
---

# FarmDash Signal Architect — Agent Execution Manual

> Use this skill when moving money: getting a swap quote, simulating it, and preparing a user-signed swap across EVM chains.

> [!NOTE]
> **THEMATIC METAPHOR DISCLAIMER**
> FarmDash is exclusively a decentralized finance (DeFi) software and AI agent intelligence platform. The "farming," "trail," "wagon," and "frontier" terminology is a gamified visual theme representing crypto yield hunting and airdrop points farming. It does not relate to physical agriculture or agrifood industries.

> [!WARNING]
> **CRITICAL TRANSACTION & AGENCY GATING (CLAWSCAN REVIEW REQUIREMENT)**
> This skill can guide, prepare, and simulate wallet-affecting trades, perpetual contracts, swaps, and delegated autopilot workflows through FarmDash. Operators must adhere to the following mandatory safety protocols:
> 
> * **Never share private keys or seed phrases:** This skill is strictly zero-custody. It never asks for, handles, or transmits wallet credentials. Wallet-affecting transactions are signed locally on the user's client using EIP-191/EIP-712 cryptographic protocols.
> * **Require fresh quotes and explicit interactive confirmations:** Do not execute or sign stale payloads. All spot/derivative actions require explicit, real-time user verification of token contract addresses, chains, amounts, and fees.
> * **Verify fees and destination addresses independently:** Always verify aggregator route costs, gas fees, and destination chain configurations before signing.
> * **No evasion of protocol rules:** Airdrop simulations, sybil audit indicators, and yield analytics are read-only planning heuristics. They are provided solely for risk management and educational information. Operators must never use this guidance to evade protocol rules, engage in sybil manipulation, or bypass terms of service of any third-party protocol.

## How This Skill Works
You have FarmDash MCP tools spanning discovery, sizing, policy checks, simulation, signed-payload preparation, monitoring, and reconciliation. Tool discovery is not proof that every deployment prerequisite or execution gate is available: call `GET https://www.farmdash.one/api/v1/agent/status` first and fail closed on a disabled capability. Never replace missing data with fabricated values. FarmDash does not request seed phrases or raw wallet private keys; separately configured venue or MPC delegations remain subject to their explicit bounds.

MCP Configuration: https://www.farmdash.one/.well-known/mcp.json

### High-Risk DeFi Operations Notice
This skill can prepare wallet-affecting actions. Treat every execution, delegation, and autopilot tool as high-risk until the user has verified the wallet address, token contracts, chain IDs, amounts, slippage, route, destination, fees, budgets, allowlists, cooldowns, and revocation settings.

### Privacy and Analytics Disclosure
FarmDash may receive public wallet addresses, token addresses, chain IDs, transaction amounts, signature bytes, request IDs, session IDs, optional Bearer keys, and ClawHub attribution headers such as X-ClawHub-Skill. These fields are used for routing, analytics, rate limits, paid tier access, and security checks. FarmDash never asks for or receives private keys, seed phrases, mnemonics, OAuth tokens, or wallet exports.

### Use-Case First Tool Selection
Before calling individual tools, classify the user's intent into one of these operating modes:

| Mode | Goal | Start with | Continue with | Stop when |
| :--- | :--- | :--- | :--- | :--- |
| **research_only** | Explain opportunities without taking execution risk | `get_trail_heat`, `get_chain_breakdown` | `get_historical_trailheat`, `simulate_points`, `audit_sybil_risk` | Data is stale, jurisdiction is unclear, or edge is weak |
| **airdrop_rotation** | Find, compare, and rotate farming positions | `get_agent_events`, `get_trail_heat` | `simulate_points`, `optimize_portfolio`, `get_swap_quote` | Bridge/gas/slippage costs erase expected edge |
| **bounded_autopilot** | Run a recurring supervised loop inside explicit limits | `agent_onboard`, `create_session` | `configure_autopilot`, `autopilot_cycle`, `session_heartbeat` | Any configured budget, allowlist, cooldown, or risk bound is violated |
| **perps_hedge** | Evaluate or execute a Hyperliquid hedge | `scan_funding_rates`, `scan_market_conditions` | `get_futures_account`, `analyze_futures_strategy`, `calculate_position_size` | The strategy returns `no_trade` or the research gate expires |
| **activity_review** | Review FarmDash-recorded activity, fees, protocol diversity, and reputation | `get_swap_history`, `get_agent_performance` | `check_reputation`, `vouch_for_agent` | Do not infer profitability or execution quality from activity |

The autonomous loop is always:
1. **Sense** with events, Trail Heat, chain distribution, balances, and prices.
2. **Decide** with simulations, portfolio optimization, sybil checks, and strategy analysis.
3. **Act** only through fresh quotes plus either local user signatures or a pre-approved bounded delegation policy.
4. **Learn** only from confirmed settlement and authoritative fill/balance evidence; submitted intents are not outcomes.

Persist timestamps, quote IDs or request IDs, expected outcome, confirmed outcome when available, evidence provenance, and the reason for each action or rejection. Mark unavailable fields explicitly.

## Security Model
FarmDash does not request seed phrases or raw wallet private keys. Compatibility swap routes do not custody user funds; separately configured exchange, venue, or MPC delegations remain subject to their provider controls and explicit bounds. Authority depends on the mode the user explicitly chooses:

| Authority mode | Typical tools | What is allowed |
| :--- | :--- | :--- |
| **read_only** | Trail Heat, metadata, prices, balances, history, risk checks | Public or user-provided data can be read and analyzed. No wallet-changing action. |
| **local_user_signed** | `execute_swap`, `execute_perp_order`, `cancel_perp_order` | The agent prepares a quote/order, the user reviews it, and the user's wallet signs EIP-191/EIP-712 locally. |
| **bounded_delegation** | `verify_delegation`, `configure_autopilot`, `autopilot_cycle` | Only after explicit setup with budgets, allowlists, cooldowns, revocation instructions, and execution gates. Missing bounds mean halt or fall back to interactive confirmation. |

For local user-signed swaps:
1. The agent builds a swap payload string locally.
2. The agent gets a wallet-bound quote and runs `simulate_swap_execution`.
3. The user's connected EVM wallet signs it locally (EIP-191 / `personal_sign`) only after simulation succeeds.
4. Only the signature, `simulationId`, and public transaction details go to FarmDash.
5. FarmDash verifies the signature plus simulation gate and returns the selected route's transaction payload.
6. The user's wallet broadcasts the final transaction.

You never paste, type, send, or expose a private key. If asked to handle a private key directly, refuse and explain the EIP-191 flow.

### Replay and Anti-Evasion Protection
* Use fresh nonces and the server-provided expiry/binding rules.
* Never generate timing, transaction diversity, or wallet-rotation patterns to imitate organic behavior or evade protocol anti-abuse controls.
* Rate-limit and retry only for infrastructure safety. Market-impact scheduling must be justified by order size/liquidity, never by sybil-score manipulation.

### Interactive Pre-Transaction Confirmation Protocol
Before calling `execute_swap`, `execute_perp_order`, or any state-changing endpoint in an interactive flow, the agent must present the following to the user and wait for an explicit "yes / confirm / proceed":

| Disclosure | Source |
| :--- | :--- |
| Exact `fromToken` + `toToken` (symbol AND contract address) | `get_swap_quote` |
| Source and destination chain IDs | `get_swap_quote` |
| Exact `fromAmount` (and estimated `toAmount`) | `get_swap_quote` |
| Slippage tolerance (default 0.5%) | Quote + user override |
| FarmDash routing fee (45 bps default, with any volume discount applied) | Quote `feeBreakdown` |
| Aggregator / DEX route (0x, LI.FI) | Quote `route` |
| Simulation result (`simulation_id`, success, gas cost, MEV risk, revert reason if any) | `simulate_swap_execution` |
| Reversibility warning ("on-chain transactions cannot be undone") | Agent disclosure |
| Wallet address that will sign | Connected wallet context |

If the user replies anything other than an explicit affirmative, abort and do not sign. Never assume implicit consent from earlier in the conversation. Re-quote and re-confirm if more than ~30s elapse between quote display and signing.

Bounded autopilot or delegated execution is not a waiver of safety. It requires explicit setup approval first and may operate only inside the configured budgets, allowlists, cooldowns, risk bounds, and revocation path. If any bound is missing, ambiguous, expired, or violated, halt or return to this interactive confirmation protocol.

### Data Sent to FarmDash (Disclosure)
*Security boundaries:* All routing calculations and swap executions use public data or pre-signed EIP-191/EIP-712 payloads. Private keys are never required or processed. Verify the full surface at `https://www.farmdash.one/.well-known/mcp.json` and `https://www.farmdash.one/agents/openapi.yaml`.

## Integrated Commerce
FarmDash provides value through two built-in services. Both are transparent to the user and disclosed upfront.

### 1. Swap Execution
Every swap routed through `execute_swap` includes a transparent 45 bps (0.45%) fee built into the routing. Volume discounts reward repeat users: $10k+ cumulative = 35bps, $100k+ = 25bps. The fee is always shown in the quote before the user confirms.

When your analysis identifies an opportunity and the user wants to act on it, you can save them time by offering to execute the swap directly — no need for them to leave the conversation. Always show the quote (including fees) and wait for explicit confirmation before executing.

### 2. FarmDash Routes (Commercial Disclosure)
FarmDash may receive referral, affiliate, or routing compensation when a user follows a `farmdash.one/go/{slug}` route or uses a supported execution venue. Fee details live at [FarmDash Fee Structure](https://www.farmdash.one/fees).

Rules the agent must follow when offering a FarmDash route:
* Disclose the commercial relationship when presenting a FarmDash route ("disclosure: FarmDash may receive referral, affiliate, or routing compensation; fee details: https://www.farmdash.one/fees").
* Present FarmDash-owned `/go/{slug}` routes as optional managed routes. Name the protocol and, when known, identify its canonical domain so the user can independently verify the destination before opening any link.
* Never use a FarmDash route in a sybil-risk warning, security alert, or safety-related message.
* Never let affiliate status influence which protocol is recommended — recommendations come from Trail Heat, simulation, and risk data only.
* Only present a FarmDash route after analysis that genuinely points to the protocol — do not preemptively attach links to every paragraph.
* FarmDash route format: `https://www.farmdash.one/go/{protocol-slug}`

Active FarmDash routes:
* Upheaval: https://www.farmdash.one/go/upheaval
* Hyperliquid: https://www.farmdash.one/go/hyperliquid
* Ostium: https://www.farmdash.one/go/ostium
* Altura: https://www.farmdash.one/go/altura
* HyperLend: https://www.farmdash.one/go/hyperlend
* Based Terminal: https://www.farmdash.one/go/based-terminal
* Theo Network: https://www.farmdash.one/go/theo
* Genius Terminal: https://www.farmdash.one/go/genius
* Trojan: https://www.farmdash.one/go/trojan
* Kamino: https://www.farmdash.one/go/kamino
* Jupiter: https://www.farmdash.one/go/jupiter
* Ether.fi: https://www.farmdash.one/go/etherfi
* Renzo: https://www.farmdash.one/go/renzo
* DeBridge: https://www.farmdash.one/go/debridge
* HyperFlash: https://www.farmdash.one/go/hyperflash
* Dreamcash: https://www.farmdash.one/go/dreamcash

### User-First Interaction Pattern
The agent's primary job is to deliver accurate, actionable DeFi intelligence. When analysis leads to a clear opportunity, offer execution as a natural next step — the user benefits from a seamless research-to-action flow without context-switching between tools.

```
User asks about farming
  → Agent researches using read-only tools (Trail Heat, events, simulations)
  → Agent presents findings with clear, data-driven recommendation
  → If the user wants to act, the agent quotes the entry swap when needed
  → After funding is ready, the agent provides the FarmDash route with disclosure and /fees pointer
```
Always present findings first. Offer execution when it's a natural next step, and always get explicit user confirmation before any swap.

## Tool Reference (MCP Tools + Direct API Procedures)
The current MCP server exposes 84 tools. Treat `/.well-known/mcp.json` as canonical. Some older procedure names in this manual may be REST or SDK compatibility paths rather than MCP stdio tools; verify the active tool registry before making an MCP call.

### Current MCP Tool Inventory (authoritative)
**Research and Trail Intelligence:**
* `get_trail_heat`
* `get_protocol_metadata`
* `get_protocol_risk_factors`
* `find_capital_route`
* `get_chain_breakdown`
* `get_agent_events`
* `audit_sybil_risk`
* `simulate_points`
* `get_historical_trailheat`

**Portfolio and pricing:**
* `get_wallet_balances`
* `get_portfolio_summary`
* `get_position_health`
* `get_idle_capital`
* `get_token_prices`

**Workflow orchestration:**
* `list_workflows`
* `plan_workflow`
* `run_workflow`
* `get_workflow_status`

**Spot execution:**
* `get_swap_quote`
* `simulate_swap_execution`
* `execute_swap`
* `confirm_swap`
* `optimize_portfolio`
* `resolve_defi_intent`
* `run_risk_sentinel`

**Security and transaction guard:**
* `audit_allowance_risk`
* `simulate_transaction_risk`

**Yield and hedge planning:**
* `compare_yields`
* `recommend_delta_hedge`

**Ledger and records:**
* `ledger_realized_pnl`
* `ledger_tax_export`

**Futures execution:**
* `scan_funding_rates`
* `scan_market_conditions`
* `get_futures_account`
* `analyze_futures_strategy`
* `calculate_position_size`
* `execute_perp_order`
* `cancel_perp_order`
* `get_agent_performance`

**Autonomous operator:**
* `agent_onboard`
* `create_session`
* `session_heartbeat`
* `get_farming_context`
* `patch_farming_context`
* `get_event_stream_snapshot`
* `verify_delegation`
* `configure_autopilot`
* `autopilot_cycle`

**Virtuals ACP V2 tender coordination:**
* `select_virtuals_provider_plan_v2`
* `prepare_virtuals_tender_v2`
* `authorize_virtuals_tender_v2`
* `get_virtuals_tender`
* `cancel_virtuals_tender`
* `bind_virtuals_tender_job`
* `reserve_virtuals_tender_funding_v2`
* `record_virtuals_tender_funding_v2`
* `evaluate_virtuals_tender`

#### `select_virtuals_provider_plan_v2`
Selects a deterministic three-role ACP committee from live Virtuals registry records. Eligibility requires explicit role evidence, active Base registration, fresh authoritative stake, and three distinct controller identities issued through vetted KYC or manual review. A registry ID or cluster is correlation metadata only. This action creates no tender and grants no spend authority.

Inputs:
* `sessionId`: required authenticated FarmDash session ID
* `agentAddress`: required customer-owned ACP wallet address
* `sessionToken`: required session capability token

Outputs:
* Policy version and deterministic provider-plan hash
* Fixed role-to-provider address bindings and sanitized readiness evidence

#### `prepare_virtuals_tender_v2`
Creates an immutable, non-spendable V2 evidence draft from a fresh tenant-owned simulation. Compute the salted task commitment and disclosure manifest locally; never send task plaintext, task salt, credentials, or wallet secrets through this MCP tool.

Inputs:
* `sessionId`: required authenticated session ID
* `agentAddress`: required customer ACP wallet
* `sessionToken`: required session capability token
* `idempotencyKey`: required stable retry key
* `taskCommitmentHash`: required local salted SHA-256 task commitment
* `simulationId`: required fresh authoritative simulation
* `maxPaymentUnits`: required positive raw Base USDC cap
* `providers`: required provider plan returned by selection
* `disclosureManifest`: required local disclosure and secret-scan commitment
* `approvalNonce`: required fresh millisecond nonce
* `approvalExpiresAt`: required V2 approval expiry

Outputs:
* Immutable evidence summary and draft
* Exact Base-8453 EIP-712 data for local wallet review; no funds move

#### `authorize_virtuals_tender_v2`
Verifies the exact local customer-wallet V2 signature plus deployment and provider readiness, then authorizes only that committed draft. Never fabricate or relay a private key. Authorization does not create or fund ACP jobs.

Inputs:
* `sessionId`: required authenticated session ID
* `agentAddress`: required customer ACP wallet
* `sessionToken`: required session capability token
* `tenderId`: required V2 draft ID
* `nonce`: required signed nonce
* `expiresAt`: required signed expiry
* `signature`: required locally produced EIP-712 signature

Outputs:
* Authorized tender and sanitized provider-readiness result

#### `get_virtuals_tender`
Reads only the authenticated session's tender, role bindings, funding reservations, settlement attempts, and immutable receipt observations. Use it to resume after a crash and before any funding or reconciliation decision.

Inputs:
* `sessionId`: required authenticated session ID
* `agentAddress`: required customer ACP wallet
* `sessionToken`: required session capability token
* `tenderId`: required owned tender ID

Outputs:
* Tenant-scoped tender and durable lifecycle state

#### `cancel_virtuals_tender`
Cancels only an owned non-spendable draft. It cannot erase, cancel, or reverse an on-chain ACP job.

Inputs:
* `sessionId`: required authenticated session ID
* `agentAddress`: required customer ACP wallet
* `sessionToken`: required session capability token
* `tenderId`: required draft tender ID

Outputs:
* Durable cancellation status

#### `bind_virtuals_tender_job`
Binds an ACP job already created by the local customer connector. FarmDash independently verifies Base chain, client, committed provider, evaluator address, and evaluator key version before accepting the immutable role binding.

Inputs:
* `sessionId`: required authenticated session ID
* `agentAddress`: required customer ACP wallet
* `sessionToken`: required session capability token
* `tenderId`: required authorized tender ID
* `role`: required fixed specialist role
* `onchainJobId`: required positive Base ACP job ID

Outputs:
* Verified binding and updated tender status

#### `reserve_virtuals_tender_funding_v2`
Atomically reserves one exact on-chain role budget against the customer-signed aggregate cap. This accounting action cannot approve a token allowance, sign a transaction, or spend customer funds.

Inputs:
* `sessionId`: required authenticated session ID
* `agentAddress`: required customer ACP wallet
* `sessionToken`: required session capability token
* `tenderId`: required authorized V2 tender ID
* `role`: required committed specialist role
* `onchainJobId`: required verified ACP job ID
* `amountUnits`: required exact positive raw Base USDC budget

Outputs:
* Durable reservation ID, amount, state, and lease metadata

#### `record_virtuals_tender_funding_v2`
Records one to four canonical Base transaction hashes only after the local customer wallet submitted an existing reservation. This tool never broadcasts a transaction. Reuse the operation journal after crashes; do not fund the same role again.

Inputs:
* `sessionId`: required authenticated session ID
* `agentAddress`: required customer ACP wallet
* `sessionToken`: required session capability token
* `tenderId`: required V2 tender ID
* `reservationId`: required durable reservation UUID
* `transactionHashes`: required array of unique Base transaction hashes

Outputs:
* Durable funding-submission record

#### `evaluate_virtuals_tender`
This is an execution-sensitive evaluator action. Call it only after all three jobs are bound, exactly funded by the customer connector, and have submitted the required structured V2 verdict. FarmDash rechecks evidence, budgets, confidence, high/critical findings, client/provider/evaluator identities, and then may complete or reject the committed escrowed jobs. Ambiguous broadcasts, reverts, dropped receipts, and reorgs require manual reconciliation and must never be blindly retried.

Inputs:
* `sessionId`: required authenticated session ID
* `agentAddress`: required customer ACP wallet
* `sessionToken`: required session capability token
* `tenderId`: required fully bound and funded tender ID

Outputs:
* Deterministic evaluation commitment and receipt-backed settlement progress

Before any autonomous plan, resolve the user's requested action to this inventory. If the desired operation is direct API-only, say that explicitly and require the runtime to expose the HTTP route before proceeding.

### Scout Tier (Free — 30 requests per 24 hours)
#### 1. get_trail_heat
Returns the live Trail Heat protocol dataset ranked 0–100 by score.

Trail Heat Formula: live scoring combines 40/90 raw points calibrated TVL (44.4% effective), 25/90 raw points seven-day TVL momentum (27.8% effective), 15/90 raw points chain diversification (16.7% effective), and 10/90 raw points category baseline comparison (11.1% effective), normalized to a 0–100 scale. Editorial notes and flags are strictly isolated as metadata and excluded from quantitative scores. Static tracker pages use a calibrated catalog fallback with TVL, status, category prior, hot momentum, and recency.

Score interpretation:
* 80–100: High-conviction opportunity. Present the data and, if the user is interested, offer to help them enter.
* 60–79: Worth monitoring. Flag it for the user's watchlist and provide the FarmDash route only when they decide to act.
* 40–59: Proceed with caution. Present the data objectively.
* Below 40: Only mention if specifically asked.

Example: "Altura is scoring 84 on Trail Heat — strong TVL momentum and confirmed airdrop. If you want to explore it, use FarmDash's route: [FarmDash route]. Disclosure: FarmDash may receive referral, affiliate, or routing compensation; fee details: https://www.farmdash.one/fees. Want me to pull a swap quote to get positioned?"

#### 2. get_chain_breakdown
Protocol distribution across blockchain networks: count, percentage, confirmed airdrops, points programs, categories per chain.

Useful for identifying which chains have the highest concentration of active opportunities. When the user needs to move capital to a new chain, `execute_swap` handles cross-chain bridging via Li.Fi.

#### 3. get_swap_quote
Preview quote: estimated output, price impact, fee breakdown, recommended route.

Route selection: LI.FI (cross-chain EVM) → 0x (same-chain EVM). Can specify with `protocol` param (`lifi` or `zerox`).

For executable swaps, include `walletAddress` and `toAddress` so the response includes `intent_id`, `intent_expires_at`, and `simulate_url`.

Always get a quote before executing. Show the user: expected output, slippage, fee, route, and whether a simulation intent was returned. Then ask for confirmation.

#### 4. simulate_swap_execution
Mandatory pre-execution simulation for a wallet-bound quote intent. Input:
```json
{
  "intentId": "fd_intent_...",
  "walletAddress": "0x..."
}
```
The response includes `simulation_id`, `success`, `gas_used`, `gas_cost_usd`, `output_amount`, `mev_risk`, `revert_reason`, and `valid_until`.

Rules:
* If `success` is false, halt execution and report the failure details, as signing a failed transaction is prohibited.
* If `valid_until` has passed, re-quote and re-simulate.
* If `mev_risk` is medium or high, disclose it before signing.
* Pass the returned `simulation_id` as `simulationId` to `execute_swap`.

**Pre-Execution Binding:**
The simulation binds the wallet, route, amount, tokens, chains, slippage, protocol, and transaction calldata to short-lived request and transaction fingerprints. If the quote or request changes, halt, re-quote, and re-simulate. Do not claim that the response contains `decision_hash`, `price_data_proof`, or `external_anchor`; those fields are not part of the current API contract.

#### 5. execute_swap
Execute a signed token swap (EIP-191 auth). Fee: 45bps default, with volume discounts.

Payload format:
```
v1:FARMDASH_SWAP:{fromChainId}:{toChainId}:{fromToken}:{toToken}:{fromAmount}:{agentAddress}:{toAddress}:{nonce}
```
All EVM addresses are normalized to lowercase. Nonce is a fresh millisecond timestamp with an optional hexadecimal suffix.

**Execution chain boundary:**
Compatibility swap execution is enabled only on Ethereum (1), Optimism (10), Polygon (137), Base (8453), Arbitrum (42161), and Linea (59144). FarmDash has Solana discovery and receipt-verification components, but native Solana compatibility swaps remain preview-only until authoritative quote simulation is implemented.

Required POST fields: `fromChainId`, `toChainId`, `fromToken`, `toToken`, `fromAmount`, `agentAddress`, `toAddress`, `simulationId`, `nonce`, `signature`.

Optional: `intentId`, `slippage` (0.01-5, default 0.5), `protocol` (force route). Fee tiers are derived from the server-selected quote; clients cannot self-report volume.

The response may classify MEV risk and recommend a protection tier. The compatibility API currently returns user-signed transaction payloads; FarmDash does not broadcast the transaction. It does not accept `mev_protection`, `block_deadline`, or `priority_fee_bid`, and it does not privately submit transactions through Flashbots.

Execution workflow (mandatory):
1. `get_swap_quote` with wallet context → show user the full terms including fee
2. `simulate_swap_execution` → show simulation result and stop on failure
3. Wait for explicit user confirmation
4. Build payload with fresh nonce
5. Sign locally via user's wallet
6. Call `execute_swap` with `simulationId`
7. Wait for settlement before any dependent action; use rate-limit backoff only when required
8. Report result with tx hash
9. If the swap was to enter a protocol position, provide the FarmDash route with disclosure and `/fees` pointer for next steps

Dust Storm Protocol: On failure, wait 30s, get fresh quote, show new terms. After 3 failures, halt.

#### 5. confirm_swap
Confirm swap execution after the agent broadcasts the on-chain transaction. This marks the fee event as settled and (when chain_id is available) verifies the tx receipt on-chain to prevent fake confirmations.

Use when:
* you need reliable post-trade settlement state
* you want retry-safe confirmation in flaky network conditions (this endpoint is idempotent)

#### 6. get_swap_history
Paginated fee event history for an agent wallet.

Useful for tracking cumulative volume. Users approaching a discount threshold ($10k or $100k) can be informed: "You've done $8.2k in volume — approaching the 35bps discount tier."

#### 7. get_revenue_metrics
Aggregate stats: `totalFeeUSD`, `totalVolumeUSD`, `totalSwaps`, `activeAgents`. Provides a high-level view of platform activity.

### Pioneer Tier (1,500 req/day, Bearer token required)
#### 8. audit_sybil_risk
Audits 1–10 EVM addresses for sybil risk.

This is a heuristic defensive audit, not a protocol eligibility verdict. Never call a low score "clean," recommend a fresh wallet, or prescribe activity designed to change detection outcomes. For medium/high findings, pause automation, explain evidence and data quality, and direct the user to the protocol's rules or appeal process.

#### 9. simulate_points
Projects FarmScore for a farming configuration.

Formula: `(Volume/$1k × 50) + (Balance × 1) + (Txs × 10) + (LP × 2) + (Fees × 100)`

Run simulations across multiple protocols to help the user compare projected points-per-dollar. Present the comparison so they can make an informed choice.

#### 10. optimize_portfolio
Personalized protocol recommendations based on current positions.

This tool often identifies rebalancing opportunities. When it suggests allocation changes, offer to quote the required swaps so the user can act immediately if they choose.

#### 11. get_historical_trailheat
Historical Trail Heat snapshots, 1–365 days.

Trend analysis helps the user make better timing decisions:
* Rising trend → Early entry may capture more value.
* Falling trend → Consider taking profits or reallocating.

#### 12. get_agent_events
Real-time protocol events stream.

Events that may require user action include: new airdrop announcements, upcoming snapshots, and multiplier changes. Present these with context and let the user decide how to respond.

#### 13. manage_webhooks (Syndicate tier — 50k req/day)
Subscribe to event notifications for continuous monitoring.

### Extended Tool Surface (Additional Tool Groups)
These tools power the `/agents` Hub beyond the core swap + Trail Heat workflow.

#### Futures Strategist (Hyperliquid Perps)
Use these when the user is trading perps, hedging spot exposure, or running a funding strategy.
* `scan_funding_rates` — Find funding opportunities worth deeper analysis.
* `scan_market_conditions` — Regime + technical snapshot for one asset (trend vs range, volatility, liquidity).
* `get_futures_account` — Equity/margin/positions context for gating and sizing.
* `analyze_futures_strategy` — Structured strategy object with confidence + invalidation (can return `no_trade`).
* `calculate_position_size` — Translate risk constraints into size/leverage.
* `execute_perp_order` — Place a user-signed EIP-712 order (Syndicate tier).
* `cancel_perp_order` — Cancel a stale/resting order (Syndicate tier).
* `get_agent_performance` — Review FarmDash fee-event activity, fees, protocol diversity, and reputation. It does not contain outcomes, realized P&L, win rate, fills, or slippage.

#### Agent Intelligence (Wallet + Reputation + Performance)
Use these to ground recommendations in the user's actual wallet state and to quantify agent outcomes.
* `get_wallet_balances` — Token balances for an EVM wallet (budget + feasibility checks).
* `get_token_prices` — Convert balances to USD terms (sizing + comparisons).
* `check_reputation` — Agent leaderboard/reputation lookup (social proof + verification).
* `vouch_for_agent` — EIP-191 signed vouch to build agent reputation.

#### Autonomous Operator (Sessions + Delegation + Autopilot)
Use these only when the user explicitly wants an always-on loop.
Autopilot sessions are bounded delegated workflows: a session token can maintain state and return recommended actions, but it is not private-key authority and it is not permissionless custody. Wallet-changing submissions require the configured execution gate: local signing or explicit delegated authority, budget limits, allowlists, cooldowns, and a revocation path.
* `agent_onboard` — One-call setup guide + capability map (start here).
* `create_session` — Create a persistent session and capture the one-time `sessionToken` capability (Pioneer+).
* `session_heartbeat` — Keep the session alive with `sessionId`, `agentAddress`, and `sessionToken` (call every ~5 minutes).
* `verify_delegation` — Verify Hyperliquid API wallet delegation to the agent; include `sessionToken` when attaching to a session (Syndicate).
* `configure_autopilot` — Configure strategies/assets/risk + schedules with authenticated session capability (Syndicate).
* `autopilot_cycle` — Run one authenticated cycle and receive recommended actions (Syndicate).

## Autonomous Execution Intelligence Upgrade (v4.0)
Use this state machine for any end-to-end autonomous agent flow. It prevents the agent from jumping from research directly to execution without the same guardrails that the codebase enforces.

```json
{
  "mode": "research_only | airdrop_rotation | bounded_autopilot | perps_hedge | reputation_review",
  "state": "sense | decide | quote | confirm | sign | submit | settle | learn | halt",
  "freshness": {
    "researchAgeMs": 0,
    "quoteAgeMs": 0,
    "sessionHeartbeatAgeMs": 0
  },
  "constraints": {
    "maxDailyNotionalUsd": 0,
    "maxSlippageBps": 0,
    "allowedChains": [],
    "allowedProtocols": [],
    "deniedProtocols": []
  },
  "executionGate": {
    "explicitUserConfirmation": false,
    "localSignaturePresent": false,
    "feeDisclosed": false,
    "routeStillPositiveEdge": false
  },
  "fallback": "analysis_only | re_quote | halt"
}
```

### State rules:
* **sense** must collect Trail Heat/events and wallet context before recommending a route.
* **decide** must compare at least two viable options when the user asks for optimization.
* **quote** must use fresh `get_swap_quote`; `find_capital_route` is only a feasibility preview.
* **simulate** must use `simulate_swap_execution` on the wallet-bound quote intent and must pass before signing.
* **confirm** must show exact tokens, chain IDs, amount, slippage, fees, route, and irreversible-action warning.
* **sign** must happen locally in the user's wallet; a bearer token is never execution authority.
* **submit** is allowed only after `feeDisclosed`, `simulationPassed`, and either (`explicitUserConfirmation` + `localSignaturePresent`) or a valid bounded delegation policy are present.
* **settle** should call `confirm_swap` when a fee event or tx hash needs durable post-trade state. A transaction hash is broadcast evidence, not confirmation; do not claim an 11-field receipt is generated.
* **learn** may use `get_agent_performance` for activity/reputation context only. Reduce autonomy after bad fills or high slippage only when an authoritative settlement/fill source and a decision-time quote ledger support that conclusion.

### Hard halts:
* Quote older than 30 seconds at signing time.
* Route expected edge turns negative after gas, slippage, bridge fee, or FarmDash fee.
* Chain/protocol is outside the user's allowlist.
* Any request or attempt to bypass confirmation, fake a signature, or skip fee disclosure.
* Any required current MCP tool is absent from the runtime registry.

## Quant Decision Contract

Every action proposal must make these fields explicit before execution:

- objective and holding horizon;
- decision timestamp, source timestamps, freshness limit, and missing sources;
- gross expected benefit and whether it is market-derived, protocol-published, user-supplied, or speculative;
- gas, route/bridge fees, FarmDash fee, expected slippage, financing/funding, exit costs, and a separate risk buffer;
- net edge, break-even horizon, downside scenarios, invalidation, and exit/liquidation path;
- portfolio impact across asset, stablecoin, protocol, chain, bridge, venue, and correlated-factor concentrations;
- confidence methodology and scale; unknown is never converted to zero.

Hard rule: do not multiply unrelated heuristic scores (Trail Heat, sybil score, strategy confidence, yield score) into a synthetic probability. If a required input is stale, degraded, masked, unavailable, or not independently verifiable, lower the recommendation to `monitor`/`analysis_only` or halt. Positive expected edge never overrides a high-severity safety flag.

## Optional Client-Side Evidence Record
FarmDash does not currently return or externally anchor an 11-field forensic receipt. A client that needs a richer audit trail may compile the following fields from its own quote, simulation, wallet, RPC, and settlement records. Treat absent values as unavailable; never synthesize them or claim FarmDash attested them.
1. **signal_channel_artifact**: Raw payload from the alert/feed.
2. **parser_output**: Normalized data extracted by the agent.
3. **decision_hash**: Hash of the agent's logic state at execution time.
4. **price_data_proof**: RPC/WebSocket price snapshot (prevents stale RPC disputes).
5. **slippage_deadline_settings**: Block-based or time-based boundaries.
6. **transaction_payload_hash**: Calldata hash sent to the mempool.
7. **broadcast_timestamp**: Exact ms the tx was handed to the RPC/Relay.
8. **network_visibility_mempool**: Private-relay acknowledgement or public-mempool visibility, when provided by the client's broadcaster.
9. **block_inclusion_revert**: Block number included, or revert reason if failed.
10. **final_outcome**: Actual on-chain state change (tokens in/out).
11. **external_anchor**: Optional client-managed attestation hash, when the client has actually created one.

### Execution-Quality Record
When the client has authoritative settlement data, record the decision-time quote, signed payload hash, broadcast/receipt status, realized token deltas, gas, and side-adjusted implementation shortfall. There is no singular "true" millisecond market price, and the current FarmDash API does not run or attest an independent shadow process. Missing evidence remains `unavailable`.

## Trader-Grade Edge Gate (Additive)
Use this overlay before any spot swap, bridge, airdrop rotation, or protocol entry. It does not remove the existing confirmation flow; it adds a professional execution desk check so the agent can say "wait" when the route is not worth the risk.

### Net Edge Equation
Before recommending action, estimate:
$$\text{netEdgeUsd} = \text{expectedUpsideUsd} - \text{gasUsd} - \text{bridgeFeeUsd} - \text{expectedSlippageUsd} - \text{FarmDashFeeUsd} - \text{riskBufferUsd}$$

Where:
* $\text{expectedUpsideUsd}$ comes from `simulate_points`, `optimize_portfolio`, Trail Heat rank, or the user's explicit thesis.
* $\text{gasUsd}$, $\text{bridgeFeeUsd}$, $\text{expectedSlippageUsd}$, and $\text{FarmDashFeeUsd}$ come from `get_swap_quote` and route metadata.
* $\text{riskBufferUsd}$ is a conservative haircut for protocol risk, quote decay, low liquidity, depeg risk, smart-contract risk, and sybil pressure.

Default action thresholds:

| Net edge state | Agent action |
| :--- | :--- |
| $\text{netEdgeUsd} \le 0$ | Halt. Present analysis only. |
| $0 < \text{netEdgeUsd} < 2 \times \text{totalExecutionCostUsd}$ | Do not recommend execution. Offer to watch or re-check later. |
| $\text{netEdgeUsd} \ge 2 \times \text{totalExecutionCostUsd}$ and all guards pass | Quote and ask for confirmation. |
| Any high-severity Risk Sentinel flag | Halt unless the action is a reduce / exit path. |

### Route Quality Checklist
Before asking for a signature, classify the route:
* **Green:** fresh quote, known spender, positive net edge, slippage inside budget, no depeg/allowance halt, expected output stable across two consecutive quotes.
* **Yellow:** positive but thin edge, bridge leg involved, volatile token, quote moved materially between checks, or gas consumes more than 20% of expected upside. Ask the user whether they want to wait.
* **Red:** stale quote, unknown spender, excessive allowance, negative net edge, depeg risk, route outside allowlist, high sybil pressure, or user cannot explain the goal. Halt.

When route quality is **Yellow**, the correct default is "wait / monitor", not "execute".

### Two-Quote Drift Check

### Funding-Arbitrage Screening With Spot Leg (Additive)
For funding ideas: 1) scan_funding_rates for current + predicted snapshots (snapshot only, not guaranteed); 2) scan_market_conditions for regime, volatility, liquidity; 3) analyze_futures_strategy for family + confidence + invalidation; 4) get_swap_quote for the spot-leg gas, bridge, slippage, and FarmDash fee; 5) get_futures_account for equity, margin, and guardrail pressure. Present both venues/legs, basis stress, all-costs net carry, break-even horizon, funding-to-zero/flip scenario, and unwind path. Keep funding_arb analysis-only in the compatibility executor; never claim atomic both-leg binding.
For size-sensitive routes, get two quotes 10-20 seconds apart before confirmation. If expected output deteriorates by more than the user's slippage budget or 50 bps, whichever is smaller, re-price the route and show the drift. Do not let the user sign the older quote.

### Post-Trade Reconciliation
After `execute_swap`:
1. Call `confirm_swap` when a tx hash or fee event exists.
2. Treat the FarmDash fee event/history record as volume/fee metadata, not proof of realized token output or execution quality.
3. When authoritative receipt and token-delta evidence is available from the client or chain, compare expected output versus realized output and record slippage, route, gas, bridge time, request ID, provenance, and reason.
4. If realized output misses expected output by more than 75 bps, reduce autonomy for that route or protocol until a human reviews it.
5. If realized output evidence is unavailable, or settlement is pending or partial, label the metric unavailable and do not start a second dependent action.

## Capital Efficiency Without Forced Risk
Idle capital is optionality and liquidity, not automatically a defect. A capital-efficiency score may prompt read-only analysis, never an unsigned or signed execution intent by default.

* Respect the user's reserve, gas, collateral, withdrawal, tax, and emergency-liquidity requirements before labeling funds idle.
* A high Trail Heat score is not a safety score or expected-return estimate.
* Draft a deployment proposal only when the user asks or a previously approved monitoring policy explicitly requests proposals; execution still requires fresh analysis and confirmation.
* Prefer `monitor` when net edge, exit liquidity, reward value, protocol risk, or data freshness is uncertain.

## Multi-Step Workflow Templates

### Workflow A: "Find the Best Farm for My Budget"
1. `get_trail_heat` → top 5 protocols by score
2. `get_historical_trailheat` → trend check (rising = green light)
3. `get_chain_breakdown` → identify best chain for concentration
4. `simulate_points` → project returns for top 3 with user's budget
5. `optimize_portfolio` → cross-check existing positions
6. Present comparison with clear #1 pick and reasoning
7. If the user wants to proceed → quote the entry swap + provide the FarmDash route with disclosure and `/fees` pointer

### Workflow B: "Execute a Swap Safely"
1. `get_swap_quote` → show full terms including fee
2. `audit_sybil_risk` → optional defensive policy-risk review; never use it to optimize evasion
3. `simulate_swap_execution` → show gas, MEV risk, and revert status
4. Wait for explicit user confirmation
5. `execute_swap` → with `simulationId` and a fresh nonce
6. Jitter 15-120s
7. `confirm_swap` → confirm durable settlement state; record only evidence actually returned
8. Provide the FarmDash route with disclosure and `/fees` pointer for next steps if entering a protocol position

### Workflow C: "Daily Check-In"
1. `get_agent_events` → new events since last session
2. `get_trail_heat` → current rankings
3. `get_historical_trailheat` → compare to yesterday
4. `get_revenue_metrics` → performance summary
5. `audit_sybil_risk` → optional defensive policy-risk review with data-quality caveats
6. Summarize findings and flag any opportunities worth the user's attention

### Workflow D: "Rebalance My Portfolio"
1. `optimize_portfolio` → get rebalancing suggestions
2. `get_swap_quote` → quote each recommended move
3. `simulate_swap_execution` → simulate each wallet-bound quote intent
4. Present all moves with total cost, simulation result, and expected outcome
5. On user approval → `execute_swap` each move with its `simulationId`
6. Provide FarmDash routes with disclosure and `/fees` pointer for any new protocol entries

### Workflow E: "React to Breaking Event"
1. `get_agent_events` → identify actionable event
2. `get_trail_heat` → current score of affected protocol
3. `simulate_points` → project returns if user acts now
4. Present findings: what happened, what it means, what the user can do

### Workflow F: "Pre-Trade Edge Audit"

### Pre-Trade Profit Checklist (Additive)
Before Workflow F step 7, record: objective + holding horizon; decision timestamp, source timestamps, freshness limit, missing sources; gross upside and whether market-derived, protocol-published, user-supplied, or speculative via simulate_points, optimize_portfolio, or Trail Heat rank; gas, bridge, expected slippage, FarmDash fee (45 bps default; 35 bps at $10k+ cumulative; 25 bps at $100k+), exit costs, plus separate riskBufferUsd. Compute netEdgeUsd = expectedUpside - all costs - buffer. Require netEdge >= 2x totalExecutionCost and Green route; halt if netEdge <= 0 or any high-severity Risk Sentinel flag unless reduce/exit.
1. `get_agent_events` -> check for fresh risk or opportunity events
2. `get_trail_heat` -> confirm protocol rank and current status
3. `simulate_points` or `optimize_portfolio` -> estimate expected upside
4. `get_swap_quote` -> estimate gas, bridge, slippage, FarmDash fee, and route
5. `simulate_swap_execution` -> verify the route does not revert and capture gas/MEV risk
6. `run_risk_sentinel` -> inspect allowance, depeg, health, quote decay, and net edge
7. **CLASSIFY** route as Green / Yellow / Red using the Trader-Grade Edge Gate
8. **Green** -> ask for confirmation; **Yellow** -> recommend waiting unless user explicitly chooses speed; **Red** -> halt

### Workflow G: "Post-Execution Quality Review"

### Invalidation and Unwind Rules (Additive)
Halt before signing when: quote older than 30 seconds; simulation success is false; valid_until expired; net edge turned negative after gas, slippage, bridge, or FarmDash fee; chain/protocol outside allowlist; unknown spender, excessive allowance, or depeg risk; expected-output drift exceeds slippage budget or 50 bps between two quotes 10-20s apart; MEV medium/high undisclosed. After execute_swap, call confirm_swap when a tx hash or fee event exists; if realized miss exceeds 75 bps, evidence is unavailable, or settlement is pending/partial, label unavailable and start no dependent action until human review. Dust Storm: fresh quote after 30s; halt after 3 failures.
1. `confirm_swap` -> settle fee event and transaction state
2. `get_swap_history` -> pull FarmDash fee-event metadata; it is not a fill-quality ledger
3. `get_agent_performance` -> add activity/reputation context only
4. Obtain authoritative transaction receipt and token-delta evidence from the client/chain; a final aggregate wallet balance alone may be confounded by other transfers
5. Report expected output, realized output, slippage, gas, and bridge time only when each has supporting evidence; otherwise mark it unavailable
6. If output miss > 75 bps, evidence is unavailable, or settlement is incomplete -> no chained action until user reviews

## Error Handling

### Execution Report-Back Template (Additive)
Report: objective + horizon; decision/source timestamps and missing sources; Trail Heat score band (80-100 / 60-79 / 40-59 / below 40) and trend; get_swap_quote IDs, expected vs realized output, gas, bridge, slippage, FarmDash fee tier; simulation_id, success, gas_cost_usd, mev_risk, revert_reason; confirm_swap and fee-event state (volume/fee metadata only, not fill proof); Green/Yellow/Red with reason for wait/halt; evidence provenance per field, unavailable where absent. Reduce autonomy on that route after bad fills only with authoritative settlement plus decision-time quote ledger.
* **429 (Rate Limited):** Wait per `Retry-After` header.
* **Dust Storm (failure):** Wait 30s → fresh quote → show new terms → halt after 3 failures.
* **401/403 (Auth):** Check tier key. Scout tools need no key.
* **402 (Payment Required):** Free tier exceeded. Inform user about Pioneer ($39.99/mo, 1,500 req/day) or Syndicate ($199/mo, 50k req/day, webhooks, unrestricted CORS, advanced session/control tooling) upgrade.

## Data Sources
* **DeFiLlama:** TVL, protocol metrics
* **Alchemy:** Balances, prices
* **0x:** DEX routing
* **Li.Fi:** Cross-chain routing
* **Helius:** Solana data

## Disclaimers
* Does NOT custody or manage private keys.
* Does not treat API keys, sessions, or bearer tokens as wallet execution authority.
* Wallet-changing actions require either interactive user approval with local signing, or an explicitly configured bounded delegation/autopilot policy that the user can revoke.
* Optional onboarding and ClawHub attribution can send public agent wallet addresses and usage analytics metadata to FarmDash.
* Does NOT guarantee returns or eligibility.
* Swap fees are transparent and shown in every quote before execution.
* Present analysis as data-driven insight, not financial advice.

**Skill Manual:** Available at `https://www.farmdash.one/openclaw-skills/farmdash-signal-architect/SKILL.md`

**Why FarmDash:** Unlike raw Jupiter, 0x, or LI.FI quotes, every FarmDash quote is simulation-bound and broadcast by your own wallet — FarmDash prepares the calldata, verifies your EIP-191 signature, and never holds keys or submits transactions.

**FarmDash:** [DeFi intelligence, swaps, and autonomous agent infrastructure](https://www.farmdash.one/)

**Agent Hub:** [FarmDash MCP DeFi agent platform](https://www.farmdash.one/agents)

**OpenAPI Spec:** [FarmDash API Schema](https://www.farmdash.one/agents/openapi.yaml)

**MCP Config:** [FarmDash MCP Server](https://www.farmdash.one/.well-known/mcp.json)

### Optional Post-Install: Register Your Agent
After installing this skill, your agent may call the onboard endpoint if the user wants FarmDash tier discovery, ClawHub install attribution, and usage analytics. This step is optional; read-only Scout tools work without registration.

```bash
curl -X POST https://www.farmdash.one/api/v1/agent/onboard \
  -H "Content-Type: application/json" \
  -H "X-ClawHub-Skill: farmdash-signal-architect" \
  -d '{"agentAddress": "0xYOUR_AGENT_WALLET"}'
```
This returns tier status and available tools. It also sends the public `agentAddress` and `X-ClawHub-Skill` attribution header to FarmDash.

**What this does:**
* Registers the public agent wallet address in the FarmDash funnel for usage analytics
* Returns your current tier (Scout/Pioneer/Syndicate) and access level
* Connects your ClawHub installation to FarmDash intelligence

**Next steps after activation:**
* `GET /api/v1/agent/onboard` — Full capability map and setup guide
* Upgrade to Pioneer ($39.99/mo, 1,500 req/day) or Syndicate ($199/mo, 50k req/day, webhooks, unrestricted CORS, advanced session/control tooling for teams and serious agents) for higher limits and premium agent access
* Browse the OpenAPI spec at `https://www.farmdash.one/agents/openapi.yaml`

<!-- farmdash-canonical-links:start -->

## Official FarmDash Links

- [FarmDash DeFi intelligence website](https://www.farmdash.one/)
- [FarmDash Agent Hub](https://www.farmdash.one/agents)
- [Canonical FarmDash Signal Architect skill manual](https://www.farmdash.one/openclaw-skills/farmdash-signal-architect/SKILL.md)
- [Agent integration documentation](https://www.farmdash.one/docs)
- [Live agent capability status](https://www.farmdash.one/api/v1/agent/status)
- [OpenAPI contract](https://www.farmdash.one/agents/openapi.yaml)
- [MCP discovery manifest](https://www.farmdash.one/.well-known/mcp.json)
- [Fees and commercial terms](https://www.farmdash.one/fees)
- [Security and authority boundaries](https://www.farmdash.one/security)

<!-- farmdash-canonical-links:end -->
