---
name: client-reporting-delivery
description: "Design, generate, and deliver client performance reports across all channels, covering quarterly reports, tax reporting, portal integration, and compliance review. Use when the user asks about building or redesigning report templates, choosing what to include in quarterly or annual client reports, transitioning from print to digital delivery, integrating a client portal, presenting net-of-fee performance with benchmarks, managing report production timelines, or handling e-delivery consent. Also trigger when users mention 'client reporting', 'quarterly performance report', 'report customization', 'tax lot report', '1099 supplement', 'report disclaimers', 'UHNW reporting', or 'report QA process'."
---

# Client Reporting and Delivery

## Purpose

Enable Claude to assist advisory firms with designing, generating, customizing, and delivering client reports across all channels. This skill covers the full reporting lifecycle from data sourcing through delivery confirmation, including quarterly performance reports, tax reporting, client portal integration, compliance review, and quality assurance. It provides guidance on report content structure, personalization by client segment, delivery channel strategy, and the operational workflows that ensure timely, accurate, and compliant report production.

## Layer

10 — Advisory Practice (Front Office)

## Direction

Retrospective

## When to Use

- An advisor or operations team asks about designing or redesigning client report templates
- Questions arise about what sections to include in quarterly or annual client reports
- A firm needs guidance on transitioning from printed to digital report delivery
- Someone asks about client portal integration for reporting
- Questions about performance presentation in client reports (return periods, benchmarks, net vs gross)
- A firm needs to build or improve its report generation workflow and production timeline
- Tax reporting questions: realized gains/losses reports, 1099 supplements, coordination with CPAs
- Compliance review of client reports: required disclaimers, supervisory review, record retention
- Quality assurance processes for report accuracy and error remediation
- Client segmentation for report customization (mass affluent vs HNW vs UHNW)
- E-delivery consent and electronic delivery compliance questions
- Report frequency management: quarterly, annual, ad-hoc, on-demand

## Core Concepts

### Client Reporting Architecture

The reporting pipeline in an advisory firm flows from data sources through a generation engine to client delivery. The primary data sources are the portfolio management system (PMS), custodian data feeds, financial planning tools, and the billing system. Each source contributes distinct data elements: the PMS provides portfolio holdings, performance calculations, and asset allocation; the custodian provides official transaction records, settled positions, and tax lot data; the financial planning tool provides goal progress and projection data; and the billing system provides fee calculations and payment history.

Report types span the full advisory relationship:

- **Quarterly performance reports** — The cornerstone deliverable. Summarizes portfolio performance, allocation, holdings, and transactions for the quarter with trailing period returns.
- **Annual reviews** — Comprehensive year-in-review combining performance, planning progress, and forward outlook. Often presented in person.
- **Financial plan updates** — Progress toward goals, updated projections, and recommended adjustments. May be quarterly or semi-annual.
- **Tax reports** — Realized gains and losses, unrealized gains and losses, cost basis reports, 1099 supplements, wash sale reports, and tax-loss harvesting summaries.
- **Billing summaries** — Detailed fee calculations showing AUM tiers, fee rates, amounts debited, and billing period.
- **Custom and ad-hoc reports** — Client-requested reports outside the standard cycle, such as a holdings detail for a mortgage application or a performance report for a specific date range.

Reporting platforms fall into several categories. PMS-embedded reporting tools (Orion Portfolio Solutions, Black Diamond, Tamarac Reporting) generate reports directly from the portfolio management database, ensuring data consistency. Standalone reporting platforms (Addepar, Backstop Solutions) aggregate data from multiple sources and offer advanced customization, often favored by firms serving UHNW clients and family offices. Client portal integration layers the reporting function into a broader digital client experience.

Custodian statements and advisor-produced reports serve complementary but distinct purposes. Custodian statements are the official record of account activity and positions, produced by the custodian (Schwab, Fidelity, Pershing). Advisor-produced reports add value through consolidated household views, custom benchmarks, goal-based framing, blended performance across custodians, and advisor commentary. Clients receive both, and firms should help clients understand the relationship between the two, particularly when minor data differences arise from timing or methodology.

### Report Content and Structure

A well-designed quarterly performance report follows a logical structure that guides the client from high-level summary to supporting detail:

1. **Cover page** — Firm branding, client or household name, reporting period, key headline metrics (total portfolio value, period return, net change in value). The cover page sets the tone and provides the most critical data points at a glance.

2. **Executive summary and market commentary** — A brief narrative (typically one page) covering market conditions during the period, key events that affected portfolios, and a forward-looking perspective. This section can be firm-level (same for all clients) or personalized by the advisor.

3. **Portfolio summary** — Asset allocation (current vs target, shown as pie chart or bar chart and table), total holdings count, cash position, and net deposits/withdrawals during the period. Household-level view aggregating all accounts.

4. **Performance summary** — Period returns (MTD, QTD, YTD, 1-year, 3-year, 5-year, 10-year, since inception) with benchmark comparison. Displayed as both table and chart. Net-of-fee returns as the primary presentation with gross-of-fee available.

5. **Account detail** — Individual account summaries within the household, each showing account type, custodian, value, allocation, and performance. Important for clients with multiple accounts across different registration types.

6. **Holdings detail** — Complete listing of positions by account or by asset class, showing security name, ticker, shares/units, market value, percentage of portfolio, unrealized gain/loss, and yield.

7. **Transaction summary** — Purchases, sales, income received, contributions, withdrawals, and fee debits during the period. Level of detail varies by client preference.

8. **Fee summary** — Advisory fees charged during the period, showing calculation methodology (AUM, billing rate, proration if applicable). Increasingly important given regulatory emphasis on fee transparency.

9. **Disclosures and disclaimers** — Required legal language including past performance disclaimers, benchmark descriptions, fee impact disclosure, and firm registration information.

Content customization by client segment is essential. Mass affluent clients typically prefer simplified reports emphasizing total value, return, and allocation with minimal holdings detail. High-net-worth (HNW) clients generally want comprehensive reports including full holdings, transaction detail, and benchmark comparisons. Ultra-high-net-worth (UHNW) and family office clients often require institutional-grade reporting with performance attribution, alternative investment detail, multi-entity consolidation, and custom analytics. The challenge is balancing comprehensiveness with readability — a 40-page report that goes unread serves no one.

### Performance Presentation in Reports

Performance is the most scrutinized section of any client report. Presenting returns accurately and clearly requires attention to methodology, time periods, benchmarks, and context.

**Return methodologies:**

- **Time-weighted return (TWR)** measures the compound rate of growth independent of external cash flows. TWR is the standard for evaluating manager or strategy performance because it removes the effect of the client's deposit and withdrawal timing. Most PMS platforms calculate daily-valued TWR using the Modified Dietz method for sub-period returns.
- **Money-weighted return (MWR/IRR)** reflects the client's actual experience including the impact of cash flow timing. A client who added significant funds just before a downturn will see a lower MWR than TWR. MWR is more intuitive for clients asking "how did my money do?" and is increasingly presented alongside TWR in client reports.

Presenting both TWR and MWR can be powerful when accompanied by a brief explanation of the difference. When the two diverge significantly, it signals that cash flow timing had a material impact and opens a productive conversation.

**Return periods:**

Standard periods displayed in quarterly reports include MTD (month-to-date), QTD (quarter-to-date), YTD (year-to-date), trailing 1-year, trailing 3-year, trailing 5-year, trailing 10-year, and since-inception. Annualization conventions are critical: returns for periods exceeding one year should be annualized (geometric annualization), while returns for periods of one year or less should be presented as cumulative (non-annualized). Mixing conventions without clear labeling is a common source of confusion and potential compliance issues.

**Benchmark selection and display:**

Every portfolio should have a clearly defined benchmark. The primary benchmark should reflect the portfolio's strategic asset allocation and investment universe. For diversified portfolios, a blended benchmark (e.g., 60% MSCI ACWI / 40% Bloomberg US Aggregate) is more appropriate than a single index. Reports should include the benchmark description, component indices and weights, and a note that the benchmark is not investable and does not reflect fees. Some firms also display peer group comparisons or risk-adjusted metrics (Sharpe ratio, Sortino ratio) for sophisticated clients.

**Net-of-fee vs gross-of-fee returns:**

Net-of-fee returns are the preferred presentation for client reports because they represent the client's actual experience after paying advisory fees. Gross-of-fee returns may be shown alongside net for transparency or for GIPS-compliant presentations. The fee impact over long periods is substantial and should not be obscured.

**GIPS compliance considerations:**

Firms that claim compliance with the Global Investment Performance Standards must adhere to specific presentation requirements in composite reports, including required disclosures, composite construction rules, and prescribed return calculation methodologies. Individual client reports are not composites, but firms claiming GIPS compliance should ensure client-level reporting does not contradict or undermine their composite presentations.

**Performance disclaimers:**

Every report displaying performance data must include disclaimers stating that past performance is not indicative of future results, describing the benchmark and its limitations, disclosing whether returns are net or gross of fees, and noting any material factors affecting comparability across periods (e.g., strategy change, benchmark change).

### Report Customization and Personalization

Report customization operates at multiple levels, from firm-wide template design to individual client preferences.

**Level of detail:** Some clients want a two-page summary; others want 30 pages of detail. The reporting system should support configurable section inclusion, allowing advisors to toggle sections on or off per client. Common toggleable sections include holdings detail, transaction detail, individual account breakdowns, and performance attribution.

**Grouping and organization:** Reports can organize portfolio data in several ways depending on client preference and portfolio structure:

- **By account** — Each account presented separately, useful for clients focused on specific account objectives (IRA vs taxable).
- **By asset class** — All holdings grouped by asset class across accounts, useful for clients focused on overall allocation.
- **By goal or sleeve** — Holdings grouped by investment objective (retirement, education, legacy), useful for goal-based planning relationships.
- **By manager or strategy** — Holdings grouped by underlying manager or model portfolio, useful for multi-manager platforms.

**Household vs account-level reporting:** Most clients prefer a consolidated household view as the primary presentation, with account-level detail as a secondary section. The household view enables total portfolio allocation, consolidated performance, and a single net worth perspective. Account-level detail remains important for tax planning, beneficiary considerations, and account-specific objectives.

**Custom benchmarks:** Clients with unique portfolio constraints (ESG exclusions, concentrated stock positions, alternative allocations) may require custom benchmarks that reflect their investable universe. The reporting system should support advisor-defined blended benchmarks with custom weights and component indices, updated as the target allocation evolves.

**Personalized commentary:** The highest-value customization is advisor-written commentary specific to the client's situation. This might address recent portfolio changes, progress toward financial plan goals, upcoming planning actions, or responses to client questions. Some firms provide a firm-level market commentary as a default with an editable field for advisor personalization. Advisors who consistently add personalized commentary report stronger client engagement and retention.

**White-labeling:** Multi-advisor firms, RIA aggregators, and sub-advisory relationships often require white-labeled reports carrying the presenting firm's branding rather than the platform or TAMP provider's branding. The reporting system should support configurable logos, firm names, disclosures, and contact information.

**Language and terminology:** Reports should use language appropriate to the client's financial sophistication. A retired schoolteacher needs different terminology than a former CFO. Avoid unnecessary jargon where plain language suffices, but do not oversimplify for sophisticated clients who expect precision.

### Delivery Channels and Methods

Report delivery has evolved from exclusively print-and-mail to a multi-channel environment. Firms must manage several delivery methods simultaneously.

**Client portal (primary digital channel):**

The client portal is the hub of digital delivery. Reports are published to the portal where clients can view them online, download as PDF, and access historical reports in an archive. Portal-based delivery offers several advantages: immediate availability (no mail delay), persistent access (clients can revisit reports anytime), reduced cost (no printing or postage), environmental sustainability, and integration with other portal features (real-time portfolio view, document vault, secure messaging). The portal should provide notification (email or push) when new reports are available.

**Email delivery:**

Email delivery remains common, typically as an encrypted PDF attachment or a link to the client portal. Email is familiar and requires no portal login, making it accessible for less tech-savvy clients. However, email delivery raises security concerns (sensitive financial data in transit or in inboxes), so best practices include PDF encryption with a client-specific password, secure email platforms, or portal links rather than attachments. Firms should document email delivery preferences and security measures.

**Print and mail:**

Physical printed reports delivered via postal mail are declining but not extinct. Some clients, particularly older individuals or those in jurisdictions with specific requirements, prefer or require printed reports. Print delivery involves additional cost (printing, paper, postage), longer delivery time (days vs instant), and environmental impact. Firms transitioning to digital-first delivery should maintain a print capability for clients who opt in and for any regulatory requirements that mandate physical delivery.

**In-person review:**

Many advisors present reports during client meetings rather than simply delivering them. The meeting context allows the advisor to walk through results, provide context, answer questions in real time, and connect performance to financial plan progress. In-person presentation may use the same PDF report, a slide-deck derivative, or an interactive portal screen share. The report serves as both a leave-behind document and a meeting framework.

**Multi-channel strategy:**

The recommended approach is digital-first with print opt-in. Default delivery is portal publication with email notification. Clients who prefer print explicitly opt in and receive mailed copies in addition to (not instead of) digital access. This ensures every client has portal access to current and historical reports while accommodating print preferences.

**E-delivery consent:**

SEC rules on electronic delivery (primarily from SEC guidance releases and interpretive letters) require that firms provide notice that documents are available electronically, ensure the client has access to the electronic format, and obtain evidence of delivery (or evidence of notice with access). Firms should document client consent to electronic delivery, provide clear instructions for portal access, and maintain systems that confirm report availability and client access. Under FINRA rules, broker-dealers have additional requirements for implied consent and opt-out rights.

**Delivery confirmation and tracking:**

Firms should track report delivery status: portal published, email sent, email opened (if tracked), portal accessed, print mailed, print delivered (via tracking number if warranted). Delivery tracking supports compliance (evidence of delivery), operations (identifying delivery failures), and client service (confirming clients received their reports).

### Report Generation Workflow

The quarterly reporting cycle is a firm's most operationally intensive recurring process, typically spanning T+5 to T+15 after quarter-end (5 to 15 business days after the quarter closes).

**Workflow stages:**

1. **Data finalization (T+1 to T+5):** Custodian data feeds settle, reconciliation between PMS and custodian records completes, corporate actions process, and pricing finalizes. Reports cannot be generated until data is clean. The most common delay is waiting for custodian reconciliation to complete, particularly for accounts holding alternative investments, private placements, or international securities with delayed settlement.

2. **Report generation (T+5 to T+7):** Batch report generation runs for all client accounts and households. The PMS or reporting platform compiles data into report templates, calculates performance for all required periods, generates charts and tables, and produces PDF output. Batch runs may take several hours for large firms (thousands of accounts). Exception reports flag accounts with data issues that prevent clean report generation.

3. **Quality assurance (T+7 to T+9):** QA is the critical gate between generation and delivery. The QA process includes automated validation (returns within expected ranges, AUM totals match PMS, fee calculations correct, no missing data fields) and manual spot-checking (visual inspection of formatting, chart rendering, correct client names and account numbers, cross-referencing with custodian statements). QA should cover a statistical sample at minimum; many firms review all reports for households above a materiality threshold.

4. **Compliance review (T+9 to T+10):** Compliance reviews a sample of reports to verify disclaimers are present and current, performance presentation is accurate and not misleading, benchmark descriptions are complete, and fee disclosures are appropriate. Any reports used for marketing purposes (e.g., shared with prospects) trigger additional review under the SEC Marketing Rule.

5. **Advisor review and commentary (T+8 to T+11):** Advisors review reports for their client relationships, add personalized commentary where applicable, and flag any issues (data they know to be incorrect, clients with special circumstances requiring modified reports). This stage often runs in parallel with compliance review.

6. **Approval and release (T+11 to T+12):** Final approval, either by a designated operations manager, the Chief Compliance Officer, or through an automated workflow, clears reports for delivery. Once approved, reports are locked against further editing.

7. **Delivery (T+12 to T+15):** Reports are published to the client portal, email notifications are sent, and print reports are dispatched. Delivery may be staggered (largest clients first, or by advisor team) to manage volume and catch any last-minute issues before the full batch goes out.

**Handling exceptions:**

- Accounts with unresolved data issues receive delayed reports with a communication to the client explaining the delay.
- New accounts with short history (less than one full quarter) may receive a modified report or a welcome package in lieu of a performance report.
- Closed accounts require a final report covering the period from the last report through the closing date, including final performance and distribution details.

**Timeline management:**

The reporting cycle compresses many dependencies into a tight window. Bottleneck identification is essential: late custodian data, slow reconciliation, advisor commentary delays, and compliance review capacity are the most common constraints. Firms should establish clear deadlines for each stage with escalation procedures when deadlines slip.

### Client Portal Integration

The client portal has become central to the reporting strategy, serving as both a delivery channel and an interactive extension of the static report.

**Report access models:**

- **Batch-published reports:** Traditional PDF reports generated quarterly and published to the portal on a scheduled date. Clients access them like a digital filing cabinet.
- **On-demand reports:** Clients can generate reports for custom date ranges or specific accounts directly through the portal, without waiting for the quarterly cycle.
- **Interactive dashboards:** Real-time or near-real-time portfolio views that complement static reports. Dashboards show current allocation, performance, holdings, and transactions with drill-down capability.

The most effective portal strategy combines all three: periodic batch reports for the formal record, on-demand capability for ad-hoc needs, and interactive dashboards for day-to-day engagement.

**Portal features that complement reports:**

- **Real-time portfolio view** — Current holdings, values, and allocation without waiting for the next report cycle.
- **Transaction history** — Searchable history of all transactions across accounts.
- **Document vault** — Secure storage for financial plans, tax documents, estate documents, and other sensitive files shared between advisor and client.
- **Secure messaging** — Encrypted communication channel between client and advisor, replacing unsecured email for sensitive topics.
- **Goal tracking** — Visual progress toward financial plan goals (retirement funded percentage, education savings target, etc.) that contextualizes portfolio performance.
- **Fee transparency** — Itemized fee history and current fee schedule accessible through the portal.

**Driving portal adoption:**

Many firms struggle with portal adoption rates, which typically range from 40% to 70% of clients actively using the portal. Strategies to improve adoption include making the portal the default delivery channel, demonstrating the portal during client meetings, simplifying the registration process (single sign-on, mobile-friendly), providing portal training materials, and emphasizing features beyond report access (document vault, secure messaging, goal tracking). Younger clients and those with larger portfolios tend to have higher adoption rates.

**Portal vendors:**

Leading platforms include Orion Connect (integrated with Orion PMS, strong reporting and planning integration), Black Diamond Client Experience (known for visual report quality and client experience), Tamarac Reporting (integrated with Envestnet ecosystem), Addepar Client Portal (favored by UHNW and family office firms for advanced analytics), and custom-built portals (used by larger firms wanting full control over the client experience). Selection criteria include integration with the firm's PMS, report customization capability, mobile experience, security features, and total cost of ownership.

### Tax Reporting and Year-End Deliverables

Tax reporting is a distinct reporting function with its own timeline, data requirements, and audience (the client's CPA or tax preparer in addition to the client).

**Tax-related reports:**

- **Realized gain/loss report** — Lists all securities sold during the tax year with purchase date, sale date, proceeds, cost basis, and gain or loss. Categorized by short-term vs long-term. This is the primary report used for tax return preparation. Must reconcile to the custodian's 1099-B.
- **Unrealized gain/loss report** — Shows the embedded gains and losses in current holdings as of year-end. Critical for year-end tax planning: identifying positions to sell for tax-loss harvesting or gain realization before year-end.
- **1099 supplement** — A reconciliation document explaining any differences between the custodian-issued 1099 and the firm's records. Differences commonly arise from amortization methods, return of capital classification, or wash sale adjustments.
- **Cost basis report** — Detailed tax lot information for all current holdings, showing original purchase date, acquisition cost, adjustments (wash sales, corporate actions, return of capital), and current tax basis.
- **Wash sale report** — Identifies wash sale events where losses were disallowed due to repurchase of substantially identical securities within the 30-day window before or after the sale.
- **Tax-loss harvesting summary** — For firms that actively harvest tax losses, a summary of harvesting activity during the year: losses harvested, replacement securities purchased, estimated tax benefit.

**Year-end deliverables beyond tax reports:**

- **Annual performance summary** — Full-year performance across all standard periods, often presented in a more polished format than the Q4 report.
- **Annual fee summary** — Total fees paid during the calendar year, useful for tax deduction purposes where applicable and for client awareness of total cost.
- **Year-end portfolio appraisal** — Complete holdings listing with market values as of December 31, often used as a reference point for estate planning, insurance reviews, and net worth statements.

**Timing and coordination:**

Tax reporting follows a distinct timeline from performance reporting. Preliminary tax reports are typically available in January, based on the best available data. However, custodians issue corrected 1099s through February and sometimes into March (particularly for accounts holding partnerships, REITs, or international securities). Final tax reports should be issued only after the custodian's 1099 correction period closes. Firms should communicate the timeline clearly to clients and their CPAs to avoid filing with preliminary data that later changes.

Coordination with client CPAs is a value-added service. Proactive firms send tax reports directly to the client's CPA (with client authorization), provide a cover letter explaining the reports and any notable items, and make themselves available to answer CPA questions during tax season. This reduces friction for the client and positions the advisor as a hub of the client's financial team.

### Compliance Requirements for Client Reports

Client reports are communications to clients and therefore subject to regulatory scrutiny. Compliance requirements vary based on the firm's registration type (RIA, broker-dealer, dual registrant) and how the reports are used.

**Regulatory framework:**

- **SEC Marketing Rule (Rule 206(4)-1):** If client reports or performance extracts are shared with prospective clients, they become advertisements subject to the Marketing Rule. This includes requirements for performance presentation (net returns, one/five/ten year periods, prominent disclosure), prohibitions on misleading statements, and compliance review and approval before use.
- **FINRA Rule 2210 (Communications with the Public):** For broker-dealers, client reports are "correspondence" (communication with up to 25 retail investors in 30 days) or "retail communication" (more than 25). Retail communications require principal pre-approval; correspondence requires supervisory procedures. All communications must be fair, balanced, and not misleading.
- **SEC Custody Rule:** Reports may create "custody" implications if the firm has the ability to deduct fees directly. Fee disclosures in reports should be consistent with the firm's custody rule compliance.
- **Regulation S-P (Privacy):** Reports contain non-public personal information and must be delivered securely. Delivery methods (email, portal, mail) must comply with the firm's privacy policies and procedures.

**Required disclaimers:**

- Past performance is not indicative of future results.
- Description of each benchmark used, including that the benchmark is not investable and does not reflect fees or expenses.
- Whether returns are presented net or gross of advisory fees, and the impact of fees on returns.
- Firm registration information (RIA registration with the SEC or state, FINRA membership if applicable).
- Material facts necessary to avoid misleading the client (e.g., strategy changes, benchmark changes, calculation methodology changes).

**Supervisory review:**

Firms must establish supervisory procedures for client report review. The scope of supervisory review typically includes verifying performance accuracy (sampling), confirming disclaimers are present and current, reviewing advisor-written commentary for compliance (no guarantees, no promissory language, fair and balanced), and checking that reports are consistent with the client's actual account and investment strategy. Compliance should document the review process, the reviewer, the date, and any issues identified and resolved.

**Record retention:**

Under the SEC's books-and-records rules (Rule 204-2 for RIAs, Rule 17a-4 for broker-dealers), firms must retain copies of all communications delivered to clients, including client reports. Retention periods are typically five years (RIAs) or six years (broker-dealers) from the date of delivery. The retained copy must be the exact version delivered to the client. Digital archiving of PDFs published to portals satisfies this requirement when properly indexed and backed up.

**GIPS requirements:**

Firms claiming GIPS compliance must present composite-level performance in GIPS-compliant reports to prospective clients. Individual client reports are not composites, but the firm should ensure that client-level performance data does not contradict composite presentations and that GIPS-required disclosures appear on any report used to market the firm's investment capabilities.

### Report Quality Assurance

Quality assurance is the safeguard between report generation and client delivery. Errors in client reports damage credibility, create compliance risk, and generate costly re-issuance work.

**Automated validation checks:**

- **Return reasonableness:** Period returns for each account and the household fall within expected ranges (e.g., equity-heavy portfolios during a quarter when the S&P 500 returned 5% should show returns in a reasonable band around that figure). Flag outliers for manual review.
- **AUM reconciliation:** Total market value on the report matches the PMS balance and is within tolerance of the custodian statement balance. Differences exceeding a threshold (e.g., 0.1%) trigger investigation.
- **Fee calculation validation:** Advisory fees shown on the report match the billing system records. Fee rates match the client's fee schedule.
- **Completeness checks:** No missing data fields (blank returns, zero AUM for active accounts, missing benchmark data, absent disclaimers). All accounts in the household are included.
- **Period consistency:** The reporting period is correct (e.g., the Q4 report covers October 1 through December 31, not a different range).

**Visual and manual inspection:**

- **Formatting:** Charts render correctly, tables are properly aligned, page breaks fall at logical points, fonts and colors are consistent with the template.
- **Client-specific accuracy:** The correct client name, account numbers, and advisor name appear on the report. Reports are not crossed (Client A receiving Client B's data).
- **Data cross-check:** Spot-check report data against the PMS and custodian statement for a sample of accounts. Verify that holdings, transactions, and performance are consistent across sources.

**Common errors and root causes:**

- **Stale data:** Reports generated before custodian reconciliation is complete, reflecting outdated positions or missing transactions.
- **Incorrect benchmark:** A benchmark assignment error in the PMS causes the wrong benchmark to appear on the report, making performance comparison meaningless.
- **Wrong time period:** A configuration error causes reports to display incorrect period dates or returns for the wrong quarter.
- **Formatting glitches:** Template updates that break chart rendering, cause text overflow, or misalign columns.
- **Missing accounts:** An account recently added to the household is excluded from the consolidated report because the PMS grouping was not updated.
- **Cross-client errors:** The most severe error type — delivering a report containing another client's data. This is both a compliance violation and a privacy breach requiring notification.

**Error tracking and resolution:**

Firms should maintain an error log tracking each identified issue: date discovered, report affected, error type, root cause, resolution, and corrective action to prevent recurrence. Error rate metrics (errors per 1,000 reports generated) should be tracked over time and reported to management. A rising error rate signals a systemic issue (data quality, template instability, staffing) requiring intervention.

**Client-reported errors:**

When a client identifies an error, the resolution workflow includes acknowledgment (prompt response to the client), investigation (verify the error and identify the cause), correction (generate a corrected report), re-issuance (deliver the corrected report with a brief explanation), and root cause analysis (determine whether the error is isolated or systemic). The tone of client communication should be transparent and professional, treating the error seriously while reassuring the client that their actual account and investments are unaffected if the error is limited to the report.

## Worked Examples

### Example 1: Redesigning a Quarterly Reporting Package

**Scenario:**

A 20-advisor RIA firm managing $3.5 billion across 2,400 households is redesigning its quarterly reporting package. The current reports are generic, text-heavy PDF exports from the PMS with no customization by client segment. Advisors report that clients find the reports confusing, and the operations team spends two weeks each quarter manually adjusting reports for key clients. The firm uses Orion as its PMS and has a client portal but only 35% portal adoption. The firm wants a modern, tiered reporting approach with efficient production.

**Design Considerations:**

The report template structure should follow a modular design where sections can be toggled by client tier:

- **Cover page:** Firm-branded, household name, reporting period, headline metrics (portfolio value, quarterly return, year-to-date return, net contributions/withdrawals). Clean visual design with the firm's color palette.
- **Executive summary (1 page):** Firm-level market commentary (written by the CIO or investment committee) with an editable field for advisor personalization. Advisors for top-tier clients write 2-3 sentences specific to the client's situation.
- **Portfolio summary (1-2 pages):** Asset allocation chart (current vs target), allocation table, total portfolio value, cash position. Household-level view as the primary presentation.
- **Performance summary (1-2 pages):** TWR and MWR for the portfolio and each account. Periods: QTD, YTD, 1-year, 3-year, 5-year, since inception. Benchmark comparison with blended benchmark matching the portfolio's target allocation. Chart showing cumulative growth of portfolio vs benchmark since inception.
- **Holdings detail (2-5 pages, toggleable):** Complete position listing by asset class. Security name, ticker, shares, market value, percentage of portfolio, unrealized gain/loss. Included by default for HNW and UHNW tiers; excluded by default for mass affluent (available on request).
- **Transaction summary (1-2 pages, toggleable):** Purchases, sales, dividends, contributions, withdrawals, fees. Included for HNW and above by default.
- **Fee summary (1 page):** Quarterly fee calculation detail: beginning AUM, fee rate, fee amount, payment method. Always included for transparency.
- **Disclosures (1-2 pages):** Standard disclaimers, benchmark descriptions, firm information. Updated quarterly by compliance.

Client tier customization:

- **Mass affluent (under $1M):** Cover page, executive summary, portfolio summary, performance summary, fee summary, disclosures. Total approximately 6-8 pages. Simplified language, fewer metrics.
- **HNW ($1M-$10M):** All sections included. Approximately 12-18 pages. Full detail with benchmark comparison and advisor commentary.
- **UHNW ($10M+) and family office:** All sections plus performance attribution summary, alternative investment detail, multi-entity consolidation, and custom analytics. Approximately 20-30 pages. Advisor writes substantive personalized commentary for each household.

For digital delivery via the client portal: all reports are published to the Orion Connect portal with automated email notification. The email contains a branded message with the client's name and a direct link to the portal (no PDF attachment for security). To boost portal adoption from 35% toward 70%, the firm launches a portal onboarding campaign concurrent with the new report rollout, with advisors demonstrating the portal during quarterly review meetings.

The 10-business-day production workflow from quarter-end:

- T+1 to T+4: Data finalization, custodian reconciliation, corporate action processing.
- T+5 to T+6: Batch report generation for all households, exception report produced.
- T+6 to T+7: Automated QA validation, manual spot-check of a 10% sample plus all UHNW households.
- T+7 to T+8: Compliance review of a 5% sample plus all reports containing advisor-written commentary.
- T+7 to T+9: Advisor review and personalized commentary entry (runs in parallel with compliance review).
- T+9: Final approval by operations manager and compliance officer.
- T+10: Batch publication to portal, email notifications sent, print copies mailed for opt-in clients.

**Analysis:**

The modular template design eliminates manual per-client adjustments by encoding customization rules into the report generation configuration. Tier-based defaults reduce the operations team's workload from two weeks of manual adjustments to exception handling only. The 10-business-day cycle is achievable with disciplined data finalization and parallel compliance/advisor review stages. The portal-first delivery strategy, paired with an adoption campaign, should reduce print volume by 50% or more within two quarters. Key risk: advisor commentary delays can push the timeline past T+10, so the firm should establish a hard T+9 deadline for commentary with an auto-populated default if the advisor does not provide custom text.

### Example 2: Transitioning from Print to Digital-First Delivery

**Scenario:**

A 45-year-old advisory firm with 1,800 clients is transitioning from mailing printed quarterly reports to digital-first delivery. Currently, 100% of clients receive printed reports via USPS mail at a cost of $4.50 per report (printing, assembly, postage), totaling approximately $32,400 per year for quarterly reports alone. The firm has a client portal (Black Diamond Client Experience) but has never used it for report delivery. The client base skews older — 40% of clients are over 65 — and the firm is concerned about resistance to change.

**Design Considerations:**

The transition plan should balance efficiency gains with client experience, executed in phases:

**Phase 1 — Communication and consent (Month 1-2):**

- Send a personalized letter to all clients announcing the transition to digital delivery, emphasizing benefits (faster access, 24/7 availability, historical archive, environmental sustainability).
- Include a response form for delivery preference: digital-only (portal and email notification), digital with print supplement (portal access plus mailed copy), or print-only (opt-in exception, requires written request).
- Advisors call their top 50 clients personally to explain the transition and address concerns.
- E-delivery consent documentation collected and filed per SEC electronic delivery guidance.

**Phase 2 — Portal onboarding (Month 2-3):**

- Dedicated onboarding support: a team member or recorded webinar walks clients through portal registration, login, and report access.
- Simplified registration process: pre-populated registration links sent via email requiring only password creation.
- Mobile-friendly portal experience, since many older clients are comfortable with tablets even if not desktop computers.
- Printed quick-start guide mailed to all clients with step-by-step portal access instructions and support phone number.
- Advisors demonstrate the portal during every client meeting during the transition quarter.

**Phase 3 — Parallel delivery (Quarter 1 of new approach):**

- For the first quarterly cycle, deliver reports through both channels: publish to portal with email notification and mail printed copies. This gives clients a safety net and builds confidence in the digital experience.
- Track portal access: which clients logged in, viewed their report, and downloaded PDFs.
- Follow up with clients who did not access the portal, offering additional onboarding support.

**Phase 4 — Digital-first (Quarter 2 onward):**

- Default delivery switches to digital-only (portal publication with email notification).
- Clients who opted for print supplement or print-only continue receiving mailed copies.
- Quarterly review of print opt-in list: advisors gently encourage digital adoption during meetings.

**Exception handling for print-required clients:**

- Clients over age 80 or with documented technology barriers are automatically enrolled in the print supplement program.
- No client is denied printed reports if they request them.
- Print reports are identical to digital (same PDF), printed in color, and mailed in a firm-branded envelope.
- The firm budgets for 20-30% of clients remaining on print in Year 1, declining to 10-15% by Year 3.

**Compliance review of electronic delivery:**

- E-delivery consent forms reviewed by compliance counsel to ensure they meet SEC guidance requirements (informed consent, evidence of access, opt-out ability).
- Portal security reviewed: encryption in transit and at rest, authentication requirements (multi-factor authentication recommended), session timeout, and access logging.
- Record retention: portal automatically archives all published reports with delivery timestamp, satisfying books-and-records requirements. Emailed notification records are also retained.
- Privacy review: portal access controls ensure each client sees only their own data.

**Adoption metrics tracking:**

- Portal registration rate (target: 85% within 6 months).
- Active portal usage rate (logged in at least once per quarter; target: 65% within 12 months).
- Report access rate (percentage of clients who viewed their report within 14 days of publication).
- Print opt-in rate (track trend quarterly, targeting decline).
- Client satisfaction: survey question on report delivery satisfaction added to annual client survey.
- Cost savings: track printing, postage, and assembly cost reduction quarterly.

**Analysis:**

The phased approach minimizes client disruption while systematically driving digital adoption. The parallel delivery quarter is costly (double delivery) but critical for building client confidence. The 40% over-65 demographic is a legitimate concern, but portal adoption among older adults has increased significantly and the firm's approach of personal outreach, simplified onboarding, tablet-friendly design, and continued print availability mitigates the risk. Expected cost savings are substantial: if 70% of clients move to digital-only, annual printing and mailing costs drop from $32,400 to under $10,000, with additional savings in staff time for assembly and mailing. The compliance framework for e-delivery must be established before the first digital delivery, not after.

### Example 3: Remediating Performance Calculation Errors in Quarterly Reports

**Scenario:**

During a routine internal audit, a mid-size RIA discovers that approximately 5% of quarterly reports (60 out of 1,200 households) delivered in the most recent quarter contained performance calculation errors. The errors originated from late custodian data corrections for accounts holding a specific alternative investment fund that revised its NAV two weeks after the initial quarter-end pricing. The firm's reporting workflow generated reports using the preliminary NAV, and the corrected NAV arrived after reports were already delivered. The differences in reported returns ranged from 5 to 35 basis points, affecting since-inception and trailing-period returns for the affected accounts.

**Design Considerations:**

**Root cause analysis:**

The root cause is a timing mismatch between the report generation schedule and the data finalization timeline for alternative investments. The firm's standard T+7 report generation date assumed all custodian data was final, but the alternative investment fund in question consistently provides corrected NAVs at T+14 to T+18. The PMS ingested the corrected data after reports were generated and delivered, but no process existed to flag that delivered reports contained stale pricing for specific holdings.

Contributing factors: (a) no data readiness checklist identifying securities with known delayed pricing, (b) no automated comparison between report-date pricing and current PMS pricing after corrections, (c) the alternative investment was added to client portfolios 18 months ago without updating the reporting workflow to accommodate its pricing timeline.

**Data validation checks to implement:**

- **Pre-generation data readiness gate:** Before batch report generation, run an automated check confirming that all holdings have final pricing. Maintain a watchlist of securities with known delayed pricing (alternatives, private placements, international funds with delayed NAVs). If any watchlist security has preliminary pricing, delay report generation for affected accounts or flag them for manual review.
- **Post-generation pricing comparison:** After the custodian data correction window closes (T+20), automatically compare the pricing used in delivered reports against current PMS pricing. Flag any account where the pricing difference exceeds a materiality threshold (e.g., 10 basis points of return impact).
- **Alternative investment pricing tracker:** Maintain a log of all alternative investments with their expected pricing finalization dates. Cross-reference against the reporting calendar to identify conflicts.

**QA workflow enhancements:**

- Add a specific QA step for accounts holding alternative investments, private placements, or other securities with delayed pricing.
- Implement a two-tier generation process: generate reports for accounts with all-final pricing on the standard timeline (T+7); hold accounts with pending pricing data for a second generation run (T+18 to T+20) after corrections are received.
- Establish a materiality threshold for pricing changes: differences below 5 basis points may not warrant re-issuance; differences above 5 basis points trigger the re-issuance process.

**Re-issuance process for affected clients:**

1. Generate corrected reports for all 60 affected households using final pricing data.
2. QA review all corrected reports (100% review, not sampling, given the sensitivity).
3. Compliance review of corrected reports and the client communication.
4. Prepare a client communication letter (reviewed by compliance counsel) explaining: (a) a pricing correction for a specific investment affected the performance data in the previously delivered report, (b) the corrected report is enclosed/attached/available on the portal, (c) the actual portfolio holdings and transactions were not affected — only the reported performance calculation, (d) the specific line items that changed and the magnitude of the difference, and (e) an apology for the error and a description of the steps the firm is taking to prevent recurrence.
5. Deliver corrected reports and communication letter through each client's preferred channel. Advisors for top-tier clients call the client before or concurrently with the letter to provide a personal explanation.
6. File the corrected reports and communication in the firm's books and records, noting the original report, the correction, and the reason.

**Ongoing monitoring to prevent recurrence:**

- Quarterly review of the security watchlist for delayed-pricing holdings, updated as new investments are added to client portfolios.
- Monthly reporting operations meeting that includes a review of the data readiness gate results and any exceptions.
- Annual review of the reporting timeline relative to custodian data correction windows, adjusting the production calendar as needed.
- Error rate tracking: monitor the corrected-report rate quarterly with a target of zero re-issuances due to data timing issues.
- If the firm adds additional alternative investments, the onboarding process must include updating the reporting watchlist and confirming the pricing timeline is compatible with the report production schedule.

**Analysis:**

The 5% error rate, while seemingly modest, represents a meaningful compliance and reputational risk. Performance reporting accuracy is a fundamental fiduciary obligation, and delivering incorrect returns — even by a few basis points — erodes client trust. The remediation approach addresses both the immediate issue (corrected reports with transparent client communication) and the systemic cause (inadequate data readiness checking for delayed-pricing securities). The two-tier generation process adds operational complexity but is necessary for firms holding alternatives with delayed pricing. The materiality threshold (5 basis points) provides a practical standard for triggering re-issuance while avoiding excessive corrections for immaterial differences. The firm should also evaluate whether its compliance manual and supervisory procedures need updating to reflect the new QA steps and data readiness requirements.

## Common Pitfalls

- **Generating reports before data is final.** Rushing to meet a delivery deadline with preliminary data — particularly for alternative investments, international securities, or accounts with pending corporate actions — leads to inaccurate reports and costly re-issuance. Establish a data readiness gate that must pass before report generation begins.

- **One-size-fits-all report design.** Delivering the same 25-page report to every client regardless of portfolio size, complexity, or sophistication wastes the client's time and the firm's resources. Tier-based customization ensures each client receives an appropriately scoped report.

- **Neglecting the performance disclaimer.** Omitting or using outdated performance disclaimers creates compliance risk. Disclaimers must be reviewed and updated at least annually by compliance, covering past performance language, benchmark descriptions, fee impact, and calculation methodology.

- **Ignoring delivery preferences.** Forcing all clients to digital delivery or continuing to print for clients who prefer digital wastes resources and frustrates clients. Maintain an accurate delivery preference database and honor stated preferences.

- **Presenting annualized returns for periods under one year.** Annualizing a three-month return inflates the apparent performance and is misleading. Only annualize returns for periods exceeding one year, and clearly label all return periods.

- **Failing to reconcile advisor reports to custodian statements.** When clients notice discrepancies between the advisor's report and the custodian statement, they lose confidence in the advisor's data. Proactively explain common differences (timing, methodology, household consolidation) and ensure the report includes a note about the relationship between the two.

- **Treating the report as a standalone document rather than a conversation tool.** Reports are most valuable when reviewed with the client, not simply mailed. Advisors who use reports as a framework for client meetings extract significantly more relationship value from the reporting investment.

- **Underinvesting in quality assurance.** Skipping or minimizing QA to speed delivery is a false economy. A single cross-client error (delivering Client A's data to Client B) creates a privacy breach, compliance violation, and severe reputational damage that far exceeds the cost of thorough QA.

- **Not tracking portal adoption metrics.** Launching a client portal without measuring adoption leads to low usage and wasted technology investment. Set specific adoption targets and actively manage the onboarding funnel.

- **Delaying tax report delivery without client communication.** Clients and their CPAs expect tax reports by a certain date. When corrected 1099s delay final tax reporting, proactive communication about the timeline prevents frustration and demonstrates professionalism.

## Cross-References

- **performance-reporting** (Layer 8, wealth-management) — Client reports implement the performance reporting standards defined in this skill. Report templates and content must align with the firm's performance reporting policy.
- **performance-metrics** (Layer 1a, wealth-management) — Reports display the return and risk metrics calculated per this skill. Ensures consistency between the metrics definition and their presentation in reports.
- **performance-attribution** (Layer 5, wealth-management) — Attribution analysis is included in detailed client reports for HNW and UHNW tiers. The attribution skill defines the methodology; this skill addresses how to present attribution results clearly.
- **gips-compliance** (Layer 9, compliance) — GIPS presentation standards apply to composite-level performance reporting and influence client-level report design for firms claiming compliance.
- **advertising-compliance** (Layer 9, compliance) — Reports shared with prospects become marketing materials subject to the SEC Marketing Rule and advertising compliance requirements.
- **books-and-records** (Layer 9, compliance) — Delivered reports must be retained per SEC and FINRA recordkeeping rules. The delivery channel and archiving process must support compliant record retention.
- **client-disclosures** (Layer 9, compliance) — Required disclaimers and disclosures that appear in client reports are defined and maintained per this compliance skill.
- **portfolio-management-systems** (Layer 10, advisory-practice) — The PMS is the primary data source for report generation. Data quality, reconciliation status, and system configuration directly affect report accuracy.
- **advisor-dashboards** (Layer 10, advisory-practice) — Dashboards provide real-time portfolio views that complement the periodic snapshots in client reports. Together they form a complete client information ecosystem.
- **fee-billing** (Layer 10, advisory-practice) — Fee summaries included in client reports draw data from the billing system. Fee calculation accuracy in reports depends on billing system integration.
- **financial-planning-integration** (Layer 10, advisory-practice) — Financial plan progress reporting is included in comprehensive client reports, connecting portfolio performance to goal achievement.
- **client-review-prep** (Layer 10, advisory-practice) — Review preparation feeds into and complements the report delivery workflow; reports are a key component of the review meeting package.
