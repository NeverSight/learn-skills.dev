---
name: bridge-analysis
description: >
  Methodology playbook for analyzing cross-chain bridge and messaging-protocol data on
  Allium — CCTP, LayerZero, Wormhole, Across, canonical/application bridges, and
  general lock-and-mint flows. Use whenever a question touches bridge transfer volume,
  net flows between chains, tracing a specific cross-chain transaction, or attributing
  bridge activity to a protocol/integrator — even if the user just names a bridge or
  asks to "trace this transfer across chains." Covers the direction/double-counting
  mechanics and non-EVM tracing gap that come up repeatedly before you write the SQL.
  Distinct from a formal third-party coverage benchmark (see
  bridge-protocol-coverage-assessment for that) — this is the lighter-weight reference
  for getting an individual bridge query right.
---

# Bridge Analysis

Bridge transfer tables are asymmetric by design — they don't always record both legs of
a transfer. Get the directionality model right before summing anything.

## Bridge transfer tables record net single-directional flows, not always both legs

The exact coverage shape depends on the bridge type:
- **Canonical bridges on Ethereum** typically carry both inbound and outbound rows.
- **Application-level bridges**, and bridge activity on **non-Ethereum chains**,
  typically carry only the outbound leg from the chain that initiated the transfer.

This is a deliberate anti-double-counting design, not a coverage gap — but it means
`SUM(usd_amount)` behaves differently depending on which chain/bridge-type combination
you're querying. Check what `direction` values actually exist for the specific
bridge/chain before summing across them, rather than assuming every transfer has a
matching inbound+outbound pair somewhere in the table.

## Filtering to ≥2 target chains creates a double-counting trap a single-chain filter doesn't have

If you filter bridge flows to a list of target chains (e.g. "flows among ethereum,
arbitrum, base") and both ends of a given transfer are in that list, the transfer can
satisfy the WHERE clause twice — once as an outflow row for the source chain, once as an
inflow row for the destination chain — inflating `SUM(usd_amount)`.

- Flag transfers where both source and destination are in your target set as a special
  case rather than summing them in with everything else.
- Prefer `net_flow_usd` (inflow − outflow) as the safe cross-chain aggregate when you
  need a single number spanning multiple chains — it stays correct regardless of whether
  double-counting would otherwise occur, because the same transfer contributes
  symmetrically to both sides and nets out.

## Isolate one protocol correctly

To pull volume for a specific bridge protocol out of a unified/crosschain transfers
table, filter on the protocol identifier field (commonly named `protocol`), not a
generic `bridge` field if both exist — `protocol` is typically the more granular,
reliable filter for isolating e.g. Circle's CCTP specifically. Match case-insensitively.

When reporting one protocol's volume, express it as a share of a meaningful denominator
(e.g. protocol volume ÷ total cross-chain volume for that asset, or ÷ all bridging
volume) rather than an absolute number alone — that's how stakeholders actually reason
about protocol adoption, and it's a more stable metric across time than a raw dollar
figure.

## Bridge identity is derivable onchain; integrator/aggregator attribution is not

Every bridge transfer's protocol (contract address + event signature → registry mapping)
is knowable from onchain data alone. **Who routed the transaction** — which frontend or
aggregator originated it (a bridge's own UI vs. a wallet's built-in bridge feature vs. a
third-party aggregator) — is generally not a standardized onchain field, and dedicated
"aggregator" columns are sometimes deliberately excluded from unified transfer tables to
avoid a different kind of double-counting. Don't expect SQL alone to answer "who routed
this transfer" — that needs off-chain API/analytics data, a contract-level change adding
an integrator parameter, or heuristic `tx.to`/call-stack tracing against a maintained
aggregator-contract registry, and any of those should be flagged as a heavier lift than
a normal query.

## Tracing a specific transfer when there's no direct join key

Some legs simply aren't captured in a per-chain bridge-transfers table — most commonly
**non-EVM-native legs** (e.g. a Bitcoin-origin transfer bridged into an EVM chain), where
the bridge event only shows up as a mint on the destination side with no upstream link
back to the source chain's raw transaction.

The general pattern for tracing this kind of lock-and-mint flow without a direct join
key:
1. Pull the source-chain amount and timestamp from the relevant raw table.
2. Search the destination chain's wrapped-token transfers for a **mint** (`from_address`
   = the zero/burn address) in a short window after the source timestamp.
3. Match on amount within the bridge's fee tolerance (typically a few basis points) —
   exact-amount matching will usually fail because of the fee.

When neither side has a decoded bridge event linking them at all (e.g. a wrapped asset
minted independently of any captured bridge transaction), don't force a transfer-level
join — build an entity map (entity, chain, address, type, confidence) instead and track
correlated-but-independent activity on each side as a flow proxy, presenting it as
correlation evidence rather than a matched trace.

## Fee/gas attribution

Destination-side gas for a bridge-triggered mint or relay is typically paid by the
bridge's relayer address, not the recipient — don't attribute that gas cost to the end
user when reconstructing bridge economics or a fee breakdown for a specific user's
transfer.

## Coverage gaps by surface

If working through Allium's Wallet API rather than raw SQL tables, note that
cross-chain/bridge activity types surfaced there are commonly EVM-only — Solana and
Bitcoin-side bridge activity may not appear in the enriched activity feed and needs
direct raw-table tracing (see above) instead.

---

## Data source

Bridge data lives in two places: every chain database has its own `bridges` schema
(`<chain>.bridges.*`), and there is also a shared `crosschain.bridges` schema for
cross-chain rollups and comparisons. Prefer `crosschain.bridges` for anything that spans
more than one chain rather than unioning per-chain tables by hand.

Within either schema, activity is split into three distinct categories — don't treat them
as interchangeable:

1. **Bridges** — canonical and application-level bridges that move value directly
   (lock-and-mint, burn-and-mint, liquidity-pool bridges).
2. **Messaging protocols** — generalized message-passing infra (e.g. LayerZero, Wormhole,
   CCIP) that can carry a value transfer but isn't itself a bridge; a message doesn't
   guarantee an accompanying transfer, and vice versa.
3. **Aggregators** — routers that select among multiple underlying bridges/messaging
   protocols for a given transfer; the aggregator layer and the underlying bridge it
   routed through are two different attributions, and a query aimed at one will silently
   miss the other.

Each category is split into separate **inbound** and **outbound** tables (e.g. an
outbound-transfers table for the source-chain leg, an inbound-transfers table for the
destinationchain leg) rather than one table with a direction column — this is the same
asymmetric-recording design described above, made explicit at the table level. Join the
two sides on the message/transfer identifier rather than assuming a single table has
both legs.

**Avoid the flat `<db>.bridges.transfers` table where possible — it's deprecated.** It
predates the bridges/messaging-protocols/aggregators split above and doesn't carry that
attribution; a query against it can't distinguish which category or direction produced a
row.

Table and column names drift as this schema evolves, so don't hard-code any of the names
above from memory. Run `data-matching` first to confirm the current tables for your
specific question, and use `search_schemas`/`search_docs` directly
if you need to double check a column before writing SQL.
