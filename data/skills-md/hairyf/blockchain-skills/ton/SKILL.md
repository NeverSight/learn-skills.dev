---
name: ton
description: TON Blockchain — addresses, messages, TVM, cells, Blueprint, contracts, payments, API.
metadata:
  author: Hairy
  version: "2026.2.9"
  source: Generated from https://github.com/ton-org/docs, scripts located at https://github.com/antfu/skills
---

> Skill is based on TON documentation (ton-org/docs), generated at 2026-02-09.

TON (The Open Network) is a decentralized blockchain with an Actor model (all entities are smart contracts), stack-based TVM, and cell-based serialization. This skill covers foundations, contract development with Blueprint, payments, and API access.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Addresses | Internal/external addresses, workchains, account ID | [core-addresses](references/core-addresses.md) |
| Messages | Message types, StateInit, deploy, transactions | [core-messages](references/core-messages.md) |
| Cells & serialization | Cells, BOC, builders and slices | [core-cells-serialization](references/core-cells-serialization.md) |
| TVM | Stack, data types, gas, instructions, get methods | [core-tvm](references/core-tvm.md) |
| TVM exit codes | Compute/action phase codes, testing | [core-tvm-exit-codes](references/core-tvm-exit-codes.md) |
| Fees & status | Storage/compute/forward fees, account status (nonexist, uninit, active, frozen) | [core-fees-status](references/core-fees-status.md) |
| TVM registers | c0–c7, c4/c5 durable, c7 environment | [core-tvm-registers](references/core-tvm-registers.md) |

## Features

### Development

| Topic | Description | Reference |
|-------|-------------|-----------|
| Blueprint | create-ton, Sandbox, project structure | [features-blueprint](references/features-blueprint.md) |
| Contract development | First contract, storage, messages, get methods, Tolk | [features-contract-development](references/features-contract-development.md) |
| Tolk language | Types, message handling, lazy loading, IDE | [features-tolk](references/features-tolk.md) |
| Contract upgrades | setCodePostponed, setData, delayed and hot upgrades | [features-upgrades](references/features-upgrades.md) |
| Standard wallets | V4, V5, Highload, comparison, use cases | [features-wallets](references/features-wallets.md) |
| Standard tokens | Jettons, NFTs, transfer, mint, burn, discovery | [features-tokens](references/features-tokens.md) |
| Signing | Ed25519, wallet/gasless/server patterns, TypeScript | [features-signing](references/features-signing.md) |

### Payments & API

| Topic | Description | Reference |
|-------|-------------|-----------|
| Payments | Toncoin, Jettons, finality, monitoring | [features-payments](references/features-payments.md) |
| API | Liteservers, TON Center, TonAPI, dTON | [features-api](references/features-api.md) |

## Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Security | Integers, replay, accept_message, gas, random, front-running | [best-practices-security](references/best-practices-security.md) |
