---
name: pionex-earn-arbitrage
description: >
  Use when the user asks about Pionex Earn Arbitrage (InstFund):
  fetching available arbitrage products, querying user balances,
  staking (investing) into a product, or unstaking (withdrawing) from a product.
  Do NOT use for Dual Investment (pionex-earn-dual), spot trading (pionex-trade),
  futures grid bots (pionex-bot), or market data only (pionex-market).
license: MIT
metadata:
  author: pionex
  version: "1.0.0"
  homepage: "https://www.pionex.com"
  agent:
    requires:
      bins: ["pionex-trade-cli"]
    install:
      - id: npm
        kind: node
        package: "@pionex/pionex-ai-kit"
        bins: ["pionex-trade-cli", "pionex-ai-kit"]
        label: "Install pionex CLI (npm)"
---

# Pionex Earn Arbitrage Skill

Arbitrage (InstFund) products on Pionex: browse products, query user balances, stake into a product, and unstake from a product via `pionex-trade-cli`. Read operations require **Enable reading** permission; write operations require **Earn** permission.

> **Invite Only:** The Earn Arbitrage API is currently invite-only and only available to onboarded institutional users. Contact your BD representative or [open@pionex.com](mailto:open@pionex.com) to request access.

## Skill Routing

- Arbitrage products, balances, stake, unstake → **pionex-earn-arbitrage** (this skill)
- Dual Investment products, prices, invest, revoke, collect → **pionex-earn-dual**
- Spot market data (depth, tickers, klines) → **pionex-market**
- Spot account balance → **pionex-portfolio**
- Spot order placement/cancellation → **pionex-trade**
- Futures Grid Bot lifecycle → **pionex-bot**

## Prerequisites

1. Install CLI:
   ```bash
   npm install -g @pionex/pionex-ai-kit
   ```
2. Configure credentials:
   ```bash
   pionex-ai-kit onboard
   ```
   Ensure your API key has the required permissions:
   - **Enable reading** — for `fetchProducts`, `fetchUserBalances`
   - **Earn** — for `stake`, `unStake`

---

## API Endpoints

| # | Method | Path | Permission | Description |
|---|--------|------|------------|-------------|
| 1 | GET | `/api/v1/earn/arbitrage/fetchProducts` | Enable reading | List available arbitrage products |
| 2 | GET | `/api/v1/earn/arbitrage/fetchUserBalances` | Enable reading | Query user arbitrage balances |
| 3 | POST | `/api/v1/earn/arbitrage/stake` | Earn | Stake (invest) into an arbitrage product |
| 4 | POST | `/api/v1/earn/arbitrage/unStake` | Earn | Unstake (withdraw) from an arbitrage product |

---

## Command Index

### Public-with-auth Commands (Enable reading permission)

| # | Command | Flags | Type |
|---|---------|-------|------|
| 1 | `pionex-trade-cli earn arbitrage fetchProducts` | `[--coin <currency>] [--visibility <v>]` | READ |
| 2 | `pionex-trade-cli earn arbitrage fetchUserBalances` | `[--business-type <n>]` | READ |

### Private Commands — Earn permission

| # | Command | Flags | Type |
|---|---------|-------|------|
| 3 | `pionex-trade-cli earn arbitrage stake` | `--amount <n> --coin <c> --product-id <id> [--unique-id <id>]` | WRITE |
| 4 | `pionex-trade-cli earn arbitrage unStake` | `--amount <n> --coin <c> --product-id <id> [--unique-id <id>] [--unstake-id <id>]` | WRITE |

---

## Safety Rules

1. **Dry-run first, confirm before real execution** — For `stake` and `unStake`, always run with `--dry-run`, show output to user, then confirm before running without it.
2. **Never infer `--product-id`** — Must come from the API (`fetchProducts`), never assumed.
3. **Never infer `--unique-id`** — Propose one and get user confirmation. It acts as an idempotency key.
4. **Check balance before unstaking** — Use `fetchUserBalances` to verify the position exists before calling `unStake`.

---

## Stake Workflow (Mandatory 2-Step Process)

### Step 1: Get available products

```bash
# List all available arbitrage products
pionex-trade-cli earn arbitrage fetchProducts

# Filter by coin
pionex-trade-cli earn arbitrage fetchProducts --coin USDT
```

Choose a `productId` from the response.

### Step 2: Dry-run, confirm, then submit

```bash
# Dry-run first — shows the request payload without executing
pionex-trade-cli earn arbitrage stake \
  --coin USDT \
  --product-id <productId> \
  --amount 100 \
  --unique-id my-stake-001 \
  --dry-run

# After user confirmation, submit (same command without --dry-run)
pionex-trade-cli earn arbitrage stake \
  --coin USDT \
  --product-id <productId> \
  --amount 100 \
  --unique-id my-stake-001
```

---

## Examples

### Browse products

```bash
# All available arbitrage products
pionex-trade-cli earn arbitrage fetchProducts

# Filter by coin
pionex-trade-cli earn arbitrage fetchProducts --coin USDT
```

### Query user balances

```bash
# All arbitrage balances
pionex-trade-cli earn arbitrage fetchUserBalances
```

### Stake

```bash
# 1. Get products
pionex-trade-cli earn arbitrage fetchProducts --coin USDT

# 2. Dry-run stake
pionex-trade-cli earn arbitrage stake \
  --coin USDT \
  --product-id <productId> \
  --amount 100 \
  --unique-id my-stake-001 \
  --dry-run

# 3. Execute after user confirmation
pionex-trade-cli earn arbitrage stake \
  --coin USDT \
  --product-id <productId> \
  --amount 100 \
  --unique-id my-stake-001
```

### Unstake

```bash
# 1. Verify balance exists
pionex-trade-cli earn arbitrage fetchUserBalances

# 2. Dry-run unstake
pionex-trade-cli earn arbitrage unStake \
  --coin USDT \
  --product-id <productId> \
  --amount 100 \
  --unique-id my-stake-001 \
  --dry-run

# 3. Execute after user confirmation
pionex-trade-cli earn arbitrage unStake \
  --coin USDT \
  --product-id <productId> \
  --amount 100 \
  --unique-id my-stake-001
```
