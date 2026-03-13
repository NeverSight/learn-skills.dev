---
name: pinescript
description: >-
  Pine Script v6 patterns: syntax, performance, error diagnosis, backtesting,
  visualization. Use when working with PineScript, TradingView, indicators,
  strategies, or backtesting.
---

# Pine Script Development

## Critical Syntax Rules

- **Ternary operators MUST stay on one line** — splitting across lines causes "end of line without line continuation" error. For complex ternaries, use intermediate variables:
  ```
  isBull = close > open
  barColor = isBull ? color.green : color.red
  ```
- **Continuation lines MUST be indented MORE than the starting line** — same indentation = error
- **NEVER use plot() inside local scopes** (if/for/functions) — use conditional value instead: `plot(condition ? value : na)`
- **barstate.isconfirmed** — use to prevent repainting on real-time bars

## Platform Limits

500 bars history for `request.security()` | 500 plot calls | 64 drawing objects | 40 `request.security()` calls | 100KB compiled size

## Performance

- **Tuple security calls** — one `request.security()` returning `[close, high, low]` instead of 3 separate calls
- Pre-allocate arrays with `array.new<type>(size)` instead of push-and-resize
- Short-circuit signals: build conditions incrementally, exit early when first condition fails
- Cache repeated calculations in variables — Pine recalculates every bar

## Debugging

TradingView has no console or debugger. Use these patterns:

- **Label debugging**: `label.new(bar_index, high, str.tostring(myVar))` to inspect values
- **Table monitor**: `table.new()` with `barstate.islast` for real-time variable dashboard
- **Debug mode toggle**: wrap all debug code in `if input.bool("Debug", false)` — remove before publishing
- **Repainting detector**: track `previousValue = value[1]`, flag when historical values change

## Strategy & Backtesting

- Use `strategy.*` functions: `strategy.wintrades`, `strategy.losstrades`, `strategy.grossprofit`
- Drawdown tracking: `maxEquity = math.max(strategy.equity, nz(maxEquity[1]))`, then `dd = (maxEquity - strategy.equity) / maxEquity * 100`
- Sharpe: `dailyReturn * 252 / (stdDev * math.sqrt(252))`
- **Walk-forward validation** — optimize on period 1, test on period 2, re-optimize on period 2, test on period 3. If metrics degrade > 30%, parameters are overfit.
- **Indicator accuracy testing** — use forward-looking `close[lookforward]` to measure prediction accuracy, track true/false positive rates

## Visualization

- `color.from_gradient()` for trend strength coloring
- Adaptive text sizing: `size.small` for intraday, `size.normal` for daily+
- Dynamic table rows — resize based on enabled features via input toggles
- Professional color constants: define BULL_COLOR, BEAR_COLOR, NEUTRAL_COLOR once with transparency

## Publishing

- Documentation goes at TOP of .pine file as comments before `indicator()`/`strategy()`
- Use `@version`, `@description`, `@param` tags
- Multi-line tooltips: `tooltip="Line 1" + "\n" + "Line 2"`
- **TradingView House Rules**: no financial advice, no performance guarantees, no external links, no obfuscated code, no donation requests

## Anti-Patterns

- Indicator stacking (RSI + Stochastics + CCI) — all measure the same thing (momentum). Use indicators from different categories instead.
- Trading divergence without structure confirmation — wait for break above prior swing high before entry, divergence alone can persist far longer than expected
- Overfitting signals: if optimal parameters are oddly specific (RSI 23 instead of 20), the backtest is curve-fitted. Use round numbers.
- Treating support/resistance as exact prices — they are zones (crypto 1-3%, forex 20-50 pips)
