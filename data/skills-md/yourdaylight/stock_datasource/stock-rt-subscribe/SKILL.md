---
name: stock-rt-subscribe
description: Subscribe to real-time stock market data via WebSocket (A-shares, HK stocks, ETFs). Use this skill when the user wants to monitor live stock prices, set up real-time alerts, or stream minute-level K-line data. Requires a valid real-time subscription token purchased from the management platform.
---

# Real-time Stock Data Subscription

Subscribe to live stock market data with 1.5-second K-line updates via WebSocket.

## Prerequisites

This skill requires:

1. **STOCK_RT_TOKEN** environment variable — a JWT token from a real-time subscription plan
2. **STOCK_RT_WS_URL** environment variable — the WebSocket endpoint URL (provided at purchase time)

## Setup Check

```bash
# Check if token exists
echo ${STOCK_RT_TOKEN:+Token is set}${STOCK_RT_TOKEN:-ERROR: STOCK_RT_TOKEN not set}
echo ${STOCK_RT_WS_URL:+WS URL is set}${STOCK_RT_WS_URL:-ERROR: STOCK_RT_WS_URL not set}
```

If not set:

1. Visit the management platform (nps_enhanced web panel)
2. Navigate to "Real-time Stock Subscription" page
3. Choose a plan based on how many symbols you need to track:
   - Pack 5: 5 symbols, 10 CNY/month
   - Pack 15: 15 symbols, 20 CNY/month
   - Pack 50: 50 symbols, 50 CNY/month
4. Select a node that supports real-time stock data
5. Complete purchase and copy the token + WebSocket URL
6. Set environment variables:
   ```bash
   export STOCK_RT_TOKEN="eyJ..."
   export STOCK_RT_WS_URL="wss://your-node:8443/ws/stock"
   ```

## Subscription Plans

| Plan | Symbols | Markets | Price |
|------|---------|---------|-------|
| Pack 5 (Entry) | 5 | A-shares + HK | 10 CNY/month |
| Pack 15 (Standard) | 15 | A-shares + HK | 20 CNY/month |
| Pack 50 (Pro) | 50 | A-shares + HK | 50 CNY/month |

All plans include ETF data. Symbol quota stacks when renewing.

## WebSocket Connection

Connect to the WebSocket endpoint with your token:

```
WebSocket URL: ${STOCK_RT_WS_URL}
Authorization: Bearer ${STOCK_RT_TOKEN}
```

### Message Protocol

**Subscribe to symbols:**
```json
{
  "action": "subscribe",
  "symbols": ["000001.SZ", "600519.SH", "00700.HK"]
}
```

**Unsubscribe:**
```json
{
  "action": "unsubscribe",
  "symbols": ["000001.SZ"]
}
```

**Real-time data format (pushed every ~1.5s):**
```json
{
  "type": "kline",
  "symbol": "000001.SZ",
  "data": {
    "open": 10.50,
    "high": 10.55,
    "low": 10.48,
    "close": 10.52,
    "volume": 123456,
    "amount": 1298765.00,
    "timestamp": "2026-03-08T14:30:01.500Z"
  }
}
```

## Data Characteristics

- **Update Frequency**: ~1.5 seconds during market hours
- **Markets**: CN (A-shares), HK (Hong Kong)
- **Data Retention**: Real-time stream via Redis (72-hour window), minute-level data persisted to ClickHouse
- **Latency**: Depends on network and node location

## Token Scope

The JWT token contains:
- **markets**: Which markets you can access (e.g., `["CN", "HK"]`)
- **levels**: Data levels (e.g., `["L1"]`)
- **quota.max_subs**: Maximum concurrent symbol subscriptions

## Troubleshooting

- **WebSocket connection refused**: Check that the node supports real-time data and the WS URL is correct
- **401 on connect**: Token expired or invalid. Check subscription status on the management platform
- **No data after subscribe**: Verify the market is currently open; no data is pushed during closed hours
- **Max subscriptions reached**: You've hit your symbol quota. Upgrade your plan or unsubscribe from some symbols
