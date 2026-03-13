---
name: corporate-actions
description: "Process and manage corporate actions from announcement through settlement. Use when handling dividends stock splits reverse splits mergers or spin-offs, managing voluntary elections for tender offers rights offerings or exchange offers, calculating record date and ex-date entitlements under current settlement cycles, building client notification workflows for upcoming corporate actions, collecting and submitting voluntary action elections to DTC or custodians, calculating fractional share handling or proration for reorganization events, adjusting cost basis and tax lots after corporate actions, reconciling expected entitlements against actual receipts, investigating missed or incorrectly processed corporate actions, or designing corporate action processing systems and controls."
---

# Corporate Actions

## Purpose

Guide the processing and management of corporate actions in securities operations. Covers mandatory actions (dividends, splits, mergers), voluntary actions (tender offers, rights offerings, optional dividends), corporate action lifecycle from announcement through payment/settlement, record date and ex-date mechanics, client notification, election processing, and impact on portfolio accounting and reconciliation. Enables building or operating corporate actions processing that is accurate, timely, and properly reflected across all systems.

## Layer

12 — Client Operations (Account Lifecycle & Servicing)

## Direction

both

## When to Use

- Processing or validating mandatory corporate actions such as cash dividends, stock splits, reverse splits, mergers, or spin-offs
- Managing voluntary corporate action elections including tender offers, rights offerings, exchange offers, or optional dividends
- Determining record date and ex-date logic for entitlement calculation under current settlement cycles
- Building or reviewing client notification workflows for upcoming corporate actions
- Collecting and submitting voluntary action elections to DTC or custodians
- Calculating entitlements, fractional share handling, or proration for reorganization events
- Adjusting cost basis, tax lots, and position quantities after corporate actions
- Reconciling expected entitlements against actual receipts from depositories or agents
- Investigating missed or incorrectly processed corporate actions
- Designing or improving corporate action processing systems and controls

## Core Concepts

### 1. Corporate Action Types

Corporate actions are events initiated by a company that affect its securities. They fall into four broad categories based on the level of shareholder participation required.

**Mandatory Actions.** These occur automatically for all holders of record and require no election. The holder receives the entitlement without taking any action.
- Cash dividends (regular, special, interim, final)
- Stock dividends (bonus shares distributed pro rata)
- Stock splits (forward splits increase share count, reduce price proportionally)
- Reverse stock splits (decrease share count, increase price proportionally)
- Mergers with fixed terms (cash-only or fixed-ratio stock consideration)
- Spin-offs (new entity shares distributed to parent company holders)
- Name changes and symbol changes (CUSIP/ISIN may change)

**Mandatory with Choice.** The action will occur regardless, but the holder may choose among alternatives. If no election is made, a default option applies.
- Stock or cash dividend election (holder chooses stock or cash; default is typically cash)
- Merger consideration election (cash, stock, or mixed; subject to proration if oversubscribed)

**Voluntary Actions.** The holder may choose whether to participate. Non-participation means the holder retains their existing position unchanged.
- Tender offers (issuer or third party offers to purchase shares at a specified price)
- Rights offerings (existing holders receive rights to purchase new shares at a discount)
- Exchange offers (holders may exchange existing securities for different securities)
- Consent solicitations (holders asked to consent to changes in bond covenants or terms)
- Dutch auction tender offers (holders specify price within a range)
- Odd-lot tender offers (small holders may tender at favorable terms)

**Information-Only Events.** No direct financial impact on positions, but require tracking and communication.
- Annual and special meeting notifications
- Proxy vote solicitations
- Credit rating changes
- Regulatory filings (e.g., issuer SEC filings affecting the security)

### 2. Corporate Action Lifecycle

Every corporate action follows a sequence from announcement through final settlement. Processing accuracy depends on disciplined execution at each stage.

**Announcement.** The issuer or its agent announces the corporate action. Data is disseminated through DTCC (via its Corporate Actions product suite, including GCA — Global Corporate Actions), market data vendors (Bloomberg, Refinitiv, ICE Data Services), and exchange filings (SEC EDGAR for US issuers). Multiple vendor sources may report different details or timings, requiring scrubbing and cross-referencing.

**Data Scrubbing and Validation.** The operations team or automated system receives the raw announcement and validates key fields: event type, security identifiers (CUSIP, ISIN, SEDOL), record date, ex-date, payment/effective date, terms (ratio, price, consideration), election options and deadlines, and default election. Discrepancies between vendor sources must be resolved before the event is set up in internal systems. A "golden source" hierarchy is established (e.g., DTCC as primary for US events, then Bloomberg, then Refinitiv).

**System Setup.** The validated event is entered into the corporate actions processing system. This includes mapping the event to affected accounts, calculating preliminary entitlements, and flagging accounts that require client notification (for voluntary or mandatory-with-choice events).

**Client Notification.** For voluntary and mandatory-with-choice events, clients (or their advisors) must be notified with sufficient lead time to make informed elections. Notification includes event description, options available, default election, election deadline, and any relevant analysis (e.g., economic comparison of tender price vs. market price).

**Election Collection and Submission.** For voluntary events, elections are collected from clients, validated against their positions, aggregated, and submitted to DTC (via PTOP or ATOP systems) or the custodian before the election deadline. Late elections may be rejected or subject to penalty.

**Entitlement Calculation.** On the record date, the system determines which accounts hold the affected security and calculates entitlements based on position size and event terms (ratio, rate, price). For fractional shares, the system applies the issuer's fractional share policy (cash-in-lieu, round up, round down).

**Settlement and Payment.** On the payment or effective date, the entitlements are settled: cash is credited, new shares are delivered, old shares are removed, or positions are adjusted. The depository (DTC for US securities) processes bulk entitlements and allocates to participants (custodians/broker-dealers), who in turn allocate to beneficial owner accounts.

**Post-Settlement Reconciliation.** Actual receipts from the depository or agent are reconciled against expected entitlements. Discrepancies (short pays, over-deliveries, missing allocations) are investigated and resolved through claims processes.

### 3. Record Date and Ex-Date Mechanics

The relationship between record date, ex-date, and settlement cycle is fundamental to correct entitlement processing.

**Record Date.** The date on which the issuer (via its transfer agent) determines the holders of record who are entitled to the corporate action. Only holders whose names appear on the shareholder register as of the close of business on the record date receive the entitlement.

**Ex-Date.** The date on or after which the security trades without the entitlement. Under the current US settlement cycle of T+1, the ex-date is typically set to the record date itself (T+0 equals the record date when settlement is T+1), because a trade executed on the record date will settle T+1, meaning the buyer will not be the holder of record on the record date. In practice, exchange rules set the ex-date to one business day before the record date for most events, ensuring trades settling after the record date do not carry the entitlement.

**Cum-Dividend vs. Ex-Dividend.** A security trading "cum-dividend" (before the ex-date) entitles the buyer to the upcoming dividend. A security trading "ex-dividend" (on or after the ex-date) does not. On the ex-date, the market price typically drops by approximately the amount of the dividend or the value of the entitlement.

**Due Bills.** When a trade is executed between the ex-date and the record date under circumstances where normal settlement would result in the wrong party receiving the entitlement, a due bill may be issued. The due bill obligates the seller to pass the entitlement to the buyer. Due bills are more common in complex reorganization events and when settlement cycles change.

**International Variations.** Ex-date conventions differ by market. Some markets set the ex-date two business days before the record date (under T+2 settlement). Cross-border corporate actions require awareness of each market's convention.

### 4. Dividend Processing

Dividends are the most frequent corporate action and require systematic processing across declaration, record, ex, and payment dates.

**Cash Dividend Lifecycle.**
- Declaration date: Board declares dividend amount, record date, and payment date
- Ex-date: Security begins trading without entitlement to the dividend
- Record date: Shareholder register is fixed; holders of record are entitled
- Payment date: Dividend cash is distributed to entitled holders

**Dividend Rate Application.** The entitlement is calculated as: shares held on record date multiplied by the per-share dividend rate. For ADRs (American Depositary Receipts), the dividend is declared in the foreign currency and converted to USD, less ADR depositary fees and foreign withholding taxes.

**Stock Dividends.** Instead of cash, additional shares are distributed. A 5% stock dividend means 5 new shares per 100 held. Fractional shares result when the position is not evenly divisible. The issuer's policy determines whether fractional shares are paid in cash-in-lieu, rounded, or accumulated.

**Special and Extra Dividends.** One-time or irregular dividends declared outside the normal dividend schedule. These may indicate unusual income, asset sales, or capital return. They require careful classification for tax reporting purposes (ordinary income vs. return of capital).

**Return of Capital (ROC).** A distribution classified as return of capital is not taxable income in the period received but instead reduces the holder's cost basis. When cost basis reaches zero, further ROC is treated as capital gain. Correct classification requires the issuer's year-end reclassification notice, which may not be available until January or February of the following year. Preliminary estimates may need to be revised.

**Qualified vs. Non-Qualified Dividends.** US tax law distinguishes between qualified dividends (taxed at capital gains rates) and non-qualified (ordinary income rates). Qualification depends on the issuer being a US corporation or a qualified foreign corporation, and the holding period requirement (held for more than 60 days during the 121-day period surrounding the ex-date). This distinction affects tax reporting on Form 1099-DIV.

**Foreign Withholding Tax.** Dividends from foreign issuers may be subject to withholding tax by the source country. Treaty rates may reduce the standard withholding rate. The withholding is reported on Form 1099-DIV and may be eligible for a foreign tax credit on the client's tax return. ADR holders face an additional layer of complexity as the depositary bank handles the withholding and may not always apply the optimal treaty rate.

**Dividend Reinvestment (DRIP).** Clients enrolled in dividend reinvestment plans have their cash dividends automatically used to purchase additional shares. DRIP processing requires: calculating the reinvestment amount (net of any fees), determining the reinvestment price (often the closing price on the payment date, sometimes at a discount), purchasing whole and fractional shares, and creating new tax lots with the reinvestment date and price as the acquisition date and cost basis.

**ADR Fees.** ADR depositary banks charge periodic fees (typically $0.01-$0.05 per share annually) that are often deducted from dividend payments. These fees must be tracked separately from the gross dividend for accurate tax reporting.

### 5. Reorganization Events

Reorganizations alter the fundamental structure of the security — share count, issuer identity, or security type.

**Stock Splits.** A forward split increases the number of shares outstanding while proportionally reducing the per-share price. A 2-for-1 split doubles the share count and halves the price. Processing requires:
- Multiplying each account's position by the split ratio
- Dividing the per-share cost basis by the split ratio (total cost basis is unchanged)
- Updating pending orders and limit prices
- Handling fractional shares per the issuer's policy
- Adjusting option contracts (strike prices and contract multipliers)

**Reverse Stock Splits.** A reverse split reduces the share count and increases the per-share price (e.g., 1-for-10 reverse split converts 1,000 shares into 100 shares at 10x the price). Reverse splits frequently generate fractional shares, which are typically cashed out. This cash-out creates a taxable event for the fractional portion.

**Mergers and Acquisitions.** When Company A acquires Company B, holders of Company B receive consideration that may be:
- All cash: Position in Company B is removed, cash is credited. Taxable event — gain or loss is recognized.
- All stock: Position in Company B is replaced with shares of Company A at the exchange ratio. May qualify as a tax-free reorganization (deferred gain/loss).
- Mixed (cash and stock): Combination of the above. Cash portion ("boot") is taxable; stock portion may be tax-deferred.
- Subject to proration: When the acquirer offers a choice of cash or stock but limits the total cash or stock available, elections are prorated so that each electing holder receives a proportional share of the available pool.

**Spin-Offs.** The parent company distributes shares of a subsidiary as a new, independent company. Processing requires:
- Allocating the parent's cost basis between the parent and spin-off based on relative fair market values on the distribution date (the issuer typically publishes the allocation percentages via IRS Form 8937)
- Creating new positions for the spin-off shares
- Updating the parent position's cost basis (reduced by the amount allocated to the spin-off)
- Handling fractional spin-off shares (cash-in-lieu)
- Adjusting tax lots individually — each parent tax lot must be split proportionally

**Tender Offers.** A tender offer is an invitation to shareholders to sell (tender) their shares at a specified price, usually at a premium to market. Processing includes:
- Notifying clients of the offer terms, premium to market, conditions, and deadline
- Collecting elections to tender or not tender
- Submitting tendered shares to DTC or the depositary agent
- Handling proration if the offer is oversubscribed (more shares tendered than the offeror will accept)
- Settling accepted tenders (removing shares, crediting cash)
- Returning un-accepted shares in proration scenarios
- Recognizing capital gains or losses on tendered shares

**Rights Offerings.** Existing holders receive rights to purchase additional shares at a discounted subscription price. Each right typically entitles the holder to purchase a specified number of new shares. Processing includes:
- Distributing rights to holders of record
- Notifying clients of subscription terms, pricing, and deadline
- Collecting subscription elections and payment
- Processing oversubscription (if the offering allows additional subscriptions beyond the base entitlement)
- Handling unexercised rights (which expire worthless or may be sold on the open market if the rights are transferable)
- Creating new positions for subscribed shares with the subscription price as cost basis

### 6. Voluntary Action Election Processing

Voluntary actions require a structured process to ensure every affected client is notified, elections are collected accurately, and submissions are made on time.

**Client Notification Workflow.** Upon validating a voluntary event, the system generates notifications to all affected clients or their advisors. Notifications include: event summary, available options with economic analysis (e.g., tender price vs. current market price, subscription price vs. market price), default election if no response is received, election deadline (internal deadline, set earlier than the DTC deadline to allow processing time), and instructions for submitting the election.

**Default Election Rules.** Firms must establish and disclose default election policies. Common defaults:
- Tender offers: Default is typically "do not tender" (preserves the client's position)
- Mandatory with choice (stock/cash dividend): Default is typically cash
- Rights offerings: Default is typically "do not subscribe" (rights expire)
- Exchange offers: Default is typically "do not exchange"

Defaults should be documented in the client agreement or disclosed in the notification. The client must have adequate time to override the default.

**Election Deadline Management.** The critical path for voluntary actions is the election deadline chain:
- DTC deadline (the hard deadline imposed by the depository)
- Custodian deadline (typically one business day before the DTC deadline)
- Internal firm deadline (typically one to two business days before the custodian deadline)
- Client notification deadline (allowing sufficient time for clients to respond — typically at least five business days before the internal deadline)

Missing any deadline in this chain can result in the default election being applied or, worse, the election being rejected entirely.

**Election Submission.** Aggregated elections are submitted to DTC (via its PTOP/ATOP systems for US securities) or directly to the custodian. The submission must specify: security identifier, event identifier, account or participant details, number of shares electing each option, and any conditions or contingencies.

**Over-Election and Proration.** When a voluntary action has a cap on participation (e.g., a tender offer limited to 30% of outstanding shares), total elections across all holders may exceed the cap. The agent prorates elections proportionally. Firms must then prorate the accepted quantity back to individual client accounts, typically pro rata by the number of shares each client elected to tender. Fractional share proration results are rounded, with rounding methodology documented and applied consistently.

**Late Election Handling.** Elections received after the firm's internal deadline but before the custodian or DTC deadline may be processed on a best-efforts basis. Elections received after the DTC deadline are generally rejected. Firms should log all late elections, the reason for lateness, and whether the election was ultimately accepted or rejected, for risk management and client communication purposes.

### 7. Impact on Portfolio Accounting

Corporate actions directly affect position quantities, cost basis, cash balances, and derived calculations across all portfolio accounting and reporting systems.

**Cost Basis Adjustments.**
- Stock splits: Per-share cost basis is divided by the split ratio; total cost basis is unchanged.
- Reverse splits: Per-share cost basis is multiplied by the reverse ratio; total cost basis is unchanged for the non-fractional portion. Cash-in-lieu for fractional shares creates a recognized gain or loss.
- Mergers (tax-free): Cost basis in the acquired company transfers to the acquiring company shares received. Per-share basis = old total basis / new shares received.
- Mergers (taxable): Cost basis in the new shares is the fair market value at the time of the merger. Gain or loss is recognized on the old shares.
- Spin-offs: Parent cost basis is allocated between parent and spin-off based on the issuer's published allocation ratio. Each original tax lot is split proportionally.
- Return of capital: Cost basis is reduced by the ROC amount per share. If ROC exceeds basis, the excess is capital gain.

**Position Quantity Updates.** Splits, reverse splits, stock dividends, mergers, and spin-offs all change the number of shares held. The processing system must update positions atomically — removing old positions and creating new positions in a single transaction to avoid transient states that would cause reconciliation breaks.

**Cash Posting.** Cash dividends, cash-in-lieu of fractional shares, merger cash consideration, tender offer proceeds, and return of capital distributions all generate cash entries. Posting must occur on the correct date (payment date for dividends, settlement date for mergers and tenders) and to the correct account.

**Accrued Income Adjustments.** For bonds, corporate actions such as issuer defaults, early redemptions, or consent solicitations may affect accrued interest calculations. The system must recognize any accrued interest up to the effective date and adjust subsequent accrual.

**Unrealized Gain/Loss Recalculation.** After any cost basis adjustment, unrealized gains and losses must be recalculated across all affected tax lots. This affects client reporting, tax projections, and rebalancing decisions.

**Tax Lot Updates.** Each corporate action must be applied at the individual tax lot level, not at the aggregate position level. A client who acquired shares across multiple dates and prices will have different cost basis amounts per lot, and the corporate action must respect these differences. For a spin-off, every tax lot in the parent position generates a corresponding tax lot in the spin-off position.

**Performance Calculation Impact.** Corporate actions must be properly reflected in performance calculations to avoid distorting returns. Dividends are investment income. Stock splits and reverse splits are non-economic events that should not create artificial gains or losses. Mergers and spin-offs may require linking old and new securities in the performance calculation engine. The Modified Dietz or daily valuation method must account for corporate action cash flows on the correct dates.

### 8. Corporate Action Risk and Controls

The complexity and time-sensitivity of corporate actions make them a significant source of operational risk. A robust control framework is essential.

**Announcement Sourcing Accuracy.** Relying on a single data source increases the risk of processing an event based on incorrect terms. Best practice is to cross-reference at least two independent sources (e.g., DTCC and Bloomberg) and flag discrepancies for manual review.

**Processing Deadline Management.** A deadline calendar or tickler system must track every open corporate action with its key dates (ex-date, record date, election deadline, payment date). Automated alerts should fire at defined intervals before each deadline (e.g., 5 business days, 2 business days, 1 business day before election deadline).

**Entitlement Reconciliation.** After payment or settlement, expected entitlements (calculated from positions held on the record date) must be reconciled against actual receipts from the depository or custodian. Differences may arise from: positions settling after the record date, DTC claim adjustments, agent errors, or rounding differences. All variances must be investigated and resolved.

**Voluntary Action Election Verification.** Before submission, elections should be verified against client positions (cannot elect more shares than held), client instructions (election matches what the client requested), and firm policies (no conflicts of interest, appropriate for the client's investment profile). A maker-checker process (one person prepares, another reviews and approves) reduces error risk.

**Missed Corporate Action Detection.** A periodic scan should compare positions held against a feed of announced corporate actions to detect any events that were not processed. Missed dividends are the most common gap, particularly for thinly traded or foreign securities. A reconciliation of expected vs. received income at the account level is an effective catch-all control.

**Error Correction Procedures.** When a corporate action is processed incorrectly (wrong ratio, wrong date, wrong accounts), the correction process must: reverse the incorrect entries, apply the correct entries, notify affected clients if the error impacted their statements or tax reporting, and document the root cause and remediation steps. All corrections should be reviewed and approved by a supervisor.

**Segregation of Duties.** Setup, approval, and submission of corporate actions should involve at least two individuals. The person who enters the event parameters should not be the same person who approves the processing. Incorrectly processed corporate actions can flow through to Form 1099-B (cost basis reporting), Form 1099-DIV (dividend income), and client statements. Errors caught after tax forms are issued require corrected filings, which are operationally burdensome and damage client confidence.

## Worked Examples

### Example 1: Processing a Cash-and-Stock Merger Across Thousands of Client Accounts

**Scenario:** Acquirer Corp announces the acquisition of Target Inc. The merger terms are: for each share of Target Inc, shareholders receive $25.00 in cash plus 0.4 shares of Acquirer Corp stock. The merger is expected to close on March 15. Target Inc has CUSIP 876543210. Acquirer Corp has CUSIP 012345678. The firm holds Target Inc across 3,200 client accounts with positions ranging from 10 to 50,000 shares. Total firm-wide position is 4.8 million shares. Acquirer Corp's closing price on March 15 is $80.00.

**Design Considerations:**
- The merger terms are fixed (no election or proration), making this a mandatory action.
- Mixed consideration (cash + stock) means the tax treatment depends on the IRS characterization. Assume the merger qualifies as a reorganization under IRC Section 368, meaning the stock portion is tax-deferred but the cash portion ("boot") is taxable.
- Fractional shares of Acquirer Corp will be paid in cash-in-lieu at the closing price on the effective date.
- The firm must process this across two custodians (Schwab and Fidelity) and a self-clearing platform.

**Analysis:**

Step 1 — Pre-Event Validation:
Verify merger terms across DTCC, Bloomberg, and the issuer's proxy filing. Confirm: consideration per share ($25.00 cash + 0.4 shares), effective date (March 15), fractional share policy (cash-in-lieu at market), CUSIP changes, and tax treatment (Section 368 reorganization). Discrepancy check: Bloomberg initially reported the ratio as 0.40; DTCC reported 0.4000. These are consistent. No discrepancy.

Step 2 — Position Snapshot on Record Date:
Extract all accounts holding Target Inc as of the record date. For mergers, the record date is typically the effective date. Total: 3,200 accounts, 4,800,000 shares. Validate against custodian position files. Two accounts show discrepancies due to pending settlements — flag for manual review after settlement.

Step 3 — Entitlement Calculation (Per Account Example):
Client account holds 1,500 shares of Target Inc with the following tax lots:
- Lot 1: 800 shares, acquired 2019-06-15, cost basis $32.00/share ($25,600 total)
- Lot 2: 700 shares, acquired 2021-11-03, cost basis $38.00/share ($26,600 total)

Cash entitlement: 1,500 shares x $25.00 = $37,500.00.
Stock entitlement: 1,500 shares x 0.4 = 600.0 shares of Acquirer Corp (no fractional shares in this case).

For an account holding 113 shares:
Stock entitlement: 113 x 0.4 = 45.2 shares. Whole shares: 45. Fractional portion: 0.2 shares. Cash-in-lieu: 0.2 x $80.00 = $16.00.

Step 4 — Cost Basis Allocation (Section 368 Reorganization):
Under Section 368, the total cost basis in Target Inc shares carries over to the Acquirer Corp shares and any boot (cash) received. The allocation requires determining the relative fair market values of the stock and cash components.

Total consideration per share: $25.00 cash + 0.4 x $80.00 stock = $25.00 + $32.00 = $57.00.
Cash percentage: $25.00 / $57.00 = 43.86%.
Stock percentage: $32.00 / $57.00 = 56.14%.

For Lot 1 (800 shares, $25,600 total basis):
Basis allocated to cash: $25,600 x 43.86% = $11,228.07. Cash received: 800 x $25.00 = $20,000.00. Taxable gain on cash portion: $20,000.00 - $11,228.07 = $8,771.93.
Basis allocated to stock: $25,600 x 56.14% = $14,371.93. Shares received: 800 x 0.4 = 320 shares. Per-share basis: $14,371.93 / 320 = $44.91.

For Lot 2 (700 shares, $26,600 total basis):
Basis allocated to cash: $26,600 x 43.86% = $11,666.76. Cash received: 700 x $25.00 = $17,500.00. Taxable gain on cash portion: $17,500.00 - $11,666.76 = $5,833.24.
Basis allocated to stock: $26,600 x 56.14% = $14,933.24. Shares received: 700 x 0.4 = 280 shares. Per-share basis: $14,933.24 / 280 = $53.33.

Step 5 — System Processing:
For each of the 3,200 accounts, the processing engine executes atomically:
1. Remove the Target Inc position (all lots).
2. Credit cash for the cash component of the merger consideration.
3. Create new Acquirer Corp position with correctly allocated tax lots, preserving original acquisition dates for holding period purposes.
4. Credit cash-in-lieu for any fractional shares.
5. Record the taxable gain on the cash (boot) component per lot.

Step 6 — Post-Settlement Reconciliation:
Compare expected entitlements (cash and shares) against actual receipts from DTC. For Schwab-custodied accounts, compare the Schwab corporate action confirmation against the firm's calculations. Investigate any discrepancy. Common issues: pending settlements that altered the record-date position, DTC claiming adjustments for trades settling after the record date, and rounding differences on cash-in-lieu calculations.

### Example 2: Managing a Tender Offer with Oversubscription and Proration

**Scenario:** MegaCorp launches a self-tender offer to repurchase up to 10 million shares of its common stock at $50.00 per share (current market price: $46.50). The offer is open for 20 business days. The firm holds MegaCorp across 1,400 client accounts totaling 2.1 million shares. Clients may elect to tender all, some, or none of their shares.

**Design Considerations:**
- This is a voluntary action — clients must affirmatively elect to participate.
- The tender price represents a 7.5% premium to market, which may be attractive but clients must consider their investment thesis for holding MegaCorp.
- If total shares tendered across all holders exceed 10 million, the company will prorate acceptance on a pro-rata basis (with odd-lot priority for holders of fewer than 100 shares).
- The firm's internal election deadline is 3 business days before the DTC deadline to allow for aggregation and submission.
- Tendered shares that are accepted will generate a taxable event (capital gain or loss based on cost basis vs. $50.00 tender price).

**Analysis:**

Step 1 — Client Notification (Day 1-2 After Announcement):
Generate notifications to all 1,400 affected accounts. Each notification includes: tender price ($50.00), premium to market (7.5%), maximum shares the company will accept (10 million), election options (tender all, tender a specified number, or do not tender), the firm's default election (do not tender), internal election deadline, and a reminder that proration may apply if the offer is oversubscribed.

For advisory accounts, the advisor receives the notification and decides on behalf of the client within the scope of the advisory agreement. For self-directed accounts, the client receives the notification directly.

Step 2 — Election Collection (Days 2-17):
Elections trickle in over the offer period. The operations team tracks election status:
- 620 accounts elect to tender all shares (1,050,000 shares)
- 180 accounts elect to tender a portion of their shares (310,000 shares)
- 450 accounts elect not to tender
- 150 accounts have not responded by Day 15

For the 150 non-respondents, the firm sends a reminder notification on Day 15. By the internal deadline (Day 17), an additional 90 accounts respond (60 elect to tender, 30 elect not to tender). The remaining 60 non-respondents receive the default election of "do not tender."

Final election tally:
- Total shares elected to tender: 1,050,000 + 310,000 + 95,000 (from the 60 late responders) = 1,455,000 shares
- Total shares not tendering: remaining position

Step 3 — Election Submission (Day 17-18):
The firm submits its aggregated election of 1,455,000 shares to DTC via the PTOP system. The submission specifies the firm's participant number, the event ID, and the total shares tendered. At the account level, the firm maintains its own records of per-client elections.

Step 4 — Proration (After Expiration, Day 20+):
The tender offer expires. Total shares tendered across all holders: 18 million shares (oversubscribed by 80%). The company will accept 10 million shares, so the proration factor is 10,000,000 / 18,000,000 = 55.56%.

Odd-lot holders (fewer than 100 shares) are accepted in full per the offer terms. The firm identifies 45 odd-lot accounts totaling 2,800 shares — all accepted without proration.

For non-odd-lot accounts, the proration factor of 55.56% is applied:
- Example: Client elected to tender 5,000 shares. Accepted: 5,000 x 55.56% = 2,778 shares. Returned: 2,222 shares.
- Rounding: The agent rounds accepted shares down to the nearest whole share. Fractional shares are not accepted.

Firm-wide proration: 1,455,000 shares elected, less 2,800 odd-lot shares = 1,452,200 non-odd-lot shares. Accepted: 1,452,200 x 55.56% = 807,162 shares (rounded). Returned: 645,038 shares plus the odd-lot difference.

Step 5 — Settlement Processing:
For each account with accepted shares:
1. Remove the tendered and accepted shares from the position.
2. Credit cash: accepted shares x $50.00.
3. Return the un-accepted (prorated) shares to the position.
4. Calculate realized gain or loss per tax lot on the accepted shares.

Example for one account:
- Pre-tender position: 5,000 shares, single tax lot, cost basis $42.00/share.
- Elected to tender: 5,000 shares. Accepted after proration: 2,778 shares. Returned: 2,222 shares.
- Cash received: 2,778 x $50.00 = $138,900.00.
- Cost basis of accepted shares: 2,778 x $42.00 = $116,676.00.
- Realized gain: $138,900.00 - $116,676.00 = $22,224.00.
- Remaining position: 2,222 shares at $42.00/share cost basis (unchanged).

Step 6 — Post-Settlement Activities:
Reconcile DTC settlement against expected entitlements. Verify that prorated quantities match the agent's published proration factor. Communicate final results to clients, including: shares accepted, shares returned, cash received, and realized gain/loss. Update tax lot records and performance systems.

### Example 3: Handling a Spin-Off with Fractional Shares and Cost Basis Allocation

**Scenario:** ParentCo announces it will spin off its technology division as NewTechCo. Distribution ratio: 1 share of NewTechCo for every 5 shares of ParentCo held on the record date of June 10. Fractional shares will be aggregated and sold on the open market, with cash-in-lieu distributed to holders. ParentCo currently trades at $120.00. NewTechCo is expected to begin trading at approximately $30.00. The IRS Form 8937 published by ParentCo allocates 80% of the pre-spin cost basis to ParentCo and 20% to NewTechCo.

The firm holds ParentCo across 2,500 accounts totaling 3.6 million shares.

**Design Considerations:**
- This is a mandatory action — no election is required.
- The 1:5 ratio will generate fractional shares for any position not evenly divisible by 5.
- Cost basis allocation must be applied at the individual tax lot level, not the aggregate position level.
- The spin-off creates a new security (NewTechCo) that must be set up in all systems before the distribution date.
- Performance calculation engines must link the ParentCo and NewTechCo positions to avoid distorting returns on the distribution date.

**Analysis:**

Step 1 — Pre-Event Setup:
Set up NewTechCo as a new security in the master security file: assign or receive the new CUSIP, establish pricing feeds, configure the security in the portfolio accounting system, and set up trading capabilities (the security may trade on a "when-issued" basis before the distribution date).

Step 2 — Position Analysis:
Extract all ParentCo positions as of the record date (June 10).
- Total shares: 3,600,000. Distribution ratio: 1:5. Total NewTechCo shares to distribute: 720,000.
- Accounts with positions evenly divisible by 5: 1,850 accounts (no fractional shares).
- Accounts with fractional share remainders: 650 accounts.

Fractional share example: Account holds 1,237 shares of ParentCo. NewTechCo entitlement: 1,237 / 5 = 247.4 shares. Whole shares: 247. Fractional: 0.4 shares. Total fractional shares across all 650 accounts are aggregated into whole shares, sold on the market, and the cash proceeds are allocated back to each account proportionally.

Step 3 — Cost Basis Allocation:
The issuer's Form 8937 specifies: 80% of pre-spin cost basis remains with ParentCo, 20% is allocated to NewTechCo.

Example for one account with two tax lots:
- Lot 1: 600 shares of ParentCo, acquired 2018-03-20, cost basis $85.00/share ($51,000 total).
- Lot 2: 637 shares of ParentCo, acquired 2022-08-11, cost basis $105.00/share ($66,885 total).

Lot 1 cost basis adjustment:
ParentCo retained basis: $51,000 x 80% = $40,800.00. New per-share basis: $40,800 / 600 = $68.00.
NewTechCo allocated basis: $51,000 x 20% = $10,200.00. NewTechCo shares from Lot 1: 600 / 5 = 120 shares. Per-share basis: $10,200 / 120 = $85.00.
Acquisition date for NewTechCo lot: inherits the original date of 2018-03-20 (holding period tacks).

Lot 2 cost basis adjustment:
ParentCo retained basis: $66,885 x 80% = $53,508.00. New per-share basis: $53,508 / 637 = $84.00.
NewTechCo allocated basis: $66,885 x 20% = $13,377.00. NewTechCo shares from Lot 2: 637 / 5 = 127.4 shares. Whole shares: 127. Fractional: 0.4 shares.

For the fractional 0.4 shares:
Basis of fractional portion: ($13,377.00 / 127.4) x 0.4 = $42.00 (approximately).
Cash-in-lieu received: 0.4 x $30.00 (market price at sale) = $12.00.
Realized loss on fractional share: $12.00 - $42.00 = -$30.00 (loss).

NewTechCo Lot 2 (whole shares only): 127 shares, basis = $13,377.00 - $42.00 = $13,335.00, per-share basis = $105.00. Acquisition date: 2022-08-11 (holding period tacks).

Step 4 — System Processing:
For each of the 2,500 accounts:
1. Reduce ParentCo per-share cost basis to 80% of original (per lot).
2. Create NewTechCo position with allocated tax lots (20% of original basis per lot), preserving original acquisition dates.
3. For accounts with fractional NewTechCo shares, record the cash-in-lieu amount and realized gain/loss on the fractional portion.
4. Verify that the sum of (adjusted ParentCo basis + NewTechCo basis + any fractional share basis used) equals the original pre-spin ParentCo basis for each lot.

Step 5 — Post-Processing Validation:
Run a firm-wide reconciliation:
- Total NewTechCo whole shares distributed should equal the total calculated entitlement minus aggregated fractional shares.
- Total cost basis across ParentCo (adjusted) + NewTechCo + fractional share basis should equal the total pre-spin ParentCo cost basis.
- Verify that no tax lot has a negative cost basis or an unreasonable per-share basis.
- Check that performance reports for the distribution date show a combined value (ParentCo + NewTechCo) approximately equal to the pre-spin ParentCo value, confirming no artificial gain or loss was created by the event.

Step 6 — Ongoing Monitoring:
The issuer's Form 8937 with the final allocation percentages may not be available until several weeks or months after the spin-off. If the firm used preliminary estimates (e.g., based on when-issued trading), the cost basis allocation must be revised when the final Form 8937 is published. This revision may require amended tax lot records and, if tax forms have already been issued, corrected 1099-Bs.

## Common Pitfalls

- **Using stale or single-source announcement data.** Processing a corporate action based on incorrect terms (wrong ratio, wrong date, wrong consideration) cascades errors across every affected account. Always cross-reference at least two independent sources and resolve discrepancies before setup.
- **Missing the ex-date/record date relationship.** Applying the wrong ex-date convention (e.g., using T+2 rules in a T+1 settlement market) results in incorrect entitlement calculations. The ex-date convention must match the current settlement cycle of the relevant market.
- **Failing to process at the tax lot level.** Applying cost basis adjustments at the aggregate position level instead of per tax lot produces incorrect cost basis for individual lots, leading to errors in realized gain/loss when shares are eventually sold.
- **Ignoring fractional share tax consequences.** Cash-in-lieu of fractional shares is a taxable event. Failing to calculate and report the gain or loss on fractional portions is a tax reporting error.
- **Missing voluntary action election deadlines.** Internal deadlines must be set sufficiently before custodian and DTC deadlines. A missed deadline results in the default election being applied, which may not be in the client's interest.
- **Not reconciling entitlements against actual receipts.** Assuming that expected entitlements equal actual receipts without verification allows errors to persist. DTC claiming, pending settlements, and agent errors all create discrepancies that require investigation.
- **Incorrect return-of-capital classification.** Treating return of capital as ordinary income (or vice versa) overstates taxable income and produces incorrect 1099-DIV reporting. Final reclassification data from the issuer may not be available until the following January.
- **Applying split ratios to cost basis incorrectly.** In a stock split, the total cost basis must remain unchanged; only the per-share basis changes. Errors here create phantom gains or losses.
- **Overlooking DRIP lots in reorganization processing.** Small DRIP lots with unique cost bases are easily missed when processing mergers or spin-offs, leading to residual positions or incorrect basis calculations.
- **Failing to update pending orders after splits or reverse splits.** Open limit orders and stop orders must have their prices and quantities adjusted after a split. Unadjusted orders may execute at unintended prices.
- **Processing the same event twice.** Duplicate processing (e.g., from two different vendor feeds) doubles entitlements and creates reconciliation breaks. Deduplication controls based on event identifiers must be in place.
- **Not communicating proration results to clients.** After a prorated tender offer, clients need to know how many shares were accepted, how many were returned, and the realized gain/loss. Delayed or missing communication erodes trust.

## Cross-References

- **reconciliation** — Entitlement reconciliation against depository and custodian records; position reconciliation after corporate action processing.
- **account-maintenance** — Account-level updates triggered by corporate actions, including position and cash balance changes.
- **settlement-clearing** — Settlement mechanics for corporate action entitlements, DTC processing, and claiming.
- **tax-efficiency** — Tax implications of corporate actions: cost basis adjustments, gain/loss recognition, qualified dividend determination, and return-of-capital treatment.
- **performance-attribution** — Impact of corporate actions on portfolio return calculations and attribution analysis.
- **books-and-records** — Recordkeeping requirements for corporate action processing, elections, and entitlements.
- **portfolio-management-systems** — System integration for corporate action data flow, position updates, and cost basis adjustments.
- **operational-risk** — Corporate action processing as a key operational risk area; controls, deadline management, and error detection.
