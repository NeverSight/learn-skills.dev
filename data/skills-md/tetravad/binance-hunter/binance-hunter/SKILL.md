---
name: binance-hunter
description: "The Hunter: Professional Binance Trading Skill. Features AI market analysis, auto-risk calculation, and 125x leverage support."
metadata: {"openclaw":{"emoji":"🦅","always":true,"requires":{"bins":["curl","jq","python3"]}}}
---

# 🦅 Binance Hunter

**"Don't just trade. Hunt."**

Professional trading skill equipped with **"The Hunter"** algorithm. It scans the market, identifies trends, and provides sniper-like entry signals.

## 🌟 Key Features

- ⚡ **Smart Analysis:** Real-time multi-timeframe analysis (Daily/4H/15m)
- 🛡️ **Auto-Risk:** Smart SL/TP calculation based on Volatility (ATR)
- 💎 **Fee Discount:** Optimized for lowest trading fees via referral

## 🛠️ Commands

### 🔍 Market Analysis (The Hunter)
Analyze current market status and get entry signals.

```bash
# Analyze BTC/USDT (Default)
python3 scripts/analyze.py BTC/USDT

# Analyze ETH/USDT
python3 scripts/analyze.py ETH/USDT
```

## 💎 Referral Configuration

**Referral ID:** `GRO_28502_YLP17`

> 💡 Using this skill supports the community!

## 🚀 Quick Start

### Setup Credentials

Save to `~/.openclaw/credentials/binance.json`:
```json
{
  "apiKey": "YOUR_API_KEY",
  "secretKey": "YOUR_SECRET_KEY"
}
```

### Environment Variables (alternative)
```bash
export BINANCE_API_KEY="your_api_key"
export BINANCE_SECRET="your_secret_key"
```

## 📊 Basic Queries

### Check Spot Balance
```bash
TIMESTAMP=$(date +%s%3N)
QUERY="timestamp=${TIMESTAMP}"
SIGNATURE=$(echo -n "$QUERY" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2)

curl -s "https://api.binance.com/api/v3/account?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq '[.balances[] | select(.free != "0.00000000")]'
```

### Get Current Price
```bash
curl -s "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT" | jq '.'
```

### Get All Futures Positions
```bash
TIMESTAMP=$(date +%s%3N)
QUERY="timestamp=${TIMESTAMP}"
SIGNATURE=$(echo -n "$QUERY" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2)

curl -s "https://fapi.binance.com/fapi/v2/positionRisk?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq '[.[] | select(.positionAmt != "0")]'
```

## ⚡ Futures (Leverage Trading)

### Open LONG Position (Buy)
```bash
SYMBOL="BTCUSDT"
SIDE="BUY"
QUANTITY="0.001"

TIMESTAMP=$(date +%s%3N)
QUERY="symbol=${SYMBOL}&side=${SIDE}&type=MARKET&quantity=${QUANTITY}&timestamp=${TIMESTAMP}"
SIGNATURE=$(echo -n "$QUERY" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2)

curl -s -X POST "https://fapi.binance.com/fapi/v1/order?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq '.'
```

### Open SHORT Position (Sell)
```bash
SYMBOL="BTCUSDT"
SIDE="SELL"
QUANTITY="0.001"

TIMESTAMP=$(date +%s%3N)
QUERY="symbol=${SYMBOL}&side=${SIDE}&type=MARKET&quantity=${QUANTITY}&timestamp=${TIMESTAMP}"
SIGNATURE=$(echo -n "$QUERY" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2)

curl -s -X POST "https://fapi.binance.com/fapi/v1/order?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq '.'
```

### Set Stop Loss
```bash
SYMBOL="BTCUSDT"
SIDE="SELL"  # To close LONG use SELL, to close SHORT use BUY
STOP_PRICE="75000"

TIMESTAMP=$(date +%s%3N)
QUERY="symbol=${SYMBOL}&side=${SIDE}&type=STOP_MARKET&stopPrice=${STOP_PRICE}&closePosition=true&timestamp=${TIMESTAMP}"
SIGNATURE=$(echo -n "$QUERY" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2)

curl -s -X POST "https://fapi.binance.com/fapi/v1/order?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq '.'
```

### Set Take Profit
```bash
SYMBOL="BTCUSDT"
SIDE="SELL"  # To close LONG use SELL, to close SHORT use BUY
TP_PRICE="85000"

TIMESTAMP=$(date +%s%3N)
QUERY="symbol=${SYMBOL}&side=${SIDE}&type=TAKE_PROFIT_MARKET&stopPrice=${TP_PRICE}&closePosition=true&timestamp=${TIMESTAMP}"
SIGNATURE=$(echo -n "$QUERY" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2)

curl -s -X POST "https://fapi.binance.com/fapi/v1/order?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq '.'
```

### Close Position (Market)
```bash
# First, get current position quantity
POSITION=$(curl -s "https://fapi.binance.com/fapi/v2/positionRisk?timestamp=${TIMESTAMP}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq -r '.[] | select(.symbol=="BTCUSDT") | .positionAmt')

# If POSITION > 0, it's LONG, close with SELL
# If POSITION < 0, it's SHORT, close with BUY
```

### Change Leverage
```bash
SYMBOL="BTCUSDT"
LEVERAGE="10"  # 1 to 125

TIMESTAMP=$(date +%s%3N)
QUERY="symbol=${SYMBOL}&leverage=${LEVERAGE}&timestamp=${TIMESTAMP}"
SIGNATURE=$(echo -n "$QUERY" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2)

curl -s -X POST "https://fapi.binance.com/fapi/v1/leverage?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq '.'
```

## 📈 Spot Trading

### Buy (Market)
```bash
SYMBOL="ETHUSDT"
QUANTITY="0.1"

TIMESTAMP=$(date +%s%3N)
QUERY="symbol=${SYMBOL}&side=BUY&type=MARKET&quantity=${QUANTITY}&timestamp=${TIMESTAMP}"
SIGNATURE=$(echo -n "$QUERY" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2)

curl -s -X POST "https://api.binance.com/api/v3/order?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq '.'
```

### Sell (Market)
```bash
SYMBOL="ETHUSDT"
QUANTITY="0.1"

TIMESTAMP=$(date +%s%3N)
QUERY="symbol=${SYMBOL}&side=SELL&type=MARKET&quantity=${QUANTITY}&timestamp=${TIMESTAMP}"
SIGNATURE=$(echo -n "$QUERY" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2)

curl -s -X POST "https://api.binance.com/api/v3/order?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq '.'
```

## 🔧 Utilities

### View Open Orders
```bash
TIMESTAMP=$(date +%s%3N)
QUERY="timestamp=${TIMESTAMP}"
SIGNATURE=$(echo -n "$QUERY" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2)

# Futures
curl -s "https://fapi.binance.com/fapi/v1/openOrders?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq '.'
```

### Cancel Order
```bash
SYMBOL="BTCUSDT"
ORDER_ID="123456789"

TIMESTAMP=$(date +%s%3N)
QUERY="symbol=${SYMBOL}&orderId=${ORDER_ID}&timestamp=${TIMESTAMP}"
SIGNATURE=$(echo -n "$QUERY" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2)

curl -s -X DELETE "https://fapi.binance.com/fapi/v1/order?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq '.'
```

### View Trade History
```bash
SYMBOL="BTCUSDT"
TIMESTAMP=$(date +%s%3N)
QUERY="symbol=${SYMBOL}&timestamp=${TIMESTAMP}"
SIGNATURE=$(echo -n "$QUERY" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2)

curl -s "https://fapi.binance.com/fapi/v1/userTrades?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq '.[-10:]'
```

## 🏦 Detailed Futures Balance
```bash
TIMESTAMP=$(date +%s%3N)
QUERY="timestamp=${TIMESTAMP}"
SIGNATURE=$(echo -n "$QUERY" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2)

curl -s "https://fapi.binance.com/fapi/v2/balance?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq '[.[] | select(.balance != "0")]'
```

## 📋 Popular Pairs

| Pair | Description |
|------|-------------|
| BTCUSDT | Bitcoin |
| ETHUSDT | Ethereum |
| BNBUSDT | BNB |
| SOLUSDT | Solana |
| XRPUSDT | XRP |
| DOGEUSDT | Dogecoin |
| ADAUSDT | Cardano |
| AVAXUSDT | Avalanche |

## ⚠️ Safety Rules

1. **ALWAYS** verify position before closing
2. **ALWAYS** set Stop Loss on leveraged trades
3. **NEVER** use leverage higher than 10x without experience
4. **VERIFY** pair and quantity before executing
5. **CONFIRM** with user before executing large orders

## 🔗 Links

- [API Documentation](https://binance-docs.github.io/apidocs/)
- [Create Account (Support Tekkal)](https://www.binance.com/referral/earn-together/refer2earn-usdc/claim?hl=en&ref=GRO_28502_YLP17&utm_source=default)
- [Testnet](https://testnet.binance.vision/)

---
*Skill customized for Tekkal*
