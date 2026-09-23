---
name: breaking-news-monitor
description: >
  Detect breaking news from authoritative Chinese and English sources.
  Use this skill when you need to check for breaking/urgent news, monitor news feeds,
  or when the agent is scheduled to perform periodic news checks.
  MUST USE whenever the user mentions "breaking news", "news check", "news monitor",
  "突发新闻", "新闻快讯", or any periodic news monitoring task.
  Extremely lightweight — designed for high-frequency polling (every 5 minutes).
---

# Breaking News Monitor

Lightweight breaking news detector. Zero LLM cost — pure script-based RSS polling + keyword filtering.

## Usage

Run this single command:

```bash
python3 ~/.opencode/skills/breaking-news-monitor/scripts/check.py
```

That's it. The script handles everything: fetch, parse, filter, dedup, output.

## Output Format

**No breaking news:**
```
NO_BREAKING
```

**Breaking news detected:**
```
BREAKING|<source>|<timestamp_utc>|<headline>|<url>
BREAKING|<source>|<timestamp_utc>|<headline>|<url>
```

## How It Works

1. Fetches RSS from: Google News (EN+CN), 中新网, NPR
2. Filters entries published in the last 15 minutes
3. Matches against breaking-news keywords (EN+CN)
4. Deduplicates against previously seen headlines (state stored in `~/.opencode/skills/breaking-news-monitor/state.json`)
5. Returns only NEW breaking items

## What Counts as "Breaking"

The script filters for high-impact categories only:
- Natural disasters, major accidents, terror attacks, wars
- Major political changes (leadership, coups, policy shocks)
- Market crashes, currency crises, circuit breakers
- Major tech breakthroughs (fusion, AGI milestones)
- Pandemic/health emergencies

NOT breaking: sports results, entertainment, routine politics, opinion pieces, business as usual.

## State Management

State file: `~/.opencode/skills/breaking-news-monitor/state.json`

Contains last 200 headline hashes for dedup. Auto-pruned. Safe to delete to reset.

## Agent Integration

When called by an agent on a schedule:
1. Run the command above
2. If output is `NO_BREAKING` → do nothing, continue monitoring
3. If output contains `BREAKING|...` lines → alert the user with the headlines

## Limitations

- RSS feeds may have 5-15 minute delay vs real-time
- Google News RSS covers most major outlets but may miss very early reports
- Keyword-based filtering may miss unusual breaking events (trade-off for speed)
