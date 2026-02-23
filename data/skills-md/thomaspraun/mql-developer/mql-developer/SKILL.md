---
name: mql-developer
description: >
  Comprehensive MQL4/MQL5 development for MetaTrader 4 and MetaTrader 5 platforms.
  Use when writing, reviewing, debugging, or architecting: Expert Advisors (EAs),
  custom indicators, scripts, libraries (.mqh), graphical panels, or any MQL code.
  Also use for: order/position management, risk management, backtesting strategies,
  communication with external APIs (WebRequest, REST, JSON), inter-program communication,
  code protection/licensing, and MQL4-to-MQL5 migration. Covers the full MQL ecosystem
  including trading automation, technical analysis, UI panels, and server integration.
---

# MQL Developer

Guide for professional MQL4/MQL5 development on MetaTrader platforms.

## Quick Reference Navigation

Load the appropriate reference file based on the task:

| Task | Reference File |
|------|---------------|
| MQL4 syntax, types, functions, predefined vars | [references/mql4-reference.md](references/mql4-reference.md) |
| MQL5 syntax, OOP, CTrade, Standard Library | [references/mql5-reference.md](references/mql5-reference.md) |
| Project structure, EA architecture, design patterns | [references/architecture-patterns.md](references/architecture-patterns.md) |
| Orders, positions, risk management, trailing stops | [references/trading-operations.md](references/trading-operations.md) |
| Custom indicators, UI panels, scripts, chart objects | [references/indicators-and-ui.md](references/indicators-and-ui.md) |
| WebRequest, JSON, REST API, Node.js integration | [references/external-communication.md](references/external-communication.md) |
| Strategy Tester, optimization, walk-forward, Monte Carlo | [references/backtesting.md](references/backtesting.md) |
| Code protection, licensing, anti-decompilation | [references/security-licensing.md](references/security-licensing.md) |

### Search Patterns for Large References

For targeted lookup in large files, grep for these section headers:

**mql4-reference.md:** `Data Types`, `Variables`, `Operators`, `Arrays`, `Strings`, `Program Types`, `Predefined Variables`, `Technical Indicator Functions`, `Order Management`, `Market Information`, `Account Functions`, `Preprocessor`, `Error Handling`, `Common Gotchas`, `File Operations`, `WebRequest`, `Utility Functions`, `Global Terminal Variables`

**architecture-patterns.md:** `Project Structure`, `Simple Single-File`, `Modular EA`, `State Machine`, `Multi-Timeframe`, `Multi-Symbol`, `Singleton`, `Strategy Pattern`, `Observer`, `Include File Design`, `Complete Templates`

**mql5-reference.md:** `OOP Features`, `Trade Functions`, `CTrade`, `Native Trade`, `Event Handlers`, `Standard Library`, `Key Enumerations`, `SQLite`, `Sockets`, `Resources`, `OpenCL`

## MQL4 vs MQL5 Key Differences

| Aspect | MQL4 | MQL5 |
|--------|------|------|
| Paradigm | Procedural (C-like) | Full OOP (C++-like) |
| Trade model | Orders only (`OrderSend`) | Orders + Deals + Positions (`CTrade`) |
| Account model | Hedging only | Netting + Hedging |
| Indicator buffers | Max 8 | Max 512 |
| Draw styles | 6 basic | 18 (basic + color) |
| Standard Library | Minimal | Comprehensive |
| Database | None | SQLite built-in |
| Sockets | None | TCP + TLS |
| OpenCL | No | Yes |

## Core Workflow

### Creating an Expert Advisor

1. Define strategy signal logic (entry/exit conditions)
2. Choose architecture: simple (single-file) or modular (Signal + Trade + Risk + Filter)
3. Implement order/position management with proper error handling and retries
4. Add risk management (position sizing, drawdown control)
5. Add filters (time, spread, volatility)
6. Backtest with Strategy Tester (Open Prices first, then Every Tick)
7. Walk-forward validate and Monte Carlo test

### Creating a Custom Indicator

1. Choose window: `indicator_chart_window` or `indicator_separate_window`
2. Define buffers and plots (`indicator_buffers`, `indicator_plots` in MQL5)
3. Implement `OnCalculate()` with efficient recalculation using `prev_calculated`
4. Set draw styles, colors, labels
5. Handle multi-timeframe data if needed

### Communicating with External APIs

1. Whitelist URL in Tools > Options > Expert Advisors
2. Use `WebRequest()` for REST calls (POST/GET)
3. Build JSON manually (MQL has no native JSON)
4. Parse response with string functions
5. Use `EventSetTimer()` for polling patterns
6. Handle network errors with retries

## Critical Gotchas

- **Double comparison**: Never use `==` with doubles. Use `NormalizeDouble()` or tolerance
- **4-digit vs 5-digit brokers**: 1 pip = 1 point (4-digit) or 10 points (5-digit). Always detect
- **Reverse loop for closing**: Iterate `OrdersTotal()-1` down to `0` when closing orders (MQL4)
- **ECN brokers**: Some require two-step: `OrderSend()` without SL/TP, then `OrderModify()`
- **Filling policy (MQL5)**: Always detect via `SYMBOL_FILLING_MODE`, never hardcode FOK
- **WebRequest limitations**: Synchronous/blocking, not available in indicators or Strategy Tester
- **Trade context busy (MQL4)**: Only one EA can trade at a time per terminal
- **Array indexing**: Series arrays index 0 = newest bar. Use `ArraySetAsSeries()` to control

## Project Structure (Recommended)

```
MQL5/                          (or MQL4/)
├── Experts/
│   └── MyEA/
│       └── MyEA.mq5           // EA entry point
├── Indicators/
│   └── MyIndicator.mq5
├── Scripts/
│   └── MyScript.mq5
├── Include/
│   ├── Core/
│   │   ├── CTradeManager.mqh  // Order execution + retries
│   │   ├── CRiskManager.mqh   // Position sizing + drawdown
│   │   └── CSignalBase.mqh    // Signal interface
│   ├── Communication/
│   │   ├── CHttpClient.mqh    // WebRequest wrapper
│   │   └── CJsonHelper.mqh    // JSON build/parse
│   ├── UI/
│   │   └── CPanel.mqh         // Trading panel
│   └── Utils/
│       ├── CTimeFilter.mqh    // Session/time filters
│       └── CSymbolHelper.mqh  // Multi-market helpers
└── Libraries/
```

For simpler projects, a single-file EA with inline functions is acceptable.

## Code Style Conventions

- Prefix member variables with `m_` (e.g., `m_magicNumber`)
- Prefix global variables with `g_` (e.g., `g_isInitialized`)
- Use `input` for user parameters, not `extern`
- Always use `#property strict` in MQL4
- Normalize all prices before sending to server: `NormalizeDouble(price, Digits)`
- Always check return values of `OrderSelect()`, `OrderSend()`, trade operations
- Comment magic numbers and explain non-obvious trading logic

## Official Documentation

- MQL4: https://docs.mql4.com/
- MQL5: https://www.mql5.com/en/docs
- MQL5 Articles: https://www.mql5.com/en/articles
- MQL5 Code Base: https://www.mql5.com/en/code
