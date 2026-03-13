---
name: post-trade-compliance
description: "Guide post-trade compliance monitoring and trade surveillance system design. Use when building alert logic to detect churning, front-running, cherry-picking, layering, spoofing, wash trading, or marking the close, implementing post-trade best execution review, evaluating allocation fairness with pro-rata verification or dispersion analysis, designing exception-based monitoring workflows with escalation paths, correlating trading with MNPI events for insider trading detection, building personal trading surveillance for preclearance and blackout enforcement, determining SAR or blue sheet or CAT reporting triggers, or tuning surveillance thresholds to reduce false positives. Also covers turnover ratios, cost-to-equity ratios, and investigation case management."
---

# Post-Trade Compliance

## Purpose
Guide the design and implementation of post-trade compliance monitoring and trade surveillance systems. Covers trade surveillance pattern detection, best execution review, allocation fairness analysis, exception-based monitoring workflows, insider trading detection, market manipulation surveillance, and regulatory reporting triggers. Enables building systems that detect compliance violations after execution and satisfy ongoing surveillance obligations.

## Layer
11 — Trading Operations (Order Lifecycle & Execution)

## Direction
retrospective

## When to Use
- Designing or enhancing a trade surveillance program for a broker-dealer or investment adviser
- Building alert logic to detect churning, front-running, cherry-picking, or other prohibited trading patterns
- Implementing post-trade best execution review processes and quarterly committee reporting
- Evaluating allocation fairness across accounts, including pro-rata verification and dispersion analysis
- Designing exception-based monitoring workflows with alert generation, investigation, escalation, and disposition
- Detecting insider trading patterns by correlating trading activity with material non-public information events
- Identifying market manipulation behaviors such as layering, spoofing, wash trading, and marking the close
- Building personal trading surveillance systems for employee preclearance, holding periods, and blackout enforcement
- Determining when post-trade activity triggers regulatory reporting obligations (SAR, 13H, blue sheets, CAT)
- Tuning surveillance alert thresholds to balance detection sensitivity against false positive rates
- Preparing surveillance documentation and case files for regulatory examinations
- Establishing SLA-driven investigation workflows with aging dashboards and escalation paths

## Core Concepts

### Trade Surveillance Framework
Trade surveillance is the systematic, ongoing monitoring of executed transactions to detect potential violations of securities laws, firm policies, and regulatory rules. A surveillance program operates across multiple time horizons:

- **T+0 (same-day) monitoring** — Real-time or end-of-day reviews targeting time-sensitive patterns such as front-running (trading ahead of a customer block order), late trading (mutual fund orders placed after the 4:00 p.m. ET NAV pricing cutoff), and marking the close (orders placed to influence the closing price). T+0 alerts require immediate investigation because the regulatory harm is ongoing or the evidence window is narrow.
- **T+1 through T+3 monitoring** — Next-day and settlement-window reviews for patterns that emerge across a short sequence of events: allocation fairness on block trades, partial fill distribution, and settlement failures. These alerts align with the trade settlement cycle and CAT error correction windows.
- **T+N rolling-window monitoring** — Longer-horizon reviews (weekly, monthly, quarterly) for patterns that only become visible over time: churning and excessive trading (turnover ratios measured over months), coordinated trading across accounts, systematic favoritism in allocations, and insider trading correlations (trading patterns around earnings announcements or M&A events). Rolling windows must be calibrated to the specific pattern — churning detection typically requires 3-12 months of data, while insider trading correlation windows may span 30-90 days around a material event.

**Surveillance scope** varies by firm type and business activity. A full-service broker-dealer conducting equities, fixed income, and derivatives trading must maintain surveillance across all asset classes. An RIA managing model portfolios may focus surveillance on allocation fairness, best execution, and personal trading. The surveillance program must cover both customer/client accounts and proprietary/firm accounts.

**Alert generation** is the process of applying quantitative thresholds, pattern matching rules, or scoring models to transaction data to produce alerts requiring human review. Effective alert generation requires clean, normalized data from multiple sources: order management systems, execution management systems, account master data, market data, and — for insider trading detection — corporate event calendars and restricted lists.

**Investigation workflow** follows a standard lifecycle:

1. Alert generation
2. Initial triage and prioritization
3. Investigation and fact gathering
4. Disposition (close with no finding, close with finding, escalate)
5. Escalation to senior compliance or legal
6. Regulatory filing if warranted (SAR, STR, or self-report)

Each stage must be documented in a case management system with timestamps, analyst notes, evidence, and supervisory sign-off.

**Disposition and escalation** decisions are among the most consequential in a compliance program. A disposition of "no finding" must be supported by documented analysis — regulators will review closed alerts during examinations. Escalation criteria should be defined in written procedures: escalate when the pattern is consistent with a securities law violation, when the activity involves a senior person or high-risk account, when the dollar amount exceeds a defined threshold, or when a pattern recurs after a prior warning.

**Regulatory filing triggers** — Post-trade surveillance may identify activity that requires a SAR filing (for broker-dealers and, effective January 1, 2026, covered investment advisers), an STR (Suspicious Transaction Report, the international equivalent under FATF standards), or a self-report to FINRA or the SEC. The decision to file a SAR based on surveillance findings must be made by the AML Compliance Officer in coordination with the surveillance team. The SAR tipping-off prohibition (31 U.S.C. Section 5318(g)(2)) applies — the subject of the surveillance alert must not be informed of a SAR filing.

### Pattern Detection
Surveillance systems must be designed to detect specific prohibited trading patterns. Each pattern has distinct data requirements, detection logic, and evidentiary standards:

**Churning / excessive trading** — Quantitative metrics include turnover ratio (aggregate purchases divided by average equity, with ratios above 6 presumptively excessive), cost-to-equity ratio (annualized costs as a percentage of average equity, with ratios above 20% generally excessive), and in-and-out trading frequency. Detection requires account-level transaction history, commission and fee data, and the customer's stated investment objectives. Churning surveillance is typically run on a rolling 3-12 month window.

**Front-running** — Trading in a firm or personal account ahead of a pending customer order that is expected to move the market. Detection requires correlating proprietary/personal trading activity with the timestamps of customer order receipt and execution. Key data elements: order receipt time (from CAT or order management system), execution time, account ownership, and the direction and size of the customer order. Front-running alerts are time-sensitive and should be generated on T+0 or T+1.

**Cherry-picking (favorable allocations)** — A pattern where an adviser or trader allocates profitable trades to favored accounts and unprofitable trades to disfavored accounts. Detection involves comparing the performance of allocations across accounts within a block trade or across trades over time. Statistical methods include comparing average returns by account against the expected distribution under fair allocation. Cherry-picking is a form of fraud that violates fiduciary duty and Section 10(b) of the Exchange Act.

**Insider trading** — Trading by persons with access to material non-public information (MNPI) ahead of corporate events such as earnings announcements, M&A transactions, FDA approvals, or regulatory actions. Detection requires correlating trading activity with an events calendar and identifying trades that are unusual in timing, size, or profitability relative to the trader's historical pattern. Insider trading surveillance often relies on restricted list and watch list monitoring, where securities of companies about which the firm possesses MNPI are placed on restricted or watch lists and trading activity is monitored or prohibited.

**Layering / spoofing** — Placing non-bona fide orders on one side of the order book to create a false impression of supply or demand, then executing on the opposite side and canceling the layered orders. Detection requires order-level data (not just executions) including order submissions, modifications, and cancellations with timestamps. Key indicators: high order-to-execution ratios, rapid cancellation patterns, and consistent profitability on the execution side when layered orders are present.

**Wash trading** — Simultaneously or near-simultaneously buying and selling the same security with no change in beneficial ownership, creating the appearance of market activity. Detection involves identifying offsetting transactions in the same security, same account (or related accounts), within a narrow time window. Wash trading can also occur across accounts controlled by the same beneficial owner.

**Marking the close** — Placing orders near the end of the trading session to influence the closing price. Detection requires analyzing order timestamps relative to market close, particularly for securities where the closing price affects portfolio valuations, options settlements, or performance calculations. Key indicator: late-session orders in securities where the firm or its clients have a valuation interest.

**Coordinated trading** — Multiple accounts trading the same securities in the same direction within a narrow time window, suggesting coordination or common direction. Detection involves clustering analysis across accounts by security, direction, and time, particularly when the accounts share a common adviser, trader, or beneficial owner.

**Late trading** — Submitting mutual fund orders after the 4:00 p.m. ET NAV pricing cutoff but receiving the current day's NAV. Detection requires comparing order entry timestamps with the 4:00 p.m. cutoff, with attention to time zone differences, system clock accuracy, and any manual order entry processes that could allow backdating.

### Best Execution Review
Best execution is the obligation to seek the most favorable terms reasonably available for client transactions. Post-trade best execution review measures execution quality after the fact and identifies systematic deficiencies.

**Benchmark comparison** — Each execution is compared against one or more benchmarks to measure quality. Common benchmarks include:

- **VWAP (Volume-Weighted Average Price)** — The average price weighted by volume over a defined period (typically the trading day). Executions below VWAP (for buys) or above VWAP (for sells) indicate favorable execution.
- **Arrival price** — The mid-quote at the time the order was received. Measures the cost of execution relative to the decision price, capturing both market impact and timing cost.
- **Closing price** — Used primarily for orders benchmarked to end-of-day pricing, such as index fund rebalancing.
- **Implementation shortfall** — The difference between the portfolio's paper return (using decision prices) and the actual return (using execution prices), capturing all explicit and implicit costs of execution.

**Outlier detection** — Identify executions that deviate significantly from the benchmark. Common approaches: flag executions more than a defined number of standard deviations from the mean benchmark deviation, or flag executions where the deviation exceeds a basis-point threshold (e.g., more than 50 basis points worse than VWAP). Outlier thresholds must be calibrated by asset class, order size, and market conditions — a 50 bps deviation may be normal for a small-cap equity but alarming for a large-cap liquid name.

**Venue analysis** — Compare execution quality across venues (exchanges, ATSs, market makers, OTC dealers) to determine whether the firm's order routing is systematically achieving best execution. Metrics include effective spread, fill rate, speed of execution, and price improvement. Venue analysis should account for order flow characteristics — routing difficult orders to one venue and easy orders to another will skew venue-level statistics.

**Systematic review program** — Regulation NMS, FINRA rules, and the SEC's interpretive guidance require broker-dealers to conduct regular and rigorous reviews of execution quality. Most firms conduct quarterly reviews with formal committee reporting and an annual comprehensive review. The review should cover:

- Execution quality statistics by security type, order size, and venue
- Changes in market structure that may affect execution quality
- Assessment of routing logic and smart order router performance
- Evaluation of whether the firm's execution arrangements (payment for order flow, internalization, affiliated venue routing) are consistent with best execution obligations

**Best execution committee** — Many firms establish a formal best execution committee composed of representatives from trading, compliance, technology, and senior management. The committee meets quarterly to review execution quality data, evaluate routing arrangements, approve changes to routing logic, and document its findings. Committee minutes serve as key evidence of the firm's best execution compliance during regulatory examinations.

### Allocation Fairness
When a single order is executed on behalf of multiple accounts (a block trade), the resulting executions must be allocated fairly. Allocation fairness monitoring detects systematic patterns of favoritism.

**Pro-rata allocation verification** — The standard method for block trade allocation is pro rata, where each participating account receives shares in proportion to its intended participation. Post-trade monitoring verifies that actual allocations match the pro-rata methodology by comparing each account's allocation percentage to its intended participation percentage. Deviations must be documented and justified (e.g., rounding, minimum lot sizes, odd-lot avoidance).

**Dispersion analysis** — Measures the distribution of execution prices across accounts within a block trade. In a fair allocation, all accounts should receive approximately the same average execution price. Dispersion analysis flags block trades where certain accounts received systematically better prices than others. The analysis should account for legitimate reasons for dispersion, such as different allocation methods (average price vs. sequential fill) and account-level constraints.

**Systematic favoritism detection** — Extends cherry-picking analysis across time to detect patterns where specific accounts consistently receive more favorable allocations. Statistical approaches include:

1. Comparing each account's average allocation quality (measured as deviation from benchmark) against the group mean over a rolling period
2. Rank-ordering accounts by allocation quality and testing whether the ranking is correlated with account type (e.g., proprietary accounts, performance-fee accounts, or accounts of firm principals)
3. Regression analysis testing whether account characteristics predict allocation quality after controlling for order characteristics

**IPO allocation rules** — FINRA Rules 5130 and 5131 restrict the allocation of new issues (IPOs, secondary offerings) to certain persons, including broker-dealer personnel, portfolio managers, and their immediate family members. Post-trade surveillance must verify that IPO allocations do not flow to restricted persons. Rule 5131 also prohibits quid pro quo allocations (conditioning allocations on the receipt of excessive compensation) and spinning (allocating hot IPOs to executives of investment banking clients).

**Trade rotation monitoring** — For firms that use a rotation system (where the first account to receive an allocation rotates across trades), post-trade monitoring verifies that the rotation is being followed. Deviations from the rotation schedule should be flagged and investigated.

**Partial fill allocation** — When a block order is only partially filled, the partial fill must be allocated fairly. Post-trade monitoring verifies that partial fills are allocated pro rata (or according to the firm's stated methodology) rather than being concentrated in favored accounts. Partial fill allocation is a common area of cherry-picking because partial fills on profitable trades are particularly valuable.

### Exception-Based Monitoring
Exception-based monitoring is the operational framework for managing the volume of alerts generated by surveillance systems.

**Alert tuning** — Surveillance systems generate alerts based on thresholds and rules. Alert tuning is the ongoing process of adjusting these parameters to optimize the trade-off between sensitivity (catching real violations) and specificity (minimizing false positives). A system that generates too many false positives overwhelms investigators and leads to alert fatigue, causing real violations to be missed. A system that is too conservative misses violations. Tuning involves analyzing historical alert data: review disposition outcomes (what percentage of alerts resulted in findings?), adjust thresholds based on statistical analysis, and implement machine learning or scoring models to prioritize alerts by risk.

**Alert prioritization** — Not all alerts are equally urgent or significant. Prioritization frameworks assign risk scores based on factors such as:

- The severity of the potential violation (insider trading is more serious than a minor allocation deviation)
- The dollar amount involved
- The account type (customer, proprietary, employee)
- The individual involved (senior personnel, repeat offenders)
- The time sensitivity (front-running requires immediate review)

High-priority alerts should be routed to senior investigators with defined response-time SLAs.

**Investigation workflow** — The standard investigation lifecycle is:

1. **Alert receipt** — the alert is generated and assigned to an investigator.
2. **Initial triage** — the investigator reviews the alert details and determines whether the alert warrants a full investigation or can be closed as a known false positive. Triage decisions must be documented.
3. **Full investigation** — the investigator gathers additional evidence: transaction records, communications (email, chat, phone records), account documentation, market data, and any relevant context (was the security on a restricted list? was there a pending corporate event?).
4. **Disposition** — the investigator documents findings and recommends a disposition: close with no finding, close with finding and corrective action, or escalate.
5. **Supervisory review** — a senior compliance officer reviews the investigation and approves the disposition.
6. **Escalation** — if warranted, the matter is escalated to the CCO, legal counsel, or senior management for determination of whether regulatory reporting or disciplinary action is required.

**Aging and SLA management** — Alerts must be investigated within defined timeframes. SLAs should be tiered by priority:

- High-priority alerts: within 2-5 business days
- Medium-priority alerts: within 10 business days
- Low-priority alerts: within 20 business days

An aging dashboard tracks open alerts against SLAs and flags overdue items. Persistent SLA breaches indicate insufficient staffing, poor alert tuning, or systemic workflow issues. Regulators expect that firms can demonstrate timely disposition of alerts — an examination finding of hundreds of unreviewed aged alerts is a serious supervisory deficiency.

**Alert documentation** — Every alert must be documented from generation through disposition. Documentation must include: the alert details (trigger, threshold, data), the investigator's analysis, evidence reviewed, disposition rationale, supervisory approval, and any follow-up actions. Documentation serves two purposes: it creates an examination-ready audit trail, and it provides data for alert tuning and program assessment.

### Personal Trading Surveillance
Firms must monitor the personal securities trading of employees, officers, and access persons to prevent conflicts of interest and insider trading.

**Employee trading monitoring** — Firms must receive and review reports of personal securities transactions by access persons. Under SEC Rule 204A-1 (for investment advisers) and FINRA rules (for broker-dealers), access persons must report holdings and transactions. Surveillance systems compare employee trading against restricted lists, watch lists, and client trading activity to detect potential front-running or trading on MNPI.

**Preclearance verification** — Many firms require employees to obtain preclearance before executing personal trades. Post-trade surveillance verifies that all personal trades were precleared by comparing executed trades against preclearance records. Trades executed without preclearance — or trades that differ from the precleared terms (different security, larger size, different direction) — must be flagged and investigated.

**Holding period compliance** — Firm codes of ethics commonly impose minimum holding periods (e.g., 30 or 60 days) to discourage short-term speculative trading that could conflict with client interests. Post-trade surveillance monitors buy-sell intervals for personal accounts and flags violations.

**Blackout period enforcement** — During blackout periods (typically around earnings announcements, fund portfolio rebalancing, or when the firm possesses MNPI about a security), employees are prohibited from trading the affected securities. Surveillance systems must cross-reference personal trading against active blackout periods and restricted lists.

**Reporting deadline monitoring** — Access persons must file:

- Initial holdings reports within 10 days of becoming an access person
- Annual holdings reports within 45 days of the reporting period end
- Quarterly transaction reports within 30 days of quarter end

Surveillance systems track filing compliance and flag late or missing reports.

### Regulatory Reporting Triggers
Post-trade surveillance activities may identify conditions that trigger specific regulatory reporting obligations.

**SAR filing thresholds** — Broker-dealers must file SARs for transactions of $5,000 or more that the firm knows, suspects, or has reason to suspect involve illegal activity, BSA evasion, or no apparent lawful purpose (31 CFR Section 1023.320). Post-trade surveillance findings — such as wash trading, layering, or unusual trading patterns with no economic rationale — may satisfy the suspicion element. The decision to file rests with the AML Compliance Officer, and the SAR tipping-off prohibition applies. Effective January 1, 2026, covered investment advisers are also subject to SAR filing requirements under the FinCEN final rule.

**Large trader reporting (Form 13H)** — Post-trade analysis may identify accounts or persons whose aggregate trading activity meets the large trader thresholds (2 million shares or $20 million in a single day, or 20 million shares or $200 million in a calendar month). Broker-dealers must monitor for customers who meet the threshold but have not self-identified with an LTID, and must maintain transaction records for all large trader accounts.

**Blue sheet requests** — Although blue sheet requests originate from the SEC, a firm's post-trade surveillance system must be capable of extracting and producing the required transaction data (customer identity, account, security, date, price, quantity, capacity) within the SEC's specified timeframe. Firms that discover potential issues during blue sheet preparation (e.g., trading by restricted persons, unreported large trader activity) should evaluate whether self-reporting is appropriate.

**CAT reporting obligations** — All reportable events in the order lifecycle — origination, routing, modification, cancellation, execution, and allocation — must be reported to CAT by 8:00 a.m. ET on T+1. Post-trade compliance processes must verify that CAT submissions are accurate and complete, and that errors are corrected within T+3.

**TRACE reporting (fixed income)** — OTC transactions in TRACE-eligible fixed income securities must be reported within 15 minutes of execution. Post-trade monitoring should verify that TRACE reports are timely and accurate, and flag late reports for remediation.

**Short interest reporting** — FINRA Rule 4560 requires semi-monthly reporting of short positions. Post-trade systems must accurately track and report short positions as of the designated settlement dates.

### Surveillance Technology
Effective post-trade compliance requires robust technology infrastructure.

**Data requirements** — Surveillance systems consume data from multiple sources:

- Order management systems (order details, timestamps, account identifiers)
- Execution management systems (fill prices, quantities, venues)
- Account master data (customer profiles, investment objectives, account type, relationships)
- Market data (prices, volumes, benchmarks)
- Corporate events data (earnings dates, M&A announcements, FDA actions)
- Communications data (email, chat, voice)
- Reference data (restricted lists, watch lists, employee rosters)

Data completeness and timeliness are foundational — surveillance analytics are only as good as the input data.

**Data normalization** — Transaction data from multiple source systems must be normalized to a common schema:

- Consistent security identifiers (mapping between CUSIPs, ISINs, tickers, and internal identifiers)
- Standardized timestamps (UTC or a single reference timezone with millisecond precision)
- Uniform account identifiers (mapping across systems that may use different account numbering)
- Consistent trade type classifications (buy, sell, short sale, cover)

Normalization failures are a leading cause of surveillance system false positives and missed detections.

**Analytics and scoring models** — Modern surveillance systems use a combination of rule-based alerts (threshold breaches, pattern matches) and statistical/machine learning models (anomaly detection, behavioral scoring). Rule-based alerts are transparent and auditable but rigid. Statistical models can detect novel patterns but require careful validation and explainability for regulatory purposes. A hybrid approach — using models to score and prioritize alerts generated by rules — is increasingly common. All models must be documented, validated, and subject to periodic review.

**Case management** — A case management system tracks each alert through its lifecycle: assignment, investigation, evidence attachment, disposition, supervisory review, and closure. The system must support workflow routing, SLA tracking, escalation, audit trails, and reporting. Case management data is the primary artifact reviewed during regulatory examinations of a firm's surveillance program.

**Regulatory examination support** — Surveillance systems must be able to produce examination-ready reports: alert volumes and disposition statistics, investigation timelines and outcomes, tuning history and rationale, coverage analysis (which patterns are monitored, which are not and why), and sample case files demonstrating the quality of investigations. Regulators — particularly the SEC's Division of Examinations and FINRA's Market Regulation department — evaluate not just whether a firm has a surveillance program, but whether it is effective, adequately staffed, and responsive to identified issues.

## Worked Examples

### Example 1: Building a Trade Surveillance Program for a Mid-Size Broker-Dealer

**Scenario:** A broker-dealer with 120 registered representatives, $8 billion in customer assets, and business lines spanning equities, fixed income, and listed options is building a formal trade surveillance program. The firm currently relies on ad hoc supervisory review and basic exception reports (concentration, large trades) but has no systematic surveillance for manipulative trading patterns. FINRA's most recent examination identified the absence of structured surveillance as a deficiency.

**Step 1 — Scope and risk assessment.**

The surveillance program must cover the firm's entire business: equity trading (agency and principal), fixed income (corporate and municipal bonds), and listed options. Begin with a risk assessment mapping each business line to the applicable manipulative trading patterns:

- For equities: front-running, churning, wash trading, marking the close, layering/spoofing, insider trading, coordinated trading
- For fixed income: excessive markups/markdowns, interpositioning, trading ahead of customer orders, best execution deviations
- For options: front-running using options, manipulation of underlying securities to affect options values, and unauthorized options trading beyond approved strategy levels

**Step 2 — Data infrastructure.**

Inventory all data sources: the order management system (order timestamps, account IDs, security IDs, order terms), the execution platform (fill prices, quantities, venues, counterparties), the account master (customer profiles, investment objectives, risk tolerance, account type), market data feeds (prices, volumes, index levels, benchmark rates), and the firm's restricted and watch lists.

Identify gaps: Does the OMS capture order receipt time with sufficient precision for front-running detection? Are account relationships (households, common beneficial owners) mapped for coordinated trading analysis? Are fixed income markup calculations available for post-trade review? Remediate data gaps before deploying surveillance analytics.

**Step 3 — Alert design and calibration.**

For each pattern identified in the risk assessment, design alert logic with quantitative thresholds:

- **Churning:** Flag accounts where the annualized turnover ratio exceeds 4 or the cost-to-equity ratio exceeds 12% on a rolling 6-month window. Set a higher threshold (turnover > 6, cost-to-equity > 20%) for immediate escalation. Exclude accounts with documented active trading mandates.
- **Front-running:** Correlate proprietary and employee account trades with customer block orders received within the preceding 60 minutes. Flag instances where the direction matches, the customer order is large enough to move the market (e.g., greater than 10% of average daily volume), and the employee or proprietary trade precedes the customer execution.
- **Marking the close:** Flag orders entered in the last 10 minutes of the trading session in securities where the firm or its clients hold positions sensitive to the closing price (e.g., options positions, performance-fee calculations, mutual fund NAV determinations). Require that the flagged order exceeds 5% of the final-10-minute volume for the security.
- **Wash trading:** Identify buy-sell pairs in the same security, same account (or related accounts), within a 5-minute window, with no change in net position. Also monitor cross-account wash patterns among accounts sharing a common beneficial owner or adviser.
- **Insider trading:** Correlate trading in securities appearing on the firm's watch list (securities for which the firm may possess MNPI due to investment banking or advisory relationships) with material corporate events occurring within 30 days after the trade. Flag trades by employees, their households, and accounts over which the firm exercises discretion.

**Step 4 — Investigation workflow and staffing.**

Establish a tiered investigation workflow. Assign two full-time surveillance analysts and a senior compliance officer to oversee the program. Define SLAs: high-priority alerts (front-running, insider trading) investigated within 3 business days; medium-priority (churning, marking the close) within 10 business days; low-priority (minor allocation deviations) within 20 business days. Implement a case management system to track each alert from generation through disposition, capturing investigator notes, evidence, and supervisory sign-off.

**Step 5 — Governance and tuning.**

Establish a quarterly surveillance review in which the compliance team presents alert volumes, disposition statistics, false positive rates, and findings to senior management. Use disposition data to tune thresholds — if 95% of churning alerts are false positives, consider tightening the threshold or adding qualifying criteria (e.g., also requiring that the account has a conservative investment objective). Document all tuning decisions and rationale. Annually, engage an independent party (internal audit or outside consultant) to assess the surveillance program's effectiveness, consistent with the expectation of FINRA Rule 3120 (supervisory control system testing).

**Step 6 — Regulatory readiness.**

Maintain examination-ready documentation including: the surveillance policy and procedures manual, the risk assessment, alert calibration methodology and tuning history, sample investigation case files demonstrating thorough analysis, disposition statistics showing timely review, and evidence of senior management oversight. During examinations, FINRA and the SEC will request a walkthrough of the surveillance program, review a sample of closed alerts, and assess whether the firm's surveillance is commensurate with its business risk profile.

### Example 2: Implementing Allocation Fairness Monitoring for an RIA Managing Model Portfolios

**Scenario:** A registered investment adviser manages $2.5 billion across 800 client accounts using a model portfolio approach. The firm executes block trades and allocates fills across accounts using a pro-rata method. A recent compliance review identified that allocation records are maintained in spreadsheets with minimal oversight, and no systematic monitoring exists to verify fairness. The CCO wants to implement a post-trade allocation fairness monitoring system.

**Step 1 — Establish the allocation policy.**

Before monitoring can be effective, the firm must have a clear, written allocation policy. The policy should specify:

- Block trades are allocated pro rata based on each account's target participation at the time the order is placed
- Partial fills are allocated pro rata, with rounding adjustments distributed based on a defined methodology (e.g., largest remainder method)
- De minimis exceptions: allocations that would result in fractional shares or odd lots below a threshold may be adjusted
- IPO and new issue allocations follow FINRA Rules 5130 and 5131 restrictions
- Any deviation from pro-rata allocation must be documented with a rationale and approved by the CCO

**Step 2 — Data infrastructure.**

Build a data pipeline that captures:

- The pre-trade allocation schedule (which accounts are participating and at what target percentage)
- Execution data (fill prices, quantities, timestamps, venues)
- The post-trade allocation record (which accounts received which fills at which prices)
- Account metadata (account type, fee structure, whether the account is a proprietary account, a performance-fee account, or an account of a firm principal or employee)

The pre-trade allocation schedule is critical — without it, the firm cannot verify whether post-trade allocations match the intended pro-rata distribution.

**Step 3 — Pro-rata verification.**

For each block trade, compute the expected allocation for each account (target percentage multiplied by total shares filled) and compare to the actual allocation. Flag deviations exceeding a defined tolerance (e.g., more than 1% relative deviation or more than 100 shares absolute deviation, whichever is smaller). For partial fills, verify that the partial allocation preserves the pro-rata distribution.

Investigate flagged deviations: legitimate reasons include rounding, odd-lot avoidance, account-level restrictions (e.g., an account that cannot hold a particular security due to client guidelines), and minimum lot requirements.

**Step 4 — Dispersion analysis.**

For each block trade allocated across multiple accounts, compute the dispersion of average execution prices across accounts. In a perfectly fair allocation, all accounts receive the same average price (the block's average execution price). Compute the standard deviation of account-level average prices and flag block trades where any account's average price deviates by more than a defined threshold from the block average (e.g., more than 5 basis points).

High dispersion may indicate sequential allocation rather than average-price allocation, timing manipulation, or cherry-picking.

**Step 5 — Systematic favoritism detection.**

On a monthly and quarterly basis, run a longitudinal analysis across all block trades. For each account, compute the average allocation quality (measured as the difference between the account's average execution price and the block benchmark, aggregated across all block trades in the period). Rank accounts by allocation quality and test for patterns:

- Test whether proprietary accounts, performance-fee accounts, or accounts of firm principals consistently receive better-than-average allocations
- Use statistical tests (t-test or Mann-Whitney U test) to determine whether the observed differences are statistically significant
- If the firm manages both wrap-fee and commission-based accounts, test whether allocation quality differs between the two — commission-based accounts generate per-trade revenue and may be disfavored in allocation

**Step 6 — Reporting and governance.**

Produce a monthly allocation fairness report for the CCO summarizing: total block trades, number of flagged deviations, root causes of deviations, and results of the systematic favoritism analysis. The CCO should review and sign off on the report.

On a quarterly basis, present allocation fairness findings to the firm's investment or compliance committee. Annually, the allocation fairness monitoring program should be reviewed for effectiveness, and the statistical thresholds should be recalibrated based on the prior year's data. Maintain all reports, investigation files, and committee minutes as examination-ready documentation.

### Example 3: Designing a Best Execution Review Framework for Quarterly Committee Review

**Scenario:** A broker-dealer that routes approximately 50,000 equity orders per month needs to formalize its best execution review process. The firm routes orders to three external market makers (two of which provide payment for order flow) and directly to two exchanges. FINRA has flagged the absence of a formal best execution committee and documented review process as an examination finding. The firm must design a framework for quarterly best execution committee reporting.

**Step 1 — Define benchmarks and metrics.**

Select benchmarks appropriate to the firm's order flow:

- VWAP as the primary benchmark for market orders and marketable limit orders
- Arrival price (mid-quote at order receipt) as the benchmark for non-marketable limit orders
- Effective spread and price improvement as supplementary metrics

For each execution, compute: the benchmark deviation (execution price minus benchmark), the effective spread (2 times the absolute difference between the execution price and the midpoint at time of execution), and price improvement (the improvement over the NBBO at time of order receipt, measured in cents per share). Aggregate these metrics by order type (market, limit, stop), order size (small/medium/large), security type (large-cap, mid-cap, small-cap), and venue.

**Step 2 — Venue-level analysis.**

For each routing destination (the three market makers and two exchanges), compute: average effective spread, average price improvement, fill rate (percentage of orders that receive a complete fill), speed of execution (time from order submission to fill), and average benchmark deviation. Compare venues against each other and against the consolidated market benchmark.

Identify any venue that is systematically underperforming — e.g., a market maker whose effective spread is consistently wider than the other venues, or a venue with a notably lower fill rate for large orders. For the two market makers providing payment for order flow (PFOF), specifically assess whether the PFOF arrangement is associated with inferior execution quality, since the SEC and FINRA scrutinize PFOF arrangements for conflicts of interest.

**Step 3 — Outlier identification.**

Flag individual executions where the benchmark deviation exceeds a threshold: for example, executions where the VWAP deviation exceeds 25 basis points (for large-cap) or 75 basis points (for small-cap). Review a sample of outlier executions to determine root cause:

- Abnormal market conditions (high volatility, wide spreads)
- Order handling issues (delayed routing, stale limit prices)
- Venue-specific issues (slow execution, partial fills at inferior prices)

Document the root cause analysis for each reviewed outlier.

**Step 4 — Quarterly committee report.**

Structure the quarterly report as follows:

- **Executive summary** — overall execution quality trends, any material changes since the prior quarter, and key findings
- **Aggregate execution quality** — average effective spread, price improvement, and VWAP deviation across all orders, with trend analysis over the trailing four quarters
- **Venue analysis** — performance by routing destination, including comparison tables and any venues flagged for underperformance
- **PFOF analysis** — specific analysis of execution quality for orders routed to PFOF venues versus non-PFOF venues, assessing whether the PFOF arrangements are consistent with best execution
- **Outlier analysis** — summary of outlier executions reviewed, root causes identified, and corrective actions taken
- **Routing changes** — any changes to routing logic, new venue relationships, or terminated venues since the prior quarter
- **Recommendations** — proposed changes to routing, venue relationships, or monitoring methodology

**Step 5 — Committee governance.**

The best execution committee should include the head of trading, the CCO or a senior compliance officer, a representative from technology (responsible for order routing systems), and a member of senior management. The committee meets quarterly to review the report, discuss findings, and approve or reject recommendations.

All committee discussions and decisions must be documented in formal minutes. The minutes should record: attendees, data reviewed, findings discussed, decisions made (e.g., to terminate a venue, adjust routing parameters, or investigate a specific pattern further), and any dissenting views. Committee minutes are a primary examination artifact — FINRA and SEC examiners routinely request them to assess the rigor and independence of the firm's best execution review.

**Step 6 — Annual comprehensive review.**

In addition to quarterly reviews, conduct an annual comprehensive best execution review that includes:

- A reassessment of the firm's order routing arrangements and venue relationships
- A review of market structure developments (new venues, SEC rulemaking, changes to exchange fee schedules) that may affect execution quality
- An evaluation of whether the firm's benchmarks and metrics remain appropriate
- A review of the surveillance methodology and thresholds

The annual review should result in a written report to senior management documenting the firm's best execution practices and any recommended changes.

## Common Pitfalls
- Running churning surveillance with a single fixed turnover threshold for all account types — thresholds must be calibrated to the customer's investment objectives, with lower thresholds for conservative and income-oriented accounts
- Monitoring allocations only at the block trade level without running longitudinal systematic favoritism analysis — a firm can produce fair individual allocations while still systematically favoring certain accounts over time through subtle selection of which accounts participate in which blocks
- Relying on end-of-day batch surveillance for time-sensitive patterns like front-running and marking the close — these patterns require T+0 or near-real-time detection to enable timely investigation and intervention
- Failing to integrate communications surveillance (email, chat, voice) with trade surveillance — insider trading and coordinated trading cases almost always require communications evidence; siloed systems miss these connections
- Setting alert thresholds too conservatively to minimize false positives, which creates under-detection of genuine violations — regulators view under-detection as a more serious deficiency than a high false positive rate, provided the firm can demonstrate timely disposition of alerts
- Treating alert disposition statistics as the measure of program effectiveness — a program that closes 99% of alerts with "no finding" may indicate poor calibration rather than a clean book of business
- Allowing a backlog of aged, uninvestigated alerts to accumulate — regulators consider a large backlog of open alerts to be evidence of an inadequate surveillance program, regardless of the firm's explanation for the backlog
- Excluding proprietary trading accounts and employee accounts from the surveillance scope — these accounts are higher-risk and should receive heightened, not reduced, scrutiny
- Conducting best execution reviews using only aggregate statistics without examining individual outlier executions — aggregate metrics can mask systematic issues with specific order types, securities, or venues
- Documenting investigation dispositions with conclusory statements ("no violation found") rather than substantive analysis — regulatory examiners expect to see the analytical work supporting the disposition
- Failing to update the surveillance risk assessment when the firm enters new business lines, launches new products, or experiences significant growth — the surveillance program must evolve with the firm's risk profile
- Neglecting personal trading surveillance for non-investment personnel who may nonetheless have access to MNPI (e.g., operations staff processing block orders, technology personnel with access to order management systems)

## Cross-References
- **pre-trade-compliance** (Layer 11): Pre-trade checks (restricted list screening, position limits, margin requirements) are the first line of defense; post-trade surveillance catches what pre-trade controls miss and validates that pre-trade controls are functioning
- **trade-execution** (Layer 11): Execution quality data feeds directly into best execution review; post-trade compliance evaluates whether the execution function is meeting its obligations
- **order-lifecycle** (Layer 11): Post-trade surveillance depends on complete, accurate order lifecycle data from origination through execution and allocation; gaps in order lifecycle data create surveillance blind spots
- **sales-practices** (Layer 9): Churning, unauthorized trading, and breakpoint abuse are sales practice violations detected through post-trade surveillance; the sales-practices skill covers the substantive rules, while this skill covers the detection methodology
- **anti-money-laundering** (Layer 9): SAR filing obligations may be triggered by post-trade surveillance findings; the AML skill covers the substantive compliance framework, while this skill covers the surveillance detection that identifies reportable activity
- **books-and-records** (Layer 9): Surveillance case files, alert documentation, investigation records, and committee minutes are books and records subject to retention requirements under SEC Rules 17a-3/17a-4 and Rule 204-2
- **regulatory-reporting** (Layer 9): Post-trade surveillance may trigger regulatory reporting obligations (SARs, 13H filings, TRACE corrections, CAT error remediation); the regulatory-reporting skill covers the filing mechanics
- **conflicts-of-interest** (Layer 9): Allocation fairness, cherry-picking, and personal trading surveillance all address conflicts of interest; the conflicts-of-interest skill covers the identification and mitigation framework, while this skill covers the post-trade detection methodology
