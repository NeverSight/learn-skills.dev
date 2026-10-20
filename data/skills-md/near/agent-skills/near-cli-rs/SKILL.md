---
name: near-cli-rs
description: Generate near-cli-rs v0.14+ commands for NEAR Protocol — account management, NEAR/FT/NFT token transfers, staking delegation, contract deployment and calls, transaction signing (keychain, Ledger, seed phrase, MPC, offline), and network config
---

# SKILL: near-cli-rs — NEAR Protocol CLI Reference for AI Agents

**Purpose:** This file is for LLMs generating non-interactive `near` commands. When a user request maps to a CLI action, look up the correct syntax here, construct the complete one-liner, show it to the user for approval, then execute it.

**Rule:** Always produce complete commands from `near` through the final action token (`send`, `display`, `now`, `create`, etc.). Never omit `network-config <NETWORK>`.

**Version:** near-cli-rs v0.14+ (tested through v0.30.x, 2026-09)

**Sources:** [near/near-cli-rs](https://github.com/near/near-cli-rs) · [Releases](https://github.com/near/near-cli-rs/releases) · [docs.near.org/tools/cli](https://docs.near.org/tools/cli)

## Changes Since v0.24 (v0.25–v0.30.x)

Newer CLI versions changed behavior worth knowing when generating commands:

- **Gas keys** (nearcore 2.13+): transactions can be signed with a gas key; signing prompts a `nonce_index` selection. `near transaction sign-message` also supports gas-key signing.
- **Post-quantum keys (draft)**: ML-DSA-65 keys can be generated in v0.28+ (`ml-dsa-65:` key format); pubkey display includes `ml-dsa-65-hash`. Experimental — usually stick with `ed25519`.
- **Removed:** the standalone `generate-keypair` command (use `account import-account` with a locally generated key instead).
- **New commands:** `tokens send-ft-call` (`ft_transfer_call` on the `tokens` subcommand); `account import-account` works non-interactively against an existing account; `contract state-init` initializes a new contract's state at deploy time.
- **Defaults changed:** function-call gas limits updated to 1000 TGas; contract-surface FT listing improved (view FTs for all contracts in an account, not only a hardcoded list).
- Global-hash deployment is retry-safe; beneficiary account is validated before `account delete-account`.

Verify exact syntax with `near --help` / `near <group> <subcommand> --help` if your CLI version disagrees with a generated command here.

---

## Command Grammar

```
near [GLOBAL_FLAGS] <COMMAND_GROUP> [ENTITY_ARGS] <SUBCOMMAND> [SUB_ARGS] network-config <NETWORK> [SIGNING_OPTION] [FINAL_ACTION]
```

- **View commands** end with: `now` | `at-block-height <N>` | `at-block-hash <HASH>`
- **Transaction commands** end with a signing option followed by `send` or `display`
- **Account creation via faucet** ends with `create`
- `network-config` keyword is **always required** (even for view commands)

---

## Global Flags

| Flag         | Effect                                               |
| ------------ | ---------------------------------------------------- |
| `--offline`  | Create/sign tx without network access                |
| `--quiet`    | Suppress progress output (recommended for scripting) |
| `--teach-me` | Print all RPC calls and their parameters             |

---

## Networks and View Qualifiers

| Item                  | Value                                                       |
| --------------------- | ----------------------------------------------------------- |
| Built-in networks     | `mainnet`, `testnet`                                        |
| Custom network        | any `<connection-name>` from `near config show-connections` |
| View: latest block    | `now`                                                       |
| View: specific height | `at-block-height <BLOCK_HEIGHT>`                            |
| View: specific hash   | `at-block-hash <BLOCK_HASH>`                                |

---

## Amount and Gas Formats

| Asset     | Format                      | Notes                                    |
| --------- | --------------------------- | ---------------------------------------- |
| NEAR      | `'1 NEAR'` or `'0.5 NEAR'`  | Quoted, space before unit                |
| yoctoNEAR | `'1 yoctoNEAR'`             | Required deposit for many contract calls |
| Gas       | `'30 Tgas'` to `'300 Tgas'` | Default `'100 Tgas'`, max `'300 Tgas'`   |
| FT amount | `'10 usn'`                  | Number + FT symbol, quoted               |
| FT all    | `all`                       | Transfer entire balance                  |

---

## Signing Options Reference

Replace `<SIGNING_OPTION>` in any transaction command with one of:

| Option                                   | Full syntax                                                                                                        |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| OS keychain (recommended)                | `sign-with-keychain send`                                                                                          |
| Legacy keychain (`~/.near-credentials/`) | `sign-with-legacy-keychain send`                                                                                   |
| Ledger hardware wallet                   | `sign-with-ledger send`                                                                                            |
| Plaintext private key                    | `sign-with-plaintext-private-key --signer-public-key ed25519:<PUBKEY> --signer-private-key ed25519:<PRIVKEY> send` |
| Access key file                          | `sign-with-access-key-file /path/to/key.json send`                                                                 |
| Seed phrase                              | `sign-with-seed-phrase 'word1 ... word12' --seed-phrase-hd-path 'm/44'"'"'/397'"'"'/0'"'"'' send`                  |
| MPC                                      | `sign-with-mpc send`                                                                                               |
| Produce unsigned tx (sign later)         | `sign-later`                                                                                                       |

Replace `send` with `display` to print the signed transaction in base64 without broadcasting.

---

## `account` Commands

### view-account-summary

```sh
# Current block
near account view-account-summary <ACCOUNT_ID> network-config <NETWORK> now

# Specific block height
near account view-account-summary <ACCOUNT_ID> network-config <NETWORK> at-block-height <BLOCK_HEIGHT>

# Specific block hash
near account view-account-summary <ACCOUNT_ID> network-config <NETWORK> at-block-hash <BLOCK_HASH>
```

### import-account

```sh
# Using seed phrase (non-interactive)
near account import-account using-seed-phrase '<SEED_PHRASE>' --seed-phrase-hd-path 'm/44'"'"'/397'"'"'/0'"'"'' network-config <NETWORK>

# Using private key
near account import-account using-private-key ed25519:<PRIVATE_KEY> network-config <NETWORK>

# NOTE: using-web-wallet requires a browser redirect — not suitable for non-interactive use
```

### export-account

```sh
# Export as seed phrase
near account export-account <ACCOUNT_ID> using-seed-phrase network-config <NETWORK>

# Export as private key
near account export-account <ACCOUNT_ID> using-private-key network-config <NETWORK>
```

### create-account

```sh
# Testnet faucet (testnet only) — autogenerate keypair
near account create-account sponsor-by-faucet-service <NEW_ACCOUNT_ID> autogenerate-new-keypair save-to-keychain network-config testnet create

# Testnet faucet — use known seed phrase
near account create-account sponsor-by-faucet-service <NEW_ACCOUNT_ID> use-manually-provided-seed-phrase '<SEED_PHRASE>' network-config testnet create

# Testnet faucet — use known public key
near account create-account sponsor-by-faucet-service <NEW_ACCOUNT_ID> use-manually-provided-public-key ed25519:<PUBKEY> network-config testnet create

# Fund-myself: create sub-account (signer is implicit from keychain)
near account create-account fund-myself <NEW_ACCOUNT_ID> '<INITIAL_BALANCE>' autogenerate-new-keypair save-to-keychain sign-as network-config <NETWORK> sign-with-keychain send

# Fund-myself: create account specifying explicit signer
near account create-account fund-myself <NEW_ACCOUNT_ID> '<INITIAL_BALANCE>' autogenerate-new-keypair save-to-keychain sign-as <SIGNER_ACCOUNT_ID> network-config <NETWORK> sign-with-keychain send

# Fund-myself: use known seed phrase for new account
near account create-account fund-myself <NEW_ACCOUNT_ID> '<INITIAL_BALANCE>' use-manually-provided-seed-phrase '<SEED_PHRASE>' sign-as <SIGNER_ACCOUNT_ID> network-config <NETWORK> sign-with-keychain send

# Fund-myself: use known public key for new account
near account create-account fund-myself <NEW_ACCOUNT_ID> '<INITIAL_BALANCE>' use-manually-provided-public-key ed25519:<PUBKEY> sign-as <SIGNER_ACCOUNT_ID> network-config <NETWORK> sign-with-keychain send
```

### delete-account

```sh
near account delete-account <ACCOUNT_ID> beneficiary <BENEFICIARY_ACCOUNT_ID> network-config <NETWORK> sign-with-keychain send
```

### list-keys

```sh
near account list-keys <ACCOUNT_ID> network-config <NETWORK> now
```

### get-public-key

```sh
# From seed phrase
near account get-public-key from-seed-phrase '<SEED_PHRASE>' --seed-phrase-hd-path "m/44'/397'/0'"

# From plaintext private key
near account get-public-key from-plaintext-private-key ed25519:<PRIVATE_KEY>

# From OS keychain
near account get-public-key from-keychain <ACCOUNT_ID> network-config <NETWORK>

# From legacy keychain
near account get-public-key from-legacy-keychain <ACCOUNT_ID> network-config <NETWORK>

# From Ledger (requires 5-component path)
near account get-public-key from-ledger --seed-phrase-hd-path "m/44'/397'/0'/0'/1'"
```

### add-key

```sh
# Add full-access key (provide existing public key)
near account add-key <ACCOUNT_ID> grant-full-access use-manually-provided-public-key ed25519:<PUBKEY> network-config <NETWORK> sign-with-keychain send

# Add function-call-only key (autogenerate keypair)
near account add-key <ACCOUNT_ID> grant-function-call-access --allowance '<ALLOWANCE>' --contract-account-id <CONTRACT_ID> --function-names '<METHOD1>, <METHOD2>' autogenerate-new-keypair save-to-keychain network-config <NETWORK> sign-with-keychain send

# Add function-call-only key (allow all methods on contract)
near account add-key <ACCOUNT_ID> grant-function-call-access --allowance '<ALLOWANCE>' --contract-account-id <CONTRACT_ID> --function-names '' use-manually-provided-public-key ed25519:<PUBKEY> network-config <NETWORK> sign-with-keychain send
```

### delete-keys

```sh
near account delete-keys <ACCOUNT_ID> public-keys ed25519:<PUBKEY> network-config <NETWORK> sign-with-keychain send
```

### manage-storage-deposit

```sh
# View storage balance
near account manage-storage-deposit <CONTRACT_ID> view-balance <ACCOUNT_ID> network-config <NETWORK> now

# Deposit storage
near account manage-storage-deposit <CONTRACT_ID> deposit <ACCOUNT_ID> '<AMOUNT>' sign-as <SIGNER_ACCOUNT_ID> network-config <NETWORK> sign-with-keychain send

# Withdraw from storage
near account manage-storage-deposit <CONTRACT_ID> withdraw '<AMOUNT>' sign-as <ACCOUNT_ID> network-config <NETWORK> sign-with-keychain send
```

### update-social-profile

```sh
# Update profile with JSON args
near account update-social-profile <ACCOUNT_ID> json-args '{"name":"<NAME>","image":{"ipfs_cid":"<CID>"}}' sign-as <ACCOUNT_ID> network-config <NETWORK> sign-with-keychain send

# Update profile from file
near account update-social-profile <ACCOUNT_ID> file-args /path/to/profile.json sign-as <ACCOUNT_ID> network-config <NETWORK> sign-with-keychain send
```

---

## `tokens` Commands

### view-near-balance

```sh
near tokens <ACCOUNT_ID> view-near-balance network-config <NETWORK> now
```

### view-ft-balance

```sh
near tokens <ACCOUNT_ID> view-ft-balance <FT_CONTRACT_ID> network-config <NETWORK> now
```

### view-nft-assets

```sh
near tokens <ACCOUNT_ID> view-nft-assets <NFT_CONTRACT_ID> network-config <NETWORK> now
```

### send-near

```sh
near tokens <SENDER_ACCOUNT_ID> send-near <RECEIVER_ACCOUNT_ID> '<AMOUNT>' network-config <NETWORK> sign-with-keychain send
```

### send-ft

```sh
# Send specific amount
near tokens <SENDER_ACCOUNT_ID> send-ft <FT_CONTRACT_ID> <RECEIVER_ACCOUNT_ID> '<AMOUNT>' memo '<MEMO>' network-config <NETWORK> sign-with-keychain send

# Send all tokens (with optional custom gas/deposit)
near tokens <SENDER_ACCOUNT_ID> send-ft <FT_CONTRACT_ID> <RECEIVER_ACCOUNT_ID> all memo '' --prepaid-gas '300.0 Tgas' --attached-deposit '1 yoctoNEAR' network-config <NETWORK> sign-with-keychain send
```

Note: Default `prepaid-gas` is `'100.0 Tgas'` and `attached-deposit` is `'1 yoctoNEAR'`.

### send-nft

```sh
near tokens <SENDER_ACCOUNT_ID> send-nft <NFT_CONTRACT_ID> <RECEIVER_ACCOUNT_ID> <TOKEN_ID> --prepaid-gas '300.0 Tgas' --attached-deposit '1 yoctoNEAR' network-config <NETWORK> sign-with-keychain send
```

---

## `staking` Commands

### validator-list

```sh
near staking validator-list network-config <NETWORK>
```

### delegation

```sh
# View delegated stake balance
near staking delegation <ACCOUNT_ID> view-balance <POOL_ID> network-config <NETWORK> now

# Deposit and stake (send NEAR to pool and immediately stake)
near staking delegation <ACCOUNT_ID> deposit-and-stake '<AMOUNT>' <POOL_ID> network-config <NETWORK> sign-with-keychain send

# Stake previously deposited tokens
near staking delegation <ACCOUNT_ID> stake '<AMOUNT>' <POOL_ID> network-config <NETWORK> sign-with-keychain send

# Stake all previously deposited or unstaked tokens
near staking delegation <ACCOUNT_ID> stake-all <POOL_ID> network-config <NETWORK> sign-with-keychain send

# Unstake a specific amount
near staking delegation <ACCOUNT_ID> unstake '<AMOUNT>' <POOL_ID> network-config <NETWORK> sign-with-keychain send

# Unstake everything
near staking delegation <ACCOUNT_ID> unstake-all <POOL_ID> network-config <NETWORK> sign-with-keychain send

# Withdraw a specific amount (after unstaking + ~2 epoch wait)
near staking delegation <ACCOUNT_ID> withdraw '<AMOUNT>' <POOL_ID> network-config <NETWORK> sign-with-keychain send

# Withdraw all available unstaked tokens
near staking delegation <ACCOUNT_ID> withdraw-all <POOL_ID> network-config <NETWORK> sign-with-keychain send
```

**Note:** Unstaked funds require approximately 2 epochs (~48 hours) before they can be withdrawn.

---

## `contract` Commands

### call-function (view/read-only)

```sh
# With JSON args
near contract call-function as-read-only <CONTRACT_ID> <METHOD_NAME> json-args '{"key":"value"}' network-config <NETWORK> now

# With empty args
near contract call-function as-read-only <CONTRACT_ID> <METHOD_NAME> empty-args network-config <NETWORK> now

# With text args
near contract call-function as-read-only <CONTRACT_ID> <METHOD_NAME> text-args '<STRING>' network-config <NETWORK> now

# With base64 args
near contract call-function as-read-only <CONTRACT_ID> <METHOD_NAME> base64-args '<BASE64>' network-config <NETWORK> now
```

### call-function (transaction/state-changing)

```sh
# With JSON args
near contract call-function as-transaction <CONTRACT_ID> <METHOD_NAME> json-args '{"key":"value"}' prepaid-gas '<GAS>' attached-deposit '<DEPOSIT>' sign-as <SIGNER_ACCOUNT_ID> network-config <NETWORK> sign-with-keychain send

# With empty args
near contract call-function as-transaction <CONTRACT_ID> <METHOD_NAME> empty-args prepaid-gas '<GAS>' attached-deposit '<DEPOSIT>' sign-as <SIGNER_ACCOUNT_ID> network-config <NETWORK> sign-with-keychain send
```

### deploy

```sh
# Deploy without init call
near contract deploy <ACCOUNT_ID> use-file /path/to/contract.wasm without-init-call network-config <NETWORK> sign-with-keychain send

# Deploy with init call
near contract deploy <ACCOUNT_ID> use-file /path/to/contract.wasm with-init-call <INIT_METHOD> json-args '{}' prepaid-gas '100 Tgas' attached-deposit '0 NEAR' network-config <NETWORK> sign-with-keychain send
```

### inspect

```sh
near contract inspect <CONTRACT_ID> network-config <NETWORK> now
```

### verify

```sh
near contract verify deployed-at <CONTRACT_ID> network-config <NETWORK> now
```

### download-abi

```sh
near contract download-abi <CONTRACT_ID> save-to-file <OUTPUT_FILE_PATH> network-config <NETWORK> now
```

### download-wasm

```sh
near contract download-wasm <CONTRACT_ID> save-to-file <OUTPUT_FILE_PATH> network-config <NETWORK> now
```

### view-storage

```sh
# View all storage as JSON
near contract view-storage <CONTRACT_ID> all as-json network-config <NETWORK> now

# View storage filtered by key prefix (string)
near contract view-storage <CONTRACT_ID> keys-start-with-string '<PREFIX>' as-json network-config <NETWORK> now

# View storage filtered by key prefix (base64)
near contract view-storage <CONTRACT_ID> keys-start-with-bytes-as-base64 '<BASE64_PREFIX>' as-json network-config <NETWORK> now
```

---

## `transaction` Commands

### view-status

```sh
near transaction view-status <TX_HASH> network-config <NETWORK>
```

### reconstruct-transaction

```sh
near transaction reconstruct-transaction <TX_HASH> network-config <NETWORK>
```

### sign-transaction

```sh
near transaction sign-transaction '<UNSIGNED_TX_BASE64>' network-config <NETWORK> sign-with-keychain send
```

### send-signed-transaction

```sh
near transaction send-signed-transaction '<SIGNED_TX_BASE64>' network-config <NETWORK>
```

### print-transaction

```sh
# Print signed transaction fields
near transaction print-transaction signed '<SIGNED_TX_BASE64>'

# Print unsigned transaction fields
near transaction print-transaction unsigned '<UNSIGNED_TX_BASE64>'
```

### send-meta-transaction

```sh
near transaction send-meta-transaction '<SIGNED_DELEGATE_BASE64>' network-config <NETWORK>
```

---

## `config` Commands

### show-connections

```sh
near config show-connections
```

### add-connection

```sh
near config add-connection --network-name <NETWORK_NAME> --connection-name <CONNECTION_NAME> --rpc-url <RPC_URL> --wallet-url <WALLET_URL> --explorer-transaction-url <EXPLORER_TX_URL> [--rpc-api-key '<API_KEY>'] [--linkdrop-account-id <LINKDROP_ID>] [--faucet-url <FAUCET_URL>] [--meta-transaction-relayer-url <RELAYER_URL>]
```

### delete-connection

```sh
near config delete-connection <CONNECTION_NAME>
```

---

## Common Patterns (Cookbook)

Quick-reference one-liners for the most frequent tasks. Substitute placeholders with real values.

### 1. Check NEAR balance

```sh
near tokens alice.near view-near-balance network-config mainnet now
```

### 2. Transfer NEAR tokens

```sh
near tokens alice.near send-near bob.near '5 NEAR' network-config mainnet sign-with-keychain send
```

### 3. View account details

```sh
near account view-account-summary alice.near network-config mainnet now
```

### 4. List access keys

```sh
near account list-keys alice.near network-config mainnet now
```

### 5. Send fungible tokens

```sh
near tokens alice.near send-ft usdt.tether-token.near bob.near '10 USDT' memo '' network-config mainnet sign-with-keychain send
```

### 6. View FT balance

```sh
near tokens alice.near view-ft-balance usdt.tether-token.near network-config mainnet now
```

### 7. Call a view-only contract method

```sh
near contract call-function as-read-only wrap.near ft_balance_of json-args '{"account_id":"alice.near"}' network-config mainnet now
```

### 8. Call a state-changing contract method

```sh
near contract call-function as-transaction wrap.near ft_transfer json-args '{"receiver_id":"bob.near","amount":"1000000000000000000000000"}' prepaid-gas '100 Tgas' attached-deposit '1 yoctoNEAR' sign-as alice.near network-config mainnet sign-with-keychain send
```

### 9. Stake NEAR with a validator

```sh
near staking delegation alice.near deposit-and-stake '10 NEAR' aurora.pool.near network-config mainnet sign-with-keychain send
```

### 10. Unstake from a validator

```sh
near staking delegation alice.near unstake-all aurora.pool.near network-config mainnet sign-with-keychain send
```

### 11. Withdraw unstaked NEAR (after ~2 epoch wait)

```sh
near staking delegation alice.near withdraw-all aurora.pool.near network-config mainnet sign-with-keychain send
```

### 12. Create a testnet account (faucet-funded)

```sh
near account create-account sponsor-by-faucet-service myaccount.testnet autogenerate-new-keypair save-to-keychain network-config testnet create
```

### 13. Create a sub-account (self-funded)

```sh
near account create-account fund-myself sub.alice.testnet '1 NEAR' autogenerate-new-keypair save-to-keychain sign-as alice.testnet network-config testnet sign-with-keychain send
```

### 14. Deploy a contract

```sh
near contract deploy mycontract.testnet use-file ./contract.wasm without-init-call network-config testnet sign-with-keychain send
```

### 15. Delete an access key

```sh
near account delete-keys alice.testnet public-keys ed25519:<PUBKEY_TO_REMOVE> network-config testnet sign-with-keychain send
```

### 16. Add a full-access key

```sh
near account add-key alice.testnet grant-full-access use-manually-provided-public-key ed25519:<NEW_PUBKEY> network-config testnet sign-with-keychain send
```

---

## Offline Mode and Scripting Tips

### Offline signing workflow (air-gapped / two-machine)

```sh
# Machine A (offline): produce signed tx in base64 without broadcasting
near --offline tokens alice.near send-near bob.near '1 NEAR' network-config mainnet sign-with-seed-phrase '<SEED_PHRASE>' --seed-phrase-hd-path 'm/44'"'"'/397'"'"'/0'"'"'' display

# Machine B (online): broadcast the base64 tx
near transaction send-signed-transaction '<SIGNED_TX_BASE64>' network-config mainnet
```

### sign-later workflow

```sh
# Step 1: produce unsigned base64 tx
near tokens alice.near send-near bob.near '1 NEAR' network-config mainnet sign-later

# Step 2: sign it (outputs signed base64)
near transaction sign-transaction '<UNSIGNED_TX_BASE64>' network-config mainnet sign-with-keychain display

# Step 3: broadcast
near transaction send-signed-transaction '<SIGNED_TX_BASE64>' network-config mainnet
```

### Scripting tips

- Always add `--quiet` to suppress progress output in scripts
- Always quote amounts: `'1 NEAR'`, `'0.5 NEAR'`, `'1 yoctoNEAR'`
- Seed phrase HD path shell escaping: `'m/44'"'"'/397'"'"'/0'"'"''`
- Use `display` instead of `send` to inspect signed tx before broadcasting

---

## Key Format Reference

| Item             | Format                       | Example                         |
| ---------------- | ---------------------------- | ------------------------------- |
| Public key       | `ed25519:<BASE58>`           | `ed25519:8h7kFK4...`            |
| Private key      | `ed25519:<BASE58>`           | `ed25519:2qM8v3N...`            |
| Transaction hash | 44-char base58               | `F3eZmht...`                    |
| Named account    | `name.near` / `name.testnet` | `alice.near`                    |
| Implicit account | 64-char lowercase hex        | `a4b05ef3...`                   |
| Standard HD path | `m/44'/397'/0'`              | NEAR BIP44                      |
| Ledger HD path   | `m/44'/397'/0'/0'/N'`        | 5-component required for Ledger |
| PQ public key (v0.28+, draft) | `ml-dsa-65:<BASE58>` | post-quantum keys; experimental |

---

## Common Errors

| Error                      | Likely cause / fix                                         |
| -------------------------- | ---------------------------------------------------------- |
| "Account does not exist"   | Wrong network, or account not yet funded                   |
| "Access key not found"     | Use `sign-with-legacy-keychain` or `sign-with-seed-phrase` |
| "Exceeded prepaid gas"     | Increase gas: `'300 Tgas'`                                 |
| FT transfer fails silently | FT `ft_transfer` requires `attached-deposit '1 yoctoNEAR'` |
| "Method not found"         | Check method name with `near contract inspect`             |
| Seed phrase HD path error  | Escape single quotes: `'m/44'"'"'/397'"'"'/0'"'"''`        |
