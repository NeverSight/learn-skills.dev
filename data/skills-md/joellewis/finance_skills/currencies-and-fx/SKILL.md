---
name: currencies-and-fx
description: "Analyze currency markets, exchange rate mechanics, and FX risk management for international portfolios. Use when the user asks about exchange rates, FX hedging, interest rate parity, carry trades, forward premiums, cross rates, or currency overlay programs. Also trigger when users mention 'strong dollar', 'weak euro', 'hedging foreign stocks', 'purchasing power parity', 'currency risk in my portfolio', 'EUR/USD', 'yen carry trade', or ask whether to hedge international investments."
---

# Currencies and FX

## Purpose
Analyze currency markets including spot and forward exchange rates, interest rate parity relationships, FX hedging mechanics, cross rate derivation, and carry trade dynamics. This skill is essential for international investing, currency risk management, and understanding how interest rate differentials drive forward exchange rates.

## Layer
2 — Asset Classes

## Direction
both

## When to Use
- User asks about currency analysis, exchange rates, or FX markets
- User asks about FX hedging or managing currency risk in international portfolios
- User asks about interest rate parity (covered or uncovered)
- User asks about carry trades or currency carry strategies
- User asks about cross rates or currency quoting conventions
- User asks about forward exchange rates or forward premium/discount
- User asks about purchasing power parity (PPP) or real exchange rates
- User asks about currency overlay programs

## Core Concepts

### Spot Rate
The price of one currency in terms of another for immediate delivery (T+2 settlement). Quoting convention: EUR/USD = 1.10 means 1 euro costs 1.10 US dollars. Some pairs are quoted as the number of foreign currency units per dollar (USD/JPY = 150), while others are quoted as dollars per foreign unit (EUR/USD = 1.10, GBP/USD = 1.27).

### Forward Rate
The agreed exchange rate for a future currency transaction, determined by the interest rate differential between the two currencies. Forward rates are not forecasts of future spot rates — they are arbitrage-determined prices that reflect the cost of carry.

### Covered Interest Rate Parity (CIP)
An arbitrage condition that must hold (and empirically does, closely):

F/S = (1 + r_d) / (1 + r_f)

where F = forward rate, S = spot rate, r_d = domestic interest rate, r_f = foreign interest rate (for the same period). If CIP were violated, riskless arbitrage would be possible by borrowing in one currency, converting, investing, and locking in the return with a forward.

### Uncovered Interest Rate Parity (UIP)
A theoretical (not arbitrage-enforced) condition:

E(S_t) / S_0 = (1 + r_d) / (1 + r_f)

UIP predicts that the expected future spot rate adjusts to offset interest rate differentials. Empirically weak — high-interest-rate currencies tend to appreciate rather than depreciate as UIP predicts, which is why carry trades can be profitable.

### Forward Premium/Discount
Forward Premium = (F - S) / S = (r_d - r_f) / (1 + r_f)

If the domestic interest rate exceeds the foreign rate, the forward rate is at a premium to spot (the foreign currency is more expensive forward). If the domestic rate is lower, the forward is at a discount.

### Carry Trade
Borrow in a low-interest-rate currency and invest in a high-interest-rate currency, profiting from the interest rate differential. Profitable when UIP fails (i.e., the high-rate currency does not depreciate enough to offset the interest differential). Carry trades exhibit positive returns on average but with significant tail risk — sudden unwinds during risk-off episodes can cause severe losses (negative skewness, fat tails).

### Cross Rate
Derive the exchange rate between two currencies using their rates against a common third currency:

EUR/GBP = (EUR/USD) / (GBP/USD)

For example, if EUR/USD = 1.10 and GBP/USD = 1.27, then EUR/GBP = 1.10 / 1.27 = 0.8661.

### Currency Hedging
Use forward contracts to eliminate FX risk in international investments. A US investor with EUR assets can sell EUR forward to lock in the conversion rate. The hedging cost equals the interest rate differential between the two currencies (per CIP). When the domestic rate exceeds the foreign rate, hedging earns a positive return; when it is lower, hedging has a cost.

### Real Exchange Rate
Adjusts the nominal exchange rate for relative price levels:

Real Rate = Nominal Rate × (Foreign Price Level / Domestic Price Level)

Changes in the real exchange rate reflect changes in competitiveness. If the real rate appreciates, domestic goods become more expensive relative to foreign goods.

### Purchasing Power Parity (PPP)
The long-run anchor for exchange rates. PPP posits that exchange rates should adjust so that identical goods cost the same across countries. Empirically, PPP holds poorly in the short run but provides a reasonable guide to fair value over decades. Deviations from PPP can persist for years.

### Currency Overlay
A systematic hedging program for international portfolios, managed separately from the underlying asset allocation. Overlay managers implement hedging ratios (e.g., hedge 50% of foreign exposure) and may make tactical adjustments based on valuation, carry, and momentum signals.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| CIP Forward Rate | F = S × (1+r_d)/(1+r_f) | Arbitrage-determined forward |
| UIP Expected Spot | E(S_t) = S_0 × (1+r_d)/(1+r_f) | Theoretical future spot |
| Forward Premium | (F-S)/S = (r_d-r_f)/(1+r_f) | Forward vs spot differential |
| Cross Rate | A/B = (A/C) / (B/C) | Derive from common currency |
| Real Exchange Rate | q = e × (P*/P) | Competitiveness measure |
| Hedging Cost | ≈ r_d - r_f (annualized) | Cost to hedge FX exposure |

## Worked Examples

### Example 1: Forward Rate Calculation
**Given:** USD/JPY spot = 150, US 1-year rate = 5%, Japan 1-year rate = 0.5%
**Calculate:** 1-year forward rate
**Solution:**
F = S × (1 + r_JPY) / (1 + r_USD)
F = 150 × (1 + 0.005) / (1 + 0.05)
F = 150 × 1.005 / 1.05
F = 150 × 0.95714 = 143.57

The forward rate is 143.57 JPY/USD. The yen is at a forward premium (fewer yen per dollar forward than spot) because Japanese rates are lower. A US investor hedging yen assets back to dollars would receive this favorable forward rate, effectively earning the interest rate differential.

### Example 2: Hedging Cost for EUR Investor
**Given:** EUR/USD spot = 1.10, EUR 1-year rate = 3%, USD 1-year rate = 5%
**Calculate:** Annual cost/benefit of hedging USD exposure back to EUR
**Solution:**
Forward rate: F = 1.10 × (1.03)/(1.05) = 1.10 × 0.98095 = 1.0790

A EUR investor hedging USD assets sells USD forward at 1.0790 EUR/USD.
Hedging benefit = (S - F) / S = (1.10 - 1.079) / 1.10 = 1.91%

Because EUR rates (3%) are lower than USD rates (5%), the EUR investor earns a positive hedging return of approximately 2% (the interest rate differential). The hedged return on USD assets for a EUR investor is the USD return plus approximately 2% from the hedge.

## Common Pitfalls
- Currency quoting conventions — EUR/USD vs USD/JPY use opposite conventions; always clarify which currency is base and which is quote
- Confusing nominal and real interest rate differentials — CIP uses nominal rates; real rate differentials affect real exchange rates differently
- Carry trade crash risk — carry strategies exhibit negative skewness and fat tails; profits accumulate slowly but losses can be sudden and severe
- CIP holds by arbitrage; UIP is a theory that often fails empirically — do not assume forward rates predict future spot rates

## Cross-References
- **historical-risk** (wealth-management plugin, Layer 1a): return measurement in multi-currency portfolios
- **equities** (wealth-management plugin, Layer 2): international equity investing and currency effects
- **fixed-income-sovereign** (wealth-management plugin, Layer 2): international bond investing and rate differentials
- **portfolio-construction** (wealth-management plugin, Layer 3): currency hedging decisions in portfolio context

## Reference Implementation
See `scripts/currencies_and_fx.py` for computational helpers.
