---
name: advisor-dashboards
description: "Design, build, and optimize dashboards for RIA practice management with AUM tracking, revenue analytics, and KPI frameworks. Use when the user asks about tracking firm-level metrics, monitoring advisor productivity, measuring organic growth rate, analyzing client retention and attrition, building executive or branch manager views, setting up exception alerts for NIGO or rebalancing drift, benchmarking against industry peers, or designing role-based dashboard access. Also trigger when users mention 'how is the practice doing', 'revenue per advisor', 'client attrition', 'net new assets', 'effective fee rate', 'practice benchmarking', 'AUM growth decomposition', 'advisor capacity', or 'referral tracking'."
---

# Advisor Dashboards

## Purpose

Provide comprehensive guidance on designing, building, and operating dashboards for registered investment advisory firms. This skill covers the full spectrum of advisory practice dashboards — from executive-level practice analytics and AUM/revenue tracking through advisor-facing daily operational views, client flow analysis, exception monitoring, and KPI frameworks. It enables Claude to advise on dashboard architecture, metric selection, role-based access design, data source integration, alerting logic, and the benchmarking frameworks that transform raw operational data into actionable practice intelligence for advisors, managers, compliance officers, and firm leadership.

## Layer

10 — Advisory Practice (Front Office)

## Direction

both

## When to Use

- Designing or evaluating dashboards for an RIA's management team or executive committee
- Building an advisor-facing daily operational dashboard or morning briefing view
- Defining practice-level KPIs and metric hierarchies for an advisory firm
- Tracking AUM growth, revenue trends, and fee analytics across advisors, teams, or segments
- Analyzing client flows — new client acquisition, attrition, money-in-motion, and competitive losses
- Designing exception and alert dashboards for operations, compliance, or billing teams
- Evaluating advisor productivity metrics — clients per advisor, revenue per advisor, capacity planning
- Establishing benchmarking frameworks using industry data for RIA performance comparison
- Selecting dashboard technology and data integration architecture for multi-system advisory environments
- Building role-based views that serve different audiences (advisor, branch manager, compliance, executive)
- Setting firm-level and advisor-level goals with progress tracking and trend visualization
- Reviewing or improving an existing dashboard for relevance, usability, or data accuracy

## Core Concepts

### 1. Practice-Level KPIs

Key performance indicators for advisory practices fall into several categories, each measuring a different dimension of firm health. A well-designed KPI framework provides both a snapshot of current performance and the trend data needed to identify emerging risks or opportunities.

**AUM (Assets Under Management).** The foundational metric for any AUM-based advisory practice. Total firm AUM is the product of client count, average relationship size, and market performance. AUM should be tracked at multiple levels: firm total, by advisor or team, by client segment (high-net-worth, mass affluent, institutional), by account type (taxable, IRA, trust, plan), and by custodian. AUM changes decompose into two components — market appreciation/depreciation and net new assets — and tracking each separately reveals whether growth is organic (advisor-driven) or market-driven.

**Revenue.** Total advisory revenue, broken down by fee type (AUM-based fees, financial planning fees, hourly fees, performance fees, other), by advisor or team, by client segment, and by billing period. The effective fee rate (total revenue divided by average AUM) is a critical derived metric that reveals fee compression trends over time. Revenue should be tracked on both an accrual basis (for GAAP reporting) and a cash basis (for cash flow management).

**Client Count.** The number of active client households, tracked by segment, advisor, and tenure. Distinguish between households (the billing and relationship unit) and accounts (the custodial unit). A firm with 500 households might have 2,000 accounts. Client count trends — net new households per quarter, attrition rate, and average household tenure — reveal the health of the firm's client acquisition and retention efforts.

**Revenue Per Client.** Average annual revenue per household, segmented by client tier. This metric exposes whether the firm is growing revenue through larger relationships or by adding many small ones. Declining revenue per client may indicate fee compression, client downsizing, or an acquisition strategy that targets smaller relationships than the firm's economics require.

**Average Account Size.** Total AUM divided by the number of accounts (or households). Tracked over time, this metric reveals whether the firm is attracting larger or smaller relationships. When combined with revenue per client, it exposes effective fee rate trends at the client level.

**Organic Growth Rate.** Net new assets (new client assets plus existing client contributions minus withdrawals minus terminated client assets) divided by beginning-of-period AUM, expressed as an annualized percentage. Organic growth strips out market appreciation to isolate the advisor-driven component of AUM change. Industry benchmarks for healthy RIAs typically target 5-10% annual organic growth. Negative organic growth — even during strong markets — signals that the firm is losing ground despite favorable conditions.

**Retention Rate.** The percentage of beginning-of-period AUM or client count that remains at the end of the period, excluding market effects. A 95% client retention rate means 5% of clients (by count or AUM) left during the period. Retention is often more valuable than acquisition: replacing a departed $2M client requires acquiring two new $1M clients, each carrying acquisition cost and onboarding effort.

**Referral Rate.** New clients acquired through existing client referrals as a percentage of total new clients. Referral-sourced clients tend to have higher AUM, lower acquisition cost, and higher retention. Tracking referral rate by advisor identifies which advisors have the strongest referral networks and which may benefit from referral training or process improvement.

**Profitability Metrics.** For firms that track practice-level financials, operating margin (revenue minus direct and allocated expenses, divided by revenue) is the ultimate measure of practice efficiency. Industry benchmarks for well-run RIAs typically show operating margins of 25-35%. Revenue per employee (total revenue divided by total headcount) provides a simpler proxy for overall productivity. Compensation-to-revenue ratio (total compensation including advisor payouts divided by total revenue) should typically fall between 55-70% for sustainable practices.

### 2. AUM and Revenue Dashboards

AUM and revenue dashboards provide the financial pulse of the advisory practice. They answer the questions firm leadership asks most frequently: how much do we manage, how much are we earning, where is the growth coming from, and what does the trajectory look like?

**AUM by Advisor/Team/Segment.** A hierarchical view that drills from firm total AUM down to team, advisor, and individual household. Heatmaps or bar charts comparing advisors by AUM highlight concentration risk (if one advisor manages a disproportionate share) and identify capacity constraints (advisors approaching their effective management limit). Segment views (by client tier, account type, or investment model) reveal the composition of the firm's book and inform strategic decisions about target markets.

**Revenue by Fee Type.** A breakdown showing what percentage of total revenue comes from AUM-based fees versus planning fees, hourly fees, or other sources. Firms diversifying beyond pure AUM-based revenue should track the mix over time. A rising share of planning fee revenue indicates successful adoption of comprehensive planning services. Billing exception rates by fee type highlight operational trouble spots.

**Pipeline and Flows Tracking.** The flow of assets into and out of the firm, tracked on a rolling basis. Key flow metrics include:

- **Gross inflows** — New client assets plus existing client contributions. Decompose into new relationship inflows (first deposit from a new household) and existing relationship inflows (additional assets from current clients, including rollovers, consolidations, and savings contributions).
- **Gross outflows** — Client withdrawals plus terminated client assets. Decompose into distribution outflows (planned withdrawals for income, RMDs, or specific needs) and attrition outflows (clients leaving the firm entirely or moving assets to competitors).
- **Net flows** — Gross inflows minus gross outflows. Positive net flows indicate the firm is gathering more than it is losing. Net flows should be tracked monthly and displayed as a rolling 12-month trend.
- **Pipeline** — Prospective clients and anticipated asset transfers that have not yet funded. Pipeline tracking requires CRM integration and should display the prospect's name, estimated AUM, probability of close, expected funding date, and assigned advisor.

**AUM Growth Decomposition.** A waterfall chart or stacked bar showing the components of AUM change over a period:

- Beginning AUM
- Plus: market appreciation (or minus: market depreciation)
- Plus: net new assets (inflows minus outflows)
- Equals: ending AUM

This decomposition is essential for management because it separates controllable growth (net new assets) from uncontrollable growth (market returns). A firm whose AUM grew 12% in a year where markets returned 10% actually achieved only 2% organic growth — a far less impressive result than the headline number suggests.

### 3. Client Flow Analytics

Client flow analytics go beyond aggregate flow numbers to analyze the dynamics of client acquisition, retention, and asset consolidation at a granular level.

**New Client Acquisition Funnel.** Track the conversion pipeline from initial lead through prospect meeting, proposal delivery, agreement signing, and account funding. Key funnel metrics include: lead-to-meeting conversion rate, meeting-to-proposal rate, proposal-to-close rate, close-to-fund rate, average time from lead to funded account, and average funded amount versus initial estimate. Funnel analytics by advisor expose differences in prospecting effectiveness and identify bottlenecks (an advisor with a high meeting-to-proposal rate but low proposal-to-close rate may need help with proposal quality or pricing).

**Client Attrition Tracking.** Monitor departing clients by reason (voluntary termination, death, relocation, fee sensitivity, service dissatisfaction, competitor solicitation), by advisor, by client segment, and by tenure. Attrition dashboards should display both the count and the AUM impact of departures. Early-tenure attrition (clients leaving within the first two years) suggests onboarding or expectation-setting issues. Long-tenure attrition (clients of 10+ years departing) may signal relationship fatigue or a generational transition where heirs move assets.

**Money-in-Motion Indicators.** Proactive signals that a client may be consolidating assets (opportunity) or preparing to leave (risk). Key indicators include: large cash deposits from external sources (potential rollover or inheritance), systematic outflows exceeding income needs (possible transfer to a competitor), reduced engagement (fewer meetings, unanswered communications), and changes to beneficiary designations or account titling. The dashboard should flag these indicators for advisor follow-up before the client makes a final decision.

**Asset Consolidation Tracking.** For existing clients with held-away assets, track consolidation opportunities — the gap between total household assets (visible through aggregation) and managed assets. A client with $3M managed and $2M held away in a former employer 401(k) represents a $2M consolidation opportunity. Consolidation dashboards rank opportunities by dollar value and likelihood, enabling advisors to prioritize outreach.

**Competitive Losses.** When clients depart, capture the destination (self-directed, competitor RIA, wirehouse, robo-advisor, bank) and the stated reason. Over time, this data reveals competitive threats and informs the firm's value proposition and pricing strategy. A cluster of departures to a lower-cost competitor signals fee pressure; departures to a full-service wirehouse may indicate that clients want services the firm does not offer.

**Generational Transfer Tracking.** A growing concern for advisory firms is the risk that heirs of deceased clients move inherited assets elsewhere. Track accounts where the primary account holder is over age 75, the estimated intergenerational transfer value, whether the firm has an established relationship with the next generation, and the outcome of recent inheritance events (assets retained vs. assets departed). Firms that proactively engage the next generation retain significantly more inherited assets than those that wait until the triggering event occurs.

### 4. Exception and Alert Dashboards

Exception dashboards surface items that require immediate attention — anomalies, breaches, overdue tasks, and operational failures that deviate from expected norms. These dashboards are typically used by operations managers, compliance officers, and practice managers rather than individual advisors.

**Compliance Alerts.** Items requiring compliance attention: overdue annual reviews, stale client profiles, unsigned disclosures, advertising items awaiting review, trade pre-clearance violations, outside business activity disclosures due, gift and entertainment reporting gaps, and code of ethics certification deadlines. Each alert should display the responsible party, the deadline, days until (or past) the deadline, and the escalation status. Color coding (green/yellow/red) provides an at-a-glance severity assessment.

**Operational Exceptions.** Reconciliation breaks between the PMS and custodian, failed data feeds, NIGO (not in good order) account opening documents, incomplete account transfers (ACAT failures), unsigned paperwork, and pending account maintenance requests. The dashboard should display exception age (how long the item has been open) and flag items that have exceeded their service-level agreement.

**Rebalancing Drift Alerts.** Accounts where portfolio drift exceeds the firm's threshold but rebalancing has not been initiated. Display the client name, account, current allocation versus target, magnitude of drift, days since threshold breach, and assigned advisor. Persistent drift alerts may indicate advisor inattention or intentional deviation that requires documentation.

**Billing Exceptions.** Accounts with unusual billing outcomes: fees significantly higher or lower than the prior period, zero-dollar fees, negative fee calculations, accounts missing from the billing run, fee-schedule mismatches (the rate charged differs from the assigned schedule), and overdue invoice payments. Billing exception dashboards should be reviewed before every billing run approval.

**Custodian NIGO Status.** A centralized view of account opening and maintenance requests that have been returned as "not in good order" by the custodian. NIGO items delay account funding and create a poor client experience. The dashboard should track NIGO reason (missing signature, incorrect form version, incomplete information), age, assigned CSA, and resolution status.

**Pending Tasks and Aging.** A consolidated view of all open tasks across the practice — from NBA-recommended actions and CRM tasks to operational work items and compliance deadlines. Group by responsible party, sort by age, and flag items approaching or exceeding their SLA. Aging analysis (average days to resolve by task type) identifies process bottlenecks and staffing constraints.

### 5. Advisor Productivity Metrics

Productivity dashboards help practice managers and firm leadership understand how effectively advisors are using their time and where capacity exists for growth.

**Clients Per Advisor.** The number of active client households assigned to each advisor. Industry data suggests that a solo advisor can effectively manage 75-125 households depending on service model complexity and support staff. Advisors approaching their capacity limit need either additional support staff, a service model adjustment, or a planned transition of smaller clients. Advisors well below capacity represent either growth potential or an underperformance concern.

**Revenue Per Advisor.** Total advisory revenue generated per advisor, calculated both as the advisor's personal book revenue and as revenue per advisor adjusted for team support (dividing team revenue by the number of team members). Revenue per advisor benchmarked against industry surveys (Schwab RIA Benchmarking, InvestmentNews Adviser Compensation Study, FA Insight) reveals whether the firm's advisor economics are competitive.

**Meeting Volume.** The number of client meetings (in-person, video, phone) conducted per advisor per period, sourced from CRM activity logs or calendar integration. Meeting volume is a leading indicator of relationship health and prospecting activity. Advisors with declining meeting counts may be disengaging from proactive client management.

**Proposal-to-Close Ratio.** The percentage of formal proposals or financial plans delivered that result in a signed advisory agreement and funded account. This metric, sourced from CRM pipeline data, measures advisor effectiveness at converting prospects into clients. Low ratios may indicate pricing issues, proposal quality problems, or a mismatch between the firm's value proposition and the prospect's needs.

**Onboarding Pipeline.** New clients in various stages of the onboarding process — from signed agreement through account opening, asset transfer, initial investment, and first review meeting. Bottlenecks in the onboarding pipeline (e.g., transfers taking 30+ days) create client dissatisfaction and delay revenue recognition. Track average onboarding time and identify the stage where delays most commonly occur.

**Capacity Planning.** A forward-looking view that combines current client count, revenue per client, and projected growth to estimate when each advisor will reach capacity. Capacity planning dashboards inform hiring decisions, team restructuring, and client assignment strategies. A firm projecting that three advisors will hit capacity within 12 months should begin recruiting and training before capacity becomes a constraint.

### 6. Dashboard Design Principles for Advisory Firms

Dashboard effectiveness depends as much on design and delivery as on the underlying data. A technically accurate dashboard that no one uses provides zero value.

**Role-Based Views.** Different roles need different information:

- **Advisor view** — Personal book of business: today's priority actions (NBA queue), client alerts, portfolio drift, pending tasks, personal KPIs (AUM, revenue, client count, meeting count), and upcoming client milestones. The advisor view should be a focused, action-oriented morning briefing that answers "what should I do today?"
- **Manager/team lead view** — Team-level aggregation: advisor comparison (AUM, revenue, meeting volume, compliance completion), team pipeline, team flows, team exceptions, and capacity utilization. The manager view should identify which advisors need support and which processes need attention.
- **Compliance view** — Firm-wide compliance status: overdue reviews, disclosure delivery status, trade surveillance alerts, advertising review queue, regulatory filing deadlines, and exception aging. The compliance view should provide the CCO with confidence that supervisory obligations are being met.
- **Executive/owner view** — Firm-level financials: total AUM, revenue, growth decomposition, profitability, organic growth rate, retention, and benchmarking against industry peers. The executive view should support strategic decision-making about hiring, pricing, M&A, and market positioning.

**Drill-Down from Summary to Detail.** Every summary metric should be clickable, allowing the user to drill from the firm-level number down to the team, advisor, client, and account level. An executive who sees that net flows turned negative this quarter should be able to click through to see which advisors experienced outflows, which clients departed, and what reasons were recorded. Without drill-down capability, dashboards generate questions but do not answer them.

**Real-Time vs. Batch Refresh.** Not all metrics require real-time data. AUM and performance figures depend on end-of-day custodian feeds and should refresh overnight. Exception dashboards benefit from intraday refresh (especially compliance and operational alerts). Pipeline and flow data depend on CRM updates and are typically current as of the last advisor entry. Clearly label the data freshness on every dashboard panel so users understand whether they are seeing today's data or yesterday's close.

**Mobile-First Design.** Advisors spend significant time outside the office — at client meetings, conferences, and working remotely. Dashboards must function on tablet and phone screens. Mobile design requires ruthless prioritization: show only the top 3-5 metrics on the mobile view, with the option to expand. Push notifications for critical alerts (compliance deadlines, large cash movements, billing exceptions) ensure that time-sensitive items reach the advisor regardless of whether they are at their desk.

**Data Source Integration.** Advisory dashboards pull data from multiple systems: the portfolio management system (AUM, positions, performance, drift), CRM (client data, activities, pipeline, tasks), billing engine (revenue, fee analytics, exceptions), custodian feeds (account status, NIGO, transfers), financial planning tools (plan status, funded ratios), and compliance systems (review tracking, surveillance). Dashboard architecture must include a data integration layer — whether a data warehouse, an ETL pipeline, or direct API connections — that normalizes and reconciles data from these disparate sources into a single consistent view.

### 7. Benchmarking and Goal Tracking

Dashboards become significantly more valuable when metrics are displayed alongside benchmarks and goals, providing context that transforms raw numbers into performance assessments.

**Firm-Level Targets.** Annual and quarterly targets set by firm leadership for key metrics: total AUM, organic growth rate, revenue, revenue growth, net new clients, retention rate, and profitability. Display actual performance against targets with a simple actual/target/variance format and a progress bar or gauge. Color code based on whether the firm is on track (green), at risk (yellow), or behind (red) based on year-to-date run rate.

**Advisor-Level Goals.** Individual goals negotiated between each advisor and firm management. Common advisor-level goals include: net new AUM gathered, new households acquired, revenue target, meeting count, and planning engagement conversions. Advisor goal dashboards should be visible to the individual advisor (for self-management) and to the practice manager (for coaching and accountability). Display goals with the same actual/target/variance format and include a trend line showing progress over time.

**Industry Benchmarks for RIA Metrics.** Annual benchmarking studies published by Schwab (RIA Benchmarking Study), Fidelity (RIA Benchmarking), InvestmentNews (Adviser Compensation and Staffing Study), and FA Insight (Growth by Design) provide median and top-quartile figures for key RIA metrics: revenue per advisor, AUM per advisor, operating margin, clients per advisor, staff-to-advisor ratio, organic growth rate, and client retention rate. Displaying firm metrics alongside these industry benchmarks reveals whether the firm is performing at, above, or below peer levels. Benchmarking is most meaningful when filtered by firm size (AUM range), geography, and service model to ensure an apples-to-apples comparison.

**Trend Analysis.** Every KPI should be displayed with at least 8-12 quarters of historical trend data. Trends reveal patterns that point-in-time snapshots miss: gradual fee compression (effective fee rate declining 2 bps per year), seasonal flow patterns (outflows spike in April for tax payments), or advisor capacity approaching saturation (clients per advisor rising steadily). Moving averages (3-quarter or 4-quarter) smooth volatility and make the underlying trend more visible.

## Worked Examples

### Example 1: Building an Executive Dashboard for an RIA's Management Team

**Scenario:** A $1.8 billion RIA with 22 advisors, 1,400 client households, and two offices needs an executive dashboard for the three-member management committee (CEO, COO, CCO). The firm has a portfolio management system (Orion), a CRM (Salesforce), and a standalone billing system. The management committee meets weekly and wants a single-page view that answers: Are we growing? Are we profitable? Are we compliant? Where do we need to act?

**Design Considerations:**

The executive dashboard must synthesize data from three separate systems into a unified view without requiring the management committee to log into multiple platforms. The data integration layer should pull AUM and performance data from Orion nightly, client and pipeline data from Salesforce via API, and revenue and billing data from the billing system after each quarterly billing run (with interim accrual estimates during the quarter). All data should land in a lightweight data warehouse that powers the dashboard, ensuring that metric calculations are consistent and auditable.

The layout should be organized into four quadrants aligned with the management committee's four key questions. The Growth quadrant displays: total firm AUM with quarter-over-quarter and year-over-year change, AUM growth decomposition waterfall (market vs. net new assets), organic growth rate (annualized) benchmarked against the 5-10% industry target, net flows for the current quarter with a rolling 12-month trend, and new client pipeline with estimated AUM and probability-weighted forecast. The Revenue quadrant displays: total quarterly revenue with prior-quarter and prior-year comparison, effective fee rate trend (trailing 8 quarters), revenue by advisor ranked by contribution, revenue concentration (percentage of revenue from top 10 clients flagged if any single household exceeds 5%), and revenue forecast for the next quarter based on current AUM and effective fee rates. The Compliance quadrant displays: annual review completion rate (percentage of clients current, target 100%), overdue compliance items count with aging breakdown, disclosure delivery status for any pending regulatory updates, and trade surveillance exception count. The People/Productivity quadrant displays: AUM per advisor and revenue per advisor benchmarked against Schwab RIA Benchmarking medians, clients per advisor with capacity indicators, advisor retention (have any advisors departed or signaled intent to leave), and staff-to-advisor ratio compared to industry benchmarks.

**Analysis:**

The key design challenge is data freshness alignment. AUM data refreshes nightly from custodian feeds through Orion, but revenue data updates quarterly (with monthly accrual estimates providing interim visibility). Pipeline data in Salesforce depends on advisor diligence in updating opportunity records — stale pipeline data is worse than no pipeline data because it creates false confidence. The management committee should be trained to understand the refresh cadence of each metric, and the dashboard should display "as of" timestamps on every panel.

The most actionable items for the weekly meeting are: the organic growth rate (is the firm gathering assets or just riding the market?), the compliance completion rate (are we on track for 100% before year-end?), and advisor capacity indicators (do we need to hire before capacity constrains growth?). Revenue concentration deserves special attention — if the firm discovers that its top 10 households generate 25% of total revenue, that concentration risk should trigger a strategic discussion about diversification through new client acquisition and service-tier expansion.

Over time, the trailing trend data will prove more valuable than any single week's snapshot, enabling the management committee to detect gradual shifts — fee compression, rising attrition, declining organic growth — before they become critical. The firm should establish a quarterly dashboard review cadence to assess whether the displayed metrics are still driving decisions and whether any new strategic priorities require additional panels.

### Example 2: Designing an Advisor-Facing Daily Dashboard

**Scenario:** A 10-advisor RIA wants to replace its current practice of advisors checking multiple systems each morning (CRM for tasks, PMS for drift alerts, email for custodian notifications, spreadsheet for client birthdays) with a single daily dashboard that serves as the advisor's operational home screen. Each advisor manages approximately 100 client households. The firm uses Tamarac for portfolio management, Redtail for CRM, and Schwab as its primary custodian.

**Design Considerations:**

The daily dashboard must be the first screen the advisor sees each morning and should answer: What requires my attention today? The design should prioritize actionability over comprehensiveness — every item on the screen should have a clear next step, and the advisor should be able to act directly from the dashboard without navigating to another system.

The top section is a personal scorecard showing: the advisor's total AUM with daily change (from Tamarac), year-to-date net new assets versus annual goal, number of active client households, and upcoming milestone (next goal checkpoint). This section is compact — one line of key metrics providing context for the day.

The primary section is the action queue, displaying the top five to seven prioritized items drawn from multiple sources. Portfolio drift alerts from Tamarac (accounts exceeding the firm's 5% absolute drift threshold, showing client name, magnitude of drift, and a link to the rebalancing tool). CRM tasks due today from Redtail (follow-up calls, document collection, meeting preparation). Compliance deadlines approaching within 30 days (annual reviews, disclosure deliveries, profile updates). Client milestones from Redtail (birthdays this week, anniversaries, age-based triggers). Large cash movements detected from Schwab's transaction feed (deposits or withdrawals exceeding $25,000 in the prior business day). Each queue item includes the client name, a one-line description of why it matters, and direct-action buttons (call, email, schedule, view account, create proposal).

The secondary section provides awareness without demanding action: a market summary (major index performance for context during client conversations), the advisor's meeting schedule for the day (pulled from calendar integration), and a client communication log showing the last five outbound contacts with days-since-contact for the advisor's top-tier clients.

**Analysis:**

The critical success factor is integration depth. If the dashboard simply links to Tamarac, Redtail, and Schwab without pulling data into a unified view, it is merely a bookmark page and will not change advisor behavior. True integration means that clicking a drift alert opens Tamarac's rebalancing screen with the client's account pre-loaded, clicking a CRM task opens the Redtail activity record, and clicking a cash movement alert shows the client's full account detail from Schwab with the recent transaction highlighted.

The data refresh cadence should be: market data updates continuously during market hours, portfolio drift and cash movements refresh overnight from custodian EOD feeds, CRM tasks refresh in real-time via API, and compliance deadlines update daily from the compliance calendar. Mobile responsiveness is essential — when an advisor is at a client lunch and receives a push notification about a large deposit, they should be able to view the alert and make a note on their phone without returning to the office.

Adoption measurement is critical for the first 90 days. Track how many advisors log in to the dashboard daily, how many action items are completed through the dashboard versus through the underlying systems directly, and whether advisors report reduced time spent checking multiple systems. If adoption is low, conduct advisor interviews to identify friction points — the most common barriers are slow load times, stale data, and actions that require too many clicks to execute.

### Example 3: Creating an Exception Monitoring Dashboard for Operations

**Scenario:** A $3.5 billion RIA with a five-person operations team processes approximately 200 account-level events per day across two custodians (Schwab and Fidelity). The operations manager wants an exception dashboard that centralizes all items requiring human intervention, replaces the current process of checking multiple custodian portals and email inboxes, and provides aging and escalation visibility to ensure nothing falls through the cracks.

**Design Considerations:**

The exception dashboard should be organized by exception category, with each category displaying a count badge, a sortable detail list, and aging statistics. The categories are:

Reconciliation breaks: position, transaction, and cash discrepancies between the PMS and each custodian, sourced from the daily reconciliation job in Orion. Display break type, account, security (if applicable), PMS value versus custodian value, magnitude of the discrepancy, age in business days, and assigned operations staff member. Flag breaks older than 3 business days in yellow and older than 5 in red. The target is fewer than 10 open breaks at any time and zero breaks older than 5 business days.

Transfer tracking (ACAT and non-ACAT): all pending asset transfers, showing originating and receiving custodian, client name, estimated asset value, submission date, expected completion date, current status, and any NIGO or rejection notices. Transfers taking longer than 10 business days should escalate to the operations manager. Track NIGO rate (percentage of transfers returned as not in good order) and average transfer completion time as process health metrics.

Account opening status: new accounts in various stages of setup at each custodian, showing client name, account type, submission date, current status, and any outstanding documentation requirements. NIGO items should be flagged with the specific deficiency (missing signature, wrong form version, incomplete beneficiary designation) so the assigned CSA can resolve them efficiently.

Billing exceptions: sourced from the billing system's exception report after each billing preview. Display accounts with fees that deviate more than 10% from the prior period, zero-dollar fees, accounts missing from the billing run, and fee-schedule mismatches. Billing exceptions must be resolved before the billing run is approved and custodian debit instructions are submitted.

Custodian communication queue: items requiring follow-up with the custodian — rejected trades, failed fee debits, account restriction inquiries, cost basis disputes, and general service requests. Track submission date, custodian case number (if applicable), and days open.

**Analysis:**

The operations manager should configure a summary banner at the top of the dashboard showing total open exceptions by category, total exceptions opened today, total resolved today, and the current oldest unresolved item. This banner provides instant visibility into whether the team is keeping pace or falling behind.

Weekly trend charts showing exception volume by category help identify systemic issues: a rising reconciliation break count may indicate a custodian feed problem or a PMS configuration issue, while a rising NIGO rate may indicate that the firm's account opening forms need updating or that CSA training is required. Seasonal patterns also emerge from trend data — transfer volumes spike in January (new year rollovers) and April (tax-related movements), and the operations team can prepare by adjusting staffing or pre-staging common documentation.

The dashboard should also generate a daily email digest to the operations manager at end of day, summarizing open items, items resolved, and items approaching their SLA — ensuring that the manager has a complete picture even on days they cannot monitor the dashboard in real-time. SLA targets for each exception category should be prominently displayed: reconciliation breaks resolved within 3 business days, NIGO items resubmitted within 2 business days, transfers escalated if not completed within 10 business days, and billing exceptions resolved before the billing approval deadline. These SLAs provide both team accountability and the basis for process improvement when targets are consistently missed.

## Common Pitfalls

- **Displaying too many metrics on a single screen.** Dashboard overload causes users to ignore the dashboard entirely. Limit each view to 5-7 primary metrics with drill-down available for detail. Executive views need fewer metrics with larger visualizations; operational views can be denser but should still be scannable.
- **Failing to decompose AUM growth into market vs. net new assets.** Reporting total AUM growth without separating market appreciation from organic growth creates a misleading picture. A firm that grew AUM 15% in a year where markets returned 20% actually experienced negative organic growth — a critical distinction that a headline AUM number obscures.
- **Using inconsistent metric definitions across dashboards.** If the executive dashboard defines "active client" differently than the advisor dashboard, metrics will not reconcile and trust in the data erodes. Establish a firm-wide data dictionary with authoritative definitions for every metric, and enforce those definitions in every dashboard.
- **Neglecting data freshness labeling.** When a dashboard panel shows AUM as of yesterday's close but revenue as of last quarter-end, users may combine them in ways that produce nonsensical results. Every panel should display its data-as-of timestamp prominently.
- **Building dashboards without drill-down capability.** A summary number that cannot be explored is a conversation starter but not a decision-making tool. Every aggregate metric should be clickable through to the underlying detail — firm to team to advisor to client to account.
- **Ignoring the mobile experience.** Advisors who cannot access their daily dashboard on a phone or tablet while away from the office will revert to checking individual systems. Design for mobile first and add desktop richness second.
- **Treating all exceptions as equally urgent.** An exception dashboard that shows 200 items with no prioritization or aging is overwhelming. Implement severity levels, SLA-based aging, and escalation rules so the operations team focuses on what matters most.
- **Setting advisor goals without providing progress visibility.** Goals that are set at the beginning of the year and reviewed only at year-end provide no motivational or corrective value. Display goal progress continuously so advisors can self-correct and managers can coach in real-time.
- **Relying on manual data entry for metrics that can be automated.** Meeting counts, client contact frequency, and task completion should be captured automatically from calendar and CRM integration. Manual entry introduces lag, inaccuracy, and advisor resentment.
- **Benchmarking against inappropriate peer groups.** Comparing a $500M RIA's metrics against benchmarks for $5B+ firms produces misleading conclusions. Filter industry benchmarks by firm size, geography, and service model.
- **Failing to act on dashboard insights.** The most common dashboard failure is not technical but behavioral — the dashboard works correctly but no one changes their behavior based on what it shows. Embed dashboards into operational rhythms: reference them in weekly meetings, tie advisor compensation to dashboard-visible goals, and route exceptions into assignment queues.
- **Not revisiting dashboard design after the first year.** Metric priorities shift as the firm evolves. A startup RIA needs acquisition-focused dashboards; a mature firm needs retention and profitability views. Review dashboard relevance annually and retire or replace metrics that no longer drive decisions.

## Cross-References

- **crm-client-lifecycle** (Layer 10, advisory-practice) — CRM data (client segments, activity logs, pipeline, lifecycle stage) is a primary data source for dashboard metrics including client count, attrition, meeting volume, and acquisition funnel analytics.
- **fee-billing** (Layer 10, advisory-practice) — Billing system data feeds revenue metrics, effective fee rates, billing exception counts, and fee-schedule compliance indicators displayed on revenue and exception dashboards.
- **performance-reporting** (Layer 7, wealth-management) — Performance calculation outputs (TWR, MWR, benchmark comparisons) feed dashboard panels showing portfolio-level and firm-level investment results, and performance dispersion across accounts.
- **client-reporting-delivery** (Layer 10, advisory-practice) — Client reporting workflows generate data on report delivery status, portal engagement, and communication frequency that inform advisor productivity and client engagement dashboard sections.
- **portfolio-management-systems** (Layer 10, advisory-practice) — The PMS provides AUM data, position-level holdings, drift analysis, and reconciliation status that power AUM dashboards, drift alert panels, and reconciliation exception views.
- **next-best-action** (Layer 10, advisory-practice) — NBA systems generate the prioritized action queue displayed on the advisor daily dashboard; dashboard adoption metrics (acceptance rate, completion rate) feed NBA effectiveness measurement.
- **operational-risk** (Layer 11, trading-operations) — Operational risk event data (trade errors, settlement failures, process breakdowns) feeds exception dashboards and provides the risk metrics displayed on management and compliance views.
