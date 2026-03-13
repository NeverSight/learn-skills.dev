---
name: client-onboarding
description: "Design and implement end-to-end client onboarding workflows from prospect intake through funded account, covering KYC verification, document collection, e-signature, and custodian submission. Use when the user asks about building a digital onboarding flow, integrating identity verification or CIP checks, reducing NIGO rejection rates, opening complex account types like trusts or entities, connecting to custodian APIs, designing suitability questionnaires, or comparing advisor-assisted vs self-service models. Also trigger when users mention 'new account opening', 'onboarding bottleneck', 'KYC integration', 'beneficial ownership', 'OFAC screening', 'account funding', or 'onboarding automation'."
---

# Client Onboarding

## Purpose
Guide the design and implementation of client onboarding workflows for wealth management and advisory firms. This skill covers the end-to-end process from prospect intake through funded account — including digital identity verification, suitability data collection, account type selection, document generation, e-signature, custodian submission, and initial investment. It enables a user or agent to design, evaluate, or troubleshoot onboarding systems that satisfy regulatory requirements while minimizing friction for advisors and clients.

## Layer
10 — Advisory Practice (Front Office)

## Direction
prospective

## When to Use
- Designing or redesigning a digital client onboarding workflow
- Evaluating onboarding platforms or technology vendors
- Integrating KYC/CIP verification into account opening processes
- Building document collection and generation pipelines for new accounts
- Implementing e-signature workflows for account opening forms
- Connecting onboarding systems to custodian APIs (Schwab, Fidelity, Pershing)
- Troubleshooting high NIGO (Not In Good Order) rejection rates
- Designing suitability and risk profiling questionnaires for new clients
- Determining which compliance checkpoints to embed in onboarding flows
- Opening complex account types (trusts, entities, estates) that require additional documentation
- Comparing advisor-assisted vs self-service (digital-direct) onboarding models
- Measuring onboarding efficiency and identifying workflow bottlenecks

## Core Concepts

### Onboarding Workflow Architecture
Client onboarding is an orchestrated, multi-stage process that transforms a prospect into a funded, investable account. The canonical stages are:

1. **Prospect intake** — capture contact information, establish CRM record, assign advisor
2. **Identity verification** — CIP/KYC checks (name, DOB, address, SSN/TIN, government ID)
3. **Suitability data collection** — investment objectives, risk tolerance, time horizon, financial situation
4. **Account type selection** — individual, joint, trust, IRA, entity, or other structure
5. **Document generation** — assemble the required document package based on account type and features
6. **E-signature** — execute new account forms, agreements, and disclosures electronically
7. **Custodian submission** — transmit the completed application to the custodian for account creation
8. **Funding** — ACH, wire, ACAT transfer, or check deposit to fund the new account
9. **Initial investment** — assign the funded account to a model portfolio or execute the initial trade

The two primary flow models are **advisor-assisted** and **self-service (digital-direct)**. In advisor-assisted onboarding, the advisor guides the client through each step, often in a meeting or screen-share, with the onboarding platform pre-populating data from the CRM. In self-service onboarding, the client completes a guided digital workflow independently, with the advisor reviewing and approving the completed application. Most firms support a hybrid model where self-service handles simple account types and advisor-assisted handles complex ones.

The onboarding platform acts as an orchestrator across multiple downstream systems: CRM (client master), KYC/AML vendor (identity verification), custodian (account opening API), document management (storage and retrieval), and portfolio management system (model assignment). The platform must manage state transitions, handle errors at each stage, and provide visibility to both the advisor and compliance.

### Digital Identity Verification
Identity verification during onboarding must satisfy CIP requirements under USA PATRIOT Act Section 326 and, for legal entities, the FinCEN CDD Rule (31 CFR 1010.230). The onboarding workflow collects the following minimum identifying information:

- **Individuals:** Full legal name, date of birth, residential address, Social Security Number (or TIN for non-citizens)
- **Entities:** Legal name, formation date, principal place of business, EIN/TIN, formation documents

**Verification methods integrated into digital onboarding:**

- **Database verification** — real-time API calls to identity verification vendors (LexisNexis Risk Solutions, Equifax, TransUnion, Alloy) that cross-reference provided data against credit bureau, public records, and government databases. This is the most common method for digital onboarding because it requires no document handling and provides a pass/fail result in seconds.
- **Document verification** — the client uploads a photo of a government-issued ID (driver's license, passport), and optionally a selfie for facial comparison. OCR extracts data fields; liveness detection prevents spoofing. Used as a fallback when database verification is inconclusive or as a primary method for non-US persons.
- **Knowledge-based authentication (KBA)** — the client answers challenge questions generated from their credit file (e.g., "Which of the following addresses have you lived at?"). KBA is declining in use due to data breach exposure but remains a supplementary method.
- **Biometric verification** — fingerprint or facial recognition, typically used in mobile onboarding flows.

**OFAC and sanctions screening** is a mandatory gate before account opening. The onboarding platform must screen all individuals associated with the account (account holders, authorized signers, beneficial owners, trustees) against the OFAC SDN list, FinCEN 314(a) lists, and any firm-specific restricted lists. A match or potential match must halt the onboarding flow and route to compliance for manual review.

**Beneficial ownership collection for entity accounts** requires identification of every individual who directly or indirectly owns 25% or more of the equity interests in the legal entity, plus at least one individual with significant managerial control (the control person). The onboarding workflow must dynamically present beneficial ownership forms when the account type is an entity (LLC, corporation, partnership, certain trusts).

**Enhanced due diligence triggers** that the onboarding system should detect and flag: politically exposed persons (PEPs), connections to high-risk jurisdictions (per FinCEN advisories and FATF guidance), complex multi-layered ownership structures, and negative news screening results. When EDD is triggered, the onboarding flow should pause and escalate to the compliance team before proceeding.

### Suitability and Risk Profiling
Onboarding is the primary data collection event for investment suitability. Before any investment recommendation can be made, the firm must gather sufficient information to satisfy FINRA Rule 2111 (suitability) for broker-dealers and Regulation Best Interest for BD recommendations, or the fiduciary duty of care for registered investment advisers.

**Required data elements:**
- Investment objectives (capital preservation, income, growth, aggressive growth, speculation)
- Time horizon (short-term under 3 years, intermediate 3-10 years, long-term over 10 years)
- Risk tolerance (conservative, moderate, aggressive — and the behavioral willingness to endure volatility)
- Liquidity needs (anticipated withdrawals, major expenses, emergency reserves)
- Annual income and net worth (including liquid net worth)
- Investment experience (years of experience, asset classes traded, knowledge level)
- Tax status (marginal tax bracket, tax-sensitive vs tax-exempt accounts)
- Special circumstances (concentrated stock positions, employer restrictions, ESG preferences)

**Risk questionnaire design** follows two approaches:

- **Psychometric questionnaires** measure the client's emotional and behavioral relationship with risk — willingness to accept losses, reaction to market downturns, comfort with uncertainty. These are better at capturing true risk tolerance but can be subjective.
- **Knowledge-based questionnaires** assess the client's understanding of investment concepts and their objective financial capacity to bear risk. These are more defensible from a compliance standpoint but may not capture behavioral tendencies.

Best practice is a combined approach: psychometric questions to assess willingness, financial data to assess capacity, and a mapping algorithm that produces a risk score or category. The risk score then maps to a model portfolio or investment strategy range.

**Regulatory requirements at onboarding:** The suitability profile must be documented before the first investment recommendation. For discretionary accounts, the investment policy statement (IPS) should be established during onboarding. For Reg BI accounts, the Care Obligation requires that any recommendation — including account type — have a reasonable basis given the client's profile.

### Account Type Selection and Configuration
The onboarding workflow must guide account type selection based on the client's needs. Account types and their key characteristics:

**Individual and joint accounts:**
- Individual taxable — single owner, simplest structure
- Joint Tenants with Right of Survivorship (JTWROS) — co-owners; on death, surviving owner inherits automatically
- Tenants in Common (TIC) — co-owners; each owns a specified share that passes to their estate
- Community Property — available in community property states; assets acquired during marriage are jointly owned

**Retirement accounts:**
- Traditional IRA — tax-deductible contributions (subject to income limits), tax-deferred growth, RMDs at age 73
- Roth IRA — after-tax contributions, tax-free growth and qualified withdrawals, no RMDs during owner's lifetime
- SEP IRA — employer-funded; contribution limits up to 25% of compensation or the annual dollar limit
- SIMPLE IRA — employee salary deferral plus employer match or non-elective contribution
- Inherited IRA — beneficiary account; subject to 10-year distribution rule (SECURE Act) for most non-spouse beneficiaries

**Trust accounts:**
- Revocable (living) trust — grantor maintains control; assets avoid probate; grantor's SSN typically used as TIN
- Irrevocable trust — grantor gives up control; separate tax entity with its own EIN; beneficial ownership rules apply
- Testamentary trust — created by will; requires court documentation

**Entity accounts:**
- LLC — requires articles of organization, operating agreement, EIN, beneficial ownership certification
- Corporation (C-Corp, S-Corp) — requires articles of incorporation, bylaws, corporate resolution, EIN
- Partnership (LP, LLP, GP) — requires partnership agreement, EIN, identification of general partner(s)

**Custodial accounts:**
- UTMA/UGMA — custodian manages assets for a minor until the age of majority (18 or 21 depending on state)

**Estate accounts:**
- Require letters testamentary or letters of administration, death certificate, EIN for the estate

**Account features configured during onboarding:**
- Margin eligibility (requires separate margin agreement and additional disclosures)
- Options approval level (levels 0-4 depending on custodian; requires options agreement and risk disclosure)
- Check writing and debit card access
- Tax lot accounting method selection (specific identification, FIFO, average cost)
- Beneficiary designation (primary and contingent for retirement and TOD accounts)
- Dividend and capital gains reinvestment preferences
- Trusted contact person (FINRA Rule 4512)

### Document Collection and Generation
Each account type requires a specific document package. The onboarding system should dynamically assemble the required documents based on the account type and features selected.

**Universal documents (all account types):**
- New account application form (custodian-specific)
- W-9 (US persons) or W-8BEN/W-8BEN-E (non-US persons)
- Advisory agreement or brokerage agreement
- Form CRS (Client Relationship Summary)
- Privacy notice (Reg S-P)
- Trusted contact person designation

**Account-type-specific documents:**
- Joint accounts: joint account agreement specifying ownership type
- Trust accounts: trust certification (or full trust agreement), trustee identification, trust TIN documentation
- Entity accounts: formation documents (articles of incorporation/organization, partnership agreement), corporate resolution or operating agreement authorizing the account, beneficial ownership certification form (FinCEN)
- IRA accounts: IRA adoption agreement, beneficiary designation form, IRA disclosure statement, rollover/transfer forms (if funding from another retirement account)
- Estate accounts: letters testamentary/administration, death certificate, EIN assignment letter
- Custodial accounts (UTMA/UGMA): custodial account agreement, minor's SSN

**Feature-specific documents:**
- Margin: margin agreement, margin risk disclosure
- Options: options agreement, OCC Characteristics and Risks of Standardized Options document

**Document assembly** in modern onboarding platforms involves pre-populating forms with data already collected during earlier onboarding stages (identity, suitability, account type). The system generates a personalized document package with client data filled in, leaving only signature blocks and any fields that require manual completion. This dramatically reduces errors and accelerates the process.

**Document management considerations:**
- Version control: track which version of each form was used (custodians update forms periodically)
- Expiration tracking: certain documents (e.g., trust certifications, corporate resolutions) may need periodic recertification
- Retention: SEC Rule 17a-4 (broker-dealers) and Rule 204-2 (investment advisers) govern document retention periods — typically 5-6 years, with some records retained for the life of the account
- Storage: documents should be stored in a searchable, indexed repository linked to the client and account records

### E-Signature and Consent
Electronic signatures are legally binding for account opening documents under the E-SIGN Act (15 USC 7001) and the Uniform Electronic Transactions Act (UETA), adopted in some form by 49 states and DC.

**E-SIGN Act requirements for valid electronic signatures:**
- The signer must consent to use electronic records and signatures
- The consent must be informed — the signer must be told what types of records will be provided electronically and how to withdraw consent
- The signer must demonstrate the ability to access electronic records in the format used
- The firm must retain the electronic record in a form that accurately reproduces the original

**E-signature platform integration:** Most advisory firms use DocuSign, Adobe Sign, or custodian-embedded signing tools (e.g., Schwab's e-signature within their account opening API). Integration patterns include:

- **Embedded signing** — the e-signature ceremony is embedded within the onboarding platform's user interface, providing a seamless experience
- **Redirect signing** — the client is redirected to the e-signature vendor's portal to complete signing, then returned to the onboarding platform
- **Email-based signing** — the client receives an email with a link to review and sign documents, completing the process asynchronously

**Consent to electronic delivery** is a prerequisite. Before delivering documents electronically, the firm must obtain the client's affirmative consent, inform them of their right to receive paper copies, and verify their ability to access electronic documents. This consent is typically captured as one of the first steps in a digital onboarding flow.

**Wet signature exceptions:** Some custodians and certain form types still require original (wet ink) signatures. Common exceptions include: certain international account forms, some trust documentation, specific alternative investment subscription agreements, and medallion signature guarantees for account transfers. The onboarding system should identify these exceptions and route them to a wet-signature workflow.

**Signature ceremony design for multi-party accounts:**
- Joint accounts: both owners must sign; the system should define a signing order or allow parallel signing
- Trust accounts: all trustees authorized to act on the account must sign
- Entity accounts: authorized signers per the corporate resolution or operating agreement must sign
- The system must track completion status for each signer and send reminders for incomplete ceremonies

**Audit trail requirements:** The e-signature record must include: signer identity (name, email), timestamp of each signature, IP address, authentication method used, document hash (to prove the signed document was not altered post-signature), and a certificate of completion. This audit trail must be retained as part of the account records.

### Custodian Submission and Account Funding
After documents are signed, the completed application package is submitted to the custodian for account creation. Submission methods vary by custodian and account complexity:

**API-based submission (straight-through processing):**
- Major custodians (Charles Schwab, Fidelity, Pershing, TD Ameritrade/Schwab) offer account opening APIs that accept structured data and documents
- The onboarding platform submits client data, account configuration, and signed documents programmatically
- The custodian validates the submission and returns an account number (typically within minutes to hours for standard accounts)
- This is the target state for high-volume firms seeking straight-through processing (STP)

**Semi-automated submission:**
- Some custodians accept submissions through their advisor portal with pre-populated data
- The onboarding platform generates a data file or pre-fills the custodian's web forms
- An operations team member reviews and clicks "submit" — human-in-the-loop

**Manual submission:**
- Complex account types (certain trusts, estates, entities, international accounts) often require manual submission
- Signed documents are uploaded to the custodian's document portal or sent via secure file transfer
- Processing time ranges from days to weeks depending on account complexity

**NIGO (Not In Good Order) handling:**
A NIGO rejection means the custodian has found errors or missing information in the application. Common NIGO causes:
- Missing or illegible signatures
- Inconsistent data between forms (e.g., name on W-9 does not match account application)
- Missing required documents (e.g., trust certification not included)
- Invalid or expired identity documents
- Missing beneficial ownership certification for entity accounts
- Incorrect account type coding
- Missing beneficiary designation for retirement accounts

NIGO remediation workflow: the onboarding system should receive NIGO notifications from the custodian (via API callback, email, or status polling), parse the rejection reason, notify the advisor and/or client, collect the corrected information or documents, and resubmit. Reducing NIGO rates is one of the highest-impact onboarding optimizations.

**Account funding methods:**
- **ACH transfer** — electronic transfer from a linked bank account; typically 2-4 business days; requires bank account verification (micro-deposits, Plaid, or manual voided check)
- **Wire transfer** — same-day or next-day funding for large amounts; requires wire instructions from the custodian
- **ACAT transfer** — Automated Customer Account Transfer system (DTCC) for transferring assets from another brokerage; typically 4-6 business days for full transfers; partial ACAT for specific positions
- **Check deposit** — physical check or mobile check deposit; subject to hold periods
- **In-kind transfer** — transferring existing securities without liquidating; important for tax-sensitive clients
- **Rollover** — direct rollover from employer plan or another IRA; requires rollover paperwork from the distributing institution

**Initial investment:** Once the account is funded, the onboarding system should trigger model portfolio assignment. For discretionary accounts, this means linking the account to the appropriate model in the portfolio management system (PMS) and generating the initial trade orders. For non-discretionary accounts, the advisor submits the first investment recommendation.

### Compliance Checkpoints
Effective onboarding embeds compliance gates at specific stages, preventing the workflow from advancing until requirements are met:

**Gate 1 — Identity verification (before account opening):**
- CIP verification must return a pass result
- OFAC/sanctions screening must clear all associated individuals
- If either fails, the flow halts and routes to compliance
- No account can be opened until identity is verified (USA PATRIOT Act Section 326)

**Gate 2 — Suitability documentation (before investment):**
- Investment profile (objectives, risk tolerance, time horizon, financial situation) must be completed
- Risk questionnaire must be scored and documented
- For Reg BI: the initial recommendation (including account type recommendation) must have a documented reasonable basis
- For fiduciary advisers: the suitability profile must support the proposed investment strategy

**Gate 3 — Beneficial ownership (before entity account opening):**
- FinCEN beneficial ownership certification must be completed for all legal entity accounts
- 25% owners and at least one control person must be identified and verified
- Exempt entity types (publicly traded companies, regulated financial institutions, government entities) must be documented

**Gate 4 — Disclosure delivery (before or at account opening):**
- Form CRS must be delivered before or at the time of opening the account
- Form ADV Part 2A (RIAs) must be delivered before or at the time of entering the advisory agreement
- Privacy notice must be delivered at account opening
- Margin and options disclosures must be delivered if those features are selected

**Gate 5 — Supervisory review (risk-based, before account activation):**
- Certain account types or client profiles trigger mandatory supervisory review before the account becomes active
- Common triggers: discretionary authority requested, margin or options trading, senior investors (age 65+), high-net-worth thresholds, PEPs or EDD clients, concentrated positions, complex entity structures
- The supervisor reviews the application package, suitability documentation, and any compliance flags
- The system must track review status and prevent account activation until supervisory approval is recorded

**Compliance hold and escalation:**
- When any gate fails, the application enters a compliance hold state
- The system notifies the compliance team with the specific failure reason and supporting documentation
- Escalation paths: line supervisor, compliance officer, chief compliance officer, legal counsel
- Resolution options: request additional information from the client, approve with conditions, decline the account
- All compliance decisions must be documented and retained

### Data Flow and System Integration
Onboarding is the primary data collection event that populates downstream systems. The data collected during onboarding flows to:

- **CRM (client master)** — contact information, household relationships, advisor assignment, service tier, communication preferences. The CRM should be the first system updated, often serving as the source of truth for client identity data.
- **Portfolio management system (PMS)** — account number, model portfolio assignment, investment restrictions, tax lot method, rebalancing preferences. The PMS receives the new account once it is created at the custodian and funded.
- **Custodian/account master** — the custodian maintains the official account record, including registration, tax status, beneficiaries, and authorized parties. The onboarding system submits data to the custodian; the custodian returns the account number and confirmation.
- **Compliance systems** — KYC/AML records, suitability documentation, disclosure delivery confirmations, supervisory review records. These records must be retained per regulatory requirements and accessible for examinations.
- **Document repository** — signed account opening documents, identity verification records, formation documents for entities, trust certifications. Must be indexed by client and account for retrieval.
- **Financial planning system** — goals, time horizons, income projections, tax data. If the firm uses a planning tool, onboarding data should feed into the initial plan.

**Integration patterns:**
- **Real-time API calls** — for identity verification, custodian submission, OFAC screening. These require immediate responses and should include timeout handling and fallback procedures.
- **Asynchronous/event-driven** — for downstream notifications (e.g., notifying the PMS that a new account is ready for model assignment). Message queues or webhook patterns are common.
- **Batch processing** — some custodian integrations operate on batch submission cycles (e.g., end-of-day file uploads). The onboarding system must queue submissions and reconcile results.

**Data validation:** The onboarding system should validate data consistency across systems. Common validation checks:
- Name and SSN/TIN match across all forms and systems
- Account type is consistent between the onboarding platform and custodian
- Beneficiary designations match between the onboarding record and custodian record
- Advisor assignment in CRM matches the advisory agreement
- Tax lot method in the PMS matches the client's election

**Pre-population for existing clients:** When an existing client opens an additional account, the onboarding system should pre-populate known data from the CRM and existing account records. Identity verification may be streamlined (re-verification vs full CIP depending on firm policy), and suitability data may only need to be confirmed rather than re-collected.

### Onboarding Metrics and Optimization
Measuring onboarding effectiveness enables continuous improvement:

**Key performance indicators:**
- **Time-to-funded-account** — elapsed time from prospect intake to first funded dollar. Industry benchmarks: 3-5 business days for simple accounts via digital onboarding, 2-4 weeks for complex accounts. Target for best-in-class digital: same day for individual taxable accounts.
- **Application abandonment rate** — percentage of onboarding flows started but not completed. High abandonment at a specific step indicates friction. Industry average: 25-40% for digital-direct flows; significantly lower for advisor-assisted.
- **NIGO rate** — percentage of submissions rejected by the custodian. Target: under 5%. Industry average: 10-20% for firms without automated validation.
- **Straight-through processing (STP) rate** — percentage of applications that pass from submission to account creation without manual intervention. Target: above 80% for standard individual and joint accounts.
- **First-contact resolution rate** — percentage of onboarding issues resolved without requiring the client to take additional action.
- **Client satisfaction score** — post-onboarding survey measuring the client's experience.

**Bottleneck identification:**
- Analyze time spent at each onboarding stage to identify where applications stall
- Common bottlenecks: identity verification failures (especially for non-US persons), missing trust documents, client delays in completing e-signature, custodian processing backlogs, compliance review queues
- Implement dashboards showing pipeline status: how many applications are at each stage, average time per stage, aging applications

**Optimization strategies:**
- **Reduce data entry** — pre-populate from CRM, use OCR for document data extraction, integrate with bank verification services (Plaid, Yodlee) for funding
- **Validate early** — run real-time validation checks as data is entered rather than waiting for custodian submission; catch NIGO-causing errors before documents are signed
- **Parallelize where possible** — run identity verification while the client completes the suitability questionnaire; generate documents while waiting for verification results
- **Design mobile-first** — clients increasingly complete onboarding on mobile devices; forms must be responsive and signature flows must work on small screens
- **A/B test onboarding flows** — test different question orders, form layouts, and communication cadences to reduce abandonment
- **Automate follow-up** — send automated reminders for incomplete applications, unsigned documents, and unfunded accounts

## Worked Examples

### Example 1: Designing a digital onboarding flow for individual taxable accounts
**Scenario:** A mid-sized RIA with $2B AUM and 50 advisors wants to implement digital onboarding for individual taxable accounts. The firm uses Schwab as its primary custodian, Salesforce as its CRM, and Orion as its portfolio management system. Currently, onboarding is paper-based, takes 7-10 business days, and has a 22% NIGO rate. The firm wants to reduce time-to-funded-account to under 3 business days and NIGO rate below 5%.

**Design Considerations:**
- The onboarding platform must integrate with Schwab's account opening API, Salesforce for client data pre-population, and Orion for model portfolio assignment
- Identity verification should use a database verification vendor (such as Alloy or LexisNexis) as the primary method, with document verification (ID upload) as fallback
- OFAC screening must be integrated as an automated gate that runs immediately after identity data is collected
- The suitability questionnaire should combine psychometric risk tolerance questions with financial data collection, producing a risk score that maps to the firm's model portfolios
- Document generation should be fully automated: the system assembles the Schwab new account form, W-9, advisory agreement, Form CRS, privacy notice, and trusted contact designation, pre-populated with collected data
- E-signature should be embedded in the onboarding flow (not email-based) to minimize drop-off, using DocuSign or Schwab's native e-signature
- Real-time validation must check for common NIGO causes before custodian submission: name consistency, SSN format, complete address, all required signatures present
- After Schwab returns the account number, the system should automatically initiate ACH funding (if the client linked a bank account during onboarding) and notify Orion to assign the account to the model portfolio matching the client's risk score

**Analysis:** The recommended flow is: (1) advisor initiates onboarding from Salesforce, pre-populating known client data; (2) client receives a secure link to complete onboarding digitally; (3) client enters personal information and the system runs real-time identity verification and OFAC screening; (4) client completes the suitability questionnaire and the system generates a risk score; (5) system presents the recommended model portfolio and the advisor confirms; (6) document package is generated and the client signs electronically; (7) system validates the complete package against Schwab's requirements; (8) application is submitted to Schwab via API; (9) Schwab returns the account number; (10) ACH funding is initiated and Orion receives the new account for model assignment. For the 22% NIGO rate, the primary remediation is step 7 — pre-submission validation that catches the errors Schwab would reject. Common causes like name mismatches, missing signatures, and incomplete forms can be caught in real time. The 3-business-day target is achievable for the digital path: identity verification and document signing can occur in a single session (day 1), Schwab API submission processes within hours (day 1-2), and ACH funding settles in 2-3 business days (day 2-3).

### Example 2: Onboarding a trust account for a high-net-worth client
**Scenario:** An advisor at a registered investment adviser is onboarding a new high-net-worth client who wants to invest $5M through a family irrevocable trust. The trust was established 3 years ago, has its own EIN, and names the client and her attorney as co-trustees. The trust has four beneficiaries (the client's adult children). The client also wants a personal taxable account and a Roth IRA.

**Design Considerations:**
- The irrevocable trust is a legal entity requiring full beneficial ownership certification under the FinCEN CDD Rule: identify all individuals owning 25% or more of the trust's beneficial interests and at least one control person
- With four beneficiaries who are the beneficial interest holders, the firm must determine if any owns 25% or more. If the trust splits evenly (25% each), all four meet the threshold and must be identified. The control persons are the co-trustees (the client and her attorney)
- The trust requires its own EIN, a trust certification (or relevant pages of the trust agreement showing formation, trustees, and investment powers), and verification that the trustees have authority to open investment accounts
- Enhanced due diligence considerations: $5M meets most firms' high-net-worth thresholds for supervisory review; irrevocable trust is a complex structure warranting additional scrutiny of the trust's purpose and source of funds
- The personal taxable account and Roth IRA can follow the standard individual onboarding flow; identity verification for the client carries across all three accounts
- Document packages differ substantially: the trust account requires the new account form in the trust's name, W-9 with the trust's EIN, trust certification, beneficial ownership form, and advisory agreement naming the trust as the client; the taxable account requires standard individual forms with the client's SSN; the Roth IRA requires the IRA adoption agreement, beneficiary designation, and IRA disclosure statement
- All three accounts should be linked to a single household in the CRM and PMS for consolidated reporting

**Analysis:** The onboarding workflow should handle this as a single onboarding event with multiple account openings. Start with client identity verification (CIP), which satisfies requirements for the individual accounts and verifies one of the trustees for the trust account. Then collect suitability data for each account (the trust may have different investment objectives than the personal accounts). Next, request the trust documentation: the full trust certification, trust EIN assignment letter, and identification information for the co-trustee (attorney) and all four beneficiaries. Run OFAC screening on all individuals (client, attorney co-trustee, four beneficiaries — six people total). Complete the FinCEN beneficial ownership certification form. Route the trust account application through supervisory review given the complexity and dollar amount. Generate three separate document packages, one per account. The trust account will likely require manual or semi-automated submission to the custodian even if the individual accounts can use API submission, due to the additional documentation. Expect the trust account to take 1-2 weeks from submission to account opening, while the individual accounts can be opened within days. Funding the trust account via wire transfer is common for this dollar amount; the taxable account can be funded via ACAT if the client has an existing brokerage account elsewhere; the Roth IRA may involve a rollover or contribution depending on the source of funds.

### Example 3: Reducing a 35% NIGO rate
**Scenario:** A broker-dealer and RIA with 200 advisors processes 500 new account applications per month through a combination of custodians (Schwab, Fidelity, Pershing). The firm's current NIGO rate is 35%, meaning 175 applications per month are rejected on first submission. Average remediation time for a NIGO rejection is 5 business days, and the operations team spends 60% of its time on NIGO resolution. The firm wants to reduce the NIGO rate to under 10%.

**Design Considerations:**
- First priority is to categorize existing NIGO rejections by cause. Common categories: missing signatures (often 20-30% of NIGOs), data inconsistencies between forms (15-25%), missing or expired documents (15-20%), incorrect account type coding (10-15%), incomplete beneficiary designations (5-10%), missing beneficial ownership for entities (5-10%)
- Each custodian has different form requirements and validation rules; the firm must maintain a rules engine that knows each custodian's specific requirements
- The root cause is often that advisors complete forms manually with no real-time validation, and errors are not caught until the custodian reviews the application days later
- Multi-custodian complexity amplifies the problem: advisors must know which forms and requirements apply to each custodian, and mistakes are more likely when switching between custodians

**Analysis:** A phased approach to reducing the NIGO rate from 35% to under 10%:

Phase 1 — Diagnose (weeks 1-2): Categorize the last 6 months of NIGO rejections by custodian, account type, rejection reason, and originating advisor. Identify the top 5 rejection reasons, which will typically account for 70-80% of all NIGOs. Identify whether certain advisors or offices have disproportionately high NIGO rates (indicating a training issue vs a systemic issue).

Phase 2 — Implement pre-submission validation (weeks 3-8): Build a validation rules engine that checks every application against the applicable custodian's requirements before submission. Critical validations: all required fields populated, signatures present on all required pages, name and SSN/TIN consistent across all forms, account type code matches the application data, beneficiary designation complete for retirement accounts, beneficial ownership form included for entity accounts, required supporting documents attached (trust certification, formation documents). The validation engine should prevent submission until all checks pass and provide clear error messages to the advisor or operations team.

Phase 3 — Automate document assembly (weeks 6-12): Replace manual form completion with automated document generation that pre-populates custodian-specific forms from a single data collection workflow. This eliminates the majority of data inconsistency errors because data is entered once and propagated to all forms. Support all three custodians with custodian-specific form templates and validation rules.

Phase 4 — Train and monitor (ongoing): Provide targeted training to advisors with high NIGO rates. Publish a weekly NIGO dashboard showing rates by custodian, account type, rejection reason, and advisor. Set NIGO rate targets (under 15% at 90 days, under 10% at 180 days) and review progress monthly.

Expected outcome: Pre-submission validation alone typically reduces NIGO rates by 50-60% (from 35% to 14-17%). Adding automated document assembly reduces the remaining errors by another 50% or more (to 7-10%). The combined effect should achieve the sub-10% target within 6 months, freeing the operations team to focus on complex account types rather than routine error remediation.

## Common Pitfalls
- Opening an account before identity verification is complete — CIP must be satisfied before or at account opening, not after
- Collecting suitability data but not documenting it in a format that satisfies regulatory requirements — the profile must be written, signed or acknowledged, and retained
- Using a one-size-fits-all document package rather than dynamically assembling documents based on account type and features
- Not screening all associated individuals (co-owners, trustees, beneficial owners, authorized signers) against OFAC — screening only the primary account holder is insufficient
- Allowing the onboarding flow to proceed past compliance gates when a checkpoint fails — soft gates that can be bypassed undermine the compliance framework
- Assuming e-signatures are universally accepted — certain custodians and form types still require wet signatures
- Not maintaining a mapping between risk questionnaire scores and model portfolios, leading to inconsistent investment recommendations across advisors
- Failing to validate data consistency before custodian submission, resulting in high NIGO rates
- Treating entity and trust onboarding the same as individual onboarding — these account types require substantially more documentation, verification, and review
- Not linking multiple accounts opened for the same client into a single household, causing fragmented client data across CRM and PMS
- Neglecting the funding step — an opened but unfunded account generates no revenue and may be closed by the custodian after an inactivity period
- Collecting beneficial ownership information but not verifying the identities of the beneficial owners, violating the CDD Rule's verification requirement

## Cross-References
- **know-your-customer** (Layer 9, compliance): KYC/CIP requirements that the onboarding identity verification stage must satisfy; the KYC skill defines the regulatory standards, and this skill describes how to implement them in an onboarding workflow
- **investment-suitability** (Layer 9, compliance): Suitability data collection during onboarding provides the foundation for all subsequent investment recommendations; the suitability skill defines the regulatory obligations, and this skill covers how to gather the required data
- **anti-money-laundering** (Layer 9, compliance): OFAC screening and AML checks are embedded compliance gates in the onboarding flow; the AML skill covers the regulatory framework, and this skill describes the integration points
- **reg-bi** (Layer 9, compliance): Reg BI disclosure and care obligations must be satisfied at or before account opening; Form CRS delivery is a required onboarding step for broker-dealers and RIAs
- **client-disclosures** (Layer 9, compliance): Disclosure documents (Form ADV, Form CRS, privacy notice, prospectus) must be delivered during onboarding at prescribed trigger points
- **crm-client-lifecycle** (Layer 10, advisory-practice): The CRM receives client and household data from the onboarding process; onboarding creates the client master record that CRM manages throughout the relationship
- **portfolio-management-systems** (Layer 10, advisory-practice): The PMS receives new accounts from onboarding for model portfolio assignment and initial investment execution
- **privacy-data-security** (Layer 9, compliance): Onboarding collects sensitive nonpublic personal information (SSN, financial data, identity documents) that must be protected under Reg S-P and firm cybersecurity policies
- **account-opening-workflow** (client-operations plugin, Layer 12): Back-office account opening process that receives onboarding outputs; handles operations processing, custodian submission, and account activation
