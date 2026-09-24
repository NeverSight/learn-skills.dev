---
name: transfer-pricing
description: >
  Transfer pricing policy design, documentation, and defense aligned with OECD
  Guidelines and the arm's length principle. USE THIS SKILL when the user asks
  about transfer pricing, intercompany pricing, TP documentation, arm's length
  pricing, intercompany transactions, benchmarking studies, comparability
  analysis, functional analysis, FAR analysis, advance pricing agreements,
  master file, local file, Country-by-Country Reporting, management fees,
  intercompany loans, cost sharing arrangements, or MAP/arbitration for double
  taxation disputes.
---

# Transfer Pricing

## Required Inputs

- **Group Structure**: Entities involved, jurisdictions, and ownership chain.
- **Intercompany Transactions**: Types (goods, services, IP, financing), volumes, and current pricing.
- **Functional Profile**: Functions performed, assets employed, and risks assumed by each entity (FAR profile).
- **Industry Context**: Sector, competitive dynamics, and market conditions affecting pricing.
- **Jurisdictions**: Countries involved and their specific TP rules and documentation thresholds.
- **Financial Data**: Segmented P&L by entity, intercompany balances, and consolidated financials.
- **Existing TP Documentation**: Current policies, benchmarking studies, intercompany agreements.
- **Dispute History**: Any ongoing or past TP audits, adjustments, or competent authority proceedings.

## Execution Steps

### 1. Intercompany Transaction Identification and Categorization

Map all intercompany transactions across the group:

| Transaction # | Description | From Entity | To Entity | Type | Annual Value ($M) | Current Pricing Method | Agreement in Place? |
|---|---|---|---|---|---|---|---|
| T-001 | [e.g., Finished goods] | [Entity A] | [Entity B] | Tangible goods | $___M | [Method] | Yes/No |
| T-002 | [e.g., R&D services] | [Entity C] | [Entity D] | Services | $___M | [Method] | Yes/No |
| T-003 | [e.g., Trademark license] | [Entity E] | [Entity F] | IP / Royalty | $___M | [Method] | Yes/No |
| T-004 | [e.g., Intercompany loan] | [Entity G] | [Entity H] | Financing | $___M | [Method] | Yes/No |

**Transaction categories**:
- **Tangible goods**: Raw materials, components, finished goods, commodities
- **Services**: Management, administrative, technical, R&D, contract manufacturing, contract R&D
- **Intangible property**: Licenses (patents, trademarks, know-how, software), cost sharing payments
- **Financial transactions**: Loans, guarantees, cash pooling, insurance, factoring

### 2. Functional Analysis (FAR Analysis)

For each entity involved in intercompany transactions, document the FAR profile:

| Factor | Entity A (e.g., Principal) | Entity B (e.g., Limited-Risk Distributor) | Entity C (e.g., Contract Manufacturer) |
|---|---|---|---|
| **FUNCTIONS** | | | |
| Strategic management | Yes — key decisions | No | No |
| R&D / product development | Yes — directs and funds | No | No — follows specs |
| Manufacturing | No | No | Yes — per contract |
| Procurement | Yes — sources key inputs | No | Limited — local inputs |
| Marketing & sales strategy | Yes — global strategy | Limited — local execution | No |
| Distribution | No | Yes — local market | No |
| Quality control | Yes — sets standards | No | Yes — executes standards |
| **ASSETS** | | | |
| IP (patents, trademarks) | Owns all material IP | None | None |
| Inventory | Limited | Yes — finished goods | Yes — WIP and raw materials |
| Fixed assets (plant) | No | Warehouse | Manufacturing plant |
| Customer relationships | Owns globally | Local relationships | None |
| **RISKS** | | | |
| Market risk | Yes — bears demand risk | Limited — guaranteed margin | No — guaranteed cost-plus |
| Inventory risk | Limited | Yes — local stock | Limited — consignment |
| Credit risk | Yes — group-level | Yes — local AR | No |
| Product liability | Yes — ultimate | No | No |
| Foreign exchange risk | Yes — manages centrally | Limited | No |
| R&D / obsolescence risk | Yes — bears fully | No | No |

**Entity characterization** (derived from FAR analysis):

| Entity | Characterization | Expected Return Profile |
|---|---|---|
| Entity A | Entrepreneur / Principal | Residual profit (volatile; upside and downside) |
| Entity B | Limited-risk distributor | Stable, routine margin on sales (e.g., 2-5% operating margin) |
| Entity C | Contract manufacturer | Stable, routine return on costs (e.g., 5-10% cost-plus markup) |
| Entity D | Contract R&D provider | Cost-plus markup (e.g., 8-15% on total costs) |
| Entity E | Commissionnaire agent | Commission on sales (e.g., 3-7% of net sales) |

### 3. Transfer Pricing Method Selection

Apply the OECD Guidelines hierarchy and the following decision tree:

```
Is there a directly comparable uncontrolled transaction (identical product/service)?
  |
  YES --> Use CUP (Comparable Uncontrolled Price)
  |
  NO --> Is the tested party a distributor/reseller?
           |
           YES --> Is gross margin data available for comparables?
                    |
                    YES --> Use Resale Price Method
                    NO  --> Use TNMM (with operating margin as PLI)
           |
           NO --> Is the tested party a manufacturer/service provider?
                   |
                   YES --> Is cost data reliable and comparable?
                            |
                            YES --> Use Cost Plus Method
                            NO  --> Use TNMM (with operating margin or Berry ratio as PLI)
                   |
                   NO --> Are both parties making unique, valuable contributions?
                           |
                           YES --> Use Profit Split Method
                           NO  --> Use TNMM
```

**Method comparison for each transaction**:

| Transaction | CUP | Resale Price | Cost Plus | TNMM | Profit Split | **Selected** |
|---|---|---|---|---|---|---|
| T-001: Goods | [Feasible? Why/why not] | | | | | [Method + rationale] |
| T-002: Services | | | | | | |
| T-003: IP License | | | | | | |
| T-004: Loan | | | | | | |

**Methods defined** (per OECD Guidelines Chapter II):

| Method | Description | Profit Level Indicator (PLI) | Best For |
|---|---|---|---|
| **CUP** | Compares price in controlled transaction to price in comparable uncontrolled transaction | Price per unit | Commodities, quoted financial instruments, identical goods |
| **Resale Price** | Starts from resale price to third party; subtracts appropriate gross margin | Gross margin % | Distributors who add limited value |
| **Cost Plus** | Starts from costs incurred by supplier; adds appropriate markup | Cost-plus markup % | Contract manufacturers, routine service providers |
| **TNMM** | Examines net profit relative to an appropriate base (costs, sales, assets) | Operating margin, Berry ratio, return on assets | Most common; one-sided method for routine entities |
| **Profit Split** | Divides combined profit based on relative value of each party's contributions | Contribution analysis or residual analysis | Highly integrated operations; unique IP on both sides |

### 4. Comparability Analysis and Benchmarking

#### 4a. Search Strategy

| Step | Action | Detail |
|---|---|---|
| 1. Database selection | Choose benchmark database | Bureau van Dijk (Orbis/TP Catalyst), S&P Capital IQ, Bloomberg, or jurisdiction-specific databases |
| 2. Geographic filter | Match to tested party region | Same country preferred; expand to region if insufficient results |
| 3. Industry filter | Apply SIC/NACE codes | Primary activity codes matching the tested party's function |
| 4. Quantitative screens | Apply financial filters | Revenue > $___M; positive operating income in majority of years; independence (no >25% single shareholder) |
| 5. Qualitative review | Manual review of remaining companies | Reject companies with non-comparable functions, assets, risks, or extraordinary events |
| 6. Comparability adjustments | Adjust for differences | Working capital adjustment, accounting differences, capacity utilization |

#### 4b. Benchmarking Results Template

| # | Company Name | Country | Description | Operating Margin Y1 | Y2 | Y3 | Weighted Avg |
|---|---|---|---|---|---|---|---|
| 1 | [Comparable 1] | [Country] | [Brief description] | ___% | ___% | ___% | ___% |
| 2 | [Comparable 2] | | | | | | |
| ... | | | | | | | |
| | **Interquartile Range** | | | | | | |
| | 25th percentile | | | | | | ___% |
| | Median | | | | | | ___% |
| | 75th percentile | | | | | | ___% |
| | **Tested party result** | | | | | | ___% |

**Arm's length range**: The interquartile range (25th to 75th percentile) of the benchmark set is the arm's length range. If the tested party's result falls within this range, no adjustment is required. If outside, adjust to the median.

#### 4c. Working Capital Adjustment

Adjust comparables for differences in working capital intensity:

```
Adjusted Operating Margin = Unadjusted OM + (Working Capital Adjustment Factor x Risk-Free Rate)

Where Working Capital Adjustment Factor =
  (Tested Party WC/Revenue - Comparable WC/Revenue)
  WC = Trade Receivables + Inventory - Trade Payables
```

### 5. Intercompany Agreement Framework

Each intercompany transaction must be governed by a written agreement. Key terms by transaction type:

| Agreement Element | Goods | Services | IP License | Financing |
|---|---|---|---|---|
| Parties and relationship | Required | Required | Required | Required |
| Scope and description | Products, volumes, quality specs | Service description, deliverables, SLAs | Licensed IP, field of use, territory | Loan amount, purpose |
| Pricing mechanism | CUP / resale minus / cost plus | Cost plus markup / fixed fee / % of benefit | Royalty rate (% of net sales) | Interest rate (fixed/floating + spread) |
| Price adjustment clause | Annual review; market price adjustment | Annual benchmarking review | Periodic royalty rate review | Rate reset mechanism |
| Payment terms | Net 30-60 days | Monthly/quarterly in arrears | Quarterly royalty payments | Interest payment schedule; principal repayment |
| IP ownership | Background IP retained by each party | Work product ownership | Licensor retains ownership | N/A |
| Term and termination | Annual, auto-renewing | 1-3 years with renewal | Matches IP useful life | Loan maturity date |
| Indemnification | Product liability allocation | Service quality guarantee | IP infringement indemnity | Lender protections |
| Governing law | Licensor/principal jurisdiction | Service provider jurisdiction | IP owner jurisdiction | Lender jurisdiction |
| Dispute resolution | Mediation then arbitration | Mediation then arbitration | Mediation then arbitration | Mediation then arbitration |

### 6. Documentation Requirements by Jurisdiction

#### 6a. OECD Three-Tiered Framework

| Document | Content | Filing | Threshold (Typical) |
|---|---|---|---|
| **Master File** | Group overview: org structure, business description, intangibles, intercompany financial activities, financial and tax positions | Filed with local tax authority or available on request | Revenue > EUR 750M (CbCR) or per local rules |
| **Local File** | Tested party analysis: local entity information, controlled transactions, TP methods, comparability analysis, financial data | Filed locally or available on request | Varies by jurisdiction (often > EUR 1-5M intercompany) |
| **Country-by-Country Report (CbCR)** | Revenue, profit, tax paid, tax accrued, employees, tangible assets, stated capital, retained earnings — per jurisdiction | Filed by ultimate parent entity; exchanged via treaty | Consolidated group revenue > EUR 750M |

#### 6b. Jurisdiction-Specific Requirements

| Jurisdiction | Master File | Local File | CbCR | Filing Deadline | Penalties for Non-Compliance |
|---|---|---|---|---|---|
| United States | Not required (but helpful) | Contemporaneous documentation required | Yes (Form 8975) | Due with tax return | 20-40% penalty on underpayment; no penalty if contemporaneous docs maintained |
| United Kingdom | Required (if threshold met) | Required | Yes | 12 months after period end | Penalties: GBP 3,000 per local file failure + tax-geared penalties |
| Germany | Required | Required | Yes | Available on 60-day request | 5-10% surcharge on TP adjustment if no documentation |
| Australia | Required | Required | Yes | Due with tax return (CbCR: 12 months) | AUD 525,000 per statement; doubled penalties if no docs |
| India | Required | Required | Yes | Due date of tax return | 2% of transaction value per doc failure |
| Singapore | Recommended | Required (if threshold met) | Yes (if threshold met) | Contemporaneous | 5% surcharge on adjustments |
| [Add as needed] | | | | | |

### 7. Advance Pricing Agreement (APA) Evaluation

Evaluate whether to pursue an APA:

| Factor | Assessment | Favorable for APA? |
|---|---|---|
| Transaction value | $___M annually | Yes if >$10M/year (justifies cost) |
| Audit risk | Low/Med/High | Yes if high audit risk |
| Double taxation exposure | $___M potential | Yes if significant |
| Complexity of method | [Simple/Complex] | Yes if complex method requires certainty |
| Number of jurisdictions | ___ | Bilateral/multilateral APA if multiple |
| Cost of APA process | $___K (advisory fees + government fees) | Compare to cost of controversy |
| Timeline | 2-4 years (bilateral) | Consider if timing acceptable |

**APA types**:
- **Unilateral**: Agreement with one tax authority. Fast but does not prevent double taxation.
- **Bilateral**: Agreement between two tax authorities under treaty MAP. Eliminates double taxation.
- **Multilateral**: Three or more tax authorities. Complex but comprehensive.

**Recommendation**: [Pursue / Do not pursue APA] — with rationale.

### 8. Transfer Pricing Dispute Resolution

| Mechanism | Description | Timeline | Cost | When to Use |
|---|---|---|---|---|
| **Self-adjustment** | Tested party adjusts pricing to fall within arm's length range | Immediate | Minimal | Result is marginally outside range |
| **Competent authority (MAP)** | Treaty-based process; two tax authorities negotiate | 2-3 years average (OECD target: 24 months) | Advisory fees | Assessment in one country creates double taxation |
| **Arbitration** | Binding resolution if MAP fails (under MLI or bilateral treaty) | Typically 2 years after MAP deadline | Higher advisory fees | MAP stalled; available under treaty/MLI |
| **Domestic appeal/litigation** | Challenge adjustment in local courts | 3-7 years | Highest cost | Fundamental disagreement on method or facts |
| **Corresponding adjustment** | Request other jurisdiction to adjust accordingly | Varies | Moderate | Accepted adjustment in one jurisdiction |

### 9. Management Fee Allocation Methodology

| Allocation Approach | Description | Best For | OECD Guidance |
|---|---|---|---|
| **Direct charge** | Specific service directly identified and charged to recipient | Services clearly benefiting one entity | Preferred by OECD (most accurate) |
| **Indirect allocation** | Pool of costs allocated via allocation keys | Shared services benefiting multiple entities | Acceptable if direct charge not feasible |

**Allocation key options** (for indirect allocation):

| Allocation Key | Basis | Best For |
|---|---|---|
| Revenue | Proportional to entity revenue | Revenue-driven services (marketing, sales support) |
| Headcount | Number of employees per entity | HR, IT support, training |
| Assets | Total assets or specific asset class | Asset-intensive services (treasury, insurance) |
| Transactions | Number of transactions processed | Transaction processing, accounting |
| Composite | Weighted combination of above | Multi-function shared services |

**Benefit test**: Every management fee must pass the benefit test — would an independent enterprise have been willing to pay for this service or perform it in-house? Shareholder activities (e.g., consolidation reporting, investor relations) are NOT chargeable.

**Markup determination**: Low-value-adding services may qualify for simplified 5% cost-plus markup under OECD simplified approach (Chapter VII, Section D.1).

### 10. Intercompany Financing

#### 10a. Interest Rate Benchmarking

| Factor | Analysis |
|---|---|
| Borrower credit rating | Stand-alone credit rating (not group rating) using rating agency methodology or synthetic rating tools |
| Loan terms | Amount, tenor, currency, security, covenants |
| Comparable data sources | Bloomberg BVAL, loan syndication databases, bond yields for comparable-rated issuers |
| Arm's length interest rate | Base rate (e.g., SOFR, EURIBOR) + credit spread based on borrower rating |
| Range | [Lower bound]% to [Upper bound]% |

#### 10b. Guarantee Fee Analysis

| Scenario | Analysis |
|---|---|
| Explicit guarantee | Parent formally guarantees subsidiary debt; fee = credit spread differential x guaranteed amount |
| Implicit support | Market recognizes group membership; quantify implicit support benefit |
| Pricing approach | Yield approach (spread differential) or CDS-based pricing |
| Typical range | 0.25% - 2.00% of guaranteed amount annually |

#### 10c. Cash Pooling

| Element | Arm's Length Consideration |
|---|---|
| Pool leader compensation | Spread between deposit and borrowing rates; or fixed fee |
| Participant deposit rate | Above bank deposit rate (participants contribute liquidity) |
| Participant borrowing rate | Below external borrowing rate (benefit of pool) |
| Credit balances | Allocate netting benefit among participants |
| Documentation | Master cash pooling agreement with all participants |

### 11. Compliance Calendar and Risk Monitoring

| Activity | Frequency | Deadline | Responsible |
|---|---|---|---|
| Update benchmarking studies | Every 3 years (annual financial data update) | Q1 each year | TP team / external advisor |
| Prepare local file documentation | Annual | Tax return filing date per jurisdiction | Local tax / TP team |
| Prepare master file | Annual | Tax return filing date of parent entity | Group TP team |
| CbCR filing | Annual | 12 months after fiscal year end | Parent entity tax team |
| Intercompany agreement review | Annual | Q4 each year | Legal / TP team |
| Year-end TP adjustments | Annual (if needed) | Before books close | Finance / TP team |
| Functional analysis update | When business changes occur | Within 90 days of change | TP team |
| APA renewal | Per APA term (typically 3-5 years) | 6-12 months before expiry | External advisor |
| TP risk assessment | Annual | Q1 each year | TP team / tax director |

**Risk monitoring dashboard**:

| Risk Indicator | Green | Yellow | Red |
|---|---|---|---|
| Tested party operating margin vs. benchmark | Within IQR | Between IQR and full range | Outside full range |
| Documentation completeness | All local files current | 1-2 jurisdictions pending | >2 jurisdictions without docs |
| Intercompany agreements | All signed and current | Some need updating | Missing agreements |
| CbCR consistency | No anomalies | Minor misalignments | Profit/substance mismatch |
| Year-end adjustments | None needed | Adjustments <5% | Adjustments >5% of transaction value |

## Output Template

```markdown
## Transfer Pricing Analysis: [Client / Group Name]

**Date**: [Date] | **Prepared by**: Tax Advisory Practice
**Period covered**: FY [Year]
**Jurisdictions**: [List of relevant jurisdictions]

> This analysis provides a strategic framework for tax planning. It does not
> constitute tax advice or a legal opinion. Implementation requires review by
> qualified tax counsel in each relevant jurisdiction. Tax laws change
> frequently; all analysis is based on current rules as of the date provided.

---

### 1. Group Overview and Intercompany Transaction Map

[Group structure diagram showing entities and intercompany flows]

**Intercompany transactions summary**:
| # | Description | Parties | Type | Annual Value | Method |
|---|---|---|---|---|---|
| T-001 | [Description] | [From] -> [To] | [Type] | $___M | [Method] |

### 2. Functional Analysis

| Function/Asset/Risk | [Entity A: Role] | [Entity B: Role] | [Entity C: Role] |
|---|---|---|---|
| [Key function 1] | | | |
| [Key function 2] | | | |
| [Key asset 1] | | | |
| [Key risk 1] | | | |

**Entity characterization**: [Entrepreneur / Limited-risk distributor / Contract manufacturer / etc.]

### 3. Transfer Pricing Method Selection

| Transaction | Selected Method | PLI | Rationale |
|---|---|---|---|
| T-001 | [Method] | [PLI] | [Why this method is most reliable] |

### 4. Benchmarking Results

| Transaction | Tested Party | PLI Result | Arm's Length Range (IQR) | In Range? |
|---|---|---|---|---|
| T-001 | [Entity] | ___% | ___% - ___% (median: ___%) | Yes/No |

### 5. Intercompany Agreements

| Transaction | Agreement Status | Key Terms | Action Needed |
|---|---|---|---|
| T-001 | [In place / Draft / Missing] | [Summary] | [None / Update / Draft new] |

### 6. Documentation Compliance

| Jurisdiction | Master File | Local File | CbCR | Status |
|---|---|---|---|---|
| [Country] | [Required/Not] | [Required/Not] | [Required/Not] | [Compliant / Gap] |

### 7. APA and Dispute Resolution Recommendations

[Assessment of whether APA is recommended; any ongoing dispute resolution needs]

### 8. Management Fee Analysis

| Service | Allocation Method | Allocation Key | Markup | Passes Benefit Test? |
|---|---|---|---|---|
| [Service] | [Direct/Indirect] | [Key] | ___% | Yes/No |

### 9. Intercompany Financing

| Loan/Facility | Amount | Rate | Arm's Length Range | Compliant? |
|---|---|---|---|---|
| [Loan] | $___M | ___% | ___% - ___% | Yes/No |

### 10. Risk Assessment

| Risk | Level | Financial Exposure | Recommended Action |
|---|---|---|---|
| Pricing outside arm's length range | [Low/Med/High] | $___M potential adjustment | [Action] |
| Documentation gaps | [Low/Med/High] | [Penalty exposure] | [Action] |
| Substance mismatch | [Low/Med/High] | [Recharacterization risk] | [Action] |
| CbCR inconsistencies | [Low/Med/High] | [Audit trigger] | [Action] |

### 11. Compliance Calendar

[Customized calendar with jurisdiction-specific deadlines]

### Key Recommendations

1. [Priority recommendation with rationale and estimated risk reduction]
2. [Second priority recommendation]
3. [Third priority recommendation]

### Cross-References
- `tax-structure-advisory` skill for entity restructuring implications
- `ip-strategy` skill for IP licensing and DEMPE analysis
- `tax-incentive-analysis` skill for incentive-related TP implications
- `valuation` skill for intangible asset valuation in IP transfers
```

## Quality Checks

- [ ] All analysis is clearly labeled as an analytical framework, not legal advice; disclaimer is included.
- [ ] Every intercompany transaction is identified, categorized, and assigned a TP method.
- [ ] FAR analysis is completed for each entity involved in intercompany transactions.
- [ ] Transfer pricing method selection follows the OECD Guidelines decision hierarchy with documented rationale.
- [ ] Benchmarking study uses a documented, replicable search strategy with named databases.
- [ ] Arm's length range is the interquartile range; tested party result is compared to this range.
- [ ] Working capital adjustments are applied to comparables where material differences exist.
- [ ] Intercompany agreements are reviewed or drafted for every transaction with all required terms.
- [ ] Documentation compliance is mapped for every jurisdiction with specific deadlines.
- [ ] Management fee analysis includes benefit test assessment; shareholder activities excluded from charges.
- [ ] Intercompany financing uses borrower-specific (not group) credit rating for interest rate benchmarking.
- [ ] APA evaluation is completed with cost-benefit analysis when transaction value exceeds $10M annually.
- [ ] Anti-avoidance risk assessment covers pricing risk, documentation risk, substance risk, and CbCR consistency.
- [ ] Compliance calendar includes all jurisdiction-specific filing deadlines and monitoring activities.
- [ ] Cross-references to related skills (tax-structure-advisory, ip-strategy, valuation) are included.
