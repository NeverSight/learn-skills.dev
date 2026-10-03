---
name: predictive-burn-rate
description: When the user wants to predict future cash consumption and "Runway" using time-series AI models. Also use when the user mentions "startup runway," "predicting cash out," "future burn rate," "Prophet for finance," "LSTM cash forecasting," or "when will we run out of money."
metadata:
  version: 1.0.0
---

# Predictive Burn Rate

You are a Startup Data Scientist. Your goal is to use time-series forecasting to predict exactly when a company will require more capital, accounting for seasonality and growth trends.

## Initial Assessment

1. **Cash Flow Data**
   - Do we have monthly net cash flow (Net Burn) for at least 12-24 months?
   - What are the major "lumpy" expenses? (e.g., Annual software renewals, bi-annual bonuses).

2. **Growth Assumptions**
   - Are headcount and marketing spend scaling linearly or exponentially?
   - Is there a "Target Zero" date for profitability?

---

## Predictive Framework

### Technical Limitation
Linear extrapolations (Actuals / Average Burn) are often wrong because they ignore seasonality. This skill uses **Prophet** or **ARIMA** logic for more accurate modeling.

### Priority Order
1. **Decomposition** (Separating Trend, Seasonality, and Noise).
2. **Growth Modeling** (Adjusting the burn rate based on headcount growth).
3. **Runway Calculation** (Predicting the month the cash balance hits zero).
4. **Buffer Analysis** (Identifying the "Safety Zone" for fundraising).

---

## Technical Predictive Steps

### 1. Time-Series Decomposition
- Identify if the burn rate is increasing due to a long-term trend or a one-time seasonal spike (e.g., Q4 marketing push).

### 2. Facebook Prophet Integration
- Use the `Prophet` library to handle missing data and outliers while modeling complex seasonality (holiday effects).

### 3. Scenario Probability
- Instead of one date, provide a probability distribution: "70% chance of cash out in Oct, 20% in Nov, 10% in Dec."

---

## Output Format

### Runway Forecast Report

**The Prediction**
- **Estimated Cash Out Date**: The "Zero Date."
- **Current Runway**: Expressed in months.
- **Trend Rating**: (e.g., "Accelerating Burn," "Stabilizing").

**AI Visuals (Description)**
- Confidence intervals for the next 12 months.
- Breakdown of burn drivers (fixed vs. variable).

**Actionable Insight**
- "Fundraising Trigger": The date you must start your next round to avoid a cash crunch.

---

## Scripts
- [calculate.py](./scripts/calculate.py): Runway, growth-adjusted burn, and collections curve functions. Run with `python3 scripts/calculate.py` to self-test; import the functions for actual computations.

---

## References
- [Time Series Basics](./references/time-series-forecasting.md): ARIMA vs. Prophet.
- [Startup Runway Metrics](./references/startup-metrics.md): How VCs look at burn.

---

## Related Skills
- **budget-forecast**: For the manual planning of the burn rate.
- **treasury-management**: For managing the cash reserves predicted here.
- **investment-analysis**: For valuing the startup based on its burn and growth.
