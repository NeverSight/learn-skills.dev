---
name: deal-structuring
description: >
  M&A deal structuring and term sheet design. USE THIS SKILL when the user
  asks about deal structure, term sheet, purchase agreement terms, asset deal
  vs. stock deal, earnout, escrow, reps and warranties, indemnification,
  locked box, completion accounts, consideration mix, seller note, MAC clause,
  material adverse change, non-compete, conditions precedent, purchase price
  mechanism, closing conditions, merger agreement, or SPA terms. Also trigger
  when asked to draft or review M&A transaction terms.
---

# M&A Deal Structuring & Term Sheet Design

## Required Inputs

- **Transaction Overview**: Buyer, target, deal rationale, and indicative valuation range.
- **Buyer Type**: Strategic acquirer or financial sponsor (PE fund).
- **Target Entity Type**: C-corp, S-corp, LLC, partnership, or international entity.
- **Consideration Budget**: Available cash, appetite for stock issuance, and debt capacity.
- **Key Sensitivities**: Seller priorities (cash at close, tax efficiency, retention of upside) and buyer priorities (risk allocation, price protection, integration flexibility).

## Execution Steps

### 1. Deal Structure Selection

Choose the legal structure for the transaction. Each has materially different tax, liability, and operational consequences.

#### Structure Comparison Table

| Dimension | Asset Purchase | Stock Purchase | Statutory Merger |
|---|---|---|---|
| **What transfers** | Selected assets and liabilities | Entire legal entity (shares) | Target merges into buyer or sub |
| **Successor liability** | Generally no (except specific carve-outs) | Yes — all liabilities transfer | Yes — surviving entity assumes all |
| **Tax to seller (C-corp)** | Double tax (corporate + shareholder) | Single tax at shareholder level | Single tax (if structured properly) |
| **Tax to seller (S-corp/LLC)** | Single tax at owner level | Single tax at owner level | Single tax at owner level |
| **Buyer tax benefit** | Step-up in asset basis (higher future D&A) | No step-up (unless 338(h)(10) election) | No step-up (unless 338(h)(10)) |
| **Contract assignment** | Requires consent per contract | Automatic (unless change-of-control clause) | Automatic by operation of law |
| **Employee transfer** | New employment offers required | Employees remain with entity | Employees remain with surviving entity |
| **Third-party consents** | Extensive (each asset/contract) | Limited (change-of-control only) | Limited |
| **Minority shareholders** | N/A | Must acquire 100% or deal with holdouts | Squeeze-out via appraisal rights |
| **Regulatory complexity** | Lower | Moderate | Higher (board + shareholder approvals) |
| **Best for** | Buying specific divisions; avoiding liabilities | Clean companies; speed to close | Public targets; tax-efficient combinations |

#### Decision Framework

Score each factor 1-5 based on deal circumstances:

| Factor | Favors Asset Deal | Favors Stock Deal | Favors Merger | Score |
|---|---|---|---|---|
| Buyer wants tax step-up | 5 | 1 | 1 | |
| Seller wants single tax layer | 1 | 5 | 5 | |
| Significant contingent liabilities | 5 | 1 | 1 | |
| Many non-assignable contracts | 1 | 5 | 5 | |
| Target has valuable NOLs | 1 | 4 | 4 | |
| Minority shareholder squeeze-out needed | 1 | 1 | 5 | |
| Partial acquisition (division/unit) | 5 | 1 | 1 | |
| Speed to close priority | 2 | 4 | 3 | |
| **Total** | | | | |

Recommend the structure with the highest total score. Document trade-offs for the runner-up.

### 2. Consideration Design

#### Consideration Types

| Type | Description | Seller Impact | Buyer Impact |
|---|---|---|---|
| **Cash** | Immediate payment at close | Certainty; immediate tax event | Cash outflow; possibly debt-funded |
| **Stock** | Buyer equity issued to seller | Tax deferral possible (tax-free reorg); retains upside | No cash outflow; dilution to existing shareholders |
| **Earnout** | Contingent payments tied to future performance | Bridges valuation gap; deferred and uncertain | Reduces upfront risk; creates alignment incentives |
| **Seller note** | Deferred cash payment (promissory note) | Installment sale tax treatment; credit risk on buyer | Reduces upfront cash; cheaper than bank debt |
| **Rollover equity** | Seller reinvests portion into buyer/NewCo | Tax deferral on rolled amount; ongoing participation | Reduces cash need; aligns seller post-close |

#### Consideration Mix Design

State the proposed mix as a table:

| Component | Amount ($M) | % of Total | Key Terms |
|---|---|---|---|
| Cash at close | | | Funded by [source] |
| Stock consideration | | | Exchange ratio: [X] buyer shares per target share; collar/fixed |
| Earnout | | | Metric: [revenue/EBITDA]; Period: [X] years; Cap: $[X]M |
| Seller note | | | Term: [X] years; Interest: [X]%; Subordination: [senior/sub] |
| Rollover equity | | | [X]% of seller proceeds rolled into NewCo |
| Escrow/holdback | | | [X]% held for [X] months for indemnification |
| **Total consideration** | | 100% | |

### 3. Purchase Price Mechanism

Choose between the two standard approaches:

| Dimension | Locked Box | Completion Accounts |
|---|---|---|
| **Reference date** | Pre-signing balance sheet date | Closing date balance sheet |
| **Price certainty** | Fixed at signing (seller-friendly) | Adjusted post-closing (buyer-friendly) |
| **Leakage protection** | Seller covenants against value extraction post-locked-box date | N/A — price adjusts to actual |
| **Working capital** | Included in locked-box price | True-up to agreed target NWC |
| **Cash / debt** | Fixed at locked-box date | Adjusted to actual at close |
| **Dispute risk** | Low (price is fixed) | Higher (completion accounts disputed) |
| **Best for** | Competitive auctions; clean businesses | Volatile working capital; buyer-friendly deals |

If using **completion accounts**, define:

| Adjustment | Target / Peg | Mechanism |
|---|---|---|
| Net working capital | $___M (based on trailing [X]-month average) | Dollar-for-dollar adjustment above/below target |
| Net debt | $0 (cash-free / debt-free basis) | Deducted from headline price |
| Cash | $0 (cash-free / debt-free basis) | Added to headline price |
| Transaction expenses | $0 | Deducted from headline price |
| CapEx true-up | $___M minimum spend | Shortfall deducted from price |

### 4. Key Deal Terms

#### 4a. Representations and Warranties

| Category | Seller Reps (typical) | Buyer Reps (typical) |
|---|---|---|
| **Fundamental** | Authority, organization, capitalization, title to shares | Authority, organization |
| **Financial** | Accuracy of financial statements, no undisclosed liabilities | Solvency, available funds |
| **Operational** | Material contracts, compliance with laws, litigation, IP, employees, tax, environmental, insurance | — |
| **Bring-down** | All reps true at signing and closing | All reps true at signing and closing |

**Survival periods**: Fundamental reps (indefinite or 5-7 years); General reps (12-24 months); Tax reps (statute of limitations + 60 days); Environmental (3-6 years).

#### 4b. Indemnification

| Parameter | Market Range | Recommendation |
|---|---|---|
| **Cap (general)** | 10-20% of enterprise value | [X]% based on risk profile |
| **Cap (fundamental/fraud)** | 100% of purchase price | Full recourse |
| **Basket (deductible)** | 0.5-1.5% of EV | [X]% — tipping vs. true deductible |
| **Mini-basket (de minimis)** | $[X]K per claim threshold | Exclude trivial claims |
| **Escrow amount** | 5-15% of purchase price | $[X]M held for [X] months |
| **Escrow release** | 12-24 months post-close | [X] months, partial release at [X] months |
| **R&W insurance** | Increasingly common; 2-4% premium | Buy-side policy recommended if > $[X]M EV |

#### 4c. Material Adverse Change (MAC) Clause

Define what constitutes a MAC allowing the buyer to terminate:

| Included in MAC Definition | Carved Out (NOT a MAC) |
|---|---|
| Material decline in target's business, operations, financial condition | General economic or industry-wide changes |
| Loss of key customers representing > [X]% revenue | Changes in law or accounting standards |
| Regulatory action materially impairing operations | Effects of the announced transaction itself |
| Material breach of reps or covenants | Pandemics, natural disasters (negotiate) |
| | Changes in financial markets generally |

**Materiality qualifier**: MAC must be material to the target's business "taken as a whole" and must be "durable" (not temporary).

#### 4d. Additional Key Terms

| Term | Description | Market Standard |
|---|---|---|
| **Non-compete** | Seller restricted from competing post-close | 2-4 years; defined geography and scope |
| **Non-solicit** | Seller cannot recruit target employees | 2-3 years; covers employees and customers |
| **Conditions precedent** | Required before closing | Regulatory approvals, third-party consents, financing condition (PE only), no MAC |
| **Interim operating covenants** | Seller runs business in ordinary course between sign and close | Defined positive and negative covenants; materiality thresholds |
| **Termination rights** | Circumstances allowing either party to walk | Longstop date, regulatory failure, uncured breach, board fiduciary out |
| **Break fee / reverse break fee** | Penalty for termination | 2-4% of EV (target break fee); 3-6% (reverse break fee for financing failure) |
| **Go-shop / no-shop** | Post-signing solicitation rights | No-shop standard; go-shop in PE deals (20-40 days) |

### 5. Earnout Design (if applicable)

Earnouts require careful design to avoid disputes:

| Design Element | Recommendation |
|---|---|
| **Metric** | Revenue (harder to manipulate) preferred over EBITDA (subject to cost allocation) |
| **Measurement period** | 1-3 years; annual measurements with interim payments |
| **Targets** | Tiered: threshold (floor), target (midpoint), stretch (cap) |
| **Accounting treatment** | Specify GAAP/IFRS basis; define permitted and excluded adjustments |
| **Operational covenants** | Buyer commits to operate business in manner consistent with earnout achievement |
| **Dispute resolution** | Independent accountant for calculation disputes; arbitration for covenant disputes |
| **Acceleration** | Full earnout payable if buyer materially changes business or sells target |
| **Cap** | Maximum total earnout payment = $[X]M |

### 6. Tax Implications Summary

| Structure | Seller Tax Treatment | Buyer Tax Treatment | Key Consideration |
|---|---|---|---|
| Cash asset purchase | Ordinary income on recaptured depreciation; capital gain on goodwill | Step-up in basis; amortize goodwill over 15 years (Section 197) | Best buyer tax outcome; worst seller tax outcome (C-corp double tax) |
| Cash stock purchase | Capital gains on share sale | No step-up; carryover basis | Clean for seller; suboptimal for buyer |
| Stock purchase + 338(h)(10) | Treated as asset sale for tax | Step-up in basis (same as asset deal) | Requires both parties' agreement; only for S-corps and subs |
| Tax-free reorganization (stock-for-stock) | Tax deferred on stock received | Carryover basis in target assets | Requires continuity of interest (>40% stock); no step-up |
| Installment sale (seller note) | Gain recognized as payments received | Interest deductible | Seller defers tax; must meet installment sale rules |

Recommend structure based on combined tax efficiency. Model the after-tax proceeds to the seller under each alternative.

## Output Template

```markdown
## Deal Structure: [Buyer] Acquisition of [Target]

**Date**: [Date] | **Indicative EV**: $[X]M | **Structure**: [Asset/Stock/Merger]

### Transaction Summary
| Item | Detail |
|---|---|
| Buyer | [Name and type] |
| Target | [Name, entity type, jurisdiction] |
| Enterprise value | $[X]M |
| Equity value | $[X]M |
| Structure | [Asset purchase / Stock purchase / Merger] |
| Consideration | [Cash/Stock/Mixed — summary] |

### Structure Rationale
[Why this structure was selected over alternatives, with reference to scoring]

### Consideration Mix
| Component | Amount ($M) | % of Total | Key Terms |
|---|---|---|---|
| ... | | | |

### Purchase Price Mechanism
[Locked box or completion accounts with adjustment mechanics]

### Key Terms Summary

#### Representations and Warranties
[Summary of scope and survival periods]

#### Indemnification
[Cap, basket, escrow, R&W insurance recommendation]

#### MAC Clause
[Definition and carve-outs]

#### Restrictive Covenants
[Non-compete, non-solicit scope and duration]

#### Conditions Precedent
[Required approvals and conditions for closing]

#### Termination Rights
[Break fees and termination triggers]

### Earnout Structure (if applicable)
[Metric, targets, measurement period, protections]

### Tax Analysis
| Structure Option | Seller After-Tax Proceeds | Buyer NPV of Tax Benefit | Combined Efficiency |
|---|---|---|---|
| ... | | | |

### Key Risks and Mitigants
| Risk | Probability | Impact | Mitigant |
|---|---|---|---|
| ... | | | |

### Indicative Timeline
| Milestone | Target Date |
|---|---|
| LOI / Term sheet | Week [X] |
| Due diligence completion | Week [X] |
| Definitive agreement signed | Week [X] |
| Regulatory filings | Week [X] |
| Closing | Week [X] |
```

## Quality Checks

- [ ] Deal structure (asset/stock/merger) explicitly selected with documented rationale using the scoring framework.
- [ ] Tax implications modeled for both buyer and seller under the chosen structure and at least one alternative.
- [ ] Consideration mix fully specified with dollar amounts, percentages, and key terms for every component.
- [ ] Purchase price mechanism (locked box or completion accounts) defined with specific adjustment items and targets.
- [ ] Reps and warranties categorized (fundamental, financial, operational) with survival periods stated.
- [ ] Indemnification terms specified: cap, basket, de minimis, escrow amount, and escrow duration.
- [ ] MAC clause defined with both inclusions and carve-outs explicitly listed.
- [ ] Earnout (if included) has a defined metric, measurement period, tiered targets, operational covenants, dispute resolution, and cap.
- [ ] Non-compete and non-solicit have specific duration and scope (not left as "to be agreed").
- [ ] Conditions precedent enumerated, including regulatory approvals, consents, and financing conditions.
- [ ] Cross-reference: `valuation` skill used or referenced for the enterprise-to-equity value bridge and valuation basis.
- [ ] Cross-reference: `tax-structure-advisory` skill referenced for detailed tax structuring analysis where applicable.
