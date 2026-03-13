---
name: coinstats-nft
description: CoinStats NFT discovery commands. Use when browsing trending NFTs, wallet-held assets, or collection asset details.
metadata:
  openclaw:
    requires:
      env:
        - COINSTATS_API_KEY
      bins:
        - coinstats
    primaryEnv: COINSTATS_API_KEY
    install:
      - kind: node
        package: coinstats-cli
        bins: [coinstats]
allowed-tools: Bash(coinstats:*)
---

# CoinStats NFT

## Auth Setup

```bash
export COINSTATS_API_KEY=<key>
coinstats whoami
```

## Commands

```bash
coinstats nft trending
coinstats nft wallet-assets --address <wallet>
coinstats nft collection --collection-address <address>
coinstats nft collection-assets --collection-address <address>
coinstats nft asset --collection-address <address> --token-id <tokenId>
```
