---
name: valuation
description: >
  Business valuation using multiple methodologies: DCF, comparable companies,
  precedent transactions, and asset-based approaches. USE THIS SKILL when the
  user asks about company valuation, enterprise value, equity value, WACC,
  terminal value, valuation multiples, football field chart, valuation range,
  valuation bridge, control premium, minority discount, fair market value,
  intrinsic value, or "what is this business worth." Also trigger when asked
  to value a division, business unit, or target company for M&A purposes.
---

# Business Valuation

## Required Inputs

- **Subject Company**: Name, industry, and brief description of the business.
- **Purpose of Valuation**: M&A, fairness opinion, strategic planning, litigation, tax, or fundraising.
- **Financial Data**: Revenue, EBITDA, net income, total assets, debt, and cash (trailing twelve months + projections if available).
- **Standard of Value**: Fair market value, fair value, investment value, or liquidation value.
- **Control vs. Minority**: Whether the interest being valued is a controlling stake or minority position.

## Execution Steps

### 1. Preliminary Analysis

Assess the company before selecting methods:

| Factor | Assessment | Impact on Methodology |
|---|---|---|
| Profitability | Profitable / Pre-profit / Distressed | Pre-profit: weight revenue multiples; Distressed: weight asset-based |
| Growth stage | Early / Growth / Mature / Decline | Early: weight DCF with scenario analysis; Mature: weight comps |
| Asset intensity | Asset-light / Asset-heavy | Asset-heavy: include asset-based approach |
| Comparable availability | Strong peer set / Weak peer set | Weak: increase DCF weight, reduce comps weight |
| Transaction context | Control acquisition / Minority investment | Control: include precedent transactions + control premium |

### 2. DCF Valuation (Intrinsic Value)

#### 2a. WACC Derivation

Calculate the weighted average cost of capital:

| Component | Formula | Source |
|---|---|---|
| Cost of equity (Ke) | Risk-free rate + Beta x Equity risk premium + Size premium + Company-specific premium | CAPM model |
| Risk-free rate | 10-year or 20-year government bond yield | Treasury data |
| Equity risk premium | Historical market return minus risk-free rate (typically 5-7%) | Damodaran / Duff & Phelps |
| Beta | Unlevered peer beta, re-levered for target capital structure | Regression or peer-derived |
| Size premium | Small-cap premium if applicable (1-5%) | Duff & Phelps / Kroll |
| Cost of debt (Kd) | Yield on comparable-rated debt x (1 - tax rate) | Market or synthetic rating |
| WACC | Ke x (E / (D+E)) + Kd x (D / (D+E)) | Target capital structure weights |

State every assumption explicitly. Document risk-free rate date, ERP source, beta peers, and size premium category.

#### 2b. Free Cash Flow Projection

Project unlevered free cash flow (UFCF) for the explicit forecast period (typically 5-10 years):

```
UFCF = EBIT x (1 - Tax Rate) + D&A - CapEx - Change in Net Working Capital
```

Use the `financial-modeling` skill for detailed three-statement model construction when building projections from scratch.

#### 2c. Terminal Value (Two Methods)

**Perpetuity Growth Method:**
```
TV = UFCFn+1 / (WACC - g)
```
Where g = long-term sustainable growth rate (typically 2-3%, must not exceed nominal GDP growth).

**Exit Multiple Method:**
```
TV = EBITDAn x Exit Multiple
```
Where the exit multiple is derived from current trading multiples of mature peers.

**Sanity check**: Both methods should produce terminal values within 20% of each other. If not, re-examine assumptions. Terminal value typically represents 60-80% of total enterprise value for growth companies.

#### 2d. DCF Summary

| Item | Value | Notes |
|---|---|---|
| PV of projected FCFs | $___M | Sum of discounted UFCFs |
| PV of terminal value | $___M | Discounted TV |
| Enterprise value (DCF) | $___M | Sum of above |
| Terminal value as % of EV | ___% | Flag if >85% |

Produce a sensitivity table on **WACC (rows) x Terminal growth rate (columns)** with at least 5x5 grid, centered on the base case.

### 3. Comparable Companies Analysis (Market Value)

#### 3a. Peer Selection

Select 6-12 comparable public companies based on:
- Same or adjacent industry (SIC/NAICS codes)
- Similar size (revenue within 0.5x-2.0x if possible)
- Similar growth profile and margin structure
- Same geographic exposure

Document why each peer was included or excluded.

#### 3b. Trading Multiples

| Peer | EV/Revenue | EV/EBITDA | EV/EBIT | P/E | EV/FCF |
|---|---|---|---|---|---|
| Peer 1 | | | | | |
| Peer 2 | | | | | |
| ... | | | | | |
| **Mean** | | | | | |
| **Median** | | | | | |
| **25th percentile** | | | | | |
| **75th percentile** | | | | | |

Apply the most relevant multiples to the subject company's metrics. Use LTM and NTM metrics where available.

#### 3c. Comps-Implied Valuation

| Multiple Applied | Subject Metric | Multiple Range (25th-75th) | Implied EV Range |
|---|---|---|---|
| EV/Revenue | $___M revenue | ___x - ___x | $___M - $___M |
| EV/EBITDA | $___M EBITDA | ___x - ___x | $___M - $___M |

### 4. Precedent Transactions Analysis (Deal Value)

#### 4a. Transaction Selection

Identify 5-10 comparable M&A transactions from the last 3-5 years. Prioritize:
- Same industry and sub-sector
- Similar target size
- Similar deal rationale (strategic vs. financial buyer)
- Comparable market conditions at time of deal

#### 4b. Transaction Multiples

| Transaction | Date | Target | Acquirer | EV ($M) | EV/Revenue | EV/EBITDA |
|---|---|---|---|---|---|---|
| Deal 1 | | | | | | |
| Deal 2 | | | | | | |
| ... | | | | | | |
| **Median** | | | | | | |

Note: Precedent transaction multiples inherently include a control premium paid by acquirers.

### 5. Asset-Based Valuation (Liquidation / Floor Value)

Use when the company is asset-heavy, in distress, or as a floor valuation.

| Asset Category | Book Value | Fair Market Value Adjustment | FMV |
|---|---|---|---|
| Cash and equivalents | | 100% of book | |
| Accounts receivable | | 80-95% of book (net of doubtful) | |
| Inventory | | 50-90% of book (depends on type) | |
| PP&E | | Appraisal-based or 40-80% of book | |
| Intangibles (identifiable) | | Separate IP valuation if material | |
| Real estate | | Appraisal value | |
| **Total adjusted assets** | | | |
| Less: Total liabilities | | At face value + contingent liabilities | |
| **Net asset value** | | | |

### 6. Valuation Bridge: Enterprise Value to Equity Value

Regardless of methodology, bridge from EV to equity value:

| Item | Value | Notes |
|---|---|---|
| Enterprise value | $___M | From selected methodology |
| Less: Total debt | ($___M) | All interest-bearing obligations |
| Less: Minority interests | ($___M) | If consolidated |
| Less: Preferred equity | ($___M) | At liquidation preference |
| Less: Unfunded pension | ($___M) | If applicable |
| Less: Contingent liabilities | ($___M) | Litigation, earnouts owed |
| Plus: Cash and equivalents | $___M | Unrestricted cash |
| Plus: Non-operating assets | $___M | Excess real estate, investments |
| **Equity value** | $___M | |
| Diluted shares outstanding | ___M | Treasury stock method for options/warrants |
| **Equity value per share** | $___ | |

### 7. Control Premium / Minority Discount

| Adjustment | Typical Range | When to Apply |
|---|---|---|
| Control premium | 20-40% over trading price | Valuing a controlling interest using public comps (which reflect minority prices) |
| Minority discount | 15-30% from control value | Valuing a minority stake from a control-level valuation |
| Marketability discount (DLOM) | 15-35% | Valuing illiquid/private shares with no public market |

Apply adjustments only once and document the basis. Never double-count (e.g., precedent transactions already include control premiums).

### 8. Football Field Summary (Range by Method)

Produce a text-based range chart showing the valuation range from each methodology:

```
Valuation Range Summary ($M)
                        Low          Mid          High
DCF                 |=====[=========]=========|
                    $XXX         $XXX         $XXX

Comparable Cos.     |======[=======]====|
                    $XXX         $XXX    $XXX

Precedent Txns          |====[========]============|
                        $XXX     $XXX              $XXX

Asset-Based         |==|
                    $XX $XX

Selected Range             |====[====]====|
                           $XXX    $XXX   $XXX
```

### 9. Conclusion and Selected Value

State the concluded valuation range and point estimate:
- Weight assigned to each methodology with rationale
- Selected enterprise value range (low / mid / high)
- Selected equity value range
- Key assumptions that most influence the result
- Sensitivity to the top 2-3 variables

## Output Template

```markdown
## Valuation Analysis: [Company Name]

**Date**: [Date] | **Purpose**: [Purpose] | **Standard of Value**: [Standard]

### Executive Summary
[Company] is valued at an enterprise value of $[X]M to $[Y]M, with a midpoint
of $[Z]M, based on a weighted analysis of [methods used]. The equity value
range is $[A]M to $[B]M ($[C] to $[D] per share on [N]M diluted shares).

### WACC Derivation
| Component | Value | Source |
|---|---|---|
| Risk-free rate | X.X% | [source and date] |
| Equity risk premium | X.X% | [source] |
| Beta (re-levered) | X.XX | [peer set] |
| Size premium | X.X% | [category] |
| Cost of equity | X.X% | CAPM |
| Pre-tax cost of debt | X.X% | [basis] |
| Tax rate | X.X% | [statutory / effective] |
| Debt / total capital | X.X% | [target structure] |
| **WACC** | **X.X%** | |

### DCF Valuation
[Projected UFCF table, terminal value calculation, sensitivity table]

### Comparable Companies
[Peer table with multiples, implied valuation ranges]

### Precedent Transactions
[Transaction table with multiples, implied valuation ranges]

### Asset-Based Valuation
[Adjusted net asset value table — include only if applicable]

### Valuation Bridge
| Item | Value |
|---|---|
| Enterprise value (midpoint) | $___M |
| Less: Net debt | ($___M) |
| Less: Other EV adjustments | ($___M) |
| **Equity value** | **$___M** |
| Per share (diluted) | $___  |

### Football Field
[Text-based range chart showing all methods]

### Methodology Weighting
| Method | Weight | Rationale |
|---|---|---|
| DCF | X% | [why] |
| Comparable companies | X% | [why] |
| Precedent transactions | X% | [why] |
| Asset-based | X% | [why] |

### Key Sensitivities
[WACC x Growth sensitivity table]
[Multiple sensitivity table]

### Risks and Caveats
- [Key risk 1 and its impact on valuation]
- [Key risk 2 and its impact on valuation]
```

## Quality Checks

- [ ] At least two independent valuation methodologies applied and cross-referenced.
- [ ] WACC derivation fully documented with every input sourced and dated.
- [ ] Terminal value sanity-checked: perpetuity growth method and exit multiple method are within 20% of each other.
- [ ] Terminal value as percentage of total EV calculated and flagged if >85%.
- [ ] Valuation bridge from enterprise value to equity value explicitly shown with every line item.
- [ ] Control premium or minority discount applied exactly once (never double-counted with precedent transaction premiums).
- [ ] DLOM applied only to private/illiquid interests, not to publicly traded shares.
- [ ] Sensitivity analysis covers at least WACC and terminal value assumptions in a grid format.
- [ ] Football field chart shows the range from every method used, plus the selected range.
- [ ] Every peer in the comparable companies set has a stated inclusion rationale.
- [ ] Concluded value range is explicitly stated with methodology weights and rationale.
- [ ] Cross-reference: `financial-modeling` skill used or referenced for underlying projection model construction.
