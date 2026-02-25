---
name: metaplex
description: Metaplex development on Solana — NFTs, tokens, compressed NFTs, candy machines, token launches. Use when working with Token Metadata, Core, Bubblegum, Candy Machine, Genesis, or the mplx CLI.
license: Apache-2.0
metadata:
  author: metaplex-foundation
  version: "0.1.0"
  openclaw: {"emoji":"💎","os":["darwin","linux","win32"],"requires":{"bins":["node"]},"homepage":"https://developers.metaplex.com"}
---

# Metaplex Development Skill

## Overview

Metaplex provides the standard infrastructure for NFTs and tokens on Solana:
- **Core**: Next-gen NFT standard (recommended for new NFT projects)
- **Token Metadata**: Fungible tokens + legacy NFTs/pNFTs
- **Bubblegum**: Compressed NFTs (cNFTs) using Merkle trees — massive scale at minimal cost
- **Candy Machine**: NFT drops with configurable minting rules
- **Genesis**: Token launch protocol with fair distribution + liquidity graduation

## Tool Selection

> **Prefer CLI over SDK** for direct execution. Use SDK only when user specifically needs code.

| Approach | When to Use |
|----------|-------------|
| **CLI (`mplx`)** | Default choice - direct execution, no code needed |
| **Umi SDK** | User needs code — default SDK choice. Covers all programs (TM, Core, Bubblegum, Genesis) |
| **Kit SDK** | User specifically uses @solana/kit, or asks for minimal dependencies. Token Metadata only — no Core/Bubblegum/Genesis support |

## Task Router

> **IMPORTANT**: You MUST read the detail file for your task BEFORE executing any command or writing any code. The command syntax, required flags, setup steps, and batching rules are ONLY in the detail files. Do NOT guess commands from memory.

| Task Type | Read This File |
|-----------|----------------|
| Any CLI operation (shared setup) | `./references/cli.md` |
| CLI: Core NFTs/Collections | `./references/cli.md` + `./references/cli-core.md` |
| CLI: Token Metadata NFTs | `./references/cli.md` + `./references/cli-token-metadata.md` |
| CLI: Compressed NFTs (Bubblegum) | `./references/cli.md` + `./references/cli-bubblegum.md` |
| CLI: Candy Machine (NFT drops) | `./references/cli.md` + `./references/cli-candy-machine.md` |
| CLI: Token launch (Genesis) | `./references/cli.md` + `./references/cli-genesis.md` |
| CLI: Fungible tokens | `./references/cli.md` (toolbox section) |
| SDK setup (Umi) | `./references/sdk-umi.md` |
| SDK: Core NFTs | `./references/sdk-umi.md` + `./references/sdk-core.md` |
| SDK: Token Metadata | `./references/sdk-umi.md` + `./references/sdk-token-metadata.md` |
| SDK: Compressed NFTs (Bubblegum) | `./references/sdk-umi.md` + `./references/sdk-bubblegum.md` |
| SDK: Token Metadata with Kit | `./references/sdk-token-metadata-kit.md` |
| SDK: Token launch (Genesis) | `./references/sdk-umi.md` + `./references/sdk-genesis.md` |
| Account structures, PDAs, concepts | `./references/concepts.md` |

## CLI Capabilities

The `mplx` CLI can handle most Metaplex operations directly. **Read `./references/cli.md` for shared setup, then the program-specific file.**

| Task | CLI Support |
|------|-------------|
| Create fungible token | ✅ |
| Create Core NFT/Collection | ✅ |
| Create TM NFT/pNFT | ✅ |
| Transfer TM NFTs | ✅ |
| Transfer fungible tokens | ✅ |
| Transfer Core NFTs | ❌ SDK only |
| Upload to Irys | ✅ |
| Candy Machine drop | ✅ (setup/config/insert — minting requires SDK) |
| Compressed NFTs (cNFTs) | ✅ (batch limit ~100, use SDK for larger) |
| Check SOL balance / Airdrop | ✅ |
| Query assets by owner/collection | ❌ SDK only (DAS API) |
| Token launch (Genesis) | ✅ |

## Program IDs

```
Token Metadata:  metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s
Core:            CoREENxT6tW1HoK8ypY1SxRMZTcVPm7R94rH4PZNhX7d
Bubblegum V1:    BGUMAp9SX3uS4efGcFjPjkAQZ4cUNZhtHaMq64nrGf9D
Bubblegum V2:    BGUMAp9Gq7iTEuizy4pqaxsTyUCBK68MDfK752saRPUY
Core Candy:      CMACYFENjoBMHzapRXyo1JZkVS6EtaDDzkjMrmQLvr4J
Genesis:         GENSkbJAfXcp9nvQm9eBPMg4MUefawD4oBNK7P8aLvEC
```

## Quick Decision Guide

### NFTs: Core vs Token Metadata

| Choose | When |
|--------|------|
| **Core** | New NFT projects, lower cost (87% cheaper), plugins, royalty enforcement |
| **Token Metadata** | Existing TM collections, need editions, pNFTs for legacy compatibility |

### Compressed NFTs (Massive Scale)

Use **Bubblegum** when minting thousands+ of NFTs at minimal cost. See `./references/cli-bubblegum.md` (CLI) or `./references/sdk-bubblegum.md` (SDK).

### Fungible Tokens

Always use **Token Metadata**. Read `./references/cli.md` (toolbox section) for CLI commands.

### NFT Drops

Use **Core Candy Machine**. Read `./references/cli.md` + `./references/cli-candy-machine.md`.

### Token Launches (Token Generation Event / Fair Launch)

Use **Genesis**. Read `./references/cli.md` + `./references/cli-genesis.md` (CLI) or `./references/sdk-genesis.md` (SDK).

## External Resources

- Documentation: https://developers.metaplex.com
- Core: https://developers.metaplex.com/core
- Token Metadata: https://developers.metaplex.com/token-metadata
- Bubblegum: https://developers.metaplex.com/bubblegum-v2
- Candy Machine: https://developers.metaplex.com/core-candy-machine
- Genesis: https://developers.metaplex.com/genesis
