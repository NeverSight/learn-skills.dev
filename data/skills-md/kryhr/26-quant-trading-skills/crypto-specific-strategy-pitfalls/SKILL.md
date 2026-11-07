---
name: crypto-specific-strategy-pitfalls
description: 'Use this skill when building, backtesting, or reviewing a strategy that trades crypto spot or perpetual futures, in addition to the general checks elsewhere in this repo. Also use it when a user is porting a strategy originally designed for traditional markets over to crypto without having considered what''s actually different about crypto market structure. This skill exists because crypto markets have specific structural features, funding rates, exchange fragmentation, wash-trading-inflated volume figures, that don''t exist in traditional markets and that a strategy or backtest built without accounting for them will get quietly wrong.'
---

# Crypto-Specific Strategy Pitfalls

## Why this matters

[market-data-sourcing](../market-data-sourcing/SKILL.md) notes that crypto data is the easiest and cheapest asset class to source, but easy-to-source doesn't mean easy-to-correctly-model; crypto markets have real structural features that don't have a direct equivalent in traditional markets, and a strategy (or a backtest of one) that doesn't account for them can look fine on paper while missing real, material costs and risks that only show up once actually trading.

## Do this

### Model perpetual futures funding rate payments explicitly, as a real, ongoing cost or income stream

Perpetual futures (the dominant instrument on most crypto derivatives exchanges) have no expiry, and instead use a periodic funding rate payment between long and short positions to keep the perpetual's price tethered to the underlying spot price. This funding rate can be a meaningful, ongoing cost (or, for a strategy structured to receive it, income) that a backtest ignoring it will materially misstate, especially for any strategy holding a directional position for an extended period; model actual historical funding rates explicitly, per [transaction-cost-and-market-impact-modeling](../transaction-cost-and-market-impact-modeling/SKILL.md)'s general principle of modeling real, ongoing position costs.

### Be skeptical of reported trading volume, since wash trading has historically inflated apparent liquidity on many exchanges

Crypto exchanges, especially smaller or less-regulated ones, have a documented history of wash-traded or otherwise artificially inflated volume figures, which matters directly for [transaction-cost-and-market-impact-modeling](../transaction-cost-and-market-impact-modeling/SKILL.md)'s market-impact modeling: a strategy sized against apparent liquidity that's actually substantially wash-traded will face real market impact far larger than the reported volume figures would suggest. Prefer volume and liquidity data from exchanges with a credible reputation for genuine volume, and treat reported liquidity on less-established venues with real skepticism when sizing a strategy.

### Account for exchange fragmentation and the resulting price/liquidity differences across venues

Unlike most traditional asset classes with a small number of dominant, well-regulated venues, crypto trading is fragmented across many exchanges with genuinely different prices, liquidity, and fee structures at any given moment. A strategy or backtest that treats "the price" of a crypto asset as a single, unambiguous number, without specifying which venue's price and liquidity it's actually assuming, is glossing over a real source of both opportunity (venue-based arbitrage) and risk (executing on a different, less liquid venue than the backtest assumed).

### Explicitly consider exchange counterparty and custody risk, which is a real, non-market risk specific to this asset class

Crypto exchange failures, hacks, and insolvencies (including of major, well-known exchanges) have happened and are a real, distinct risk category beyond normal market risk: capital held on an exchange is exposed to that exchange's own solvency and security, in a way that's structurally different from the counterparty risk of, for instance, a regulated traditional brokerage. This isn't a backtest-modelable risk in the usual sense, but it needs to be an explicit part of position sizing, custody decisions (how much capital sits on an exchange versus in self-custody), and venue selection, not an unconsidered background assumption.

### Check for and account for the actual, real-world tax and regulatory treatment relevant to the specific strategy and jurisdiction

Crypto's tax treatment (frequently different from traditional securities, and evolving) and regulatory status can materially affect a strategy's real, after-tax, after-compliance-cost economics in ways a pure backtest never touches. This isn't a market-risk consideration, but it's a real cost/constraint that needs to be understood before committing meaningful capital, since it can change a strategy's actual viability independent of its trading performance.

## Never do this

- Never backtest a perpetual futures strategy without modeling actual historical funding rate payments as a real, ongoing cost or income stream.
- Never size a strategy against reported exchange volume/liquidity without considering that a meaningful fraction of it may be wash-traded, especially on smaller or less-established venues.
- Never treat "the price" of a crypto asset as a single, venue-agnostic number when building or backtesting a strategy that will actually execute on a specific venue with its own price and liquidity.
- Never leave exchange counterparty/custody risk as an unconsidered background assumption; make it an explicit part of sizing and venue/custody decisions.
- Never commit meaningful capital to a crypto strategy without understanding the actual tax and regulatory treatment relevant to that specific strategy and jurisdiction.

## Verification checklist

- [ ] Perpetual futures funding rate payments are modeled explicitly using actual historical rates, not ignored or assumed negligible
- [ ] Sizing and market-impact assumptions account for the possibility of wash-traded or inflated reported volume, especially on less-established exchanges
- [ ] The specific venue(s) whose price and liquidity the strategy actually assumes are identified explicitly, rather than treating crypto price as one venue-agnostic number
- [ ] Exchange counterparty and custody risk is an explicit part of position sizing and venue/custody decisions, not an unconsidered background assumption
- [ ] The actual tax and regulatory treatment relevant to this specific strategy and jurisdiction has been checked before committing meaningful capital
