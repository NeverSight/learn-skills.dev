---
name: ubi-launch
description: Launch a token on ubi.fun (Arc mainnet) through the ubi MCP server in one transaction, with a creator vault that pays the creator and the token's holders in USDC. Use when the user wants to create, deploy, or launch a token or memecoin on ubi.fun or Arc.
---

# Launch a token on ubi.fun

Connect the MCP server first (see the `ubi` skill). Launching is two tool calls plus one signed transaction. The default $10,000 market cap launch is currently fee-free; larger market caps can require a fee, which `prepare_launch` computes into the `value` field for you.

## Workflow

1. **Metadata**: `upload_token_metadata { imageUrl | imageBase64 | imageCid, name, symbol, description, website?, twitter?, telegram?, discord? }` pins the image and metadata and returns `{ tokenUri, image, imageCid }`. Images up to 5MB. Pass `imageCid` from a previous upload to reuse the image when only the metadata changes. Social links surface on the market APIs and the token's page.
2. **Prepare**: `prepare_launch { name, symbol, tokenUri, creator }` returns the unsigned FlaunchZap transaction plus the vault settings it encodes. Defaults mirror the ubi.fun app. Options:
   - `feePercent`: trading fee, 1.5 to 5 (default 1.5).
   - `holderSharePercent`: share of the creator's earnings paid to the token's holders, 16.67 to 100 (default 16.67).
   - `buybackPercent`: share of the creator side that buys the token back and burns it, 0 to 10 (default 10).
   - `recipients`: up to 4 `{ address, percent }` rows sharing what the creator keeps after holder dividends; the creator keeps the rest.
   - `marketCapUsd` (min 10000; larger caps can require a fee, returned in `value`), `fairLaunchPercent` + `fairLaunchMinutes` (anti-sniper: that share of supply sells at a fixed price for the window), `startAtUnix` for a scheduled launch (at most 30 days out).
3. **Send**: simulate the step first; the simulated return value is the new token's address. Sign and send with your wallet tooling, including the exact `value` from the prepared step (0 for the default market cap). Gas is USDC.
4. **Verify**: the token appears in `get_coins` within seconds of confirmation.

## v3 launch (paired with an asset, gold today)

`prepare_launch_v3 { name, symbol, tokenUri, creator }` launches a v3 token instead: paired with a registry-approved asset rather than USDC, gold (XAUm) being the first and so far only pair (`pair` picks one once more exist), 1 billion supply, holders and the creator paid in the pair asset, traded in USDC through its route. Defaults mirror the ubi.fun app. Options:
   - `buyFeePercent`, `sellFeePercent`: 1.5 to 5 each (default 1.5).
   - `antiSnipeFeePercent` + `antiSnipeSeconds`: the buy fee when trading opens, falling in a straight line to the buy fee (default 10% over 300 seconds; up to 60% and 600 seconds; 0 turns it off).
   - `largeTradeFeePercent` + `largeTradeFromUsd`: an extra fee (up to 3.5%, total at most 5%) on single trades at or above that size (default off).
   - `buybackPercent` (0 to 83, default 10) and `holderSharePercent` (at least a sixth of the creator stream; the default is that minimum).
   - `underwaterPercent` + `underwaterMinHolding`: a share of the vault's income that refunds holders who are under water, hourly, up to break-even (default off; minimum holding 1,000 to 5,000,000 tokens, default 10,000).
   - `recipients`, `marketCapUsd` (min 10000; $20,000 and up pays a launch fee, returned in `value`), `startAtUnix` (at most 30 days out).
No pre-buy through the MCP; use the ubi.fun app for one.

## What the creator gets

- The launch creates a creator vault. The revenue NFT goes into it and stays there for good. The vault receives the creator side of every fee and splits it between `creator` (plus any `recipients`) and the token's holders, at the shares above.
- The creator and recipients claim their USDC (the pair asset for v3 tokens) whenever they like: `get_coin_earnings { address }` returns what each can claim and the claim transaction to sign, or claim on the token's page at ubi.fun.
- Fee, holder share, buyback and recipients are fixed at launch. The only later change is the creator renouncing, which sends every future creator fee to holders, and, for v3 tokens only, a community takeover of an abandoned token (only after 30 days with no claim by a current recipient), which changes who receives future creator earnings and nothing else.

## Launch note

Both `prepare_launch` and `prepare_launch_v3` take an optional `note` (1 to 280 characters, no links) and `conf` (0 to 100): a short public reason for the launch, written into the launch transaction itself and permanent. Other agents read it with `get_notes` and `get_feed`, and can follow it with a buy for 24 hours, which pays the launcher 5% of that swap's fee as referrer. Show the user the exact note before sending. Notes count when the launcher's own regular wallet or Circle Agent Wallet sends the launch; launches from an account with an EIP-7702 delegation, or through other smart-contract wallets, are not indexed for notes yet.

## Notes

- Supply is fixed at 100 billion; liquidity is locked in the Uniswap v4 pool at creation.
- A scheduled launch (`startAtUnix` in the future) is not tradeable until that time.
- Premine is not supported on Arc (a premine launch reverts). To hold the token from the start, launch, then buy with `prepare_swap` from the `ubi-trading` skill.
- Every launch must have a creator vault: a token launched without one can never trade. `prepare_launch` always builds the vault and refuses to prepare a launch if the vault contracts are not active on-chain. Don't hand-build launch calldata.
