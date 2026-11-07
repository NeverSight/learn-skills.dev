---
name: radar-metrics
description: Resolve current model input pricing and report Radar's repository context-savings estimate in tokens and money; use when asked about savings or once near the handoff of substantial Radar navigation.
license: MIT
---

1. Identify the active provider/model from session or runtime context. If the
   exact model is unavailable, select the provider's current general coding
   model as a clearly labeled reference; never ask the user for a rate.
2. Read its current standard, uncached input price in USD per million tokens
   from the provider's official pricing page. Do not use search snippets or
   cached memory. If official pricing is unreachable, say pricing is
   unavailable and report no money estimate rather than guessing.
3. At repository root run
   `radar status --input-usd-per-million RATE`.
4. Render one compact terminal-style panel, not the raw row. Abbreviate every
   displayed count with up to three significant digits: `k`, `M`, `B`, then
   `T`; never print `1000k` when `1M` applies. Use a 20-cell bar rounded from
   `reduction` (`█` saved, `░` retained):

   ```text
   RADAR // CONTEXT DELTA
   [████████████████████] 98.64%
   SOURCE   ~361k tok
   MAPS     ~4.92k tok
   AVOIDED  ~356k tok
   VALUE    ~$0.445493
   MODEL    GPT-5 · $1.25/MTok
   MODE     full-source → maps · estimate
   ```

   Follow it with the official pricing link. Preserve `~` on estimates and
   compact money with `k`, `M`, `B`, or `T` only when it reaches 1,000.
5. Call it an estimated repository snapshot, not observed session usage,
   money spent, or an invoice. Do not accumulate snapshots.

Cadence: on request, or once near handoff after a substantial navigation task;
skip one-off queries and never emit it after every command.
