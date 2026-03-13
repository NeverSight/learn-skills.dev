---
name: coinstats-fiats
description: CoinStats fiat currency listing. Use when you need the supported fiat list from the public API.
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

# CoinStats Fiats

## Auth Setup

```bash
export COINSTATS_API_KEY=<key>
coinstats whoami
```

## Commands

```bash
coinstats fiats list --pretty
```
