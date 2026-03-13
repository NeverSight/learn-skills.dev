---
name: performance-reporting
description: "Generate clear, accurate performance reports for investment portfolios with benchmarks, attribution, and risk dashboards. Use when the user asks about portfolio performance reports, return summaries, benchmark comparison, risk dashboards, goal progress tracking, or GIPS-compliant reporting. Also trigger when users mention 'quarterly report', 'how did my portfolio do', 'time-weighted vs money-weighted return', 'annualized returns', 'net-of-fee performance', 'rolling Sharpe', or ask how to present investment results to clients."
---

# Performance Reporting — Reporting & Communication

## Purpose
Generate clear, accurate, and contextually rich performance reports for investment portfolios. This skill covers return calculation and presentation, benchmark comparison, attribution analysis, risk dashboards, goal progress tracking, and visualization best practices — all with an emphasis on honest, plain-language communication that serves the reader.

## Layer
8 — Reporting & Communication

## Direction
retrospective

## When to Use
- Creating portfolio performance reports (monthly, quarterly, annual)
- Summarizing investment returns across multiple time periods
- Comparing portfolio performance to appropriate benchmarks
- Presenting attribution analysis (what drove returns)
- Building risk dashboards with current and rolling metrics
- Tracking progress toward financial goals (retirement, education, etc.)
- Designing charts and visualizations for investment reporting
- Translating quantitative results into plain-language summaries for clients

## Core Concepts

### Return Reporting
Accurate and consistent return calculation is the foundation of all performance reporting.

**Period returns:** Report standard time periods — MTD (month-to-date), QTD (quarter-to-date), YTD (year-to-date), 1Y, 3Y, 5Y, 10Y, and since inception. Always state the exact inception date.

**Cumulative vs annualized:** Annualize returns only for periods greater than 1 year. Annualizing a 3-month return is misleading because it implies the rate is sustainable for a full year. For periods under 1 year, report cumulative (total) returns only.

- Annualized return formula: `(1 + cumulative_return)^(1/years) - 1`
- For multi-year periods, always present both cumulative and annualized figures so the reader can see total wealth growth and the rate of compounding.

**Gross vs net of fees:** Always specify whether returns are gross or net of management fees, advisory fees, and transaction costs. Net-of-fee returns are what the investor actually experiences and should be the primary presentation. If showing gross returns, also show the fee drag.

**GIPS (Global Investment Performance Standards):** For institutional reporting, follow GIPS requirements — composite construction, full disclosure, verified calculations, and standardized presentation. Even for non-GIPS reports, the principles of fair representation and full disclosure apply.

**Time-weighted vs money-weighted returns:**
- Time-weighted return (TWR) removes the impact of cash flows — use for evaluating the investment manager's skill.
- Money-weighted return (MWR / IRR) reflects the investor's actual experience including timing of contributions and withdrawals — use for evaluating the investor's outcome.

### Benchmark Comparison
A return number in isolation is meaningless. Context requires a benchmark.

**Appropriate benchmark selection:** The benchmark must match the portfolio's investment style, geography, capitalization, and asset class mix. A US large-cap equity portfolio should be compared to the S&P 500 or Russell 1000, not the MSCI Emerging Markets Index.

- For multi-asset portfolios, use a blended benchmark (e.g., 60% S&P 500 / 40% Bloomberg Aggregate).
- The benchmark should be investable — the investor could have held it as a passive alternative.
- Document the benchmark rationale and keep it consistent over time to avoid cherry-picking.

**Active return (alpha):** Portfolio return minus benchmark return. Positive alpha indicates outperformance; negative alpha indicates underperformance.

**Tracking error:** The standard deviation of active returns (portfolio return minus benchmark return) over time. Measures the consistency of active management.

**Information ratio:** Alpha divided by tracking error. Measures the efficiency of active management — how much excess return is generated per unit of active risk. An IR above 0.5 is generally considered good; above 1.0 is exceptional.

### Risk Dashboard
Complement return reporting with risk metrics to give a complete picture.

**Current snapshot metrics:**
- Annualized volatility (standard deviation of returns)
- Maximum drawdown (peak-to-trough decline) and current drawdown
- Value at Risk (VaR) at 95% and 99% confidence levels
- Beta relative to the benchmark

**Rolling metrics:** Show how risk evolves over time, not just a point-in-time estimate.
- 12-month rolling Sharpe ratio
- 12-month rolling volatility
- 36-month rolling beta
- Rolling drawdown chart

**Risk exposure breakdown:**
- Sector concentration and weights vs benchmark
- Factor exposures (value, growth, momentum, quality, size)
- Geographic allocation
- Duration and credit quality (for fixed income)

### Attribution Summary
Explain *why* the portfolio outperformed or underperformed.

**Brinson attribution (allocation vs selection):**
- Allocation effect: did the manager overweight sectors that performed well?
- Selection effect: within each sector, did the manager pick better-performing securities?
- Interaction effect: the combined impact of allocation and selection decisions.

**Factor contribution decomposition:** Decompose returns into contributions from market beta, size, value, momentum, quality, and other factors. The residual is the manager's idiosyncratic alpha.

**Top/bottom contributors (holdings-level):**
- List the 5-10 holdings that contributed most positively and most negatively to portfolio returns.
- Show both the return of the holding and its contribution to total portfolio return (weight x return).
- Provide brief commentary on why each top/bottom contributor performed as it did.

### Goal Progress Tracking
For goal-based investors, frame performance in terms of progress toward their specific objectives.

**On-track assessment:** Is the portfolio on track, behind, or ahead relative to the financial plan?

**Probability of success:** Use Monte Carlo simulation to estimate the probability of reaching the goal given current assets, savings rate, time horizon, and expected return/risk assumptions. Express as a percentage (e.g., "82% probability of funding retirement at age 65").

**Projected vs required return:** Compare the return needed to reach the goal with the expected return of the current portfolio. If the required return exceeds what is reasonable, flag this as a planning gap.

**Milestone tracking:** Express progress as percentage of goal funded. For example: "Retirement goal: $2,000,000. Current portfolio: $850,000. 42.5% funded with 15 years remaining."

### Visualization Best Practices
Charts communicate faster than tables. Choose the right chart for the message.

**Growth of $10,000 chart:** Shows cumulative wealth growth of portfolio vs benchmark over time. Intuitive for all audiences. Use log scale for long time periods to avoid visual distortion from compounding.

**Rolling return chart:** Shows trailing 12-month or 36-month returns over time. Reveals consistency and regime changes. More informative than a single annualized number.

**Drawdown chart:** Shows peak-to-trough declines over time. Viscerally communicates risk in a way that volatility numbers cannot.

**Asset allocation pie/bar chart:** Current allocation vs target/benchmark. Use a grouped bar chart to show both side by side.

**Risk-return scatter plot:** Plot portfolio and benchmark (and possibly peer group) on an annualized return vs annualized volatility plane. Positions in the upper-left (high return, low risk) are desirable.

### Report Frequency and Structure
- **Monthly brief:** 1-page summary — headline return, benchmark comparison, major attribution drivers, any notable events.
- **Quarterly detailed:** 3-5 pages — full return table, attribution, risk dashboard, goal progress, market commentary, and outlook.
- **Annual comprehensive:** 8-15 pages — everything in the quarterly report plus year-in-review, tax reporting summary, planning updates, and IPS review.

### Plain Language Communication
The most important reporting skill is translating numbers into meaning.

- Do not just state "the portfolio returned 8.1% YTD." Add context: "The portfolio returned 8.1% YTD, outperforming its benchmark by 0.6 percentage points, driven primarily by strong stock selection in the technology sector."
- Explain whether performance is good or bad relative to expectations and the plan.
- Use analogies and comparisons the audience understands.
- Define technical terms on first use or include a glossary.
- Lead with the conclusion, then provide supporting detail for those who want to dig deeper.

## Worked Examples

### Example 1: Quarterly Performance Report Summary
**Given:** A balanced portfolio (60% equity / 40% fixed income) returned 3.2% in Q3 (benchmark: 2.8%). YTD the portfolio returned 8.1% vs 7.5% for the benchmark. The portfolio Sharpe ratio is 0.85 over the trailing 12 months. Equity selection in technology (+0.3%) and an underweight in energy (-0.1%) were the main attribution drivers.

**Analysis:**

**Headline:** The portfolio outperformed its benchmark by 0.4 percentage points in Q3 and 0.6 percentage points YTD, driven by strong stock selection in technology.

**Return summary table:**

| Period | Portfolio | Benchmark | Active Return |
|--------|-----------|-----------|---------------|
| Q3     | +3.2%     | +2.8%     | +0.4%         |
| YTD    | +8.1%     | +7.5%     | +0.6%         |

**Attribution highlights:**
- Technology stock selection contributed +0.3% — the largest single driver of outperformance.
- Underweight energy allocation detracted -0.1% as energy prices rallied in the quarter.
- Net active return of +0.4% demonstrates disciplined bottom-up security selection.

**Risk context:**
- Trailing 12-month Sharpe ratio of 0.85 indicates the portfolio is generating meaningful risk-adjusted excess return.
- Portfolio volatility remains in line with the benchmark, so outperformance is not coming from taking additional risk.

**Plain-language summary for the client:** "Your portfolio gained 3.2% this quarter, beating the benchmark by about half a percent. Year-to-date, you are ahead of the benchmark by a similar margin. The main driver was our technology stock picks, which outperformed the broader tech sector. We remain on track relative to your long-term financial plan."

### Example 2: Goal Progress — Retirement Funding
**Given:** A client has a retirement goal of $2,000,000 in today's dollars. Current portfolio value is $850,000. Time horizon is 15 years. Current annual contribution is $30,000 (increasing 3% per year). Portfolio expected return is 7% nominal, expected volatility is 12%. Inflation assumption is 2.5%.

**Analysis:**

**Current status:**
- Goal: $2,000,000 (in today's dollars)
- Current assets: $850,000
- Funded ratio: 42.5%
- Time remaining: 15 years

**Projection (deterministic):**
- Future value of current assets at 4.5% real return over 15 years: $850,000 x (1.045)^15 = approximately $1,636,000
- Future value of contributions ($30,000/yr escalating 3%/yr) at 4.5% real: approximately $620,000
- Projected total (real): approximately $2,256,000
- Deterministic assessment: **On track** — projected to exceed goal by ~$256,000

**Projection (Monte Carlo, 10,000 simulations):**
- Median outcome: $2,180,000
- 25th percentile: $1,650,000
- 10th percentile: $1,320,000
- Probability of reaching $2,000,000 goal: **68%**

**Interpretation:** While the deterministic projection shows the client is on track, the Monte Carlo analysis reveals a 68% probability of success — reasonable but not highly confident. The gap between the deterministic and probabilistic views is driven by sequence-of-returns risk and volatility drag.

**Recommendations to improve probability of success:**
- Increase annual contributions by $5,000 (raises probability to ~78%).
- Consider modest reduction in spending goal or flexible retirement date.
- Maintain current allocation — reducing risk at this stage would lower expected return and reduce success probability.

**Client-facing summary:** "You have $850,000 saved toward your $2,000,000 retirement goal, which is 42.5% of the way there with 15 years to go. Based on our projections, you have roughly a 68% chance of reaching your goal with your current savings plan. This is a reasonable position, but we can improve your odds by increasing your annual contribution or building in some flexibility on your retirement date."

## Common Pitfalls
- Cherry-picking favorable time periods to present performance in the best light. Always show standard periods and since-inception returns.
- Not showing risk alongside returns. A 15% return with 30% volatility is a very different story than 15% with 10% volatility.
- Using inappropriate benchmarks to flatter performance. Comparing a growth equity fund to a value index during growth-favoring markets is dishonest.
- Too much jargon for non-technical audiences. Sharpe ratios and tracking error mean nothing to most clients without explanation.
- Not providing context for numbers. Is 8% good or bad? It depends on the benchmark, the risk taken, the market environment, and the goal.
- Showing short-period returns annualized. A 5% return in one month is not "60% annualized" — this is misleading and should never be presented.
- Presenting only time-weighted returns when the client's cash flow timing significantly impacted their actual experience. Show money-weighted returns alongside TWR when there are large or ill-timed flows.
- Survivorship bias in composite reporting: excluding terminated accounts or poor-performing strategies from historical track records.
- Ignoring taxes: for taxable investors, after-tax returns are what actually matters.

## Cross-References
- **statistics-fundamentals** (core plugin, Layer 0): return distributions, confidence intervals for projections
- **time-value-of-money** (core plugin, Layer 0): future value projections, annualization math
- **performance-metrics** (wealth-management plugin, Layer 1a): Sharpe, Sortino, Information Ratio calculation details
- **historical-risk** (wealth-management plugin, Layer 1a): volatility, drawdown, VaR computation for risk dashboards
- **asset-allocation** (wealth-management plugin, Layer 4): benchmark construction for multi-asset portfolios
- **quantitative-valuation** (wealth-management plugin, Layer 3): forward-looking return assumptions for goal projections
- **finance-psychology** (wealth-management plugin, Layer 7): framing effects in how performance is presented to clients
- **client-review-prep** (advisory-practice plugin, Layer 10): performance data is assembled into the client review meeting package

## Reference Implementation
See `scripts/performance_reporting.py` for computational helpers.
