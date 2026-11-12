---
name: telegram-ton
description: TON blockchain where it meets Telegram — TON Connect wallets in Mini Apps, wallet login with ton_proof, accepting and verifying TON or jetton payments, jettons and NFTs, token-gated access, reading the chain through the TON Center API, and Tolk contracts built with Acton. Use this skill whenever the user mentions TON, Toncoin, Gram, TON Connect, a wallet, jettons, NFTs, a .tolk file, Acton, a smart contract, deposits or withdrawals in crypto, or checking a TON address or transaction, even inside a Telegram bot or Mini App. Read the Stars rule first, because digital goods sold inside Telegram can't be paid in crypto.
---

# TON for Telegram products

Naming: Toncoin is also called **Gram**. The smallest unit is 10^-9; keep amounts as integers
(BigInt, Python `int`, or strings), never floats.

## First: is TON even allowed here?

Telegram requires **Stars** for **digital goods and services** sold inside bots and Mini Apps
and does not allow crypto for them (App Store and Play Store rules). An app that ignores this
may stop being shown to mobile users. So before building any TON checkout, ask what is sold:

- In-app items, access, boosts, content, subscriptions → Stars (`telegram-payments`). Do not
  build a TON or jetton checkout for these, and say so to the user up front.
- Physical goods, payouts to users, deposits and withdrawals of on-chain assets, wallet login,
  owning an NFT or token the user can take elsewhere → TON fits.
- Borderline → point to Section 6.2 of the Telegram Bot Platform Developer Terms; don't decide
  for the user. Record the decision in `PRODUCT.md`.

## Pick the job, then read one reference

| Job | Read |
|---|---|
| Connect a wallet in a Mini App, sign a transaction | `references/tonconnect-troubleshooting.md` |
| Log in with a wallet / bind a wallet to a Telegram user | `references/ton-proof-auth.md` |
| Accept TON or jettons, deposits, payouts | `references/ton-payments.md` |
| Launch or integrate a jetton or NFT collection, token-gating | `references/jettons-nft.md` |
| Check balances, transactions, why something failed | `references/chain-reading.md` |
| Write or change a Tolk contract | `references/contracts.md`, then `tolk-essentials.md` |
| Tests for a contract | `references/testing-recipes.md` (or the `tolk-test-writer` agent) |
| Before any release | `references/security-checklist.md` |
| Acton commands and flags | `references/acton-cheatsheet.md` |

## Rules that are easy to get wrong

**Wallet login.** A wallet address sent by the client proves nothing. Verify `ton_proof` on the
backend: one-time nonce from your server, domain, timestamp, the **network** (the signature
doesn't fix it), public key taken from `walletStateInit`, and that it matches the address.

**TON Connect transactions.** Set `validUntil` (a few minutes), an explicit `network` (`-239`
mainnet, `-3` testnet), a user-friendly address and `amount` as a string of nano units. Use
`messages`, not the alpha `items`. The returned BOC is for showing progress only.

**Accepting payments.** The order exists on the server before payment. Credit only from the
incoming transaction on your address, found by polling or a stream, never from a browser
"paid" signal. Never fulfil on `pending`; wait for `finalized` before anything valuable or
irreversible. The Streaming API doesn't replay missed events, so after a restart catch up through
API v3 from a stored checkpoint.

**Jettons.** Keep an allowlist of trusted masters. Derive your jetton wallet with
`get_wallet_address` on the master and accept `transfer_notification` (`0x7362d09c`) only from
that wallet. Names, symbols and images prove nothing. When you send jettons, set
`forward_ton_amount` to at least 1 nano unit, or the recipient gets no notification.

**Tolk (v1.5).** `ton("0.05")` is deprecated, write `grams("0.05")`. Outgoing messages take
`bounce: BounceMode.NoBounce | Only256BitsOfBody | RichBounce`; bounces arrive in
`onBouncedMessage`, never in `onInternalMessage`. Chat answers and older examples often show the
old syntax; check `references/tolk-essentials.md`.

**Acton.** Doesn't run on native Windows; use WSL (Ubuntu 22.04+). There is no `acton deploy`;
deployment is a script. `acton verify` targets testnet only; mainnet verification is the user's
job at verifier.ton.org.

## Safety

- Default to **testnet**. Claude never sends transactions: this plugin's hook blocks
  `acton script --net`, `acton wallet airdrop`, `acton verify` and mainnet commands. Give the user
  the exact command to run in their own terminal, then check the result on chain.
- Never ask for, print, log or commit a seed phrase or private key. Reading the chain needs only
  an address. Anything that moves funds is signed by the user in their own wallet.
- Before mainnet run the `ton-security-reviewer` agent and recommend a human audit for anything
  that holds value.

## Deep contract work

This plugin covers contracts at the level a Telegram product needs. For deep Tolk or FunC work,
migrations and the full Acton surface, the official skills in
https://github.com/ton-blockchain/skills (`acton`, `tolk`, `func2tolk`, `ton-blockchain`) go
further; prefer them for their area if the user has them installed.
