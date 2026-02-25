---
name: solana-kit
description: Solana Kit (JavaScript SDK) — RPC, signers, transactions, accounts, codecs, instruction plans, and program clients for agent-driven Solana tooling.
metadata:
  author: Hairy
  version: "2026.2.25"
  source: Generated from https://github.com/anza-xyz/kit, scripts located at https://github.com/antfu/skills
---

> Skill based on Kit (anza-xyz/kit), generated 2026-02-25.

Concise reference for building Solana apps with Kit: functional API, tree-shakeable imports, RPC + RPC Subscriptions, signers, transaction messages, account fetch/decode, codecs, and program clients.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Setup | Install, RPC/RPC Subscriptions, typed client | [core-setup](references/core-setup.md) |
| RPC | HTTP client — getBalance, getAccountInfo, getLatestBlockhash, send | [core-rpc](references/core-rpc.md) |
| RPC Subscriptions | WebSocket — accountNotifications, slotNotifications | [core-rpc-subscriptions](references/core-rpc-subscriptions.md) |
| Functional | pipe(), pipeline transforms | [core-functional](references/core-functional.md) |
| Signers | KeyPairSigner, airdrop, wallet swap, no-op | [core-signers](references/core-signers.md) |
| Transactions | pipe, fee payer, lifetime, instructions, sign, send-and-confirm | [core-transactions](references/core-transactions.md) |
| Transaction confirmation | Block height exceedence, recent signature, nonce invalidation, timeout | [core-transaction-confirmation](references/core-transaction-confirmation.md) |
| Accounts | fetchEncodedAccount, program fetch/decode (fetchMint, decodeMint) | [core-accounts](references/core-accounts.md) |
| Address lookup tables | fetchLookupTables, compress message, decompile with lookups | [core-address-lookup-tables](references/core-address-lookup-tables.md) |
| Addresses | Address type, validation, PDA derivation, codecs | [core-addresses](references/core-addresses.md) |
| Sysvars | Fetch/decode Clock, Rent, EpochSchedule, etc. | [core-sysvars](references/core-sysvars.md) |

## Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| Instructions | Program clients — System, Token, Compute Budget | [features-instructions](references/features-instructions.md) |
| Instruction plans | Sequential/parallel plans, planner, executor | [features-instruction-plans](references/features-instruction-plans.md) |
| Codecs | Encode/decode structs, program getXCodec | [features-codecs](references/features-codecs.md) |
| Compatible program clients | @solana-program/*, Codama-generated clients | [features-compatible-clients](references/features-compatible-clients.md) |
| Compat (Web3.js) | fromLegacyPublicKey, fromLegacyKeypair, fromVersionedTransaction | [features-compat](references/features-compat.md) |
| Errors | SolanaError, isSolanaError, context | [features-errors](references/features-errors.md) |
| GraphQL | createSolanaRpcGraphQL, nested queries, caching/batching | [features-graphql](references/features-graphql.md) |
| Key pairs | generateKeyPair, import bytes, polyfill | [features-keypairs](references/features-keypairs.md) |
| Offchain messages | Build, sign, verify, encode/decode (sRFC 3) | [features-offchain-messages](references/features-offchain-messages.md) |
| Program errors | isProgramError — attribute tx failure to program/code | [features-program-errors](references/features-program-errors.md) |
| React | useSignIn, useWalletAccountTransactionSigner, useSignAndSendTransaction | [features-react](references/features-react.md) |
| RPC transports | Custom transport — failover, retry, round-robin, sharding | [features-rpc-transports](references/features-rpc-transports.md) |
| RPC API augmentation | mainnet/devnet, cherry-pick methods, custom RPC methods | [features-rpc-api-augmentation](references/features-rpc-api-augmentation.md) |
| Create Solana program | pnpm create solana-program, Codama-generated JS client | [features-create-solana-program](references/features-create-solana-program.md) |
| Unstable subscriptions | createSolanaRpcSubscriptions_UNSTABLE, block/slotsUpdates | [features-unstable-subscriptions](references/features-unstable-subscriptions.md) |

## Best practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Abort RPC/subscriptions | AbortController, timeout, cancel on navigation | [best-practices-abort-rpc](references/best-practices-abort-rpc.md) |
| Tree-shaking | Narrow imports, sub-packages, smaller bundles | [best-practices-tree-shaking](references/best-practices-tree-shaking.md) |
| Upgrade from Web3.js | Connection → RPC, PublicKey → address, compatible clients | [best-practices-upgrade](references/best-practices-upgrade.md) |
