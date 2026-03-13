---
name: polymarket-analyzer
description: Analyze Polymarket prediction market data to provide investment insights for Chinese concept stocks (中概股) and A-shares. This skill should be used when the user asks about Polymarket data, prediction markets, A-share (A股) investment advice based on prediction market sentiment, or 中概股 correlations.
---

# Polymarket + Multi-Source China Market Sentiment Analyzer

Collect data from multiple information channels to support comprehensive sentiment analysis for Chinese concept stocks (中概股) and A-shares.

**The agent performs all judgment and interpretation.** The scripts in this skill are pure data collectors — they fetch raw information without making directional calls.

---

## When to Use

- The user asks about Polymarket prediction market data for China/HK topics
- The user wants sentiment context for A-share or 中概股 investment decisions
- The user requests multi-source market intelligence (news, macro, market proxies)
- The user asks about specific stocks: BYD, NIO, Alibaba, Tencent, SMIC, etc.

---

## Prerequisites

### Polymarket CLI (required for prediction market data)

```bash
brew tap Polymarket/polymarket-cli https://github.com/Polymarket/polymarket-cli
brew install polymarket
# or
curl -sSL https://raw.githubusercontent.com/Polymarket/polymarket-cli/main/install.sh | sh
polymarket --version
```

### yfinance (optional — enables market proxy data)

```bash
pip install yfinance
```

---

## Skill Structure

```
polymarket-analyzer/
├── SKILL.md
├── references/
│   ├── china_stock_mapping.json        # 21 China concept stocks → A-share sector/ticker mapping
│   ├── signal_weights.json             # Configurable source weights for composite analyzer
│   ├── workflows/
│   │   ├── scenario-1-macro-geopolitical.md  # Top-down macro & geopolitical risk workflow
│   │   ├── scenario-2-sector-catalyst.md     # Bottom-up sector/company catalyst workflow
│   │   └── scenario-3-daily-pulse.md         # Fast daily digest / delta-only briefing
│   └── templates/
│       ├── comprehensive-insight-report.md   # Full deep-dive report template (Scenarios 1 & 2)
│       └── quick-brief.md                    # 30-second pulse template (Scenario 3)
└── scripts/
    ├── polymarket_analyzer.py     # Full 7-source composite analyzer
    ├── query-markets.py           # Polymarket search — active markets only by default
    ├── filter-markets.py          # Polymarket multi-filter — active markets only by default
    ├── fetch-market-data.py       # Raw price/volume for China proxy instruments
    └── fetch-cn-news.py           # Raw headlines from Chinese domestic + global sources
```

---

## Information Channels

### Channel 1 — Polymarket Prediction Markets
**Scripts**: `scripts/query-markets.py`, `scripts/filter-markets.py`

Real-money crowd probabilities on macro, geopolitical, and corporate events. Best for tail risks such as Taiwan conflict, trade war escalation, and rate decisions.

### Channel 2 — Financial Market Proxies
**Script**: `scripts/fetch-market-data.py`

Raw daily price and volume data for 11 China-sensitive instruments:

| Ticker | Instrument | Relevance |
|--------|-----------|-----------|
| FXI | iShares China Large-Cap ETF | Direct China equity sentiment |
| KWEB | KraneShares China Internet ETF | China tech/internet |
| ^HSI | Hang Seng Index | HK market |
| HG=F | Copper Futures | China industrial demand |
| AUDUSD=X | AUD/USD | China commodities activity |
| CNY=X | USD/CNY | Renminbi strength |
| ^VIX | CBOE Volatility Index | Global risk appetite |
| GC=F | Gold Futures | Safe-haven demand |
| ^TNX | US 10-yr Treasury Yield | US rate pressure on EM |
| EEM | iShares Emerging Markets ETF | EM flow proxy |
| UUP | US Dollar Index ETF | USD strength |

### Channel 3 — Chinese Domestic Financial News
**Script**: `scripts/fetch-cn-news.py`

Raw headlines from domestic Chinese financial media:

| Source ID | Name | Coverage |
|-----------|------|---------|
| `caixin` | 财新 Caixin Global | Investigative finance/economy (EN+ZH) |
| `sina_finance` | 新浪财经 | Breaking A-share news, policy |
| `yicai` | 第一财经 | Macro, banking, real estate |
| `eastmoney` | 东方财富 | Retail investor hot topics |
| `stcn` | 证券时报 | Regulatory / official securities news |
| `21cbh` | 21世纪经济报道 | Industry deep dives |
| `xinhua_finance` | 新华财经 | State macro/policy announcements |

### Channel 4 — Global / HK China-Focused News
**Script**: `scripts/fetch-cn-news.py` (same script, global sources)

| Source ID | Name | Coverage |
|-----------|------|---------|
| `reuters_china` | Reuters China | Breaking, macro, corporate |
| `scmp` | South China Morning Post | HK/Greater China business |
| `ft_china` | Financial Times China | Western institutional view |
| `nikkei_china` | Nikkei Asia China | Japan/Asia regional perspective |
| `xinhua_en` | Xinhua English | Official Chinese government narrative |

### Channels 5–7 — Embedded in Composite Analyzer
Invoked automatically by `scripts/polymarket_analyzer.py`:
- **CNN Fear & Greed Index** — US market psychology; extreme readings affect EM risk appetite
- **Reddit Social Sentiment** — r/investing, r/wallstreetbets, r/china, r/ChineseStocks, r/emergingmarkets
- **World Bank Macro** — China GDP, CPI, export growth, FDI, US real interest rate

---

## Scripts Usage

### `scripts/query-markets.py` — Polymarket raw search
Returns **active markets only by default**. Use `--all` to include closed/resolved markets.
```bash
python3 scripts/query-markets.py "china"
python3 scripts/query-markets.py "taiwan" --limit 100 --format json
python3 scripts/query-markets.py "byd" --limit 50
python3 scripts/query-markets.py "pboc rate"
# Include resolved markets (for historical analysis only):
python3 scripts/query-markets.py "taiwan" --limit 100 --format json --all
```

### `scripts/filter-markets.py` — Polymarket multi-filter
Defaults to `--status active`. Use `--status closed` or `--status all` to override.
```bash
python3 scripts/filter-markets.py --keywords taiwan,invasion --volume 100000
python3 scripts/filter-markets.py --keywords byd,nio,xpeng,alibaba,tencent
python3 scripts/filter-markets.py --status active --volume 50000 --format json
# Closed markets (historical reference only):
python3 scripts/filter-markets.py --keywords taiwan --status closed --format json
```

### `scripts/fetch-market-data.py` — Market proxy raw data
```bash
python3 scripts/fetch-market-data.py
python3 scripts/fetch-market-data.py --format json
python3 scripts/fetch-market-data.py --period 30d
python3 scripts/fetch-market-data.py --tickers "FXI KWEB ^VIX"
```

### `scripts/fetch-cn-news.py` — China news raw headlines
```bash
python3 scripts/fetch-cn-news.py
python3 scripts/fetch-cn-news.py --format json --limit 20
python3 scripts/fetch-cn-news.py --source caixin --limit 30
python3 scripts/fetch-cn-news.py --source caixin,scmp
```

### `scripts/polymarket_analyzer.py` — Full composite run
Executes all seven channels and prints a structured report:
```bash
python3 scripts/polymarket_analyzer.py
```
Channels unavailable at runtime degrade gracefully with no crash.

---

## Analysis Workflows & Scenarios

Three scenario-specific workflows are defined in `references/workflows/`. Each workflow applies **First Principles Thinking** — defining a hypothesis first, then fetching only the data needed to test it.

| Scenario | File | Use When |
|----------|------|-----------|
| 1. Macro & Geopolitical Risk (Top-Down) | `references/workflows/scenario-1-macro-geopolitical.md` | Taiwan, tariffs, PBOC, elections, USD/CNY stress |
| 2. Sector-Specific Catalyst (Bottom-Up) | `references/workflows/scenario-2-sector-catalyst.md` | EVs, Semiconductors, Property, Internet, specific companies |
| 3. Daily Market Pulse / Fast Digest | `references/workflows/scenario-3-daily-pulse.md` | Pre-market briefing, end-of-day delta check |

### Core Analytical Principles (applied in all scenarios)
1. **Liquidity Weighting**: Polymarket odds mean nothing without volume. Verify pool size. A 90% probability with $500 volume is noise; with $5M volume, it's a signal.
2. **Divergence Detection**: The most profitable insights stem from *discrepancies* between explicit prediction market odds and implicit market proxy pricing.
3. **Probability Momentum**: Focus on the *delta* (change over time). A contract moving from 10% to 30% in two days is highly actionable.
4. **Active Markets Only (Data Collection)**: Scripts default to active-only. Never treat a closed/resolved contract as a current signal.
5. **Historical Context (Mandatory)**: Always compare the current PM probability against: (a) the trend of the last 7–30 days for this specific contract, and (b) how analogous resolved contracts priced and resolved historically. A probability without a trend is not a signal — it is a datapoint. Use `--all` to retrieve resolved contracts for comparison.
6. **Conflict-First Analysis**: When any two sources disagree, the conflict itself is the most important finding in the report. Explain the conflict and its likely cause before forming any directional thesis. A thesis built by ignoring a conflict is not a thesis — it is wishful reasoning.
7. **Multi-Source Minimum**: A directional conclusion requires ≥2 independent channels in agreement. Single-source signals must be labeled "Unconfirmed — Watch Only." State explicitly which channels confirm and which dissent.

## Accumulated Experience

Before running any analysis, check `EXPERIENCE.md` for relevant prior observations:
- Source reliability notes calibrated from past sessions
- Known false signal patterns (e.g., sectors where PM historically misprices)
- Conflict resolution examples from past analyses
- User feedback on conviction thresholds

After the user provides feedback on analysis quality or outcome accuracy, append a new entry to `EXPERIENCE.md` using the format defined in that file.

---

## Standardized Output Templates

Two templates are defined in `references/templates/`. **Always** use the appropriate template when generating a response.

| Template | File | Use When |
|----------|------|-----------|
| A: Comprehensive Investment Insight Report | `references/templates/comprehensive-insight-report.md` | Full analysis from Scenario 1 or 2; includes confidence score, proxy confirmation table, source attribution, and data provenance |
| B: Quick Brief | `references/templates/quick-brief.md` | Daily pulse (Scenario 3) or when user needs a rapid digest; ALERT / WATCH / No-Change triage format |

---

## References

### `references/china_stock_mapping.json`
Maps 21 China concept stocks to A-share sectors, tickers, supply chain names, HK listings, and correlation coefficients. Companies covered: BYD, NIO, XPeng, Li Auto, Tencent, Alibaba, Baidu, Xiaomi, Pinduoduo, JD.com, Meituan, NetEase, Kuaishou, Bilibili, SMIC, Huawei supply chain, Evergrande, Anta, Haier, Midea, Foxconn. Also includes macro factor mappings for: PBOC rate cuts, US-China trade war, Taiwan tensions, China stimulus.

### `references/signal_weights.json`
Configurable source weights for the composite analyzer. Four profiles:

| Profile | Description |
|---------|-------------|
| `default` | Polymarket 35%, market_data 25%, news 20%, fear_greed 10%, … |
| `news_heavy` | Elevates news to 35% when Polymarket coverage is thin |
| `market_only` | 90% weight on market proxies only |
| `sentiment_focus` | Emphasis on social + Fear & Greed for retail sentiment reads |

---

## A-share Sector Quick Reference

| Market Signal | A-share Sector | Key Tickers |
|---------------|---------------|------------|
| EV sales / BYD / NIO | New Energy + Battery | BYD 002594.SZ, CATL 300750.SZ |
| Taiwan tensions | Defense | AVIC 600893.SH, CSGC 000768.SZ |
| US chip restrictions | Semiconductor localization | SMIC 688981.SH, Hua Hong 688347.SH |
| Trade war / tariffs | Export manufacturing | Luxshare 002475.SZ, Hisense 600060.SH |
| PBOC rate cut | Banks + Real estate | ICBC 601398.SH, Vanke 000002.SZ |
| China stimulus | Infrastructure | CRCC 601186.SH, CREC 601390.SH |
| Copper surge | Industrial metals | Jiangxi Copper 600362.SH |

---

## Troubleshooting

**Polymarket CLI not found**
```bash
export PATH="$PATH:$HOME/.cargo/bin:$HOME/.local/bin"
```

**yfinance not installed** — `fetch-market-data.py` will print an error and exit cleanly; all other channels still work.

**Chinese news sources unreachable** — Some domestic RSS feeds block non-CN IPs. Use a HK/mainland proxy, or focus on: `caixin`, `reuters_china`, `scmp`, `xinhua_en`.
