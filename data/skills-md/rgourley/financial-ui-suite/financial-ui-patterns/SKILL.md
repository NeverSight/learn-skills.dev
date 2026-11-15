---
name: financial-ui-patterns
description: Use when building any UI that displays prices, P&L, holdings, orders, trades, charts, order books, watchlists, or streaming market data. Covers patterns from Kraken, Coinbase, TradingView, Bloomberg, Robinhood. Read before writing JSX for any financial surface.
---

# Financial UI Patterns

## Overview

Generic AI output for financial UIs fails in predictable ways: raw color values instead of design tokens, jittery non-tabular numbers, no decimal alignment, missing tick-flash on updates, hard-coded dark theme, broken Tailwind dynamic classes, no streaming/staleness states, no accessibility for color-blind users.

This skill codifies the patterns that production trading UIs (Kraken, Coinbase, TradingView, Bloomberg Terminal, Robinhood, Binance) actually ship.

**Core principle:** numbers must be legible, aligned, and trustworthy. Color is a signal, not decoration. Latency must be visible. Every digit shift is a failure.

## When to Use

- Tables with prices, P&L, holdings, positions, orders, fills, trades
- Order books, depth charts, ladders
- Watchlists, tickers, market overviews
- Streaming/live data of any kind
- Portfolio screens, transaction history
- Charts with OHLC, candlesticks, sparklines
- Any UI showing money, percentages, basis points, or quantities

**Don't use for:** marketing pages, blog posts, generic product UI without numbers.

## Quick Reference

| Concern | Rule |
|---|---|
| Number rendering | Always `tabular-nums`. Never let digits reflow. |
| Number alignment | Right-align in tables. Decimal-align when precision varies. |
| Ticker/ID display | Use `font-mono` (JetBrains Mono, Roboto Mono, IBM Plex Mono). |
| Colors | Semantic tokens only (`text-positive`, `text-negative`). Never `text-green-500`. |
| Theme | Light + dark via CSS variables. Never hard-code surface colors. |
| Tick flash | 300-500ms tinted background on price update. CSS only, no JS animation. |
| P&L sign | Always show `+` for positive returns. `-` is automatic on negatives. |
| Tailwind dynamic | NEVER `bg-${color}-500/10`. Use static class maps. |
| Streaming state | Show connecting / live / stale / disconnected explicitly. |
| Accessibility | Pair color with icon, position, or shape. Never color alone. |
| Decimals | Crypto: dynamic precision by price magnitude. Stocks: 2 dp. FX: 4-5 dp. |
| Large numbers | Compact notation (`1.2B`, `847M`) for caps/volume, not for prices/balances. |
| Density | Default to compact. 32-40px row height in tables. 24-28px in order books. |

## Required Reading

| File | When to load |
|---|---|
| `references/typography-and-color.md` | Designing any financial surface from scratch |
| `references/number-formatting.md` | Implementing any price/quantity/percentage display |
| `references/components.md` | Building tables, order books, tickers, charts |
| `references/streaming-and-state.md` | Live data, WebSocket UIs, tick-flash, staleness |
| `references/accessibility.md` | Any production UI (always) |
| `references/mobile-and-responsive.md` | Targeting phones/tablets, responsive tables, bottom sheets, touch interactions |
| `references/industry-patterns.md` | Want specific references from Kraken/Coinbase/TradingView/Bloomberg |
| `references/charts-and-candles.md` | Building any chart (candles, OHLC, line, volume, indicators) |
| `references/loading-and-skeletons.md` | First-load and reconnect treatments for tables, order books, charts |
| `references/empty-and-error-states.md` | Empty positions/orders, rejected orders, market closed, rate-limit copy |
| `references/timestamps-and-timezones.md` | Trade times, "as of" stamps, multi-TZ status bar, ms precision rules |
| `references/virtualization.md` | Tables over 100 streaming rows, trades tape, sticky headers, row memoization |
| `references/chart-interactions.md` | Crosshair, zoom/pan, drawing tools, multi-pane stacks, number animations |
| `references/order-entry-and-lifecycle.md` | Order forms, types (market/limit/stop/bracket/OCO), preview-then-submit, pending→filled states, time-and-sales |
| `references/alerts-and-disclosures.md` | Price alerts, fill notifications, escalation rules, PDT/wash-sale/options/restricted-symbol disclosures |
| `references/data-sources-and-freshness.md` | Real-time/delayed/stale/frozen/disconnected chain, source chips (CBOE, NBBO), multi-account context |
| `references/heatmaps-and-density-viz.md` | Sector heatmaps, options chain color scales, IV surfaces, correlation grids |

## Core Pattern: Numbers

The single most important fix vs. generic AI output:

```tsx
// ❌ BAD: digits shift width on update, color is decorative, no sign on positive
<span className="text-green-500 font-medium">
  {value.toFixed(2)}%
</span>

// ✅ GOOD: tabular-nums locks width, semantic color, explicit sign, fixed width
<span
  className={`tabular-nums font-medium tracking-tight ${
    value >= 0 ? "text-positive" : "text-negative"
  }`}
  style={{ minWidth: 64, textAlign: "right" }}
>
  {value >= 0 ? "+" : ""}{value.toFixed(2)}%
</span>
```

Three failures the bad version causes:
1. Width changes when value goes from `9.99%` to `10.00%` — the entire row reflows
2. `text-green-500` breaks light theme and ignores any design system
3. No `+` prefix means positive and zero look identical at a glance

## Core Pattern: Color Tokens

Define semantic colors via CSS variables, expose via Tailwind, never use raw color values in components.

```css
/* globals.css */
:root {
  --positive: 34 197 94;   /* green for gains, buy, success */
  --negative: 239 68 68;   /* red for losses, sell, danger */
  --warning: 251 191 36;   /* amber for partial fills, stale data */
  --info: 0 143 250;       /* blue for working orders, neutral signals */
  --surface: 13 13 16;
  --surface-elevated: 22 22 26;
  --text-primary: 240 240 245;
  --text-secondary: 180 180 192;
  --text-muted: 110 110 125;
}

[data-theme="light"] {
  --positive: 22 163 74;
  --negative: 220 38 38;
  --surface: 248 249 251;
  /* ... */
}
```

**Tailwind v3 form** (`tailwind.config.ts`):
```ts
colors: {
  positive: "rgb(var(--positive) / <alpha-value>)",
  negative: "rgb(var(--negative) / <alpha-value>)",
  surface: {
    DEFAULT: "rgb(var(--surface) / <alpha-value>)",
    elevated: "rgb(var(--surface-elevated) / <alpha-value>)",
  },
  text: {
    primary: "rgb(var(--text-primary) / <alpha-value>)",
    secondary: "rgb(var(--text-secondary) / <alpha-value>)",
    muted: "rgb(var(--text-muted) / <alpha-value>)",
  },
}
```

**Tailwind v4 form** (in your CSS, no config file needed):
```css
@theme {
  --color-positive: rgb(var(--positive));
  --color-negative: rgb(var(--negative));
  --color-surface: rgb(var(--surface));
  --color-surface-elevated: rgb(var(--surface-elevated));
  --color-text-primary: rgb(var(--text-primary));
  --color-text-secondary: rgb(var(--text-secondary));
  --color-text-muted: rgb(var(--text-muted));
}
```

## Core Pattern: Tick Flash

When a price updates, briefly tint the background. CSS only. Robinhood, Coinbase, and TradingView all use this.

```tsx
// PriceCell.tsx
import { useEffect, useRef, useState } from "react";

export function PriceCell({ value, format }: { value: number; format: (n: number) => string }) {
  const prev = useRef(value);
  const [flash, setFlash] = useState<"up" | "down" | null>(null);

  useEffect(() => {
    if (value === prev.current) return;
    setFlash(value > prev.current ? "up" : "down");
    prev.current = value;
    const t = setTimeout(() => setFlash(null), 400);
    return () => clearTimeout(t);
  }, [value]);

  return (
    <span
      data-flash={flash ?? undefined}
      className="tabular-nums tracking-tight transition-colors duration-300 px-1 rounded-sm data-[flash=up]:bg-positive/15 data-[flash=down]:bg-negative/15"
    >
      {format(value)}
    </span>
  );
}
```

Why this beats animation libraries: zero JS during the flash, scales to hundreds of cells, no jank on heavy WebSocket traffic.

## Core Pattern: Decimal Alignment

`tabular-nums` aligns digit positions but does not align decimal points across different-magnitude values. Two fixes:

**Option A — pad with hair spaces (Bloomberg approach):**
```ts
function alignDecimal(value: number, totalDigits = 8): string {
  const s = value.toFixed(2);
  const [int] = s.split(".");
  const padNeeded = totalDigits - int.length;
  return " ".repeat(padNeeded) + s; // hair space, non-breaking
}
```

**Option B — fixed-width columns with right-align (TradingView approach):**
```tsx
<div className="grid grid-cols-[1fr_120px_120px_120px] gap-2 tabular-nums">
  <div>{symbol}</div>
  <div className="text-right">{formatPrice(price)}</div>
  <div className="text-right">{formatQty(qty)}</div>
  <div className="text-right">{formatValue(value)}</div>
</div>
```

Use B by default. Use A only when values must fit in flowing text.

## Common Mistakes

| Mistake | Why it breaks | Fix |
|---|---|---|
| `text-green-500` / `text-red-500` | Doesn't respect theme, no light/dark, generic look | Semantic tokens: `text-positive` / `text-negative` |
| `bg-${color}-500/10` dynamic class | Tailwind JIT strips it, renders without bg | Static class map: `{ up: "bg-positive/10", down: "bg-negative/10" }[dir]` |
| `font-medium` numbers without `tabular-nums` | Digits shift width on every update | Always pair `tabular-nums` with any updating number |
| Hard-coded `bg-zinc-950` | Breaks light theme | Use `bg-surface` from CSS variable tokens |
| `text-emerald-400` for prices | Color overload, makes deltas harder to spot | Color only deltas/signals. Keep prices neutral. |
| `toFixed(2)` for all prices | Wrong for BTC ($100K, 0 dp needed) and SHIB ($0.00001, 8 dp needed) | Magnitude-aware: see `references/number-formatting.md` |
| Re-rendering whole row on tick | Drops frames at 100+ symbols streaming | Isolate updating cell, memoize the rest |
| No staleness indicator | Users trade on dead data | Show grey/dim state when last update > N seconds |
| Color-only gain/loss | 8% of men can't distinguish red/green | Add ▲ ▼ arrows or +/- prefix |
| Animation libraries for ticks | Bundle bloat, GPU thrash at scale | CSS transitions on `data-*` attributes |
| `text-zinc-500` for axis labels | Generic AI tell | Use `text-text-muted` token |
| Centered numbers in tables | Eye can't compare magnitudes | Right-align numbers, left-align labels |

## Red Flags — Stop and Reread

When writing financial UI you may rationalize. These mean stop:

- "It's just a prototype, I'll fix tokens later" — semantic tokens take the same time to write as raw colors. Write them now.
- "The user won't notice digit shift" — they will, especially on a watchlist. It's the #1 tell of an unprofessional trading UI.
- "Tailwind should expand `bg-${color}-500/10` since the strings exist somewhere" — JIT does not scan dynamic templates. Use a static map.
- "Light theme isn't needed" — Bloomberg, IBKR, and TradingView all ship both. Light theme is a serious-trader signal. Build with CSS variables from day one.
- "Mono font for tickers looks dated" — it's the opposite. Bloomberg, Reuters, TradingView all use mono for tickers/symbols. It's a professionalism signal.
- "I don't need a tick flash for a non-realtime page" — every list of prices that ever updates should flash. Even hourly updates benefit.

## Industry Reference Points

| Pattern | Who does it best | Why study it |
|---|---|---|
| Order book depth bars (asks fill right→left, bids left→right) | Kraken, Binance, Coinbase Pro | Standard convention; users expect it |
| Compact density toggle | TradingView, Bloomberg | Pro users want maximum data per screen |
| Tick-flash on price cells | Robinhood, Coinbase, Massive dashboards | Confirms data is live without distraction |
| OHLC color coding (green hollow / red filled candles) | TradingView | Industry standard candle styling |
| Status pills for orders (filled/partial/working/cancelled/rejected) | Interactive Brokers, Coinbase Pro | Lets traders scan order state in milliseconds |
| Sparklines next to prices | Robinhood, Yahoo Finance, Massive | Compact trend signal without consuming chart space |
| "Last / Mark / Index" price split for derivatives | Binance, Bybit, dYdX | Critical for liquidation awareness |
| Significant-figure pricing for low-value tokens | Coinbase, CoinGecko | `$0.00001234` is readable; `$0.00` is broken |
| Color-blind safe pairs (blue/orange) as alternative to red/green | Bloomberg accessibility mode | Required for accessibility-serious products |

See `references/industry-patterns.md` for screenshots' worth of detail on each.

## Verification

Before claiming a financial UI is done, check:

- [ ] Every number has `tabular-nums`
- [ ] Every color is a semantic token, no raw `text-green-*` / `bg-zinc-*`
- [ ] Light theme renders correctly (toggle and verify)
- [ ] Streaming prices flash on update
- [ ] Stale data state is visible (e.g., dim or grey when > N seconds old)
- [ ] Positive returns show `+` prefix
- [ ] Numbers are right-aligned, labels are left-aligned
- [ ] Tickers use mono font
- [ ] No `bg-${var}` or other dynamic Tailwind classes
- [ ] Color is paired with non-color signal (arrow, icon, sign, position)
- [ ] Order/trade states use status pills, not just text color
- [ ] At least 5 rows visible without scroll on a typical laptop screen (density check)
