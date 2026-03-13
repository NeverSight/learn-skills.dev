---
name: gate-news-eventexplain
version: "2026.3.12-1"
updated: "2026-03-12"
description: "Event attribution and explanation. Use this skill whenever the user asks for the reason behind a price move. Trigger phrases include: why did X crash, what just happened, why is it pumping, what caused. MCP tools: news_events_get_latest_events, info_marketsnapshot_get_market_snapshot, news_events_get_event_detail, info_onchain_get_token_onchain, news_feed_search_news."
---

# gate-news-eventexplain

> The "Why is it pumping/dumping?" Skill. When the market experiences abnormal volatility and the user asks why, the system traces the event source through multi-step calls, cross-references market data to verify impact magnitude, and delivers a complete "Event → Impact Chain → Market Reaction" analysis report.

**Trigger Scenarios**: User expresses curiosity about a market anomaly, e.g., "why did BTC crash", "what just happened", "why did ETH suddenly spike".

---

## Routing Rules

| User Intent | Keywords | Action |
|-------------|----------|--------|
| Reason for price move | "why pump" "why dump" "crash" "surge" "what caused" "what happened" | Execute this Skill's full workflow |
| General news query | "any recent news" | Route to `gate-news-briefing` |
| Comprehensive coin analysis | "analyze BTC for me" | Route to `gate-info-coinanalysis` |
| Technical analysis | "BTC technical analysis" | Route to `gate-info-trendanalysis` |
| Market overview | "how's the market" | Route to `gate-info-marketoverview` |

---

## Execution Workflow

### Step 1: Intent Recognition & Parameter Extraction

Extract from user input:
- `coin`: The coin involved (e.g., BTC, ETH; may be empty = overall market)
- `direction`: Up or down (aids search)
- `time_hint`: Time clue ("just now", "today", "yesterday"; default: past 24h)

### Step 2: Phase 1 — Event Search + Market Verification (Parallel)

| Step | MCP Tool | Parameters | Retrieved Data | Parallel |
|------|----------|------------|----------------|----------|
| 1a | `news_events_get_latest_events` | `coin={coin}, time_range="24h", limit=10` | Related event list | Yes |
| 1b | `info_marketsnapshot_get_market_snapshot` | `symbol={coin}, timeframe="1d", source="spot"` | Real-time market snapshot (verify volatility magnitude) | Yes |

> Both Tools called in parallel.

### Step 3: Decision Branch

```
events response
    │
    ├── Matching event found (event time aligns with volatility onset)
    │   └── → Step 4a: Get event details
    │
    └── No clear event match
        └── → Step 4b: Expand news search
```

### Step 4a: Event Found → Get Details + On-chain Verification

| Step | MCP Tool | Parameters | Retrieved Data | Parallel |
|------|----------|------------|----------------|----------|
| 2a | `news_events_get_event_detail` | `event_id={matched_event_id}` | Event details (cause, impact, timeline) | Yes |
| 2b | `info_onchain_get_token_onchain` | `token={coin}, chain="eth", scope="transfers"` | On-chain anomalies (large transfers, exchange inflows/outflows) | Yes |

### Step 4b: No Event Found → Expand Search

| Step | MCP Tool | Parameters | Retrieved Data | Parallel |
|------|----------|------------|----------------|----------|
| 2c | `news_feed_search_news` | `coin={coin}, sort_by="time", limit=15` | Latest related news (sorted by time) | Yes |
| 2d | `info_onchain_get_token_onchain` | `token={coin}, chain="eth", scope="transfers"` | On-chain anomalies | Yes |

### Step 5: LLM Attribution Reasoning

The LLM must complete the following reasoning chain:

1. **Confirm the volatility**: Based on the market snapshot, confirm the timing, magnitude, and volume change
2. **Identify the trigger event**: From events/news, find the event with the closest time alignment
3. **Verify causality**: Did the event precede the price move? Is there corresponding on-chain activity?
4. **Assess the impact chain**: Event → Direct impact → Sentiment transmission → Price reaction
5. **Evaluate follow-on potential**: Based on the event's nature, assess whether the impact is short-term or sustained

### Step 6: Output Structured Report

---

## Report Template

```markdown
## {coin} {Pump/Dump} Attribution Analysis

> Analysis time: {timestamp}

### 1. Volatility Summary

| Metric | Value |
|--------|-------|
| Current Price | ${price} |
| Move Magnitude | {change}% (within {timeframe}) |
| High | ${high} ({time}) |
| Low | ${low} ({time}) |
| Volume Change | {volume_change}% (vs 24h average) |
| Futures Liquidations | ${liquidation} (if available) |

### 2. Core Triggering Event

🔴 **{event_title}**

- Event Time: {event_time}
- Event Type: {Regulation / Project Development / Market Manipulation / Macro Economic / Technical Failure / Whale Activity}
- Details: {2-3 sentence description}
- Source: {source}

### 3. Event → Impact Chain

```
{event}
  │
  ├── Direct Impact: {description}
  │     e.g., SEC lawsuit → Regulatory uncertainty for the token increases
  │
  ├── Sentiment Transmission: {description}
  │     e.g., Panic spreads → Fear & Greed Index drops from 65 to 35
  │
  └── Price Reaction: {description}
        e.g., {coin} dropped from ${high} to ${low} within 2 hours of the event
```

### 4. On-chain Verification

{If on-chain data is available:}

| On-chain Metric | Anomaly |
|----------------|---------|
| Exchange Inflows | {increase/decrease}, {description} |
| Large Transfers | {count} transfers exceeding ${threshold} |
| Whale Activity | {description} |
| Futures Funding Rate | {change description} |

{Does the on-chain data corroborate the event narrative?}

### 5. Ripple Effects

{Did this event affect other coins/sectors?}

- {Related coin 1}: {impact description}
- {Related coin 2}: {impact description}
- Sector impact: {e.g., L1 sector declined broadly, DeFi sector affected}

### 6. Forward Outlook

{Based on the event's nature, assess the follow-on impact:}

| Dimension | Assessment |
|-----------|------------|
| Impact Duration | {One-time shock / Short-term (1-3 days) / Medium-term (1-2 weeks) / Long-term} |
| What to Watch Next | {Items to monitor: court ruling, policy details, project response, etc.} |
| Historical Precedent | {Similar past events and their outcomes, if any} |

### ⚠️ Important Notes

- Market moves may be caused by multiple overlapping factors; the above analysis is based on currently available information
- Long-term impact of the event remains uncertain

> The above analysis is based on public information and on-chain data. It does not constitute investment advice.
```

### Template When No Event Can Be Identified

```markdown
## {coin} Volatility Analysis

> Analysis time: {timestamp}

### Volatility Summary

{Same as above}

### Possible Cause Analysis

⚠️ No single clear triggering event was identified. The following is a composite analysis:

**Possible Factor 1: {description}**
- Evidence: {related news/data}
- Likelihood: {High/Medium/Low}

**Possible Factor 2: {description}**
- Evidence: ...
- Likelihood: ...

**On-chain Clues**
{Any anomalous on-chain data that could help explain the move?}

### Composite Assessment

{LLM's composite analysis, with uncertainty explicitly acknowledged}

> Note: No single clear triggering event was found for this move. The above analysis is an informed assessment based on available data.
```

---

## Reasoning Logic

### Event Matching Logic

| Condition | Assessment |
|-----------|------------|
| Event time < price move start time | ✅ Temporally plausible as a trigger |
| Event time > price move start time | ❌ Unlikely to be the trigger (may be follow-up reporting) |
| Event impact rating = "High" | Weight +2 |
| Event involves the queried coin | Weight +3 |
| Event type = "Regulation/Policy" | Typically causes larger moves |
| Multiple events simultaneously | Composite analysis — likely multi-factor |

### Volatility Magnitude Assessment

| Magnitude | Label |
|-----------|-------|
| < 3% | Normal volatility — may not require a specific event explanation |
| 3% – 10% | Moderate volatility — look for recent news/events |
| 10% – 20% | Large volatility — typically has a clear event driver |
| > 20% | Extreme volatility — major event or black swan almost certain |

### On-chain Anomaly Assessment

| Condition | Assessment |
|-----------|------------|
| Exchange inflows surge > 3x average | "Large token inflows to exchanges — potential selling pressure" |
| Exchange outflows surge > 3x average | "Large token outflows from exchanges — possible accumulation" |
| Large transfer count > 5x average | "Abnormally active large transfers" |
| Futures liquidations > $100M | "Massive futures liquidation cascade — amplified price volatility" |

---

## Error Handling

| Error Type | Handling |
|------------|----------|
| `news_events_get_latest_events` finds no matching event | Proceed to Step 4b — expand news search |
| `news_events_get_event_detail` fails | Generate report based on event list summaries only |
| `info_onchain_get_token_onchain` unavailable (P1 phase) | Skip on-chain verification section; note "On-chain data temporarily unavailable" |
| `info_marketsnapshot_get_market_snapshot` fails | Cannot confirm volatility magnitude; degrade to showing event info only |
| Both news and events return no results | Honestly inform the user "No clear cause has been identified at this time"; suggest monitoring for updates |
| All Tools fail | Return error message; suggest the user try again later |

---

## Cross-Skill Routing

| User Follow-up Intent | Route To |
|-----------------------|----------|
| "Analyze BTC for me" | `gate-info-coinanalysis` |
| "Give me a technical analysis" | `gate-info-trendanalysis` |
| "How's the overall market?" | `gate-info-marketoverview` |
| "Recent news?" | `gate-news-briefing` |
| "Any on-chain anomalies?" | `gate-info-tokenonchain` |
| "Track this address" | `gate-info-addresstracker` |

---

## Safety Rules

1. **No definitive causal claims**: Use language like "likely caused by", "the most closely related event is" — avoid absolute causal assertions
2. **No follow-on predictions**: Do not output "it will continue to rise/fall" style predictions
3. **No investment advice**: Do not give buy/sell recommendations based on event analysis
4. **Acknowledge uncertainty**: When the causal link between event and move is uncertain, explicitly state it
5. **Source attribution**: Events and news must cite their sources
6. **Flag missing data**: When on-chain data or event details are unavailable, explicitly state it
7. **Avoid amplifying panic**: When describing crashes or black-swan events, maintain objective, neutral language — no sensationalist rhetoric
