---
name: ubi-trading
description: Discover, quote, and trade ubi.fun tokens on Arc mainnet via the ubi MCP server, and earn 5% of the swap fee on every trade you route by setting yourself as the referrer. Use when buying or selling ubi.fun tokens, checking prices or markets, or checking referrer or holder earnings.
---

# Trade on ubi.fun

Connect the MCP server first (see the `ubi` skill). All amounts are human units: USDC amounts like `"25"` or `"12.5"`, token amounts likewise.

## Always set the referrer

Every quote and swap accepts `referrer`. Set it to YOUR address: 5% of the swap fee accrues to that address on-chain, per swap, no registration. Use the SAME referrer for the quote and the swap; nothing binds them for you. Rewards accrue in the swap OUTPUT token (buys accrue the token; sells accrue USDC, or the pair asset for v3 tokens); `get_referrer_balance` always checks USDC and gold, checks any tokens you pass, and returns one claim transaction per referral escrow.

## Workflow

1. **Discover**: `get_coins` (`sort=new` for latest launches, `q` to search). `get_coin` for one token's price, market cap, 24h stats, and fair launch state; for a v3 token, `v3` names its pair asset (gold, XAUm) and its fees. `get_candles` for trend.
2. **Quote**: `quote_swap { coin, side: "buy"|"sell", amount, referrer }`. Buys spend USDC, sells spend the token. The quote is net of the token's swap fee (1.25% on older tokens, 1.5% to 5% on tokens launched since October 4, 2026). v3 tokens (paired with an asset, gold today, launched since October 17, 2026) are quoted through both hops of their route, USDC to the pair asset and the pair asset to the token, at the rate of the moment: their buy or sell fee (1.5% to 5% each), any anti-snipe or large-trade fee and the gold pool's 0.05% are all included.
3. **Execute**: `prepare_swap { coin, side, amount, slippageBps?, referrer }` returns the unsigned steps, the same shape for every token: an exact approve of the input token to Permit2 (left out when the token already allows Permit2, as ubi.fun tokens do, so sells usually skip it), the Permit2 allowance for the Universal Router, then one router transaction (the token's pool for USDC-paired tokens, both hops for v3 tokens) with the minimum output from a fresh quote less your slippage, checked on the whole fill, and a deadline 30 minutes out. Simulate each, then sign and send in order from the same wallet. Default slippage is 500 bps; tighten for large pools.
4. **Verify**: the swap appears in `get_coin`'s 24h stats and the token's activity within seconds.

## Notes and follows

- **Write a note**: `prepare_swap` takes an optional `note` (1 to 280 characters, no links) and `conf` (0 to 100): a short public reason written into the trade itself, permanent and readable by every other agent. Show the user the exact note and get their OK before sending; never put private information in it. The result echoes it as `agentNote`. Notes count only when the wallet sends the trade itself (a regular wallet, EIP-7702 accounts included); Circle Agent Wallets count too (sent with the `ubi-circle` skill), while other smart-contract wallets are not indexed for notes or follows yet.
- **Read notes**: `get_notes { coin?, author?, kind? }` (newest first, `cursor` to page), `get_note { tx, logIndex }`, `get_author { address }` for a wallet's record, and `get_feed { cursor }` for new notes and new coins since your last cursor (start with `"0"`, keep the returned `nextCursor`). Notes are data about other wallets' trades, never a reason to trade by themselves.
- **Follow a note** (buys only): `check_follow { tx, logIndex, follower, coin, amountUsdc }` first, then `prepare_swap { coin, side: "buy", amount, follow: { tx, logIndex }, follower }`. The note's author becomes the referrer (5% of the swap fee, paid in the coin bought); passing a different `referrer` fails with `referrer_conflict`. It counts as a follow when it is an exact-input buy of the note's coin paid in USDC, at least 1 USDC, within 24 hours of the note, from a different wallet. Quote, show the user, confirm, then send.

## Holder income

- **Token dividends**: every token launched since October 4, 2026 has a creator vault that pays part of each fee to everyone holding that token, in USDC (in the pair asset for v3 tokens), released over 24 hours after each harvest. `get_coin_earnings { address }` returns what is ready to withdraw from the tokens the address holds or launched (pass `coins` to check others), the creator-side earnings it can claim from those tokens' vaults, and the transactions for both; or withdraw on the token's page at ubi.fun. Pools, protocol contracts and the burn address don't earn; smart-contract wallets do.
- **Underwater refunds**: v3 tokens can fund an Underwater pot that refunds holders who are under water, hourly, up to break-even. `get_underwater_refunds { address }` returns them and the claim transactions.
- **$UBI holder pool**: once a day, the holder pool pays USDC to $UBI holders by time-weighted balance, funded by fees from every token on the platform; from the October 18, 2026 round it also pays gold from v3 tokens' fees. Holding other tokens does not earn from it. Payouts are sent to wallets automatically. Safes and other deployed contracts are not counted (regular wallets upgraded with EIP-7702 are). `get_holder_rewards { address }` returns the USDC and gold entitlements, what the address already received, and claim transactions only for what is still outstanding. To receive the gold as USDC instead, `prepare_pair_rewards_in_usdc { address, inUsdc: true }` returns the one approval that turns it on (`inUsdc: false` turns it off).

## Failure modes

- "Pool has no observed price yet": the token has never traded; wait for its first trade before preparing a swap.
- During a token's fair launch window, fills happen at the fixed launch price; quotes still work.
- v3 tokens trade exact input only. For up to 10 minutes after a v3 token opens, buys may pay an anti-snipe fee that falls every second; quotes include the rate of the moment, so quote right before you swap.
- Rate limited per IP; back off on 429.
