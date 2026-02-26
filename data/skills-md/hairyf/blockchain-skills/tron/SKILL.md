---
name: tron
description: TRON (java-tron) - account model, DPoS, resources, system contracts, TVM, TRC-10/TRC-20, DEX, APIs, events, TronGrid.
metadata:
  author: Hairy
  version: 2026.2.25
  source: Generated from https://github.com/tronprotocol/documentation-en
---

> Skill based on TRON documentation (tronprotocol/documentation-en), generated 2026-02-25.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Account model | Address, EOA vs contract, activation, signing | [core-account](references/core-account.md) |
| Account permissions | Owner, witness, active; multi-sig; AccountPermissionUpdateContract | [core-account-permissions](references/core-account-permissions.md) |
| Resource model | Bandwidth, Energy, TP; staking, fee_limit, delegation | [core-resource-model](references/core-resource-model.md) |
| DPoS | Super Representatives, voting, slots, epochs | [core-dpos](references/core-dpos.md) |
| SR and Committee | Election, brokerage, block/vote rewards, proposals | [core-sr-committee](references/core-sr-committee.md) |
| System contracts | Transaction types and HTTP/gRPC APIs | [core-system-contracts](references/core-system-contracts.md) |
| TVM | EVM compatibility, Bandwidth vs Energy, deploy/trigger | [core-tvm](references/core-tvm.md) |
| Tokens TRC-10/TRC-20 | Native vs contract; issue, transfer, query | [core-tokens-tr10-tr20](references/core-tokens-tr10-tr20.md) |
| DEX | Native trading pairs (Bancor), create/trade/inject/withdraw | [core-dex](references/core-dex.md) |

## Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| HTTP wallet APIs | Accounts, transactions, broadcast, resources, voting | [features-http-wallet](references/features-http-wallet.md) |
| gRPC and JSON-RPC | When to use each; eth_* compatibility, buildTransaction | [features-api-grpc-jsonrpc](references/features-api-grpc-jsonrpc.md) |
| Smart contracts | Constant vs inconstant, delegate call, CREATE | [features-smart-contracts](references/features-smart-contracts.md) |
| Event subscription | Plugin vs ZeroMQ; types, filtering, historical sync | [features-events](references/features-events.md) |
| TronGrid | Hosted API - FullNode proxy and v1 REST | [features-trongrid](references/features-trongrid.md) |
| Developer tools | TronIDE, TronBox, TronWeb, Trident | [features-tools](references/features-tools.md) |
| wallet-cli | CLI for signing, broadcasting, querying via gRPC | [features-wallet-cli](references/features-wallet-cli.md) |
| Node deployment and ops | Deploy, upgrade, private network, lite fullnode, backup, metrics | [features-node-ops](references/features-node-ops.md) |

## Best practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Upgrade and verify | Upgrade steps; JAR signature verification for integrity | [best-practices-upgrade-verify](references/best-practices-upgrade-verify.md) |
