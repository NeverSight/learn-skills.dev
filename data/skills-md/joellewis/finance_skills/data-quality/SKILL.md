---
name: data-quality
description: "Design and operate data quality programs for financial data — golden source architecture, validation rules, data lineage, exception management, profiling, and governance. Use when building validation rules for pricing or client data pipelines, designing a data quality monitoring framework, establishing golden source designations across systems, implementing data lineage for BCBS 239 or MiFID II, investigating reconciliation breaks or billing errors traced to bad data, preparing for regulatory exams on data accuracy, building data quality scorecards, or defining data stewardship roles. Trigger on: data quality, golden source, data lineage, data validation, data profiling, exception management, data governance, BCBS 239, data completeness, data accuracy, validation rules, data anomaly, data stewardship, data quality scorecard."
---

# Data Quality

## Purpose

Guide the design and operation of data quality management programs for financial services firms. Covers the six dimensions of data quality (accuracy, completeness, timeliness, consistency, validity, uniqueness) applied to financial data domains, golden source architecture and master data management, data lineage and provenance tracking, validation rule design for security prices, client data, transaction data, and position data, data profiling and anomaly detection, exception management workflows, data quality governance frameworks, and regulatory requirements for data accuracy including BCBS 239, MiFID II, GIPS, and SEC recordkeeping obligations. Enables building or evaluating data quality infrastructure that ensures downstream systems — portfolio management, trading, compliance, reporting, and billing — operate on trustworthy data.

## Layer

13 — Data Integration (Reference Data & Integration)

## Direction

both

## When to Use

- Designing a data quality monitoring framework for a wealth management or asset management platform
- Building validation rules for security pricing, client data, transaction data, or position data pipelines
- Conducting a data quality assessment for regulatory reporting readiness (SEC filings, GIPS, AML/KYC)
- Establishing golden source designations and conflict resolution rules across multiple systems
- Implementing data lineage tracking to satisfy BCBS 239 or MiFID II requirements
- Designing exception management workflows for data quality breaks
- Building data quality scorecards and governance reporting for operations committees
- Investigating root causes of reconciliation breaks, billing errors, or performance calculation discrepancies traced to data quality
- Evaluating data profiling tools or data quality monitoring platforms
- Defining data stewardship roles and accountability structures
- Preparing for regulatory examinations where data accuracy is a focus area
- Trigger phrases: "data quality," "golden source," "data lineage," "data validation," "data profiling," "exception management," "data stewardship," "data governance," "BCBS 239," "data quality scorecard," "validation rules," "data anomaly," "data completeness," "data accuracy"

## Core Concepts

### 1. Data Quality Dimensions for Financial Data

Six dimensions define data quality. Each has domain-specific meaning in financial services.

**Accuracy** — Data values correctly represent the real-world entity or event they describe. A security price is accurate if it reflects the actual market closing price or evaluated value from the designated source. A client address is accurate if it matches the client's current legal address of record. Accuracy failures propagate: an inaccurate price produces inaccurate valuations, performance, billing, and regulatory reports. Accuracy is measured by comparing data against an independent authoritative source — cross-vendor price comparison, custodian-to-PMS reconciliation, client confirmation of personal data. In practice, accuracy is the hardest dimension to measure because it requires an independent reference point for comparison.

**Completeness** — All required data elements are present for every record. A security master record is incomplete if it lacks an ISIN, asset class classification, or pricing source designation. A client onboarding record is incomplete if beneficial ownership for entity accounts is missing. Completeness is measured as the percentage of records with all mandatory fields populated. Financial data completeness requirements are often regulatory: FinCEN requires complete beneficial ownership data, GIPS requires complete portfolio inclusion in composites, SEC Rule 17a-4 requires complete transaction records. Completeness must be defined per record type — a required field for an entity account (beneficial ownership) differs from a required field for an individual account (employment status).

**Timeliness** — Data is available when needed for its intended use. End-of-day pricing must arrive before the nightly valuation batch runs. Trade confirmations must be generated within SEC Rule 10b-10 timeframes. NAV calculations must complete before fund company deadlines. Timeliness is measured as the lag between event occurrence and data availability in consuming systems. Late data is functionally equivalent to missing data if it arrives after the processing window closes. Timeliness requirements vary dramatically by use case: real-time market data must arrive in milliseconds, EOD pricing within hours, and quarterly regulatory filings within weeks.

**Consistency** — The same fact is represented identically across all systems and time periods. A client's legal name must match across the CRM, custodian, PMS, and billing system. A security's sector classification must be the same in the portfolio management system and the compliance monitoring system. Inconsistency typically indicates either a missing golden source designation or a broken synchronization process. Consistency is measured by cross-system comparison for the same entity attribute. Temporal consistency also matters: a security's classification should not change retroactively without documented justification and downstream impact assessment.

**Validity** — Data conforms to defined formats, ranges, and business rules. A CUSIP must be exactly 9 characters with a valid check digit. An account registration type must be one of the firm's defined values. A bond coupon rate cannot be negative (for conventional bonds). A trade settlement date cannot precede the trade date. Validity is enforced through schema constraints, field-level validation, and business rule engines. Invalid data that passes into production indicates insufficient input validation. Validity rules should be versioned and maintained as a formal catalog — when rules change, the change should be documented with effective date and rationale.

**Uniqueness** — Each real-world entity is represented exactly once. A client appearing as two records in the CRM (duplicate due to name variation or data entry error) causes fragmented reporting, missed household billing discounts, and potential compliance failures (wash sale detection across accounts requires a unified client view). A security represented as two master records per custodian causes duplicated positions. Uniqueness is enforced through deduplication at ingestion and periodic duplicate detection scans. Common deduplication techniques include exact-match on identifiers (SSN, CUSIP), fuzzy matching on names and addresses (Jaro-Winkler, Levenshtein distance), and probabilistic matching combining multiple weak identifiers into a confidence score.

| Dimension | Measurement Method | Typical Target | Key Risk if Unmet |
|---|---|---|---|
| Accuracy | Cross-source comparison, reconciliation | >99.5% for pricing, >99% for client data | Incorrect valuations, billing, filings |
| Completeness | Percentage of required fields populated | >98% for critical fields | Regulatory findings, incomplete reporting |
| Timeliness | Lag from event to system availability | Within processing window | Stale valuations, missed deadlines |
| Consistency | Cross-system attribute comparison | >99% agreement | Conflicting reports, audit failures |
| Validity | Format and business rule pass rate | >99.9% | Processing failures, corrupt records |
| Uniqueness | Duplicate detection rate | <0.1% duplicate rate | Fragmented reporting, compliance gaps |

### 2. Golden Source Architecture

A golden source (also called system of record or authoritative source) is the single designated source for a specific data domain. Every data element should have exactly one golden source, and all consuming systems should retrieve that element from the golden source rather than maintaining independent copies.

**Designations by data domain:**

| Data Domain | Typical Golden Source | Rationale |
|---|---|---|
| Security reference data | Security master (fed by Bloomberg, Refinitiv) | Centralized, vendor-validated, corporate-action-managed |
| Client identity data | Custodian | Verified through CIP/KYC processes, used for tax reporting |
| Client relationship/advisory data | CRM (Salesforce, Redtail, Wealthbox) | Advisor-maintained, includes preferences and suitability |
| Position and transaction data | Custodian books and records | Legal record of ownership, basis for regulatory reporting |
| Performance data | Performance calculation engine (Orion, Black Diamond, Addepar) | Calculated from reconciled positions and pricing |
| Pricing data | Pricing service or security master pricing module | Vendor hierarchy with defined fallback and validation |
| Billing data | Billing system | Derived from positions and pricing via their golden sources |

The golden source designation must be documented, communicated to all stakeholders, and enforced through system architecture — ideally, non-golden-source systems should not allow manual edits to fields owned by another system.

**Conflict resolution:** When multiple sources provide the same data element, the golden source designation determines which value is authoritative. Conflicts require explicit resolution rules: custodian legal name overrides CRM legal name (custodian verified through CIP), but CRM preferred name overrides custodian (advisory relationship data). For pricing, a vendor hierarchy with defined fallback order resolves conflicts — e.g., exchange close, then Bloomberg, then Refinitiv, then manual override with documentation.

**Golden record construction:** In master data management (MDM), the golden record is constructed by merging the best attributes from multiple sources according to survivorship rules. Example: for a client record, legal name comes from the custodian, email and phone from the CRM, risk profile from the PMS, and KYC status from the compliance system. Each attribute has its own golden source, and the composite golden record draws from all of them.

**MDM patterns:**

| Pattern | Description | Data Quality Trade-off |
|---|---|---|
| Registry | Links records across systems without copying data | Lowest cost; no conflict resolution, queries require cross-system joins |
| Consolidation | Read-only golden record aggregated from sources | Good for reporting; does not write corrections back to sources |
| Coexistence | Bidirectional sync between MDM hub and source systems | Keeps all systems current; complex to implement and maintain |
| Transaction hub | Single point of entry for all creates and updates | Highest data quality; requires all users to adopt new workflows |

Most wealth management and advisory firms operate at the consolidation level, aggregating custodian, CRM, and PMS data into a reporting warehouse. Firms with significant data quality issues or regulatory pressure may advance to coexistence, where the MDM hub enforces quality rules and pushes corrections back to source systems.

### 3. Data Lineage and Provenance

Data lineage tracks the full path of data from its origin through every transformation, enrichment, aggregation, and delivery to consuming systems. Provenance records who or what created, modified, or approved data at each stage.

**Lineage metadata:** For each data element, lineage captures: source system and original field, extraction method and timing, every transformation applied (mapping, conversion, calculation, enrichment, aggregation), intermediate staging locations, destination systems and fields, and the timestamp and process identity at each step.

**Why lineage matters in finance:** When a performance report shows unexpected returns, lineage enables tracing the result back through the calculation engine, to the pricing data it used, to the vendor source and extraction timestamp, identifying exactly where an error entered. Without lineage, root cause analysis is manual, slow, and unreliable.

**Impact analysis:** Lineage enables forward impact analysis — if a data source changes its schema or delivery format, lineage identifies every downstream system, calculation, and report affected. This is critical for vendor migrations, system upgrades, and regulatory reporting changes.

**Regulatory requirements:** BCBS 239 (Principles for effective risk data aggregation and risk reporting) requires banks to maintain comprehensive data lineage for risk data, including the ability to trace any risk report value back to its source data and every transformation applied. While BCBS 239 applies to globally systemically important banks (G-SIBs), its principles are increasingly adopted by smaller institutions and non-bank financial firms as best practice. MiFID II requires investment firms to maintain records demonstrating the accuracy and integrity of transaction reports, which effectively requires lineage from trade execution through reporting. SEC examinations increasingly ask firms to demonstrate how reported figures are derived from source data.

**Implementation approaches:** Manual lineage documentation (spreadsheets, data dictionaries) is common but becomes stale quickly as systems evolve. Automated lineage tools parse ETL code, SQL queries, and data pipeline configurations to extract lineage automatically. Leading platforms include Collibra, Alation, Informatica, and Apache Atlas. Hybrid approaches combine automated extraction with manual annotation for business context. For smaller firms, even a manually maintained data flow diagram per critical process (pricing, performance, billing, regulatory reporting) provides significant value over no lineage documentation at all.

**Lineage granularity levels:** Coarse-grained lineage tracks system-to-system data flows (e.g., "custodian feed populates PMS positions"). Fine-grained lineage tracks field-to-field transformations (e.g., "custodian field ACCT_BAL maps to PMS field market_value via currency conversion using the FX rate from Bloomberg as of 4:00 PM ET"). Regulatory use cases (BCBS 239, SEC examination support) increasingly require fine-grained lineage for critical data elements.

### 4. Validation Rules for Financial Data

Validation rules are automated checks that evaluate data against defined criteria before it is loaded into production systems or used for downstream processing. Rules operate at multiple levels.

**Field-level validation:** Individual field format and range checks applied to each field independently.

- **CUSIP:** Exactly 9 alphanumeric characters, check digit validates via Luhn algorithm variant.
- **ISIN:** Exactly 12 characters, 2-letter ISO 3166-1 country prefix, check digit validates via double-add-double algorithm.
- **Price:** Positive numeric (with exceptions for certain derivatives), reasonable decimal precision per asset class (2 decimals for equities, 6 for bonds, 8 for FX rates).
- **Date:** Valid calendar date, within expected range (not in the distant past or future).
- **Account number:** Matches expected format per custodian (Schwab: 8 characters, Fidelity: 9 characters, etc.).
- **Currency code:** Valid ISO 4217 three-letter code.

**Cross-field validation:** Relationships between fields within a single record.

- Trade settlement date must follow trade date by the correct settlement cycle (T+1 for US equities post-May 2024, T+2 for international equities in most markets).
- Bond maturity date must be after issue date.
- Option expiration date must be after trade date.
- A tax-exempt account (Roth IRA) holding tax-exempt municipal bonds is valid but inefficient — flag for suitability review.
- Margin-enabled accounts require margin agreement documentation on file.
- Account inception date must precede first transaction date.

**Cross-record validation:** Relationships between records within a single system.

- Position quantities across all accounts for a security must reconcile to the custodian's total.
- Sum of portfolio weights within a composite must equal 100%.
- All accounts assigned to an advisor must reference a valid advisor record in the advisor master.
- A security referenced in a trade must exist in the security master (referential integrity).
- All accounts within a household must share a consistent billing tier assignment.

**Cross-system validation:** Consistency between systems holding overlapping data.

- Position quantities in the PMS must match the custodian (daily reconciliation).
- Client name and address in the CRM must match the custodian (quarterly consistency check).
- Trade records in the OMS must match confirmations from the executing broker.
- Billing AUM must reconcile to the PMS valuation within defined tolerance.
- Performance returns computed internally must reconcile to custodian-reported returns.

**Temporal validation:** Detecting anachronistic or temporally inconsistent data.

- A corporate bond with a maturity date in the past should not be active in the security master.
- A client whose date of birth implies age greater than 120 (or negative age) has a data error.
- A trade with a future settlement date beyond the expected cycle window requires investigation.
- Price as of a weekend or market holiday should not exist for exchange-traded securities.
- An account opened after a client's date of death (if recorded) indicates a data error or fraud.

**Domain-specific validation examples:**

- **Security prices** — Variance check against prior day (flag moves exceeding asset-class thresholds: 15% equities, 5% investment-grade bonds, 10% high-yield), zero-price detection, negative-price detection, stale-price detection (unchanged beyond expected window adjusted for holidays and trading calendars), cross-vendor comparison, currency verification against security master.
- **Client data** — Address standardization and USPS deliverability verification, SSN/TIN format and check digit validation (mod-9 algorithm), phone and email format validation, PEP and sanctions screening against OFAC SDN list, age reasonableness check against date of birth, employment status consistency with account type (e.g., retirement account contributions require earned income).
- **Transaction data** — Trade quantity and price within normal ranges for the security type, commission within expected bounds per trade size and security, settlement instructions complete (DTC participant, account number), counterparty validation against approved counterparty list, duplicate trade detection (same security, quantity, price, date).
- **Position data** — No negative quantities for long-only accounts, cost basis present for all lots in taxable accounts, inception-to-date position reconciliation with custodian, aggregate position value reasonableness relative to account size and investment policy.

### 5. Data Profiling and Monitoring

Data profiling is the systematic analysis of data to understand its structure, content, quality characteristics, and statistical properties. Monitoring extends profiling into continuous, automated observation.

**Statistical profiling:** For each field, profiling captures:

- **Completeness rate** — percentage of records with non-null, non-default values.
- **Distinct value count and distribution** — cardinality and frequency analysis. A field expected to have high cardinality (client SSN) showing low cardinality indicates duplicates or defaults.
- **Min/max/mean/median/standard deviation** — for numeric fields. A pricing field with a suspiciously low minimum may indicate zero-price contamination.
- **Pattern analysis** — for string fields, identifying format variations (phone numbers with and without area codes, date formats mixing MM/DD and DD/MM).
- **Null and default value rates** — distinguishing genuinely missing data from system defaults masquerading as real values (e.g., "1/1/1900" as a default date).
- **Outlier identification** — values falling outside expected statistical bounds.

In financial data, profiling reveals issues invisible to spot-checking: a pricing field that is 99.8% complete may have the 0.2% gap concentrated in illiquid fixed income — exactly where pricing errors are most consequential.

**Drift detection:** Establishing baselines for data characteristics and alerting when they shift. If a daily pricing file typically contains 2,000 records and today contains 1,200, the record count drift signals a potential upstream issue even if every individual record passes validation. If the percentage of securities with stale prices increases from a 0.5% baseline to 3%, the trend indicates a vendor delivery problem.

**Anomaly detection:** Statistical and rule-based identification of unusual data. Isolation forest or z-score methods for detecting outlier prices in large universes. Sudden changes in data distributions (a sector classification field that historically has 11 distinct values suddenly has 15). Transaction volume anomalies (a 10x spike in trades for a single account).

**Monitoring dashboards:** Operational data quality dashboards display real-time quality metrics across dimensions: completeness percentages, validation pass rates, exception counts by severity, stale data counts, cross-system reconciliation status, and trend charts. Dashboards serve both operational staff (identifying issues to resolve) and management (assessing overall data health).

**Alerting thresholds:** Critical alerts for conditions requiring immediate attention — zero prices loaded for actively traded securities, missing pricing file, reconciliation break exceeding materiality threshold. Warning alerts for conditions requiring investigation within a defined window — rising stale price count, declining completeness trend, unusual exception volume. Thresholds should be calibrated to avoid alert fatigue (too many false positives) while ensuring material issues are never missed. A common calibration approach: run validation rules in observation mode for 30 days, analyze the distribution of flagged items, set initial thresholds at the 95th percentile, then tighten quarterly as data quality improves.

**Trend analysis:** Beyond point-in-time monitoring, trend analysis reveals whether data quality is improving or degrading over time. Weekly and monthly trend reports should track: exception volume by domain and severity, mean time to resolution, completeness and accuracy percentages, and vendor performance metrics (file timeliness, error rates). Deteriorating trends warrant investigation even when individual metrics remain within acceptable bounds.

### 6. Exception Management

An exception is a data quality event that fails validation and requires investigation and resolution. Effective exception management transforms ad hoc firefighting into a structured, measurable process.

**Exception categorization:** Severity levels drive response timelines and escalation. Critical — data quality issue that will cause material financial impact if unresolved (incorrect NAV pricing, missing data for regulatory filing, reconciliation break exceeding threshold). Must be resolved before the affected process runs. High — data quality issue affecting accuracy of reports or calculations but not causing immediate financial harm (stale price for a small position, incomplete client field needed for upcoming regulatory report). Resolve within same business day. Medium — data quality issue that degrades data but has limited immediate impact (missing optional classification field, minor cross-system inconsistency). Resolve within defined SLA (typically 3-5 business days). Low — cosmetic or minor issues (formatting inconsistency, preferred name mismatch). Resolve during scheduled maintenance cycles.

**Exception workflow:** A structured lifecycle ensures no exception is lost or ignored.

1. **Detection** — Automated validation flags the issue, or a user reports it manually.
2. **Categorization** — Severity assigned based on predefined rules (data domain, affected systems, financial impact).
3. **Queuing** — Routed to the responsible data steward or operations team based on data domain ownership.
4. **Investigation** — Root cause determination: vendor error, transformation bug, manual entry mistake, upstream system change, or business rule gap.
5. **Resolution** — Correct the data at source, apply a temporary override with documentation and expiration, accept with written justification, or escalate to data owner for decision.
6. **Closure** — Log resolution details, update root cause tracking database, verify downstream impact is resolved, and confirm consuming systems reflect corrected data.

**Root cause analysis:** Tracking exception root causes reveals systemic issues. If 40% of pricing exceptions trace to a single vendor's corporate bond coverage, that is a vendor quality issue requiring escalation or vendor change. If client data exceptions cluster around a specific onboarding workflow, that workflow needs redesign. Root cause categories: vendor data quality, internal processing error, manual entry error, system integration failure, upstream source change, business rule gap.

**Exception metrics:** Key performance indicators for exception management include:

- **Volume** — Daily exception count by severity and data domain. Establishes baselines and reveals spikes.
- **Mean time to resolution (MTTR)** — Average time from detection to closure, tracked by severity. Targets: critical <2 hours, high <8 hours, medium <3 business days.
- **Aging** — Count of exceptions open beyond their SLA. Aging exceptions indicate capacity issues or process gaps.
- **Root cause distribution** — Percentage breakdown by cause category. Reveals systemic issues amenable to structural fixes.
- **Repeat rate** — Percentage of exceptions that recur within 30 days of resolution. High repeat rates indicate fixes addressing symptoms rather than root causes.
- **Exception rate** — Exceptions as a percentage of total records processed. The primary trend indicator for overall data quality health.

### 7. Data Quality Governance

Governance provides the organizational structure, policies, and accountability framework that sustains data quality beyond individual initiatives.

**Data quality policies:** Formal documentation of quality standards per data domain — acceptable completeness thresholds, accuracy targets, timeliness SLAs, validation rule catalogs, exception handling procedures, and override authorization levels. Policies should be reviewed annually and updated when business processes, regulatory requirements, or system landscapes change.

**Data stewardship roles:** Data owners (senior business leaders accountable for data quality in their domain — e.g., CCO owns client identity data quality, Head of Operations owns transaction data quality), data stewards (operational staff who execute quality processes daily — monitor dashboards, resolve exceptions, coordinate with vendors, maintain data dictionaries), and data custodians (technology staff who implement and maintain the technical infrastructure — validation engines, profiling tools, monitoring systems, lineage capture).

**Quality scorecards:** Monthly or quarterly scorecards reporting data quality metrics by domain, dimension, and system. Scorecards aggregate completeness, accuracy, timeliness, and consistency percentages into an overall quality score per domain. Trend lines show improvement or degradation. Red/amber/green status indicators highlight domains requiring attention. Scorecards are presented to operations committees and executive sponsors to maintain organizational focus.

**Remediation prioritization:** Not all data quality issues warrant equal investment. Prioritize by: regulatory impact (issues affecting filings, compliance monitoring, or examination readiness), financial impact (issues affecting billing, performance, or valuations), client impact (issues affecting client reporting or servicing), and volume (systemic issues affecting many records vs isolated exceptions). A structured prioritization framework prevents remediation resources from being consumed by low-impact issues while material problems persist.

**Accountability frameworks:** Data quality targets (e.g., 99.5% pricing accuracy, 98% client data completeness) are assigned to data owners and included in performance objectives. Escalation paths are defined for quality degradation. Governance committees (monthly data quality council with representation from operations, technology, compliance, and business leadership) review scorecards, approve remediation priorities, and resolve cross-domain issues.

**Periodic quality audits:** Scheduled deep-dive assessments beyond continuous monitoring.

- **Annual comprehensive profiling:** Full statistical profiling of all critical data domains to detect drift from baselines and identify new quality issues.
- **Sampling-based accuracy verification:** Random sample of records compared against independent authoritative sources (e.g., 100 security prices verified against a second vendor, 50 client records verified against custodian source documents).
- **Process audits:** Review of data entry, transformation, and distribution workflows for control gaps, unauthorized access, or undocumented manual steps.
- **Gap analysis:** Comparison of current data quality practices against regulatory expectations (SEC examination priorities, FINRA guidance) and industry frameworks (BCBS 239, DAMA DMBOK).
- **Audit findings** feed into the remediation backlog with assigned owners, target dates, and tracked completion status.

### 8. Data Quality in Regulatory Context

Financial regulators do not typically prescribe specific data quality standards, but they hold firms accountable for the accuracy and completeness of data underlying regulated activities.

**BCBS 239 — Principles for effective risk data aggregation and risk reporting:** Issued by the Basel Committee in 2013, these 14 principles establish expectations for risk data architecture, aggregation capabilities, and reporting practices. Key data quality principles include: Principle 3 (Accuracy and Integrity) — risk data must be accurate, reliable, and produced on a timely basis; Principle 4 (Completeness) — risk data must capture all material risks across the firm; Principle 5 (Timeliness) — risk data must be available within required timeframes; Principle 6 (Adaptability) — risk data systems must be flexible enough to produce ad hoc reports during stress periods. While formally applicable to G-SIBs, BCBS 239 principles have become the de facto framework for data quality governance across the financial industry.

**SEC expectations for data accuracy:** SEC Rule 17a-4 requires broker-dealers to maintain accurate books and records. SEC examinations of investment advisers (under the Investment Advisers Act) evaluate whether client data, portfolio data, and performance data supporting disclosures are accurate. Errors in Form ADV, Form PF, or client reports traced to data quality failures may constitute violations of the antifraud provisions. The SEC's Division of Examinations has repeatedly cited data integrity as an examination priority.

**GIPS requirements for performance data quality:** Firms claiming GIPS compliance must maintain data quality controls ensuring: all actual, fee-paying, discretionary portfolios are included in composites (completeness), returns are calculated using accurate valuations and cash flows (accuracy), portfolio-level returns are time-weighted with appropriate valuation frequency (validity), and composite construction is applied consistently over time (consistency). GIPS verification includes testing data quality controls as part of the verification procedures.

**AML/KYC data accuracy requirements:** FinCEN's Customer Identification Program (CIP) rules require firms to verify client identity information. Customer Due Diligence (CDD) rules require identifying and verifying beneficial owners of legal entity customers. Ongoing monitoring requires current, accurate client data — stale or incomplete client data undermines the effectiveness of transaction monitoring and sanctions screening. The 2026 investment adviser AML/CIP requirements extend these obligations to SEC-registered investment advisers.

**Risk data aggregation:** Beyond BCBS 239, prudential regulators (OCC, Fed, PRA) expect firms to demonstrate that risk calculations (VaR, stress testing, capital adequacy) are based on accurate, complete, timely data with documented lineage. Supervisory stress tests (CCAR, DFAST) require firms to aggregate exposure data across business lines and legal entities with demonstrated accuracy — data quality failures during stress testing exercises have resulted in supervisory findings and remediation orders.

**Practical implications for non-bank financial firms:** While BCBS 239 and CCAR/DFAST formally apply to banks, the SEC and FINRA increasingly expect data quality controls from broker-dealers and investment advisers. SEC examination staff assess whether firms can demonstrate the accuracy of client-facing reports, regulatory filings, and fee calculations. FINRA Rule 4370 (business continuity planning) and FINRA Rule 3110 (supervision) both implicitly depend on data integrity. Firms that proactively adopt data quality governance — even without a specific regulatory mandate — are better positioned for examinations and significantly reduce operational risk exposure.

## Worked Examples

### Example 1: Implementing a Data Quality Monitoring Framework for a Wealth Management Platform

**Scenario:** A $5B RIA operating on Orion PMS with Schwab and Fidelity custody, Salesforce CRM, and a proprietary client portal discovers recurring issues: quarterly performance reports for 15 clients contained incorrect returns traced to stale bond pricing, three clients received bills calculated on positions that had already been transferred out (custodian data lag), and the compliance team found that 8% of client records lacked updated suitability questionnaires despite a firm policy requiring annual review. No systematic data quality monitoring exists — issues surface only when clients or advisors complain.

**Design Considerations:** The firm establishes a data quality monitoring framework across four data domains. For pricing data: daily automated validation compares vendor prices against prior day (flag >5% variance for bonds, >15% for equities), detects stale prices (unchanged >2 business days for equities, >5 for bonds, adjusted for holidays), cross-checks Schwab and Fidelity pricing against the primary vendor, and generates a pricing exception dashboard reviewed by operations before the nightly valuation batch. For position data: daily custodian-to-PMS reconciliation with automated matching on security identifier, quantity, and market value (tolerance: 0.01% of market value), transfer detection logic that flags accounts with zero positions at one custodian and new positions at another, and position breaks categorized by severity (>$10K critical, >$1K high, <$1K medium). For client data: weekly completeness scan checking all required fields (SSN, address, suitability questionnaire date, beneficiary designation, trusted contact), monthly timeliness check flagging suitability questionnaires older than 13 months, quarterly CRM-to-custodian consistency check on legal name, address, and account registration. For billing data: pre-billing validation comparing billing AUM against PMS valuations (flag >0.5% variance), account-level fee schedule validation (advisory fee within contracted range), and terminated account detection (no billing for accounts closed >30 days). Golden source designations are formalized: Schwab/Fidelity for positions and legal identity, Salesforce for relationship and suitability data, Orion for performance, and the pricing vendor for security valuations. A weekly data quality scorecard is generated and reviewed in the Monday operations meeting.

**Analysis:** The framework addresses all three original issues systematically. Stale bond pricing is caught by the daily pricing validation before it reaches performance calculations. Transferred-out positions are detected by the position reconciliation before billing runs. Stale suitability data is flagged by the completeness scan with sufficient lead time for advisor outreach. The ongoing cost is approximately 0.5 FTE of operations analyst time plus monitoring tool licensing. The firm targets resolution within 6 months: 99.5% pricing accuracy, <0.1% position breaks by value, and 95% client data completeness. The weekly scorecard creates organizational accountability — when the COO sees pricing exception rates trending upward, the conversation shifts from reactive firefighting to proactive vendor management and process improvement.

### Example 2: Building Validation Rules for a Security Pricing Pipeline

**Scenario:** An asset manager values 3,500 securities nightly across US/international equities, corporate bonds, municipal bonds, structured products, and alternative investments held in 50 institutional separate accounts and 8 commingled funds. The current pricing process loads a single vendor file with no validation — the operations team manually reviews a sample of 50 prices per night. Recent incidents: a structured product priced at par for two weeks after the vendor discontinued coverage (the file contained the last known price with no flag), an international equity priced in the wrong currency (GBP instead of USD) causing a 30% valuation error for one fund, and a municipal bond with a decimal-point error (10.50 instead of 105.00) that produced a material NAV error caught only by a shareholder complaint.

**Design Considerations:** The firm implements a multi-layer validation pipeline. Layer 1 (file-level): verify file arrival by expected time (6:30 PM ET for EOD pricing), validate record count within expected range (3,400-3,600, flag if <3,300 or >3,700), check file format integrity (header, delimiter, encoding). Layer 2 (field-level): every price must be positive numeric, currency code must be valid ISO 4217 and match the security master's expected currency, price date must equal the expected business date, identifier (CUSIP/ISIN) must exist in the security master. Layer 3 (cross-field): price-times-quantity must produce a reasonable market value per position (flag if single position >20% of fund NAV for diversified strategies), bond prices should be expressed in standard convention (percentage of par for most, dollar price for converts — validate against security type). Layer 4 (temporal): variance check against prior day — thresholds by asset class (equities 15%, investment-grade bonds 3%, high-yield 8%, structured products 10%, munis 5%), stale price detection with asset-class-specific windows (equities 2 days, liquid bonds 5 days, structured products 15 days, alternatives 45 days), and price-unchanged detection distinguished from true staleness (a money market fund NAV of 1.0000 unchanged for months is correct, not stale). Layer 5 (cross-source): secondary vendor comparison for all securities with >$1M total exposure, flag divergence exceeding thresholds (equities 2%, bonds 5%). Exception routing: critical exceptions (zero price, wrong currency, missing file, NAV-impacting variance) alert the pricing analyst immediately and block the valuation batch. High exceptions (stale prices, moderate variance) must be resolved before batch but do not trigger immediate alerts. The pricing analyst resolves exceptions via a defined hierarchy: accept primary vendor price, substitute secondary vendor price, obtain broker quote, or apply manual override (requires supervisor approval and documented rationale in the audit trail).

**Analysis:** The five-layer pipeline catches all three prior incident types. The discontinued structured product would be caught by stale-price detection at Layer 4. The currency mismatch would be caught at Layer 2 (currency code validation against security master). The decimal-point error would be caught at Layer 4 (variance check) and Layer 5 (cross-source comparison). The firm targets a false positive rate below 3% of the universe per night to keep the pricing analyst's workload manageable, calibrating thresholds through a 30-day baseline period before activating blocking behavior. The most important design decision is making critical exceptions block the valuation batch — this prevents bad data from reaching NAV calculations and client reports, converting a downstream client-facing error into an internal operational issue resolved before market open.

### Example 3: Conducting a Data Quality Assessment for Regulatory Reporting Readiness

**Scenario:** A mid-size broker-dealer and RIA (dual-registered, $8B AUM, 200 employees) is preparing for a likely SEC examination. The CCO has identified regulatory reporting as a risk area: the firm files Form ADV, Form CRS, 13F filings, FOCUS reports (broker-dealer), and provides GIPS-compliant performance presentations to institutional prospects. The CCO wants a data quality assessment to identify and remediate gaps before the examination.

**Design Considerations:** The assessment is structured by regulatory obligation, evaluating data quality across all six dimensions for each filing's source data. Form ADV: verify AUM calculation traces to custodian position data through a documented process with reconciled inputs (accuracy, lineage), confirm client count matches the CRM with documented methodology for counting (completeness), check that fee schedules in ADV Part 2A match the billing system configuration (consistency), verify disciplinary history disclosures against FINRA BrokerCheck and firm records (accuracy). 13F filings: validate that the security universe in the filing matches all 13(f) securities held across all accounts (completeness), confirm share quantities reconcile to custodian records as of the reporting date (accuracy), verify security classification against the SEC's Official List of Section 13(f) Securities (validity), document the data flow from custodian positions through aggregation to the filed report (lineage). FOCUS reports: trace each line item to source ledger entries with documented calculation methodology (lineage, accuracy), validate net capital computation inputs against trial balance (accuracy, consistency), confirm customer reserve calculation (Rule 15c3-3) uses reconciled position and cash data (accuracy). GIPS presentations: verify composite membership lists against the firm's inclusion/exclusion criteria and document any discretion removals (completeness, validity), confirm return calculations use custodian-reconciled valuations (accuracy), validate that presentations include all required disclosures and that historical returns have not been retroactively altered except through documented error correction procedures (consistency, validity). Cross-cutting assessment: map all reporting data elements to their golden sources and document gaps in golden source designation, profile all critical reporting fields for completeness and validity, test timeliness by comparing actual data availability against filing deadlines with buffer, and verify that the firm can reproduce any previously filed report from archived source data (a common SEC examination request). Remediation is prioritized: critical findings (data that would produce incorrect filings) targeted for 30-day resolution, high findings (missing lineage documentation, incomplete golden source designations) targeted for 60 days, medium findings (process documentation gaps, monitoring enhancements) targeted for 90 days.

**Analysis:** The assessment transforms regulatory reporting from a periodic clerical exercise into a continuously quality-controlled process. The most common examination finding in this area is inability to reproduce filed figures — firms that cannot trace a 13F position count or ADV AUM figure back to source data face adverse findings. The assessment typically reveals that lineage documentation is the largest gap (firms produce correct reports but cannot demonstrate how), followed by completeness issues in less-frequent filings. The remediation effort is substantial (estimated 200-400 hours across compliance, operations, and technology) but materially reduces examination risk.

## Common Pitfalls

- **No designated golden source per data element.** Without explicit golden source designation, multiple systems maintain competing versions of the same data, creating irreconcilable conflicts and no authoritative answer during disputes or examinations.
- **Validating data after loading rather than before.** Once invalid data enters production, it propagates to downstream systems before corrections can be applied. Validation must gate the loading process, not follow it.
- **Treating data quality as a technology project rather than a business program.** Technology enables quality, but governance requires business ownership, data steward accountability, and executive sponsorship. Technology-only initiatives produce tools without sustained adoption.
- **Setting validation thresholds too tight or too loose.** Thresholds too tight generate excessive false positives, causing alert fatigue and ignored exceptions. Thresholds too loose miss material errors. Calibrate using historical data and adjust quarterly.
- **Ignoring data quality for low-frequency processes.** Quarterly or annual processes (regulatory filings, tax reporting, GIPS presentations) receive less operational attention than daily processes, but their data quality failures have disproportionate regulatory and reputational impact.
- **Measuring data quality without acting on measurements.** Scorecards and dashboards are meaningless without defined remediation workflows, assigned owners, and accountability for improvement. Measurement without action creates a false sense of governance.
- **Assuming vendor data is correct.** Vendor data must be validated like any other source. Vendors have errors, coverage gaps, and delivery failures. Multi-vendor comparison is a critical quality control, not optional.
- **Neglecting data lineage until a regulator asks.** Constructing lineage retroactively is expensive and error-prone. Building lineage into data pipelines from inception costs a fraction of retrofitting it under examination pressure.
- **Manual exception management without workflow tooling.** Tracking exceptions in email or spreadsheets leads to lost exceptions, inconsistent resolution, no metrics, and no audit trail. Exception management requires purpose-built workflow with assignment, SLA tracking, and reporting.
- **Confusing data quality with data quantity.** Having more data sources does not improve quality — it increases complexity. Each additional source requires integration, validation, and conflict resolution. Fewer, higher-quality sources with robust validation outperform many loosely managed sources.
- **Failing to version validation rules.** When validation rules change, historical exception data becomes incomparable. Version validation rule sets and document changes to support trend analysis and audit.
- **Underinvesting in data quality for client data relative to market data.** Firms typically build robust pricing validation but neglect client data quality. Client data errors cause AML screening failures, billing disputes, regulatory findings, and servicing breakdowns with direct client impact.

## Cross-References

- **reference-data** (Layer 13, data-integration) — Reference data (security master, client master, account master) is the primary domain where data quality governance applies; quality of reference data determines quality of all downstream processes.
- **market-data** (Layer 13, data-integration) — Market data pricing quality is a critical data quality domain; real-time and EOD pricing validation rules are a core application of data quality principles.
- **integration-patterns** (Layer 13, data-integration) — Integration failures (file delivery issues, API errors, transformation bugs) are a leading source of data quality issues; integration architecture determines lineage capture capability.
- **reconciliation** (Layer 12, client-operations) — Reconciliation is the primary detective control for data quality, comparing positions, transactions, and cash across systems to identify breaks caused by data quality failures.
- **gips-compliance** (Layer 9, compliance) — GIPS requires documented data quality controls for performance data, including composite completeness, valuation accuracy, and return calculation integrity.
- **books-and-records** (Layer 9, compliance) — Data quality directly affects regulatory recordkeeping obligations; inaccurate or incomplete records violate SEC Rule 17a-4 and Investment Advisers Act requirements.
- **regulatory-reporting** (Layer 9, compliance) — Regulatory filings (Form ADV, 13F, FOCUS, Form PF) depend on accurate, complete source data; data quality failures in reporting data carry direct regulatory risk.
- **operational-risk** (Layer 11, trading-operations) — Data quality failures are an operational risk category; material data errors can cause financial losses, regulatory sanctions, and reputational damage.
