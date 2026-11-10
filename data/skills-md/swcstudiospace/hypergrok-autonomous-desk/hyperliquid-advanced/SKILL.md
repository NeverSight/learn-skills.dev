---
name: hyperliquid-advanced
description: Less common Hyperliquid actions and their rules - dead-man's switch (scheduleCancel), TWAP orders, spot orders, expiresAfter and nonces, API wallet approval from code, sub-account and vault addressing, HIP-3 dexs, and what the desk deliberately does not do (transfers, withdrawals, builder fees, staking). Write actions are Execution Trader only, through scripts/desk_send.py on a gate-approved ticket. Use when a ticket asks for one of these or when a user asks whether the desk can.
license: MIT
metadata:
  version: "1.2.0"
  author: Galleon Labs
  category: hyperliquid
  network-default: testnet
---

# Hyperliquid advanced actions

Uses the same header as `hyperliquid-orders` (`info`, `exchange`, `ACCOUNT`, `round_px`, `round_sz`, `new_cloid`). Everything that signs is Execution Trader only, through `scripts/desk_send.py` on a ticket with a Risk PASS and a policy-gate approval; the snippets are reference and testnet rehearsal material, and the desk's live sends go through `desk_send.py`.

## Dead-man's switch (`scheduleCancel`)

Tells the exchange to cancel **all** of the account's open orders at a future time unless you push the time out or clear it. Useful when the desk runs a watch that could die while resting orders sit on the book. The user asks for it explicitly; the report states the time.

```python
from hyperliquid.utils.signing import get_timestamp_ms
res = exchange.schedule_cancel(get_timestamp_ms() + 10 * 60 * 1000)   # 10 minutes out; must be >= 5 s in the future
res = exchange.schedule_cancel(None)                                    # clear it
```

TypeScript: `await exchange.scheduleCancel({ time: Date.now() + 600_000 })`; omit `time` to clear. Limits: at most 10 triggers per day per account (resets 00:00 UTC).

**It cancels protective stops too, and it is not position-aware.** If it fires while a position is open, that position is left naked on the exchange and nothing re-arms it automatically. So: it is for a desk with resting orders and no position, or for a user who has explicitly accepted that outcome for this account. Do not arm it as routine hygiene while a position is open. If it does fire with a position open, that is an unprotected position the moment it lands - declare it and run playbook D in `desk-incident-response` at priority, rather than treating re-arming as clean-up.

## TWAP

Splits a size into slices at fixed intervals (30 seconds minimum) over `m` minutes: 5 minutes to 7 days per the docs, though the TypeScript SDK's schema caps `m` at 1440 (24 hours), so longer runs need the raw action. Minimum 100 USD total; each slice capped at 3% slippage; `t: true` randomises slice sizes by up to 20%. Not in the Python SDK's high-level `Exchange`; use TypeScript or the raw action.

```ts
const twap = await exchange.twapOrder({ twap: { a, b: true, s: "10", r: false, m: 30, t: true } });
const twapId = (twap.response.data.status as { running: { twapId: number } }).running.twapId;
await exchange.twapCancel({ a, t: twapId });
```

Raw action: `{"type":"twapOrder","twap":{"a":1,"b":true,"s":"10","r":false,"m":30,"t":true}}`; response `{"status":{"running":{"twapId":N}}}` or `{"status":{"error":"..."}}`. Monitor with the `twapStates` / `userTwapSliceFills` WebSocket subscriptions or `userTwapSliceFills` reads; TWAP fills carry a zero hash. A TWAP is still one ticket; the ticket states size, minutes, randomisation and reduce-only.

## Spot orders

Same `order` action; asset id is `10000 + index` of the pair in `spotMeta.universe`; size decimals are the **base token's** `szDecimals`; price gets `8 - szDecimals` decimals (still 5 significant figures); minimum order value is 10 quote tokens. The Python SDK resolves `"PURR/USDC"` (and app-style aliases such as `"HYPE/USDC"` where unambiguous) to the spot asset id for you:

```python
# header from hyperliquid-orders, then spot-specific rounding from spotMeta
pair_name = "PURR/USDC"
spot = info.spot_meta()
pair = next(p for p in spot["universe"] if p["name"] == pair_name)
base_dec = next(t for t in spot["tokens"] if t["index"] == pair["tokens"][0])["szDecimals"]

def round_px_spot(px):
    px = float(f"{float(px):.5g}")
    return float(Decimal(str(px)).quantize(Decimal(1).scaleb(-(8 - base_dec)), rounding=ROUND_HALF_UP))

def round_sz_spot(sz):
    return float(Decimal(str(sz)).quantize(Decimal(1).scaleb(-base_dec), rounding=ROUND_DOWN))

sz, px = round_sz_spot(120), round_px_spot(0.1234)
assert sz * px >= 10, "below the 10 quote-token minimum"
res = exchange.order(pair_name, True, sz, px, {"limit": {"tif": "Gtc"}}, cloid=new_cloid())
```

Read balances with `spotClearinghouseState` (`hyperliquid-account`). Spot has no leverage and no liquidation. Under `unifiedAccount`/`portfolioMargin` abstraction modes balances behave differently; the desk stays in the default mode unless the user changes it in the app.

## expiresAfter and nonces

- Every signed action carries a `nonce` (unix ms). The SDKs manage it. Nonces are per **signer**, so two processes signing with the same API wallet at the same time will collide; the desk keeps one Execution Trader and one process at a time.
- `expiresAfter` (ms) makes an action void if it reaches the exchange after that time. Useful protection against a delayed duplicate after a reconnect: `exchange.set_expires_after(get_timestamp_ms() + 60_000)` in Python (applies to following L1 actions; must be `None` for user-signed actions), or per-call `{ expiresAfter }` in TypeScript. A stale rejection costs 5x rate-limit weight, so keep it generous (a minute) rather than tight.
- `noop` is an action that just burns a nonce; documented as a way to invalidate in-flight actions signed with lower nonces.

## Approving an API wallet from code

The desk's normal path is the app (`hyperliquid-setup` section 4), because approval must be signed by the **main** wallet and that key never touches the desk computer. For completeness: `Exchange(main_wallet).approve_agent(name)` in Python generates a fresh agent key and returns `(result, agent_private_key)`; TypeScript `exchange.approveAgent({ agentAddress, agentName })` approves an address you generated. Named agents can carry an expiry via `"name valid_until <ms>"` (up to 180 days); an account may hold 1 unnamed and up to 3 named agents, plus 2 named per sub-account; re-approving the same name (or a new unnamed agent) replaces the previous key. Never reuse a revoked agent address.

## Sub-accounts and vaults

Orders can be sent **for** a sub-account or vault by setting `vaultAddress` (Python: `Exchange(..., vault_address="0x...")`; TypeScript: `defaultVaultAddress` or per-call `{ vaultAddress }`); the API wallet of the master signs. Reads for that address use the sub-account/vault address as `user`. The desk supports this only if the user asks and records it in `desk.md`; it never creates sub-accounts or transfers funds into or out of them.

## HIP-3 builder dexs

Other perp dexs exist beside the main one (`perpDexs`). Coins are `dex:COIN`, asset ids are `100000 + 10000 x dex index + index in that dex's meta`, margin is often isolated-only, and reads take a `dex` parameter. Off by default on the desk; if the user wants one, everything above applies with the prefixed coin name and the dex's own `meta`.

## Rate limits and `reserveRequestWeight`

Address-based limits for actions: a buffer of 10,000 plus 1 per 1 USDC of cumulative volume; when exhausted, 1 action per 10 seconds (cancels get extra headroom). Check `userRateLimit`. An account can buy more with `reserveRequestWeight` (0.0005 USDC each) - the desk does not do this automatically; mention it if the user hits the limit. Per-IP `/exchange` weight is `1 + floor(batch size / 40)`.

## Deliberately not on this desk

These exist in the API and SDKs; the desk does not use them, and the user does them in the Hyperliquid app with their main wallet:

| Action | What it does |
| --- | --- |
| `usdSend`, `spotSend`, `sendAsset` | send USDC or tokens to another address or between dexs (`agentSendAsset`, the self-only variant, is L1-signed and agent-capable) |
| `withdraw3` | withdraw USDC to Arbitrum |
| `usdClassTransfer` | move USDC between perp and spot balances |
| `vaultTransfer`, `subAccountTransfer`, `createSubAccount` | move funds into or out of vaults and sub-accounts (L1-signed, so an API wallet technically can; the desk's rule is the guard) |
| `approveBuilderFee`, `builder` on orders | let a builder charge a fee on your orders |
| `cDeposit`, `cWithdraw`, `tokenDelegate` | HYPE staking |
| `userSetAbstraction` and friends | change the account's margin mode |

If a ticket asks for one of these, the Execution Trader declines and the Desk Lead explains why (`desk-operating-model`, "Excluded on purpose").

## Pitfalls

- A dead-man's switch that fires also removes stops. Re-arm protection.
- TWAP minimum size and duration errors (`Invalid TWAP duration`) come back inside `status`, not as `resting`.
- Spot size decimals come from the base token, not the pair; ids differ per network.
- Reusing an agent address after revocation can replay old signed actions; generate fresh keys.
- Two signers on one API wallet in parallel: nonce collisions and rejected actions.
