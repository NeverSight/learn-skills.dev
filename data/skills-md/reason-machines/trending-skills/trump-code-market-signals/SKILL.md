---
name: trump-code-market-signals
description: AI-powered analysis of Trump's social media posts to predict stock market movements using 31.5M brute-force tested rules
triggers:
  - analyze trump posts for market signals
  - run trump code prediction
  - check today's trading signals from trump
  - decode trump truth social posts
  - trump market signal analysis
  - run overnight brute force model search
  - check surviving trading rules
  - trump code cli predict

---

# Trump Code — Market Signal Analysis

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Trump Code is an open-source system that applies brute-force computation to find statistically significant patterns between Trump's Truth Social/X posting behavior and S&P 500 movements. It has tested 31.5M model combinations, maintains 551 surviving rules, and has a verified 61.3% hit rate across 566 predictions (z=5.39, p<0.05).

## Installation

```bash
git clone https://github.com/sstklen/trump-code.git
cd trump-code
pip install -r requirements.txt
```

### Environment Variables

```bash
# Required for AI briefing and chatbot
export GEMINI_KEYS="key1,key2,key3"       # Comma-separated Gemini API keys

# Optional: for Claude Opus deep analysis
export ANTHROPIC_API_KEY="your-key-here"

# Optional: for Polymarket/Kalshi integration
export POLYMARKET_API_KEY="your-key-here"
```

## CLI — Key Commands

```bash
# Today's detected signals from Trump's posts
python3 trump_code_cli.py signals

# Model performance leaderboard (all 11 named models)
python3 trump_code_cli.py models

# Get LONG/SHORT consensus prediction
python3 trump_code_cli.py predict

# Prediction market arbitrage opportunities
python3 trump_code_cli.py arbitrage

# System health check (circuit breaker state)
python3 trump_code_cli.py health

# Full daily report (trilingual)
python3 trump_code_cli.py report

# Dump all data as JSON
python3 trump_code_cli.py json
```

## Core Scripts

```bash
# Real-time Trump post monitor (polls every 5 min)
python3 realtime_loop.py

# Brute-force model search (~25 min, tests millions of combos)
python3 overnight_search.py

# Individual analyses
python3 analysis_06_market.py        # Posts vs S&P 500 correlation
python3 analysis_09_combo_score.py   # Multi-signal combo scoring

# Web dashboard + AI chatbot on port 8888
export GEMINI_KEYS="key1,key2,key3"
python3 chatbot_server.py
# → http://localhost:8888
```

## REST API (Live at trumpcode.washinmura.jp)

```python
import requests

BASE = "https://trumpcode.washinmura.jp"

# All dashboard data in one call
data = requests.get(f"{BASE}/api/dashboard").json()

# Today's signals + 7-day history
signals = requests.get(f"{BASE}/api/signals").json()

# Model performance rankings
models = requests.get(f"{BASE}/api/models").json()

# Latest 20 Trump posts with signal tags
posts = requests.get(f"{BASE}/api/recent-posts").json()

# Live Polymarket Trump prediction markets (316+)
markets = requests.get(f"{BASE}/api/polymarket-trump").json()

# LONG/SHORT playbooks
playbook = requests.get(f"{BASE}/api/playbook").json()

# System health / circuit breaker state
status = requests.get(f"{BASE}/api/status").json()
```

### AI Chatbot API

```python
import requests

response = requests.post(
    "https://trumpcode.washinmura.jp/api/chat",
    json={"message": "What signals fired today and what's the consensus?"}
)
print(response.json()["reply"])
```

## MCP Server (Claude Code / Cursor Integration)

Add to `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "trump-code": {
      "command": "python3",
      "args": ["/path/to/trump-code/mcp_server.py"]
    }
  }
}
```

Available MCP tools: `signals`, `models`, `predict`, `arbitrage`, `health`, `events`, `dual_platform`, `crowd`, `full_report`

## Open Data Files

All data lives in `data/` and is updated daily:

```python
import json, pathlib

DATA = pathlib.Path("data")

# 44,000+ Truth Social posts
posts = json.loads((DATA / "trump_posts_all.json").read_text())

# Posts with signals pre-tagged
posts_lite = json.loads((DATA / "trump_posts_lite.json").read_text())

# 566 verified predictions with outcomes
predictions = json.loads((DATA / "predictions_log.json").read_text())

# 551 active rules (brute-force + evolved)
rules = json.loads((DATA / "surviving_rules.json").read_text())

# 384 features × 414 trading days
features = json.loads((DATA / "daily_features.json").read_text())

# S&P 500 OHLC history
market = json.loads((DATA / "market_SP500.json").read_text())

# Circuit breaker / system health
cb = json.loads((DATA / "circuit_breaker_state.json").read_text())

# Rule evolution log (crossover/mutation)
evo = json.loads((DATA / "evolution_log.json").read_text())
```

## Download Data via API

```python
import requests

BASE = "https://trumpcode.washinmura.jp"

# List available datasets
catalog = requests.get(f"{BASE}/api/data").json()

# Download a specific file
raw = requests.get(f"{BASE}/api/data/surviving_rules.json").content
rules = json.loads(raw)
```

## Real Code Examples

### Parse Today's Signals

```python
import requests

signals_data = requests.get("https://trumpcode.washinmura.jp/api/signals").json()

today = signals_data.get("today", {})
print("Signals fired today:", today.get("signals", []))
print("Consensus:", today.get("consensus"))        # "LONG" / "SHORT" / "NEUTRAL"
print("Confidence:", today.get("confidence"))      # 0.0–1.0
print("Active models:", today.get("active_models", []))
```

### Find Top Performing Rules from Surviving Rules

```python
import json

rules = json.loads(open("data/surviving_rules.json").read())

# Sort by hit rate descending
top_rules = sorted(rules, key=lambda r: r.get("hit_rate", 0), reverse=True)

for rule in top_rules[:10]:
    print(f"Rule: {rule['id']} | Hit Rate: {rule['hit_rate']:.1%} | "
          f"Trades: {rule['n_trades']} | Avg Return: {rule['avg_return']:.3%}")
```

### Check Prediction Market Opportunities

```python
import requests

arb = requests.get("https://trumpcode.washinmura.jp/api/insights").json()
markets = requests.get("https://trumpcode.washinmura.jp/api/polymarket-trump").json()

# Markets sorted by volume
active = [m for m in markets.get("markets", []) if m.get("active")]
by_volume = sorted(active, key=lambda m: m.get("volume", 0), reverse=True)

for m in by_volume[:5]:
    print(f"{m['title']}: YES={m['yes_price']:.0%} | Vol=${m['volume']:,.0f}")
```

### Correlate Post Features with Returns

```python
import json
import numpy as np

features = json.loads(open("data/daily_features.json").read())
market   = json.loads(open("data/market_SP500.json").read())

# Build date-indexed return map
returns = {d["date"]: d["close_pct"] for d in market}

# Example: correlate post_count with next-day return
xs, ys = [], []
for day in features:
    date = day["date"]
    if date in returns:
        xs.append(day.get("post_count", 0))
        ys.append(returns[date])

correlation = np.corrcoef(xs, ys)[0, 1]
print(f"Post count vs same-day return: r={correlation:.3f}")
```

### Run a Backtest on a Custom Signal

```python
import json

posts    = json.loads(open("data/trump_posts_lite.json").read())
market   = json.loads(open("data/market_SP500.json").read())

returns  = {d["date"]: d["close_pct"] for d in market}

# Find days with RELIEF signal before 9:30 AM ET
relief_days = [
    p["date"] for p in posts
    if "RELIEF" in p.get("signals", []) and p.get("hour", 24) < 9
]

hits = [returns[d] for d in relief_days if d in returns]
if hits:
    print(f"RELIEF pre-market: n={len(hits)}, "
          f"avg={sum(hits)/len(hits):.3%}, "
          f"hit_rate={sum(1 for h in hits if h > 0)/len(hits):.1%}")
```

## Key Signal Types

| Signal | Description | Typical Impact |
|--------|-------------|----------------|
| `RELIEF` pre-market | "Relief" language before 9:30 AM | Avg +1.12% same-day |
| `TARIFF` market hours | Tariff mention during trading | Avg -0.758% next day |
| `DEAL` | Deal/agreement language | 52.2% hit rate |
| `CHINA` (Truth Social only) | China mentions (never on X) | 1.5× weight boost |
| `SILENCE` | Zero-post day | 80% bullish, avg +0.409% |
| Burst → silence | Rapid posting then goes quiet | 65.3% LONG signal |

## Model Reference

| Model | Strategy | Hit Rate | Avg Return |
|-------|----------|----------|------------|
| A3 | Pre-market RELIEF → surge | 72.7% | +1.206% |
| D3 | Volume spike → panic bottom | 70.2% | +0.306% |
| D2 | Signature switch → formal statement | 70.0% | +0.472% |
| C1 | Burst → long silence → LONG | 65.3% | +0.145% |
| C3 ⚠️ | Late-night tariff (anti-indicator) | 37.5% | −0.414% |

> **Note:** C3 is an anti-indicator — if it fires, the circuit breaker auto-inverts it to LONG (62% accuracy after inversion).

## System Architecture Flow

```
Truth Social post detected (every 5 min)
    → Classify signals (RELIEF / TARIFF / DEAL / CHINA / etc.)
    → Dual-platform boost (TS-only China = 1.5× weight)
    → Snapshot Polymarket + S&P 500
    → Run 551 surviving rules → generate prediction
    → Track at 1h / 3h / 6h
    → Verify outcome → update rule weights
    → Circuit breaker: if system degrades → pause/invert
    → Daily: evolve rules (crossover / mutation / distillation)
    → Sync data to GitHub
```

## Troubleshooting

**`realtime_loop.py` not detecting new posts**
- Check your network access to Truth Social scraper endpoints
- Verify `data/trump_posts_all.json` timestamp is recent
- Run `python3 trump_code_cli.py health` to see circuit breaker state

**`chatbot_server.py` fails to start**
- Ensure `GEMINI_KEYS` env var is set: `export GEMINI_KEYS="key1,key2"`
- Port 8888 may be in use: `lsof -i :8888`

**`overnight_search.py` runs out of memory**
- Runs ~31.5M combinations — needs ~4GB RAM
- Run on a machine with 8GB+ or reduce search space in script config

**Hit rate dropping below 55%**
- Check `data/circuit_breaker_state.json` — system may have auto-paused
- Review `data/learning_report.json` for demoted rules
- Re-run `overnight_search.py` to refresh surviving rules

**Stale data in `data/` directory**
- Daily pipeline syncs to GitHub automatically if running
- Manually trigger: `python3 trump_code_cli.py report` to force refresh
- Or pull latest from remote: `git pull origin main`
