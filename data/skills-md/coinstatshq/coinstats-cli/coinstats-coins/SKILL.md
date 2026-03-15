---
name: coinstats-coins
description: CoinStats coin market data. Use when listing coins, looking up a coin by id, or fetching coin charts and prices.
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

# CoinStats Coins

## Auth Setup

```bash
export COINSTATS_API_KEY=<key>
coinstats whoami
```

## Commands

```bash
coinstats coins list --limit 10 --pretty
coinstats coins by-id --coin-id bitcoin --currency USD
coinstats coins chart-by-id --coin-id bitcoin --period 1w
coinstats coins avg-price --coin-id bitcoin --date 2025-01-01
coinstats coins exchange-price --coin-id bitcoin --exchange binance
```
