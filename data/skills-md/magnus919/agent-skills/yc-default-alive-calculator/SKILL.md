---
name: yc-default-alive-calculator
description: >-
  Evaluate startup runway, burn, revenue, and profitability trajectory using the Default
  Alive / Default Dead framework. Do not use this skill for weekly growth experiments or
  operating growth decisions; use `yc-weekly-growth-compass` for those decisions.
license: MIT
compatibility: Python 3.9+ with standard library only (no external dependencies).
  The default-alive.py script uses only math, json, and sys.
metadata:
  spec-version: '1.0'
  tags: startup-finance, runway-analysis, ycombinator, paul-graham, fundraising, financial-modeling,
    default-alive, burn-rate, startup-metrics
  sources: https://paulgraham.com/aord.html, https://paulgraham.com/die.html, https://www.ycombinator.com/about
  skills: yc-weekly-growth-compass
  requires-toolsets: terminal
---

# Default Alive / Default Dead Calculator

A startup is "default alive" if its current revenue trajectory will reach profitability before it runs out of cash — without additional funding. It is "default dead" if it will run out of money first. This is the single most important financial diagnostic Paul Graham developed at Y Combinator.

**This is not a fundraising model.** It's a reality check. The answer determines whether fundraising is optional or existential.

## When to Load

| Trigger | Example |
|---------|---------|
| "Am I default alive?" | Founder asking about runway |
| "How much runway do I have?" | Financial planning |
| "Should I raise money?" | Strategic decision |
| "What's my burn multiple?" | Investor-ready metrics |
| "How long until we break even?" | Trajectory check |
| "Default alive/dead analysis" | Explicit framework request |

## When Not to Use

- **Detailed financial planning.** This is a diagnostic, not a budget. It projects one growth curve with fixed assumptions; it does not model hiring plans, contract timing, seasonality, or capital expenditures. Use a proper financial model for those.
- **Fundraising valuation.** The verdict tells you whether raising money is existential; it does not compute a valuation, cap table, or round size.
- **Cost structures the default assumptions don't describe.** The model splits burn into fixed and variable components (default 70/30). Hardware, R&D, or manufacturing companies with very different cost structures will get a misleading projection.
- **Unknown or unstable growth.** The model assumes a steady monthly growth rate with a small decay. A company in launch mode or product-market-fit search does not produce a meaningful projection.
- **As the only input to a board decision.** Treat the verdict as a conversation starter with your CFO or accountant, not as financial advice.

## How to Use

### Quick Answer (No Script)

For a quick check without running the calculator, use the simplified heuristic:

```
Burn Multiple = Net Burn / Net New ARR
```

| Burn Multiple | Signal |
|--------------|--------|
| < 1x | Default Alive — growing efficiently |
| 1x–2x | Healthy — capital-efficient growth |
| 2x–3x | Warning — burning faster than growing |
| 3x+ | Default Dead — cash crisis without funding |

### Full Analysis (Script)

Run the CLI calculator for a precise analysis:

```bash
python scripts/default-alive.py \
  --monthly-revenue 50000 \
  --monthly-burn 120000 \
  --cash-on-hand 800000 \
  --monthly-growth 8
```

Output shows: the verdict, burn multiple (net burn ÷ net new ARR), burn-to-revenue ratio (net burn ÷ MRR), projected cash-out month, months to breakeven, cash gap coverage at current spend, the model's assumptions, and the key levers available.

#### Required inputs

| Flag | Description | Example |
|------|-------------|---------|
| `--monthly-revenue` | Current monthly recurring revenue (MRR) | `50000` |
| `--monthly-burn` | Total monthly operating expenses | `120000` |
| `--cash-on-hand` | Cash remaining in bank account | `800000` |
| `--monthly-growth` | Month-over-month revenue growth rate (%) | `8` |

#### Optional inputs

| Flag | Description | Example |
|------|-------------|---------|
| `--revenue-growth-deceleration` | Annual growth deceleration rate (%/month, default: 0.5) | `0.3` |
| `--json` | Machine-readable JSON output | |
| `--verbose` | Show detailed month-by-month projection | |

#### Output fields

| Field | Meaning |
|-------|---------|
| `projected_cashout_month` | Month cash runs out under the model; `null` if never within the 10-year projection |
| `burn_multiple` | Graham's burn multiple: net burn ÷ net new ARR |
| `burn_to_revenue_ratio` | Net burn ÷ MRR (secondary diagnostic, not Graham's metric) |
| `months_to_breakeven` | Months until revenue ≥ expenses (extrapolated) |
| `default_verdict` | `ALIVE`, `DEAD`, or `MARGINAL` |
| `revenue_at_breakeven` | Projected revenue when/if breakeven reached |
| `gap_to_breakeven` | Monthly shortfall remaining |
| `months_of_gap_remaining` | Static runway at current spend: cash ÷ monthly gap |
| `model_assumptions` | `fixed_burn_pct`, `variable_burn_ratio`, `growth_decay_pct`, `projection_cap_months`, `safety_buffer_months` |
| `levers` | What can change the outcome (increase price, cut costs, etc.) |

## Methodology

### The Core Calculation

The model projects month-by-month:

```
month_n_revenue = previous_revenue × (1 + growth_rate/100)
month_n_burn = fixed_burn + (variable_burn_ratio × month_n_revenue)
month_n_cash = previous_cash + month_n_revenue - month_n_burn
```

Growth rate decays over time (default: 0.5% per month) to model market saturation — startups don't grow at a constant rate forever.

### Default Alive Test

The startup is **Default Alive** if:
```
projected_revenue > projected_expenses
```
at some point *before* cumulative cash goes negative, *and* the crossover happens with at least 3 months of remaining runway (safety buffer).

It is **Default Dead** if cash runs out first.

It is **Marginal** if breakeven happens with less than 3 months of runway remaining — technically possible but dangerously tight.

### Burn Multiple

A metric Graham began tracking at YC to measure capital efficiency:

```
Burn Multiple = Net Burn / Net New ARR
```

Where:
- Net Burn = cash spent per month (total expenses minus revenue)
- Net New ARR = new annual recurring revenue added that month

A burn multiple below 1x means the company is generating more than it spends in new ARR terms — the strongest default-alive signal.

## Levers

When the verdict is DEAD or MARGINAL, evaluate these levers (in rough order of impact):

1. **Revenue growth** — 10% faster growth compounds dramatically over 18 months
2. **Cost reduction** — Every dollar cut extends runway by one dollar
3. **Pricing** — A 20% price increase with minimal churn impact is often the fastest lever
4. **Gross margin** — Reducing COGS improves unit economics without topline change
5. **Funding** — Default dead means fundraising is existential, not optional

## Examples

### YC Typical Profile (Default Dead under the model)

```bash
python3 scripts/default-alive.py \
  --monthly-revenue 30000 \
  --monthly-burn 75000 \
  --cash-on-hand 500000 \
  --monthly-growth 10
```

- Projected cash-out: month 14
- Burn multiple: 1.25x (net burn / net new ARR)
- Breakeven would require 22 months, after cash runs out
- Verdict: **DEAD** — needs faster growth, cost cuts, or funding

### Pre-Revenue Startup (Default Dead)

```bash
python3 scripts/default-alive.py \
  --monthly-revenue 0 \
  --monthly-burn 80000 \
  --cash-on-hand 400000 \
  --monthly-growth 0
```

- Projected cash-out: month 8 (the model burns only the fixed 70% of burn at zero revenue)
- Burn multiple: undefined (no revenue)
- Verdict: **DEAD** — fundraising is existential

### Capital-Efficient SaaS (Default Alive)

```bash
python3 scripts/default-alive.py \
  --monthly-revenue 150000 \
  --monthly-burn 180000 \
  --cash-on-hand 2000000 \
  --monthly-growth 7
```

- Projected cash-out: none within the 10-year projection
- Burn multiple: 0.24x (net burn / net new ARR)
- Verdict: **ALIVE**

## References

- `references/default-alive-framework.md` — Paul Graham's original framework with essay excerpts
- `references/yc-fundraising-context.md` — How default state drives fundraising strategy
- `yc-weekly-growth-compass` companion skill — For growth rate analysis
