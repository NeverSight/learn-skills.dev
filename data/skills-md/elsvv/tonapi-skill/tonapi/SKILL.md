---
name: tonapi
description: |
  Use when the user needs to interact with TON blockchain via TonAPI —
  account balances, transactions, jetton/NFT data, smart contract methods,
  staking, DNS, rates, emulation, gasless transactions, webhooks, or streaming.
  Triggers: tonapi, ton api, TON blockchain, TON balance, jetton, NFT on TON,
  TON transaction, TON staking, TON DNS, .ton domain, TON wallet, TON rates,
  toncoin price, TON smart contract, TON emulation, gasless TON.
---

# tonapi

TonAPI — REST API for TON blockchain: accounts, transactions, jettons, NFTs, staking, DNS, rates, emulation, webhooks.

## Config

Requires `TONAPI_TOKEN` in `config/.env`.
Get your token at [TonConsole](https://tonconsole.com/). See `config/README.md` for setup.

**First-time setup:**
```bash
cp config/.env.example config/.env
# Edit config/.env and paste your token
bash scripts/check_connection.sh
```

## Network

Default: **mainnet** (`https://tonapi.io`).
For testnet: pass `--testnet` flag to any script or set `TONAPI_NETWORK=testnet` in `config/.env`.

**IMPORTANT:** Always run scripts with `bash` prefix. Scripts use bash-specific features and will not work if sourced from zsh.

## Quick Start

```bash
# 1. Check connection
bash scripts/check_connection.sh

# 2. Get account info
bash scripts/accounts.sh --action get --account UQDNzlh0XSZdb5_Qrlx5QjyZHVAO74v5oMeVVrtF_5Vt1rIt

# 3. Get jetton balances
bash scripts/accounts.sh --action jettons --account UQDNzlh0XSZdb5_Qrlx5QjyZHVAO74v5oMeVVrtF_5Vt1rIt

# 4. Get TON price
bash scripts/rates.sh --action get --tokens ton --currencies usd

# 5. Get masterchain head
bash scripts/blockchain.sh --action masterchain-head
```

## API Overview

| Category | Script | Key Features |
|----------|--------|--------------|
| Accounts | `accounts.sh` | Balance, events, jettons, NFTs, traces, bulk, search |
| Blockchain | `blockchain.sh` | Blocks, transactions, config, validators, send message, run methods |
| Jettons | `jettons.sh` | Metadata, holders, bulk, transfer payloads |
| NFT | `nft.sh` | Items, collections, bulk, history |
| DNS | `dns.sh` | Resolve, bids, auctions |
| Events | `events.sh` | Events, account events, emulation |
| Traces | `traces.sh` | Execution traces, emulation |
| Staking | `staking.sh` | Pools, nominators, history |
| Rates | `rates.sh` | Token prices, charts, markets |
| Wallet | `wallet.sh` | Wallet info, seqno, TonConnect |
| Gasless | `gasless.sh` | Config, estimate, send gasless tx |
| Multisig | `multisig.sh` | Multisig info, orders |
| LiteServer | `liteserver.sh` | Raw ADNL proxy (16 endpoints) |
| Streaming | `streaming.sh` | SSE: blocks, transactions, traces, mempool |
| Webhooks | `webhooks.sh` | Webhook CRUD, subscriptions, opcodes |
| Utilities | `utilities.sh` | Status, address parse, TonConnect |

## Scripts

### check_connection.sh
Verify token and TonAPI availability.
```bash
bash scripts/check_connection.sh
bash scripts/check_connection.sh --testnet
```

### accounts.sh
Account info, balances, events, jettons, NFTs.
```bash
# Account info
bash scripts/accounts.sh --action get --account <ADDR>

# Bulk accounts
bash scripts/accounts.sh --action bulk --accounts <ADDR1>,<ADDR2>

# Search by domain
bash scripts/accounts.sh --action search --query "wallet"

# Jetton balances
bash scripts/accounts.sh --action jettons --account <ADDR>

# Specific jetton
bash scripts/accounts.sh --action jetton --account <ADDR> --jetton <JETTON_ADDR>

# NFTs owned
bash scripts/accounts.sh --action nfts --account <ADDR> --limit 50

# Events history
bash scripts/accounts.sh --action events --account <ADDR> --limit 20

# Balance diff
bash scripts/accounts.sh --action diff --account <ADDR> --start-date 1700000000 --end-date 1700100000

# Public key
bash scripts/accounts.sh --action publickey --account <ADDR>

# Traces
bash scripts/accounts.sh --action traces --account <ADDR>

# Jetton transfer history
bash scripts/accounts.sh --action jettons-history --account <ADDR>

# NFT transfer history
bash scripts/accounts.sh --action nfts-history --account <ADDR>

# Reindex cache
bash scripts/accounts.sh --action reindex --account <ADDR>
```

| Param | Description |
|-------|-------------|
| `--action` | get, bulk, search, dns, events, jettons, jetton, nfts, traces, subscriptions, publickey, diff, jettons-history, nfts-history, multisigs, reindex |
| `--account` | Account address |
| `--accounts` | Comma-separated addresses (bulk) |
| `--jetton` | Jetton master address |
| `--query` | Search query |
| `--limit` | Max results |
| `--offset` | Offset |
| `--before-lt` | Cursor: before logical time |
| `--start-date` | Unix timestamp start |
| `--end-date` | Unix timestamp end |

### blockchain.sh
Blocks, transactions, methods, send messages.
```bash
# Masterchain head
bash scripts/blockchain.sh --action masterchain-head

# Transaction by hash
bash scripts/blockchain.sh --action transaction --tx-hash <HASH>

# Account transactions
bash scripts/blockchain.sh --action account-transactions --account <ADDR> --limit 10

# Run smart contract method
bash scripts/blockchain.sh --action run-method --account <ADDR> --method get_wallet_address --args "0:addr..."

# Send message
bash scripts/blockchain.sh --action send --boc <BASE64_BOC>

# Validators
bash scripts/blockchain.sh --action validators

# Blockchain config
bash scripts/blockchain.sh --action config

# Inspect contract
bash scripts/blockchain.sh --action inspect --account <ADDR>
```

| Param | Description |
|-------|-------------|
| `--action` | masterchain-head, block, block-transactions, shards, blocks, transactions, config, config-by-block, transaction, msg-transaction, account-raw, account-transactions, inspect, run-method, send, validators, reduced-blocks |
| `--block-id` | Block ID |
| `--seqno` | Masterchain seqno |
| `--tx-hash` | Transaction hash |
| `--msg-hash` | Message hash |
| `--account` | Account address |
| `--method` | Smart contract method name |
| `--args` | Comma-separated method args |
| `--boc` | Base64-encoded BOC |
| `--batch` | Comma-separated BOCs (max 5) |
| `--limit` | Max results (max 1000) |
| `--before-lt` / `--after-lt` | Cursor |
| `--sort-order` | asc or desc |

### jettons.sh
Jetton token data and holders.
```bash
# List all jettons
bash scripts/jettons.sh --action list --limit 20

# Jetton metadata
bash scripts/jettons.sh --action get --jetton <MASTER_ADDR>

# Holders
bash scripts/jettons.sh --action holders --jetton <MASTER_ADDR> --limit 50

# Bulk metadata
bash scripts/jettons.sh --action bulk --addresses <ADDR1>,<ADDR2>
```

### nft.sh
NFT items and collections.
```bash
# Get NFT item
bash scripts/nft.sh --action get --address <NFT_ADDR>

# List collections
bash scripts/nft.sh --action collections --limit 20

# Collection items
bash scripts/nft.sh --action collection-items --address <COLLECTION_ADDR> --limit 50

# Bulk NFTs
bash scripts/nft.sh --action bulk --addresses <ADDR1>,<ADDR2>
```

### dns.sh
TON DNS domains and auctions.
```bash
# Domain info
bash scripts/dns.sh --action info --domain wallet.ton

# DNS resolve
bash scripts/dns.sh --action resolve --domain wallet.ton

# Domain bids
bash scripts/dns.sh --action bids --domain wallet.ton

# All auctions
bash scripts/dns.sh --action auctions
```

### events.sh
High-level events (human-readable transaction actions).
```bash
# Event by ID
bash scripts/events.sh --action get --event-id <ID>

# Account events
bash scripts/events.sh --action account-events --account <ADDR> --limit 10

# Emulate
bash scripts/events.sh --action emulate --boc <BASE64>
```

### traces.sh
Full execution traces.
```bash
# Trace by ID or tx hash
bash scripts/traces.sh --action get --trace-id <ID>

# Emulate trace
bash scripts/traces.sh --action emulate --boc <BASE64> --ignore-signature
```

### staking.sh
Staking pools and nominators.
```bash
# All pools
bash scripts/staking.sh --action pools

# Pool info
bash scripts/staking.sh --action pool --account <POOL_ADDR>

# Nominator's pools
bash scripts/staking.sh --action nominator-pools --account <ADDR>
```

### rates.sh
Token prices and charts.
```bash
# TON price
bash scripts/rates.sh --action get --tokens ton --currencies usd,eur

# Jetton price
bash scripts/rates.sh --action get --tokens <JETTON_ADDR> --currencies usd

# Price chart
bash scripts/rates.sh --action chart --token ton --currency usd --points 100

# Markets
bash scripts/rates.sh --action markets
```

### wallet.sh
Wallet operations and TonConnect.
```bash
# Wallet info
bash scripts/wallet.sh --action get --account <ADDR>

# Seqno
bash scripts/wallet.sh --action seqno --account <ADDR>

# Wallets by pubkey
bash scripts/wallet.sh --action by-pubkey --pubkey <HEX>

# Emulate wallet message
bash scripts/wallet.sh --action emulate --boc <BASE64>
```

### gasless.sh
Gasless (fee-free) transactions.
```bash
# Gasless config
bash scripts/gasless.sh --action config

# Estimate
bash scripts/gasless.sh --action estimate --master <JETTON_ADDR> \
  --wallet <WALLET_ADDR> --pubkey <HEX> --boc <HEX_MSG>

# Send
bash scripts/gasless.sh --action send --pubkey <HEX> --boc <BASE64>
```

### multisig.sh
Multisig wallets.
```bash
bash scripts/multisig.sh --action get --account <ADDR>
bash scripts/multisig.sh --action order --account <ORDER_ADDR>
```

### liteserver.sh
Raw Lite Server proxy (low-level).
```bash
bash scripts/liteserver.sh --action masterchain-info
bash scripts/liteserver.sh --action account-state --account <ADDR>
bash scripts/liteserver.sh --action time
```

### streaming.sh
SSE real-time streaming.
```bash
# Stream all transactions
bash scripts/streaming.sh --action transactions --accounts ALL

# Stream specific accounts
bash scripts/streaming.sh --action transactions --accounts <ADDR1>,<ADDR2>

# Stream blocks
bash scripts/streaming.sh --action blocks --workchain -1

# Stream mempool
bash scripts/streaming.sh --action mempool
```

### webhooks.sh
Webhook management (rt.tonapi.io).
```bash
# Create webhook
bash scripts/webhooks.sh --action create --endpoint https://your-server.com/webhook

# List webhooks
bash scripts/webhooks.sh --action list

# Subscribe to account transactions
bash scripts/webhooks.sh --action subscribe-tx --webhook-id <ID> --accounts <ADDR1>,<ADDR2>

# Subscribe to opcode
bash scripts/webhooks.sh --action subscribe-opcode --webhook-id <ID> --opcode 0x0524c7ae

# Delete webhook
bash scripts/webhooks.sh --action delete --webhook-id <ID>
```

### utilities.sh
Service status and address parsing.
```bash
# Service status
bash scripts/utilities.sh --action status

# Parse address (all formats)
bash scripts/utilities.sh --action parse-address --address <ADDR>
```

## Key Concepts

| Concept | Description |
|---------|-------------|
| **nanoTON** | 1 TON = 10^9 nanoTON. All amounts in nanoTON |
| **Addresses** | Raw (`0:hex`) or base64url (EQ.../UQ...). Use `utilities.sh parse-address` to convert |
| **BOC** | Bag of Cells — binary TON serialization, base64-encoded |
| **Logical Time (lt)** | Transaction ordering, used for cursor pagination |
| **Events** | High-level human-readable actions (display only, structure may change) |
| **Traces** | Full execution trees of transactions |

## Rate Limits

| Condition | Limit |
|-----------|-------|
| Without API key | 0.25 RPS (1 req / 4 sec) |
| With API key | Per plan (see [pricing](https://tonconsole.com/tonapi/pricing)) |
| Testnet + mainnet | Shared limits |

## Detailed Reference

Full endpoint list with schemas, params, and response formats:
[references/api-reference.md](references/api-reference.md)
