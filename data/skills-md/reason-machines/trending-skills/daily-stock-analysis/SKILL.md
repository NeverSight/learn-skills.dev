---
name: daily-stock-analysis
description: LLM-powered A/H/US stock intelligent analysis system with multi-source data, real-time news, AI decision dashboards, and multi-channel push notifications via GitHub Actions.
triggers:
  - analyze stocks with AI
  - set up daily stock analysis
  - configure stock push notifications
  - add stocks to watch list
  - set up LLM stock analyzer
  - deploy stock analysis GitHub Actions
  - configure WeChat Telegram stock alerts
  - backtest stock analysis accuracy
---

# Daily Stock Analysis (股票智能分析系统)

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

LLM-powered stock analysis system for A-share, Hong Kong, and US markets. Automatically fetches quotes, news, and fundamentals, generates AI decision dashboards with buy/sell targets, and pushes results to WeChat/Feishu/Telegram/Discord/Email on a schedule via GitHub Actions — zero server cost.

## What It Does

- **AI Decision Dashboard**: One-line conclusion + precise buy/sell/stop-loss prices + checklist per stock
- **Multi-market**: A-shares (CN), HK stocks, US stocks + indices (SPX, DJI, IXIC)
- **Data sources**: AkShare, Tushare, YFinance for quotes; Tavily/SerpAPI/Brave for news
- **LLM backends**: Gemini, OpenAI, Claude, DeepSeek, Qwen via LiteLLM (unified)
- **Push channels**: WeChat Work, Feishu, Telegram, Discord, DingTalk, Email, PushPlus
- **Automation**: GitHub Actions cron schedule, no server needed
- **Web UI**: Portfolio management, history, backtesting, Agent Q&A
- **Agent**: Multi-turn strategy Q&A with 11 built-in strategies (MA crossover, Elliott Wave, etc.)

## Installation

### Method 1: GitHub Actions (Recommended, Zero Cost)

**Step 1: Fork the repository**
```
https://github.com/ZhuLinsen/daily_stock_analysis
```

**Step 2: Configure Secrets** (`Settings → Secrets and variables → Actions`)

**Required — at least one LLM key:**
```
GEMINI_API_KEY        # Google AI Studio (free tier available)
OPENAI_API_KEY        # OpenAI or compatible (DeepSeek, Qwen, etc.)
OPENAI_BASE_URL       # e.g. https://api.deepseek.com/v1
OPENAI_MODEL          # e.g. deepseek-chat, gpt-4o
AIHUBMIX_KEY          # AIHubMix (recommended, covers Gemini+GPT+Claude+DeepSeek)
ANTHROPIC_API_KEY     # Claude
```

**Required — stock list:**
```
STOCKS                # e.g. 600519,300750,AAPL,TSLA,00700.HK
```

**Required — at least one notification channel:**
```
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID
FEISHU_WEBHOOK_URL
WECHAT_WEBHOOK_URL
EMAIL_SENDER / EMAIL_PASSWORD / EMAIL_RECEIVERS
DISCORD_WEBHOOK_URL
```

**Step 3: Trigger manually or wait for cron**

Go to `Actions → stock_analysis → Run workflow`

---

### Method 2: Local / Docker

```bash
git clone https://github.com/ZhuLinsen/daily_stock_analysis
cd daily_stock_analysis
cp .env.example .env
# Edit .env with your keys
pip install -r requirements.txt
python main.py
```

**Docker:**
```bash
docker build -t stock-analysis .
docker run --env-file .env stock-analysis
```

**Docker Compose:**
```bash
docker-compose up -d
```

## Configuration

### `.env` File (Local)

```env
# LLM - pick one or more
GEMINI_API_KEY=your_gemini_key
OPENAI_API_KEY=your_openai_key
OPENAI_BASE_URL=https://api.deepseek.com/v1
OPENAI_MODEL=deepseek-chat
AIHUBMIX_KEY=your_aihubmix_key

# Stock list (comma-separated)
STOCKS=600519,300750,AAPL,TSLA,00700.HK

# Notification
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# Optional settings
REPORT_TYPE=full           # simple | full | brief
ANALYSIS_DELAY=10          # seconds between stocks (avoid rate limiting)
MAX_WORKERS=3              # concurrent analysis threads
SINGLE_STOCK_NOTIFY=false  # push each stock immediately when done
NEWS_MAX_AGE_DAYS=3        # ignore news older than N days
```

### Multi-Channel LLM (Advanced)

```env
LLM_CHANNELS=gemini,deepseek,claude
LLM_GEMINI_PROTOCOL=google
LLM_GEMINI_API_KEY=your_key
LLM_GEMINI_MODELS=gemini-2.0-flash,gemini-1.5-pro
LLM_GEMINI_ENABLED=true

LLM_DEEPSEEK_PROTOCOL=openai
LLM_DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
LLM_DEEPSEEK_API_KEY=your_key
LLM_DEEPSEEK_MODELS=deepseek-chat
LLM_DEEPSEEK_ENABLED=true
```

### Stock Grouping (Send Different Stocks to Different Emails)

```env
STOCK_GROUP_1=600519,300750,000858
EMAIL_GROUP_1=investor1@example.com

STOCK_GROUP_2=AAPL,TSLA,NVDA
EMAIL_GROUP_2=investor2@example.com
```

### Market Review Mode

```env
MARKET_REVIEW=cn      # cn | us | both
# cn = A-share three-phase review strategy
# us = US Regime Strategy (risk-on/neutral/risk-off)
# both = both markets
```

## Key Commands (CLI)

```bash
# Run full analysis immediately
python main.py

# Analyze specific stocks only
STOCKS=600519,AAPL python main.py

# Run web dashboard
python web_app.py
# Access at http://localhost:5000

# Run with Docker (env file)
docker run --env-file .env stock-analysis python main.py

# Run schedule mode (waits for cron, then runs)
SCHEDULE_RUN_IMMEDIATELY=true python main.py
```

## GitHub Actions Workflow

The workflow file `.github/workflows/stock_analysis.yml` runs on schedule:

```yaml
# Default schedule - customize in the workflow file
on:
  schedule:
    - cron: '30 1 * * 1-5'   # 9:30 AM CST (UTC+8) weekdays
  workflow_dispatch:          # manual trigger
```

**To change schedule:** Edit `.github/workflows/stock_analysis.yml` cron expression.

**To add secrets via GitHub CLI:**
```bash
gh secret set GEMINI_API_KEY --body "$GEMINI_API_KEY"
gh secret set STOCKS --body "600519,300750,AAPL,TSLA"
gh secret set TELEGRAM_BOT_TOKEN --body "$TG_TOKEN"
gh secret set TELEGRAM_CHAT_ID --body "$TG_CHAT_ID"
```

## Code Examples

### Programmatic Analysis (Python)

```python
# Run analysis for specific stocks programmatically
import asyncio
from analyzer import StockAnalyzer

async def analyze():
    analyzer = StockAnalyzer()
    
    # Analyze a single A-share stock
    result = await analyzer.analyze_stock("600519")  # Moutai
    print(result['conclusion'])
    print(result['buy_price'])
    print(result['stop_loss'])
    print(result['target_price'])

asyncio.run(analyze())
```

### Custom Notification Integration

```python
from notifier import NotificationManager

notifier = NotificationManager()

# Send to Telegram
await notifier.send_telegram(
    token=os.environ['TELEGRAM_BOT_TOKEN'],
    chat_id=os.environ['TELEGRAM_CHAT_ID'],
    message="📈 Analysis complete\n600519: BUY at 1680, SL: 1620, TP: 1800"
)

# Send to Feishu webhook
await notifier.send_feishu(
    webhook_url=os.environ['FEISHU_WEBHOOK_URL'],
    content=analysis_report
)
```

### Using the Agent API

```python
import requests

# Ask the stock agent a strategy question
response = requests.post('http://localhost:5000/api/agent/chat', json={
    "message": "600519现在适合买入吗？用均线金叉策略分析",
    "stock_code": "600519",
    "strategy": "ma_crossover"  # ma_crossover, elliott_wave, chan_theory, etc.
})

print(response.json()['reply'])
```

### Backtest Analysis Accuracy

```python
import requests

# Trigger backtest for a stock
response = requests.post('http://localhost:5000/api/backtest', json={
    "stock_code": "600519",
    "days": 30  # evaluate last 30 days of AI predictions
})

result = response.json()
print(f"Direction accuracy: {result['direction_accuracy']}%")
print(f"Take-profit hit rate: {result['tp_hit_rate']}%")
print(f"Stop-loss hit rate: {result['sl_hit_rate']}%")
```

### Import Stocks from Image (Vision LLM)

```python
import requests

# Upload screenshot of stock list for AI extraction
with open('watchlist_screenshot.png', 'rb') as f:
    response = requests.post(
        'http://localhost:5000/api/stocks/import/image',
        files={'image': f}
    )

stocks = response.json()['extracted_stocks']
# Returns: [{"code": "600519", "name": "贵州茅台", "confidence": 0.98}, ...]
```

## Web Dashboard Features

Start the web app:
```bash
python web_app.py
```

| Route | Feature |
|-------|---------|
| `/` | Today's analysis dashboard |
| `/portfolio` | Holdings management, P&L tracking |
| `/history` | Past analysis reports (bulk delete supported) |
| `/backtest` | AI prediction accuracy backtest |
| `/agent` | Multi-turn strategy Q&A |
| `/settings` | LLM channels, notification config |
| `/import` | Import stocks from image/CSV/clipboard |

## Supported Stock Formats

```
# A-shares (6-digit code)
600519    # 贵州茅台
300750    # 宁德时代
000858    # 五粮液

# HK stocks (5-digit + .HK)
00700.HK  # 腾讯控股
09988.HK  # 阿里巴巴

# US stocks (ticker)
AAPL
TSLA
NVDA

# US indices
SPX       # S&P 500
DJI       # Dow Jones
IXIC      # NASDAQ
```

## Built-in Trading Rules

| Rule | Config |
|------|--------|
| No chasing highs | `DEVIATION_THRESHOLD=5` (%, auto-relaxed for strong trend) |
| Trend trading | MA5 > MA10 > MA20 bullish alignment required |
| Precise targets | Buy price, stop-loss, take-profit per stock |
| News freshness | `NEWS_MAX_AGE_DAYS=3` (skip stale news) |
| Checklist | Each condition marked: ✅ Satisfied / ⚠️ Caution / ❌ Not Met |

## Troubleshooting

**Analysis runs but no push received:**
```bash
# Check notification config
python -c "from notifier import test_all_channels; test_all_channels()"

# Verify secrets are set (GitHub Actions)
gh secret list
```

**LLM API errors / rate limiting:**
```env
ANALYSIS_DELAY=15        # increase delay between stocks
MAX_WORKERS=1            # reduce concurrency
LITELLM_FALLBACK_MODELS=gemini-1.5-flash,deepseek-chat  # add fallbacks
```

**AkShare data fetch fails (A-shares):**
```bash
pip install akshare --upgrade
# A-share data requires Chinese network or proxy
```

**YFinance US stock data issues:**
```bash
pip install yfinance --upgrade
# US stocks use YFinance exclusively for consistency
```

**GitHub Actions not triggering:**
- Check Actions are enabled: `Settings → Actions → General → Allow all actions`
- Verify cron syntax at [crontab.guru](https://crontab.guru)
- Check workflow file exists: `.github/workflows/stock_analysis.yml`

**Web auth issues (admin password):**
```env
# If auth was disabled and re-enabled, current password required
# Reset via environment variable
WEB_ADMIN_PASSWORD=new_password
```

**Multi-worker deployment auth state:**
```bash
# Auth toggle only applies to current process
# Must restart all workers to sync state
docker-compose restart
```

## Report Types

```env
REPORT_TYPE=simple   # Concise: conclusion + key prices only
REPORT_TYPE=full     # Complete: all technical + fundamental + news analysis
REPORT_TYPE=brief    # 3-5 sentence summary
```

**Full report includes:**
- 一句话核心结论 (one-line core conclusion)
- 技术面分析 (technical: MA alignment, chip distribution)
- 基本面 (valuation, growth, earnings, institutional holdings)
- 舆情情报 (news sentiment, social media — US stocks)
- 精确买卖点位 (precise entry/exit levels)
- 操作检查清单 (action checklist)
- 板块涨跌榜 (sector performance boards)

## LLM Priority Order

```
Gemini → Anthropic → OpenAI/AIHubMix/Compatible
```

AIHubMix is recommended for single-key access to all major models without VPN:
```env
AIHUBMIX_KEY=$AIHUBMIX_KEY  # covers Gemini, GPT, Claude, DeepSeek
# No OPENAI_BASE_URL needed — auto-configured
```
