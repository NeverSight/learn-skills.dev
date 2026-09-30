---
name: gaap-reporting
description: Prepare GAAP financial statements, classifications, disclosures, and management reporting packages.
---

## Profit and Loss Statement

### Recommended Line-Item Structure (Functional Expense Method)

```
Net Revenue
  Product sales
  Services
  Other sources
Total Net Revenue

Direct Costs
  Cost of products sold
  Cost of services delivered
Total Direct Costs

Gross Margin

Functional Operating Costs
  Research & development
  Selling & marketing
  General & administrative
Total Functional Operating Costs

Income from Operations

Non-Operating Items
  Interest earned
  Interest charges
  Gains (losses) on investments
  Miscellaneous, net
Total Non-Operating Items

Pre-Tax Income (Loss)
  Provision for income taxes
Net Income (Loss)

Per-Share Data (where applicable)
  Basic EPS
  Diluted EPS
```

### Regulatory Framework (ASC 220 / IAS 1)

- Every recognized revenue and cost item within the reporting window must appear on the face or in accompanying notes
- US registrants predominantly organize costs by business function (COGS, R&D, S&M, G&A); the alternative nature-based grouping (raw materials, wages, depreciation) is more prevalent under IFRS
- Functional filers must supplement with nature-of-expense detail (depreciation, amortization, personnel costs) in the footnotes
- Operating results and non-operating activity should occupy distinct sections
- Tax expense stands alone as its own line item
- Neither US GAAP nor IFRS permits classification of any item as "extraordinary"
- Discontinued segments are segregated below continuing operations on an after-tax basis

### Noteworthy Presentation Items

- **Revenue breakdowns:** Under ASC 606, disaggregate revenue along dimensions that reveal how economic conditions influence the nature, timing, amount, and collectibility of cash flows
- **Equity-based compensation:** Allocate across functional categories on the face; aggregate total stock compensation in the notes
- **Restructuring costs:** Disclose separately when material; otherwise embed in operating expenses with footnote detail
- **Non-GAAP metrics:** Clearly label as supplemental, provide a full reconciliation back to GAAP figures, and explain the rationale for presentation

## Statement of Financial Position

### Recommended Line-Item Structure (Classified Approach)

```
ASSETS
Short-Term Assets
  Cash & equivalents
  Marketable securities
  Trade receivables (net of credit allowance)
  Inventories
  Prepayments & other short-term assets
Total Short-Term Assets

Long-Term Assets
  Property, plant & equipment (net)
  Lease right-of-use assets (operating)
  Goodwill
  Other intangible assets (net)
  Equity & debt investments
  Other long-term assets
Total Long-Term Assets

TOTAL ASSETS

LIABILITIES & SHAREHOLDERS' EQUITY
Short-Term Liabilities
  Trade payables
  Accrued expenses
  Contract liabilities (current)
  Current maturities of borrowings
  Current operating lease obligations
  Other short-term liabilities
Total Short-Term Liabilities

Long-Term Liabilities
  Borrowings (non-current)
  Contract liabilities (non-current)
  Operating lease obligations (non-current)
  Other long-term liabilities
Total Long-Term Liabilities

Total Liabilities

Shareholders' Equity
  Common shares
  Additional paid-in capital
  Retained earnings (deficit)
  Other comprehensive income (loss)
  Treasury shares
Total Shareholders' Equity

TOTAL LIABILITIES & SHAREHOLDERS' EQUITY
```

### Regulatory Framework (ASC 210 / IAS 1)

- Segregate short-term from long-term based on the 12-month horizon (or the entity's operating cycle, if longer)
- US convention sequences assets from most liquid to least liquid
- Trade receivables carry a net presentation after deducting the expected credit loss reserve per ASC 326 (CECL)
- Tangible fixed assets appear net of cumulative depreciation
- Goodwill undergoes annual impairment review rather than systematic amortization (ASC 350)
- Both operating and finance leases produce right-of-use assets with corresponding obligations (ASC 842)

## Statement of Cash Flows

### Recommended Structure (Indirect Approach)

```
OPERATING CASH FLOWS
Net income (loss)
Non-cash reconciling items:
  Depreciation & amortization
  Equity-based compensation
  Debt discount amortization
  Deferred tax movement
  Asset disposal gains (losses)
  Impairment write-downs
  Other non-cash charges
Working capital movements:
  Trade receivables
  Inventories
  Prepayments & other assets
  Trade payables
  Accrued expenses
  Contract liabilities
  Other liabilities
Net Cash from Operating Activities

INVESTING CASH FLOWS
  Capital expenditures
  Securities purchased
  Securities sold or matured
  Business combinations (net of acquired cash)
  Other investing items
Net Cash from Investing Activities

FINANCING CASH FLOWS
  Debt proceeds
  Debt repayments
  Stock issuance proceeds
  Share repurchases
  Dividend distributions
  Debt issuance cost payments
  Other financing items
Net Cash from Financing Activities

Foreign currency translation effect on cash

Net Change in Cash & Equivalents
Opening cash & equivalents
Closing cash & equivalents
```

### Regulatory Framework (ASC 230 / IAS 7)

- The indirect method (reconciling net income to operating cash flow) dominates practice; the direct method is allowed but demands a supplemental indirect reconciliation
- Amounts of interest paid and taxes remitted require disclosure (on-face or in notes)
- Non-cash investing/financing transactions (e.g., lease asset recognition, equity issued in acquisitions) are disclosed in a supplemental schedule
- Cash equivalents are limited to highly liquid instruments originally maturing within 90 days

## Period-End Adjustments & Reclassifications

### Adjusting Entries

1. **Accrued expenses:** Capture obligations incurred but not yet billed (vendor accruals, compensation accruals, interest obligations)
2. **Deferred item amortization:** Systematically release prepayments, deferred costs, and contract liabilities over the service window
3. **Fixed asset & intangible charges:** Post scheduled depreciation and amortization from subsidiary registers
4. **Credit loss provisioning:** Update the allowance for uncollectible accounts using aging data and historical recovery patterns
5. **Inventory valuation:** Write down excess, obsolete, or damaged stock to net realizable value
6. **Currency remeasurement:** Restate monetary items denominated in foreign currencies at closing exchange rates
7. **Income tax accrual:** Compute current tax payable and adjust deferred tax assets/liabilities
8. **Fair value marks:** Remeasure trading securities, derivatives, and other Level 1-3 instruments to period-end fair value

### Reclassification Entries

1. **Maturity reclassification:** Move borrowings due within 12 months from long-term to current
2. **Contra-account presentation:** Offset gross receivables with credit loss reserves; offset gross fixed assets with accumulated depreciation
3. **Consolidation eliminations:** Remove intercompany balances and intra-group revenue/expense
4. **Discontinued operations carve-out:** Shift earnings and net assets of divested or held-for-sale segments to the required separate line
5. **Equity method recognition:** Record the investor's proportionate share of investee earnings
6. **Segment mapping:** Verify that every transaction aligns with its correct operating segment

## Comparative Analysis Approach

### Computing Period-Over-Period Movements

For every material line:
- **Absolute change:** Current period amount minus comparison period amount
- **Relative change:** Absolute change divided by the absolute value of the comparison period, expressed as a percentage
- **Margin shift (where applicable):** Difference in percentage-of-revenue ratios, expressed in basis points (1 bp = 0.01%)

### Significance Criteria

Tailor investigation thresholds to the entity's scale and risk profile:

| Balance Magnitude | Absolute Trigger | Relative Trigger |
|---|---|---|
| Above $10M | $500K | 5% |
| $1M to $10M | $100K | 10% |
| Under $1M | $50K | 15% |

### Isolating Movement Drivers

Break total movement into root causes:

- **Volume/quantity shift:** Incremental units at prior-period pricing
- **Rate/price shift:** Changed pricing applied to current-period units
- **Product or channel mix:** Composition changes affecting blended margins
- **New or exiting items:** Line items with activity in only one of the two periods
- **Non-recurring events:** Charges or gains unlikely to repeat
- **Phasing/timing:** Activity that shifted across reporting periods without affecting the annual run rate
- **Translation effects:** Impact of currency fluctuations on consolidated results

### Building the Narrative

For every movement that exceeds significance criteria:
1. State the magnitude (dollars and percentage)
2. Label the direction as favorable or unfavorable
3. Attribute the movement to specific drivers from the list above
4. Explain the underlying business rationale
5. Indicate whether the movement is transient or reflects a sustained trajectory change
6. Flag any follow-up actions (deeper investigation, forecast revision, process adjustment)
