---
name: coinstats-portfolio
description: CoinStats portfolio commands. Use when checking portfolio value, holdings, charts, transactions, sync status, or managing portfolio connections.
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

# CoinStats Portfolio

## Auth Setup

```bash
export COINSTATS_API_KEY=<key>
coinstats whoami
```

## Portfolio Identification

- Use `--portfolio-id <id>` to target a specific API-connected portfolio.
- Use `--sharetoken <token>` to read a shared portfolio. Get the share token from the CoinStats portfolio page via `Share`.
- Use `--passcode <code>` together with `--sharetoken` when the shared portfolio is protected.
- For `coinstats portfolio chart`, if you omit both `--portfolio-id` and `--sharetoken`, CoinStats returns the aggregated chart for all API-connected portfolios.

## Commands

```bash
coinstats portfolio value --portfolio-id <id>
coinstats portfolio value --sharetoken <token>
coinstats portfolio coins --sharetoken <token> --passcode <code>
coinstats portfolio chart --portfolio-id <id> --type 24h
coinstats portfolio chart --sharetoken <token> --type 24h
coinstats portfolio chart --type 24h
coinstats portfolio connect-wallet --body-file ./wallet.json --yes
coinstats portfolio add-transaction --body-file ./transaction.json --yes
coinstats portfolio sync --portfolio-id <id> --yes
coinstats portfolio delete --portfolio-id <id> --yes
```
