---
name: newsclawd
description: News and alert monitoring skill for OpenClaw. Monitors X/Twitter accounts, crypto prices, web news RSS feeds, and sends alerts when important events occur. Use when the user wants to track news, get price alerts, monitor specific Twitter accounts, or set up automated notifications for topics they care about.
---

# NewsClawd 🦞📰

Automated news monitoring and alerting system for your personal AI assistant.

## What It Does

- **X/Twitter Monitoring**: Track specific accounts, keywords, hashtags
- **Crypto Price Alerts**: Binance integration for price thresholds  
- **RSS News Feeds**: Monitor blogs, news sites, subreddits
- **Web Scraping**: Check websites for changes
- **Smart Filtering**: AI-powered relevance scoring
- **Multi-Channel Alerts**: Telegram, Discord, email notifications

## When to Use

- User says "monitor X for Y" or "alert me when..."
- User wants price alerts on crypto
- User wants to track specific Twitter accounts
- User mentions "news about..." or "keep me updated on..."
- Setting up cron-based monitoring jobs

## Core Components

### 1. Quick Monitoring Setup

```bash
# Monitor a Twitter account
newsclawd twitter --account @elonmusk --keywords "AI,tesla,spacex"

# Set crypto price alert
newsclawd crypto --symbol BTCUSDT --above 70000 --below 60000

# RSS feed monitoring
newsclawd rss --url https://feeds.bbci.co.uk/news/rss.xml --keywords "AI,technology"

# Website change detection
newsclawd web --url https://example.com --selector ".price" --interval 1h
```

### 2. Configuration

Config stored in `~/.config/newsclawd/config.json`:

```json
{
  "alerts": [
    {
      "type": "twitter",
      "account": "@notabanker1",
      "keywords": ["crypto", "AI"],
      "enabled": true
    },
    {
      "type": "crypto",
      "symbol": "BTCUSDT",
      "above": 70000,
      "below": 60000
    }
  ],
  "notifications": {
    "telegram": true,
    "discord": false,
    "email": false
  }
}
```

### 3. Cron Integration

Set up automated checks:

```bash
# Every 5 minutes for crypto
*/5 * * * * newsclawd check crypto

# Every hour for news
0 * * * * newsclawd check rss

# Every 15 min for Twitter
*/15 * * * * newsclawd check twitter
```

Use `openclaw cron add` to schedule these.

## Alert Types

### Twitter/X Alerts
- New tweets from followed accounts
- Keyword mentions in home timeline
- Trending topics in specific areas
- Reply/mention notifications

### Crypto Alerts
- Price above/below thresholds
- 24h change percentage
- Volume spikes
- New listings

### RSS/Web Alerts
- New articles matching keywords
- Website content changes
- Price/product availability
- API status changes

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `monitor.py` | Main monitoring daemon |
| `twitter.py` | X/Twitter checks (requires bird CLI) |
| `crypto.py` | Binance price checks |
| `rss.py` | RSS feed parsing |
| `web.py` | Website change detection |
| `notify.py` | Send alerts via configured channels |

## Usage Examples

### Example 1: Crypto Price Alert
```bash
# User: "Alert me if BTC drops below 60k or goes above 70k"
python3 scripts/crypto.py --symbol BTCUSDT --below 60000 --above 70000
```

### Example 2: Twitter Account Monitor
```bash
# User: "Watch @matrixdotorg for any matrix updates"
python3 scripts/twitter.py --account @matrixdotorg --keywords "update,release,security"
```

### Example 3: News RSS Monitor
```bash
# User: "Keep me updated on AI news from TechCrunch"
python3 scripts/rss.py --url https://techcrunch.com/category/artificial-intelligence/feed/ --keywords "AI,LLM,OpenAI"
```

### Example 4: Website Change Detection
```bash
# User: "Tell me when the price on this product page changes"
python3 scripts/web.py --url "https://store.example.com/product/123" --selector ".price-amount" --interval 1h
```

## Integration with OpenClaw

When user requests monitoring:

1. Parse the request (what, where, thresholds)
2. Create/update config
3. Set up cron job if recurring
4. Confirm with user
5. Route alerts back to user's preferred channel

Alert format:
```
🚨 NewsClawd Alert

Type: Crypto Price
Asset: BTCUSDT
Trigger: Above $70,000
Current: $71,245 (+5.2% 24h)

Time: 2026-02-06 14:23 UTC
```

## Dependencies

- `bird` CLI for X/Twitter (optional)
- `python3-requests` for HTTP
- `python3-feedparser` for RSS (optional, can use built-in)
- Binance API key for crypto (optional, public endpoints work)

## Security Notes

- Store API keys in `~/.config/newsclawd/.env` (gitignored)
- Rotate Twitter cookies regularly
- Use read-only API keys where possible
- Rate limit all checks to avoid bans
