---
name: desk-post-trade-review
description: The Trade Reviewer's procedure for journaling desk activity and reviewing trades from the exchange record - process graded separately from outcome, execution costs measured, one repeatable finding per review, plus the weekly desk review. Use after any send, when a trade closes, on the weekly routine, or when the user asks "how did that go".
license: MIT
metadata:
  version: "1.1.0"
  author: Galleon Labs
  category: desk
---

# Journal and post-trade review

The journal is the desk's memory; the review is how the desk learns. Both come from the exchange record first and chat second, and both keep process and outcome apart.

## 1. Journal

`/workspace/trading-desk/journal/YYYY-MM-DD.md`, one file per active day, appended in time order. Entry types:

```
14:02 UTC  HG-20260907-01 opened   ETH-PERP long idea (origin user); status evidence
14:12 UTC  HG-20260907-01 risk     PASS 0.4827 ETH, stop 2,900, 0.5% risk stressed (risk-limits v3); ticket.json written
14:15 UTC  HG-20260907-01 gate     PASS all gates, approval expires 14:25 (policy_gate.py)
14:16 UTC  HG-20260907-01 sent     buy 0.4827 @ 3,000 Gtc + sl 2,900 (normalTpsl); cloid 0x9f3e...; oid 1839201122, sl waitingForFill (desk_send.py exit 0)
16:05 UTC  HG-20260907-01 fill     0.4827 @ 3,000.0 maker, fee $0.29
09:12 UTC  HG-20260907-01 closed   tp 3,089.6, fee $1.44; position flat; sl 2,900 cancelled 09:13; realised_gain event written
10:00 UTC  limits                  risk-limits v3 -> v4: max positions 3 -> 4 (user, reason: adding HYPE)
11:40 UTC  incident INC-20260908-01 send timeout on HG-20260908-02 (exit 3); desk halted; not on exchange, waited out expiresAfter 11:41, re-checked clean; user resumed 11:50
14:31 UTC  HG-20260908-03 gate     FAIL open-risk (4.3% after vs 4.0% limit); proposal ended
18:00 UTC  note                    maker entries at 10 bps depth filled within 2h on both attempts this week
```

In the autonomous cycle the `CYCLE` block from `desk-autonomous-loop` section 1 is appended once per cycle, with the same lines above for anything that happened inside it. Rules: append only; corrections are new lines with `correction:`; every line has a UTC time and an id where one exists; no opinions in the journal (those go in reviews).

When a trade closes, the Trade Reviewer (or the cycle's reconcile step) also appends one event line to `/workspace/trading-desk/autonomy/events.jsonl`, which the gate's cooldown check reads:

```
{"type":"realised_loss","id":"HG-20260907-01","at":"2026-09-08T09:12:00Z","pnl_usd":-12.3}
```

`type` is `realised_loss` or `realised_gain`; `pnl_usd` is the fill PnL after fees from `userFills`, signed. One line per closed trade, never edited.

## 2. Trade review

Trigger: a proposal reaches `closed`, or the user asks. Inputs, always listed with timestamps:

- the proposal file (ticket, PASS, gate output, execution, reconciliation) and its `ticket.json`, `approval.json` and `execution.json`
- `userFills` / `userFillsByTime` for the window: price, size, fee, side, `crossed`
- `historicalOrders` and `orderStatus` by cloid: what rested when, what cancelled
- `userFunding` for the holding window
- optionally the Market Analyst's depth read at send time for expected slippage

Compute:

| Measure | How |
| --- | --- |
| Entry slippage | (fill avg - ticket price) / ticket price in bps, signed against the trade |
| Exit slippage | same for the exit versus its ticket or trigger price |
| Fees | sum of fill fees in USD and as bps of notional; note maker vs taker |
| Funding | sum of funding payments over the window, USD |
| Net result | realised PnL after fees and funding, in USD and in R (R from the ticket) |
| Protection | was a reduce-only stop resting on the exchange for the entire life of the position? gaps in minutes |
| Lifecycle | each stage present, in order, with timestamps; gate PASS for the sent bytes; single send through `desk_send.py`; reconciled |
| Holding time | fill to flat |

Grade:

- **Process:** clean / minor break / major break, with the specific stage named. A major break is any send without a Risk PASS and a gate approval, any send outside `desk_send.py`, any missing protection, any resend on unknown result, or any limit breached.
- **Gate FAILs** are process signals, not outcomes. A FAIL that stopped a ticket is the control working; note which gate and why. A run of FAILs on the same gate (`open-risk`, `equity-fresh`, `ticket-age`) points at sizing that ignores the policy, stale evidence or a slow cycle, and that is the finding.
- **Outcome:** result in R and USD, stated without adjectives.

Then **one thing**: a leak, a control that worked, or a break, chosen because it is repeatable. Not a list.

Write the review under `## review` in the proposal file and send the block (format in `agents/trade-reviewer.md`) by DM to the Desk Lead and the user. Set `status: closed`.

## 3. Weekly desk review

From the journal, proposals and the exchange record for the week:

- proposals opened / rejected / voided / executed / closed
- trades closed: count, hit rate, average win and loss in R, expectancy in R (mean of results), largest loss, largest drawdown in equity terms from `portfolio` or start/end equity
- costs: fees and funding in USD and as a share of gross PnL
- process: number of breaks by type; gate FAILs by gate name; halts and who resumed them; incidents and their status
- limits: any changes and why
- one pattern worth the user's attention, stated as a fact pattern

No recommendations about what to trade. If the user asks, hand strategy questions to the Strategist and sizing questions to the Risk Manager.

## 4. Incident review

For each `INC-YYYYMMDD-NN`: timeline (journal + exchange record), what the desk did, what the controls did, exposure during the incident, root cause where knowable, one corrective action with an owner and a date. Blameless in tone, exact in fact. Written to `/workspace/trading-desk/journal/incidents/<id>.md` and linked from the daily journal.

## Pitfalls

- Reviewing from chat memory rather than fills. Chat says what people meant; fills say what happened.
- Letting the outcome colour the process grade. Grade process first, then look at the outcome.
- Counterfactuals ("if we had held..."). Not evidence.
- Ten findings per review. Nobody acts on ten.
- Editing old journal lines. Append a correction.
