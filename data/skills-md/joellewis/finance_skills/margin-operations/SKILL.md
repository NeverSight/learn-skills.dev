---
name: margin-operations
description: "Guide margin lending, margin requirements, and margin call operations for brokerage and advisory accounts. Use when calculating Reg T initial margin or buying power, determining maintenance margin or house requirements, evaluating portfolio margin eligibility under OCC TIMS, generating or resolving margin calls (fed call, house call, exchange call, day-trade call), designing forced liquidation waterfall logic, structuring securities-backed lines of credit (SBLOC), computing margin interest impact on returns, assessing concentrated position margin, understanding pattern day trader rules, or reviewing FINRA 4210 and Reg U requirements. Also covers SMA calculations and short margin mechanics."
---

# Margin Operations

## Purpose
Guide the understanding and management of margin lending, margin requirements, and margin call operations in brokerage and advisory settings. Covers Regulation T initial margin, FINRA/exchange maintenance margin, portfolio margin methodology, margin call types and procedures, forced liquidation processes, securities-backed lines of credit (SBLOC), and margin risk management. Enables building or evaluating margin systems and understanding margin impact on portfolio management and client accounts.

## Layer
11 — Trading Operations (Order Lifecycle & Execution)

## Direction
both

## When to Use
- Calculating initial margin requirements and buying power for new trades
- Determining maintenance margin and house requirements for existing positions
- Evaluating portfolio margin eligibility and benefits for an account
- Generating, tracking, or resolving margin calls (fed calls, house calls, exchange calls)
- Designing or reviewing forced liquidation procedures and waterfall logic
- Structuring or evaluating securities-backed lines of credit (SBLOC or non-purpose loans)
- Stress testing margin exposure across portfolio scenarios
- Computing margin interest charges and their impact on investment returns
- Assessing concentrated position margin requirements and risk
- Understanding day-trade margin rules for pattern day traders
- Reviewing margin-related regulatory requirements (Reg T, Reg U, FINRA 4210)

## Core Concepts

### Regulation T Initial Margin
The Federal Reserve's Regulation T establishes the initial margin requirement for purchasing securities on credit. Key provisions:

- **50% initial margin requirement:** An investor must deposit at least 50% of the purchase price of marginable securities. For a $100,000 purchase, the investor must deposit $50,000 (cash or marginable securities); the broker-dealer may lend the remaining $50,000.
- **Reg T buying power:** The maximum dollar amount a client can purchase given their available equity. Buying power = SMA x 2 (for equity securities under Reg T). If a client deposits $100,000 cash in a new margin account, buying power is $200,000.
- **Special Memorandum Account (SMA):** A bookkeeping entry that tracks the client's excess Reg T equity. SMA increases when: the account has excess equity above 50%, securities are sold, dividends or cash are deposited. SMA decreases when used to purchase securities or withdraw cash. SMA is a high-water mark — it does not decrease when market values decline (unless used).
- **Reg T extension procedures:** When a client fails to meet the initial margin requirement by settlement date, the broker-dealer must request an extension from a self-regulatory organization (SRO). Extensions are typically granted for 1-5 business days. Failure to meet the call results in forced liquidation and a 90-day freeze (restricted account).
- **Exempt securities:** U.S. government bonds, municipal bonds, and certain agency securities are exempt from Reg T margin requirements — they can be purchased with lower or no initial margin.
- **Day-trade margin:** FINRA Rule 4210 provides pattern day traders (4+ day trades in 5 business days) with 4:1 intraday buying power (25% margin) but requires a minimum equity of $25,000. Overnight positions revert to standard 2:1 Reg T buying power.

### Maintenance Margin
After the initial purchase, ongoing maintenance margin requirements determine the minimum equity the account must maintain:

- **FINRA Rule 4210 minimum:** 25% equity for long positions. Account equity = market value of securities minus debit balance. If equity falls below 25% of market value, a maintenance margin call is triggered.
- **House maintenance requirements:** Most broker-dealers impose requirements above the FINRA minimum, typically 30-40% for diversified accounts. House requirements vary by firm and may change based on market conditions.
- **Concentrated position margin:** Single-stock positions exceeding a threshold (e.g., 40-60% of account value) face elevated margin requirements, often 50-75% or higher. This discourages excessive concentration in margin accounts.
- **Long margin formula:** Maintenance call triggered when equity / market value < maintenance requirement. Equivalently, a call is triggered when market value falls to: debit balance / (1 - maintenance requirement).
- **Short margin requirements:** Short positions require initial margin of 50% (Reg T) and maintenance of 30% of market value (FINRA minimum). Short account equity = credit balance - market value of short securities. A short squeeze (rising prices) increases the maintenance requirement.
- **Options margin:** Options strategies have specific margin requirements under FINRA Rule 4210 and exchange rules. Covered calls require no additional margin (shares serve as collateral). Naked short options require substantial margin — typically the greater of: (a) option premium + 20% of underlying value - out-of-the-money amount, or (b) option premium + 10% of underlying value. Spreads have defined-risk margin equal to the maximum loss.

### Portfolio Margin
A risk-based margining methodology that can significantly reduce margin requirements for hedged or diversified portfolios:

- **Methodology:** Uses the Options Clearing Corporation's Theoretical Intermarket Margin System (OCC TIMS) to compute margin based on the theoretical maximum loss of the portfolio under a range of stress scenarios, rather than applying fixed percentage requirements to each position independently.
- **Eligibility requirements:** Minimum account equity of $100,000 (FINRA Rule 4210(g)), options trading approval (typically Level 3 or 4), and the firm may impose additional requirements such as minimum net worth, trading experience, or completion of a portfolio margin agreement.
- **Stress test scenarios:** The OCC TIMS model evaluates portfolio profit and loss under standardized moves:
  - Large-cap equities: +/- 15% (with intermediate points at +/- 5%, +/- 10%)
  - Small-cap equities: +/- 10% higher stress (effectively +/- 25%)
  - Broad market indices: +/- 8% to +/- 15%
  - High-volatility securities: firm-specific add-ons
  - The largest theoretical loss across all scenarios becomes the margin requirement
- **Portfolio margin vs Reg T comparison:** A hedged equity portfolio with offsetting options positions might require 50% margin under Reg T (applied position-by-position) but only 10-20% under portfolio margin (reflecting the actual net risk). Conversely, a concentrated, unhedged portfolio may see little benefit from portfolio margin.
- **Benefits:** More efficient use of capital, margin requirements that reflect actual portfolio risk, ability to maintain larger or more complex positions, and alignment between margin and true economic risk.
- **Risks:** Lower margin requirements increase leverage, amplifying both gains and losses. A sudden correlation shift or gap move can produce losses exceeding the stress test scenarios. Portfolio margin accounts can experience rapid, severe margin calls during market dislocations.

### Margin Call Types
Multiple types of margin calls can arise, each with distinct triggers, deadlines, and resolution procedures:

- **Reg T initial call (federal call):** Triggered when a client purchases marginable securities and the account does not have sufficient equity to satisfy the 50% Reg T requirement. Must be met by settlement date (T+1 for most securities). Met by depositing cash or fully paid marginable securities. Failure to meet triggers liquidation and potential 90-day account restriction.
- **Maintenance margin call (house call):** Triggered when account equity falls below the firm's house maintenance requirement (typically 30-40%). The client is typically given T+5 business days (or less, at the firm's discretion) to deposit funds or securities, or the firm will liquidate positions. Unlike Reg T calls, there is no SRO extension mechanism for house calls — the timeline is at the firm's discretion.
- **Exchange minimum call:** Triggered when account equity falls below the FINRA/exchange minimum of 25%. These calls demand immediate attention and may be subject to same-day or next-day resolution.
- **Day-trade call:** Triggered when a pattern day trader's account equity falls below the $25,000 minimum or when day-trade buying power is exceeded. Must be met within 5 business days. Failure restricts the account to cash-available trading.
- **Concentration call:** Triggered when a single position exceeds the firm's concentration threshold and the account's equity is insufficient to meet the elevated requirement. Common in accounts holding large positions in a single stock.

### Margin Call Procedures
The end-to-end process from call generation through resolution:

- **Call generation:** Margin calls are generated during the end-of-day mark-to-market process. The firm's margin system reprices all positions at closing market values, recalculates equity and margin requirements, and identifies accounts in deficit. Intraday monitoring may generate real-time alerts for large deficits.
- **Notification requirements:** FINRA requires prompt notification to the customer. Firms typically notify via multiple channels: automated system alerts, email, phone calls from the margin department. Written notification must document the call amount, the positions involved, and the deadline for resolution.
- **Client communication:** The margin department communicates the amount due, the deadline, and the options available: deposit cash, deposit marginable securities, liquidate positions, or some combination. Best practice is to confirm the client's intentions in writing.
- **Call resolution tracking:** The margin system tracks each open call, the deadline, any partial payments received, and escalation status. Calls are resolved when equity is restored to or above the required level.
- **Extension requests:** For Reg T calls, the firm may request an extension from its designated examining authority (DEA) or SRO — typically 1-5 business days. Extensions are not automatic and are granted based on the circumstances (e.g., pending settlement of a sale, wire transfer in process). Repeated extension requests for the same account may trigger regulatory scrutiny.
- **Automatic liquidation triggers:** If the call is not met by the deadline and no extension is granted, the firm is obligated to liquidate sufficient positions to bring the account into compliance. Many firms have automated systems that initiate liquidation at a specified time on the deadline day.
- **Partial call satisfaction:** A client may partially satisfy a call through a combination of deposits and sales. The margin system must track partial payments and recalculate the remaining call amount after each action.

### Forced Liquidation
When a margin call is not met, the broker-dealer must liquidate positions to bring the account into compliance:

- **Liquidation waterfall:** Firms establish a priority order for which positions to liquidate first. A common waterfall:
  1. Fully paid (non-margin) positions with no tax consequences if available for transfer
  2. Positions specifically identified by the client (if communicated in time)
  3. Most liquid positions (highest average daily volume, tightest bid-ask spreads)
  4. Positions with the lowest unrealized gain or highest unrealized loss (minimizing tax impact where feasible)
  5. Concentrated positions contributing most to the margin deficit
  6. Least liquid positions as a last resort
- **Liquidation priority rules:** The firm has discretion over which positions to liquidate and is not required to follow client preferences, though best practice is to accommodate client requests when operationally feasible. The firm's primary obligation is to reduce the margin deficit.
- **Client notification:** The firm should notify the client before or promptly after liquidation, though FINRA does not require prior consent for liquidation of margin-deficient accounts. The client cannot prevent the firm from liquidating.
- **Best execution in liquidation:** Forced liquidation must still comply with best execution obligations. Orders should be routed to obtain the best reasonably available price, even under time pressure. Market orders in illiquid securities during forced liquidation can create adverse price impact.
- **Restricted account status:** An account that fails to meet a Reg T call may be restricted for 90 days, during which the client must fully prepay any purchases (no margin extension). Subsequent violations may result in longer restrictions or account closure.
- **Close-out obligations:** Under SEC Rule 15c3-3 and SRO rules, the firm must close out fail-to-deliver positions within specified timeframes. Margin liquidation must be completed promptly, and any resulting short positions or failed deliveries must be resolved per regulatory requirements.

### Securities-Backed Lines of Credit (SBLOC)
Lending products that use an investment portfolio as collateral, distinct from traditional margin lending:

- **Non-purpose loans vs purpose loans:** An SBLOC is typically a non-purpose loan — the proceeds may be used for any purpose except purchasing, carrying, or trading securities. This distinction matters because non-purpose loans are governed by Regulation U (for banks) or Regulation T (for broker-dealers), with different requirements depending on the lender type.
- **Collateral requirements:** The investment portfolio secures the loan. Lenders apply loan-to-value (LTV) ratios to determine borrowing capacity:
  - Equities (large-cap, diversified): 50-70% LTV
  - Fixed income (investment grade): 70-90% LTV
  - Mutual funds/ETFs (broad market): 50-75% LTV
  - Cash and money market: 90-95% LTV
  - Concentrated single-stock positions: 30-50% LTV (reduced due to specific risk)
  - Alternative investments, restricted stock, penny stocks: 0% LTV (not accepted as collateral)
- **Concentration limits:** Lenders limit the percentage of the collateral portfolio that can be in a single security (typically 40-60% maximum). Positions exceeding the concentration limit receive reduced or zero LTV on the excess.
- **Maintenance and call procedures:** Similar to margin accounts, SBLOC facilities have maintenance requirements. If the portfolio value declines such that the LTV exceeds the maintenance threshold, the lender issues a collateral call. The borrower must deposit additional collateral, repay part of the loan, or face liquidation of the pledged portfolio.
- **Regulatory considerations:** Banks offering SBLOCs are subject to Regulation U (Fed), which imposes a 50% maximum LTV for purpose loans but has no specific LTV limit for non-purpose loans — the bank applies its own underwriting standards. Broker-dealers offering similar credit are subject to Regulation T. The distinction between purpose and non-purpose must be documented (Form U-1 for banks, Form T-4 for broker-dealers).
- **Risks to the borrower:** Portfolio declines can trigger collateral calls; forced liquidation of securities may occur at unfavorable prices and create taxable events; the interest rate is typically variable (prime + spread); and the borrower retains full investment risk on the pledged portfolio while adding debt service obligations.

### Margin Risk Management
Ongoing monitoring and management of margin-related risks across the firm and client accounts:

- **Portfolio-level margin monitoring:** The firm's risk management system continuously monitors aggregate margin exposure, identifying accounts approaching margin call thresholds, concentrated positions, and correlated risks across the client base. Real-time intraday monitoring supplements end-of-day calculations.
- **Stress testing margin requirements:** The firm should stress test margin exposure under adverse scenarios — market declines of 10-20%, sector-specific shocks, volatility spikes, and correlation breakdowns. Stress tests reveal accounts and portfolios that would face large margin calls under stressed conditions.
- **Concentrated position risk:** Positions that represent a large percentage of account value or a large percentage of a security's outstanding shares create elevated margin risk. Firms typically impose higher margin requirements and may impose position limits or require diversification plans.
- **Margin impact on investment returns:** Margin amplifies both gains and losses. A 50% margin (2:1 leverage) doubles the percentage gain or loss:
  - Unleveraged: $100K invested, market +10% = $10K gain (10% return)
  - Leveraged at 2:1: $200K invested with $100K equity, market +10% = $20K gain minus interest = ~18% return on equity
  - Leveraged at 2:1: $200K invested with $100K equity, market -10% = $20K loss plus interest = ~-22% return on equity
- **Interest rate calculation on margin debit balances:** Margin interest is calculated daily on the outstanding debit balance:
  - Daily interest = debit balance x (annual rate / 360)
  - Interest is typically charged monthly (sum of daily accruals)
  - Rates are tiered by debit balance size: larger balances receive lower rates
  - Example rate schedule: <$25K = broker call rate + 1.5%; $25K-$100K = call rate + 1.0%; >$100K = call rate + 0.5%
- **Tax treatment of margin interest:** Margin interest is deductible as investment interest expense on Schedule A (Form 1040), but only up to the amount of net investment income. Excess margin interest can be carried forward. Investment interest does not include qualified dividends or long-term capital gains unless the taxpayer elects to treat them as ordinary income. This deduction requires itemizing.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Reg T buying power | SMA x 2 | Maximum purchase amount |
| Initial margin requirement | Purchase price x 50% | Cash/equity deposit required |
| Account equity (long) | Market value - debit balance | Current equity in account |
| Maintenance call trigger (long) | Debit balance / (1 - maintenance %) | Price at which call is triggered |
| Maintenance call amount | (Maintenance % x market value) - equity | Dollar amount due |
| Short account equity | Credit balance - market value (short) | Equity in short positions |
| Margin interest (daily) | Debit balance x (annual rate / 360) | Daily interest accrual |
| Leveraged return | (Portfolio return x leverage) - (interest x (leverage - 1)) | Return on equity with margin |
| SBLOC borrowing capacity | Sum(collateral value x LTV by type) | Maximum loan amount |
| Day-trade buying power | (Equity - $25,000 minimum) x 4 | Intraday purchasing power |

## Worked Examples

### Example 1: Calculating margin requirements and buying power for a diversified brokerage account

**Given:** A client opens a new margin account and deposits $150,000 in cash. The client wants to build a diversified portfolio.

**Step 1 — Determine Reg T buying power:**
- Cash deposit: $150,000
- SMA: $150,000 (initial cash deposit establishes the SMA)
- Reg T buying power: $150,000 x 2 = **$300,000**

**Step 2 — Client purchases a diversified portfolio:**
- $120,000 in large-cap equity ETF (VTI)
- $60,000 in international equity ETF (VXUS)
- $40,000 in investment-grade bond ETF (BND)
- $30,000 in REIT ETF (VNQ)
- Total purchases: $250,000

**Step 3 — Post-purchase account status:**
- Market value: $250,000
- Debit balance: $250,000 - $150,000 = $100,000
- Account equity: $250,000 - $100,000 = $150,000
- Equity percentage: $150,000 / $250,000 = **60%** (above 50% Reg T requirement)
- Remaining SMA: $150,000 - ($250,000 x 50%) = $150,000 - $125,000 = $25,000
- Remaining buying power: $25,000 x 2 = **$50,000**

**Step 4 — Determine maintenance call trigger (assuming 30% house requirement):**
- House maintenance: 30%
- Call triggered when: equity / market value < 30%
- Equivalently: market value falls to debit balance / (1 - 0.30) = $100,000 / 0.70 = **$142,857**
- This represents a decline of ($250,000 - $142,857) / $250,000 = **42.9%** from current value

**Step 5 — Margin interest cost estimate:**
- Debit balance: $100,000
- Assume margin rate: broker call rate (6.50%) + 0.75% = 7.25%
- Annual interest: $100,000 x 7.25% = $7,250
- Monthly interest: approximately $604
- This cost must be offset by portfolio returns exceeding 7.25% (on the borrowed portion) to add value through leverage

**Step 6 — Impact of a 15% market decline:**
- New market value: $250,000 x 0.85 = $212,500
- Debit balance unchanged: $100,000
- New equity: $212,500 - $100,000 = $112,500
- Equity percentage: $112,500 / $212,500 = **52.9%** (still above 30% house requirement; no margin call)
- New SMA: remains at $25,000 (SMA is a high-water mark; does not decrease with market decline)

### Example 2: Managing a margin call sequence from generation through resolution

**Given:** An existing margin account with the following position prior to market decline:
- Market value: $400,000 (80% equities, 20% bonds)
- Debit balance: $160,000
- Equity: $240,000 (60%)
- House maintenance requirement: 35%

**Day 1 — Market decline triggers a margin call:**
- Equities decline 18% over several days; bonds flat
- New equity market value: $320,000 x 0.82 = $262,400
- New bond market value: $80,000
- New total market value: $262,400 + $80,000 = $342,400
- Debit balance unchanged: $160,000
- New equity: $342,400 - $160,000 = $182,400
- Equity percentage: $182,400 / $342,400 = **53.3%** (above 35%; no call yet)

**Day 5 — Further decline triggers the call:**
- Additional equity decline of 10% from Day 1 levels
- New equity market value: $320,000 x 0.72 = $230,400
- New bond market value: $80,000
- New total market value: $230,400 + $80,000 = $310,400
- Debit balance: $160,000
- New equity: $310,400 - $160,000 = $150,400
- Equity percentage: $150,400 / $310,400 = **48.5%** (above 35%; still no call)

**Day 8 — Continued decline and call is triggered:**
- Equities now down 35% total from original; bonds down 3%
- New equity market value: $320,000 x 0.65 = $208,000
- New bond market value: $80,000 x 0.97 = $77,600
- New total market value: $208,000 + $77,600 = $285,600
- Debit balance: $160,000
- New equity: $285,600 - $160,000 = $125,600
- Equity percentage: $125,600 / $285,600 = **43.98%** (above 35%; still no call)

**Day 12 — Severe decline triggers call:**
- Equities now down 45% total from original; bonds down 5%
- New equity market value: $320,000 x 0.55 = $176,000
- New bond market value: $80,000 x 0.95 = $76,000
- New total market value: $176,000 + $76,000 = $252,000
- Debit balance: $160,000
- New equity: $252,000 - $160,000 = $92,000
- Equity percentage: $92,000 / $252,000 = **36.5%** (above 35%, but very close)

**Day 14 — Call triggered:**
- Equities down 48% total; bonds down 5%
- New equity market value: $320,000 x 0.52 = $166,400
- New bond market value: $76,000
- New total market value: $166,400 + $76,000 = $242,400
- Debit balance: $160,000
- New equity: $242,400 - $160,000 = $82,400
- Equity percentage: $82,400 / $242,400 = **34.0%** — **below 35% house requirement**
- **House margin call generated** at end of day

**Margin call amount calculation:**
- Required equity: 35% x $242,400 = $84,840
- Current equity: $82,400
- **Call amount: $84,840 - $82,400 = $2,440**

**Day 14 — Notification and communication:**
- Automated margin call alert sent via system notification and email
- Margin department places phone call to client
- Notification states: $2,440 due by Day 19 (T+5 business days)
- Options presented: deposit cash, deposit marginable securities (at loan value), or liquidate positions

**Day 16 — Client responds:**
- Client deposits $5,000 cash (exceeds call amount to provide buffer)
- New debit balance: $160,000 - $5,000 = $155,000
- Assuming market unchanged: equity = $242,400 - $155,000 = $87,400
- Equity percentage: $87,400 / $242,400 = **36.1%** (above 35%)
- **Margin call satisfied**

**Alternative resolution — Partial liquidation:**
- If client cannot deposit, sell $7,000 of bond ETF
- Proceeds reduce debit balance: $160,000 - $7,000 = $153,000
- New market value: $242,400 - $7,000 = $235,400
- New equity: $235,400 - $153,000 = $82,400
- Equity percentage: $82,400 / $235,400 = **35.0%** (at the requirement; call met but no buffer)
- Better approach: sell more to create a buffer above the requirement

### Example 3: Evaluating portfolio margin benefits for an active options trader

**Given:** An experienced options trader maintains the following portfolio:
- Account equity: $500,000
- Long 2,000 shares SPY at $450 = $900,000
- Long 20 SPY 420 puts (protective puts, 3-month expiry), premium paid $8 per contract = $16,000
- Short 20 SPY 480 calls (covered calls, 3-month expiry), premium received $5 per contract = $10,000
- Net portfolio delta: reduced from 2,000 to approximately 1,400 (hedged)

**Step 1 — Calculate Reg T margin requirement:**
Under Reg T, margin is calculated position-by-position:
- Long 2,000 shares SPY at $450: 50% initial margin = $450,000
- Long 20 SPY 420 puts: fully paid (no margin required; cost $16,000 already paid)
- Short 20 SPY 480 calls: covered by long shares (no additional margin required)
- **Total Reg T margin requirement: $450,000**
- Account equity: $500,000
- Excess equity: $500,000 - $450,000 = $50,000
- The protective puts and covered calls provide risk reduction, but Reg T does not recognize the hedge

**Step 2 — Calculate portfolio margin requirement:**
Under portfolio margin (OCC TIMS), the entire position is evaluated as a unit under stress scenarios:
- The key stress scenario is SPY -15% (worst case for this long-biased portfolio):
  - SPY drops from $450 to $382.50
  - Long stock loss: 2,000 x ($450 - $382.50) = -$135,000
  - Long 420 puts gain: puts move deep in-the-money; approximate gain: 20 x 100 x ($420 - $382.50 - $8) = +$59,000
  - Short 480 calls gain: calls expire worthless; gain: 20 x 100 x $5 = +$10,000
  - **Net portfolio loss under -15% stress: -$135,000 + $59,000 + $10,000 = -$66,000**
- Additional stress scenarios (+15%, +/-5%, +/-10%) produce smaller losses for this position
- **Portfolio margin requirement: approximately $66,000** (the largest loss across all scenarios)

**Step 3 — Compare Reg T vs portfolio margin:**

| Metric | Reg T | Portfolio Margin |
|--------|-------|-----------------|
| Margin requirement | $450,000 | $66,000 |
| Equity required | $450,000 | $66,000 |
| Excess equity | $50,000 | $434,000 |
| Additional buying power | $100,000 | $868,000 |
| Margin as % of market value | 50% | 7.3% |
| Leverage ratio | 1.8x | 13.6x (available, not necessarily used) |

**Step 4 — Assess the implications:**
- Portfolio margin reduces the requirement by **85%** because it recognizes the protective puts and covered calls as risk-reducing hedges
- The trader can deploy excess capital to additional strategies or maintain a larger cash buffer
- **Risk consideration:** The 13.6x available leverage is dangerous if fully utilized. The trader should maintain a self-imposed margin buffer well above the minimum — targeting no more than 50-60% utilization of portfolio margin capacity
- **Stress test beyond the model:** If SPY gaps down 25% overnight (beyond the 15% stress scenario), the portfolio loss would be approximately $100,000 — still within the $500,000 equity but illustrating that the OCC TIMS scenarios do not capture tail risk. The trader should run their own stress tests at more extreme levels
- **Qualification check:** The account meets the $100,000 minimum equity requirement. The trader must have appropriate options approval and complete the firm's portfolio margin agreement

## Common Pitfalls
- Confusing SMA with account equity — SMA is a high-water mark that does not decline with market value drops, leading clients to believe they have more cushion than they do
- Failing to account for margin interest as a drag on returns — at 7-8% margin rates, the hurdle rate for margined positions is substantial
- Relying on Reg T buying power without monitoring maintenance levels — a position can be purchased within buying power but quickly trigger a maintenance call after a decline
- Assuming portfolio margin is always more favorable — concentrated, unhedged positions may receive similar or higher margin under portfolio margin stress tests
- Not planning for margin call deadlines — margin calls arrive during market stress when the client is least likely to have available cash
- Treating SBLOC as "free" liquidity — a market decline can trigger a collateral call simultaneously with the investment losses, creating a double impact
- Liquidating positions for margin calls without considering tax consequences — forced sales may realize gains or losses at inopportune times
- Pattern day trader margin surprise — accounts can be reclassified as pattern day trader and face the $25,000 minimum equity requirement unexpectedly
- Ignoring correlation between margin calls and market stress — the client's ability to deposit cash may be impaired at exactly the time a margin call demands it
- Assuming the firm must contact the client before liquidation — the firm has the right to liquidate margin-deficient accounts without prior notice or client consent
- Overlooking the purpose/non-purpose distinction in SBLOCs — using non-purpose loan proceeds to buy securities violates Regulation U and can result in regulatory action

## Regulatory Reference Summary

| Regulation / Rule | Authority | Scope |
|-------------------|-----------|-------|
| Regulation T | Federal Reserve | Initial margin for broker-dealer credit |
| Regulation U | Federal Reserve | Credit by banks secured by margin stock |
| FINRA Rule 4210 | FINRA | Maintenance margin, portfolio margin, day-trade margin |
| SEC Rule 15c3-3 | SEC | Customer protection, segregation of funds |
| FINRA Rule 4521 | FINRA | Margin reporting requirements to FINRA |
| OCC TIMS | OCC | Theoretical pricing model for portfolio margin |

## Cross-References
- **order-lifecycle** (Layer 11): Margin requirements are checked as part of the order validation and pre-trade process
- **trade-execution** (Layer 11): Forced liquidation requires best execution compliance even under time pressure
- **settlement-clearing** (Layer 11): Margin is settled as part of the trade settlement process; fails can trigger margin obligations
- **lending** (Layer 6): SBLOC products overlap with personal lending analysis; HELOC vs SBLOC comparison
- **liquidity-management** (Layer 6): Margin calls create sudden liquidity demands that must be anticipated in cash flow planning
- **pre-trade-compliance** (Layer 9): Pre-trade margin checks prevent orders that would exceed margin capacity
- **operational-risk** (Layer 9): Margin system failures, forced liquidation errors, and call processing breakdowns are key operational risks
- **counterparty-risk** (Layer 3): Margin lending creates counterparty exposure between the firm and the client
- **investment-suitability** (Layer 9): Margin accounts and leverage strategies require suitability assessment
- **diversification** (Layer 4): Concentrated position margin requirements reinforce diversification principles
