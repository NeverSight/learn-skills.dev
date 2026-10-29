---
name: suan-launchpad
description: Trade tokens launched on SUAN Agent Launchpad, the .ai Agent ID launch protocol on BNB Chain (PancakeSwap Infinity hook pool). Use when the user wants to check, quote, buy or sell a SUAN Agent Launchpad token, see its stage (.ai window, hold-cap window, tax period), time windows or fees, or check a SUAN Agent Launchpad trade. Builds the transaction and executes it with the Binance Agentic Wallet (`baw contract-call`, Developer Mode).
---

# SUAN Agent Launchpad

Each SUAN Agent Launchpad token trades in one locked PancakeSwap Infinity hooked pool from its first block: the whole 1B
supply sits in a single position from the launch price (market cap 4.2 BNB) upward. During the first minutes only
wallets holding a **.ai Agent ID** can buy, and .ai wallets pay a lower tax than everyone else.

`scripts/suan-launchpad.mjs` is a self-contained, read-only CLI (Node ≥ 22, no dependencies). It reads the chain,
simulates the exact trade, and prints the transaction. It never signs or sends anything: the wallet does that with
`baw contract-call preview` → `baw contract-call execute`.

```bash
node scripts/suan-launchpad.mjs <command> '<json_params>'
```

Every command prints `{"success": true, "data": …}` or `{"success": false, "error": {"code", "message", …}}`.

## Configuration

| Setting | Param | Env var | Default |
|---|---|---|---|
| Hook (launch registry and pool hook) | `hook` | `SUAN_LAUNCHPAD_HOOK` | mainnet `0xa8E32E5Bc1d3Ce8aFe6bf3ef2069F1Fc7171c061` |
| Router (buy / sell entry point) | `router` | `SUAN_LAUNCHPAD_ROUTER` | mainnet `0x119dCa55DCbB37998E9bA0845196acc0FFf2FAc2` |
| BSC RPC | `rpc` | `BSC_RPC_URL` | public `bsc-dataseed` endpoints |

The defaults are the SUAN Agent Launchpad on BSC mainnet, as published on https://launch.suan.bid. Only override
them when the user explicitly gives other addresses; never guess them. A token that does not answer through the hook fails with `UNKNOWN_LAUNCH`.

## Time windows

Everything that changes is measured from the launch time, in chain time (the latest block's timestamp). `info` shows
the current `stage` and the end of each window under `windows`:

| Stage | Until | Who can buy | Who can sell | Rules |
|---|---|---|---|---|
| `ai-only` | `aiOnlyUntil` (2 min default, 2–30 min) | .ai Agent ID wallets | .ai wallets and the creator | Tokens only move between the pool and .ai wallets; 1% cap |
| `hold-cap` | `holdCapUntil` (1 h default, at most 24 h) | anyone | anyone | No address may hold more than **1% of the supply** (10,000,000 tokens) |
| `taxed` | `taxPeriodEndsAt` (15 days default, 15–365 days, or `"permanent"`) | anyone | anyone | The token refuses other pools |
| `open` | — | anyone | anyone | Everyone pays the .ai rate; other pools are allowed |

- The 1% cap applies during the .ai window too. At the launch price 1% is only about 0.04 BNB of buying; selling frees
  room again. `holdRoom` in `info` shows what this wallet can still take.
- During the tax period the token refuses PancakeSwap and Uniswap V2/V3 pools, Uniswap v4, LikwidVault and any other
  Infinity pool, so trading stays in the hooked pool. A launch can make the tax period permanent (`"permanent"`); the
  token then only ever trades in its own pool. Aggregators and the PancakeSwap Universal Router work once the hold-cap
  window is over, as long as the route goes through the hooked pool.
- The anti-sniper surcharge applies in the first 5 blocks after creation (`antiSniperNow`). Buys in the creation block
  itself are blocked.

## Fees

All fees are taken in BNB.

| Fee | Rate | Goes to |
|---|---|---|
| Trading fee (`baseFee`) | 1% on every trade | 0.5% buys back and burns $SUAN (the platform's share, from the first trade) + 0.5% creator, or holders once the creator switched its share to holders (`creatorShareToHolders: true`, one-way) |
| Tax | Everyone: the .ai rate (0–7%, default 0) | Split by the launch weights: founder, holder rewards, buyback-and-burn of the token, platform treasury |
| Surcharge | Wallets without .ai, during the tax period only: +3 points (`taxes.buyNow` / `taxes.sellNow` include it) | All to buyback-and-burn; no one receives it |
| Anti-sniper | four.meme's ladder in the first 5 blocks, buys only | Buyback-and-burn |

Platform fees: 100% buy back and burn $SUAN. That is the 0.5% platform share of every trade plus the one-time 0.005 BNB
launch fee. PancakeSwap's own protocol fee (`pancakeProtocolFee`) is on top and is already included in the quote.

## Commands

| Command | Params | What it does |
|---|---|---|
| `info` | `token`, `wallet?` | Stage, time windows, fees, creator-share switch, hold-cap room, and whether this wallet can buy / sell |
| `quote-buy` | `token`, `wallet`, `amount` (BNB), `slippageBps?` | Simulates the buy and builds the router call |
| `quote-sell` | `token`, `wallet`, `tokenAmount`, `slippageBps?` | Simulates the sell and builds the router call, plus an `approve` first when the router's allowance is too low |
| `receipt` | `txHash`, `token?` | Status, trades (`Swapped`: BNB paid or received, tokens), fees taken (`FeeTaken`), token transfers and `CreatorShareToHolders` events of a submitted transaction |

Amounts are decimal strings (`"0.05"`), not wei. `slippageBps` defaults to 1000 (10%) and sets `minReceive`.

Quotes are not estimates from a formula: the CLI runs the real router call with `eth_call` from the user's wallet, so
the hook and token apply the same .ai check, hold cap and fees as the real trade. Buys pass no price limit. For sells it adds a
temporary allowance in the simulation only, so a quote works before the approval exists.

## Workflow

### Prerequisites

1. The user has a Binance Agentic Wallet with **Developer Mode** on, since `contract-call` needs it. Developer Mode has
   its own daily limit and balance cap, which the user sets in the Binance App.
2. To buy during the .ai window, and for the lower .ai tax at any time, the wallet holds a .ai Agent ID. Check
   `data.wallet.hasAgentId` from `info`. If it is `false`, the user claims one through the Binance Agentic Wallet
   skill's Agent ID flow first. It is free, one per user, and non-transferable.

### Buy

1. `info {token, wallet}`. Show the stage and when it ends, the fees this wallet pays (`data.wallet.fees`) and,
   during the .ai and hold-cap windows, `holdRoom`. Stop if `canBuy` is `false` and explain why (no .ai Agent ID
   during the .ai window: claim one, or wait until `windows.aiOnlyUntil`).
2. `quote-buy {token, wallet, amount}`. Show `estimate.receive`, `estimate.minReceive` and `estimate.fees`.
3. Run `transactions[0].baw` (that is, `baw contract-call preview --binanceChainId 56 --from <wallet> --to <router>
   --value <wei> --inputData <hex> --json`). Show the user the preview's balance changes and any `risks`.
4. Only after the user confirms, run `baw contract-call execute --requestId <requestId> --json`. If the preview has
   `requireConfirmation: true`, tell the user to approve the order in the Binance App.
5. `receipt {txHash, token}` to report the fees paid and tokens received.

### Sell

1. `quote-sell {token, wallet, tokenAmount}`. If `transactions` starts with `approve`, preview and execute it first,
   then run `quote-sell` again so the sell is built from fresh state.
2. Preview and execute the `sell` transaction as in the buy flow.

## Safety

- Never call `execute` without showing the preview and getting the user's confirmation for that trade.
- Never execute an intercepted preview. A preview that fails with `351803` (`AGENT_DEV_MODE_RISK_BLOCKED`) has no
  `requestId`; tell the user the wallet's risk engine blocked it and stop.
- Re-quote if more than a minute has passed or the user changes the amount. During the first blocks the anti-sniper
  fee falls every block, so an older quote only underestimates the output.
- Do not raise `slippageBps` above 1000 unless the user asks for it.
- The contracts are unaudited; say so when the user asks about safety.

## Errors

| Code | Meaning | What to tell the user |
|---|---|---|
| `NO_AGENT_ID` | The .ai window is running and the wallet has no .ai Agent ID (sells: and is not the creator) | Claim a .ai Agent ID first, or wait until `windows.aiOnlyUntil` |
| `HOLDING_CAP_REACHED` | The buy would take the wallet over 1% of supply during the hold-cap window | Buy less; `holdRoom` shows the room left, and the cap ends at `windows.holdCapUntil` |
| `ANTI_SNIPER_BLOCK` | Buys in the creation block cost 100% or more | Retry from the next block |
| `SLIPPAGE` | The price moved past `minReceive` | Re-quote |
| `INSUFFICIENT_BNB` / `INSUFFICIENT_TOKEN_BALANCE` | Not enough funds | Show the balance from `info` |
| `INSUFFICIENT_ALLOWANCE` | The router is not approved | Run the `approve` transaction from `quote-sell` |
| `TRANSFER_LOCKED` / `ALT_POOL_BLOCKED` | The token only moves through its own pool right now (.ai window / tax period) | Trade through this skill's router call |
| `PRESALE_CAP` | The creator presale asks for more than 3% of supply (`maxTokens`) | Launch with a smaller presale |
| `NOT_CREATOR` / `BUYBACK_TOO_EARLY` | Creator-only call, or a buyback before the .ai window ended | Not something a trade can fix |
| `INVALID_AI_ONLY` / `INVALID_HOLD_CAP` / `INVALID_TAX_PERIOD` | Launch parameters out of range (2–30 min; ≥ .ai window and ≤ 24 h; 15–365 days or permanent) | Fix the launch parameters |
| `UNKNOWN_LAUNCH` / `BAD_HOOK` | Not a SUAN Agent Launchpad token, or wrong hook address | Check the addresses |
| `RPC_UNAVAILABLE` | No RPC answered | Retry, or pass `rpc` |

`references/contracts.md` lists the contract interface, selectors, events and fee rules.
