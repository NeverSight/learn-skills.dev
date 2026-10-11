---
name: nvidia-developer-firehose
description: |
  Real-time AI-ECOSYSTEM firehose (v3 multi-source, May 2026). Polls 12
  Atom/RSS feeds every 30 min: NVIDIA (developer-blog + main-blog +
  newsroom), hyperscalers (Azure, AWS, AWS-ML, Meta-Engineering), AI labs
  (OpenAI, DeepMind, Hugging Face), and neoclouds (CoreWeave, Together
  AI). For each new post, uses HEURISTIC EXTRACTION + yfinance.Search to
  auto-resolve every mentioned company → US ticker (no hand-maintained
  name→ticker dict), with a persistent ticker cache that learns over
  time. Surfaces names via Telegram tagged by source, separated into
  🎯 portfolio-tracked tickers vs 🔍 newly discovered tickers. Why it
  matters: hyperscalers + NVIDIA + AI labs publicly name 800V HVDC, CPO,
  optical, power, and custom-silicon partners — the forward-looking
  design ecosystem that re-rates weeks later when sell-side picks it up.
  (AMD has no public RSS — covered separately by SEC 8-K
  strategic-partner-firehose.)
  Triggers in English ("nvidia developer firehose", "ai ecosystem
  firehose", "ai partner monitor", "hyperscaler blog scraper") or
  Chinese ("NVIDIA Developer 爬虫", "AI 生态 firehose", "超大厂博客实时",
  "英伟达 + 超大厂 + AI 实验室博客").
  Do NOT trigger for: generic web scrapers, non-equity contexts, or
  individual blog reading.
---

# NVIDIA Developer Firehose

## Why this exists

NVIDIA's Technical Blog (`developer.nvidia.com/blog`) is where NVDA
publicly names the partners it's designing the next generation around —
800V HVDC chip suppliers, CPO optical module makers, custom XPU/ASIC
partners, networking/server OEMs, hyperscaler/neocloud customers. When
a partner gets named here, it's typically **weeks before** the Substack /
sell-side picks up on it. Forward-looking edge.

This firehose:
1. Polls the Atom feed every 30 min.
2. For each new post, runs **smart heuristic extraction** + **yfinance.Search**
   to auto-resolve every capitalized noun phrase → US-listed ticker.
3. **Persistent cache** (`nvdev_ticker_cache.json`) learns over time so
   newly-named partners get added automatically; never needs hand edits.
4. Sends a Telegram alert separating 🎯 **portfolio-tracked** mentions
   (high signal) from 🔍 **newly discovered** tickers (medium signal).

## Architecture

```
ATOM FEED                  CANDIDATE EXTRACT             RESOLVE
─────────                  ─────────────────             ───────
developer.nvidia.com  →    capitalized 1-4 word     →    cache HIT  →  done
/blog/feed/                phrases, minus              cache MISS →  yf.Search()
                           STOPWORDS + ALIAS                          name-overlap
                           expansion                                  US exchange?
                                                                      → cache + emit
```

**No hardcoded `name_to_ticker` dict.** A small `TRACKED_TICKERS` set
(your portfolio universe) only affects whether a hit shows up as 🎯 or 🔍.
Resolution itself is fully automatic.

**ALIAS map** handles only ambiguous short forms (e.g. `MPS` →
`Monolithic Power Systems`) so the yfinance search returns the right
company.

**STOPWORDS** filter strips NVIDIA's own products, calendar/structural
words, and common tech jargon (CUDA, TensorRT, Blackwell, GTC, etc.).

**Negative cache**: words that resolve to nothing (or non-US) are also
cached, so we never re-look up junk.

## Files

- `scripts/nvdev_firehose.py` — the engine
- (in the runtime repo)
  - `scripts/nvdev_state.json` — seen-post ids (5k cap, dedup)
  - `scripts/nvdev_ticker_cache.json` — name → {ticker,exchange,name,source}

## Workflow

The runtime repo provides a GitHub Actions workflow that runs the engine
on a `*/30 * * * *` cron with `TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID` as
secrets. First run silently seeds the state (no Telegram avalanche).

## Tuning

| Env var | Default | What it does |
|---|---|---|
| `MAX_ALERTS` | 8 | Cap Telegram alerts per run |
| `MAX_LOOKUPS` | 40 | Cap yfinance.Search calls per article (cache absorbs rest next run) |
| `TEST_MODE` | (unset) | If `1`, log to stderr; no Telegram, no state/cache write |
| `NVDEV_USER_AGENT` | (generic) | Override the polite UA string |

## Editing the cache

The cache JSON is human-editable. To override a wrong resolution or add
an alias by hand:

```json
{
  "some company": {"ticker": "ABCD", "exchange": "NMS", "name": "Some Company Inc.", "source": "manual"},
  "wrong match name": null
}
```

`null` = negative-cached, will be skipped on future runs.

## What an alert looks like

```
🟢🟪 NVIDIA Developer — new post
NVIDIA Transitions to 800V HVDC for 1MW AI Racks
作者: Mathias Blake et al
发布: 2025-05-20

🎯 组合内标的(高信号):
  • Infineon → IFNNY
  • MPS → MPWR
  • Navitas → NVTS
  • STMicroelectronics → STM
  • Texas Instruments → TXN
  • Eaton → ETN
  • Schneider Electric → SBGSF
  • Vertiv → VRT
  • TSMC → TSM
  • Coherent → COHR
  • Lumentum → LITE
  • Marvell → MRVL

🔍 其他识别到的可交易标的:
  • ROHM → ROHCY  (ROHM Co., Ltd.)
  • Flex Power → FLXP  (Flex-Power Inc.)

https://developer.nvidia.com/blog/...
```

## Related skills

- `strategic-partner-firehose` — SEC 8-K / 13D partner detection (downstream)
- `pr-wire-firehose` — vendor newsroom RSS (parallel signal source)
- `insider-firehose` — Form 4 buys (corroborating signal)
