---
name: claw-screener
description: Stock screener combining Williams %R oversold signals with Warren Buffett-style fundamental analysis. Supports US (S&P 500) and Thai (SET) markets.
homepage: https://github.com/rsoutar/claw-screener
metadata:
  clawdbot:
    emoji: "📊"
    requires:
      env: []
      files:
        - ~/.claw-screener-watchlist.json
        - sec_cache.db
        - price_cache.db
      runtime: bun >=1.3.1
      config_paths: ~/.claw-screener-watchlist.json
---

# Claw-Screener

A stock screener that combines technical analysis (Williams %R oversold signals) with Warren Buffett-style fundamental analysis using SEC data. Supports US (S&P 500) and Thai (SET) markets.

## When to Use This Skill

Use this skill when you need to:
- Find oversold stocks with strong fundamentals
- Screen for quality stocks using Buffett's 10 formulas
- Screen for long-term compounders using Carlson filters (ROIC, growth, buybacks)
- Analyze individual stocks for investment decisions
- Get daily stock screening results in text, JSON, or Telegram format

## Tools

This skill provides the following capabilities:

### 1. Combined Screening
Finds stocks that are both technically oversold (Williams %R < -80) and fundamentally strong (Buffett score >= threshold).

**Command:**
```
bun run src/screening.ts [options]
```

**Options:**
| Flag | Description | Default |
|------|-------------|---------|
| `--market` | Market: `us` or `bk` | `us` |
| `--min-score` | Minimum Buffett score (0-10) | `5` |
| `--top-n` | Number of results to show | `10` |
| `--format` | Output: `text`, `json`, `telegram` | `text` |

**Examples:**
```
bun run src/screening.ts
bun run src/screening.ts --market us --min-score 7 --top-n 5
bun run src/screening.ts --market bk
bun run src/screening.ts --format json
bun run src/screening.ts --format telegram
```

### 2. Technical Only Scan
Fast oversold scan using Williams %R indicator only. No SEC data required. Works for both US and Thai markets.

**Command:**
```
bun run src/technicalOnly.ts [options]
```

**Options:**
| Flag | Description | Default |
|------|-------------|---------|
| `--market` | Market: `us` or `bk` | `us` |
| `--threshold` | Williams %R threshold | `-80` |
| `--top-n` | Number of results to show | `20` |
| `--format` | Output: `text`, `json`, `telegram` | `text` |

**Examples:**
```
bun run src/technicalOnly.ts
bun run src/technicalOnly.ts --threshold -70 --top-n 50
bun run src/technicalOnly.ts --market bk
```

### 3. Analyze Stock
Deep analysis of a single stock using Buffett's 10 formulas.

**Command:**
```
bun run src/analyze.ts <ticker> [options]
```

**Options:**
| Flag | Description | Default |
|------|-------------|---------|
| `--format` | Output: `text`, `json`, `telegram` | `text` |

**Examples:**
```
bun run src/analyze.ts AAPL
bun run src/analyze.ts MSFT --format telegram
bun run src/analyze.ts GOOGL --format json
bun run src/analyze.ts PTT.BK
```

### 4. Compounding Machine
Screens for "compounders" using Carlson-style filters:
- Revenue and net income YoY trend strength
- ROIC threshold (default >15%)
- Share count reduction over 3 years (buyback signal)
- Operating margin threshold (default >20%)
- Includes current yield vs 5-year average and a simple 10-year DCF context

**Command:**
```
bun run src/compoundingMachine.ts [options]
```

**Options:**
| Flag | Description | Default |
|------|-------------|---------|
| `--market` | Market universe: `us` or `bk` | `us` |
| `--tickers` | Comma-separated tickers (overrides market universe) | - |
| `--max-tickers` | Limit universe size | all |
| `--top-n` | Number of passing stocks to show | `25` |
| `--concurrency` | Parallel fetch workers | `4` |
| `--format` | Output: `text` or `json` | `text` |
| `--db-path` | SQLite cache path | `sec_cache.db` |
| `--ttl-days` | Cache TTL in days | `7` |
| `--min-roic` | ROIC threshold (%) | `15` |
| `--min-op-margin` | Operating margin threshold (%) | `20` |
| `--min-buyback` | Required 3Y share reduction (%) | `2` |
| `--show-rejected` | Include failed tickers with reasons in output | off |

**Examples:**
```
bun run src/compoundingMachine.ts
bun run src/compoundingMachine.ts --tickers AAPL,MSFT,NVDA --top-n 10
bun run src/compoundingMachine.ts --format json --max-tickers 100
bun run src/compoundingMachine.ts --tickers PLTR --show-rejected
```

**Runtime / Caching Notes:**
- First uncached run on full US universe can take ~20-30+ minutes.
- This is expected: each ticker requires multiple Yahoo fundamentals/quote requests and retry backoff for rate-limit resilience.
- Subsequent runs are much faster due to SQLite caching (`sec_cache.db`, TTL default 7 days).
- For quick checks, run smaller scans first (for example `--max-tickers 50` or specific `--tickers`).

**Agent Guidance for User Messaging:**
- If user runs full-universe Compounding Machine scan, explicitly warn that initial run may take ~20-30 minutes.
- Suggest quick-test alternatives while waiting:
  - `bun run src/compoundingMachine.ts --max-tickers 50`
  - `bun run src/compoundingMachine.ts --tickers AAPL,MSFT,NVDA`

### 5. Watchlist Management
Track stocks you're interested in and get alerts when they become oversold or overbought.

**Command:**
```
bun run src/watchList.ts <command> [options]
```

**Commands:**

| Command | Description |
|---------|-------------|
| `add <ticker>` | Add a stock to your watchlist |
| `remove <ticker>` | Remove a stock from your watchlist |
| `list` | Show all watched stocks |

**Options:**
| Flag | Description | Default |
|------|-------------|---------|
| `--market us\|th` | Market: `us` (US) or `th` (Thai) | `us` |
| `--notes '...'` | Optional notes for the stock | - |
| `--alert-threshold` | Williams %R threshold for alerts | - |

**Examples:**
```
bun run src/watchList.ts add AAPL
bun run src/watchList.ts add AAPL --market us --notes 'Big tech'
bun run src/watchList.ts add PTT.BK --market th
bun run src/watchList.ts remove AAPL
bun run src/watchList.ts list
bun run src/watchList.ts list --market us
```

**Storage:** Watchlist is saved to `~/.claw-screener-watchlist.json`

## Buffett's 10 Formulas

The fundamental analysis evaluates stocks against Warren Buffett's criteria:

| # | Formula | Target | Description |
|---|---------|--------|-------------|
| 1 | Cash Test | > Total Debt | Cash covers all debt |
| 2 | Debt-to-Equity | < 0.5 | Low leverage |
| 3 | Return on Equity | > 15% | Efficient use of capital |
| 4 | Current Ratio | > 1.5 | Short-term liquidity |
| 5 | Operating Margin | > 12% | Operational efficiency |
| 6 | Asset Turnover | > 0.5 | Asset efficiency |
| 7 | Interest Coverage | > 3x | Ability to pay interest |
| 8 | Earnings Stability | Positive | Consistent profitability |
| 9 | Free Cash Flow | > 0 | Cash generation |
| 10 | Capital Allocation | > 15% ROE | Management effectiveness |

**Scoring:** Each passing formula earns 1 point. Maximum score: 10/10.

## Technical Indicator

**Williams %R (Williams Percent Range)**

- Range: -100 to 0
- Oversold: < -80 (potential buy signal)
- Overbought: > -20 (potential sell signal)

## Combined Score Formula

Combined score = (Technical Score × 0.3) + (Fundamental Score × 0.7)

- Technical Score: (Williams %R + 100) / 100
- Fundamental Score: (Buffett Score / 10) × 100

## Data Sources

- **US Stocks**: SEC EDGAR for fundamentals, Yahoo Finance for prices
- **Thai Stocks**: Yahoo Finance only (no SEC data available)

## Installation

### Runtime Requirements

- **Bun** (>=1.3.1) - Required runtime for executing TypeScript scripts
- Node.js is NOT required as Bun provides all necessary runtime functionality

### Install Bun

If you don't have Bun installed, run:

```bash
# macOS/Linux
curl -fsSL https://bun.sh/install | bash

# Windows (PowerShell)
iwr https://bun.sh/install -outfile "install.ps1"; ./install.ps1
```

### Install Dependencies

```bash
bun install
```

## File Persistence

This skill creates and manages the following files:

| File | Location | Purpose | TTL |
|------|----------|---------|-----|
| Watchlist | `~/.claw-screener-watchlist.json` | User's stock watchlist | Permanent |
| SEC Cache | `sec_cache.db` | Cached SEC EDGAR financial data | 7 days (default) |
| Price Cache | `price_cache.db` | Cached stock price data | 1 day (default) |

### Cache Management

- Cache files are automatically created on first run
- Use `--ttl-days` flag with compounding machine to adjust cache TTL
- Cache files can be deleted to force fresh data fetch
- Cache improves performance significantly on subsequent runs

### Notes
- First run on full US universe can take ~20-30+ minutes (expected behavior)
- Subsequent runs are much faster due to caching
- For quick tests, use `--max-tickers 50` or specific `--tickers`

## Bun Scripts

```bash
bun run dev              # Run screening (alias for bun run src/screening.ts)
bun run screening        # Run combined screening
bun run technical        # Run technical-only scan
bun run analyze          # Analyze a stock (requires ticker argument)
bun run compounder       # Run Compounding Machine screener
bun run watchlist:add    # Add stock to watchlist
bun run watchlist:remove # Remove stock from watchlist
bun run watchlist:list   # List watched stocks
```

## Output Format Examples

### Text (Default)
```
📊 Combined Quality Screening (US (S&P 500))
Technical: Oversold signals (Williams %R < -80)
Fundamental: Warren Buffett's 10 formulas on SEC data
Minimum Buffett Score: 5/10

Results:
  Total Scanned: 503
  Oversold Found: 42
  Quality Stocks: 8 (Buffett ≥5/10)

Top 10 Opportunities:

1. AAPL   — Combined: 85.2% | Buffett: 8/10 | WR: -82.3
2. MSFT   — Combined: 79.1% | Buffett: 7/10 | WR: -85.1
```

### Telegram
```
📊 Combined Quality Screening (US (S&P 500))
Scanned: 503 stocks
Oversold: 42
Quality (Buffett ≥5/10): 8

🌟 Top 10 Quality Opportunities:

1. **AAPL** — Combined: 85% | Buffett: 8/10 | WR: -82.3
2. **MSFT** — Combined: 79% | Buffett: 7/10 | WR: -85.1
```
