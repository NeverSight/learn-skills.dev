---
name: gate-news-briefing
version: "2026.3.12-1"
updated: "2026-03-12"
description: "News briefing. Use this skill whenever the user asks for recent news or headlines. Trigger phrases include: what happened recently, today's highlights, crypto news, any new updates. MCP tools: news_events_get_latest_events, news_feed_search_news, news_feed_get_social_sentiment."
---

# gate-news-briefing

> The crypto industry "morning briefing" Skill. The user asks what's been happening; the system calls 3 MCP Tools in parallel to fetch major events + trending news + social sentiment, then the LLM aggregates into a layered news briefing.

**Trigger Scenarios**: User asks about recent/today's news, headlines, or what's been happening.

---

## Routing Rules

| User Intent | Keywords | Action |
|-------------|----------|--------|
| General news briefing | "what happened recently" "today's headlines" "crypto news" "any new updates" | Execute this Skill's full workflow |
| Coin-specific news | "any SOL news" "what's happening with BTC" | Execute this Skill with `coin` parameter set to that coin |
| Reason for a move | "why did BTC crash" "what just happened" | Route to `gate-news-eventexplain` |
| Overall market conditions | "how's the market" | Route to `gate-info-marketoverview` |
| Exchange announcements | "any new listings on Binance" "new coins lately" | Route to `gate-news-listing` |

---

## Execution Workflow

### Step 1: Intent Recognition & Parameter Extraction

Extract from user input:
- `coin` (optional): Whether a specific coin is targeted, e.g., "SOL news" → coin=SOL
- `time_range`: Time window (default: 24h; if user says "this week" → 7d)
- `topic` (optional): Whether focused on a specific topic (e.g., "regulation", "ETF", "DeFi")

### Step 2: Call 3 MCP Tools in Parallel

**General Briefing Mode** (no specific coin):

| Step | MCP Tool | Parameters | Retrieved Data | Parallel |
|------|----------|------------|----------------|----------|
| 1a | `news_events_get_latest_events` | `time_range={time_range}, limit=10` | Major event list (with impact rating) | Yes |
| 1b | `news_feed_search_news` | `sort_by="importance", limit=10, lang="en"` | Top news ranked by importance | Yes |
| 1c | `news_feed_get_social_sentiment` | (no specific coin) | Market-wide social sentiment overview | Yes |

**Coin-Specific Mode** (user specified a coin):

| Step | MCP Tool | Parameters | Retrieved Data | Parallel |
|------|----------|------------|----------------|----------|
| 1a | `news_events_get_latest_events` | `coin={coin}, time_range={time_range}, limit=10` | Events related to that coin | Yes |
| 1b | `news_feed_search_news` | `coin={coin}, sort_by="importance", limit=10` | News related to that coin | Yes |
| 1c | `news_feed_get_social_sentiment` | `coin={coin}` | Social sentiment for that coin | Yes |

### Step 3: LLM Aggregation

The LLM must:
1. De-duplicate events and news (the same event may appear in both feeds)
2. Rank by impact/importance
3. Categorize (Regulation, Projects, Market, Technology, etc.)
4. Combine with social sentiment to identify market focus areas

### Step 4: Output Structured Briefing

---

## Report Template

```markdown
## Crypto Industry News Briefing

> Time range: Past {time_range} | Generated: {timestamp}

### 🔴 Major Events

{Top 1-3 events by impact, each containing:}

**1. {event_title}**
- Time: {event_time}
- Impact: {Market/industry impact assessment}
- Involved: {Related coins/projects/institutions}
- Details: {2-3 sentence summary}

**2. {event_title}**
- ...

---

### 📰 Trending News

{Grouped by category, 2-5 items per category:}

**Regulation & Policy**
1. {title} — {source} ({time})
   {One-sentence summary}
2. ...

**Projects & Technology**
1. {title} — {source} ({time})
   {One-sentence summary}
2. ...

**Market & Trading**
1. {title} — {source} ({time})
   {One-sentence summary}
2. ...

**DeFi / NFT / GameFi** (if applicable)
1. ...

---

### 💬 Social Sentiment

| Metric | Status |
|--------|--------|
| Overall Sentiment | {Bullish/Bearish/Neutral} |
| Discussion Volume | {High/Medium/Low} |
| Trending Topics | {topic1}, {topic2}, {topic3} |
| KOL Focus | {focus description} |

**Top 5 Coins by Discussion Volume** (if data available)

| Rank | Coin | Volume Change | Sentiment |
|------|------|--------------|-----------|
| 1 | {coin} | +{change}% | {Bullish/Bearish} |
| 2 | ... | ... | ... |

---

### 📌 Worth Watching

{LLM distills 2-3 noteworthy points from news and sentiment:}
- {Point 1}
- {Point 2}
- {Point 3}

> The above is a news summary and does not constitute investment advice.
```

### Coin-Specific Mode Template

```markdown
## {symbol} News Briefing

> Time range: Past {time_range} | Generated: {timestamp}

### Recent Key Events

1. {event} — {time}
   {details}
2. ...

### Related News

1. [{title}]({url}) — {source} ({time})
   {summary}
2. ...

### Social Sentiment

- Discussion Volume: {High/Medium/Low} (vs 7-day average: {change}%)
- Sentiment Bias: {Bullish/Bearish/Neutral}
- KOL Views: {Summary of key KOL opinions}

### Summary

{1-2 sentence summary of the coin's recent news landscape}
```

---

## De-duplication & Ranking Logic

| Rule | Description |
|------|-------------|
| Event-News de-duplication | If an event title closely matches a news headline (similarity > 80%), merge into one entry — events take priority |
| Importance ranking | Events ranked by impact rating; news ranked by `importance` field |
| Time ordering | At equal importance, reverse chronological (newest first) |
| Categorization | News auto-categorized: Regulation & Policy / Projects & Technology / Market & Trading / DeFi / Other |

---

## Error Handling

| Error Type | Handling |
|------------|----------|
| `news_events_get_latest_events` fails | Skip "Major Events" section; show news only |
| `news_feed_search_news` fails | Show events only; note "News feed temporarily unavailable" |
| `news_feed_get_social_sentiment` fails | Skip "Social Sentiment" section |
| All Tools fail | Return error message; suggest the user try again later |
| Too few news items (< 3) | Expand time range (e.g., 24h → 48h) and note the change |

---

## Cross-Skill Routing

| User Follow-up Intent | Route To |
|-----------------------|----------|
| "Why did XX pump/dump?" | `gate-news-eventexplain` |
| "Analyze XX for me" | `gate-info-coinanalysis` |
| "How's the overall market?" | `gate-info-marketoverview` |
| "Any new listings on Binance?" | `gate-news-listing` |
| "Tell me more about ETF" | Deep search via `news_feed_search_news(query="ETF")` |

---

## Safety Rules

1. **Source attribution**: Every news item must include the source (media name) and time
2. **No interpretive speculation**: News summaries must remain objective — no subjective extrapolation
3. **No fabricated news**: If data is insufficient, reduce the number of items rather than fabricate content
4. **Neutral handling of sensitive topics**: Maintain neutral tone when covering regulation, politics, or other sensitive subjects
5. **Timeliness labeling**: Clearly label the time range covered by the data
