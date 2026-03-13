---
name: coinstats-news
description: CoinStats crypto news commands. Use when browsing news feeds, source lists, typed feeds, or a specific news item.
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

# CoinStats News

## Auth Setup

```bash
export COINSTATS_API_KEY=<key>
coinstats whoami
```

## Commands

```bash
coinstats news sources
coinstats news list --page 1
coinstats news by-type --type bullish
coinstats news by-id --id <news-id>
```
