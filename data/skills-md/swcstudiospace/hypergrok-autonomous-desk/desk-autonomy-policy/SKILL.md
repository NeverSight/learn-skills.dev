---
name: desk-autonomy-policy
description: The written policy that replaces human trade approval on the autonomous desk - the autonomy.json schema, the ceilings it may only tighten, the drawdown risk ladder and the depth multiple, the JSON ticket the Risk Manager writes, what scripts/policy_gate.py checks and the signed approval it issues, the send ledger, the kill switch and who may change what. Use when setting up or changing autonomy, when a ticket is gated, when a gate fails, or when anyone asks "why did the desk (not) send that".
license: MIT
metadata:
  version: "1.0.0"
  author: SWC Studio
  category: desk
---

# Autonomy policy

On the original HyperGrok desk the user approved every trade by typing the ticket id. On this desk nobody is reading the ticket. What stands in for the user is a **policy file** the user wrote once, a **deterministic gate** that checks every ticket against it and against live account state, and a **signed approval** that the one sending script demands before it signs anything. The judgement is still the Risk Manager's; the authority is the user's, expressed in advance and enforced by code that the agents cannot argue with.

## 1. The policy file

`/workspace/trading-desk/autonomy.json`, written by the user from `template/autonomy.json`. Only the user edits it; no Bot, subagent or pass may write it, and the Claude Code guard refuses any tool that tries.

```json
{
  "version": 1,
  "mode": "testnet",
  "account": "0xYourMainAccount",
  "originate": true,
  "cycle_interval_minutes": 15,
  "limits": {
    "max_risk_per_trade_pct": 0.5,
    "max_total_open_risk_pct": 2.0,
    "max_leverage": 3,
    "max_positions": 3,
    "max_notional_per_trade_usd": 2000,
    "allowed_markets": ["BTC", "ETH", "SOL"],
    "daily_loss_stop_pct": 2.0,
    "max_sends_per_hour": 4,
    "max_sends_per_day": 20,
    "cooldown_after_loss_minutes": 30,
    "ticket_max_age_minutes": 30,
    "max_slippage_bps": 10,
    "risk_ladder": [
      {"drawdown_pct": 3.0, "scale": 0.5},
      {"drawdown_pct": 6.0, "scale": 0.25}
    ],
    "min_depth_multiple": 20
  }
}
```

| Field | Meaning |
| --- | --- |
| `mode` | `off` (nothing is auto-approved), `testnet`, or `mainnet`. The ticket's network must equal it. Promotion to mainnet is the user editing this one word, nothing else. |
| `account` | The main account the API wallet acts for. Tickets for any other account fail. |
| `originate` | `true`: the Strategist and the desk may propose their own trades. `false`: only tickets whose `origin` starts with `user` pass. |
| `cycle_interval_minutes` | How often the autonomous loop runs (`desk-autonomous-loop`). |
| `limits.*` | The user's limits. Each may only be tighter than the autonomy ceiling below. `risk-limits.md` still governs the Risk Manager's sizing; `autonomy.json` is what the gate enforces, and the two should agree. |
| `limits.risk_ladder` | Optional. A list of `{drawdown_pct, scale}` rungs, ascending by drawdown, scales in (0, 1]. The gate and the engine track the equity peak per network in `autonomy/equity-peak-<network>.json`; when drawdown from that peak reaches a rung, the per-trade risk budget at the gate and the engine's gross exposure are multiplied by the rung's scale. A multiplier only: it never enlarges a limit, and a malformed list invalidates the policy as a whole. The backtester applies the same rungs. |
| `limits.min_depth_multiple` | Optional, default 20. The engine defers an entry when resting depth within 10 bps on the entry side is below this multiple of the ticket's notional; the decision stays open and is retried for `limits.entry_retry_minutes` (default 30). Engine-side only; the gate does not read the book. |

### Autonomy ceilings

Tighter than the discretionary ceilings in `desk-risk-limits` section 0, because no human sees the ticket. A policy that sets any value looser is **invalid as a whole**: the gate refuses every ticket until the user fixes the file. Nothing on the desk may raise a ceiling.

| Ceiling | Value |
| --- | --- |
| max risk per trade | 1% of equity |
| max total open risk | 4% of equity |
| max leverage | 10x, and never above the exchange or tier max |
| max positions | 6 |
| daily loss stop | -5% of start-of-day equity |
| sends | 10 per hour, 60 per 24 hours |
| slippage tolerance at send | 50 bps |
| ticket age at gate | 30 minutes since the Risk PASS |

## 2. The ticket the gate reads

The Risk Manager's PASS produces the markdown ticket from `desk-trade-lifecycle` **and** a machine-readable copy at `proposals/<id>.ticket.json`. Every value comes from the same live reads the PASS cites; nothing is copied from an earlier brief.

```json
{
  "id": "HG-20260907-01",
  "network": "testnet",
  "account": "0xYourMainAccount",
  "market": "ETH",
  "side": "buy",
  "size": 0.4827,
  "entry": 3000.0,
  "tif": "Gtc",
  "reduce_only": false,
  "stop": 2900.0,
  "take_profit": null,
  "leverage": 3,
  "margin_mode": "cross",
  "notional_usd": 1448.1,
  "risk_usd": 51.0,
  "equity_usd": 10200.0,
  "stressed_distance": 105.65,
  "slippage_bps": 10,
  "risk_pass_at": "2026-09-07T14:12:00Z",
  "expires_at": "2026-09-07T14:42:00Z",
  "limits_version": "v3",
  "origin": "strategist:funding-mean-reversion"
}
```

- `kind` is optional: `entry` (default when `reduce_only` is false; the sender sets `leverage` and `margin_mode` on the account first if they differ), `close` (reduce-only, no `stop`, IOC at a slippage bound), `protect` (reduce-only with `stop`: a standalone stop for an existing position) or `cancel` (reduce-only, with an integer `oid` of a resting order to remove; the gate checks it is resting).
- `origin` is `user`, `user:<note>`, `strategist:<strategy name>` or `desk:discretionary`.
- `risk_usd` must equal `size x stressed_distance` within 2%; `notional_usd` must equal `size x entry`. The gate recomputes both.
- Adjustments, adds, closes and stops are tickets too, suffixed `-B`, `-C`, each with its own JSON file and its own gate run.

## 3. What the gate checks

```bash
python3 /workspace/hypergrok/scripts/policy_gate.py check --desk-root /workspace/trading-desk --ticket proposals/HG-20260907-01.ticket.json
```

It reads the policy, the ticket, `autonomy/HALT`, the send ledger, the events log, start-of-day equity, and **live** `clearinghouseState` and `frontendOpenOrders` for the policy account (or `--state` / `--orders` files in tests). Every gate is printed with its numbers:

`mode`, `network`, `account`, `halt`, `expiry`, `ticket-age`, `market`, `side`, `tif`, `notional-matches`, `min-notional`, `max-notional`, `leverage`, `slippage`, `stop-side`, `stress`, `risk-arithmetic`, `equity-fresh` (live equity within 5% of the ticket's), `risk-per-trade` (against the policy's limit multiplied by the risk ladder's scale in force; the detail reads `x ladder <scale> at <n>% drawdown from peak`), `protection` (every open position already has a resting reduce-only stop, or no new risk), `open-risk` (existing stop-to-entry risk plus this ticket), `positions`, `daily-loss`, `not-sent`, `rate-hour`, `rate-day`, `cooldown`, `origin`, for `close` and `protect` tickets `reduce-only-target` (a position in that market exists), and for `cancel` tickets `cancel-target` and `cancel-resting` (the oid is in `frontendOpenOrders`).

An `unavailable` read is exit code 2 with a reason, never a PASS. A failed gate is exit 1, with the failed names on the last line. A PASS is exit 0 and writes `proposals/<id>.approval.json`:

```json
{"id": "HG-20260907-01", "ticket_sha256": "...", "issued_at": "2026-09-07T14:15:00Z",
 "expires_at": "2026-09-07T14:25:00Z", "policy_mode": "testnet", "gates_passed": ["..."], "token": "hmac-sha256"}
```

The token is an HMAC over the ticket bytes and the expiry, keyed by `autonomy/gate.key` (created once, mode 600). The approval dies in ten minutes, dies if a single byte of the ticket changes, and is spent by one send.

## 4. What may send

Only `scripts/desk_send.py`, only with a valid approval:

```bash
python3 /workspace/hypergrok/scripts/desk_send.py --desk-root /workspace/trading-desk --ticket proposals/HG-20260907-01.ticket.json [--dry-run]
```

It re-verifies the approval, checks `HYPERLIQUID_NETWORK` and `HYPERLIQUID_ACCOUNT_ADDRESS` against the ticket, reads live `meta` and `allMids`, refuses if the mid has drifted past `slippage_bps` (or a stop is on the wrong side of the mark), rounds per `hyperliquid-orders`, writes its intent and cloids to `autonomy/sends.jsonl` **before** sending, sets `expiresAfter` one minute out, sends once, reconciles by cloid, and writes `proposals/<id>.execution.json`. Exit 3 is an unknown result: playbook A in `desk-incident-response`, and no resend.

In Claude Code the plugin's `hooks/guard.py` runs before every Bash, Edit and Write call and independently refuses a `desk_send.py` call without a valid approval, any raw `/exchange` request, any fund-moving action, and any write to the user's files. In Grok Bot the equivalent is the Require Approval rule scoped to everything that calls `/exchange` **except** the reviewed `desk_send.py` path (`desk-autonomous-loop` section 4).

## 5. Halting

```bash
python3 /workspace/hypergrok/scripts/kill_switch.py halt   --desk-root /workspace/trading-desk --reason "why" [--by who]
python3 /workspace/hypergrok/scripts/kill_switch.py status --desk-root /workspace/trading-desk
python3 /workspace/hypergrok/scripts/kill_switch.py resume --desk-root /workspace/trading-desk --by "Ove"
```

Any role may halt, and must when: an unknown send result cannot be resolved, a position cannot be protected, the daily loss stop is hit, account reads do not reconcile, the exchange has been unreachable longer than a cycle, or the policy file fails validation. While halted, `entry` tickets fail the `halt` gate; `close`, `protect` and `cancel` tickets still pass, so the desk can always get flat and tidy. Only the user resumes, from their own terminal; the guard denies the agent that command, and the script refuses `--by desk`. Every halt and resume is in `autonomy/events.jsonl`.

## 6. Ownership

| File | Written by | Read by |
| --- | --- | --- |
| `autonomy.json`, `risk-limits.md` | the user | everyone |
| `autonomy/gate.key` | `policy_gate.py`, once | `policy_gate.py` |
| `proposals/<id>.ticket.json` | Risk Manager | gate, sender |
| `proposals/<id>.approval.json`, `.execution.json` | the scripts | everyone |
| `autonomy/sends.jsonl`, `events.jsonl`, `day-*.json` | the scripts | everyone |
| `autonomy/HALT` | `kill_switch.py` | gate, loop |
| `autonomy/equity-peak-<network>.json` | `policy_gate.py` and the engine, raised only, never lowered | gate, engine, dashboard |
| `autonomy/fees.json` | `desk_send.py`, from `userFees` | engine, `execution_stats.py` |

## 7. What this does and does not protect against

The gate is arithmetic, not a judge of ideas. It guarantees that nothing is sent outside the user's written limits, on the wrong network, into an unprotected book, past the loss stop, faster than the rate cap, twice for one ticket, or after the ticket went stale. It does not make a bad strategy good, and it cannot stop an agent that has shell access from doing something outside the scripts; the trade-only API wallet, the guard, the ceilings and the testnet-first rule are what bound that. Say this plainly when the user asks what "autonomous" means here.

## Never

- Never write, patch, regenerate or "temporarily relax" `autonomy.json`, `risk-limits.md`, the equity peak file or the gate key; a ladder rung is the user's to change, and lowering the recorded peak to escape one is the same as relaxing the policy.
- Never edit a ticket after a FAIL to make it pass. A new idea is a new ticket with fresh evidence.
- Never send through anything but `desk_send.py`, and never call it twice for one id.
- Never resume a halt. Report it and wait.
- Never describe the gate as a guarantee of profit or safety; describe exactly what it checks.
