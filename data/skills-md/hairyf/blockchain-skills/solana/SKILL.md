---
name: solana
description: Solana blockchain development — core concepts, clients, RPC, tokens, and payments for agent-driven tooling.
metadata:
  author: hairy
  version: "2026.2.9"
  source: Generated from https://github.com/solana-foundation/solana-com, scripts located at https://github.com/antfu/skills
---

> Skill is based on Solana documentation (solana-com), generated 2026-02-09.

Concise reference for building on Solana: accounts, transactions, programs, PDAs, CPI, fees, JavaScript/Rust clients, frontend, SPL tokens, RPC, payments, and terminology.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Accounts | Account model, address, keypair, PDA | [core-accounts](references/core-accounts.md) |
| Transactions & Instructions | Tx format, signatures, message, build & send | [core-transactions-instructions](references/core-transactions-instructions.md) |
| Versioned Transactions | v0 message, lookup tables, maxSupportedTransactionVersion | [core-versioned-transactions](references/core-versioned-transactions.md) |
| Programs & PDA | Programs, PDA derivation, canonical bump | [core-programs-pda](references/core-programs-pda.md) |
| CPI & Fees | Cross-program invocation, base/priority fees, CU | [core-cpi-fees](references/core-cpi-fees.md) |
| Rent | Rent exemption, getMinimumBalanceForRentExemption, reclaim on close | [core-rent](references/core-rent.md) |

## Clients & Frontend

| Topic | Description | Reference |
|-------|-------------|-----------|
| JavaScript/TypeScript | @solana/kit, web3.js, @solana/client, SPL | [clients-javascript](references/clients-javascript.md) |
| Rust | solana-sdk, solana-client, keypair, RPC | [clients-rust](references/clients-rust.md) |
| React & Next.js | @solana/react-hooks, provider, wallet | [frontend-react-nextjs](references/frontend-react-nextjs.md) |

## Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| Staking | Stake accounts, delegate/withdraw, warmup/cooldown, merge/split | [features-staking](references/features-staking.md) |
| Confirmation & Expiration | Blockhash validity, commitment levels, confirmation flow | [features-confirmation](references/features-confirmation.md) |
| Actions & Blinks | Solana Actions API, blinks, actions.json | [features-actions-blinks](references/features-actions-blinks.md) |
| Retry & Rebroadcast | maxRetries, lastValidBlockHeight, when to re-sign | [features-retry](references/features-retry.md) |
| Fee Sponsorship | Fee payer, gas abstraction, fee relayer | [features-fee-sponsorship](references/features-fee-sponsorship.md) |
| Offline Signing | Serialize, sign off-network, recover, durable nonce | [features-offline-signing](references/features-offline-signing.md) |

## Tokens

| Topic | Description | Reference |
|-------|-------------|-----------|
| SPL Token Basics | Mint, token account, transfer, ATA, approve, burn | [tokens-basics](references/tokens-basics.md) |
| Token-2022 Extensions | Metadata, transfer fees, confidential, hooks | [tokens-extensions](references/tokens-extensions.md) |

## RPC & Payments

| Topic | Description | Reference |
|-------|-------------|-----------|
| RPC HTTP & WebSocket | getAccountInfo, getBalance, subscriptions | [rpc-http-websocket](references/rpc-http-websocket.md) |
| Payments & Solana Pay | Payment URLs, verification, send/accept | [payments-solana-pay](references/payments-solana-pay.md) |

## Cookbook & Reference

| Topic | Description | Reference |
|-------|-------------|-----------|
| Cookbook Recipes | Send SOL, keypair, balance, memo, priority fees | [cookbook-recipes](references/cookbook-recipes.md) |
| Clusters & Terminology | Mainnet, devnet, terms, staking | [references-clusters-terminology](references/references-clusters-terminology.md) |

## Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Compute Optimization | CU limits, measurement, logging, data types, PDAs | [best-practices-compute](references/best-practices-compute.md) |
