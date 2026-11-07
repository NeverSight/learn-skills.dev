---
name: stablecoin-analysis
description: >
  Methodology playbook for analyzing stablecoin volume, supply, holders, and geographic
  usage on Allium — USDC, USDT, DAI, USDS, RLUSD, USDG, JPYC, and other fiat/crypto/
  algorithmic-backed stablecoins. Use whenever a question touches stablecoin transfer
  volume, circulating supply, wallet/holder counts, geo splits, or cross-chain
  deployments — even if the user just names a specific stablecoin, asks for "adoption"
  or "usage" numbers, or asks to compare volume to a chart/number they already have.
  Covers the raw-vs-adjusted volume distinction, chain-specific double-counting
  mechanics, and address/case-sensitivity gotchas that come up repeatedly before you
  write the SQL.
---

# Stablecoin Analysis

The single most consequential decision in any stablecoin volume question is **raw vs.
adjusted volume** — get that wrong and every downstream number is off by 5-20x. Read
this before writing SQL.

## Raw volume overstates organic activity — use adjusted

Per-transfer tables include CEX-internal transfers, DeFi-protocol internal movements,
MEV, and wash flows. `SUM(usd_amount)` on a raw transfers table answers "how much value
moved," not "how much real economic activity happened" — and the two can differ by an
order of magnitude. For real adoption/usage analysis, use the entity-adjusted volume
columns (look for `is_adjusted_volume`, `is_inorganic_sender`/`is_inorganic_receiver`,
`is_mev_transfer` style flags, or a pre-aggregated entity-adjusted metrics table) rather
than raw `SUM`.

If a user shares a chart or number they already trust and your raw-volume query comes
back 5-20x higher, that's usually not a bug in your query — it's the raw-vs-adjusted gap.
Check for an adjusted-volume source before assuming your SQL is wrong.

## Always check for fake/bad-data tokens before trusting a total

Stablecoin volume tables can contain non-stablecoin tokens misclassified into the
catalog (a real case: a token called "xy" on Arbitrum, NULL currency, contributed $5.4T
of fake volume to a $16.65T headline number — a single bad token was ~1/3 of the
reported total). Before citing a volume total:
- Break it down by token and look for anything with an implausible share of volume
  relative to its market presence, a NULL/missing `currency`, or a suspicious
  single-day volume spike that dwarfs its typical daily pattern.
- If asked to be thorough, actually audit every token contributing >0.1% of volume, not
  just the one you happened to notice — real audits in practice have found multiple bad
  tokens (5 in one pass) once someone looked past the first one.

## Chain-specific double-counting mechanics

- **XRPL (RLUSD and other XRPL-issued stablecoins)**: the trust-line/rippling mechanism
  emits two transfer rows per real transfer (sender→issuer, then issuer→recipient).
  Naive issuer-address exclusion doesn't fix this — treasury/operational wallets sit
  downstream of the issuer and still inflate volume. Dedupe by `transaction_hash`
  (`MAX(usd_amount)` per hash), and identify treasury wallets by behavioral pattern (very
  high volume, exactly one counterparty) rather than a static address exclude-list.
- **Aptos**: some assets (USDT) have two live addresses for the same underlying token —
  a legacy Coin-module address and a newer Fungible Asset address. Supply/transfer tables
  key on one of them (often the newer FA address); querying the legacy address silently
  returns zero rows rather than erroring.
- **Bridged tickers on messaging-protocol tables**: when filtering bridge volume by
  token symbol, use an exact match, not `LIKE`/fuzzy matching — wrapped or derivative
  tickers (e.g. `PT-USDG-28MAY2026`, `USDG0`) share substrings with the real symbol and
  will silently inflate the count under a fuzzy filter.

## Address conventions are chain-specific — don't apply one rule everywhere

Lowercase EVM addresses before joining/filtering. Do **not** lowercase Solana, Tron, or
Aptos addresses — they're case-sensitive and lowercasing silently breaks the join
(returns zero rows, not an error).

## Native vs. bridged deployments are separate supplies on the same chain

The same stablecoin can have both a native issuance and a bridged representation on one
chain (e.g. native USDC vs. bridged USDC.e on Polygon). These are different addresses
with different supply — don't assume "USDC on Polygon" resolves to one canonical address,
and be explicit about which deployment a query is scoped to.

## Holders and geography need the right table, and neither table alone is complete

- "Wallets using stablecoins" requires **transactors ∪ holders**, not either alone — a
  wallet that sends its full balance out is a transactor but not an end-of-period
  holder, and a dormant holder that never transacts is the reverse. Don't answer a
  "usage" question with only one side.
- Balance/holder tables are typically EVM-only — there's often no equivalent
  `balances_daily`-style table for Solana or Tron; holder counts on those chains need a
  transfer-based approximation instead, and that limitation should be stated, not
  silently absorbed.
- For geographic splits, use an actual address-geography table (inferred from exchange
  deposit/withdrawal patterns), not a UTC-hour-of-day heuristic — "activity between
  00:00-08:00 UTC = Asia" is a weak proxy that a real geo table will contradict. Note
  that geo tables are often EVM/Tron/Solana-only with **all EVM chains collapsed into one
  bucket** — map your specific chain (ethereum, polygon, base, ...) to that bucket before
  joining, or the join will silently return nothing.

## Routed/DEX volume is not float growth

When a stablecoin issuer's token gets routed through DEX/solver activity, that trading
volume is not the same thing as growth in circulating float. Distinguish:
- **pure pass-through** — mint and burn within the same transaction/short window, net
  float impact ≈ $0;
- **inventory model** — a market-maker holds working inventory, float = inventory held;
- **genuine adoption** — sustained end-user holding.

Raw trading/routed volume vastly overstates how much of it represents #3. If asked about
adoption or float growth, don't answer with a volume number without checking which of
these three it actually reflects.

---

## Data source

Every chain database has its own `stablecoins` schema (`<chain>.stablecoins.*` — e.g.
`ethereum.stablecoins.transfers`, `solana.stablecoins.supply_change`). For anything that
spans more than one chain, **prefer the dedicated `stablecoins` database over
`crosschain.stablecoins`** — the crosschain-rollup naming has moved to its own top-level
database (`stablecoins.core.transfers`, `stablecoins.core.balances_daily`,
`stablecoins.registry.catalog` for issuer/peg-mechanism/classification metadata, and
`stablecoins.intelligence.enriched_transfers` for the adjusted-volume/organic-activity
classification described above). Don't reach for an old `crosschain.stablecoin.*` name
from memory or a prior session — that naming has been superseded.

Per-chain, an older `<chain>.assets.stablecoin_transfers` table is being phased out in
favor of `<chain>.stablecoins.transfers` — avoid the `assets`-schema version where
possible.

Table and column names move as this schema evolves, so don't hard-code any of the names
above from memory. Run `data-matching` first to confirm the current tables for your
specific question, and use `search_schemas`/`search_docs` directly
if you need to double check a column before writing SQL.
