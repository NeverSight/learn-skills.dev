---
name: desk-execution-protocol
description: The Execution Trader's procedure for turning a gate-approved ticket into one Hyperliquid action through scripts/desk_send.py and reconciling it - the pre-send checklist, what the sender checks for you, exit codes, single-send discipline, unknown-result handling and the execution report. Use before and after every send, cancel, modify, leverage change or close.
license: MIT
metadata:
  version: "1.3.0"
  author: Galleon Labs
  category: desk
---

# Execution protocol

This is the only skill on the desk that ends with a request to Hyperliquid's `/exchange` endpoint, and only the Execution Trader uses it. The request itself is built and signed by `scripts/desk_send.py`; the API mechanics it follows are in `hyperliquid-orders` and `hyperliquid-positions`. This skill is the discipline around the script.

## Inputs

- `proposals/<id>.ticket.json`, written by the Risk Manager's PASS, and the matching markdown ticket under `## risk` in `proposals/<id>.md`.
- `proposals/<id>.approval.json`, written by `policy_gate.py check` for those exact ticket bytes, unexpired (ten minutes) and unspent.
- The desk computer configured per `hyperliquid-setup`: `HYPERLIQUID_NETWORK`, `HYPERLIQUID_ACCOUNT_ADDRESS`, and the API wallet key resolvable by `engine/secrets.py` from the environment, a `HYPERGROK_KEY_COMMAND` secrets-manager command, or the user's mode-600 key file (never printed; the sender reports the source, not the value; `desk-operations` section 1).

## Pre-send checklist

Run every item and write the result under `## execution` before sending. Any failure: do not send, name the item, hand back to the Desk Lead.

1. **Valid approval for these exact bytes.** `python3 /workspace/hypergrok/scripts/policy_gate.py verify --desk-root /workspace/trading-desk --ticket proposals/<id>.ticket.json` exits 0. If the Risk Manager re-issued the ticket after the gate ran, the approval is dead and the gate runs again.
2. **Network.** `HYPERLIQUID_NETWORK` equals the ticket's network. Mainnet is never assumed.
3. **Account and wallet.** `HYPERLIQUID_ACCOUNT_ADDRESS` equals the ticket's account. The API wallet still acts for it (the readiness check in `hyperliquid-setup` section 5). If the desk has never sent from this wallet on this network, rehearse on testnet first, not on mainnet.
4. **Price still valid.** Fresh mid from `allMids` is within the ticket's slippage tolerance of the ticket price. For a stop or take-profit ticket, the trigger price is on the correct side of the current mark.
5. **Formatting.** Asset index from live `meta`; price rounded to at most 5 significant figures and at most `6 - szDecimals` decimals for perps (`8 - szDecimals` for spot); size rounded **down** to `szDecimals`; notional at least 10 USD; leverage: for an `entry` ticket the sender reads the account's leverage for that market and, if it differs from the ticket, sends `updateLeverage` first and confirms it before the entry goes; a change that does not confirm stops the send.
6. **cloid and expiry.** A fresh 16-byte client order id (`0x` + 32 hex chars) per order, never reused, written to the send ledger before the request leaves; `expiresAfter` one minute out, written beside the cloid. The cloid makes a duplicate detectable; `expiresAfter` is what later makes the original provably dead.
7. **One action.** Entry plus its stop and take-profit go in one `order` action with `grouping: normalTpsl`. Protection for an existing position is a standalone reduce-only trigger. A cancel is its own `kind: cancel` ticket by oid; a leverage change rides with the entry that needs it.
8. **Nothing else pending.** No entry in `autonomy/sends.jsonl` whose latest status is `in-flight` or `unknown`. If there is, reconcile it first.

Items 4 to 7 are performed by `desk_send.py` itself, from live `meta` and `allMids` at the moment of the send; it refuses on drift, wrong-side triggers or bad rounding and prints what it computed. The Execution Trader still reads that printed output line by line and records it, because a refusal with a reason is the desk working and a send with numbers nobody looked at is not.

## Send

One invocation, once:

```bash
python3 /workspace/hypergrok/scripts/desk_send.py --desk-root /workspace/trading-desk --ticket proposals/<id>.ticket.json
```

`--dry-run` verifies the approval, builds and prints the action and signs nothing; use it on any first-of-a-kind ticket. The real run re-verifies the approval, appends its intent and cloids to `autonomy/sends.jsonl` **before** sending, sets `expiresAfter`, sends exactly once with a finite timeout, reconciles by cloid and writes `proposals/<id>.execution.json`.

| Exit | Meaning | Then |
| --- | --- | --- |
| 0 | sent; response and reconciliation in `<id>.execution.json` | continue to reconciliation |
| 1 | refused before sending (no valid approval, spent approval, drift, halt, environment mismatch); nothing left the machine | record the reason, hand back to the Desk Lead |
| 2 | environment problem (key, SDK, network unreachable); nothing sent | `hyperliquid-setup`; nothing to reconcile |
| 3 | unknown result: the request left the machine and no clean response came back | playbook A below; no resend |

Interpret statuses in the execution file per `hyperliquid-orders`: `resting` (oid), `filled` (totalSz, avgPx, oid), `waitingForTrigger`, `waitingForFill`, or an `error` string. A top-level `status: err` is an action-level rejection: nothing was placed, and the fix is a new ticket.

### Maker-first

An `entry` ticket whose `execution.style` is `maker-first` (the engine sets it from `execution_style` in the strategy's `params.json`; the shipped strategy has it on) is still one invocation and one approval, but the sender performs a short sequence rather than a single IOC, and writes every step under `steps` in `<id>.execution.json`:

1. Post a post-only `Alo` limit at the mid moved inside by `maker_offset_bps`, with the stop grouped as usual, under the ticket's cloid family and the same `expiresAfter` discipline.
2. Poll the order by cloid for `maker_wait_s`. Filled in full: done, at the maker fee.
3. Not filled: cancel by cloid. If part filled, place a standalone reduce-only stop for exactly the filled size before anything else, so no fraction is ever unprotected.
4. Send the remainder as the bounded IOC the ticket would have been, with its own stop, unless the mid has moved past the ticket's slippage tolerance, in which case the remainder is dropped and the record says so.

The Execution Trader does not perform these steps by hand and does not re-approve between them: they are the sender's, inside the one send, and the exit codes above mean the same thing. Read `steps` in the record and report which path the fill took (maker, partial plus IOC, IOC, or dropped) and the fee that resulted; the paper record measures the real maker fill rate from those steps. What it saves and does not save is in `desk-operations` section 2.

## Unknown results

Exit 3 - a timeout, connection reset, HTTP 5xx, or a client exception after the request left the machine - is an **unknown result**. Treat it as possibly executed:

1. Do not resend.
2. Query `orderStatus` for the cloid from the ledger; check `openOrders` and `userFills` for it; check `clearinghouseState` for a position change.
3. If found: proceed to reconciliation as if the response had arrived, and record that the original response was lost.
4. If not found: **a negative check is not proof.** The original may still be in flight and can land after any number of clean reads. Do not let two quiet checks authorise a replacement.
5. The ticket is dead only when the original is *incapable of arriving*. That is the send's `expiresAfter` deadline passing (the exchange rejects it after that), confirmed by one more check once the deadline is behind you. `desk_send.py` always sets it, so this is knowable; if for any reason the ledger shows no deadline, stop, halt the desk and hand the decision to the user. Never assume elapsed time alone.
6. Then report `unconfirmed, original expired at <UTC>` to the Desk Lead and halt the desk (`kill_switch.py halt`) until it is resolved. A replacement is a new ticket with a fresh Risk PASS and a fresh gate PASS; the gate's `not-sent` check will refuse the old id, which is the point.

## Reconciliation

Immediately after the response, and again when fills arrive:

- `orderStatus` by cloid or oid: the exchange's view of the order.
- `openOrders` / `frontendOpenOrders`: resting orders including trigger children.
- `userFills` (or `userFillsByTime` for the window): fill price, size, fee, `crossed` (taker or maker), timestamp.
- `clearinghouseState`: position size, entry, leverage, liquidation price, margin used.

Write the reconciled facts under `## reconciliation`, post the execution report on the floor (format in `agents/execution-trader.md`), and DM the Trade Reviewer with the id and the report.

## Cancels, modifies, leverage, closes

Each is its own ticket (suffix `-B`, `-C`...) with its own JSON file, its own `kind`, its own Risk PASS and its own gate run, sent through `desk_send.py` like anything else.

- **Cancel:** `kind: cancel` with the `oid` from `openOrders`, reduce-only, gated like everything else (the gate checks the oid is actually resting). Confirm removal from `openOrders`.
- **Modify:** Hyperliquid's `modify`/`batchModify` cancels a resting limit order and places the replacement in one action (new oid, fresh cloid); the replacement must itself rest (`Alo`, or a non-executable `Gtc`). Stops and take-profits cannot be modified: place the new trigger order (`kind: protect`), confirm it is resting, then cancel the old one on a `cancel` ticket, so the position is never unprotected. The sender does not use `modify`.
- **Leverage or margin mode:** carried by the `entry` ticket's `leverage` and `margin_mode`; the sender issues `updateLeverage` before the entry only when the account differs and records the step in the execution file. On a market with an open position the Risk Manager keeps the ticket at the position's current leverage.
- **Close:** `kind: close`, reduce-only IOC at a slippage-bounded price for the position size read live seconds before the send. Then read `clearinghouseState` again: if the position is gone, cancel the orphaned protective orders; if it only shrank (a partial fill on the close), the remainder is still open and still needs its stop, so resize protection before cancelling anything. Report which case it was.
- **Dead-man's switch:** `scheduleCancel` only when the user asks for it, with the time written in the report; remember it cancels all of the account's open orders when it fires.

`close` and `protect` tickets pass the gate even while the desk is halted; entries do not.

## Rehearsal rule

Any action type the desk has not performed before (first TP/SL bracket, first modify, first close, first isolated-margin trade) is rehearsed on testnet with the same ticket format and a `--dry-run` first before it is done on mainnet. Record the rehearsal in the journal.

## Report

Post the block from `agents/execution-trader.md` on the floor: sent, response, reconciled, fees/funding, next. Keep the raw response in the execution file and the proposal file, not in chat.

## Never

- Never send without a Risk PASS and a valid gate approval for this exact ticket, and never through anything but `desk_send.py`.
- Never hand-write an SDK `Exchange` call or `curl` `/exchange`; the snippets in the Hyperliquid skills are for reading, reconciling and testnet rehearsal.
- Never send from a main-wallet key or with a key pasted in chat.
- Never withdraw, deposit, bridge, transfer, send tokens, approve builder fees or touch vaults and sub-accounts.
- Never resend on an unknown result while the original could still arrive; only an expired original and a fresh gate PASS on a new ticket permit a replacement. Never cancel-all as a reflex.
- Never resume a halt. The user does that.
- Never treat a clean `orderStatus` read as proof that an unknown result did not execute; only an expired original proves that.
