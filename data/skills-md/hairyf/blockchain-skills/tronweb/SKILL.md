---
name: tronweb
description: TronWeb — JavaScript/TypeScript SDK for TRON (HTTP API, contracts, transactions, events).
metadata:
  author: Hairy
  version: "2026.1.1"
  source: Generated from https://github.com/tronprotocol/tronweb, scripts located at https://github.com/antfu/skills
---

> Skill is based on TronWeb v6.2.0, generated at 2026-02-25.

TronWeb is the official JavaScript/TypeScript SDK for the TRON network. It wraps the TRON HTTP API and provides a consistent API for accounts, blocks, transactions, smart contracts, and events. Use it in Node.js or the browser to build DApps, sign and broadcast transactions, and call contracts.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Instance setup | fullHost, nodes, headers, privateKey, setPrivateKey/setAddress | [core-instance-setup](references/core-instance-setup.md) |
| Address, units, encoding | hex/base58/checksum, toSun/fromSun, fromUtf8/toUtf8, sha3 | [core-address-units](references/core-address-units.md) |
| Trx | Blocks, transactions, accounts, bandwidth, sign, broadcast, getCurrentRefBlockParams, signTypedData, ecRecover | [core-trx](references/core-trx.md) |
| Utils | ABI, transaction, deserializeTx, accounts, address, validations | [core-utils](references/core-utils.md) |
| Providers | HttpProvider, request, isConnected, timeout, headers, setStatusPage | [core-providers](references/core-providers.md) |
| Constants | ADDRESS_PREFIX, SUN/TRX, default feeLimit, BIP44 path | [core-constants](references/core-constants.md) |

## Features

### Transactions and contracts

| Topic | Description | Reference |
|-------|-------------|-----------|
| TransactionBuilder | sendTrx, sendToken, freeze/unfreeze, triggerSmartContract, createSmartContract, deployConstantContract | [features-transaction-builder](references/features-transaction-builder.md) |
| Contract | contract(abi, address), methods.call/send, decodeInput, new(), at() | [features-contract](references/features-contract.md) |
| Events | getEventsByContractAddress, getEventsByTransactionID, getEventsByBlockNumber, setServer | [features-events](references/features-events.md) |
| Plugin | register(PluginClass), pluginInterface (requires, components, fullClass) | [features-plugin](references/features-plugin.md) |
| Message and typed data | signMessage/verifyMessage, signTypedData/verifyTypedData, EIP-712 TypedDataEncoder | [features-message-typed-data](references/features-message-typed-data.md) |
| Connection and version | isConnected(), fullnodeSatisfies(version), getFullnodeVersion() | [features-connection-version](references/features-connection-version.md) |
| Trx tokens and chain | getTokenFromID, getTokensIssuedByAddress, getAccountResources, getChainParameters | [features-trx-tokens-resources](references/features-trx-tokens-resources.md) |

### Best practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Errors and typing | Error instances (e.message), ABI as const for contract inference | [best-practices-errors-typing](references/best-practices-errors-typing.md) |
| Param validation | Validator, notValid(params), param types (address, integer, resource, url, hex, etc.) | [best-practices-param-validation](references/best-practices-param-validation.md) |
| Multi-signature | getSignWeight, getApprovedList, multiSign, permissionId | [best-practices-multisig](references/best-practices-multisig.md) |
| Transaction lifecycle | Sign → broadcast → getTransactionInfo, handling receipt and FAILED | [best-practices-transaction-lifecycle](references/best-practices-transaction-lifecycle.md) |
