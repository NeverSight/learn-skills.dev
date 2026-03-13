---
name: return-calculations
description: "Compute and compare investment return metrics including TWR, MWR/IRR, CAGR, and annualized returns. Use when the user asks about portfolio performance calculation, comparing manager returns, linking sub-period returns, understanding why different return methods give different numbers, or converting returns across time periods. Also trigger when users mention 'how much did I make', 'annual return', 'compound growth', 'dollar-weighted vs time-weighted', 'what was my rate of return', 'geometric vs arithmetic mean', 'log returns', or ask about the effect of cash flows on reported returns."
---

# Return Calculations

## Purpose
This skill enables Claude to compute, explain, and compare investment return metrics across different methodologies and time horizons. It covers the full spectrum from simple holding-period returns through time-weighted and money-weighted returns, ensuring the appropriate metric is selected for each analytical context.

## Layer
0 — Mathematical Foundations

## Direction
retrospective

## When to Use
- User asks about calculating investment returns
- Comparing returns across different time periods
- Understanding arithmetic vs geometric vs log returns
- Computing CAGR, TWR, MWR/IRR
- Linking sub-period returns

## Core Concepts

### Simple (Holding Period) Return
The most basic measure of investment performance over a single period, capturing price change plus any income received.

$$R = \frac{V_{end} - V_{begin} + D}{V_{begin}}$$

where:
- `V_end` = ending value
- `V_begin` = beginning value
- `D` = distributions (dividends, interest) received during the period

### Arithmetic Mean Return
The simple average of a series of periodic returns. Represents the expected return for any single period.

$$R_a = \frac{1}{n} \sum_{i=1}^{n} R_i$$

The arithmetic mean is always greater than or equal to the geometric mean. It is an unbiased estimator of the expected single-period return but overstates the compounded growth rate.

### Geometric Mean Return
The constant rate that, if earned each period, would produce the same terminal wealth as the actual sequence of returns.

$$R_g = \left(\prod_{i=1}^{n}(1 + R_i)\right)^{1/n} - 1$$

The geometric mean captures the effects of compounding and volatility drag. It is always the correct choice for describing realized multi-period growth.

### Log (Continuously Compounded) Return
The natural logarithm of the wealth ratio. Log returns are time-additive, making them convenient for multi-period aggregation and statistical modeling.

$$r = \ln\left(\frac{V_{end}}{V_{begin}}\right)$$

Properties:
- Time-additive: `r_total = r_1 + r_2 + ... + r_n`
- Conversion: `R_simple = e^r - 1` and `r = ln(1 + R_simple)`
- More symmetric and closer to normally distributed than simple returns for small magnitudes

### CAGR (Compound Annual Growth Rate)
The annualized geometric return that equates the beginning value to the ending value over a given number of years.

$$CAGR = \left(\frac{V_{end}}{V_{begin}}\right)^{1/n} - 1$$

where `n` is measured in years. CAGR smooths out volatility and provides a single annualized growth figure.

### Time-Weighted Return (TWR)
Chain-links sub-period returns calculated between each external cash flow, thereby removing the effect of cash flow timing on the measured return. TWR measures the manager's investment skill independent of investor deposit/withdrawal decisions.

$$1 + R_{TWR} = \prod_{i=1}^{n}(1 + R_i)$$

where each sub-period return `R_i` is computed between consecutive cash flow dates:

$$R_i = \frac{V_{end,i}}{V_{begin,i} + CF_i}$$

In practice, exact TWR requires portfolio valuation on every cash flow date. The Modified Dietz method approximates TWR when daily valuations are unavailable.

### Money-Weighted Return (MWR / IRR)
The internal rate of return that sets the net present value of all cash flows (contributions, withdrawals, and terminal value) to zero.

$$0 = \sum_{t=0}^{T} \frac{CF_t}{(1 + r)^t}$$

MWR reflects the actual investor experience because it is sensitive to the timing and magnitude of cash flows. It rewards (penalizes) investors who add capital before good (bad) periods.

### Annualization
Converts a return measured over any holding period to an equivalent annual rate, assuming compounding.

$$R_{annual} = (1 + R_{period})^{periods\_per\_year} - 1$$

For example, a 2% quarterly return annualizes to `(1.02)^4 - 1 = 8.24%`.

### Sub-Period Linking
Combines returns from contiguous sub-periods into a single cumulative return.

$$(1 + R_{total}) = \prod_{i=1}^{n}(1 + R_i)$$

This is the foundational identity behind TWR and CAGR calculations.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Holding Period Return | `R = (V_end - V_begin + D) / V_begin` | Single-period total return |
| Arithmetic Mean | `R_a = (1/n) * sum(R_i)` | Expected single-period return |
| Geometric Mean | `R_g = [prod(1+R_i)]^(1/n) - 1` | Realized compound growth rate |
| Log Return | `r = ln(V_end / V_begin)` | Time-additive return for modeling |
| CAGR | `(V_end / V_begin)^(1/n) - 1` | Annualized growth over n years |
| TWR | `prod(1 + R_i) - 1` | Manager performance (cash-flow neutral) |
| MWR / IRR | `sum(CF_t / (1+r)^t) = 0`, solve for r | Investor-specific experience |
| Annualization | `(1 + R_period)^(periods/year) - 1` | Standardize to annual basis |
| Sub-Period Linking | `(1 + R_total) = prod(1 + R_i)` | Combine contiguous returns |

## Worked Examples

### Example 1: Computing CAGR from a 5-Year Investment
**Given:** An investment of $10,000 grows to $16,105.10 over exactly 5 years with no intermediate cash flows.

**Calculate:** The compound annual growth rate (CAGR).

**Solution:**

```
CAGR = (V_end / V_begin)^(1/n) - 1
CAGR = (16,105.10 / 10,000)^(1/5) - 1
CAGR = (1.610510)^(0.2) - 1
CAGR = 1.10 - 1
CAGR = 0.10 = 10%
```

The investment grew at a compound annual rate of **10%** per year.

Verification: `$10,000 * (1.10)^5 = $10,000 * 1.61051 = $16,105.10`

### Example 2: TWR vs MWR Divergence with Poorly Timed Cash Flow
**Given:** A fund has the following history:
- Start of Year 1: Portfolio value = $100,000
- End of Year 1: Portfolio value = $120,000 (return = +20%)
- Start of Year 2: Investor deposits $100,000, bringing portfolio to $220,000
- End of Year 2: Portfolio value = $198,000 (return = -10%)

**Calculate:** Both TWR and MWR, and explain the divergence.

**Solution:**

**Time-Weighted Return (TWR):**
```
Sub-period 1 return: R_1 = (120,000 - 100,000) / 100,000 = +20%
Sub-period 2 return: R_2 = (198,000 - 220,000) / 220,000 = -10%

TWR (cumulative) = (1 + 0.20) * (1 + (-0.10)) - 1
                  = 1.20 * 0.90 - 1
                  = 1.08 - 1
                  = +8.0%

TWR (annualized) = (1.08)^(1/2) - 1 = 3.92%
```

**Money-Weighted Return (MWR / IRR):**
Cash flows from the investor's perspective:
- t=0: -$100,000 (initial investment)
- t=1: -$100,000 (additional deposit)
- t=2: +$198,000 (terminal value)

Solve: `-100,000 + (-100,000)/(1+r) + 198,000/(1+r)^2 = 0`

Testing r = -0.0051 (approximately -0.51%):
```
-100,000 + (-100,000)/0.9949 + 198,000/0.9899
= -100,000 - 100,512.6 + 200,020.2
approx -492.4  (close to zero; actual IRR approx -0.48%)
```

The MWR is approximately **-0.48% annualized**.

**Interpretation:** The TWR of +3.92% annualized reflects the manager's skill: the fund gained 20% then lost 10%, netting +8% over two years. The MWR of approximately -0.48% reflects the investor's experience: more money was at risk during the losing year (Year 2) because of the large deposit, so the investor's dollar-weighted outcome was slightly negative. This divergence highlights why TWR is preferred for evaluating manager performance, while MWR better describes the specific investor's realized result.

## Common Pitfalls
- Confusing arithmetic and geometric means: the arithmetic mean is always greater than or equal to the geometric mean (AM-GM inequality). Using arithmetic mean to project compounded growth overstates terminal wealth.
- Using arithmetic mean for multi-period compounding: always use geometric mean or CAGR when describing compound growth over multiple periods.
- Annualizing returns from very short periods: annualizing a 2% weekly return yields `(1.02)^52 - 1 = 180%`, which amplifies noise and is misleading. Annualization is most meaningful for periods of at least one year.
- Ignoring cash flow timing when TWR is appropriate: MWR conflates manager skill with investor timing decisions. Use TWR for manager evaluation.
- Double-counting dividends: if the ending value `V_end` already includes reinvested dividends, do not add `D` separately in the holding period return formula.

## Cross-References
- **time-value-of-money** (core plugin, Layer 0): NPV, IRR, and discounting concepts overlap with MWR calculations
- **statistics-fundamentals** (core plugin, Layer 0): Arithmetic and geometric means, return distribution analysis

## Reference Implementation
See `scripts/return_calculations.py` for computational helpers.
