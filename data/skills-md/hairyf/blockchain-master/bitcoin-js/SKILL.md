---
name: bitcoin-js
description: JavaScript/TypeScript Bitcoin library — payments, addresses, PSBT, transactions, script.
metadata:
  author: Hairy
  version: "2026.2.9"
  source: Generated from https://github.com/bitcoinjs/bitcoinjs-lib
---

> Skill based on bitcoinjs-lib v7.x, generated 2026-02-09. Docs: https://bitcoinjs.github.io/bitcoinjs-lib/

bitcoinjs-lib is a client-side Bitcoin library for Node and browsers: build/sign transactions via PSBT, create addresses and payment outputs (P2PKH, P2SH, P2WPKH, P2WSH, P2TR), decode/encode addresses. Keys come from `ecpair` and `bip32`; ECC must be initialized with `initEccLib` for signing and Taproot.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Payments & Addresses | p2pkh, p2sh, p2wpkh, p2wsh, p2tr; toOutputScript / fromOutputScript | [core-payments-addresses](references/core-payments-addresses.md) |
| PSBT | Create, add I/O, sign, validate, finalize, extract transaction | [core-psbt](references/core-psbt.md) |
| Transaction & Script | Transaction parse/build, script compile/decompile, opcodes, networks | [core-transaction-script](references/core-transaction-script.md) |

## Features

### Networks & ECC

| Topic | Description | Reference |
|-------|-------------|-----------|
| Networks, ECC, Keys | bitcoin/testnet/regtest, initEccLib, ecpair, bip32, bip39 | [features-networks-ecc](references/features-networks-ecc.md) |

## Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Security | RNG, no address reuse, no xpub sharing, verify before broadcast | [best-practices-security](references/best-practices-security.md) |

## External Links

- [bitcoinjs-lib docs](https://bitcoinjs.github.io/bitcoinjs-lib/)
- [bitcoinjs/bitcoinjs-lib GitHub](https://github.com/bitcoinjs/bitcoinjs-lib)
