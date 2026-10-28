---
name: rwa-analysis
description: >
  Methodology playbook for analyzing tokenized real-world assets (RWA) on Allium —
  tokenized treasuries, money market funds, tokenized equities/pre-IPO stocks,
  commodities, and private credit. Use whenever a question touches RWA supply, AUM,
  market cap, holders, mint/burn activity, or classification — even if the user just
  says "tokenized treasuries," "BUIDL," "tokenized stocks," "money market fund
  AUM growth," or names a specific RWA product/issuer. Covers the aggregation
  mistakes, classification pitfalls, and data-quality exclusions that come up
  repeatedly in real RWA questions before you write the SQL.
---

# RWA Analysis

RWA questions look like simple aggregations ("what's the AUM of X," "how many holders
does Y have") but the naive query is usually wrong in a specific, recurring way. Read
this before writing SQL for an RWA question — it's cheaper than debugging a 30x-inflated
number after the fact.

## Aggregation: snapshot, don't sum

AUM, market cap, and supply are **stock** quantities (a balance at a point in time), not
**flow** quantities. Summing a daily-snapshot table across a date range compounds the
same balance over and over.

- Take the latest row per grouping key (`QUALIFY ROW_NUMBER() OVER (PARTITION BY ... ORDER
  BY date DESC) = 1`, or `MAX(date)` per group), never `SUM(market_cap_usd)` /
  `SUM(supply)` across days.
- This mistake is easy to miss because the wrong number is still plausible-looking —
  one real case reported "$220B" AUM that was actually $7.2B, a ~30x inflation from
  summing ~30 days of the same snapshot.

## Multi-chain products: sum across chains, but say so

A tokenized fund (BUIDL, BENJI, etc.) deploys separately on multiple chains. Each
per-chain deployment is a real, distinct supply — summing across chains at the *same
snapshot date* gives the true total AUM, but a query scoped to one chain will
undercount and look like a much smaller fund than it is (one real case: $415M on
Ethereum alone vs. the real $1.67B across 8 chains).

- When reporting a cross-chain total, also surface `COUNT(DISTINCT chain)` or list the
  chains — the reader needs to know the number is an aggregate, not a single deployment.

## Classification: risk factor, not legal wrapper

Classify by the underlying risk factor (`asset_class`/`asset_type`), not by legal
structure or naive keyword matching on the product name. A tokenized Treasury ETF is
`rates`, not `equities`, even though "ETF" sounds equity-like. If you find a deprecated
`rwa_class` column still in a table, don't use it — check whether it's been superseded
by a newer classification field before trusting it.

For "tokenized treasuries" specifically, the intended filter is usually
`asset_class = 'rates' AND asset_type IN ('government_debt_us', 'money_market_funds_us',
'repurchase_agreements')` — confirm the exact enum values against the live schema, since
they're the kind of thing that gets renamed.

## Pre-IPO / tokenized equities: no shortcut flag exists

There's no `is_pre_ipo` boolean. A ticker alone is not enough to tell — some genuinely
novel-sounding tickers (SKHX/SK Hynix, CRCL/Circle, KIOXIA) are already publicly traded.
To compute a real pre-IPO share of volume, look up each ticker's actual IPO date
independently and cut the time series there (e.g. SpaceX/SPCX IPO'd 2026-06-12 — volume
before that date is pre-IPO, after is not).

Also watch for **product duplication across issuing platforms**: the same underlying
instrument can exist as separate onchain products with different symbol suffixes per
platform (e.g. Dinari's dShares `FBTC.d`/`BTCO.d` vs. Robinhood's plain `FBTC`/`BTCO` are
two distinct products tracking the same underlying ETF, each with its own supply/value —
summing them as if one product double-counts; treating them as unrelated undercounts
the ecosystem's real coverage of that name). When a ticker search comes back empty,
search `symbol`, `name`, and `product_name` — the same instrument can be indexed under
any of the three depending on platform.

## Missing prices: don't report a blank

Newly-listed or illiquid tokenized assets often have `price_usd`/`market_cap_usd` = NULL
in supply tables — there's no live price feed yet. Rather than surfacing a blank or
silently dropping the row, fall back to `supply × external NAV/share price` as an
estimate, and label it clearly as an estimate rather than a measured value.

## Exclude known bad-data tokens before ranking

RWA holder/concentration rankings are vulnerable to tokens with large onchain supply
and no verifiable real-world backing (seen in practice: "QGold," "UGold" — billions of
tokens, no real reserve). These dominate a naive top-holders or top-token ranking with
numbers that mean nothing. Sanity-check any RWA token that appears unexpectedly large
before including it, rather than assuming supply-onchain implies legitimacy.

Similarly, filter out one-off **launch-day migration spikes** in mint/burn activity
(e.g. a token's initial listing mint/burn from migrating existing balances onto a new
contract) before charting "issuance" or "flow" over time — a single migration event can
dwarf every subsequent real economic period and make the whole chart about one day.

## TVL / collateral double-counting

When joining RWA tokens into a DeFi TVL context (RWA-as-collateral), sum only
`is_primary` balances (or the equivalent "primary ledger position" flag) — a position
can appear in more than one protocol-side ledger entry for the same collateral, and
summing all of them double-counts.

## Geography is a proxy, not a measurement

Allium has no native geographic data for RWA holders or flows — the chain is
pseudonymous. Entity/issuer-jurisdiction labels (via identity/entity tables) are the
closest legitimate proxy for "where is this happening," but say so explicitly rather
than presenting it as measured geographic data.

## Time windows: don't trust a relative default for "all of [year]"

When a request is "all RWA transfers in 2024" or similarly scoped to a calendar period,
use literal date bounds (`BETWEEN '2024-01-01' AND '2024-12-31'`), not a relative
rolling window (`CURRENT_DATE - INTERVAL`). RWA tables aren't necessarily clustered
tightly enough to make a silently-wrong window cheap to catch — verify the bounds
explicitly.

---

## Data source

Every chain database has its own `rwa` schema (`<chain>.rwa.*` — e.g.
`ethereum.rwa.transfers`, `ethereum.rwa.supply_change`, `ethereum.rwa.supply_daily`). For
anything that spans more than one chain, **prefer the dedicated `rwa` database over
`crosschain.rwa`** — the crosschain-rollup naming has moved to its own top-level database:
`rwa.core.transfers`, `rwa.core.supply_daily`/`supply_latest`,
`rwa.core.balances_daily`/`balances_latest`, and `rwa.registry.catalog`/`deployments` for
issuer/asset-class/asset-type taxonomy and native-vs-bridged deployment metadata. Don't
reach for an old `crosschain.rwa.*` name from memory or a prior session — that naming has
been superseded.

Table and column names move as this schema evolves, so don't hard-code any of the names
above from memory. Run `data-matching` first to confirm the current tables for your
specific question, and use `search_schemas`/`search_docs` directly
if you need to double check a column before writing SQL.
