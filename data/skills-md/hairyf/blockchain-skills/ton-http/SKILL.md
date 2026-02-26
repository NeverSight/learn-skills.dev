---
name: ton-http
description: TON HTTP API (TON Center / ton-http-api) — accounts, transactions, messages, send, runGetMethod; use Swagger for request/response parameters and return values.
metadata:
  author: Hairy
  version: "2026.2.25"
  source: Generated from sources/ton-http (toncenter/ton-http-api) and TON Index v3 Swagger
---

> Based on **ton-http-api** (sources/ton-http) and **TON Index (Go) v3**. For **request parameters and return values** of any endpoint, use [Swagger UI](https://toncenter.com/api/v3/index.html#/) or [OpenAPI doc.json](https://toncenter.com/api/v3/doc.json).

TON nodes use ADNL binary transport; an HTTP API is an intermediary that accepts HTTP and talks to TON lite servers (via tonlib). Use the public [toncenter.com](https://toncenter.com) or run your own instance from the [ton-http-api](https://github.com/toncenter/ton-http-api) repo. TON Index v3 (at toncenter.com) adds indexed REST APIs (accounts, actions, jettons, NFTs, etc.) on top of stored chain data.

## Looking up endpoint parameters and return values

- **Swagger UI (recommended):** [https://toncenter.com/api/v3/index.html#/](https://toncenter.com/api/v3/index.html#/) — browse by group, inspect query/body and response schemas.
- **OpenAPI JSON:** [https://toncenter.com/api/v3/doc.json](https://toncenter.com/api/v3/doc.json) — full machine-readable spec for parameters and models.

When calling or wrapping TON Center APIs, consult the above to confirm query/body parameters and response shapes.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| API groups and Swagger | Group list, base URL, where to look up params and return values | [core-api-overview](references/core-api-overview.md) |
| Deployment and configuration | Run locally or with Docker; webserver, tonlib, and cache env vars | [core-deployment-config](references/core-deployment-config.md) |

## API groups (quick reference)

### From ton-http-api (sources/ton-http)

| Tag | Description | Example endpoints |
|-----|-------------|------------------|
| **accounts** | Address info, wallet, balance, state, transactions, pack/unpack, token data | `GET /getAddressInformation`, `GET /getWalletInformation`, `GET /getTransactions`, `GET /getAddressBalance`, `GET /getAddressState`, `GET /packAddress`, `GET /unpackAddress`, `GET /getTokenData`, `GET /detectAddress` |
| **blocks** | Masterchain, shards, block lookup, block transactions, block header | `GET /getMasterchainInfo`, `GET /shards`, `GET /lookupBlock`, `GET /getBlockTransactions`, `GET /getBlockHeader`, `GET /getShardBlockProof`, `GET /getConsensusBlock` |
| **transactions** | Locate transactions by message | `GET /tryLocateTx`, `GET /tryLocateResultTx`, `GET /tryLocateSourceTx` |
| **get config** | Config param, libraries | `GET /getConfigParam`, `GET /getLibraries` |
| **run method** | Run get-method on contract | `POST /runGetMethod` |
| **send** | Send BOC/query, estimate fee | `POST /sendBoc`, `POST /sendBocReturnHash`, `POST /sendQuery`, `POST /estimateFee` |
| **json rpc** | All methods via JSON-RPC | `POST /jsonRPC` |

### From TON Index v3 (toncenter.com)

| Group | Description | Example endpoints |
|-------|-------------|------------------|
| **accounts** | Account states, address book, metadata, wallet states | `/api/v3/accountStates`, `/api/v3/addressBook`, `/api/v3/metadata`, `/api/v3/walletStates` |
| **actions** | Actions and traces | `/api/v3/actions`, `/api/v3/traces`, `/api/v3/pendingActions`, `/api/v3/pendingTraces` |
| **api/v2** | Address info, estimate fee, send message, runGetMethod, wallet info | `/api/v3/addressInformation`, `POST /api/v3/estimateFee`, `POST /api/v3/message`, `POST /api/v3/runGetMethod`, `/api/v3/walletInformation` |
| **blockchain** | Blocks, transactions, messages, masterchain | `/api/v3/blocks`, `/api/v3/transactions`, `/api/v3/messages`, `/api/v3/masterchainInfo`, etc. |
| **utils** | Decode | `GET/POST /api/v3/decode` |
| **dns** | TON DNS | `GET /api/v3/dns/records` |
| **jettons** | Jetton masters, wallets, transfers, burns | `/api/v3/jetton/masters`, `/api/v3/jetton/wallets`, `/api/v3/jetton/transfers`, `/api/v3/jetton/burns` |
| **multisig** | Multisig wallets and orders | `/api/v3/multisig/wallets`, `/api/v3/multisig/orders` |
| **nfts** | NFT collections, items, transfers | `/api/v3/nft/collections`, `/api/v3/nft/items`, `/api/v3/nft/transfers` |
| **stats** | Top accounts by balance | `/api/v3/topAccountsByBalance` |
| **vesting** | Vesting contracts | `/api/v3/vesting` |

## External links

- [TON Index (Go) Swagger UI](https://toncenter.com/api/v3/index.html#/)
- [OpenAPI doc.json](https://toncenter.com/api/v3/doc.json)
- [ton-http-api (GitHub)](https://github.com/toncenter/ton-http-api)
