---
name: moltrade
description: Operate the Moltrade trading bot (config, backtest, test-mode runs, Nostr signal broadcast, exchange adapters, strategy integration) in OpenClaw.
metadata:
  openclaw:
    emoji: "🤖"
    requires:
      bins: ["python", "pip"]
    homepage: https://github.com/hetu-project/moltrade.git
---

# Moltrade Bot Skill

**Moltrade** is a decentralized, automated trading assistant that lets you run quant strategies, share encrypted signals, and allow others to copy your trades—all securely via the Nostr network. Earn reputation and credits based on your trading performance.

![Moltrade](https://raw.githubusercontent.com/hetu-project/moltrade/main/assets/moltrade-background-2.jpg)

**YOUR 24/7 AI TRADER ! EARNING MONEY WHILE YOU'RE SLEEPING.**

[![Twitter Follow](https://img.shields.io/twitter/follow/hetu_protocol?style=social&label=Follow)](https://x.com/hetu_protocol) [![Telegram](https://img.shields.io/badge/Telegram-Hetu_Builders-blue)](https://t.me/+uJrRgjtSsGw3MjZl) [![ClawHub](https://img.shields.io/badge/ClawHub-Read-orange)](https://clawhub.ai/ai-chen2050/moltrade) [![Website](https://img.shields.io/badge/Website-moltrade.ai-green)](https://www.moltrade.ai/)

---

## Advantages

**Moltrade** balances security, usability, and scalability. Key advantages include:

1. **Client-side Key self-hosting,not cloud Custody,**: All sensitive keys and credentials remain on the user's machine; the cloud relay never holds funds or private keys, minimizing custodial risk.**No access to private keys or funds.**
2. **Encrypted, Targeted Communication**: Signals are encrypted before publishing and only decryptable by intended subscribers, preserving strategy privacy and subscriber security.
3. **Lightweight Cloud Re-encryption & Broadcast**: The cloud acts as an efficient relay/re-broadcaster without storing private keys; re-encryption or forwarding techniques improve delivery reliability and reach.
4. **One-Click Copy Trading (User Friendly)**: Provides an out-of-the-box copy-trading experience for non-expert users—set up in a few steps and execute signals locally.
5. **OpenClaw Strategy Advisor**: Integrates OpenClaw as an advisory tool for automated backtests and improvement suggestions; users decide whether to adopt recommended changes.
6. **Cloud Can Be Decentralized Relayer Network**: The lightweight relay architecture allows future migration to decentralized relay networks, reducing single points of failure and improving censorship resistance.
7. **Unified Incentive (Credit) System**: A transparent, verifiable Credit mechanism rewards all participants (signal providers, followers, relay nodes), aligning incentives across the ecosystem.

## **How It Works (Simplified Flow)**

```bash
1) Run Your Bot  ──→  2) Generate & Encrypt  ──→  3) Relay  ──→  4) Copy & Execute  ──→  5) Verify & Earn
```

## Install & Init

- If you are inside **OpenClaw**, you can install directly via ClawHub:

```bash
clawhub search moltrade
clawhub install moltrade
```

- OR & Clone the repo and install Python deps locally (code is required for strategies, nostr, and CLI):
  - `git clone https://github.com/hetu-project/moltrade.git`
  - `cd moltrade/trader && pip install -r requirements.txt`
- Initialize a fresh config with the built-in wizard (no trading):
  - Prefer the human user to run `python main.py --init` (prompts for relayer URL, wallet, nostr, copy-trade follower defaults, and bot registration), so you can approve prompts, handle the wallet private key entry yourself, and capture the relayer’s returned `relayer_nostr_pubkey` when registering the bot.
  - If you delegate to an agent, do so only if you trust it with the wallet key and ensure it completes the entire wizard—including the final bot registration step—so the `relayer_nostr_pubkey` gets written back to the config.
- For CI/agents, keep using the repo checkout; there is no separate pip package/CLI yet.

## Update Config Safely

- Backup or show planned diff before edits.
- Change only requested fields (e.g., `trading.exchange`, `trading.default_strategy`, `nostr.relays`).
- Validate JSON; keep types intact. Remind user to provide real secrets themselves.

## Run Backtest (local)

- Install deps: `pip install -r trader/requirements.txt`.
- Command: `python trader/backtest.py --config trader/config.example.json --strategy <name> --symbol <symbol> --interval 1h --limit 500`.
- Report PnL/win rate/trade count/drawdown if available. Use redacted config (no real keys).

## Start Bot (test mode)

- Ensure `config.json` exists (run `python main.py --init` if not) and `trading.exchange` set (default hyperliquid).
- Command: `python trader/main.py --config config.json --test --strategy <name> --symbol <symbol> --interval 300`.
- Watch `trading_bot.log`; never switch to live without explicit user approval.

## Run Bot (live)

- Only after validation on test mode; remove `--test` to hit mainnet.
- Command: `python trader/main.py --config config.json --strategy <name> --symbol <symbol>`.
- Double-check keys, risk limits, and symbol before starting; live mode will place real orders.

## Copy-trade Usage (live)

- Follower (mirrors leader, no strategy trading): `python trader/main.py --config trader/config.json --strategy momentum --symbol HYPE --copytrade follower`

## Broadcast Signals to Nostr

- Check `nostr` block: `nsec`, `relayer_nostr_pubkey`, `relays`, `sid`.
- `SignalBroadcaster` is wired in `main.py`. In test mode, verify `send_trade_signal` / `send_execution_report` run without errors.

## Binance Spot Support

Moltrade supports Binance Spot trading via `binance-sdk-spot`. Set `trading.exchange` to `"binance"` in your config and provide API credentials.

> **Related Skills** (raw API calls, not tied to the bot runtime):
>
> - [`binance/spot`](binance/spot/SKILL.md) — Binance Spot REST API skill: market data, order management, account info. Requires API key + secret; supports testnet and mainnet.
> - [`binance/square-post`](binance/square-post/SKILL.md) — Binance Square social platform skill: post trading insights/signals as text content via the Square OpenAPI. Requires a Square OpenAPI key.

### Install Binance SDK

```bash
pip install binance-sdk-spot
```

### Config Fields

Add a `binance` block alongside the existing `trading` block:

```json
{
  "trading": {
    "exchange": "binance",
    "default_symbol": "BTCUSDT",
    "default_strategy": "momentum"
  },
  "binance": {
    "api_key": "your_mainnet_api_key",
    "api_secret": "your_mainnet_api_secret",
    "testnet_api_key": "your_testnet_api_key",
    "testnet_api_secret": "your_testnet_api_secret"
  }
}
```

> **Note**: Binance testnet uses keys generated separately at <https://testnet.binance.vision> (GitHub login required). Mainnet keys do **not** work on the testnet.

### Testnet (–-test)

When `--test` is passed the bot routes all requests to `testnet.binance.vision` and uses `binance.testnet_api_key` / `testnet_api_secret`. If testnet keys are absent it falls back to mainnet keys, which will cause auth errors against the testnet endpoint.

```bash
python trader/main.py --config config.json --test --strategy momentum --symbol BTCUSDT
```

### Live Trading

```bash
python trader/main.py --config config.json --strategy momentum --symbol BTCUSDT
```

### Backtest

```bash
python trader/backtest.py --config trader/config.example.json --strategy momentum --symbol BTCUSDT --interval 1h --limit 500
```

### Supported Interface

`BinanceClient` (`trader/binance_api.py`) implements the same interface as `HyperliquidClient`:

| Method                                                 | Description                                                   |
| ------------------------------------------------------ | ------------------------------------------------------------- |
| `get_candles(symbol, interval, limit)`                 | K-line data as `[ts, open, high, low, close, vol]`            |
| `get_balance(asset)`                                   | Free balance for an asset (default `"USDT"`)                  |
| `get_positions()`                                      | Non-zero asset balances (spot has no margin positions)        |
| `get_open_orders()`                                    | All current open orders                                       |
| `place_order(symbol, is_buy, size, price, order_type)` | LIMIT or MARKET order with auto lot-size / tick-size rounding |
| `cancel_order(order_id, symbol)`                       | Cancel by order ID                                            |
| `cancel_all_orders(symbol)`                            | Cancel all orders (optionally for one symbol)                 |
| `get_ticker_price(symbol)`                             | Latest traded price                                           |

## Add Exchange Adapter

- Implement adapter in `trader/exchanges/` matching `HyperliquidClient` interface (`get_candles`, `get_balance`, `get_positions`, `place_order`, etc.).
- Register in `trader/exchanges/factory.py` keyed by `trading.exchange`.
- Update config `trading.exchange` and rerun backtest/test-mode.

## Integrate New Strategy

- Follow `trader/strategies/INTEGRATION.md` to subclass `BaseStrategy` and register in `get_strategy`.
- Add config under `strategies.<name>`; backtest, then test-mode before live.

## Safety / Secrets

- Never print or commit private keys, mnemonics, nsec, or shared keys.
- Default to test mode; require explicit consent for live trading.
