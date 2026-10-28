---
name: dex-analysis
description: >
  Methodology playbook for analyzing DEX/AMM trade, liquidity, and pricing data on
  Allium — Uniswap, PancakeSwap, PumpSwap/Pump.fun, Orca, Pendle, aggregators (0x,
  1inch), and perp DEXs like Hyperliquid. Use whenever a question touches swap volume,
  trade counts, liquidity positions, impermanent loss, aggregator fee/routing analysis,
  or DEX-derived token prices — even if the user just names a protocol or asks why a
  number "looks off" compared to a known reference. Covers the per-hop double-counting,
  protocol-vs-project grouping, and fee-leg reconstruction pitfalls that come up
  repeatedly before you write the SQL.
---

# DEX Analysis

The most common DEX-analysis mistake isn't a wrong table — it's treating a per-hop or
per-side data model as if it were per-swap or per-trade. Check the grain of the table
before aggregating.

## Trade rows are often per-hop, not per-swap

Multi-hop routes (A→B→C) can produce 2-3 trade rows for what the user experienced as one
swap. This inflates both volume and row counts — one real comparison found ~1.3x
inflation vs. an external source on a specific chain purely from hop fan-out.

- Compare `COUNT(*)` vs. `COUNT(DISTINCT transaction_hash)` on a trades table before
  trusting a volume/count total — a large gap between them is the signature of
  multi-hop fan-out.
- When you need to compare volume against an external aggregator (DefiLlama, etc.),
  either divide by the observed hop ratio or aggregate at `transaction_hash` grain first.

## Group by protocol for AMM-math questions, by project for branding

`protocol` and `project` answer different questions and get confused constantly:
- `project` identifies the branded product (e.g. "PancakeSwap V2").
- `protocol` identifies the underlying AMM implementation (e.g. PancakeSwap V2 is a
  straight fork of Uniswap V2, so both show `protocol = 'uniswap_v2'`).

Use `protocol` whenever the question is really about AMM mechanics — like impermanent
loss, which depends on the pricing curve, not the brand. Grouping IL analysis by
`project` will silently split identical-math pools (Uniswap V2 and its forks) into
separate buckets that should be one.

Don't assume every "swap-shaped" venue has the same mechanics:
- **PumpSwap ≠ Pump.fun's bonding curve.** They're sequential phases of the same token's
  life, not the same product — the bonding-curve phase has no impermanent-loss concept
  at all (there's no external LP), only the post-graduation PumpSwap pool does.
- **V3/concentrated-liquidity IL is not V2 IL scaled** — a narrower `tick_lower`/
  `tick_upper` range amplifies both IL and fee income by a range-dependent concentration
  factor. Applying a flat V2 IL formula to a V3 position will be wrong, not just
  approximate.
- **Pendle PT/YT/SY/LP positions live in a `yields`-style schema, not `dex`.** Don't
  look for Pendle in a DEX trades/liquidity table.

## Aggregator trades often need a join for basic fields, and hide their fee as a transfer

Aggregator-trade tables (0x, 1inch, etc.) can be missing fields you'd expect on a normal
trades table — e.g. no decimals columns, no swap-count column. Join to the token
metadata table for decimals, and derive a swap count via
`COUNT(*) OVER (PARTITION BY transaction_hash)` rather than assuming a column exists.
Double-check you're joining to the actual namespaced transfers table (not a
similarly-named un-namespaced one) and using the raw integer amount column, not a
pre-decimal-adjusted one, if you need exact precision.

An aggregator's implicit fee/surplus isn't a labeled column — reconstruct it by finding
the ERC20 transfer of the trade's buy/sell token that flows *out of* the aggregator's
entry contract to an address that is neither the taker nor an internal pool/router
contract. That leftover leg is the fee; decimal-adjust it using the matching side's
token decimals.

## Sanity-check ratios before trusting them

- **Capital efficiency (volume/TVL) blows up toward infinity when recorded TVL is near
  zero** — usually a sign of incomplete TVL indexing for that specific protocol, not
  genuinely infinite efficiency. Guard the ratio with a minimum-TVL threshold and return
  null/flag below it rather than reporting the raw division.
- **A large gap between average and median trade size flags an atypical venue** — a few
  large institutional-sized trades skewing the mean is a common signature of a
  liquid-staking or treasury-management protocol showing up in DEX data, not a "normal"
  retail swap venue. Don't average without also checking the median when trade-size
  distribution matters to the question.

## Perp-DEX (Hyperliquid-style) specifics

- A raw fills table is typically **one row per side per fill** (one row for the buyer's
  side, one for the seller's), with a taker/maker flag per row — don't assume a
  side-level table gives you both counterparties in one row. Use a trade-level table
  (one row per trade, both counterparty addresses) when you need both sides together.
- Because fills are per-side, **don't halve a `SUM(size)` when you've already grouped by
  user** — the "divide by 2" correction only applies to an ungrouped, market-wide sum
  where each trade would otherwise be counted from both the buyer's and seller's row;
  once you've filtered/grouped to one user's fills, that user's own volume is already
  singly counted.
- "Builder"-attributed flow (third-party order-flow submitters — bots, aggregators,
  copy-trading frontends) skews heavily toward taker orders, since it's typically
  automated and aggressive rather than passive limit orders. Don't assume builder flow
  behaves like organic retail flow when characterizing it.
- Long lookback windows (e.g. 12 months) aggregated per-user over a large perp-trades
  table can hit a warehouse statement timeout. Scope a first pass to a shorter window
  (3-6 months) before committing to the full period, especially for a threshold-style
  question ("users trading $1000+/month").

## Price data quirks

Allium's DEX-derived token prices are typically a short-interval (e.g. 1-minute) VWAP
with outlier filtering to strip pure arbitrage spikes. **Identical repeated prices across
consecutive sub-minute polls usually mean no new trade occurred in that window** (the API
is returning the last cached price), not a data bug — this is most visible on
thin-liquidity wrapped assets that trade far less frequently onchain than their
underlying does on centralized exchanges, which is also why a persistent CEX/DEX price
gap can exist without being an error.

## Cross-DEX pair rollup

When you need one number for a pair regardless of trade direction (A→B and B→A are the
same pair), normalize the pair label — e.g.
`LEAST(token_sold_symbol, token_bought_symbol) || '/' || GREATEST(...)` — so both
directions roll up together instead of appearing as two separate pairs. Watch for null
pair labels coming from unresolved token symbols before trusting a "top pairs" ranking.

---

## Data source

Every chain database has its own `dex` schema (`<chain>.dex.trades`, `<chain>.dex.pools`,
`<chain>.dex.liquidity_positions`, etc.). Unlike stablecoins and RWA, DEX doesn't have a
dedicated crosschain database yet — for a question spanning multiple chains, use the
multi-chain combo views under `crosschain.dex` (`crosschain.dex.trades`, the
EVM-optimized `crosschain.dex.trades_evm`, and the aggregator equivalents
`crosschain.dex.aggregator_trades`/`aggregator_trades_evm`) rather than unioning per-chain
tables by hand.

Table and column names move as this schema evolves, so don't hard-code any of the names
above from memory. Run `data-matching` first to confirm the current tables for your
specific question, and use `search_schemas`/`search_docs` directly
if you need to double check a column before writing SQL.
