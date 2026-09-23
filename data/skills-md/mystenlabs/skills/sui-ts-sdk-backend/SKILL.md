---
name: sui-ts-sdk-backend
description: >
  Sui TypeScript SDK for backend services and autonomous agents. Use when
  building a backend, agent, or service that interacts with Sui programmatically
  without CLI — keypair creation, faucet funding, client setup, transaction
  building and signing, package publishing from code, sponsored transactions,
  running transactions at scale with executors, cloud KMS signing (AWS/GCP),
  and multisig workflows. Also use when the user asks how to bootstrap a Sui
  agent, build a backend signer service, or run high-throughput transaction
  pipelines.

  For frontend dApp development with wallets, see the `frontend-apps` skill.
  For SDK selection (TS vs Rust vs community), see the `sui-sdks` skill.
  For PTB semantics and command reference, see the `ptbs` skill.
  For Move smart contract development, see the `sui-move` skill.
---

# Sui TypeScript SDK — Backend & Agent Patterns

> **MCP tool:** When available in your environment, also query the Sui documentation MCP server (`https://sui.mcp.kapa.ai`) for up-to-date answers. Use it for verification and for details not covered by these reference files.

> **Source constraint:** All information in this skill is sourced exclusively from [sdk.mystenlabs.com](https://sdk.mystenlabs.com). When extending or updating this skill, only pull from this source. Do not use third-party blogs, tutorials, or unofficial documentation.

This skill covers using the Sui TypeScript SDK (`@mysten/sui` v2) for backend services and autonomous agents that cannot use the Sui CLI. It provides the end-to-end programmatic workflow: creating keypairs, funding addresses, connecting to networks, building and signing transactions, publishing packages, sponsoring transactions for users, running at scale, and signing with cloud KMS or multisig.

All patterns in this skill are derived from:
  https://sdk.mystenlabs.com

If unsure about any API, fetch the relevant page before answering. Do not guess or extrapolate.

---

## Reference files

### bootstrap — Keypair, Faucet, and Client Setup
**Path:** `bootstrap.md`
**Load when:** creating a keypair programmatically, funding an address from the faucet without CLI, configuring a `SuiGrpcClient` or `SuiGraphQLClient`, or bootstrapping an agent's first connection to Sui.
**Covers:** keypair creation (random, mnemonic, import/export, Bech32 `suiprivkey` format), all three key types (Ed25519, Secp256k1, Secp256r1), programmatic faucet requests, client instantiation and network selection, client extensions, the complete bootstrap sequence.

### transactions — Building, Coins, and Execution
**Path:** `transactions.md`
**Load when:** building transactions with `tx.coin()` or `tx.balance()`, handling address balances vs coin objects, signing and executing from a backend keypair, checking results, waiting for indexing, or handling gasless transactions.
**Covers:** `tx.coin()` and `tx.balance()` (the recommended coin access pattern), address balances vs coin objects, splitting and merging coins, signing with keypairs directly, result handling (`FailedTransaction` checks), `waitForTransaction`, gasless stablecoin transfers.

### publishing — Programmatic Package Publish and Upgrade
**Path:** `publishing.md`
**Load when:** publishing a Move package from TypeScript without CLI, upgrading a published package programmatically, or constructing Publish/Upgrade PTB commands.
**Covers:** building Move bytecode, constructing Publish commands in PTBs, executing publish transactions, extracting package ID and UpgradeCap from results, programmatic upgrades with UpgradeCap, upgrade policies.

### sponsorship — Sponsored Transactions
**Path:** `sponsorship.md`
**Load when:** sponsoring transactions for users, building a gas station backend, using the `@mysten-incubation/sponsor` SDK, or implementing address-balance or coin-based sponsorship flows.
**Covers:** `@mysten-incubation/sponsor` package, client-builds flow (recommended), backend validation and co-signing, config endpoint pattern, coin-based vs address-balance sponsorship, `useGasCoin: false` for token transfers, result handling (Rejected vs FailedTransaction vs success).

### executors — Running Transactions at Scale
**Path:** `executors.md`
**Load when:** running many transactions from one address, building a high-throughput pipeline, managing gas pools, or needing parallel or serial transaction execution without manual gas management.
**Covers:** `SerialTransactionExecutor` (queuing, gas merging, object caching), `ParallelTransactionExecutor` (concurrent execution, gas pool, conflict detection), configuration options, best practices for unresolved object IDs.

### signing — Cloud KMS and Multisig
**Path:** `signing.md`
**Load when:** signing with AWS KMS or GCP KMS, setting up multisig wallets, combining partial signatures, mixing keypair types (Ed25519 + zkLogin + passkey), or building a custody/signer service.
**Covers:** Signer interface (shared across all signer types), AWS KMS signer (`@mysten/aws-kms-signer`), GCP KMS signer (`@mysten/gcp-kms-signer`), `MultiSigPublicKey` setup (threshold, weights), `MultiSigSigner`, combining partial signatures, hybrid multisig (keypairs + zkLogin + passkeys).

---

## Routing guide

| Task | Load |
|------|------|
| Bootstrapping an agent from scratch | bootstrap |
| Creating a keypair without CLI | bootstrap |
| Getting testnet SUI without CLI | bootstrap |
| Connecting to Mainnet/Testnet/Devnet | bootstrap |
| Building a transaction with coin access | transactions |
| Signing and executing from a backend | transactions |
| Handling address balances vs coin objects | transactions |
| Publishing a Move package from TypeScript | publishing |
| Upgrading a package programmatically | publishing |
| Sponsoring transactions for users | sponsorship |
| Building a gas station backend | sponsorship |
| Running many transactions efficiently | executors |
| Building a high-throughput pipeline | executors |
| Signing with AWS or GCP KMS | signing |
| Setting up multisig | signing |
| Building a custody service | signing |
| Full backend service from scratch | **all reference files** |
| Agent onboarding end-to-end | bootstrap + transactions |

---

## Rules

- Always use `@mysten/sui` v2 (`@mysten/sui/grpc`, `@mysten/sui/keypairs/ed25519`, etc.). Never use the deprecated `@mysten/sui.js` v1.
- Always use `SuiGrpcClient` as the default client. Use `SuiGraphQLClient` only when you need flexible relational queries.
- Always check `result.$kind` after transaction execution. A result that is not `Rejected` can still be `FailedTransaction` (executed on-chain but aborted — gas is still consumed).
- Always call `await client.waitForTransaction({ result })` before reading state that depends on a transaction's effects.
- Use `tx.coin()` and `tx.balance()` as the primary way to access funds. They automatically resolve from both address balances and coin objects. Specify `type` for non-SUI tokens.
- For transfers, prefer `balance::send_funds` over `transferObjects`. It deposits directly into the recipient's address balance, avoiding versioned coin objects on the receiving side.
- For sponsored transactions where the sender needs to transfer their own tokens, set `useGasCoin: false` on `tx.coin()` / `tx.balance()` calls to source from the sender's balance instead of the sponsor's gas coin.
- For scale, use `SerialTransactionExecutor` or `ParallelTransactionExecutor` instead of manual gas management loops.
- For production backends, use AWS KMS or GCP KMS signers instead of storing raw private keys.

## Common mistakes

- **Storing raw private keys in environment variables for production.** Use AWS KMS or GCP KMS signers. Raw keys are acceptable for development/testing only.
- **Not waiting for indexing after a transaction.** Read APIs may not immediately reflect transaction effects. Always `waitForTransaction` before dependent reads.
- **Assuming `result` means success.** Check `result.$kind !== 'FailedTransaction'`. A `FailedTransaction` was executed on-chain (gas consumed) but the Move call aborted.
- **Using `splitCoins(tx.gas, ...)` when the sender is not the gas owner.** In sponsored transactions, `tx.gas` belongs to the sponsor. If the sender needs to transfer their own tokens, use `tx.coin()` with `useGasCoin: false` to source from the sender's balance instead.
- **Running multiple `ParallelTransactionExecutor` instances on the same address.** This causes gas coin conflicts. Use a single executor per address.
- **Building transactions with fully-specified object refs when using executors.** Use unresolved object IDs (`tx.object('0x...')`) so the executor can leverage its object cache.
