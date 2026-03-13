---
name: trading-operations
description: Daily trading operations, monitoring, troubleshooting, deployment, and system health checks. Use when starting trading sessions, monitoring strategies, troubleshooting issues, checking system status, or deploying strategies.
---

# Trading Operations

## Daily Startup Checklist

### 1. Start OpenAlgo Server

**KiteConnect Instance (Port 5001 - NSE/MCX):**
```bash
cd /Users/mac/dyad-apps/probable-fiesta/openalgo
./QUICK_START.sh
```

**Or manually:**
```bash
cd /Users/mac/dyad-apps/probable-fiesta/openalgo
source /Users/mac/dyad-apps/openalgo/venv/bin/activate
bash start.sh
```

**Dhan Instance (Port 5002 - Options):**
```bash
cd /Users/mac/dyad-apps/probable-fiesta/openalgo
bash scripts/start_dhan_port5002_final.sh
```

### 2. Verify Server Status

**Quick Status Check:**
```bash
cd /Users/mac/dyad-apps/probable-fiesta/openalgo
./CHECK_STATUS.sh
```

**Detailed Health Check:**
```bash
cd /Users/mac/dyad-apps/probable-fiesta/openalgo
source /Users/mac/dyad-apps/openalgo/venv/bin/activate
python3 scripts/authentication_health_check.py
```

### 3. Check Broker Authentication

**KiteConnect (Port 5001):**
- Open: http://127.0.0.1:5001/auth/broker
- If token expired, reconnect Zerodha

**Dhan (Port 5002):**
- Open: http://127.0.0.1:5002/auth/broker
- Verify login status

### 4. Verify Strategies

**Strategy Dashboard:**
- Open: http://127.0.0.1:5001/python (KiteConnect strategies)
- Open: http://127.0.0.1:5002/python (Dhan strategies)
- Verify all strategies are enabled
- Check schedules: 09:30-15:15 IST

### 5. Monitor Dashboard

**Main Dashboard:**
- Open: http://127.0.0.1:5001/dashboard
- Check positions, orders, PnL

## Monitoring

### Real-Time Monitoring

**Check Strategy Logs:**
```bash
cd /Users/mac/dyad-apps/probable-fiesta/openalgo
tail -f logs/strategy_*.log | grep -E "\[ENTRY\]|\[EXIT\]|\[REJECTED\]|\[ERROR\]"
```

**Monitor All Strategy Logs:**
```bash
cd /Users/mac/dyad-apps/probable-fiesta/openalgo
bash scripts/check_all_strategy_logs.sh
```

**Check Positions:**
```bash
curl http://127.0.0.1:5001/positions | jq
```

**Check Orders:**
```bash
curl http://127.0.0.1:5001/orderbook | jq
```

### Key Endpoints

| Endpoint | Purpose | Port |
|----------|----------|------|
| `/dashboard` | Main dashboard | 5001/5002 |
| `/python` | Strategy management | 5001/5002 |
| `/positions` | Current positions | 5001/5002 |
| `/orderbook` | Order status | 5001/5002 |
| `/auth/broker` | Broker authentication | 5001/5002 |
| `/health` | System health | 5001/5002 |

## Troubleshooting

### Strategies Not Running

**Check:**
1. Server is running: `lsof -i :5001` or `lsof -i :5002`
2. Strategies are enabled in `/python` dashboard
3. Market hours: 09:15-15:30 IST (weekdays only)
4. API key is configured: Check `OPENALGO_APIKEY` env var

**Fix:**
```bash
# Restart specific strategy
curl -X POST http://127.0.0.1:5001/api/v1/strategy/restart \
  -H "Content-Type: application/json" \
  -d '{"strategy": "strategy_name"}'
```

### No Orders Being Placed

**Common Causes:**
1. Entry conditions too strict (check logs for `[REJECTED]`)
2. Risk limits blocking entries (portfolio heat limit)
3. API connectivity issues
4. Market closed or outside trading hours

**Diagnosis:**
```bash
# Check strategy logs for rejection reasons
grep "\[REJECTED\]" logs/strategy_*.log

# Check risk limits
curl http://127.0.0.1:5001/risk | jq
```

### 403 Errors

**Fix 403 errors:**
```bash
cd /Users/mac/dyad-apps/probable-fiesta/openalgo
python3 scripts/fix_403_strategies.py
```

**Restart affected strategies:**
```bash
bash scripts/restart_403_strategies.sh
```

### Authentication Issues

**KiteConnect Token Expired:**
1. Go to http://127.0.0.1:5001/auth/broker
2. Click "Reconnect Zerodha"
3. Complete OAuth flow

**Dhan Login Issues:**
- Check: `openalgo/DHAN_LOGIN_TROUBLESHOOTING.md`
- Verify credentials in `.env` file
- Check port 5002 is not blocked

## Deployment

### Deploy Ranked Strategies

After backtesting and ranking:

```bash
cd /Users/mac/dyad-apps/probable-fiesta/openalgo/strategies
bash scripts/deploy_ranked_strategies.sh
```

This script:
1. Reads backtest ranking results
2. Enables top-ranked strategies
3. Configures parameters from optimization
4. Sets up monitoring

### Manual Strategy Deployment

**Enable Strategy:**
```bash
curl -X POST http://127.0.0.1:5001/api/v1/strategy/enable \
  -H "Content-Type: application/json" \
  -d '{
    "strategy": "strategy_name",
    "symbol": "NIFTY",
    "params": {
      "risk_per_trade": 0.02,
      "stop_loss_pct": 1.5
    }
  }'
```

**Configure Schedule:**
- Set trading hours: 09:30-15:15 IST
- Set check interval: 60 seconds (or as needed)
- Configure market hours filter

## Emergency Procedures

### Emergency Stop

**Immediate Actions:**
1. Go to http://127.0.0.1:5001/python → Toggle OFF all strategies
2. Go to http://127.0.0.1:5001/positions → Close all positions
3. Stop server: `lsof -i :5001` then `kill <PID>`

**Kill Switch API:**
```bash
curl -X POST http://127.0.0.1:5001/api/v1/flatten
```

### Position Flattening

**Close All Positions:**
```bash
curl -X POST http://127.0.0.1:5001/api/v1/positions/flatten \
  -H "Content-Type: application/json" \
  -d '{"exchange": "NSE"}'
```

**Close Specific Symbol:**
```bash
curl -X POST http://127.0.0.1:5001/api/v1/positions/close \
  -H "Content-Type: application/json" \
  -d '{"symbol": "NIFTY", "exchange": "NSE"}'
```

## Daily Shutdown

### Backup Settings

**Save Settings:**
```bash
cd /Users/mac/dyad-apps/probable-fiesta/openalgo
./QUICK_BACKUP.sh
```

**Or manually:**
```bash
python3 scripts/backup_settings.py
```

**List Backups:**
```bash
python3 scripts/list_backups.py
```

**Restore Settings:**
```bash
python3 scripts/restore_settings.py
```

### End of Day Checklist

1. ✅ All positions closed (or verified as intended)
2. ✅ Settings backed up
3. ✅ Logs reviewed for errors
4. ✅ Strategy performance noted
5. ✅ Server stopped (optional, can run 24/7)

## Market Hours

**NSE/MCX Trading Hours:**
- Market Open: 09:15 IST
- Trading Window: 09:30-15:15 IST (strategies active)
- Market Close: 15:30 IST
- Token Expiry: 03:00 IST (daily)

**MCX Trading Hours:**
- Extended hours: 09:00-23:30 IST
- Check specific commodity trading hours

## Port Configuration

**Dual OpenAlgo Setup:**

| Port | Broker | Purpose | Strategies |
|------|--------|---------|------------|
| 5001 | KiteConnect | NSE/MCX | Equity, MCX strategies |
| 5002 | Dhan | Options | Options strategies, rankers |

**Strategy Routing:**
- NSE/MCX strategies → `http://127.0.0.1:5001`
- Options strategies → `http://127.0.0.1:5002`

## Log Analysis

### Key Log Patterns

**Entry Signals:**
```bash
grep "\[ENTRY\]" logs/strategy_*.log
```

**Exit Signals:**
```bash
grep "\[EXIT\]" logs/strategy_*.log
```

**Rejections:**
```bash
grep "\[REJECTED\]" logs/strategy_*.log
```

**Errors:**
```bash
grep -E "ERROR|Exception|Traceback" logs/strategy_*.log
```

### Log Locations

- Strategy logs: `openalgo/logs/strategy_*.log`
- Server logs: `openalgo/logs/server.log`
- Error logs: `openalgo/logs/error.log`

## Additional Resources

- Quick start: `START_HERE.md`
- Setup guide: `OPENALGO_LIVE_TRADING_SETUP.md`
- Paper trading: `PAPER_TRADING_GUIDE.md`
- Troubleshooting: `openalgo/DHAN_LOGIN_TROUBLESHOOTING.md`
- Status scripts: `openalgo/scripts/check_all_strategy_logs.sh`
