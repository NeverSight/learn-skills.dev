---
name: anti-money-laundering
description: "Guide BSA/AML compliance program design and operation for broker-dealers, banks, and investment advisers. Use when the user asks about suspicious activity reports, currency transaction reports, OFAC screening, structuring detection, or FinCEN requirements. Also trigger when users mention 'large cash deposit', 'sanctions check', 'money laundering red flags', 'customer risk rating', 'unusual transaction patterns', 'wire to a foreign country', 'SDN list', 'tipping off a client about a SAR', 'AML audit', 'correspondent account due diligence', or ask whether a transaction needs to be reported."
---

# Anti-Money Laundering Compliance

## Purpose
Guide the design and operation of Bank Secrecy Act / Anti-Money Laundering (BSA/AML) compliance programs for broker-dealers, banks, and investment advisers. This skill covers FinCEN reporting obligations, OFAC sanctions screening, red flag identification, customer risk rating, and the regulatory framework for detecting and preventing money laundering and terrorist financing.

## Layer
9 — Compliance & Regulatory Guidance

## Direction
prospective

## When to Use
- Designing or reviewing an AML compliance program under FINRA Rule 3310
- Determining whether a transaction triggers a Currency Transaction Report (CTR) filing
- Evaluating whether activity warrants a Suspicious Activity Report (SAR)
- Screening customers or counterparties against the OFAC SDN list
- Identifying red flags for structuring, layering, or integration
- Assessing customer risk ratings and risk-based monitoring procedures
- Reviewing AML obligations for investment advisers under evolving FinCEN rules
- Handling correspondent or omnibus account due diligence
- Preparing for an independent AML audit or regulatory examination
- Understanding FinCEN enforcement trends and penalty exposure

## Core Concepts

### Bank Secrecy Act (BSA) Framework
The Bank Secrecy Act of 1970 (31 U.S.C. §§ 5311–5332) is the foundational U.S. anti-money laundering statute. It requires financial institutions to assist government agencies in detecting and preventing money laundering by maintaining records and filing reports on certain transactions. The USA PATRIOT Act (2001) significantly expanded BSA obligations, adding enhanced due diligence requirements, information-sharing provisions (Section 314(a) and 314(b)), and the requirement for written AML programs. FinCEN (the Financial Crimes Enforcement Network) is the bureau within the U.S. Treasury Department that administers and enforces BSA compliance. FinCEN issues rules, collects reports (CTRs, SARs), and coordinates with law enforcement.

### FINRA Rule 3310 — AML Compliance Program
FINRA Rule 3310 requires every FINRA member firm to establish and implement a written AML compliance program that includes four pillars:

1. **Written procedures** — Policies and procedures reasonably designed to detect and cause the reporting of suspicious activity. Must be tailored to the firm's business model, products, customer types, and geographic exposure.
2. **Designated AML Compliance Officer (AMLCO)** — A qualified individual responsible for day-to-day AML oversight. The AMLCO must be identified by name and title in the firm's written procedures and registered with FINRA. The AMLCO must have sufficient authority, resources, and expertise.
3. **Independent testing (audit)** — The AML program must be tested independently at least every calendar year (or every two years if the firm does not execute transactions or hold customer funds/securities). Testing may be performed by qualified internal personnel not involved in the AML program or by an outside party.
4. **Ongoing training** — All relevant personnel must receive AML training appropriate to their responsibilities. Training must cover applicable BSA/AML regulations, the firm's own policies, red flags, and how to escalate suspicious activity. Training frequency and content should be documented.

### Currency Transaction Reports (CTRs)
Financial institutions must file FinCEN Form 112 (CTR) for each cash transaction exceeding $10,000 in a single business day (31 CFR § 1010.311). Key rules:

- **$10,000 threshold** — Applies to cash received or disbursed, including currency, coin, cashier's checks (under certain circumstances), and money orders purchased with cash.
- **Aggregation rule** — Multiple cash transactions by or on behalf of the same person during a single business day must be aggregated. If the aggregate exceeds $10,000, a CTR is required.
- **Filing deadline** — CTRs must be filed within 15 calendar days of the transaction date.
- **Structuring prohibition (31 U.S.C. § 5324)** — It is a federal crime to structure transactions (i.e., break up a transaction into smaller amounts) to evade CTR reporting requirements. Both the customer and any employee who assists are liable. Structuring is illegal regardless of the source of the funds — even legitimate funds structured to avoid reporting trigger criminal liability.
- **Exemptions** — Certain customers (e.g., listed companies, government agencies, banks) may be exempt from CTR filing under 31 CFR § 1020.315, but exemptions must be documented and periodically reviewed.

### Suspicious Activity Reports (SARs)
SARs are filed using FinCEN Form 111 to report known or suspected violations of law, suspicious transactions, or transactions with no apparent lawful purpose. Filing thresholds and obligations vary by institution type:

- **Broker-dealers (FINRA members)** — Must file a SAR for transactions of $5,000 or more that the firm knows, suspects, or has reason to suspect involve funds from illegal activity, are designed to evade BSA requirements, lack a business or apparent lawful purpose, or involve use of the firm to facilitate criminal activity (31 CFR § 1023.320).
- **Banks** — Must file a SAR for transactions of $5,000 or more involving known suspects, or $25,000 or more regardless of suspect identification (31 CFR § 1020.320).
- **Filing deadline** — SARs must be filed within 30 calendar days of initial detection. If no suspect is identified, the deadline extends to 60 days.
- **Continuing activity** — If suspicious activity continues, the firm must file continuing SARs at least every 90 days.
- **Tipping-off prohibition** — It is a violation to notify the subject of the SAR that a SAR has been or will be filed (31 U.S.C. § 5318(g)(2)). This prohibition extends to all employees, officers, and directors. Disclosure of a SAR filing can result in criminal penalties.
- **Safe harbor** — Financial institutions and their employees are protected from civil liability for filing SARs in good faith (31 U.S.C. § 5318(g)(3)). This safe harbor applies even if the reported activity turns out to be legitimate.
- **SAR confidentiality** — SARs are confidential. They cannot be produced in response to subpoenas, discovery requests, or FOIA requests (with narrow law enforcement exceptions). The underlying facts that triggered the SAR, however, are not themselves privileged.

### OFAC Screening
The Office of Foreign Assets Control (OFAC), a bureau within the U.S. Treasury, administers and enforces U.S. economic and trade sanctions. Financial institutions must screen customers, counterparties, and transactions against OFAC-maintained lists:

- **SDN List (Specially Designated Nationals and Blocked Persons)** — Individuals and entities owned or controlled by targeted countries, or designated as narcotics traffickers, terrorists, or proliferators. Transactions with SDN-listed parties must be blocked (frozen), and the blocked property must be reported to OFAC within 10 business days.
- **Sectoral Sanctions (SSI List)** — Restrictions on specific types of transactions with identified entities (e.g., prohibiting new debt or equity issuance). The transaction is not fully blocked; only the prohibited type of dealing is restricted.
- **Geographic sanctions** — Comprehensive sanctions programs prohibit virtually all transactions with certain countries or regions (e.g., North Korea, Iran, Cuba, the Crimea region). Any transaction touching a comprehensively sanctioned jurisdiction must be blocked or rejected.
- **Screening obligations** — Firms must screen at account opening, upon receipt of wire transfers or other transactions, and when OFAC updates its lists. Screening must cover all relevant identifiers: names, aliases, addresses, dates of birth, passport numbers, and other identifying information.
- **Strict liability** — OFAC violations are a strict liability regime. A firm can be penalized even if it did not know the counterparty was sanctioned. Penalties can reach millions of dollars per violation.
- **Voluntary self-disclosure** — OFAC looks favorably on voluntary self-disclosure and considers it a significant mitigating factor in enforcement actions.

### Red Flags for Money Laundering
Money laundering follows three stages — placement (introducing illicit funds into the financial system), layering (obscuring the trail through complex transactions), and integration (reintroducing laundered funds into the legitimate economy). Key red flags include:

- **Structuring** — Deposits or withdrawals just below $10,000 (e.g., $9,500, $9,800), especially if repeated across days or accounts. Multiple deposits at different branches in a single day.
- **Rapid movement of funds** — Funds received and immediately wired out, particularly to unrelated third parties or foreign jurisdictions. No economic rationale for the speed of movement.
- **Layering patterns** — Multiple transfers between accounts at different institutions, use of intermediary accounts, frequent conversion between asset types (cash to securities to wire transfers), round-dollar transactions with no apparent business purpose.
- **Integration patterns** — Purchase of high-value assets (real estate, luxury goods, securities) with funds of unclear origin. Use of investment accounts to create the appearance of legitimate investment returns.
- **Shell company activity** — Accounts held by entities with no apparent business operations, nominal capital, nominee directors, or registered in secrecy jurisdictions. Transactions that do not correspond to the entity's stated business purpose.
- **Unusual customer behavior** — Reluctance to provide identification, use of multiple SSNs or TINs, frequent changes to account ownership or signatory authority, unexplained wealth inconsistent with known employment or business.
- **Geographic risk** — Transactions involving jurisdictions identified as high risk by FATF, FinCEN advisories, or the firm's own risk assessment. Unexplained connections to countries with weak AML regimes or under comprehensive sanctions.
- **Third-party transactions** — Deposits or payments by unrelated third parties with no clear explanation, especially if the third party has no apparent relationship to the account holder.

### AML for Investment Advisers
Historically, registered investment advisers (RIAs) have not been subject to BSA/AML program requirements, although the SEC has long advocated extending these rules. In 2024, FinCEN issued a final rule (effective January 1, 2026) requiring certain investment advisers — specifically, SEC-registered investment advisers and exempt reporting advisers — to establish AML/CFT programs, file SARs, and comply with other BSA requirements (31 CFR Part 1032). Key elements:

- Investment advisers covered by the rule must implement risk-based AML programs with the same four pillars as broker-dealers (written procedures, designated compliance officer, independent testing, training).
- Advisers must file SARs and comply with FinCEN information-sharing requests under Section 314(a).
- Advisers with bank or broker-dealer affiliates should coordinate their AML programs to avoid gaps.
- State-registered advisers are not currently covered, but FinCEN may expand coverage in the future.

### Correspondent and Omnibus Account Considerations
Enhanced due diligence applies to correspondent accounts for foreign financial institutions (Section 312 of the USA PATRIOT Act, 31 CFR § 1010.610):

- Firms must assess the AML risk posed by each foreign correspondent relationship, considering the jurisdiction's AML regime, the institution's AML controls, and the nature of the correspondent services provided.
- For shell banks, correspondent accounts are prohibited. Firms must obtain certifications that the foreign institution is not a shell bank and that it will not permit its accounts to be used by shell banks.
- Omnibus accounts (where a single account holds positions for multiple underlying clients) present heightened risk because the firm may have limited visibility into the ultimate beneficial owners. Firms should obtain sufficient information to identify and monitor for suspicious activity, and may need to "look through" the omnibus structure in certain circumstances.

### Customer Risk Rating
A risk-based approach requires firms to assess and assign risk ratings to customers based on factors including:

- **Customer type** — Individuals, entities, trusts, PEPs (politically exposed persons), non-resident aliens, foreign financial institutions.
- **Geographic risk** — Customer domicile, transaction counterparties, and fund flow jurisdictions.
- **Product/service risk** — Higher-risk products include private banking, correspondent accounts, wire transfers, and accounts holding securities in bearer form.
- **Transaction patterns** — Volume, frequency, and nature of transactions relative to the customer's profile.

Risk ratings should be documented, periodically reviewed, and updated when new information becomes available. Higher-risk customers warrant enhanced due diligence (EDD), which may include more frequent transaction monitoring, senior management approval for account opening, and collection of additional documentation on source of funds and source of wealth.

### Recordkeeping Requirements
BSA/AML regulations impose specific recordkeeping obligations:

- **SARs** — Supporting documentation must be retained for 5 years from the date of filing (31 CFR § 1010.320(d)). The SAR itself and all supporting documentation must be made available to FinCEN and law enforcement upon request.
- **CTRs** — Records must be retained for 5 years from the date of the report (31 CFR § 1010.306(a)).
- **CIP records** — Customer identification records (copies of identification documents or descriptions of documents reviewed, methods used to verify identity) must be retained for 5 years after the account is closed (31 CFR § 1023.220(a)(3)).
- **Correspondence and transaction records** — Generally retained for 5 years under BSA and FINRA Rules (FINRA Rule 3110, SEC Rule 17a-4).
- Firms should ensure that AML records are organized, retrievable, and protected from unauthorized access or alteration.

### FinCEN Enforcement Trends and Penalties
FinCEN has significantly increased enforcement activity in recent years. Key trends include:

- **Escalating penalties** — Civil money penalties can reach the greater of the amount involved in the transaction (up to $1 million) or $77,651 per violation (adjusted for inflation under 31 U.S.C. § 5321). Criminal penalties can include imprisonment of up to 10 years.
- **Individual accountability** — FinCEN and DOJ increasingly pursue enforcement actions against individual compliance officers and senior management, not just institutions.
- **Willful blindness** — Firms and individuals can be held liable for willfully failing to implement adequate AML controls, even without direct knowledge of specific illicit transactions.
- **Areas of focus** — Virtual currency exchanges and administrators, money services businesses, and firms with repeated examination deficiencies. FinCEN has also focused on failures to file timely and complete SARs.
- **Coordination with other regulators** — FinCEN actions are frequently accompanied by parallel actions from the SEC, FINRA, OCC, or DOJ, resulting in cumulative penalties and remedial orders.
- **Beneficial Ownership Information (BOI)** — The Corporate Transparency Act (effective 2024) requires many companies to report beneficial ownership information to FinCEN, creating a new tool for AML enforcement and due diligence.

## Worked Examples

### Example 1: Detecting structuring across multiple accounts
**Scenario:** A customer at a broker-dealer makes the following cash deposits over a five-day period: Monday — $8,000 into Account A; Tuesday — $7,500 into Account B (same customer, different registration); Wednesday — $9,000 into Account A; Thursday — $6,000 into Account A; Friday — $8,500 into Account B. No individual deposit or single-day aggregate exceeds $10,000, so no CTR is filed. A compliance analyst reviewing weekly transaction reports notices the pattern.
**Compliance Issues:**
- Although no individual day triggers a CTR, the pattern of repeated cash deposits just below $10,000 across multiple accounts is a classic structuring indicator (31 U.S.C. § 5324).
- The firm has an obligation to monitor for structuring regardless of whether CTR thresholds are met.
- If the analyst has reason to suspect that the transactions are designed to evade CTR requirements, a SAR must be filed.
**Analysis:**
The compliance analyst should escalate the pattern to the AMLCO. The AMLCO should review the customer's profile, transaction history, and stated source of funds. If the cash deposits are inconsistent with the customer's known business or employment, or if the customer has no apparent reason to make frequent cash deposits into a brokerage account, the firm should file a SAR on FinCEN Form 111 within 30 days of the analyst's detection of the pattern. The SAR narrative should describe the structuring pattern, including dates, amounts, and accounts involved. The firm must not inform the customer that a SAR has been filed (tipping-off prohibition). The firm should also consider whether the customer's risk rating should be elevated and whether enhanced monitoring is warranted going forward. All supporting documentation — transaction records, analyst notes, escalation communications — must be retained for 5 years.

### Example 2: Identifying layering through rapid fund movements
**Scenario:** A newly opened brokerage account receives a $500,000 incoming wire from a foreign bank in a FATF-identified high-risk jurisdiction. Within three business days, the customer purchases and sells several highly liquid equities at negligible profit or loss, then requests an outgoing wire of $490,000 to a different bank in a third country. The customer has no prior trading history and the account application lists the customer as a "consultant" with no further detail.
**Compliance Issues:**
- Rapid movement of large funds through securities transactions with no apparent profit motive is a hallmark of layering — the second stage of money laundering.
- The foreign-source wire from a high-risk jurisdiction triggers enhanced due diligence obligations.
- The near-immediate outbound wire to a different jurisdiction suggests the brokerage account is being used as a pass-through vehicle.
- The vague occupation and lack of trading history are additional red flags.
**Analysis:**
The firm should immediately place a hold on the outgoing wire pending review by the AMLCO. The AMLCO should request additional information from the customer regarding the source of the incoming funds, the purpose of the trades, and the relationship to the recipient of the outgoing wire. Regardless of the customer's response, the pattern of activity — incoming wire from a high-risk jurisdiction, rapid buy-sell transactions with no economic rationale, and near-immediate outbound wire to a third country — strongly warrants a SAR filing. The SAR narrative should detail the timeline, amounts, counterparties, and the absence of legitimate business purpose. The firm should also evaluate whether to file a voluntary self-disclosure with OFAC if any aspect of the transaction involves a sanctioned jurisdiction or party. The customer's risk rating should be elevated to high, and the firm should consider whether to exit the relationship (file a SAR before closing the account, and do not disclose the SAR as the reason for account closure).

### Example 3: Handling a match on the OFAC SDN list during onboarding
**Scenario:** During the account opening process, a broker-dealer's automated screening system generates a potential match between a new applicant and an individual on the OFAC SDN list. The applicant's name is "Ahmad Al-Rashid," which matches an SDN entry. The applicant's date of birth and passport country also align with the SDN entry's identifying information.
**Compliance Issues:**
- If the applicant is indeed the SDN-listed individual, the firm is prohibited from opening the account and must block any property or interests in property of the individual.
- OFAC violations carry strict liability — the firm is responsible even if it inadvertently transacts with a sanctioned person.
- A false positive (a different person with the same name) must be carefully distinguished from a true match.
**Analysis:**
The firm should not open the account pending resolution of the OFAC match. The compliance team should compare all available identifying information — full legal name, aliases, date of birth, nationality, passport number, address — against the SDN entry. If the identifying details match or are substantially similar and cannot be distinguished, the firm must treat the applicant as a blocked person. The firm must reject the account application, block any funds or property submitted with the application, and file a blocked property report with OFAC within 10 business days using OFAC's online reporting system. If the compliance team determines that the applicant is definitively not the SDN-listed individual (e.g., different date of birth, different passport number, different country of citizenship), the firm should document the basis for the false-positive determination, retain the documentation, and proceed with normal account opening and CIP/CDD procedures. In ambiguous cases where the firm cannot conclusively confirm or rule out a match, the firm should contact OFAC's hotline (1-800-540-6322) for guidance before proceeding. The entire screening process, analysis, and disposition must be documented and retained.

## Common Pitfalls
- Filing CTRs but failing to monitor for structuring — the obligation to detect evasion exists independently of the CTR filing obligation
- Treating SAR filing as a one-time event rather than monitoring for continuing suspicious activity and filing 90-day continuing SARs
- Tipping off customers about SAR filings, including indirectly by citing "compliance concerns" as the reason for account closure or transaction rejection
- Relying solely on automated OFAC screening without manual review of potential matches — fuzzy matching algorithms require human judgment to resolve
- Failing to screen existing customers when OFAC updates its SDN list — screening must be ongoing, not limited to account opening
- Applying a one-size-fits-all approach to customer risk rating instead of a risk-based methodology that accounts for customer type, geography, products, and transaction patterns
- Inadequate SAR narratives that describe what happened but fail to explain why the activity is suspicious or lacks a lawful purpose
- Treating the AML program as a static document rather than updating it as the firm's business, customer base, and risk profile evolve
- Assuming investment advisers have no AML obligations — the 2024 FinCEN final rule will require covered advisers to implement full BSA/AML programs effective January 1, 2026
- Failing to coordinate AML monitoring across affiliated entities (e.g., a broker-dealer and investment adviser under common ownership), creating gaps in detection
- Neglecting to document the independent testing (audit) findings and the firm's remediation of identified deficiencies
- Not retaining SAR and CTR supporting documentation for the full 5-year period required under BSA regulations

## Cross-References
- **know-your-customer** (Layer 9) — CIP and CDD are prerequisite inputs to AML monitoring; customer identification and verification feed directly into risk rating and transaction monitoring
- **sales-practices** (Layer 9) — Supervisory systems for detecting unsuitable activity overlap with AML surveillance for detecting suspicious transaction patterns
- **client-disclosures** (Layer 9) — AML program disclosures at account opening and the interplay between SAR confidentiality and client communication obligations
