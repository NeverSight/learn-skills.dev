---
name: bitcoin
description: Bitcoin Core — full node, JSON-RPC, REST, descriptors, PSBT, wallets, and external signers.
metadata:
  author: hairy
  version: "2026.2.9"
  source: Generated from https://github.com/bitcoin/bitcoin (doc/)
---

> Skill based on Bitcoin Core, generated 2026-02-09. Docs: `sources/bitcoin/doc/`, [bitcoincore.org](https://bitcoincore.org/en/doc/)

Bitcoin Core is the reference Bitcoin full-node implementation. It syncs and validates the chain, runs a headless daemon or GUI, and exposes JSON-RPC and REST. It supports descriptor wallets, PSBT (multisig/hardware wallets), and external signers.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Overview | Executables (bitcoind, bitcoin-qt, bitcoin, bitcoin-cli), flows | [core-overview](references/core-overview.md) |
| Config | bitcoin.conf, precedence, locations | [core-config](references/core-config.md) |
| CLI | bitcoin-cli, bitcoin rpc, -rpcwallet | [core-cli](references/core-cli.md) |
| JSON-RPC | Endpoints, params, versioning, security | [core-rpc](references/core-rpc.md) |
| Build | CMake build (Unix), options, ZMQ | [core-build](references/core-build.md) |

## Features

### Wallets and Signing

| Topic | Description | Reference |
|-------|-------------|-----------|
| Descriptors | Output descriptor language and RPCs | [features-descriptors](references/features-descriptors.md) |
| PSBT | Partially Signed Bitcoin Transactions, RPCs, workflow | [features-psbt](references/features-psbt.md) |
| Wallets | Create, encrypt, backup, descriptor vs legacy | [features-wallets](references/features-wallets.md) |
| External signer | Hardware wallet, -signer, Signer API | [features-external-signer](references/features-external-signer.md) |

### APIs

| Topic | Description | Reference |
|-------|-------------|-----------|
| REST and ZMQ | REST endpoints, ZMQ notifications | [features-rest-zmq](references/features-rest-zmq.md) |

## External Links

- [Bitcoin Core docs](https://bitcoincore.org/en/doc/)
- [Bitcoin Core GitHub](https://github.com/bitcoin/bitcoin)
- [BIPs](https://github.com/bitcoin/bips)
