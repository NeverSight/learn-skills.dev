---
name: lending-analysis
description: >
  Methodology playbook for analyzing DeFi lending protocol data on Allium — Aave,
  Morpho, Fluid, Euler, Maple, Compound-style forks, and per-chain lending markets.
  Use whenever a question touches deposits, borrows, liquidations, collateral swaps,
  utilization, TVL, or leverage on a lending protocol — even if the user just names a
  protocol/asset or asks to compare two lending metrics tables. Covers the
  table-per-event-type join gotchas, column-naming inconsistencies, and
  liquidation-fill double-counting that come up repeatedly before you write the SQL.
---

# Lending Analysis

Lending schemas split activity across several event-type tables
(deposits/withdrawals/loans/repayments/liquidations) rather than one unified "lending
event" table. Most mistakes come from querying only one of them, or joining them wrong.

## Coverage is broader than Aave, and uneven across event types

Lending tables typically cover many protocols and forks beyond the obvious flagship
(Aave) — Morpho Blue, Fluid, Euler, Maple, and a long tail of forks. Don't scope a query
to "Aave only" by default; check what's actually in scope first.

Coverage isn't uniform across event types, either — a narrower table like `flashloans`
may only support a subset of protocols (e.g. just the ones with native flash-loan
functions) even when the broader deposits/loans tables cover many more. If you're
joining flash-loan data to general lending activity, you've implicitly narrowed your
protocol scope to whatever `flashloans` supports — say so.

## No table labels "collateral swap" or "debt swap" — derive it from a join

There's usually no explicit event type for portfolio-management operations like
collateral swaps, debt swaps, or leveraging/deleveraging. Detect them by joining the
event-type tables on `transaction_hash` and comparing which pair of tables fired with
which tokens:
- withdrawal + deposit (different tokens), no loan/repayment → collateral swap
- repayment + loan (different tokens), no deposit/withdrawal → debt swap
- deposit + loan → leveraging up
- repayment + withdrawal → deleveraging

Because of this, **using only the `loans` table as a proxy for "any lending interaction"
undercounts significantly** — new borrows are one slice of activity; a large share of
real position-management activity (swaps, deleveraging, self-liquidation) never touches
`loans` at all and only shows up in the other three tables.

There's typically no dedicated table for "why" a flash loan happened either (arbitrage
vs. collateral swap vs. a governance/exploit action) — classify it by checking whether
other tables share the same `transaction_hash` (a DEX trades table, a governance-related
raw-logs pattern, etc.), the same join technique as above.

## Join performance: filter by date before joining by hash

Lending event tables are usually clustered by `block_timestamp::date`, not by
`transaction_hash`. A multi-table join keyed purely on `transaction_hash` (to detect the
patterns above) won't get any partition pruning and will scan full tables. Pre-filter
each table to your date range in a CTE before the hash join.

## Column names are inconsistent across tables — check before assuming

Don't guess a column name by analogy from a sibling table; the naming isn't uniform:
- `withdrawals` uses a "withdrawer"-style column, `deposits` uses a "depositor"-style
  column, `loans` uses a "borrower"-style column, and `repayments` can have **both** a
  borrower column and a separate repayer column (they can differ — someone else can
  repay on a borrower's behalf).
- On `liquidations`, the token-symbol-style column typically refers to the **seized
  collateral**, and a separate "repay token" column refers to the **debt token being
  repaid** — these are easy to swap by mistake since both are "a token involved in the
  liquidation."
- USD columns are consistently named one way (e.g. `usd_amount`) — don't assume a
  differently-cased or differently-ordered variant (`amount_usd`) exists on any given
  table without checking.

## Ranking by volume: exclude nulls, don't let them win

Assets without a reliable price feed (exotic principal-token / interest-bearing wrapper
tokens are a common case) can have a real, high transaction count but a NULL USD amount.
If you rank "top assets by volume or count" without filtering `usd_amount IS NULL` first,
these can silently displace genuinely large assets (mainstream stablecoins, ETH) from a
top-N list purely because of a missing price join, not because they're actually smaller.

## Utilization: compute per-asset, not just protocol-level

A protocol-wide blended utilization figure can look moderate (e.g. ~45%) while
individual markets within it sit near 100% utilized (commonly stablecoins and ETH, which
tend to be the most in-demand borrow assets). If the question is really "is this market
tight," break utilization (`outstanding_loans_usd / supplied_amount_usd`) out per-asset
via a markets-grain table grouped by token, rather than trusting the protocol-level
aggregate alone.

## TVL/metrics tables aren't a linear pipeline — and don't always agree

A common shape is: a fine-grained markets-level table (project + protocol + token +
market, interpolated end-of-day) feeds two separate sibling aggregations — one
protocol-level "lending activity" table with its own TVL-style figure, and one
token-level raw onchain balance/TVL table. These are **not** the same number computed
two ways; a same-day, same-project comparison found differences of several percent
between them, likely from different pricing or timing in each pipeline. Pick one TVL
source for a given analysis and stay consistent — don't mix the two mid-analysis or
average them together.

## Cross-chain normalization

Column conventions established on EVM chains (e.g. an event-type column indicating
what kind of lending action occurred) don't automatically mean a non-EVM chain (Solana)
lacks the equivalent — verify via schema search rather than assuming a gap. A
crosschain/unioned lending table is more likely to have that field fully populated for
every source chain even if a chain's own native-schema table structures it differently
upstream — prefer selecting directly from the crosschain table over hardcoding a
per-source-chain assumption.

## Liquidation fills: check cardinality on both sides of a join

If a liquidation event can be filled by multiple partial fills sharing the same (user,
asset, timestamp) key, joining fill-level rows directly to an event-level table (one row
per liquidation event, e.g. total collateral seized) fans out — the event-level field
gets counted once per extra fill, double-counting it. Pre-aggregate fills to (user,
asset, timestamp) with SUM/COUNT before joining to the event-level table.

This is a general fills-to-event cardinality mismatch, not specific to liquidations —
whenever you're joining a many-rows-per-key table to a one-row-per-key table, check
cardinality on **both** sides (`COUNT(*) GROUP BY key` on each) before declaring a
double-counting fix complete. It's possible the "event-level" side also has unexpected
duplicates, which would cause underestimation instead — a one-sided cardinality check can
miss that.

---

## Data source

Every chain database has its own `lending` schema (`<chain>.lending.deposits`,
`withdrawals`, `loans`, `repayments`, `liquidations`, `markets_daily`, `metrics_daily`).
Like DEX, lending doesn't have a dedicated crosschain database yet — for a question
spanning multiple chains, use the multi-chain combo views under `crosschain.lending`
(`crosschain.lending.metrics_daily`, `tvl_daily`, `repayments`, and the other
per-event-type tables) rather than unioning per-chain tables by hand.

Table and column names move as this schema evolves, so don't hard-code any of the names
above from memory. Run `data-matching` first to confirm the current tables for your
specific question, and use `search_schemas`/`search_docs` directly
if you need to double check a column before writing SQL.
