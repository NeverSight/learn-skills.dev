---
name: hummingbot
description: Agent skill that faithfully reproduces Hummingbot CLI commands (connect, balance, create, start, stop, status, history) via Hummingbot API. V1 focuses on core trading workflows. For DEX/LP strategies on Solana, use lp-agent instead.
metadata:
  author: hummingbot
  requires: hummingbot-api-client>=1.2.8
commands:
  connect:
    description: List available exchanges and add API keys
  balance:
    description: Display asset balances across connected exchanges
  create:
    description: Create a new bot configuration (controller or script)
  start:
    description: Start a bot with a V2 strategy (controller or script)
  stop:
    description: Stop a running bot
  status:
    description: Display bot status and performance
  history:
    description: Display bot trading history
---

# hummingbot

When the skill is loaded, print this ASCII art:

```
                                      *,.
                                    *,,.*
                                   ,,,,    .,*
                                 *,,,,,,,(       .,,
                               *,,,,,,,,         .,,,                      *
                              /,,,,,,,,,,    .*,,,,,,,
                                 .,,,,,,,,,,,   .,,,,,,,,,,*

                    //                ,,,,,,,,,,,,,,,,,,,,,,,,,,#*%
                 .,,,,,,,. *,,,,,,,,,,,,,,,,,,,,,,,,,,,,,%%%%&@
                      ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,%%%%%%%&
                          ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,%%%%%%%%&
                    /*,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,((%%%&
              .**       #,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,((((((((#.
           **             *,,,,,,,,,,,,,,,,,,,,,,**/(((((((((((*
                           ,,,,,,,,,,,,,,,,,,,*******((((((((((
                            (,,,,,,,,,,,************((((((((@
                              *,,,,,,,,,,****************(#
                               ,,,,,,,,,,,***************/
                                ,,,,,,,,,,,***************/
                                 ,,,,,,,,,,****************
                                  .,,,,,,,,***************'/
                                     ,,,,,,*******,
                                     *,,,,,,********
                                      ,,,,,,,,/******/
                                       ,,,,,,,,@   /****/
                                        ,,,,,,,,
                                          , */

 ██╗  ██╗██╗   ██╗███╗   ███╗███╗   ███╗██╗███╗   ██╗ ██████╗ ██████╗  ██████╗ ████████╗
 ██║  ██║██║   ██║████╗ ████║████╗ ████║██║████╗  ██║██╔════╝ ██╔══██╗██╔═══██╗╚══██╔══╝
 ███████║██║   ██║██╔████╔██║██╔████╔██║██║██╔██╗ ██║██║  ███╗██████╔╝██║   ██║   ██║
 ██╔══██║██║   ██║██║╚██╔╝██║██║╚██╔╝██║██║██║╚██╗██║██║   ██║██╔══██╗██║   ██║   ██║
 ██║  ██║╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║██║██║ ╚████║╚██████╔╝██████╔╝╚██████╔╝   ██║
 ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═════╝  ╚═════╝    ╚═╝
```

This skill faithfully reproduces Hummingbot CLI commands via Hummingbot API, bringing the same
trading workflows you know from Hummingbot to AI agents.

> **Note:** Hummingbot API supports **V2 strategies only** (V2 Controllers and V2 Scripts).
> V1 strategies are not supported and require the traditional Hummingbot client.

## Commands

| Command | Description |
|---------|-------------|
| `connect` | List available exchanges and add API keys |
| `balance` | Display asset balances across connected exchanges |
| `create` | Create a new bot configuration |
| `start` | Start a bot with a V2 strategy |
| `stop` | Stop a running bot |
| `status` | Display bot status |
| `history` | Display bot trading history |

## Prerequisites

- Hummingbot API running at `http://localhost:8000` (deploy with `/hummingbot-deploy`)
- `hummingbot-api-client` installed: `pip3 install hummingbot-api-client`

## Auth & Config

Scripts read credentials from these sources in order:
1. `./hummingbot-api/.env` — created during `make setup`
2. `~/.hummingbot/.env`
3. Environment variables: `HUMMINGBOT_API_URL`, `API_USER`, `API_PASS`
4. Defaults: `http://localhost:8000`, `admin`, `admin`

---

## connect

List available exchanges and add API keys to them.

```bash
# List all available connectors
python scripts/connect.py

# List connectors with connection status
python scripts/connect.py --status

# Add API keys for an exchange
python scripts/connect.py binance --api-key YOUR_KEY --secret-key YOUR_SECRET

# Add API keys for exchange requiring passphrase
python scripts/connect.py kucoin --api-key YOUR_KEY --secret-key YOUR_SECRET --passphrase YOUR_PASS

# Remove credentials for an exchange
python scripts/connect.py binance --remove
```

**Common credential fields by exchange:**
- Binance: `--api-key`, `--secret-key`
- KuCoin: `--api-key`, `--secret-key`, `--passphrase`
- Gate.io: `--api-key`, `--secret-key`
- OKX: `--api-key`, `--secret-key`, `--passphrase`

---

## balance

Display your asset balances across all connected exchanges.

```bash
# Show all balances
python scripts/balance.py

# Show balances for a specific connector
python scripts/balance.py binance

# Show balances in USD
python scripts/balance.py --usd

# Show only non-zero balances
python scripts/balance.py --non-zero
```

**Output columns:**
- Exchange/Connector name
- Asset symbol
- Total balance
- Available balance
- USD value (with `--usd`)

---

## create

Create a new bot configuration (controller config or script config).

```bash
# List available controller templates
python scripts/create.py --list-controllers

# List available scripts
python scripts/create.py --list-scripts

# List existing configs
python scripts/create.py --list-configs

# Create a controller config
python scripts/create.py controller my_mm_config --template pmm_v1
```

### Recommended Market Making Controllers

| Controller | Best For | Key Features |
|------------|----------|--------------|
| **pmm_v1** | CEX spot trading | Multi-level spreads, inventory skew, order refresh, price bands |
| **pmm_mister** | Spot & perpetuals | Position tracking, leverage, cooldowns, profit protection, hanging executors |

**pmm_v1**: Faithful clone of the legacy Pure Market Making strategy. Configure `buy_spreads`, `sell_spreads`, `order_amount`, and enable `inventory_skew` to maintain balance.

**pmm_mister**: Advanced controller for spot and perpetual markets with `leverage`, `take_profit`, `global_stop_loss`, separate `buy_cooldown_time`/`sell_cooldown_time`, and `position_profit_protection` to prevent selling below breakeven.

---

## start

Start a bot with a V2 strategy configuration. **V1 strategies are not supported.**

```bash
# Interactive mode - prompts for strategy type
python scripts/start.py <bot_name>

# Start with a V2 Controller config
python scripts/start.py <bot_name> --controller <config_name>

# Start with a V2 Script
python scripts/start.py <bot_name> --script <script_name>

# Start with a V2 Script and config file
python scripts/start.py <bot_name> --script <script_name> --config <config_name>

# List running bots
python scripts/start.py --list
```

**V2 Strategy Types:**
- `--controller` — Deploy a V2 controller config (market making, arbitrage, etc.)
- `--script` — Deploy a V2 script (e.g., `v2_with_controllers`)

**Bot naming:** Use descriptive names like `btc_mm_bot`, `eth_arb_bot`, etc.

---

## stop

Stop a running bot.

```bash
# Stop a bot by name
python scripts/stop.py <bot_name>

# Stop a bot and close all positions
python scripts/stop.py <bot_name> --close-positions

# Stop all running bots
python scripts/stop.py --all

# Examples
python scripts/stop.py my_bot
python scripts/stop.py arb_bot --close-positions
```

---

## status

Display bot status and performance metrics.

```bash
# List all bots with status
python scripts/status.py

# Get detailed status for a specific bot
python scripts/status.py <bot_name>

# Get status with performance metrics
python scripts/status.py <bot_name> --performance

# Get live status (refreshes)
python scripts/status.py <bot_name> --live
```

**Status values:** `running`, `stopped`, `error`, `starting`

**Performance metrics:**
- Total trades
- Profit/Loss (absolute and %)
- Volume traded
- Uptime

---

## history

Display bot trading history.

```bash
# Show trade history for a bot
python scripts/history.py <bot_name>

# Show summary statistics
python scripts/history.py <bot_name> --summary
```

**History columns:**
- Timestamp
- Trading pair
- Side (buy/sell)
- Price
- Amount
- Fee
- PnL

---

## Quick Reference

### Typical Workflow

```bash
# 1. Connect to an exchange
python scripts/connect.py binance --api-key XXX --secret-key YYY

# 2. Check your balances
python scripts/balance.py binance

# 3. Create a bot config
python scripts/create.py controller btc_mm \
  --template pure_market_making \
  --connector binance \
  --trading-pair BTC-USDT

# 4. Start the bot
python scripts/start.py btc_bot --controller btc_mm

# 5. Monitor status
python scripts/status.py btc_bot

# 6. Check history
python scripts/history.py btc_bot

# 7. Stop when done
python scripts/stop.py btc_bot
```

### Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `Cannot connect to API` | API not running | `cd ./hummingbot-api && make deploy` |
| `401 Unauthorized` | Bad credentials | Check `./hummingbot-api/.env` |
| `Connector not found` | Invalid exchange name | Run `python scripts/connect.py` to list valid names |
| `No credentials` | Exchange not connected | Run `python scripts/connect.py <exchange> --api-key ...` |

---

## Related Skills

- **lp-agent** — Specialized DEX liquidity provision on Meteora/Solana. Use for CLMM strategies.
- **hummingbot-deploy** — First-time setup of the Hummingbot API server. Run this before using this skill.
