---
name: coinstats-currencies
description: CoinStats supported currency listing. Use when you need the public currencies list for display or normalization.
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

# CoinStats Currencies

## Auth Setup

```bash
export COINSTATS_API_KEY=<key>
coinstats whoami
```

## Commands

```bash
coinstats currencies list --pretty
```
