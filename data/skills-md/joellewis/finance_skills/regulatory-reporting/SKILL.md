---
name: regulatory-reporting
description: "Guide regulatory filing obligations and deadlines for investment advisers, broker-dealers, and large traders. Use when the user asks about Form PF filing thresholds, 13F institutional holdings reports, 13H large trader filings, Form ADV amendment timing, FOCUS report preparation, blue sheet requests, CAT reporting infrastructure, or FINRA short interest and TRACE reporting. Also trigger when users mention 'filing deadline calendar', 'do we need to file Form PF', 'crossed the $100M 13F threshold', 'annual updating amendment', 'CAT clock synchronization', 'how to respond to a blue sheet request', 'FOCUS report errors', or ask which regulatory filings a firm must make and when."
---

# Regulatory Reporting

## Purpose
Guide the understanding and execution of regulatory filing obligations for investment advisers, broker-dealers, and large traders. This skill covers Form PF, 13F and 13H filings, Form ADV amendments, FOCUS reports, electronic blue sheets, CAT (Consolidated Audit Trail) reporting, SAR/CTR filing mechanics, and FINRA reporting requirements — enabling a user or agent to design compliant reporting workflows, meet filing deadlines, and avoid enforcement exposure from late, incomplete, or erroneous submissions.

## Layer
9 — Compliance & Regulatory Guidance

## Direction
prospective

## When to Use
- Determining which regulatory filings a firm must make and on what schedule
- Setting up compliance calendars for recurring filing obligations
- Designing operational workflows for Form PF, 13F, 13H, or FOCUS report preparation
- Assessing whether a firm qualifies as a large private fund adviser triggering quarterly Form PF filing
- Evaluating whether an institutional investment manager has crossed the $100M threshold for 13F reporting
- Identifying when Form ADV amendments must be filed promptly versus at the annual updating amendment
- Responding to SEC blue sheet requests or remediating CAT reporting errors
- Building CAT reporting infrastructure and ensuring clock synchronization compliance
- Understanding FINRA reporting obligations for short interest, TRACE, and trade reporting
- Preparing for regulatory examinations focused on filing timeliness and accuracy
- Establishing error correction and remediation procedures for reporting failures

## Core Concepts

### Form ADV Amendments
Registered investment advisers must keep Form ADV current through two amendment mechanisms:

**Annual updating amendment** — Must be filed within 90 days of the adviser's fiscal year end (Rule 204-1 under the Investment Advisers Act of 1940). The annual amendment requires the adviser to review and update all items on Form ADV Parts 1, 2A, and 2B. The adviser must also deliver or offer to deliver the updated brochure (Part 2A) to existing clients within 120 days of fiscal year end, along with a summary of material changes.

**Other-than-annual amendments (interim/prompt amendments)** — Certain items on Form ADV must be amended promptly when information becomes inaccurate. "Promptly" is generally interpreted as within 30 days of the event, though some changes require faster action. Items requiring prompt amendment include:
- Changes in the adviser's organizational structure, control persons, or ownership (Part 1, Items 1, 2, 3, 7, 10, 11)
- Changes in disciplinary history (Part 1, Item 11, DRPs)
- Changes in the adviser's financial condition that would require disclosure under Part 2A Item 18
- Changes to the brochure (Part 2A) that are material and that clients or prospective clients should know about — including changes to types of advisory services, fee schedules, methods of analysis, risk factors, material conflicts, disciplinary events, or financial condition

**Items that may wait for the annual amendment** — Statistical information (AUM, number of clients), non-material updates to biographical information, and administrative details that do not affect client decision-making.

**Filing via IARD** — All Form ADV amendments are filed electronically through the Investment Adviser Registration Depository (IARD) system. Filing fees apply. State notice filings are typically triggered automatically upon SEC filing for advisers relying on SEC registration.

**State notice filings** — SEC-registered advisers operating in multiple states must make notice filings with each state in which they have a place of business or meet the de minimis threshold. IARD facilitates most state notice filings alongside the SEC filing.

**Form ADV-W (Withdrawal)** — An adviser withdrawing from SEC registration files Form ADV-W via IARD. Partial withdrawal (from specific states) or full withdrawal from SEC registration. A withdrawal filing becomes effective 60 days after filing unless the SEC institutes proceedings. Firms must maintain books and records for the applicable retention periods after withdrawal.

### Form PF (Private Fund Reporting)
SEC Form PF, required under Section 204(b) of the Advisers Act and Rule 204(b)-1, applies to SEC-registered investment advisers that manage one or more private funds.

**Filing thresholds and frequency:**
- **Large private fund advisers to hedge funds** — advisers with at least $1.5 billion in hedge fund AUM must file quarterly within 60 days of quarter end. They report on each qualifying hedge fund individually.
- **Large private fund advisers to liquidity funds** — advisers with at least $1 billion in combined money market fund and liquidity fund AUM must file quarterly within 15 days of quarter end.
- **Large private fund advisers to private equity funds** — advisers with at least $2 billion in private equity fund AUM must file annually but report more detailed information on each qualifying PE fund.
- **Smaller private fund advisers** — all other SEC-registered advisers with at least $150 million in private fund AUM file annually within 120 days of fiscal year end. They report aggregate information across all advised private funds.

**Content of Form PF filings:** AUM and NAV for each reported fund; borrowings and leverage (gross and net); investor concentration (largest investors as a percentage of NAV); asset class exposure and geographic breakdown; counterparty credit exposure (top counterparties); trading and clearing practices (exchange-traded vs OTC); liquidity of portfolio positions; side pocket and gate usage; performance data; investment strategy classification; use of high-frequency trading strategies.

**2023 Amendments — Current Reporting (effective 2024):** The SEC adopted amendments to Form PF requiring current reporting of certain triggering events:
- **Large hedge fund advisers** must report within 72 hours of: extraordinary investment losses (20% or more of a reporting fund's NAV over a rolling 10-business-day period), significant margin and default events (failure to meet a margin call that exceeds the reporting fund's NAV by 5% or more), counterparty defaults, material changes in prime broker relationships, changes in unencumbered cash falling below a reporting fund's requirement, and operations events (significant disruption to key operations).
- **All Form PF filers for private equity** must report within 60 days of: GP-led secondary transactions, adviser-led fund restructurings, removal of a fund's GP, election to terminate a fund's investment period, and election to terminate a fund.

Filing is through the SEC's Private Fund Reporting Depository (PFRD) on EDGAR.

### 13F Filings (Institutional Holdings)
SEC Rule 13f-1 under Section 13(f) of the Securities Exchange Act of 1934 requires institutional investment managers exercising investment discretion over $100 million or more in 13(f) securities to file Form 13F quarterly.

**Who must file:** Any "institutional investment manager" — a broad category that includes investment advisers, banks, insurance companies, broker-dealers, pension funds, and corporations — that exercises investment discretion over the threshold amount. The threshold is measured as of the last trading day of any month in the calendar year. Once crossed, the manager must file for every quarter of that calendar year and the following calendar year.

**What to report:** Long positions in 13(f) securities as of the last day of the calendar quarter. 13(f) securities include: exchange-listed equities and equity-linked securities (common stock, preferred stock, warrants, convertible securities), shares of closed-end funds, certain exchange-traded options (puts and calls), and shares of ETFs. The official list of 13(f) securities is published quarterly by the SEC.

**Required data elements:** CUSIP number, issuer name, class title (e.g., "COM" for common stock), market value (rounded to the nearest thousand dollars), number of shares or principal amount, investment discretion type (sole, shared, or none), voting authority (sole, shared, or none), and the number of shares for each voting authority type.

**Filing deadline:** Within 45 days of calendar quarter end (filed on SEC EDGAR).

**Confidential treatment requests:** Managers may request confidential treatment under Rule 24b-2 for positions where public disclosure would reveal a trading strategy still being implemented (e.g., ongoing accumulation or disposition). The SEC grants confidential treatment on a case-by-case basis and requires a showing that disclosure would likely cause competitive harm. Historically, the SEC has narrowed the grounds for confidential treatment.

**Common errors and consequences:** Late filings result in public notice and may trigger SEC enforcement. Reporting errors in CUSIPs, share counts, or market values can mislead market participants. Firms must verify 13F data against custodian records and ensure consistent treatment of jointly managed accounts. The SEC has brought enforcement actions for material misstatements on Form 13F.

### 13H Filings (Large Trader Reporting)
SEC Rule 13h-1 under Section 13(h) of the Exchange Act requires "large traders" to identify themselves to the SEC and receive a Large Trader Identification Number (LTID).

**Large trader thresholds:** A person (including a firm) is a "large trader" if their transactions in NMS securities equal or exceed:
- **2 million shares or $20 million in fair market value** during any single calendar day, or
- **20 million shares or $200 million in fair market value** during any calendar month.

Transactions across all accounts over which the person exercises investment discretion are aggregated. The thresholds apply to both purchases and sales.

**Form 13H filing requirements:**
- **Initial filing** — must be filed promptly after first meeting the threshold. Filed electronically on SEC EDGAR.
- **Annual filing** — within 45 days after the end of each full calendar year following initial filing.
- **Amended filings** — filed promptly upon the occurrence of a material change to previously reported information (e.g., change in organizational structure, new broker-dealer relationships, change in control).
- **Inactive status** — a large trader that has not met the threshold during the previous full calendar year may file for inactive status. Must reactivate if the threshold is subsequently met.

**LTID assignment and use:** Upon filing, the SEC assigns an LTID. The large trader must provide the LTID to each broker-dealer through which it trades. The LTID is attached to the large trader's accounts at each broker-dealer.

**Broker-dealer obligations:** Broker-dealers carrying accounts for large traders must: (a) maintain records of transactions effected through large trader accounts, (b) report large trader transaction data to the SEC upon request (historically via Electronic Blue Sheets, now increasingly through CAT), and (c) monitor for customers who may meet the large trader definition but have not self-identified.

### FOCUS Reports
The Financial and Operational Combined Uniform Single (FOCUS) report is the primary financial reporting form for broker-dealers, required under SEC Rule 17a-5 and filed through FINRA's systems.

**Filing frequency and form versions:**
- **Part II** — filed quarterly by introducing broker-dealers (firms that do not carry customer accounts or clear transactions). Due within 17 business days of quarter end.
- **Part IIA** — filed monthly by carrying/clearing broker-dealers (firms that hold customer funds or securities, clear transactions, or carry customer accounts). Due within 17 business days of month end.
- **Part IIC** — filed by OTC derivatives dealers.

**Content of FOCUS reports:**
- **Statement of financial condition** (balance sheet) — assets, liabilities, ownership equity
- **Net capital computation** (SEC Rule 15c3-1) — the firm's calculation of net capital, showing liquid assets minus liabilities and haircuts. The net capital rule requires broker-dealers to maintain a minimum level of liquid assets to protect customer funds and securities.
- **Aggregate indebtedness computation** — ratio of aggregate indebtedness to net capital (must not exceed 15:1 for firms using the basic method)
- **Customer reserve computation** (SEC Rule 15c3-3) — the computation determining whether the firm must deposit funds into a special reserve bank account for the exclusive benefit of customers
- **Income statement** and revenue detail
- **Operational data** — possession or control of customer fully paid and excess margin securities

**Filing and regulatory oversight:** FOCUS reports are filed with FINRA as the firm's designated examining authority (DEA). FINRA reviews filings for accuracy, timeliness, and compliance with net capital and customer protection rules. FOCUS data is shared with the SEC. Late filing, inaccurate filings, or filings showing net capital deficiencies trigger heightened regulatory scrutiny.

**Consequences of late or deficient filings:** FINRA may impose fines, censure, or suspend a firm for persistent late filings. A FOCUS report showing a net capital deficiency triggers immediate obligations under SEC Rule 17a-11 (discussed in the worked examples below).

### Blue Sheets / EBS (Electronic Blue Sheets)
SEC Rule 17a-25 requires broker-dealers to submit, upon SEC request, standardized electronic trading records for specified securities and time periods.

**When requested:** Blue sheet requests typically arise during SEC investigations into potential insider trading, market manipulation, or other trading violations. The SEC's Division of Enforcement issues blue sheet requests identifying the securities, time period, and type of trading data required.

**Data elements:** Customer identity (name, address, SSN/TIN), account number, transaction date and time, security identifier (CUSIP/symbol), buy/sell/short sale indicator, quantity, price, executing broker, clearing broker, and the capacity in which the firm acted (principal or agent).

**Timeliness:** Broker-dealers must respond within the timeframe specified in the request, typically 10 business days. Firms should have systems capable of extracting and formatting blue sheet data promptly.

**Relationship to CAT:** The Consolidated Audit Trail (CAT) has largely superseded blue sheets for routine regulatory surveillance purposes. FINRA and the SEC can now access much of the same information through CAT data. However, the SEC continues to use blue sheet requests for specific enforcement investigations, particularly when CAT data is incomplete or when historical data predating CAT implementation is needed. The SEC has announced plans to retire the Electronic Blue Sheet system as CAT reaches full maturity, but as of the current date, both systems remain in use.

**Enforcement for non-compliance:** Failure to respond accurately or timely to blue sheet requests can result in SEC enforcement action. The SEC has brought cases against firms for submitting inaccurate blue sheet data, including incorrect customer identification or missing transactions.

### CAT (Consolidated Audit Trail)
SEC Rule 613 mandated the creation of the Consolidated Audit Trail, the most comprehensive order tracking system in U.S. securities markets. The CAT Plan was adopted in 2016, and reporting obligations have been phased in for equities and options.

**Who must report:** All broker-dealers that are members of a national securities exchange or FINRA ("Industry Members") and all national securities exchanges ("Plan Participants") must report to CAT. This includes introducing brokers, clearing firms, market makers, ATSs, and exchange members.

**What is reported:** CAT captures every reportable event in the lifecycle of an order for NMS equities and listed options:
- **Order origination** — receipt of a new order from a customer or another broker-dealer, including order terms (side, quantity, price, time-in-force, order type, special handling instructions)
- **Order routing** — transmission of an order to another broker-dealer, exchange, or ATS
- **Order modification** — changes to order terms (price, quantity, time-in-force)
- **Order cancellation** — cancellation of a pending order
- **Order execution** — full or partial fill, including execution price and quantity
- **Allocation** — post-trade allocation to sub-accounts (for institutional orders)

**Customer and Account Identifying Information (CAIS):** Industry Members must submit CAIS data linking each account to its customer(s). CAIS includes: customer name, address, date of birth (for individuals), SSN/EIN, and account information. CAIS is submitted through a separate reporting channel and must be kept current.

**Clock synchronization requirements:** Accurate timestamps are essential for order lifecycle tracking. SEC Rule 613 and the CAT NMS Plan require:
- **Exchanges and ATSs** — clocks must be synchronized to within 50 milliseconds of the National Institute of Standards and Technology (NIST) atomic clock
- **Broker-dealers (Industry Members)** — clocks must be synchronized to within 1 second of the NIST atomic clock for manual order events, and within 50 milliseconds for electronic order events
- Firms must document their clock synchronization procedures, test compliance regularly, and maintain records of clock drift and synchronization corrections

**Error correction obligations:** CAT reporting firms must monitor their submissions for errors flagged by the CAT system. The CAT system validates submissions and generates error reports. Firms must:
- Repair errors within the timeframes specified by the CAT NMS Plan (generally T+3 for most errors)
- Monitor error rates — the CAT NMS Plan establishes error rate thresholds, and firms with persistently high error rates face regulatory scrutiny
- Maintain records of error identification, root cause analysis, and correction

**Implementation timeline:** Large Industry Members began reporting equities in April 2020 and options in 2022. Small Industry Members followed shortly thereafter. The full lifecycle reporting, including allocations and CAIS data, has been phased in incrementally. Firms should consult the FINRA CAT website and the CAT NMS Plan Processor (FINRA CAT, LLC) for current reporting specifications and implementation deadlines.

**Retirement of OATS:** FINRA's Order Audit Trail System (OATS), which previously served as the primary order tracking system for FINRA member firms, was retired on September 1, 2020, following the implementation of CAT reporting for equities.

### SAR and CTR Filing Mechanics
While the substantive AML compliance framework is covered in the anti-money-laundering skill, the reporting mechanics are a regulatory reporting obligation:

**FinCEN BSA E-Filing System** — SARs (FinCEN Form 111) and CTRs (FinCEN Form 112) are filed electronically through FinCEN's BSA E-Filing System. Firms must register for BSA E-Filing, designate authorized users, and maintain access credentials securely.

**SAR filing deadlines:**
- File within 30 calendar days of the date the suspicious activity is first detected by the firm
- If no suspect is identified at the time of detection, the deadline extends to 60 calendar days, but the firm must make a reasonable effort to identify the suspect before filing
- Continuing SARs for ongoing suspicious activity must be filed at least every 90 days
- SAR amendments may be filed to correct or supplement previously filed SARs

**CTR filing deadlines:**
- File within 15 calendar days of the cash transaction exceeding $10,000 (or aggregated transactions exceeding $10,000 in a single business day)

**SAR confidentiality** — 31 U.S.C. Section 5318(g)(2) prohibits any financial institution, or any officer, director, employee, or agent thereof, from disclosing to the person involved in the transaction (or any other person) that a SAR has been or will be filed. This tipping-off prohibition extends to responses to subpoenas, discovery requests, or other legal process — SARs themselves are not producible, although the underlying facts are not privileged.

**Recordkeeping for filed reports:**
- SARs — supporting documentation (transaction records, analyst notes, investigation files, SAR narrative drafts) must be retained for 5 years from the date of filing (31 CFR Section 1010.320(d))
- CTRs — records must be retained for 5 years from the date of the report (31 CFR Section 1010.306(a))
- All filed SARs and CTRs must be maintained in a format that allows retrieval upon FinCEN or law enforcement request

### FINRA Reporting Obligations
Beyond FOCUS reports and CAT, FINRA member firms have several additional reporting obligations:

**Short interest reporting (FINRA Rule 4560)** — Member firms must report short positions in all equity securities (customer and proprietary) as of settlement on the designated reporting date, which occurs twice monthly (approximately the 15th and last business day of each month). Reports are due to FINRA by 6:00 p.m. ET on the second business day after the reporting settlement date. FINRA publishes aggregate short interest data, and individual firm reports are used for regulatory surveillance.

**TRACE (Trade Reporting and Compliance Engine)** — FINRA-operated system for reporting OTC transactions in eligible fixed-income securities, including corporate bonds, agency debentures, asset-backed securities, and certain other debt instruments. Reporting is required within 15 minutes of execution for most transactions (FINRA Rules 6710-6770). TRACE-eligible securities have expanded over time to include Treasury securities (effective 2020 under FINRA Rule 6730). Late TRACE reports result in regulatory action.

**Trade reporting to FINRA-operated facilities** — For OTC equity transactions, member firms must report trades to the appropriate FINRA facility:
- **ORF (OTC Reporting Facility)** — for OTC equity securities not listed on an exchange
- **TRF (Trade Reporting Facility)** — for NMS stocks (exchange-listed equities traded OTC). Multiple TRFs exist (FINRA/Nasdaq TRF, FINRA/NYSE TRF)
- **ADF (Alternative Display Facility)** — for firms that choose to display quotations through the ADF

Trade reports must be submitted within 10 seconds of execution during market hours.

**Regulatory filings and notifications** — FINRA members must promptly notify FINRA of certain events under FINRA Rule 4530, including: violations of securities laws, written customer complaints, regulatory actions by other agencies, criminal charges against associated persons, and civil litigation related to the firm's investment banking or securities business. Annual statistical reports of customer complaints are also required.

### Regulatory Reporting Calendar

| Filing | Who Must File | Frequency | Deadline | Filed With |
|--------|--------------|-----------|----------|------------|
| Form ADV (annual) | SEC-registered IAs | Annually | 90 days after fiscal year end | SEC via IARD |
| Form ADV (interim) | SEC-registered IAs | As needed | Promptly (within 30 days of material change) | SEC via IARD |
| Form PF (small filer) | IAs with $150M+ private fund AUM | Annually | 120 days after fiscal year end | SEC via PFRD/EDGAR |
| Form PF (large hedge) | IAs with $1.5B+ hedge fund AUM | Quarterly | 60 days after quarter end | SEC via PFRD/EDGAR |
| Form PF (large liquidity) | IAs with $1B+ liquidity fund AUM | Quarterly | 15 days after quarter end | SEC via PFRD/EDGAR |
| Form PF (large PE) | IAs with $2B+ PE fund AUM | Annually | 120 days after fiscal year end | SEC via PFRD/EDGAR |
| Form PF (current report) | Large hedge fund advisers | Event-driven | 72 hours after triggering event | SEC via PFRD/EDGAR |
| Form 13F | Managers with $100M+ in 13(f) securities | Quarterly | 45 days after quarter end | SEC via EDGAR |
| Form 13H (initial) | Large traders | Once | Promptly after threshold is met | SEC via EDGAR |
| Form 13H (annual) | Large traders | Annually | 45 days after calendar year end | SEC via EDGAR |
| FOCUS Part II | Introducing BDs | Quarterly | 17 business days after quarter end | FINRA |
| FOCUS Part IIA | Carrying/clearing BDs | Monthly | 17 business days after month end | FINRA |
| CAT (equities/options) | BD members, exchanges | Daily | 8:00 a.m. ET on T+1 | FINRA CAT |
| CAIS (customer data) | BD members | Ongoing | Per CAT NMS Plan schedule | FINRA CAT |
| Short interest | FINRA members | Semi-monthly | 6:00 p.m. ET, 2nd business day after settlement date | FINRA |
| TRACE (fixed income) | FINRA members | Per transaction | Within 15 minutes of execution | FINRA |
| OTC equity trade reports | FINRA members | Per transaction | Within 10 seconds of execution | FINRA (TRF/ORF/ADF) |
| SARs | BDs, banks, covered IAs | Event-driven | 30 days after detection (60 if no suspect) | FinCEN via BSA E-Filing |
| CTRs | BDs, banks | Event-driven | 15 days after transaction | FinCEN via BSA E-Filing |
| FINRA Rule 4530 | FINRA members | Event-driven | 30 calendar days of the event | FINRA |

## Worked Examples

### Example 1: Newly registered IA crossing AUM threshold and triggering Form PF obligations
**Scenario:** An investment advisory firm has been state-registered for three years, managing $120 million in a mix of separate accounts and a single private fund (a hedge fund with $50 million in AUM). In Q2 2025, the firm's total AUM crosses $150 million, and its private fund AUM remains at $50 million. The firm files for SEC registration, which becomes effective in September 2025. The firm has a December 31 fiscal year end.
**Compliance Issues:**
- Crossing $100 million in AUM (for advisers with no state exemption) triggers the obligation to register with the SEC under Section 203A of the Advisers Act, with narrow exceptions for mid-sized advisers subject to examination by their home state.
- SEC registration triggers Form ADV filing via IARD — the firm must file a complete Form ADV (Parts 1, 2A, 2B, and Form CRS if not previously filed) at the time of registration.
- Managing a private fund with at least $150 million in total private fund AUM triggers Form PF filing as a "smaller private fund adviser." Since the firm has under $1.5 billion in hedge fund AUM, it is not a large private fund adviser and files annually.
- The firm's first Form PF is due within 120 days of its first fiscal year end after becoming obligated — meaning by April 30, 2026, for the fiscal year ending December 31, 2025.
- The firm must also transition state notice filings to the SEC IARD system and ensure it withdraws from any state registrations that are no longer required.
**Analysis:**
The firm should establish the following operational timeline: (1) File Form ADV with the SEC via IARD concurrent with the registration application, ensuring all items are completed accurately, including Schedule D for the private fund. (2) File Form CRS with the SEC and deliver to all existing clients. (3) Register for access to the Private Fund Reporting Depository on EDGAR for Form PF filing. (4) Assign compliance personnel responsible for Form PF preparation and identify data sources — NAV, leverage, asset class exposure, investor concentration, counterparty exposure — that must be compiled from the fund administrator, prime broker, and internal records. (5) Conduct a dry run of the Form PF filing process before the first filing deadline to identify data gaps. (6) Set the compliance calendar: first annual Form PF due by April 30, 2026; first annual ADV updating amendment due by March 31, 2026; Form CRS must be reviewed and updated at least annually. (7) Monitor whether hedge fund AUM approaches $1.5 billion, which would trigger quarterly filing and significantly more detailed reporting. The firm should budget for the operational burden of Form PF — smaller private fund advisers typically spend 20-40 hours on each annual filing, and the data aggregation process requires coordination across multiple service providers.

### Example 2: Broker-dealer FOCUS report reveals net capital deficiency
**Scenario:** A carrying broker-dealer files its monthly FOCUS Part IIA report for January 2026. The net capital computation shows that the firm's net capital has fallen below its minimum required net capital by $1.2 million, driven by unexpected trading losses in a proprietary account and an increase in customer debit balances that raised the firm's required net capital under the alternative method (SEC Rule 15c3-1(a)(1)(ii)). The firm's minimum requirement is $250,000, but its required net capital under the alternative method is $4.5 million, and actual net capital is $3.3 million.
**Compliance Issues:**
- SEC Rule 17a-11 imposes immediate notification obligations when a broker-dealer's net capital falls below its minimum requirement. The firm must notify the SEC, its designated examining authority (FINRA), and its designated self-regulatory organization by telegraph or facsimile (in practice, electronic notice) within 24 hours of the discovery.
- Under Rule 17a-11(b), a broker-dealer whose net capital declines below 120% of its minimum requirement must also provide early warning notice to the SEC and FINRA.
- Under Rule 15c3-1(e), a broker-dealer in net capital deficiency may not conduct securities business (i.e., cannot execute customer transactions, accept new customer accounts, or transfer customer funds or securities) until the deficiency is cured, unless granted a temporary exemption by the SEC.
- The firm must also file a notice under Rule 17a-11(d) if it fails to make a required customer reserve deposit under Rule 15c3-3.
- FINRA will likely impose heightened supervision, require a corrective action plan, and may conduct an accelerated examination.
**Analysis:**
The firm must take the following immediate steps: (1) Notify the SEC (Division of Trading and Markets), FINRA (Member Supervision), and the firm's DSRO within 24 hours of computing the deficiency. The notice must state the amount of the deficiency, the cause, and the firm's plan for remediation. (2) Cease conducting securities business until the deficiency is cured — this means suspending customer transactions, which will require notifying customers and potentially arranging for an emergency carrying agreement with another broker-dealer. (3) Compute the customer reserve formula to determine whether customer funds are at risk and whether an extraordinary reserve deposit is needed. (4) Prepare and file a supplemental FOCUS report showing the deficiency and the corrective action plan. (5) Identify the path to cure: options include capital contribution from the firm's parent or owners, liquidation of proprietary positions, reduction of customer debit balances, or a combination. (6) Once the deficiency is cured, file notice with the SEC and FINRA demonstrating that net capital is restored above the minimum (ideally above 120% to exit early warning). (7) Conduct a root cause analysis and implement controls to prevent recurrence — this may include revised proprietary trading limits, enhanced margin monitoring, or increased capital buffers. A net capital deficiency is one of the most serious regulatory events for a broker-dealer. FINRA enforcement may include fines under Rules 4110 and 4120, and repeated deficiencies can lead to suspension or expulsion.

### Example 3: Blue sheet request reveals systematic CAT reporting errors
**Scenario:** A mid-sized broker-dealer receives a blue sheet request from the SEC's Division of Enforcement seeking transaction data for a particular security over a 90-day period, related to a suspected insider trading investigation. While compiling the blue sheet response, the firm's compliance team discovers that its CAT reporting system has been systematically misidentifying customers for approximately 6 months due to a software mapping error. The error caused roughly 15,000 order events to be submitted to CAT with incorrect Customer Account IDs, linking orders to the wrong customer accounts in CAIS. The blue sheet data, compiled independently from the firm's order management system, is accurate.
**Compliance Issues:**
- The blue sheet response must be accurate and complete within the SEC's stated deadline. Submitting inaccurate blue sheet data is itself a violation of SEC Rule 17a-25 and can result in separate enforcement action.
- The 6-month CAT reporting error constitutes a violation of Rule 613 and the CAT NMS Plan. Systematic errors affecting 15,000 events over 6 months will significantly exceed normal error rate thresholds and will attract regulatory attention from FINRA CAT, LLC (the plan processor) and potentially from the SEC.
- The firm has an obligation to correct CAT errors within the timeframes specified by the CAT NMS Plan. For errors this widespread, the firm must develop a comprehensive remediation plan.
- The overlap between the blue sheet investigation and the CAT error creates additional regulatory exposure — if the incorrect CAT data impeded surveillance of the suspected insider trading, the consequences could be severe.
- Depending on the nature of the customer misidentification, there may also be implications for CAIS data integrity, which is central to linking orders to customers for surveillance purposes.
**Analysis:**
The firm must address three parallel workstreams: (1) **Blue sheet response** — prioritize compiling an accurate and complete response from source systems (not from CAT data). Verify customer identification against account records and the order management system. Submit the blue sheet data within the SEC's specified deadline. If additional time is needed due to the volume or complexity, request an extension from the Division of Enforcement promptly. (2) **CAT error remediation** — conduct a root cause analysis of the software mapping error. Identify all affected order events over the 6-month period. Develop a remediation file to correct the Customer Account IDs for all 15,000+ events. Submit corrected data to FINRA CAT. Notify FINRA's CAT Helpdesk and the firm's designated FINRA examination contact of the systematic error and the remediation plan. Document the root cause, the scope of the impact, the timeline of error detection and correction, and the controls implemented to prevent recurrence. (3) **Regulatory exposure management** — the firm should consider self-reporting the CAT error to FINRA and the SEC proactively, as self-disclosure is a mitigating factor in enforcement proceedings. The firm should assess whether the incorrect customer mapping could have masked any suspicious trading patterns that should have been visible to regulators through CAT surveillance. If so, the firm should include that analysis in its self-disclosure. Legal counsel should be engaged to evaluate the firm's exposure and advise on the self-reporting strategy. The firm should also review its broader technology change management and quality assurance processes for CAT reporting — a 6-month undetected error suggests inadequate reconciliation controls between the firm's order management system and its CAT reporting submissions. Implementing daily reconciliation of CAT-submitted data against source systems is an industry best practice that would have detected this error much sooner.

## Common Pitfalls
- Missing prompt Form ADV amendment deadlines by treating all changes as annual-only updates — material changes to advisory services, fees, disciplinary events, or organizational structure require prompt interim filing
- Failing to monitor private fund AUM against Form PF filing thresholds as assets grow, resulting in missed filing obligations
- Filing 13F reports with incorrect share counts or market values because of failures to reconcile against custodian records or to account for corporate actions (splits, mergers, spin-offs)
- Not updating Form 13H promptly when broker-dealer relationships change or organizational structure is modified
- Treating FOCUS report preparation as a back-office function without CCO review, leading to errors in net capital computation or customer reserve calculation
- Delaying response to SEC blue sheet requests or submitting data extracted from a single system without cross-verification against independent records
- Failing to implement daily CAT data reconciliation between the firm's order management system and CAT submissions, allowing errors to accumulate undetected
- Not maintaining clock synchronization compliance — broker-dealer clocks drifting beyond the 1-second (or 50-millisecond for electronic events) tolerance without detection or correction
- Treating the 72-hour current reporting requirement under the 2023 Form PF amendments as a best-efforts obligation rather than a strict deadline
- Submitting TRACE reports outside the 15-minute window and failing to mark late reports as such, compounding the violation
- Not establishing a regulatory filing calendar with automated reminders, leading to missed deadlines across multiple overlapping filing obligations
- Failing to retain SAR and CTR supporting documentation for the full 5-year period, or commingling SAR files with general compliance records in a way that risks inadvertent disclosure
- Neglecting to file FINRA Rule 4530 event notifications within 30 calendar days, particularly for written customer complaints and associated person disciplinary events

## Cross-References
- **anti-money-laundering** (Layer 9): SAR and CTR filing mechanics are regulatory reporting obligations; the substantive AML framework (detection, investigation, escalation) feeds into the reporting workflow covered here
- **client-disclosures** (Layer 9): Form ADV amendments trigger delivery obligations to existing clients — the disclosure skill covers what must be delivered and when, while this skill covers the filing mechanics
- **books-and-records** (Layer 9): Records retention requirements underpin all regulatory reporting; accurate books and records are the source data for FOCUS reports, 13F filings, Form PF, and CAT submissions
- **know-your-customer** (Layer 9): CAT CAIS data and blue sheet responses require accurate customer identification information sourced from the firm's KYC and CIP processes
- **fee-disclosure** (Layer 9): Form ADV amendments reflecting changes to fee schedules are both a filing obligation (covered here) and a fee disclosure requirement (covered in fee-disclosure)
