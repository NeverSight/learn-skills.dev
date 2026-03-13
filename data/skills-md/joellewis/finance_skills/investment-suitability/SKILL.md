---
name: investment-suitability
description: "Assess investment suitability obligations under FINRA Rules 2111 and 2090 across all three suitability prongs. Use when the user asks about reasonable-basis, customer-specific, or quantitative suitability, product-specific concerns for complex products, leveraged ETFs, variable annuities, or alternatives, household-level suitability, hold recommendations, or the institutional suitability exemption. Also trigger when users mention 'is this investment suitable', 'turnover ratio is too high', 'cost-to-equity ratio', 'churning metrics', 'suitability questionnaire design', 'complex product due diligence', 'customer refused to provide their risk tolerance', or ask whether a recommendation fits a customer's profile."
---

# Investment Suitability

## Purpose
Guide the assessment of investment suitability obligations under FINRA rules and related standards. This skill covers the three suitability obligations, the required customer profile elements, product-specific suitability concerns, household-level considerations, and enforcement patterns — enabling a user or agent to identify where suitability problems may arise in recommendation workflows.

## Layer
9 — Compliance & Regulatory Guidance

## Direction
prospective

## When to Use
- Evaluating whether a recommendation is suitable for a specific customer
- Designing recommendation engines, suitability questionnaires, or account review processes
- Assessing product-specific suitability concerns (complex products, alternatives, leveraged ETFs, variable annuities)
- Reviewing account-level vs household-level suitability
- Understanding where Reg BI has raised the bar beyond traditional suitability
- Evaluating hold recommendations or account type recommendations for suitability
- Assessing institutional suitability exemption applicability
- Reviewing for quantitative suitability (excessive trading) concerns

## Core Concepts

### FINRA Rule 2111 — Suitability
The foundational rule requiring that a broker-dealer or associated person have a reasonable basis for believing a recommendation is suitable for the customer. Applies to recommendations of securities and investment strategies involving securities, including recommendations to hold. Three distinct obligations arise from Rule 2111:

### Three Suitability Obligations

**1. Reasonable-Basis Suitability (Rule 2111.05(a))**
The firm or associated person must perform reasonable diligence to understand the nature of the recommended security or strategy, including its risks, rewards, and features. This is a product-level obligation — the representative must understand what they are recommending before recommending it to anyone. A representative who does not understand a complex product cannot satisfy reasonable-basis suitability regardless of how well it might fit a particular customer.

**2. Customer-Specific Suitability (Rule 2111.05(b))**
The recommendation must be suitable for the particular customer based on that customer's investment profile. The investment profile includes, but is not limited to: age, other investments, financial situation and needs, tax status, investment objectives, investment experience, investment time horizon, liquidity needs, risk tolerance, and any other information the customer discloses.

**3. Quantitative Suitability (Rule 2111.05(c))**
A person with actual or de facto control over a customer account must have a reasonable basis for believing that a series of recommended transactions, even if each is individually suitable, is not excessive and unsuitable when taken together in light of the customer's investment profile. Key metrics: turnover ratio (annualized), cost-to-equity ratio, and use of in-and-out trading patterns. Generally, turnover ratios above 6 and cost-to-equity ratios above 20% raise presumptive concerns.

### FINRA Rule 2090 — Know Your Customer
Requires every member to use reasonable diligence to know and retain the essential facts concerning every customer and the authority of each person acting on the customer's behalf. This is the foundation that feeds suitability analysis — you cannot assess suitability without first knowing the customer. Essential facts include identity, financial status, investment objectives, and the nature and type of account.

### Suitability Profile Factors
The customer investment profile under Rule 2111 includes:
- **Age** — affects time horizon, risk capacity, and product suitability
- **Financial situation and needs** — income, net worth, liquid net worth, expenses, liabilities
- **Tax status** — marginal tax bracket, tax-deferred vs taxable accounts
- **Investment objectives** — capital preservation, income, growth, speculation
- **Investment time horizon** — short-term (<3 years), intermediate (3-10), long-term (>10)
- **Liquidity needs** — anticipated cash needs, emergency reserves
- **Risk tolerance** — willingness and capacity to bear losses
- **Investment experience** — familiarity with securities types, strategies, and risks
- **Other investments** — existing portfolio holdings, concentration risk, held-away assets

A customer may decline to provide profile information, but the firm must document the refusal and recognize that the more information withheld, the narrower the range of suitable recommendations.

### Product-Specific Suitability Concerns

**Complex Products:** FINRA Regulatory Notice 12-03 provides heightened suitability guidance for complex products (structured products, leveraged/inverse ETFs, hedge funds, non-traded REITs). Firms must perform heightened reasonable-basis diligence, develop targeted training, and consider whether enhanced customer-specific suitability review is needed.

**Leveraged and Inverse ETFs:** These products reset daily, meaning their performance over periods longer than one day can deviate significantly from the leveraged/inverse benchmark return. FINRA has flagged that these are generally unsuitable for buy-and-hold investors. Suitability analysis must account for the daily reset mechanism and its compounding effects.

**Variable Annuities:** Subject to FINRA Rule 2330, which imposes heightened suitability requirements. Before recommending a VA, the representative must consider: liquidity needs (surrender charges typically 5-8 years), tax status (tax-deferred growth is redundant in an IRA), subaccount investment options, rider costs and benefits, and whether a 1035 exchange is in the customer's interest.

**Options:** FINRA Rule 2360 requires account-level approval before options trading, with suitability assessed across strategy tiers (covered writing, spreads, uncovered writing, etc.). The Options Disclosure Document (ODD) must be delivered before account approval.

**Alternative Investments:** Private placements, hedge funds, and non-traded products present heightened suitability concerns due to illiquidity, complexity, high fees, and limited transparency. FINRA expects enhanced due diligence on the product issuer and heightened customer-specific suitability review.

### Household vs Account-Level Suitability
Suitability is assessed at the customer level, not the account level, but household context matters. A concentrated position in one account may be suitable if diversified across the household. However, firms must have a reasonable basis for knowing the household context — relying on assumptions about held-away assets without verification creates risk. FINRA expects firms to consider a customer's overall financial picture to the extent it is known or reasonably discoverable.

### The Hold Recommendation
Since the 2020 amendment to Rule 2111, an explicit recommendation to hold a security is a recommendation subject to suitability obligations. This closed a longstanding gap where representatives could avoid suitability review by recommending inaction. A hold recommendation on a concentrated or illiquid position must be evaluated against the customer's current profile.

### Institutional Suitability Exemption (Rule 2111.07)
The customer-specific suitability obligation may be modified for institutional accounts (as defined in FINRA Rule 4512(c)) if: (1) the firm has a reasonable basis to believe the institutional customer is capable of evaluating investment risks independently, and (2) the institutional customer affirmatively indicates it is exercising independent judgment. Both conditions must be met — the exemption is not automatic for all institutional clients.

### Reg BI's Elevation Beyond Suitability
Since June 30, 2020, broker-dealer recommendations to retail customers are governed by Regulation Best Interest (Reg BI), which imposes a higher standard than FINRA suitability. Reg BI's Care Obligation requires consideration of reasonably available alternatives and a cost-benefit analysis — obligations that go beyond traditional suitability. FINRA suitability remains relevant for institutional clients and as a component of the Reg BI framework. See the **reg-bi** skill for full Reg BI coverage.

### Enforcement Patterns
FINRA disciplinary actions frequently target:
- Recommending complex products without understanding them (reasonable-basis failures)
- Recommending concentrated positions to risk-averse or elderly customers
- Excessive trading in discretionary or de facto controlled accounts
- Failure to update customer profiles after material life changes
- Ignoring red flags (customer complaints, account losses inconsistent with stated objectives)
- VA exchanges that serve the representative's commission interest but not the customer's investment interest

## Worked Examples

### Example 1: Concentrated position recommended to a retiree
**Scenario:** A registered representative recommends that a 72-year-old retired client invest 60% of her $500,000 IRA in a single technology stock. The client's investment objective is listed as "income" with a "moderate" risk tolerance. She relies on the account for living expenses.
**Compliance Issues:** Customer-specific suitability violation. The recommendation creates concentration risk inconsistent with income objectives, moderate risk tolerance, short time horizon (income-dependent), and high liquidity needs. Age is a significant factor — the client has limited ability to recover from a loss.
**Analysis:** The representative should have recommended a diversified income-oriented portfolio consistent with the stated objectives. Even if the client expressed enthusiasm for the stock, the representative has an independent obligation to assess suitability and document the rationale. FINRA would likely view this as a customer-specific suitability violation and potentially a supervision failure if the firm lacked exception reporting for concentration.

### Example 2: Complex product recommended without adequate understanding
**Scenario:** A representative recommends a leveraged inverse ETF to a moderate-risk client as a "hedge" against market declines, suggesting the client hold it for six months. The representative cannot explain the daily reset mechanism or the compounding effects over multi-day holding periods.
**Compliance Issues:** Reasonable-basis suitability violation. The representative does not understand the product's key feature (daily reset) and is recommending a holding period inconsistent with the product's design. Additionally, customer-specific suitability is questionable for a moderate-risk investor.
**Analysis:** FINRA Regulatory Notice 09-31 specifically warns that leveraged/inverse ETFs that reset daily are typically unsuitable for retail investors who plan to hold them longer than one trading session. The representative's inability to explain the reset mechanism is a clear reasonable-basis failure. The firm should have product-specific training requirements and suitability guardrails for leveraged ETF recommendations.

### Example 3: Excessive trading in a discretionary account
**Scenario:** A representative with discretionary authority over a client's $200,000 account executes 150 trades over 12 months, generating $46,000 in commissions. The account's annualized turnover ratio is 8.2 and the cost-to-equity ratio is 23%. The client's objective is "growth" with a "moderate-to-aggressive" risk tolerance.
**Compliance Issues:** Quantitative suitability violation. The turnover ratio (8.2 > 6 threshold) and cost-to-equity ratio (23% > 20% threshold) both exceed presumptive thresholds for excessive trading. The representative has de facto control through discretionary authority.
**Analysis:** Even though individual trades may have been suitable, the pattern of trading is excessive in the aggregate. The account must generate returns exceeding 23% just to break even after costs — an unreasonable hurdle. FINRA would examine control (established through discretion), excessive activity (quantitative metrics), and scienter (representative's awareness that trading was excessive). The firm's supervision system should have flagged this through exception reporting on turnover and cost-to-equity ratios.

## Common Pitfalls
- Treating suitability as a one-time assessment at account opening — it must be reassessed with each recommendation and when circumstances change
- Confusing account-level suitability with customer-level suitability — the customer's full financial picture matters
- Recommending complex products without completing reasonable-basis diligence on the product
- Failing to document the rationale for recommendations, especially for higher-risk or concentrated positions
- Ignoring the hold recommendation obligation — advising a client to maintain a concentrated or unsuitable position is itself a recommendation
- Assuming institutional clients are automatically exempt from customer-specific suitability — both prongs of Rule 2111.07 must be satisfied
- Not updating customer profiles after life events (retirement, inheritance, divorce, job loss)
- Applying suitability standards when Reg BI's higher standard applies to retail customers
- Overlooking quantitative suitability in accounts with high activity but no single unsuitable trade
- Failing to consider tax status — recommending tax-deferred products (VAs) in already tax-deferred accounts (IRAs) without justification

## Cross-References
- **reg-bi** (Layer 9): Higher standard for BD recommendations to retail customers; supersedes suitability for retail
- **know-your-customer** (Layer 9): KYC obligations provide the customer profile that feeds suitability analysis
- **fiduciary-standards** (Layer 9): IA fiduciary duty parallel; different standard, similar customer-interest focus
- **investment-policy** (Layer 5): IPS constraints (time horizon, risk tolerance, liquidity) map directly to suitability factors
- **sales-practices** (Layer 9): Churning/excessive trading enforcement overlaps with quantitative suitability
- **conflicts-of-interest** (Layer 9): Compensation conflicts can drive unsuitable recommendations
- **tax-loss-harvesting** (wealth-management plugin, Layer 5): replacement securities selected during TLH must still satisfy suitability requirements
