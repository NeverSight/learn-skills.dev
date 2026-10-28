---
name: binance-futures-signal-bot
description: Professional automated trading bot for Binance, Bybit, and OKX Futures with multi-strategy engine, Telegram/TradingView signal integration, and real-time P&L dashboard.
triggers:
  - set up binance futures trading bot
  - configure crypto signal bot with telegram
  - add trading strategy to futures bot
  - connect tradingview webhook to trading bot
  - configure leverage and position sizing for crypto bot
  - set up bybit automated trading
  - implement trailing stop loss for futures bot
  - troubleshoot binance signal bot not trading
---

# Binance Futures Signal Bot

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Automated trading bot for Binance, Bybit, and OKX Futures markets. Receives signals from Telegram channels, TradingView webhooks, or custom APIs, then executes trades with configurable leverage, dynamic position sizing, trailing stop-loss, and a real-time P&L terminal dashboard.

---

## Installation

```bash
git clone https://github.com/Whit1985/Binance-Futures-Signal-Bot.git
cd Binance-Futures-Signal-Bot
pip install -r requirements.txt
```

Or via the interactive menu:

```bash
python main.py   # choose option 1 → Install Dependencies
```

**Required Python: 3.10+**

Key dependencies:

| Package | Purpose |
|---|---|
| `rich` | Terminal UI / dashboards |
| `python-binance` | Binance REST & WebSocket |
| `ccxt` | Unified multi-exchange interface |
| `pandas` | OHLCV data & indicators |
| `ta` | Technical analysis (RSI, MACD, BB, EMA) |
| `websockets` | Real-time market streams |
| `cryptography` | Secure key storage |

---

## Quick Start

```bash
python main.py
```

Interactive menu options:

```
1 → Install Dependencies
2 → Settings (API keys, exchange, leverage)
3 → About
4 → Connect Signal Source (Telegram / TradingView / API)
5 → Start Auto Trading
6 → Strategy Configuration
7 → Position Manager (view & close positions)
8 → P&L Dashboard
0 → Exit
```

**Windows:**
```batch
run.bat
```

**Linux / macOS:**
```bash
chmod +x run.sh && ./run.sh
```

---

## Configuration

### config.json (full reference)

```json
{
  "exchange": "binance",
  "api_key": "",
  "api_secret": "",
  "testnet": false,
  "leverage": 10,
  "max_position_pct": 5.0,
  "trailing_stop_pct": 1.5,
  "signal_source": "telegram",
  "telegram_bot_token": "",
  "telegram_channel_id": "-100XXXXXXXXXX",
  "tradingview_webhook_port": 8080,
  "strategies": {
    "ema_crossover":     {"enabled": true,  "fast": 9,  "slow": 21},
    "rsi_divergence":    {"enabled": true,  "period": 14, "overbought": 70, "oversold": 30},
    "bollinger_breakout":{"enabled": false, "period": 20, "std_dev": 2.0},
    "macd_momentum":     {"enabled": true,  "fast": 12,  "slow": 26, "signal": 9}
  },
  "pairs": ["BTCUSDT", "ETHUSDT", "SOLUSDT"],
  "risk_management": {
    "max_open_positions": 5,
    "max_daily_loss_pct": 3.0,
    "stop_loss_pct": 2.0,
    "take_profit_pct": 4.0
  }
}
```

### Environment Variables (preferred for secrets)

```bash
export BINANCE_API_KEY="your_api_key_here"
export BINANCE_API_SECRET="your_api_secret_here"
export BYBIT_API_KEY="your_bybit_key"
export BYBIT_API_SECRET="your_bybit_secret"
export OKX_API_KEY="your_okx_key"
export OKX_API_SECRET="your_okx_secret"
export OKX_PASSPHRASE="your_okx_passphrase"
export TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
```

Never commit `config.json` with real keys — it is `.gitignore`d by default.

---

## Exchange Setup

### Binance Futures

```python
# config.py usage pattern
import os
import json

config = {
    "exchange": "binance",
    "api_key": os.environ.get("BINANCE_API_KEY"),
    "api_secret": os.environ.get("BINANCE_API_SECRET"),
    "testnet": True,   # always test first
    "leverage": 5,
    "pairs": ["BTCUSDT", "ETHUSDT"]
}

with open("config.json", "w") as f:
    json.dump(config, f, indent=2)
```

### Bybit Perpetual

```json
{
  "exchange": "bybit",
  "api_key": "",
  "api_secret": "",
  "leverage": 5,
  "pairs": ["BTCUSDT", "ETHUSDT"]
}
```

### OKX Perpetual Swap

```json
{
  "exchange": "okx",
  "api_key": "",
  "api_secret": "",
  "okx_passphrase": "",
  "leverage": 5,
  "pairs": ["BTC-USDT-SWAP", "ETH-USDT-SWAP"]
}
```

---

## Signal Sources

### 1. Telegram Channel

```python
# Setup steps:
# 1. Create bot at https://t.me/BotFather → get token
# 2. Add bot to signal channel as admin
# 3. Get channel ID (negative number starting with -100)

config_snippet = {
    "signal_source": "telegram",
    "telegram_bot_token": os.environ.get("TELEGRAM_BOT_TOKEN"),
    "telegram_channel_id": "-1001234567890"
}
```

### 2. TradingView Webhook

```json
{
  "signal_source": "tradingview",
  "tradingview_webhook_port": 8080
}
```

TradingView alert message format (JSON):

```json
{
  "symbol": "BTCUSDT",
  "side": "BUY",
  "leverage": 10,
  "price": "{{close}}",
  "strategy": "ema_crossover"
}
```

Point your TradingView alert webhook URL to:
```
http://YOUR_SERVER_IP:8080/webhook
```

### 3. Custom API Signal Source

```json
{
  "signal_source": "api",
  "custom_api_url": "https://your-signal-provider.com/signals",
  "custom_api_key": ""
}
```

---

## Strategies

### EMA Crossover

```json
{
  "ema_crossover": {
    "enabled": true,
    "fast": 9,
    "slow": 21
  }
}
```

- **LONG**: fast EMA crosses above slow EMA
- **SHORT**: fast EMA crosses below slow EMA
- Best timeframes: 15m, 1h, 4h

### RSI Divergence

```json
{
  "rsi_divergence": {
    "enabled": true,
    "period": 14,
    "overbought": 70,
    "oversold": 30
  }
}
```

- **Bullish**: price lower lows + RSI higher lows → LONG
- **Bearish**: price higher highs + RSI lower highs → SHORT

### Bollinger Band Breakout

```json
{
  "bollinger_breakout": {
    "enabled": true,
    "period": 20,
    "std_dev": 2.0
  }
}
```

- **LONG**: close above upper band
- **SHORT**: close below lower band

### MACD Momentum

```json
{
  "macd_momentum": {
    "enabled": true,
    "fast": 12,
    "slow": 26,
    "signal": 9
  }
}
```

- Trades histogram crossovers with signal line confirmation
- Zero-line acts as trend filter

### Running Multiple Strategies

All enabled strategies run per candle. The bot takes the **highest-confidence signal** and filters conflicts:

```json
{
  "strategies": {
    "ema_crossover":      {"enabled": true,  "fast": 9,  "slow": 21},
    "rsi_divergence":     {"enabled": true,  "period": 14},
    "bollinger_breakout": {"enabled": false},
    "macd_momentum":      {"enabled": true}
  }
}
```

---

## Risk Management

```json
{
  "leverage": 10,
  "max_position_pct": 5.0,
  "trailing_stop_pct": 1.5,
  "risk_management": {
    "max_open_positions": 5,
    "max_daily_loss_pct": 3.0,
    "stop_loss_pct": 2.0,
    "take_profit_pct": 4.0
  }
}
```

| Parameter | Description |
|---|---|
| `leverage` | 1x–125x (start with 2–5x) |
| `max_position_pct` | % of account balance per trade |
| `trailing_stop_pct` | Trailing SL activates after price moves this % in profit |
| `max_open_positions` | Hard cap on concurrent open trades |
| `max_daily_loss_pct` | Bot halts trading if daily loss exceeds this |
| `stop_loss_pct` | Fixed stop-loss distance from entry |
| `take_profit_pct` | Fixed take-profit distance from entry |

**Trailing stop-loss behavior:** Once position is in profit by `trailing_stop_pct`, the stop follows the peak price. Position closes automatically on reversal of that distance.

---

## Testnet Mode

Always validate on testnet before live trading:

```json
{
  "testnet": true,
  "exchange": "binance"
}
```

Binance testnet: https://testnet.binancefuture.com  
Bybit testnet: https://testnet.bybit.com

---

## Project Structure

```
Binance-Futures-Signal-Bot/
├── main.py              # Entry point — interactive menu
├── bot_actions.py       # Core trading action handlers
├── config.py            # Configuration loader (JSON + env vars)
├── requirements.txt
├── run.bat / run.sh     # Platform launchers
├── actions/
│   ├── about.py         # Feature display
│   ├── install.py       # Dependency installer
│   └── settings.py      # Configuration UI
├── utils/
│   ├── __init__.py      # Environment bootstrap
│   ├── compat.py        # Platform compatibility
│   ├── ui.py            # Rich terminal interface
│   ├── http.py          # HTTP client
│   ├── integrity.py     # Data integrity checks
│   └── bootstrap.py     # Runtime initialization
└── release/
    └── README.md        # Pre-compiled binary info
```

---

## Common Patterns

### Load Config Programmatically

```python
import json
import os

def load_config(path="config.json"):
    with open(path) as f:
        cfg = json.load(f)
    # Override with env vars if set
    cfg["api_key"]    = os.environ.get("BINANCE_API_KEY", cfg.get("api_key", ""))
    cfg["api_secret"] = os.environ.get("BINANCE_API_SECRET", cfg.get("api_secret", ""))
    return cfg

config = load_config()
```

### Minimal Safe Config for Testing

```python
import json

safe_config = {
    "exchange": "binance",
    "api_key": "",       # set via env var BINANCE_API_KEY
    "api_secret": "",    # set via env var BINANCE_API_SECRET
    "testnet": True,
    "leverage": 2,
    "max_position_pct": 1.0,
    "signal_source": "telegram",
    "telegram_bot_token": "",   # set via env var TELEGRAM_BOT_TOKEN
    "telegram_channel_id": "",
    "strategies": {
        "ema_crossover": {"enabled": True, "fast": 9, "slow": 21},
        "rsi_divergence": {"enabled": False},
        "bollinger_breakout": {"enabled": False},
        "macd_momentum": {"enabled": False}
    },
    "pairs": ["BTCUSDT"],
    "risk_management": {
        "max_open_positions": 1,
        "max_daily_loss_pct": 1.0,
        "stop_loss_pct": 1.5,
        "take_profit_pct": 3.0
    }
}

with open("config.json", "w") as f:
    json.dump(safe_config, f, indent=2)
```

### Verify Installation

```python
# Quick dependency check
required = ["rich", "binance", "ccxt", "pandas", "ta", "websockets", "cryptography"]
import importlib

for pkg in required:
    try:
        importlib.import_module(pkg)
        print(f"✓ {pkg}")
    except ImportError:
        print(f"✗ {pkg} — run: pip install {pkg}")
```

---

## Troubleshooting

### Bot won't connect to exchange

```bash
# Check API key permissions — must have:
# Binance: Enable Futures, Enable Reading, Enable Spot & Margin Trading
# Bybit:   Unified Trading, Read/Write
# OKX:     Trade, Read

# Test connectivity
python -c "
import ccxt, os
exchange = ccxt.binance({
    'apiKey': os.environ['BINANCE_API_KEY'],
    'secret': os.environ['BINANCE_API_SECRET'],
    'options': {'defaultType': 'future'}
})
print(exchange.fetch_balance())
"
```

### Telegram signals not received

1. Confirm bot is **admin** in the channel
2. Verify `telegram_channel_id` starts with `-100`
3. Send a test message to the channel after adding the bot
4. Check bot token with: `https://api.telegram.org/bot<TOKEN>/getMe`

### TradingView webhook not triggering

```bash
# Ensure port 8080 is open and accessible
# Check firewall rules
sudo ufw allow 8080/tcp

# Test webhook endpoint locally
curl -X POST http://localhost:8080/webhook \
  -H "Content-Type: application/json" \
  -d '{"symbol":"BTCUSDT","side":"BUY","leverage":5}'
```

### Leverage rejected by exchange

- Binance max leverage varies per symbol (BTC: 125x, altcoins: lower)
- Bybit requires setting leverage per symbol before trading
- Start with `"leverage": 5` and increase carefully

### ImportError on startup

```bash
pip install --upgrade -r requirements.txt
# or individually:
pip install rich>=13.0.0 python-binance>=1.0.19 ccxt>=4.2.0 pandas>=2.1.0 ta>=0.10.2 websockets>=12.0 cryptography
```

### Position not closing at stop-loss

- Ensure `stop_loss_pct` is set in `risk_management`
- Trailing stop only activates after initial profit threshold (`trailing_stop_pct`)
- Check exchange order type support — some altcoin pairs have restrictions

---

## Safety Checklist

- [ ] Always run `"testnet": true` first
- [ ] Start with `"leverage": 2` or `3`
- [ ] Set `max_daily_loss_pct` ≤ 3.0
- [ ] Keep `max_open_positions` ≤ 3 initially
- [ ] Never commit `config.json` with real API keys
- [ ] Use environment variables for all secrets
- [ ] Keep API key IP-restricted on exchange side
- [ ] Enable only one strategy initially; add more after validation

---

## Disclaimer

This software is for educational and research purposes only. Cryptocurrency futures trading involves substantial risk of loss including full account liquidation. The authors bear no responsibility for financial losses from use of this software.
