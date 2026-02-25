---
name: mmt-trading-systems
description: Best practices for building trading bots, arbitrage detectors, and high-performance trading systems with MMT. Use when building automated trading strategies, cross-exchange arbitrage, real-time market analysis, or backtesting systems using MMT's multi-exchange API.
---

# MMT Trading Systems

Rules for building trading bots, arbitrage systems, and market analysis tools with MMT.

## Bot Architecture
- [Event-Driven Architecture](rules/bot-architecture-event-driven.md): WS as event source, separate data/logic/execution layers
- [State Management](rules/bot-state-management.md): local orderbook state, candle aggregation, position tracking
- [Multi-Symbol Monitoring](rules/bot-multi-symbol-monitoring.md): multi-pair watching, subscription fan-out, correlation

## Arbitrage
- [Cross-Exchange Detection](rules/arbitrage-cross-exchange-detection.md): price discrepancy detection via multi-exchange data
- [Execution Patterns](rules/arbitrage-execution-patterns.md): signal generation from MMT, external execution

## Real-Time Analysis
- [Orderbook Management](rules/realtime-orderbook-management.md): depth channel, snapshot+delta, sequence tracking
- [Trade Stream Processing](rules/realtime-trade-stream-processing.md): trade aggregation, VWAP, large trade detection
- [Heatmap Analysis](rules/realtime-heatmap-analysis.md): liquidity walls, split index, support/resistance

## Risk Management
- [Position Management](rules/risk-position-management.md): funding rates, liquidation data, exposure monitoring
- [Rate Limit Budgeting](rules/risk-rate-limit-budgeting.md): budget allocation across bot components

## Backtesting
- [Historical Data Fetching](rules/backtest-historical-data-fetching.md): paginating REST data, time range chunking
- [Candle Reconstruction](rules/backtest-candle-reconstruction.md): custom timeframes from base candles, OHLCVT math
