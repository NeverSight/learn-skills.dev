---
name: hiero-cli
description: "Use when user wants to interact with Hedera blockchain: create/transfer tokens, manage NFTs, deploy contracts, manage topics, transfer HBAR, sign x402 payment challenges, configure networks. ALSO use when an HTTP request returns 402 with a PAYMENT-REQUIRED header for the Hedera x402 scheme (or the user wants to pay an x402-gated endpoint on Hedera): read references/x402.md for the full GET→402→sign→retry flow. Provides full spec for hcli CLI tool. Trigger keywords: hedera, hiero, hbar, token, nft, contract, topic, x402, 402, payment-required, hcli, ledger"
---

# hiero-cli (hcli)

`hcli` is a command-line tool for interacting with the Hedera blockchain — managing accounts, tokens (FT/NFT), smart contracts, consensus topics, and network configuration.

## Binary syntax

```
hcli <plugin> <command> [options]
```

## Global flags

| Flag                    | Short | Default  | Description                                                                                                                                                      |
| ----------------------- | ----- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--format`              | `-F`  | `human`  | Output format: `human` or `json`                                                                                                                                 |
| `--network`             | `-N`  | active   | Override active network for this command                                                                                                                         |
| `--payer`               | `-P`  | operator | Override payer account for this command; defaults to operator if omitted                                                                                         |
| `--confirm`             | `-Y`  | `false`  | Skip all confirmation prompts                                                                                                                                    |
| `--max-transaction-fee` | `-M`  | config   | Max transaction fee ceiling for this run: HBAR (e.g. `20`) or tinybars (`200000000t`). Overrides the `default_max_transaction_fee` config; `0` means no override |

## Prerequisites

Before executing blockchain commands:

1. Configure network: `hcli network use --global testnet`
2. Set operator: `hcli network set-operator --operator <accountId>:<privateKey>`

## Key formats

Keys and signers accept multiple formats:

- `{accountId}:{privateKey}` — inline pair, e.g. `0.0.123:abc123...`
- `{ed25519|ecdsa}:private:{hex}` — raw private key with type prefix
- `{ed25519|ecdsa}:public:{hex}` — raw public key (for supply/submit keys)
- `kr_xxx` — key reference stored in KMS
- account alias — name registered in local state

## Local state storage

State is persisted in `~/.hiero-cli/state/` as JSON files, one per plugin namespace:

| Plugin              | File                                                                 |
| ------------------- | -------------------------------------------------------------------- |
| `account`           | `account-accounts-storage.json`                                      |
| `token`             | `token-tokens-storage.json`                                          |
| `topic`             | `topic-topics-storage.json`                                          |
| `batch`             | `batch-batches-storage.json`                                         |
| `swap`              | `swap-storage.json`                                                  |
| `contract`          | `contract-contracts-storage.json`                                    |
| `schedule`          | `schedule-transactions-storage.json`                                 |
| `network`           | `network-config-storage.json`                                        |
| `config`            | `config-storage.json`                                                |
| `plugin-management` | `plugin-management-storage.json`                                     |
| `credentials` (KMS) | `kms-credentials-storage.json`, `kms-secrets-encrypted-storage.json` |

## Amount notation

- `"1"` = 1 display unit (e.g. 1 HBAR, or 1 token with decimals applied)
- `"100t"` = 100 base/raw units (tinybars for HBAR, smallest token unit)

## Plugin catalog

| Plugin              | Description                | Tasks covered                                                                                                                                                                                                                                                                           |
| ------------------- | -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `account`           | Manage Hedera accounts     | create, import, balance, list, view, update, delete, clear                                                                                                                                                                                                                              |
| `hbar`              | Transfer HBAR              | transfer HBAR, approve/revoke HBAR allowance                                                                                                                                                                                                                                            |
| `token`             | Manage FT & NFT tokens     | create-ft/nft, create-from-file, mint, burn, wipe, transfer, airdrop, associate, dissociate, freeze/unfreeze, pause/unpause, grant/revoke KYC, allowance (FT/NFT), delete-allowance-nft, update-metadata-nft, pending-airdrops, cancel/claim/reject-airdrop, list, view, import, delete |
| `topic`             | Hedera Consensus Service   | create, update, submit/find messages, import, list, delete                                                                                                                                                                                                                              |
| `schedule`          | Scheduled transactions     | create schedule record, sign pending schedule, delete schedule, verify execution state, list schedules. Use `--scheduled <name>` (`-X`) only on commands marked `[scheduled]` in the plugin reference                                                                                   |
| `contract`          | Smart contract lifecycle   | compile + deploy Solidity, import, list, delete                                                                                                                                                                                                                                         |
| `contract-erc20`    | ERC-20 contract calls      | name, symbol, decimals, balanceOf, transfer, transferFrom, approve, allowance, totalSupply. **Requires `contract` plugin** (contract must be deployed first)                                                                                                                            |
| `contract-erc721`   | ERC-721 contract calls     | balanceOf, ownerOf, approve, setApprovalForAll, safeTransferFrom, transferFrom, mint, name, symbol, tokenURI, getApproved, isApprovedForAll. **Requires `contract` plugin** (contract must be deployed first)                                                                           |
| `network`           | Network configuration      | list networks, switch network, set/get operator                                                                                                                                                                                                                                         |
| `config`            | CLI configuration          | list, get, set config options                                                                                                                                                                                                                                                           |
| `credentials`       | Key/credentials management | generate new key, import existing key, list, remove stored credentials (by id or alias)                                                                                                                                                                                                 |
| `batch`             | Batch transactions         | create batch, add transactions, execute, list, delete                                                                                                                                                                                                                                   |
| `swap`              | Multi-party asset exchange | create swap, add HBAR/FT/NFT transfers, view, list, execute, delete                                                                                                                                                                                                                     |
| `eip712`            | EIP-712 typed data signing | `hash` compute digest, `sign-ecdsa` / `sign-ed25519` sign payload (accepts pre-computed hash or domain+types+message), `verify-ecdsa` recover signer EVM address, `verify-ed25519` verify Ed25519 signature against a public key                                                        |
| `x402`              | x402 payment signing       | sign a `PAYMENT-REQUIRED` challenge into a `PAYMENT-SIGNATURE` header via KMS; payer key never exposed, facilitator submits                                                                                                                                                              |
| `plugin-management` | Plugin lifecycle           | add, remove, enable, disable, list, reset, info                                                                                                                                                                                                                                         |

## Agent instruction

**Before executing any command, read `references/<plugin>.md` for the full command spec, all options, and examples.**

Example: to use `hcli token create-ft`, first read `references/token.md`.

**When working with batch commands, read both `references/batch.md` AND the reference for the plugin being batched.**

Example: to batch `hcli token mint-ft`, read both `references/batch.md` and `references/token.md`.

**When working with scheduled transactions, read `references/schedule.md` AND the reference for the command being scheduled.**

Only commands marked **[scheduled]** in their reference support `--scheduled <name>` / `-X`.

Example: to schedule `hcli token burn-ft`, read both `references/schedule.md` and `references/token.md`.

## x402 paid endpoints

If fetching a URL returns HTTP `402` with a `PAYMENT-REQUIRED` header, the
endpoint is x402-gated. Inspect the header payload: if its `accepts` lists a
`hedera:mainnet` / `hedera:testnet` `exact` requirement, **read
`references/x402.md`** and follow the flow there. The agent makes the HTTP
requests itself; `hcli x402 sign` only produces the `PAYMENT-SIGNATURE` value.
If the challenge is for a non-Hedera scheme, this CLI cannot sign it.

## hcli not found / not installed

If any `hcli` command fails with a "command not found" or similar error, tell the user:

> `hcli` is not installed or not available in PATH.
> Docs & quick start: https://www.npmjs.com/package/@hiero-ledger/hiero-cli#quick-start
>
> Install with:
>
> ```
> npm install -g @hiero-ledger/hiero-cli
> ```
>
> Would you like me to run the install command for you?

Do not run the install automatically — wait for the user's confirmation.

## Operator not configured

If a command fails with `CLI operator is not configured` or similar:

1. Inform the user the operator must be set before running any blockchain command
2. Guide them: `hcli network set-operator --operator <accountId>:<privateKey>`
3. Retry the original command after operator is set

## Disabled plugin recovery

If a command fails with `Plugin 'X' is disabled.`:

1. Inform the user that the plugin is disabled
2. Offer to enable it: `hcli plugin-management enable --name X`
3. Retry the original command after enabling

## Common workflows

### Setup (first time)

```bash
hcli network use --global testnet
hcli network set-operator --operator 0.0.12345:302e...privatekey...
```

### Create fungible token and transfer

```bash
# 1. Create token
hcli token create-ft --token-name "MyToken" --symbol MTK --decimals 2 --initial-supply 1000000

# 2. Associate recipient account
hcli token associate --token MTK --account 0.0.67890:302e...key...

# 3. Transfer tokens
hcli token transfer-ft --token MTK --to 0.0.67890 --amount 100
```

### Deploy ERC-20 contract and interact

```bash
# 1. Deploy built-in ERC-20 template
hcli contract create --name myErc20 --default erc20 --constructor-parameter "MyToken" --constructor-parameter "MTK"

# 2. Check balance
hcli contract-erc20 balance-of --contract myErc20 --account 0.0.12345

# 3. Transfer via contract
hcli contract-erc20 transfer --contract myErc20 --to 0.0.67890 --value 50
```

### Batch multiple token mints

```bash
# 1. Create batch
hcli batch create --name mintBatch --key 0.0.12345:302e...key...

# 2. Add transactions to batch (using --batch flag on batchify-compatible commands)
hcli token mint-ft --token MTK --amount 1000 --supply-key 0.0.12345:302e...key... --batch mintBatch

# 3. Execute batch
hcli batch execute --name mintBatch
```
