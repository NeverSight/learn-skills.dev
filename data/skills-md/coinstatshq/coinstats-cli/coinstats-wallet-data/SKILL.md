---
name: coinstats-wallet-data
description: CoinStats wallet tracking and wallet sync commands. Use when checking balances, transactions, charts, and DeFi exposure for wallets.
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

# CoinStats Wallet Data

## Auth Setup

```bash
export COINSTATS_API_KEY=<key>
coinstats whoami
```

## Commands

```bash
coinstats wallet blockchains
coinstats wallet balance --address <wallet> --blockchain ethereum
coinstats wallet transactions --address <wallet> --blockchain ethereum
coinstats wallet chart --address <wallet> --blockchain ethereum --type 24h
coinstats wallet sync-transactions --blockchain ethereum --body-file ./wallet-sync.json --yes
```
