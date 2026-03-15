---
name: coinstats-exchange
description: CoinStats exchange connection commands. Use when checking supported exchanges, balances, transactions, charts, and sync status.
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

# CoinStats Exchange

## Auth Setup

```bash
export COINSTATS_API_KEY=<key>
coinstats whoami
```

## Commands

```bash
coinstats exchange support
coinstats exchange status --portfolio-id <id>
coinstats exchange transactions --portfolio-id <id>
coinstats exchange balance --body-file ./exchange-balance.json
coinstats exchange sync --portfolio-id <id> --yes
```
