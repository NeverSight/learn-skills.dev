---
name: data-matching
description: |
  Match an analytical question to the right Allium table, metric, dashboard, or
  realtime endpoint. Required when selecting a new data source for a query or
  analysis: define the intended meaning, compare schema candidates, test
  coverage, and record the fit and caveats before treating a source as correct.
  Run this before `allium-investigation` or any other analysis.
---

# Data Matching

The schema KB finds candidates. This skill decides whether a candidate actually
matches the user's question. A semantically similar table is not automatically
the right metric.

Fetch this skill when introducing a new data source. Do not repeat it when
making a narrow refinement to a previously inspected saved query unless the
metric, source, scope, or interpretation changes.

## 1. Translate the question into a data contract

Before selecting a source, state the required:

- **object** — transaction, wallet, holder, position, token, protocol, entity,
  or another unit;
- **measure** — count, balance, supply, volume, price, fees, active wallets,
  or a defined derived metric;
- **grain** — event, block, day, month, wallet-token, protocol-chain, etc.;
- **scope** — networks, addresses, assets, population, inclusions, and
  exclusions;
- **time semantics** — current state, point-in-time snapshot, activity over a
  window, or historical time series;
- **freshness and output** — realtime lookup, ad-hoc analysis, reusable query,
  dashboard, or recurring workflow.

Ask a clarifying question if a missing field could materially change the
source or conclusion. Otherwise state a reasonable assumption before querying.

## 2. Find and inspect candidates

1. Use `search_docs` for product, metric, and known-domain terminology.
2. Use `search_schemas` to find 3–5 candidate tables. Search with the object
   and measure, not only the user's project name.
3. Fetch the most promising candidates with `search_schemas(id=..., include_content=True)`.
   Read columns, grain, descriptions, and caveats; a search result title alone
   is never sufficient for selection.
4. Check relevant canonical Terminal results with `search_terminal` and
   `get_terminal_results` before recreating a commonly used metric.

Prefer a per-chain table for a single-chain question. Use cross-chain sources
only when the comparison actually spans chains and the source's chain and asset
semantics fit the question. Use Realtime for current state of a known asset or
wallet; use Explorer/SQL for historical, comparative, or aggregated analysis.

If the question falls in a covered sector — real-world assets, stablecoins,
bridges, DEX/AMM trades, or lending — check whether a sector-specific skill
(`rwa-analysis`, `stablecoin-analysis`, `bridge-analysis`, `dex-analysis`,
`lending-analysis`) is available before hand-rolling the table choice; those
skills package the recurring table/column pitfalls for that sector and can
save a coverage-probe cycle.

## 3. Compare candidates against the contract

For each serious candidate, check:

- Does its row grain match the requested unit, or would aggregation/joining
  change the meaning?
- Is it a flow, a snapshot, or a cumulative value? Do not substitute one for
  another without saying so.
- Does it include the requested networks, dates, assets, and entity universe?
- Are token units, prices, labels, bridged representations, or attribution
  fields defined at the required level of certainty?
- Is there a curated metric or canonical dashboard that is safer than deriving
  the measure from raw rows?

Do not resolve an ambiguity by choosing the top-ranked hit. Keep alternatives
when they measure different, defensible things and explain the difference.

## 4. Prove coverage before building the analysis

Run a small, bounded query against the recommended source when the metric is
load-bearing, the chain is newly selected, or coverage is uncertain. Inspect a
few rows plus a short time series or aggregate.

Coverage is not proven merely because a chain or table appears in search. Stop
and rescope if the requested period is empty, thin, stale, or represents a
different economic object. A wrapped or bridged asset is not proof of native
chain coverage.

## 5. Return a match manifest

Before writing the full query, present the decision in this form:

| Field | Record |
| --- | --- |
| Requested meaning | Object, measure, grain, scope, and time semantics |
| Recommended source | Table, endpoint, or canonical dashboard/query |
| Why it fits | Evidence from schema/docs and coverage probe |
| Alternatives rejected | Candidate and the semantic mismatch |
| Caveats | Coverage, freshness, attribution, unit, or aggregation limits |
| Decision | Use / use with caveat / rescope / unavailable |

Carry the selected source, caveats, and coverage result into the query and
final answer. If the result becomes decision-relevant, save it via
`create_explorer_query` and follow `allium-investigation`'s reproducibility
step before sharing it.
