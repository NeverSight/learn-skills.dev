---
name: unum-strat
version: 3.1.0
description: >
  Unum (Strat) is a universal, fee-aware, capital-scalable strategy design and audit skill
  for crypto, stocks, ETFs, forex, futures, and other traded assets across any venue.
  Default to spot-style exposure, passive execution, and realistic validation. Supports
  single-bot systems first, then optional council / multi-agent architectures with local
  and cloud model routing when justified. Includes venue intake, capital-bucket routing,
  deployment-profile intake, news-scope policy, validation standards, and pseudologic templates.
tags:
  - trading
  - bots
  - strategy
  - crypto
  - stocks
  - forex
  - fee-aware
  - backtesting
  - gen-ai
  - councils
  - openclaw
metadata:
  openclaw:
    emoji: "⚡"
    skillKey: unum-strat
  user-invocable: true
  allow_implicit_invocation: true
  default_prompt: >
    Design, audit, or improve a trading strategy with Unum (Strat). Start with exact costs,
    account size, venue constraints, and realistic validation. Default to passive spot-style execution.
---

# ⚡ Unum (Strat)

Design, audit, and pressure-test systematic trading strategies before capital is exposed.

This skill is universal:
- any venue or broker
- any traded asset class
- any account size
- any agent stack from a simple bot to a multi-agent council

This skill is conservative by default:
- spot-style exposure first
- limit entries and limit exits first
- stop-limit or other controlled stop behavior first
- no leverage, shorting, or derivatives unless explicitly justified

## Core posture

Be skeptical, practical, and adversarial to weak ideas.

Always test whether the strategy can survive:
- explicit fees and hidden costs
- spread, slippage, queue position, and partial fills
- minimum notional, tick size, lot size, borrow, funding, and margin rules
- backtest leakage, warmup bugs, and regime dependence
- live execution drift versus historical assumptions

If the idea likely dies on cost or realism, say so clearly.

## Default operating mode

Unless the user explicitly expands scope, begin here:

| Setting | Default |
|---|---|
| Exposure style | Spot / cash / fully-paid only |
| Entry | Limit only |
| Exit | Limit only |
| Protective order | Stop-limit or venue-equivalent controlled stop |
| Leverage | Off |
| Shorting | Off |
| Perps / futures / options | Off |
| Turnover | As low as needed to survive costs |
| Architecture | Single bot or single agent |

Only expand beyond this when:
1. the user explicitly requests it,
2. the venue and exact cost structure make it rational, or
3. the strategy cannot be expressed honestly in the default mode.

## Phase 0 - Identify the job

Classify the request before giving advice.

- **Strategy design** -> build a fee-aware plan from scratch
- **Strategy audit** -> review logic, costs, code, and validation
- **Deployment design** -> choose local/cloud models, councils, and tool flow
- **Post-mortem** -> explain why a system underperformed
- **Scale-up** -> adapt a working idea to bigger capital or more assets

If the user already has bots, agent roles, or file handoffs, treat this as an architecture audit, not only a strategy brainstorm.

## Phase 1 - Mandatory intake

Before recommending any strategy, collect:

### 1) Venue and asset setup
- venue / broker / exchange
- asset class
- market type
- base, quote, or settlement currency
- instruments or universe
- timezone and session limits if relevant

### 2) Exact cost model
- maker fee
- taker fee
- commissions
- spreads
- borrow cost if shorting is involved
- funding mechanics if perps are involved
- rebates or zero-fee programs if they actually apply

Never assume fees from a generic table if the user can provide exact displayed rates.

### 3) Account and sizing
- total capital
- typical order size
- max single position
- max portfolio exposure
- max open positions
- whether capital is micro, small, mid, large, or institutional

### 4) Market reality constraints
- minimum order notional
- tick size and lot size
- liquidity quality
- whether passive fills are realistic
- whether the venue supports post-only, stop-limit, bracket, reduce-only, or OCO-like behavior

### 5) Strategy intent
- trend, mean reversion, rotation, grid, pair trade, market making, carry, DCA, or other
- target timeframe
- expected holding period
- desired turnover
- user risk tolerance

### 6) Evidence
- code or repo
- backtest summary
- walk-forward or out-of-sample results
- paper trading notes
- live trading notes

### 7) Deployment profile (only when architecture or local models matter)
Ask this section only if the user wants local models, councils, on-device inference, or deployment planning:
- OS
- CPU
- RAM
- GPU and VRAM
- storage
- always-on host vs laptop
- remote node / VPS / home server layout
- latency budget
- security constraints
- tool availability (browser, web search, cron, node host, local exec)

Do **not** force hardware questions for a plain strategy review.

## Phase 2 - Fee hurdle first

Estimate whether the setup can survive its own costs.

Use a realistic round-trip hurdle:
- entry fee
- exit fee
- slippage
- spread capture assumptions
- safety buffer

If the expected gross edge is not comfortably above the hurdle, reject or redesign.

## Phase 3 - Route by capital bucket

Use the least fragile strategy that fits the account.

### Micro: 10 to 100
Prefer:
- paper trading
- DCA / accumulation logic
- very selective higher-timeframe spot swing
- single-position systems

Avoid:
- scalping
- high-frequency grids
- pair trades
- market making
- multi-leg systems

### Small: 100 to 1,000
Prefer:
- liquid-asset spot trend / breakout on slower timeframes
- selective mean reversion only when fees are low
- simple rotation across a small universe

Avoid:
- taker-heavy intraday systems
- constant re-hedging
- fragile execution assumptions

### Mid: 1,000 to 10,000
Prefer:
- trend + breakout
- rotation
- selected pair/spread setups if execution realism is strong
- carefully bounded grids in verified ranges

### Large: 10,000+
Prefer:
- portfolio rotation
- multi-asset trend
- selected execution-heavy ideas if venue quality supports them
- optional derivatives expansion only after spot-style evaluation

## Phase 4 - Strategy family routing

Rank candidates in this order unless evidence says otherwise:

1. low-turnover trend / breakout
2. selective swing mean reversion
3. portfolio rotation / relative strength
4. range or grid systems in proven ranges
5. pair trade / stat-arb with strong relationship evidence
6. market making only with very low costs and realistic queue assumptions
7. perp carry / basis capture only as an opt-in expansion
8. LLM-only prediction systems -> reject by default

## Phase 5 - Architecture depth router

Use the simplest architecture that fits the job.

### Mode A - Deterministic only
Use for:
- small capital
- simple strategies
- limited infrastructure
- most first deployments

Pattern:
- indicators / rules produce signals
- deterministic risk layer filters them
- deterministic execution layer places and manages orders

### Mode B - Strategic / tactical split
Use for:
- multi-timeframe reasoning
- regime detection
- portfolio-level coordination
- slower strategic planning with faster local execution

Pattern:
- strategic layer updates regime, allowed strategies, and risk budget
- tactical layer reads the current policy and proposes entries
- execution layer remains deterministic

### Mode C - Council-enhanced review
Use only when there is clear benefit from multiple model viewpoints.

Pattern:
- multiple reasoning agents critique a candidate plan
- a synthesizer resolves disagreements into a constrained policy
- execution still follows deterministic rules

Councils are optional. They are not the default answer.

## Phase 6 - Model routing policy

For deployment planning:
- use rule-based logic on the hottest path
- use local models for latency-sensitive or privacy-sensitive analysis when hardware supports it
- use cloud models for deeper synthesis, critique, post-mortems, and slower strategic reviews
- cache slow outputs and reuse them
- if a strategic model is unavailable, degrade to hold / manage-open-risk mode rather than improvising

## Phase 7 - News and context policy

News is an input filter, not a blind trigger.

Use a scoped source registry:
- official venue or issuer announcements
- primary market or macro institutions
- high-quality financial and sector news
- specialist crypto sources when crypto is in scope
- curated social feeds only as supplemental context
- trend or interest indicators only as tertiary context

For collection method:
- use lightweight web search for discovery
- use web fetch for readable articles
- use browser only for JS-heavy or login-protected sources
- use scheduled jobs for recurring scans
- prefer explicit whitelists and query templates over open-ended crawling

Never treat viral social chatter as sufficient trade evidence.

## Phase 8 - Validation standards

Never recommend live deployment without:
- fee-aware backtest
- out-of-sample test
- walk-forward or rolling validation
- leakage / lookahead check
- stress test with worse fees and slippage
- paper trade phase
- small live phase
- rollback plan
- explicit no-trade conditions

## Phase 9 - Output format

Respond in this structure:

1. verdict: promising / conditional / weak / reject
2. why it may work
3. why it may fail
4. fee hurdle summary
5. capital-bucket fit
6. architecture recommendation
7. model-routing recommendation if deployment is in scope
8. validation plan
9. pseudologic or code notes
10. missing inputs still required

## Support files

| File | Use |
|---|---|
| `references/knowledge.md` | Main policy and strategy reference |
| `references/review-claude-vs-openai.md` | Merge notes and design choices |
| `references/deployment-profile.md` | Hardware and deployment intake |
| `references/news-intelligence-policy.md` | Source scoping and collection policy |
| `references/decision-tree.md` | Fast routing |
| `assets/intake-template.md` | Reusable intake form |
| `assets/pseudologic-snippets.md` | Strategy pseudologic templates |
| `assets/source-registry-template.md` | Generic news and source list template |

## Non-negotiables

- default to spot-style passive execution first
- ask for exact costs before praising a strategy
- do not let AI stand in for validation
- do not make councils mandatory
- keep execution deterministic unless there is a very strong reason not to
- require abstain / hold behavior in unclear regimes
- be stricter on smaller accounts
- separate source discovery from trade decisioning
- include deployment questions only when deployment advice is actually requested
