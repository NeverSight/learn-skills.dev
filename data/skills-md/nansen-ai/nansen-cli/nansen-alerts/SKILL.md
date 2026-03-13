---
name: nansen-alerts
description: Manage smart alerts — list, create, update, toggle, delete. Use when setting up or managing token flow alerts, smart money alerts, or notification rules.
metadata:
  openclaw:
    requires:
      env:
        - NANSEN_API_KEY
      bins:
        - nansen
    primaryEnv: NANSEN_API_KEY
    install:
      - kind: node
        package: nansen-cli
        bins: [nansen]
allowed-tools: Bash(nansen:*)
---

# Smart Alerts

CRUD management for smart alerts. Alerts are internal-only (requires Nansen internal API key).

## Quick Reference

```bash
nansen alerts list --table
nansen alerts create --name <name> --type <type> --chains <chains> --telegram <chatId>
nansen alerts update <id> [--name <name>] [--chains <chains>]
nansen alerts toggle <id> --enabled|--disabled
nansen alerts delete <id>
```

## Options Reference

| Flag | Create | Update | Toggle | Delete |
|------|--------|--------|--------|--------|
| `<id>` (positional) | | required | required | required |
| `--name` | required | optional | | |
| `--type` | required | required with type-specific flags | | |
| `--chains` | recommended | optional | | |
| `--telegram` | chat ID | optional | | |
| `--slack` | webhook URL | optional | | |
| `--discord` | webhook URL | optional | | |
| `--description` | optional | optional | | |
| `--enabled` | | flag | flag | |
| `--disabled` | flag | flag | flag | |
| `--data` | optional (JSON escape hatch) | optional | | |

## Alert Types

### 1. `sm-token-flows` — Smart Money Token Flows

Track aggregated SM inflow/outflow. At least one flow threshold should be specified.

**Type-specific flags:**
- `--inflow-1h-min/max`, `--inflow-1d-min/max`, `--inflow-7d-min/max` (USD thresholds)
- `--outflow-1h-min/max`, `--outflow-1d-min/max`, `--outflow-7d-min/max`
- `--netflow-1h-min/max`, `--netflow-1d-min/max`, `--netflow-7d-min/max`
- `--token <address:chain>` (repeatable) — include specific tokens
- `--exclude-token <address:chain>` (repeatable)
- `--token-sector <name>` / `--exclude-token-sector <name>` (repeatable)
- `--token-age-max <days>`
- `--market-cap-min/max <usd>`, `--fdv-min/max <usd>`

**Example:**
```bash
nansen alerts create \
  --name 'SM ETH Inflow >5M' \
  --type sm-token-flows \
  --chains ethereum \
  --telegram 5238612255 \
  --inflow-1h-min 5000000 \
  --token 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2:ethereum
```

### 2. `common-token-transfer` — Token Transfer Events

Track real-time transfer events matching specified criteria.

**Subject types:** `address`, `entity`, `label`, `custom-label`
Format: `--subject type:value` (e.g. `--subject label:"Centralized Exchange"`)

**Type-specific flags:**
- `--events <buy,sell,swap,send,receive>` (comma-separated)
- `--usd-min/max <usd>`, `--token-amount-min/max <n>`
- `--subject <type:value>` (repeatable) — addresses/entities/labels to track
- `--counterparty <type:value>` (repeatable) — requires `--subject`
- `--token <address:chain>` / `--exclude-token <address:chain>` (repeatable)
- `--token-sector <name>` / `--exclude-token-sector <name>` (repeatable)
- `--token-age-min/max <days>`, `--market-cap-min/max <usd>`
- `--exclude-from <type:value>` / `--exclude-to <type:value>` (repeatable)

**Event direction notes:**
- `buy` for counterparties = `sell` for subjects
- `send` for counterparties = `receive` for subjects
- To track "any address sending to CEX": use `--subject` with `receive`, not `--counterparty` with `send`

**Example:**
```bash
nansen alerts create \
  --name 'Large USDC Transfers' \
  --type common-token-transfer \
  --chains ethereum \
  --telegram 123456789 \
  --events send,receive \
  --usd-min 1000000 \
  --token 0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48:ethereum
```

### 3. `smart-contract-call` — Smart Contract Interactions

Track contract calls matching specified criteria.

**Type-specific flags:**
- `--usd-min/max <usd>`
- `--signature-hash <hash>` (repeatable, e.g. `0x095ea7b3` for `approve`)
- `--caller <type:value>` / `--exclude-caller <type:value>` (repeatable)
- `--contract <type:value>` / `--exclude-contract <type:value>` (repeatable)

**Example:**
```bash
nansen alerts create \
  --name 'Uniswap V3 Large Swaps' \
  --type smart-contract-call \
  --chains ethereum \
  --telegram 123456789 \
  --usd-min 1000000 \
  --contract entity:"Uniswap V3"
```

## Notes

- Chain aliases: Hyperliquid = `hyperevm`, BSC = `bnb`.
- Multiple channels can be combined: `--telegram 123 --slack https://...`
- `--data '<json>'` merges raw JSON on top of named flags (escape hatch for fields without named flags).
- Alert endpoints are internal-only. Non-internal users receive 404.
- Use single quotes for names with `$` or special characters: `--name 'SM >$1M'`
