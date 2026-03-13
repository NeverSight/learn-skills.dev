---
name: coinstats-insights
description: CoinStats market insights commands. Use when checking BTC dominance, fear and greed, or rainbow chart data.
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

# CoinStats Insights

## Auth Setup

```bash
export COINSTATS_API_KEY=<key>
coinstats whoami
```

## Commands

```bash
coinstats insights btc-dominance --type 24h --pretty
coinstats insights fear-and-greed --pretty
coinstats insights fear-and-greed-chart --pretty
coinstats insights rainbow-chart --coin-id bitcoin --pretty
```
