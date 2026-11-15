---
name: financial-ui-styles
description: Use when building any financial UI to select a visual aesthetic — Bloomberg-style pro terminal, TradingView-style modern pro, Robinhood-style retail, FT-style editorial, Massive/Stripe-style API dashboard, Coinbase/Binance-style crypto exchange, TastyTrade-style options pro, Wise-style retail light, Uniswap-style DeFi, iOS Stocks-style Apple native, Yahoo Finance-style prosumer dark, AlphaSense-style research terminal, AlphaSpace-style consumer terminal, or Gloomberb-style terminal TUI. Loads AFTER `financial-ui-patterns` (which handles correctness). Read when user says "make it look like X" or specifies a brand/style direction.
---

# Financial UI Styles

## Overview

Fourteen distinct visual styles for financial UIs. The base skill `financial-ui-patterns` handles correctness (tabular nums, semantic tokens, tick flash, accessibility). This skill handles **visual style** — the brand-flavored layer on top.

**Layering:**
```
product-design                  → atomic decisions for any SaaS UI
financial-ui-patterns           → finance-specific correctness (mandatory)
financial-ui-styles (this)      → brand style / visual polish (pick one)
```

You always apply the lower layers. You pick exactly one style on top.

## When to Use

- User says "make it look like X" where X is a financial product or aesthetic
- User specifies brand/aesthetic direction ("Bloomberg style", "Robinhood feel", "FT-like", "API-dashboard aesthetic")
- Starting a new financial UI from scratch and picking the visual direction
- Refactoring an existing financial UI toward a specific aesthetic

**Don't use for:** marketing pages, blog posts, anything not loading data. Styles are calibrated for data-dense UIs.

## How to Pick

Match the user and product category, not the brand mood the founder asked for.

| If the user is... | And the product is... | Pick |
|---|---|---|
| Institutional / desk trader | Desktop terminal, command-line driven, max density | `pro-terminal` |
| Pro / prosumer trader | Modern web app, dense but not terminal-dense | `modern-pro-dark` |
| Mainstream prosumer | Chart-forward consumer market data, watchlist + multi-ticker compare | `yahoo-prosumer` |
| Self-directed retail-pro | Multi-panel custom terminal with embedded AI agent, themed views | `alphaspace` |
| Buy-side analyst | Document/transcript search, sentiment, AI summaries | `research-terminal` |
| Active options trader | Strategy builder, Greeks-forward | `tasty-pro` |
| Centralized crypto trader | Exchange (CEX), spot + perps | `crypto-exchange` |
| Onchain / DeFi user | DEX, swap UI, wallet-connect first | `defi-native` |
| Retail consumer | Mobile-first investing app, dark | `retail-polish-dark` |
| Retail consumer | Money app / neobank, light, friendly | `retail-polish-light` |
| News / analysis reader | Editorial layout with embedded market data | `editorial-financial` |
| Developer / admin | API console, dashboard, docs-adjacent | `api-dashboard` |
| iOS user | Native companion or web that mimics native iOS | `apple-native` |
| Indie / developer trader | Tiled multi-pane terminal (TUI) dashboard, muted, theme-swappable | `retro-tui` |

If two rows fit, pick the one whose **reference product** ships the closest UX. Don't blend.

## Style Index

| Style | Reference shipping products | Reference file |
|---|---|---|
| `modern-pro-dark` | TradingView, Kraken Pro, Hyperliquid | `references/modern-pro-dark.md` |
| `pro-terminal` | Bloomberg Terminal, IBKR TWS, ThinkOrSwim | `references/pro-terminal.md` |
| `tasty-pro` | TastyTrade | `references/tasty-pro.md` |
| `crypto-exchange` | Coinbase Advanced, Binance, Bybit | `references/crypto-exchange.md` |
| `retail-polish-dark` | Robinhood, Public | `references/retail-polish-dark.md` |
| `retail-polish-light` | Wise, Revolut, Cash App | `references/retail-polish-light.md` |
| `editorial-financial` | FT.com, Bloomberg.com, WSJ | `references/editorial-financial.md` |
| `api-dashboard` | Massive, Stripe, Vercel, Linear | `references/api-dashboard.md` |
| `defi-native` | Uniswap, Jupiter, Solana ecosystem | `references/defi-native.md` |
| `apple-native` | iOS Stocks, macOS Stocks widget | `references/apple-native.md` |
| `yahoo-prosumer` | Yahoo Finance (current redesign), Seeking Alpha, Investing.com | `references/yahoo-prosumer.md` |
| `alphaspace` | Yahoo Finance AlphaSpace (Gold tier), TradingView desktop, Bloomberg Terminal (layout reference) | `references/alphaspace.md` |
| `research-terminal` | AlphaSense, Visible Alpha, FactSet, Tegus | `references/research-terminal.md` |
| `retro-tui` | Gloomberb, lazygit, k9s, btop | `references/retro-tui.md` |

Each file ships with CSS variable token set (dark + light), typography table, density numbers, visual rules, style-specific patterns, anti-patterns, example component code, reference URLs, and verification checklist.

## Style Summaries

### modern-pro-dark — TradingView, Kraken Pro, Hyperliquid
Dark slate background. Single blue or purple accent. Sans body + tabular nums + mono on tickers. 28-32px table rows, 24-28px order book. Hairline borders. 4-6px radius. No gradients, no shadows beyond elevation. The default for serious pro consumer products.

### pro-terminal — Bloomberg, IBKR TWS, ThinkOrSwim
Black or near-black with amber or cyan accent. Mono-everywhere, ALL CAPS section labels. 24-28px rows, max density. 0-2px radius. Hairline borders. Function-key shortcuts in tooltips. Institutional desktop aesthetic.

### tasty-pro — TastyTrade
Black background, pink-magenta accent, green/red signals. Sans + tabular. Options-focused: prominent strikes, Greeks readability. 32-36px rows. Distinctive enough to call out separately even though it shares Modern Pro fundamentals.

### crypto-exchange — Coinbase Advanced, Binance, Bybit
Dark slate or near-black. Yellow (Binance) or blue (Coinbase) accent. Higher cell-level color saturation than Modern Pro. Subtle gradients OK on chart areas. 28-32px rows. More aggressive use of colored cells in tables.

### retail-polish-dark — Robinhood, Public
Pure or near-pure black. Single signal color (often brand green). Very large display numbers (32-48px hero). Generous whitespace. 48-56px row heights. 12-20px radius (large, friendly). Gamification-appropriate. Mobile-first feel even on web.

### retail-polish-light — Wise, Revolut, Cash App
White or near-white background. Colorful brand palette. Sans body with friendly weight choices. Big whitespace. 40-48px rows. 16-20px radius. Mobile-style cards translated to web.

### editorial-financial — FT.com, Bloomberg.com, WSJ
Cream/beige (FT salmon-on-pinkish-beige) or off-white. Serif headlines, sans body, mono for data tables. Sharper radii (0-4px). 36-44px rows. Longer-form analysis blocks between data. Newspaper sensibility.

### api-dashboard — Massive, Stripe, Vercel, Linear
Near-black or near-white. Single brand accent. Heavy on mono for code/IDs/keys. Status pills used aggressively. 40-48px rows (more relaxed than trading). Generous form fields. Documentation-adjacent aesthetic. Copy buttons everywhere.

### defi-native — Uniswap, Jupiter, Solana ecosystem
Gradients permitted (radial backgrounds, glassy panels with backdrop-blur). Saturated brand palette (Uniswap pink, Solana purple/teal). Playful, less institutional. Often light or hybrid theme.

### apple-native — iOS Stocks, macOS Stocks widget
Translucent surfaces, SF Pro Display + SF Pro Mono. System blur (vibrancy). Seamless light/dark transitions. Refined iOS feel. Use only for native companions or web that explicitly mimics native iOS.

### yahoo-prosumer — Yahoo Finance (current redesign), Seeking Alpha, Investing.com
Slate-blue near-black surfaces (#0E111A, not neutral). Single bright Yahoo-style blue accent. Sans throughout — tickers rendered in bold sans, not mono. Signature: single-ticker quote pages with hero price + delta + after-hours + OHLC stats + news strip. Multi-ticker compare chart secondary. Top ticker tape pinned, watchlist sidebar. 36-40px rows. Sits between Modern Pro Dark (less terminal-dense) and Retail Polish Dark (less consumer-flat).

### alphaspace — Yahoo Finance AlphaSpace, TradingView desktop, Bloomberg Terminal (layout reference)
Yahoo's premium terminal. Slate-blue surfaces with a bright green primary accent (the defining cue vs `yahoo-prosumer`'s blue). Multi-panel canvas (overview + chart + news + holdings + fundamentals coexisting). View-driven left sidebar with named themed dashboards (Banks & Credit, Macro, Crypto, AI Software, etc.) plus "My Views". First-class AI-agent rail pinned right ("Ask Yahoo Scout"-style), with suggested-prompt list — never collapsed. Two-row ticker tape (broad market + active theme). Bloomberg's workspace pattern reskinned for serious retail.

### research-terminal — AlphaSense, Visible Alpha, FactSet, Tegus
Light by default, near-white off-flat surfaces, saturated institutional blue accent. Document-first canvas — search bar always-on at top, source-type pills (10-K, Earnings Call, Press Release) on every result, and the signature yellow keyword highlights inside excerpt cards. AI summary block is a first-class component with a distinct accent rail and citation links. Sentiment shown as numeric + label (`Bullish · +0.42`), never color-only. Relaxed density (44-52px rows). Built for analysts who read for hours, not chart-watchers.

### retro-tui — Gloomberb, lazygit, k9s, btop
Clean terminal UI. Near-black ground, muted white/grey mono text, green/red only on values, hairline dividers, `:: Title` panel headers, tiled multi-pane grid with traffic-light window chrome. Swappable phosphor palette (22 themes) plus an optional CRT mode (scanlines + phosphor bloom) that stays **off by default**. Warm "Paper" light variant. The indie/developer cousin of `pro-terminal` — same density, muted instead of institutional. Palettes adapted from Gloomberb (MIT).

## Cross-Cutting Rules

These apply regardless of style:

1. **Base correctness from `financial-ui-patterns` still applies.** Tabular nums, semantic tokens, tick flash, accessibility, decimal alignment. A style overrides token *values* and *aesthetic choices*, not correctness rules.
2. **One style per product.** Don't mix Modern Pro Dark and Editorial Financial in the same UI; the brain reads it as broken.
3. **Light theme matters.** Every style must have a light variant. Pro Terminal's light variant uses light-amber-on-cream; Modern Pro Dark's light variant uses Supabase-slate. Define both.
4. **Density follows style.** Pro Terminal is denser than Retail Polish Dark. Don't fight the style's density rules to fit more data.
5. **Mono usage is style-specific.** Pro Terminal uses mono everywhere. Retail Polish minimal. Modern Pro on tickers only. Editorial Financial on data tables only. Apple Native on Greeks/numbers only.

## When NOT to Use This Skill

- Marketing pages, landing pages, blog content
- Product UI with no financial data (CRMs, project tools, generic SaaS)
- One-off design tests where you want full freedom

## Common Mistakes

| Mistake | Why bad | Fix |
|---|---|---|
| Mixing two styles in one product | Reads as inconsistent / broken | One style per product |
| Picking style based on user's wishful brand mood | Styles describe shipping products; picking by mood often picks wrong | Pick based on user type and product category |
| Skipping the `financial-ui-patterns` base | Correctness fails (no tabular nums, wrong colors) | Always apply base layer first |
| Using DeFi Native or Crypto Exchange for traditional finance | Aesthetic mismatch users won't trust | Match audience expectation |
| Hard-coding style token values inline | Brittle to theme switches | Use CSS variables; style = token set |
| Defining style only in dark mode | Pro users want light during the day | Ship both light + dark for every style |

## Verification

Before declaring style implementation done:

- [ ] One and only one style is applied across the product
- [ ] Light + dark variants both render correctly
- [ ] Base `financial-ui-patterns` correctness still passes (tabular nums, semantic tokens, etc.)
- [ ] Mono usage matches style's rules (everywhere / tickers only / data tables only / minimal)
- [ ] Density matches style's row-height range
- [ ] Accent color and gradient/radius rules match style
- [ ] If style is a stub: have you loaded reference URLs and matched key characteristics?

## See Also

- `financial-ui-patterns` — REQUIRED base layer
- `product-design` — atomic decisions for any SaaS UI
- `frontend-design` plugin — generic UI generation that avoids generic AI aesthetics
