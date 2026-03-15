---
name: hyperliquid-supurr
description: Build, backtest, deploy, and monitor trading bots on Hyperliquid. Author custom strategies in Rust, or use built-in Grid, DCA, and Spot-Perp Arbitrage strategies across Native Perps, Spot markets (USDC/USDH), HIP-3 sub-DEXes, and Prediction Markets (testnet).
---

# Hyperliquid Supurr Skill — Complete Command Reference

> **For LLMs**: This is the authoritative reference. Use exact syntax. Config files are in `~/.supurr/configs/`.

---

## Quick Reference

| Command                | Purpose                         |
| ---------------------- | ------------------------------- |
| `supurr init`          | Setup wallet credentials        |
| `supurr whoami`        | Show current wallet             |
| `supurr new grid`      | Generate grid strategy config   |
| `supurr new arb`       | Generate spot-perp arb config   |
| `supurr new dca`       | Generate DCA strategy config    |
| `supurr configs`       | List saved configs              |
| `supurr config <name>` | View config details             |
| `supurr backtest`      | Run historical simulation       |
| `supurr deploy`        | Deploy bot to production        |
| `supurr monitor`       | View active bots                |
| `supurr history`       | View historical bot sessions    |
| `supurr stop`          | Stop a running bot (signed)     |
| `supurr prices`        | Debug price data                |
| `supurr update`        | Update CLI to latest            |
| `supurr dev init`      | Clone/update bot source for dev |
| `supurr dev build`     | Build bot from source           |
| `supurr dev run`       | Run dev-built bot               |
| `supurr dev backtest`  | Backtest with dev-built engine  |

---

## Global Options

```bash
supurr --help              # Show all commands
supurr --version, -V       # Show CLI version
supurr -d, --debug         # Enable debug logging (any command)
```

---

## 1. `supurr init` — Credential Setup

```bash
# Interactive
supurr init

# Non-interactive
supurr init --address 0x... --api-wallet 0x...

# Overwrite existing
supurr init --force
```

| Option                | Description                    |
| --------------------- | ------------------------------ |
| `-f, --force`         | Overwrite existing credentials |
| `--address <address>` | Wallet address (0x...)         |
| `--api-wallet <key>`  | API wallet private key         |

---

## 2. `supurr whoami` — Show Identity

```bash
supurr whoami    # Shows: Address + masked key
```

---

## 3. `supurr new <strategy>` — Config Generator

Supports three strategies: `grid`, `arb`, `dca`.

```bash
supurr new grid [options]   # Grid trading
supurr new arb [options]    # Spot-perp arbitrage
supurr new dca [options]    # Dollar-cost averaging
```

---

### 3a. `supurr new grid` — Grid Strategy

#### Market Types

| Type      | Quote    | Requires  | Example                                 |
| --------- | -------- | --------- | --------------------------------------- |
| `native`  | USDC     | —         | `--asset BTC`                           |
| `spot`    | Variable | `--quote` | `--asset HYPE --type spot --quote USDC` |
| `hip3`    | Per-DEX  | `--dex`   | `--asset BTC --type hip3 --dex hyna`    |
| `outcome` | USDC     | Manual config | ⚠️ Testnet only — see [Prediction Markets tutorial](tutorials/prediction-markets.md) |

#### Grid Options

| Option                  | Default       | Description                                    |
| ----------------------- | ------------- | ---------------------------------------------- |
| `-a, --asset <symbol>`  | `BTC`         | Base asset (BTC, ETH, HYPE, etc.)              |
| `-o, --output <file>`   | `config.json` | Output filename                                |
| `--type <type>`         | `native`      | Market type: native, spot, hip3                |
| `--dex <dex>`           | —             | **Required for hip3**: hyna, xyz, km, vntl     |
| `--quote <quote>`       | —             | **Required for spot**: USDC, USDE, USDT0, USDH |
| `--mode <mode>`         | `long`        | Grid mode: long, short, neutral                |
| `--levels <n>`          | `20`          | Number of grid levels                          |
| `--start-price <price>` | —             | Grid start price                               |
| `--end-price <price>`   | —             | Grid end price                                 |
| `--investment <amount>` | `1000`        | Max investment in quote currency               |
| `--leverage <n>`        | `2`           | Leverage (1 for spot)                          |
| `--testnet`             | false         | Use Hyperliquid testnet                        |

#### Grid Examples

```bash
# Native Perp (BTC-USDC)
supurr new grid --asset BTC --levels 4 --start-price 88000 --end-price 92000 --investment 100 --leverage 20

# USDC Spot (HYPE/USDC)
supurr new grid --asset HYPE --type spot --quote USDC --levels 3 --start-price 29 --end-price 32 --investment 100

# Non-USDC Spot (HYPE/USDH)
supurr new grid --asset HYPE --type spot --quote USDH --levels 3 --start-price 29 --end-price 32 --investment 100

# HIP-3 (hyna:BTC)
supurr new grid --asset BTC --type hip3 --dex hyna --levels 4 --start-price 88000 --end-price 92000 --investment 100 --leverage 20
```

#### HIP-3 DEXes

| DEX    | Quote | Assets                              |
| ------ | ----- | ----------------------------------- |
| `hyna` | USDE  | Crypto perps (BTC, ETH, HYPE, etc.) |
| `xyz`  | USDE  | Stocks (AAPL, TSLA, etc.)           |
| `km`   | USDT  | Kinetiq Markets                     |
| `vntl` | USDE  | AI/tech tokens                      |

---

### 3b. `supurr new arb` — Spot-Perp Arbitrage Strategy

Generates a config that simultaneously trades the **spot** and **perp** legs of the same asset, capturing spread differentials.

> **Market Constraint**: Only assets that have **both** a spot token AND a perp market on Hyperliquid are eligible. The CLI auto-resolves the spot counterpart.

#### Spot Resolution Logic

Resolution order: try `U{ASSET}` first (e.g., `BTC` → `UBTC`) → fallback to exact name (e.g., `HYPE`, `TRUMP`) → error if neither exists.

> **⚠️ Always pass the perp ticker** (e.g., `BTC`, not `UBTC`). See full table → [references/arb-spot-resolution.md](references/arb-spot-resolution.md)

#### Arb Options

| Option                 | Default            | Description                                  |
| ---------------------- | ------------------ | -------------------------------------------- |
| `-a, --asset <symbol>` | `BTC`              | Perp asset name (BTC, ETH, HYPE, etc.)       |
| `--amount <usdc>`      | `100`              | Order amount in USDC per leg                 |
| `--leverage <n>`       | `1`                | Leverage for perp leg                        |
| `--open-spread <pct>`  | `0.003`            | Min opening spread (0.003 = 0.3%)            |
| `--close-spread <pct>` | `-0.001`           | Min closing spread (-0.001 = -0.1%)          |
| `--slippage <pct>`     | `0.001`            | Slippage buffer for both legs (0.001 = 0.1%) |
| `-o, --output <file>`  | `{asset}-arb.json` | Output filename                              |
| `--testnet`            | false              | Use Hyperliquid testnet                      |

#### Arb Examples

```bash
# BTC spot-perp arb (default $100/leg)
supurr new arb --asset BTC

# HYPE arb with $50 per leg, 2x leverage on perp
supurr new arb --asset HYPE --amount 50 --leverage 2

# ETH arb with tighter spreads
supurr new arb --asset ETH --open-spread 0.002 --close-spread -0.0005 --slippage 0.0005

# SOL arb on testnet
supurr new arb --asset SOL --testnet
```

> **Balance Requirement**: Arb bots require USDC balance in **both** Spot and Perps wallets on Hyperliquid, since the bot trades on both sides simultaneously.

---

### 3c. `supurr new dca` — DCA Strategy

Generates a Dollar-Cost Averaging config that opens positions in steps when price deviates, then takes profit on the averaged entry.

#### DCA Options

| Option                       | Default       | Description                                        |
| ---------------------------- | ------------- | -------------------------------------------------- |
| `-a, --asset <symbol>`       | `BTC`         | Base asset                                         |
| `--mode <mode>`              | `long`        | Direction: long or short                           |
| `--type <type>`              | `native`      | Market type: native, spot, hip3                    |
| `--trigger-price <price>`    | `100000`      | Price to trigger base order                        |
| `--base-order <size>`        | `0.001`       | Base order size in base asset                      |
| `--dca-order <size>`         | `0.001`       | DCA order size in base asset                       |
| `--max-orders <n>`           | `5`           | Max number of DCA orders                           |
| `--size-multiplier <x>`      | `2.0`         | Size multiplier per DCA step                       |
| `--deviation <pct>`          | `0.01`        | Price deviation % to trigger first DCA (0.01 = 1%) |
| `--deviation-multiplier <x>` | `1.0`         | Deviation multiplier for subsequent steps          |
| `--take-profit <pct>`        | `0.02`        | Take profit % from avg entry (0.02 = 2%)           |
| `--stop-loss <pnl>`          | —             | Optional stop loss as absolute PnL threshold       |
| `--leverage <n>`             | `2`           | Leverage (1 for spot)                              |
| `--restart`                  | false         | Restart cycle after take profit                    |
| `--cooldown <secs>`          | `60`          | Cooldown between cycles in seconds                 |
| `-o, --output <file>`        | `config.json` | Output filename                                    |
| `--testnet`                  | false         | Use Hyperliquid testnet                            |

#### DCA Examples

```bash
# BTC DCA long, trigger at $95k
supurr new dca --asset BTC --trigger-price 95000

# ETH DCA short with custom deviation
supurr new dca --asset ETH --mode short --deviation 0.02

# HYPE DCA with auto-restart
supurr new dca --asset HYPE --restart --cooldown 120 --take-profit 0.03

# DCA on spot market
supurr new dca --asset HYPE --type spot --quote USDC --trigger-price 25
```

---

## 4. `supurr configs` — List Saved Configs

```bash
supurr configs    # Lists all configs in ~/.supurr/configs/
```

**Output:**

```
📁 Configs (/Users/you/.supurr/configs):
  btc-grid.json         grid     BTC-USDC
  hype-usdc-spot.json   grid     HYPE-USDC
  hyna-btc.json         grid     BTC-USDE
```

---

## 5. `supurr config <name>` — View Config

```bash
supurr config btc-grid        # View btc-grid.json
supurr config btc-grid.json   # Same
```

---

## 6. `supurr backtest` — Run Backtest

### Syntax

```bash
supurr backtest -c <config> [options]
```

> **Supported strategies**: Grid, DCA, and custom strategies. Arb (spot-perp arbitrage) backtesting is **not supported** — arb requires simultaneous dual-market execution that cannot be accurately simulated from single-asset price feeds.

> **⚠️ IMPORTANT — Asset ID Required**: Bot configs require a `market_index` (Hyperliquid's internal asset index, e.g. `3` for BTC). You **must** know this value beforehand. It is **not** auto-resolved by the CLI. To find it, query the Hyperliquid Info API: `POST https://api.hyperliquid.xyz/info` with `{"type": "meta"}` — the response `universe` array contains all assets with their indices. Alternatively, check the [Hyperliquid Info API reference](references/hl-info-api.md) for the exact endpoint.

### Options

| Option                | Description                              |
| --------------------- | ---------------------------------------- |
| `-c, --config <file>` | **Required.** Config file (name or path) |
| `-s, --start <date>`  | Start date (YYYY-MM-DD)                  |
| `-e, --end <date>`    | End date (YYYY-MM-DD)                    |
| `-p, --prices <file>` | Use local prices file                    |
| `-o, --output <file>` | Save results to JSON                     |
| `--no-cache`          | Disable price caching                    |

### Examples

```bash
# By config name (looks in ~/.supurr/configs/)
supurr backtest -c btc-grid.json -s 2026-01-28 -e 2026-02-01

# By full path
supurr backtest -c ~/.supurr/configs/btc-grid.json -s 2026-01-28 -e 2026-02-01

# Save results
supurr backtest -c btc-grid.json -s 2026-01-28 -e 2026-02-01 -o results.json
```

### Archive Data Availability

| Dex           | Asset Format           | Example            |
| ------------- | ---------------------- | ------------------ |
| `hyperliquid` | `BTC`, `HYPE`          | Native perp + Spot |
| `hyna`        | `hyna:BTC`, `hyna:ETH` | HIP-3 DEX          |

> **Note**: Archive data available from 2026-01-28 onwards.
>
> **Important**: Backtests use Supurr's price archive (tick-level) or a user-provided prices file (`-p`). Do **not** use Hyperliquid Info API mids/candles for backtests; they don't provide tick-level historical data and will produce inaccurate results.

---

## 6b. `supurr dev` — Custom Strategy Development

Development commands for building and testing custom strategies locally.

```bash
supurr dev init              # Clone/update bot source to ~/.supurr/bot-source/
supurr dev build             # Build from source (cargo build --release)
supurr dev run -c <config>   # Run locally-built bot
supurr dev backtest -c <config> [options]  # Backtest with dev-built engine
```

### `supurr dev backtest`

Identical to `supurr backtest` but uses the **dev-built engine** at `~/.supurr/bot-source/target/release/bot` instead of the installed binary. This lets you backtest **custom strategies** that you've added to the bot source.

```bash
# Backtest your custom strategy
supurr dev backtest -c config-mystrategy.json -s 2026-01-28 -e 2026-02-01

# With local prices
supurr dev backtest -c config-mystrategy.json -p prices.json
```

All options from `supurr backtest` apply (`-s`, `-e`, `-p`, `--no-cache`, `-o`).

> **Prerequisite**: Run `supurr dev build` first to compile your custom strategy into the dev binary.

### Full Custom Strategy Workflow

```bash
# 1. Clone the bot source
supurr dev init

# 2. Add your strategy crate (see STRATEGY_API.md)
# 3. Build with your strategy
supurr dev build

# 4. Backtest it
supurr dev backtest -c config-mystrategy.json -s 2026-01-28 -e 2026-02-01

# 5. Run live (paper or real)
supurr dev run -c config-mystrategy.json
```

---

## 7. `supurr deploy` — Deploy Bot

```bash
supurr deploy -c <config> [-s <address> | -v <address>]
```

| Option                       | Description                                             |
| ---------------------------- | ------------------------------------------------------- |
| `-c, --config <file>`        | **Required.** Config file (name or path)                |
| `-s, --subaccount <address>` | Trade from a subaccount (validates master ownership)    |
| `-v, --vault <address>`      | Trade from a vault (validates you are the vault leader) |

> **Subaccount vs Vault:**
>
> - **Subaccount** = personal trading account under your master wallet. Verified via `subAccounts` API (checks `master` field).
> - **Vault** = shared investment pool you manage. Verified via `vaultDetails` API (checks `leader` field).
> - Both set `vault_address` in the bot config on success.
> - **Cannot use both** `--subaccount` and `--vault` simultaneously.

### Examples

```bash
# Deploy from main wallet
supurr deploy -c btc-grid.json

# Deploy from subaccount
supurr deploy -c btc-grid.json -s 0x804e57d7baeca937d4b30d3cbe017f8d73c21f1b

# Deploy from vault (you must be the vault leader)
supurr deploy -c config.json --vault 0xdc89f67e74098dd93a1476f7da79747f71ccb5d9

# HL: prefix is auto-stripped (copy-paste from Hyperliquid UI)
supurr deploy -c config.json -s HL:0x804e57d7baeca937d4b30d3cbe017f8d73c21f1b
```

**Output:**

```
✔ Loaded config for grid strategy
✔ Subaccount verified: 0x804e57d7...
✔ Bot deployed successfully!
📦 Deployment Details
  Bot ID:       217
  Pod Name:     bot-217
  Bot Type:     grid
  Market:       BTC-USDC
```

> **Gotchas**: `HL:` prefix is auto-stripped from addresses. Subaccount requires `master` to match your `supurr whoami` address. Only the vault leader can deploy.

---

## 8. `supurr monitor` — View User's Bots

> **Updated in v0.2.8**: Now shows only the user's bots by default (requires `supurr init`). Use `--history` to include stopped bots.

### Syntax

```bash
supurr monitor [options]
```

### Options

| Option                   | Description                          |
| ------------------------ | ------------------------------------ |
| `-w, --wallet <address>` | Filter by wallet address             |
| `--watch`                | Live mode (refreshes every 2s)       |
| `--history`              | Show all bots including stopped ones |

### Examples

```bash
supurr monitor                 # Show only active bots for current user
supurr monitor --history       # Show all bots (active + stopped)
supurr monitor --watch         # Live monitoring (Ctrl+C to exit)
supurr monitor --watch --history  # Live monitoring with history
supurr monitor -w 0x1234...    # Filter by wallet
```

### Behavior

- **User-Specific**: Fetches bots for the address in `~/.supurr/credentials.json` (from `supurr init`)
- **Default**: Shows only active bots (status = "running" or "starting")
- **With `--history`**: Shows all bots including stopped ones
- **Header**: Displays user address and sync delay: `🤖 Active Bots  │  User: 0x0ecba...  │  Sync delay: 0s`
- **Trading Link**: Shows clickable visualization link at the end with correct market format:
  - **Spot**: `KNTQ_USDH` (underscore separator)
  - **Perp**: `BTC-USDC` (hyphen separator)
  - **HIP-3**: `vntl:ANTHROPIC` (dex:base format)

**Output Columns:** ID, Type, Market, Position (size+direction), PnL. Includes a clickable trading visualization link.

---

## 9. `supurr history` — View Bot History

```bash
supurr history             # Show last 20 bot sessions
supurr history -n 50       # Show last 50 bot sessions
```

| Option                | Default | Description            |
| --------------------- | ------- | ---------------------- |
| `-n, --limit <count>` | `20`    | Number of bots to show |

**Output Columns:** ID, Market, Type, PnL, Stop Reason.

---

## 10. `supurr stop` — Stop Bot (Signature Auth)

Signs `Stop <bot-id>` with your API wallet private key (EIP-191 personal_sign) and sends the signature to the bot API.

```bash
supurr stop              # Interactive - select from list
supurr stop --id 217     # Stop specific bot by ID
```

| Option          | Description                            |
| --------------- | -------------------------------------- |
| `--id <bot_id>` | Bot ID to stop (from `supurr monitor`) |

> **Crypto:** Uses `@noble/curves/secp256k1` + `@noble/hashes/sha3` (pure JS, no native deps). Signature format: `0x{r}{s}{v}` (65 bytes).

---

## 11. `supurr prices` — Debug Price Data

```bash
supurr prices -a BTC                     # Fetch BTC prices (7 days)
supurr prices -a hyna:BTC --dex hyna     # HIP-3 prices
supurr prices -a HYPE -s 2026-01-28      # From specific date
```

| Option                 | Description                     |
| ---------------------- | ------------------------------- |
| `-a, --asset <symbol>` | **Required.** Asset symbol      |
| `--dex <dex>`          | DEX name (default: hyperliquid) |
| `-s, --start <date>`   | Start date                      |
| `-e, --end <date>`     | End date                        |
| `--no-cache`           | Disable caching                 |

---

## 12. `supurr update` — Self-Update

```bash
supurr update    # Check and install latest version
```

---

## More Info

- **Workflows**: See → [references/workflows.md](references/workflows.md)
- **Config storage**: `~/.supurr/` contains `credentials.json`, `configs/`, and `cache/`
- **Troubleshooting**: See → [references/troubleshooting.md](references/troubleshooting.md)

---

# References

## CLI & Exchange References

| Reference                                                | Contents                                               |
| -------------------------------------------------------- | ------------------------------------------------------ |
| [Hyperliquid Info API](references/hl-info-api.md)        | All `POST /info` endpoints, TypeScript helper, hazards |
| [Arb Spot Resolution](references/arb-spot-resolution.md) | Full U-prefix table, resolution logic, edge cases      |
| [Troubleshooting](references/troubleshooting.md)         | Common errors and fixes                                |
| [Complete Workflows](references/workflows.md)            | End-to-end Grid, Arb, DCA, HIP-3 workflows             |

## Strategy Authoring References

> **For LLMs**: To build a custom trading strategy, read [STRATEGY_API.md](STRATEGY_API.md) first — it has the full contract, 3-file pattern, and E2E build instructions. **For indicator-based strategies** (RSI, MACD, Bollinger, EMA crossover, etc.), also read [indicator-strategies.md](references/indicator-strategies.md) for the 3-layer pattern (BarBuilder → Indicator → Phase Machine) and the `strategy-rsi` reference implementation. Then use the API references below for exact signatures.

| Reference                                                  | Contents                                                                                        |
| ---------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| [Strategy Authoring API](STRATEGY_API.md)                  | **START HERE** — Architecture, Strategy trait, StrategyContext, 3-file pattern, E2E build guide |
| [Indicator Strategies](references/indicator-strategies.md) | 3-layer pattern (BarBuilder → Indicator → Phase Machine) for RSI, MACD, Bollinger, EMA, etc.    |
| [Strategy Trait & Context](references/strategy-trait.md)   | `Strategy` trait + `StrategyContext` method signatures (commands, timers, read-only state)      |
| [Command Structs](references/commands.md)                  | `PlaceOrder`, `CancelOrder`, `CancelAll`, `StopStrategy` — constructors + builders              |
| [Event Enum](references/events.md)                         | All events: `Quote`, `OrderFilled`, `OrderCompleted`, `OrderCanceled`, `OrderRejected`, etc.    |
| [Core Types](references/types.md)                          | All types: `Price`, `Qty`, `Market`, `Position`, `Balance`, `InstrumentMeta`, `LiveOrder`, etc. |
| [Strategy Template](templates/strategy-template/)          | Scaffold crate with TODO markers — copy to start a new strategy                                 |
| [Simple Strategy Example](examples/strategy-simple/)       | Complete working buy-low-sell-high strategy (~140 lines)                                        |
| [Custom Strategy Tutorial](tutorials/custom-strategy.md)   | End-to-end walkthrough: scaffold → implement → register → build → run                           |

---

## Tutorials

- [Grid Bot Tutorial](tutorials/grid.md) — Range trading with buy/sell grids
- [Arb Bot Tutorial](tutorials/arb.md) — Market-neutral spot-perp arbitrage
- [DCA Bot Tutorial](tutorials/dca.md) — Dollar-cost averaging with auto-restart
- [Prediction Markets](tutorials/prediction-markets.md) — Trade binary outcomes on testnet ⚠️
- [Build Your Own Strategy](tutorials/custom-strategy.md) — Custom strategy from scratch
