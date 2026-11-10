---
name: desk-incident-response
description: What the desk does when something goes wrong on Hyperliquid or in the autonomous loop - unknown send results, unexpected fills or positions, unprotected positions, stuck or orphaned orders, API outages, rate limiting, suspected API wallet compromise, a gate or guard refusing everything, and a runaway loop. Contain first, halt when in doubt, reconcile from the exchange record, act only through gated tickets, then review. Use the moment anything does not match the ticket.
license: MIT
metadata:
  version: "1.2.0"
  author: Galleon Labs
  category: desk
---

# Incident response

An incident is any moment when the exchange record and the desk's expectation disagree, when the desk cannot see the exchange at all, or when the loop itself misbehaves. The reflex is: stop adding, look, contain through the gate, then review. Never widen the harm by improvising. Halting is cheap and reversible by the user; an unreconciled send is neither.

## Declare

Any role can declare an incident. Post on the floor (or write it in the cycle journal):

```
INCIDENT INC-20260907-01 | 11:40 UTC | HG-20260907-02 | send timeout, result unknown | owner: Execution Trader
```

The Desk Lead confirms an owner (usually the Execution Trader for order/position incidents, the Risk Manager for exposure incidents, the Desk Lead for access and loop incidents). New proposals pause until the incident is contained. Every halt is an event in `autonomy/events.jsonl`.

## Playbooks

### A. Unknown send result (`desk_send.py` exit 3: timeout, 5xx, exception after send)

1. Do not resend. Halt the desk (`python3 /workspace/hypergrok/scripts/kill_switch.py halt --desk-root /workspace/trading-desk --reason "unknown send result HG-..."`); it stays halted while this is unresolved.
2. `orderStatus` by the cloid in `autonomy/sends.jsonl`; `openOrders`; `userFills` since the send; `clearinghouseState`.
3. Found: continue reconciliation as normal; journal that the response was lost; the user may resume.
4. Not found: that is not proof. The original can still arrive after any number of clean checks, so a replacement waits until the send's `expiresAfter` deadline has passed and one further check comes back clean. Then report `unconfirmed, original expired at <UTC>`. A replacement is a new ticket with a fresh Risk PASS and a fresh gate PASS; the gate refuses the old id.
5. If the exchange later shows the original order after a second one was sent: the desk has double exposure. Go to playbook C.

### B. Rejected order or partial fill

- Rejection string in the response (`error`): quote it, map it via `hyperliquid-api-reference` (price precision, minimum notional, insufficient margin, reduce-only would increase position, invalid tif...). Fix is a new ticket, not a tweak-and-resend.
- Partial fill on an IOC: the unfilled remainder is gone and the position is smaller than the ticket. Any `normalTpsl` children were **never placed** (children appear only when the parent fills fully, or is partially filled and then margin-cancelled), so the filled part is unprotected: report the actual size and get a stop for that size placed at priority (playbook D).
- Partial fill on a resting order: normal; reconciliation continues.

### C. Position does not match expectation (too big, wrong side, unexpected market)

1. Read `clearinghouseState` and `userFills` for the last hour; establish the exact state. Halt the desk.
2. Risk Manager computes exposure and liquidation distance now.
3. If exposure breaches limits: an **emergency reduce ticket** (`kind: close`, reduce-only IOC at a slippage bound for the excess size) is written by the Risk Manager with its JSON file, taken through the gate (reduce-only passes even while halted), and sent by the Execution Trader through `desk_send.py`. Priority handling, same protocol.
4. Journal what happened and why the mismatch occurred once known.

### D. Unprotected position (no resting stop)

1. Risk Manager flags it; the Desk Lead treats it as priority, before any scan or new idea.
2. Protective stop ticket (`kind: protect`: trigger, reduce-only, correct side, sized to the position read live) with its JSON file, through Risk PASS and straight through the gate. The gate always passes `protect` tickets, halted or not; no standing approval is needed or consulted. This is also the path after any partial fill of an entry that carried `normalTpsl` children.
3. `desk_send.py` sends it; reconcile that the trigger is resting in `frontendOpenOrders`.
4. If `desk_send.py` refuses or the exchange rejects the stop, halt and alert the user with the exposure and the distance to liquidation, and say plainly that the fastest fix is theirs in the Hyperliquid app. Do not keep retrying a rejected stop; read the rejection, fix the ticket if it was the ticket, and otherwise wait.

### E. Orphaned or stuck orders

- Orphaned (position flat, stop still resting): a cancel ticket, gated and sent like any other; the cycle does this as housekeeping. Confirm from `openOrders`.
- Stuck (order the exchange shows that the desk cannot cancel): read `orderStatus`; check whether it is a trigger child of a grouped order; try `cancelByCloid` if `cancel` by oid fails; if still stuck, report with the exact response and stop.

### F. Exchange unreachable, rate limited, or degraded

- `/info` failing or slow: mark the desk **blind**; no new tickets; watches log the outage; check `https://api.hyperliquid.xyz/info` with a tiny `allMids` call every minute; report when back. Blind for longer than one cycle interval: halt.
- HTTP 429: back off (respect the response), reduce polling, prefer WebSocket for continuous data. Read `userRateLimit` for the account's remaining budget.
- Blind with open positions: the user is told plainly that stops resting **on the exchange** still work while the desk cannot see; that is why stops are mandatory.

### G. Suspected API wallet compromise or misuse

Signs: orders or fills the desk did not send (no matching cloid in `autonomy/sends.jsonl`), leverage changes nobody approved, unfamiliar `cloid`s.

1. Halt the desk. The user revokes the API wallet immediately in the Hyperliquid app (the API page, `/API`) - the desk cannot do this for them and must not delay them.
2. Once revoked, the desk's key is dead; the Execution Trader confirms a `--dry-run` still builds but a real send would fail.
3. Read the full `historicalOrders` and `userFills` since the last known-good time; Risk Manager assesses exposure; emergency reduce or protection tickets as needed after the user creates a fresh API wallet and re-provisions it.
4. Rotate: new key through the secure secret store or the user's key file only; nothing pasted in chat; journal the rotation time.
5. Incident review with a timeline.

Remember the shared computer: every role could read the key's environment; that is why only an API wallet key (trade-only, cannot withdraw) is ever provisioned, and why testnet comes first.

### H. Policy gate or guard refusing every ticket

Symptom: consecutive FAILs or exit 2 on tickets that look fine, or the Claude Code guard denying `desk_send.py` with a valid-looking approval. In order:

1. **Validate the policy.** `python3 /workspace/hypergrok/scripts/policy_gate.py policy --desk-root /workspace/trading-desk`. A ceiling breach or a schema error invalidates the whole file; only the user can fix it. Report the exact line.
2. **Check the gate key.** `autonomy/gate.key` present, mode 600, unchanged since the approval was issued. A regenerated key invalidates every outstanding approval; run the gate again rather than editing anything.
3. **Check the halt.** `kill_switch.py status`. A halted desk fails every `entry` at the `halt` gate by design; reduce-only tickets still pass. If the halt is unexpected, read `autonomy/events.jsonl` for who wrote it and why.
4. **Check the clock.** Approvals live ten minutes and tickets thirty, both in UTC. A machine clock that is wrong makes every approval expired or every ticket stale; compare `date -u` with the exchange's timestamps in any `/info` response.
5. Still failing: the gate is doing what it was told. Post the failed gate names and their numbers, do not touch the ticket, the policy or the key, and wait for the user.

### I. Runaway loop

Symptom: cycles overlapping, sends faster than expected, the same proposal reopened every cycle, or a cycle that never ends.

1. **Heartbeat.** Read `autonomy/heartbeat.json` and the latest `autonomy/cycles/<UTC>.log`; note which step the cycle is in.
2. **Lock.** `autonomy/cycle.lock` stops a second cycle from starting; a stale lock from a crashed cycle blocks everything, a missing lock lets cycles overlap. Do not delete a lock while the process that holds it is alive.
3. **Halt.** `kill_switch.py halt --reason "runaway loop"` first; the rate gates (`rate-hour`, `rate-day`) and the `not-sent` ledger check bound the damage in the meantime, but a halt stops new entries at once.
4. **Cron.** Disable the timer or the Grok Bot routine, then let the running cycle finish or time out (`autonomy_cycle.py` enforces one), reconcile every `in-flight` entry in `autonomy/sends.jsonl`, and only then let the user re-enable the schedule and resume.

### J. Daily loss stop hit

Not an incident, but handled like one: Risk Manager halts the desk with the reason, posts it, protective and exit tickets continue through the gate, new risk waits for the user's written reset and `kill_switch.py resume`.

## Containment rules

- Contain with the smallest reversible action. Reduce, don't flip. Cancel one, not all, unless the user has asked for a dead-man's switch and its condition has occurred.
- Every containment action is still a ticket with its own JSON file and a gate PASS, sent through `desk_send.py`. Reduce-only containment passes while halted; that is what the halt is for.
- Never withdraw, transfer or bridge as an incident response.
- Never resend to "make sure".
- Never resume a halt; the user does, from their own terminal.

## Close the incident

The Trade Reviewer writes the incident review (`desk-post-trade-review`), the Desk Lead lifts the proposal pause and records the corrective action and its owner in `desk.md`. If the desk was halted, the review says so and the user decides when to resume.
