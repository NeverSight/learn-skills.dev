---
name: books-and-records
description: "Guide the design and maintenance of recordkeeping programs under SEC Rules 17a-3, 17a-4, and 204-2. Use when the user asks about document retention schedules, how long to keep trade records or customer complaints, WORM storage requirements, email or text message archiving, social media capture, BYOD compliance policies, or electronic storage audit trails. Also trigger when users mention 'we got an exam request for records', 'migrating to a new archiving vendor', 'blotter retention', 'order ticket requirements', 'off-channel communications', 'WhatsApp archiving', or ask how long specific records must be kept."
---

# Books and Records

## Purpose
Guide the design, implementation, and maintenance of recordkeeping programs for broker-dealers and investment advisers under federal securities laws. This skill covers the creation, retention, and storage of required records under SEC Rules 17a-3, 17a-4, and 204-2, FINRA recordkeeping obligations, electronic storage standards including WORM (Write Once, Read Many) requirements, and the archiving of electronic communications and social media. It enables users to build compliant document retention systems and respond to regulatory examinations of books and records.

## Layer
9 — Compliance & Regulatory Guidance

## Direction
prospective

## When to Use
- Designing a document retention policy or schedule for a broker-dealer or investment adviser
- Determining what records must be created under SEC Rule 17a-3
- Determining how long specific records must be retained under SEC Rule 17a-4
- Establishing recordkeeping systems for an investment adviser under Rule 204-2
- Evaluating electronic storage solutions for compliance with WORM or audit trail requirements
- Implementing email, instant messaging, or text message archiving systems
- Addressing social media archiving and supervision challenges
- Responding to an SEC or FINRA examination request for books and records
- Assessing gaps in a firm's recordkeeping practices after a systems migration or platform change
- Designing BYOD (Bring Your Own Device) policies that satisfy communications archiving obligations
- Evaluating third-party archiving vendors for regulatory compliance
- Remediating recordkeeping deficiencies identified in an examination or internal review

## Core Concepts

### SEC Rule 17a-3 (Records to be Made)
SEC Rule 17a-3 (17 CFR 240.17a-3) specifies the books and records that every registered broker-dealer must create and maintain. These records form the foundation of regulatory oversight, enabling examiners to reconstruct transactions, verify compliance, and protect investors. The principal categories of required records are:

- **Blotters (daily records):** Purchase and sale blotters recording every securities transaction (date, time, security, quantity, price, counterparty), cash receipts and disbursements blotters recording all cash flows, and securities received and delivered blotters tracking the movement of securities into and out of the firm.
- **General ledger:** A complete general ledger reflecting all assets, liabilities, income, expense, and capital accounts of the broker-dealer. Must be current and maintained in accordance with generally accepted accounting principles.
- **Customer account records:** For each customer account, the firm must create and maintain records containing: customer name and tax identification number (SSN or EIN), address, telephone number, date of birth, employment status and name of employer, whether the customer is an associated person of another broker-dealer, investment objectives, annual income and net worth, and the names of persons authorized to transact on the account. The 2003 amendments to Rule 17a-3 (Exchange Act Release No. 34-47910) expanded customer account record requirements to include customer investment profile information — specifically, investment objectives (e.g., capital preservation, income, growth, speculation), investment time horizon, risk tolerance, and other information the firm uses in making recommendations. Firms must also record the date the account was opened and the name of the associated person responsible for the account.
- **Order tickets:** A memorandum of each order received for the purchase or sale of securities, showing the terms of the order, the time of entry, the time of execution, the price, and the identity of the associated person who accepted and executed the order. For discretionary orders, the ticket must identify that discretion was exercised.
- **Confirmations:** Copies of all trade confirmations sent to customers and received from counterparties pursuant to SEC Rule 10b-10.
- **Memoranda of proprietary orders:** Records of each purchase and sale of securities for the firm's proprietary accounts, including the identity of the person who authorized the transaction.
- **Customer complaints:** A record of each written customer complaint received by the firm, including the complainant's name, the date the complaint was received, the subject matter, and the firm's response or disposition. FINRA Rule 4513 supplements this requirement with specific complaint recordkeeping standards.
- **Associated person employment applications:** Records related to associated persons including Form U4 (Uniform Application for Securities Industry Registration), employment history, disciplinary history, and background investigation results. These records must include the associated person's name, date of birth, address, and the starting date of employment or association with the firm.

### SEC Rule 17a-4 (Records to be Preserved)
SEC Rule 17a-4 (17 CFR 240.17a-4) prescribes the retention periods for broker-dealer records. Records are categorized into three tiers based on their required retention period:

**Six-year records (Rule 17a-4(a) and (b)):**
- Blotters (purchase and sale, cash receipts and disbursements, securities received and delivered)
- General ledgers and subsidiary ledgers
- Customer account records (including account statements)
- Partnership articles, if the broker-dealer is a partnership, and all amendments thereto
- Articles of incorporation or charter, if the broker-dealer is a corporation, including bylaws and amendments
- Financial statements (trial balances, computations of net capital, reserve formula calculations)
- Records of securities positions (stock record, securities record)

**Three-year records (Rule 17a-4(b) and (c)):**
- Communications — originals of all communications received by the broker-dealer and copies of all communications sent by the broker-dealer relating to its business as such, including inter-office memoranda. This encompasses letters, emails, instant messages, and other forms of business correspondence.
- Memoranda of brokerage orders and all other memoranda relating to the firm's business
- Written compliance and supervisory procedures (for the three most recent years)
- Employment applications and related documentation for associated persons — retained for three years after the individual terminates association with the firm
- Written agreements entered into by the broker-dealer (including customer agreements, clearing agreements, and employment contracts)
- Reports and questionnaires produced in connection with FINRA examinations and inspections

**Lifetime-of-enterprise records (Rule 17a-4(d)):**
- Articles of incorporation or organization, charter, minute books, and stock certificate books (or equivalent organizational documents for partnerships, LLCs, or other legal forms)
- These records must be preserved for the life of the enterprise and any successor enterprise

**First two years — easily accessible:** For all records subject to three-year or six-year retention, the records must be maintained in an easily accessible place during the first two years of the applicable retention period (Rule 17a-4(a), (b)). "Easily accessible" means the firm must be able to produce the records promptly upon regulatory request — they cannot be stored in a manner that requires extensive effort or delay to retrieve during this initial period.

**Electronic storage requirements (Rule 17a-4(f)):**
Rule 17a-4(f) governs the conditions under which broker-dealers may maintain required records in electronic format. Historically, this rule mandated that electronic records be preserved exclusively in non-rewriteable, non-erasable format — the WORM (Write Once, Read Many) standard. The 2022 SEC amendments to Rule 17a-4(f) (Exchange Act Release No. 34-96034, effective January 3, 2023) modernized these requirements by introducing an alternative to WORM storage. Under the amended rule, electronic records may now be maintained in either:

1. **WORM-compliant storage** — records preserved in a non-rewriteable, non-erasable format that ensures records cannot be altered or deleted; or
2. **Audit-trail alternative** — an electronic recordkeeping system that maintains an audit trail of all record modifications and deletions, creates a complete time-stamped record of changes, and preserves the original and all modified versions.

Regardless of which option is chosen, the following requirements apply:
- **Index system:** Records must be organized and indexed so that any individual record can be promptly accessed. The index must be stored separately from the records themselves and must be available for immediate production during regulatory examinations.
- **Auditable download capability:** The system must be capable of providing a legible, true, and complete copy of any record in the medium and format requested by the examiner.
- **Third-party access agent (Rule 17a-4(f)(3)(v) under the pre-2023 rule, now Rule 17a-4(f)(3)(vii)):** The broker-dealer must designate a third-party who has access to the electronic records if the broker-dealer ceases operations. The designated third party is sometimes called a "Designated Examining Authority access agent" or simply the "third-party access agent." The broker-dealer must file a notification with the SEC and its designated examining authority identifying the third party. The third party must file an annual undertaking (letter) with the SEC agreeing to provide access to the records. This requirement ensures continuity of regulatory access to records even if the firm fails.

### Rule 204-2 (Investment Adviser Recordkeeping)
SEC Rule 204-2 (17 CFR 275.204-2) under the Investment Advisers Act of 1940 specifies the books and records that SEC-registered investment advisers must make and keep. Investment adviser recordkeeping requirements differ from broker-dealer requirements in scope and emphasis, reflecting the advisory relationship and fiduciary obligations. Required records include:

- **Journals and ledgers:** A journal or journals (including cash receipts and disbursements records) and a general ledger (or other record) reflecting all assets, liabilities, reserves, capital, income, and expense accounts.
- **Memoranda of orders:** A memorandum of each order given by the investment adviser for the purchase or sale of any security, including the terms of the order, the person who recommended the transaction, the person who placed the order, the date, and the bank, broker-dealer, or other entity through which the order was executed.
- **Client records and powers of attorney:** All records showing the identity of each client, including name, address, and advisory agreement. All written powers of attorney and other evidence of authority granted by clients (including trading authorizations and limited powers of attorney).
- **Written communications (sent and received):** Originals of all written communications received by the adviser and copies of all written communications sent by the adviser relating to (i) any recommendation made or proposed to be made and any advice given or proposed to be given, (ii) any receipt, disbursement, or delivery of funds or securities, or (iii) the placing or execution of any order for the purchase or sale of any security. This includes emails, letters, instant messages, and any other written or electronic business communication.
- **Advertising and performance records:** All written communications that are advertisements (including website content, social media posts, and marketing materials), records substantiating the calculation of performance shown in advertisements and promotional materials, and all supporting documentation for performance claims. Under the SEC Marketing Rule (Rule 206(4)-1, effective November 4, 2022), advisers must retain records of advertisements and all information necessary to demonstrate compliance with the marketing rule's requirements.
- **Political contribution records (pay-to-play):** Rule 204-2(a)(18) requires advisers to maintain records of all political contributions made by the adviser or any of its covered associates to officials of government entities, as required under Rule 206(4)-5 (the pay-to-play rule). Records must include the name and title of each contributor, the recipient's name and office, the amount and date of the contribution, and whether the contribution was returned.
- **Investment recommendations and supporting documentation:** Records of each investment recommendation made to a client, including the basis for the recommendation, the research or analysis supporting it, and any presentations or proposals provided. Advisers must also retain records of the allocation of investment opportunities among clients (including any trade allocation policies and documentation of how allocations were made in practice).
- **Code of ethics records:** The adviser's code of ethics, records of personal securities transactions of access persons, and records of any violations of the code and actions taken.

**Retention period:** Most records required under Rule 204-2 must be retained for five years from the end of the fiscal year during which the last entry was made or the record was created. During the first two years of the five-year period, records must be kept in an easily accessible place (i.e., the adviser's principal office or another readily accessible location).

**Custody-related records:** Investment advisers that have custody of client assets must maintain additional records per Rule 206(4)-2 (the custody rule), including records of all client funds and securities over which the adviser has custody, a journal showing all purchases, sales, receipts, and deliveries of securities and funds for such accounts, and copies of all account statements delivered to clients.

### FINRA Recordkeeping Requirements
FINRA member firms are subject to FINRA-specific recordkeeping obligations that supplement and reinforce the SEC requirements under Rules 17a-3 and 17a-4.

**FINRA Rule 4511 (General Requirements):** FINRA Rule 4511 requires each member firm to make and preserve books and records as required under the FINRA rules, the Securities Exchange Act of 1934, and the applicable SEC rules (i.e., Rules 17a-3 and 17a-4). Rule 4511 also requires that all books and records be maintained in a format and medium that comply with Rule 17a-4. This means FINRA firms must meet the electronic storage, index, and accessibility requirements of Rule 17a-4(f) for all records — including FINRA-specific records not explicitly addressed by the SEC rules.

**FINRA Rule 3110 (Supervision) — Recordkeeping Implications:** FINRA Rule 3110 generates significant recordkeeping obligations through its supervision requirements:
- **Written Supervisory Procedures (WSPs):** The firm's current WSPs and all prior versions within the retention period must be maintained.
- **Exception reports:** Output from automated surveillance and exception reporting systems, together with documentation of supervisory review and disposition of each flagged item, must be retained.
- **Branch office inspection reports:** Reports from annual inspections of OSJ (Office of Supervisory Jurisdiction) locations and periodic inspections of non-OSJ branch offices, including findings and remediation actions.
- **Complaint logs:** A log of all customer complaints received by the firm, cross-referenced to the underlying complaint records and the firm's response.
- **Supervisory review documentation:** Evidence that supervisory principals reviewed correspondence (including electronic communications), customer account activity, trade blotters, and exception reports. This documentation must show the reviewer's identity, the date of review, and any actions taken.
- **Annual compliance meeting records:** Documentation of the firm's annual compliance meeting required under FINRA Rule 3110(a)(7), including attendees and topics covered.

**FINRA Rule 4513 (Records of Written Customer Complaints):** Requires a separate file of all written customer complaints, indexed by complaint type and by associated person. The complaint record must include the complainant's name, date received, associated person identified, nature of the complaint, and disposition. These records are retained for at least four years.

### Electronic Communications Archiving
SEC and FINRA rules require broker-dealers and investment advisers to capture, retain, and supervise all business-related electronic communications. The regulatory framework does not distinguish between communication platforms — the obligation applies uniformly regardless of the technology used.

**Scope of covered communications:** The requirement extends to all written business communications, including email, instant messaging (Bloomberg chat, Reuters Eikon messaging, proprietary IM systems), text messages (SMS and messaging apps such as iMessage and WhatsApp), collaboration platforms (Microsoft Teams, Slack, Zoom chat), and any other electronic medium used to communicate about firm business.

**Key regulatory guidance:**
- **FINRA Regulatory Notice 07-59** — Addressed the supervision of electronic communications, emphasizing that firms must establish systems and procedures to review electronic communications for evidence of sales practice violations, customer complaints, and other compliance concerns. Firms were reminded that the supervision obligation does not depend on the communication technology used.
- **FINRA Regulatory Notice 10-06** — Provided guidance on the supervision of electronic communications, including risk-based approaches to review (keyword surveillance, statistical sampling, targeted reviews of high-risk persons or activities). Acknowledged that a 100% review of all communications is not required, but firms must demonstrate that their review methodology is reasonably designed to detect violations.
- **FINRA Regulatory Notice 11-39** — Addressed social media and digital communications, establishing the framework for distinguishing between static and interactive social media content and providing guidance on recordkeeping and supervision for social media.
- **FINRA Regulatory Notice 17-18** — Addressed emerging technologies and communications channels, reminding firms that the use of new platforms, apps, or messaging services does not alter the obligation to capture, retain, and supervise business communications.

**Retention requirements for electronic communications:** Electronic communications related to the broker-dealer's business are treated as "correspondence" under Rule 17a-4(b)(4) and must be retained for a minimum of three years (the first two years in an easily accessible place). For investment advisers, written communications are retained for five years under Rule 204-2(a)(7).

**Supervision requirements:** Beyond mere retention, firms must supervise the content of electronic communications. FINRA Rule 3110 requires that firms establish procedures to review correspondence and internal communications. The review methodology may include automated keyword or lexicon surveillance, statistical sampling, targeted reviews of high-risk registered representatives or activity patterns, and escalation procedures for flagged communications. Supervisory reviews must be documented, and the firm must retain evidence of the review process.

**BYOD (Bring Your Own Device) policies and challenges:** Firms that permit employees and registered representatives to use personal devices for business communications face heightened compliance challenges. BYOD policies must address: mandatory installation of archiving applications on personal devices, prohibition of non-approved communication channels for business communications, technical controls to capture communications from personal devices, procedures for device collection or data preservation when an employee departs, and employee attestations acknowledging the firm's right to monitor and archive business communications on personal devices.

### WORM Storage and Electronic Recordkeeping
Rule 17a-4(f) has historically been the most technically prescriptive provision in the books-and-records framework. Understanding the WORM standard and the 2022 amendments is essential for designing compliant electronic recordkeeping systems.

**WORM (Write Once, Read Many) standard:** Under the original Rule 17a-4(f), electronic records had to be stored on non-rewriteable, non-erasable media — the WORM standard. The purpose of this requirement was to prevent firms from altering or destroying records to conceal violations. WORM-compliant storage options have historically included optical disks (CD-R, DVD-R), magnetic tape with write-protect mechanisms, and purpose-built WORM storage appliances. Cloud-based WORM storage solutions (such as those offered by Amazon S3 Object Lock, Azure Immutable Blob Storage, and similar services) are now available and widely used, provided they meet the non-rewriteability and non-erasability requirements.

**Index and retrieval system:** Regardless of storage format, the firm must maintain an index of all records stored electronically. The index must be organized to permit prompt identification and retrieval of any individual record. The index itself must be stored on a medium separate from the records and must be duplicated for disaster recovery purposes.

**Audit trail:** Under the 2022 amendments (Exchange Act Release No. 34-96034), firms that elect the audit-trail alternative (rather than WORM) must maintain an electronic recordkeeping system that creates a time-stamped, tamper-evident audit trail of every modification, deletion, or alteration of any record. The audit trail must preserve the original record and all subsequent versions, and it must be possible to reconstruct the complete history of any record from creation through its current state.

**Third-party access agent:** The broker-dealer must file with its designated examining authority (DEA) and the SEC the name, address, telephone number, and facsimile number of the designated third party who will provide access to electronic records in the event the broker-dealer ceases operations. The designated third party must file with the SEC an annual undertaking agreeing to provide such access. This requirement was designed to address the risk that electronic records could become inaccessible if the firm failed and its technology infrastructure was dismantled. The third-party access agent requirement remains in effect under the 2022 amendments for firms using either WORM or audit-trail storage.

**Annual letter from the designated third party:** The designated third party must file annually with the SEC a written statement affirming its agreement to provide the required access. Failure to maintain a current designated third party and annual undertaking is itself a books-and-records violation.

**2022 SEC amendments (effective January 3, 2023):** The amendments to Rule 17a-4 were designed to modernize the rule by: (1) offering the audit-trail alternative to WORM, (2) eliminating the requirement that firms notify the SEC before using electronic storage (firms previously had to file a notice 90 days before beginning to store records electronically), (3) permitting the use of any electronic recordkeeping system that meets the requirements, without specifying particular technologies, and (4) streamlining certain notification requirements. These amendments were adopted in recognition that WORM technology, while effective, imposed significant operational costs and that modern audit-trail technologies could achieve equivalent regulatory objectives.

### Social Media Archiving
Social media presents unique recordkeeping challenges that have been the subject of extensive regulatory guidance. The core principle remains unchanged: business-related communications on social media platforms must be captured, retained, and supervised just like any other written business communication.

**Static vs. interactive content (FINRA Regulatory Notice 11-39):**
- **Static content** — Posts, profiles, or pages that are published and do not change based on audience interaction. Static social media content is treated as **advertising** under FINRA rules and must be pre-approved by a registered principal before posting. Examples include firm websites, LinkedIn company pages, pre-scripted social media posts, and published articles or blog posts. Static content must be retained and filed with FINRA if it meets the definition of a retail communication under FINRA Rule 2210.
- **Interactive content** — Real-time or near-real-time communications with individuals or groups. Interactive content is treated as **correspondence** (communications with 25 or fewer retail investors within a 30-day period) or **institutional communication** (communications exclusively with institutional investors), subject to the applicable supervision and recordkeeping requirements. Examples include direct messages, comment threads, replies to customer inquiries, and live social media interactions.

**Ephemeral content:** Features such as Instagram/Facebook Stories, Snapchat, and disappearing messages on platforms like Telegram and WhatsApp present heightened compliance risk. If a registered representative uses an ephemeral messaging feature for business communication, the firm must capture and retain that content. Most regulatory enforcement actions involving off-channel communications have cited the failure to capture ephemeral or disappearing messages.

**Personal device usage:** Registered representatives who use personal social media accounts or personal devices for business-related communications create archiving gaps if the firm does not have technology in place to capture those communications. Firms should maintain policies that either (a) prohibit the use of personal social media accounts and unapproved platforms for business communications, or (b) deploy technology solutions to capture communications from approved personal accounts.

**Third-party archiving vendors:** The regulatory requirements have given rise to a market of specialized archiving vendors (such as Smarsh, Global Relay, Proofpoint, and others) that provide capture, retention, supervision, and retrieval capabilities across multiple communication platforms. When selecting a vendor, firms should evaluate whether the vendor's solution captures content from all platforms the firm uses, meets WORM or audit-trail requirements under Rule 17a-4(f), provides lexicon-based surveillance capabilities for supervisory review, supports search and retrieval for examination requests, and maintains its own disaster recovery and business continuity capabilities.

**FINRA guidance on social media records:** FINRA has emphasized that firms must: (1) inventory all social media platforms used by the firm and its associated persons for business purposes, (2) establish written policies identifying approved and prohibited platforms, (3) deploy archiving technology for all approved platforms, (4) train associated persons on social media policies and the consequences of using unapproved platforms, and (5) conduct periodic attestations from associated persons confirming compliance with the firm's social media policies.

### Document Retention Schedule
The following table maps common document types to their required retention periods and source rules:

| Document Type | Retention Period | Source Rule |
|---|---|---|
| Blotters (purchase/sale, cash receipts/disbursements) | 6 years | Rule 17a-4(a) |
| General ledger and subsidiary ledgers | 6 years | Rule 17a-4(a) |
| Customer account records and statements | 6 years | Rule 17a-4(a), (b) |
| Securities positions (stock record) | 6 years | Rule 17a-4(a) |
| Financial statements and net capital computations | 6 years | Rule 17a-4(b)(8) |
| Partnership articles and amendments | 6 years | Rule 17a-4(b) |
| Communications (letters, emails, IMs, texts) — BD | 3 years | Rule 17a-4(b)(4) |
| Memoranda of brokerage orders | 3 years | Rule 17a-4(b)(1) |
| Written supervisory procedures | 3 years (current plus prior versions) | Rule 17a-4(b), FINRA Rule 3110 |
| Employment applications (associated persons) | 3 years after termination | Rule 17a-4(c) |
| Customer complaints | 4 years | FINRA Rule 4513 |
| Written agreements (customer, clearing, employment) | 3 years after termination or expiration | Rule 17a-4(b)(7) |
| Exception reports and supervisory review records | 3 years | FINRA Rule 3110 |
| Branch inspection reports | 3 years (per inspection cycle) | FINRA Rule 3110 |
| Articles of incorporation, bylaws, minute books | Life of enterprise | Rule 17a-4(d) |
| IA journals and ledgers | 5 years | Rule 204-2(a)(1)-(2) |
| IA written communications (sent and received) | 5 years | Rule 204-2(a)(7) |
| IA advertising and performance records | 5 years | Rule 204-2(a)(11), (16) |
| IA client records and advisory agreements | 5 years from end of advisory relationship | Rule 204-2(a)(3), (10) |
| IA investment recommendations and supporting docs | 5 years | Rule 204-2(a)(3), (8) |
| IA political contribution records (pay-to-play) | 5 years | Rule 204-2(a)(18) |
| IA code of ethics and personal trading records | 5 years | Rule 204-2(a)(12)-(13) |
| IA proxy voting records | 5 years | Rule 206(4)-6 |

For all broker-dealer records subject to three-year or six-year retention, the first two years must be maintained in an easily accessible place. For investment adviser records, the first two years of the five-year period must be maintained in an easily accessible place.

## Worked Examples

### Example 1: Gaps in email archiving after a systems migration
**Scenario:** A mid-size broker-dealer migrates from an on-premises email system to a cloud-based platform. The migration takes place over a two-week period. Six months later, during preparation for a routine FINRA examination, the compliance department discovers that emails sent and received during the migration window were not captured by the firm's archiving vendor. The gap affects approximately 3,500 emails across 120 registered representatives over the two-week period. The firm cannot determine the content of the missing emails.

**Compliance Issues:**
- Rule 17a-4(b)(4) requires broker-dealers to preserve originals of all business communications received and copies of all business communications sent for at least three years. The failure to capture and retain the migration-window emails is a direct violation of this rule.
- FINRA Rule 4511 independently requires the firm to make and preserve books and records as required under the Exchange Act and SEC rules. The gap constitutes a failure under this rule as well.
- FINRA Rule 3110 requires the firm to supervise communications. Emails that were never captured could not have been supervised, creating a supervision failure for the migration period.
- The firm cannot demonstrate to FINRA examiners that no violative communications occurred during the gap period, which shifts the burden to the firm to show that the deficiency did not result in customer harm.

**Analysis:**
The firm should take the following remediation steps: (1) Conduct a forensic analysis to determine the exact scope of the gap — which users were affected, the precise dates, and whether any emails can be recovered from backup systems, individual mailboxes, or the cloud platform's own logs. (2) Engage the archiving vendor and the cloud platform provider to determine whether any copies of the missing emails exist in alternative storage. (3) Document the root cause of the gap — was it a failure in the migration plan, a vendor configuration error, or a lack of testing before cutover. (4) Self-report the deficiency to FINRA if the gap is material. FINRA considers self-reporting a mitigating factor in enforcement proceedings. (5) Implement preventive controls for future migrations, including parallel archiving during transition periods (running both old and new systems simultaneously), pre-migration testing of archiving capture, and post-migration validation audits. (6) Review the firm's vendor management procedures — the archiving vendor should have been involved in migration planning and should have validated capture continuity. The regulatory exposure depends on the scope of the gap and whether any of the missing communications related to customer complaints, order instructions, or other high-risk content. FINRA has brought enforcement actions for email archiving failures, with fines ranging from $10,000 to over $1 million depending on the scope and duration of the deficiency and the firm's remediation efforts.

### Example 2: Investment adviser with no recordkeeping system for investment recommendations
**Scenario:** An SEC-registered investment adviser has been operating for five years, managing $400 million in assets across 200 client accounts. The firm has maintained basic financial records (journals and ledgers) and client agreements, but has never established a systematic recordkeeping process for investment recommendations. Investment recommendations are made verbally in client meetings and documented informally in advisors' personal notes, personal email accounts, and handwritten notebooks. The firm has no centralized repository for investment recommendations, no records of the research or analysis supporting recommendations, and no documentation of how investment opportunities were allocated among clients. The deficiency is discovered when the firm receives an SEC examination notification.

**Compliance Issues:**
- Rule 204-2(a)(3) requires investment advisers to retain a memorandum of each order given for the purchase or sale of any security, including the terms of the order and the person who recommended the transaction. The firm's failure to maintain these records is a direct violation.
- Rule 204-2(a)(7) requires advisers to retain all written communications relating to recommendations made or proposed to be made and advice given or proposed to be given. Advisors' personal email accounts containing recommendation-related communications are not under the firm's control, creating both a retention and a supervision failure.
- Rule 204-2(a)(8) requires advisers to keep a record of every transaction in which the adviser or any advisory representative has a direct or indirect interest. If advisors recommended securities in which the firm or its access persons held positions, those records should have been maintained under the code of ethics and personal trading requirements.
- The absence of trade allocation records creates exposure under the adviser's fiduciary duty — without documentation of how investment opportunities were allocated, the SEC cannot verify that the firm treated clients fairly and did not favor certain accounts over others.
- Five years of missing records cannot be recreated. The deficiency spans the firm's entire operating history.

**Analysis:**
The firm faces a serious examination outcome. The remediation plan should include: (1) Immediately implement a centralized recordkeeping system for investment recommendations — this may include a CRM or portfolio management system that captures the recommendation, the date, the supporting rationale, the adviser who made it, and the client accounts that received it. (2) Collect and centralize whatever informal records exist — personal notes, emails, presentation materials — and incorporate them into the firm's official books and records going forward. Advisors should be directed to forward any business-related emails from personal accounts to the firm's archive. (3) Implement a written trade allocation policy and begin documenting how investment opportunities are allocated among clients. (4) Engage outside compliance counsel to prepare for the SEC examination. The firm should be prepared to explain the deficiency, present its remediation plan, and demonstrate that the new system satisfies Rule 204-2. (5) Consider whether a deficiency letter or self-disclosure to the SEC is appropriate before the examination begins. (6) Train all advisory personnel on recordkeeping obligations and implement attestation procedures. The SEC's examination staff will likely issue a deficiency letter at minimum. If the lack of records conceals substantive violations (unfair allocation, conflicted recommendations), the matter could escalate to an enforcement referral. The firm's prompt and comprehensive remediation will be a mitigating factor.

### Example 3: Off-channel text messaging by registered representatives
**Scenario:** A broker-dealer's compliance department learns that several registered representatives have been communicating with clients via personal cell phone text messages (iMessage and WhatsApp) for the past two years. The firm's policies prohibit the use of personal devices and unapproved platforms for business communications, but the prohibition has not been enforced. The firm has no archiving solution for text messages sent from personal devices. An estimated 15 registered representatives have exchanged thousands of text messages with clients discussing investment recommendations, trade instructions, account transfers, and complaints. The firm discovers the issue when a customer arbitration claimant produces text messages that the firm has no record of.

**Compliance Issues:**
- Rule 17a-4(b)(4) requires the firm to retain all business-related communications. Text messages containing investment recommendations, trade instructions, or customer complaints are business records subject to retention. The firm has failed to retain these communications for two years.
- FINRA Rule 3110 requires the firm to supervise communications. Text messages that were never captured cannot have been supervised. This constitutes a supervision failure.
- FINRA Rule 4511 requires the firm to make and preserve books and records as required by the SEC rules and FINRA rules. The firm has failed this obligation with respect to text messages.
- SEC Rule 17a-3(a)(17) requires records of customer complaints. If any of the text messages contained complaints, the firm has failed to record them.
- The firm's written supervisory procedures prohibited the use of personal devices, but the firm failed to enforce the prohibition, rendering the policy ineffective and compounding the supervisory failure.

**Analysis:**
This scenario reflects a pattern that has been the subject of major SEC and FINRA enforcement actions in recent years. Beginning in 2021, the SEC and FINRA initiated a series of sweeping investigations into off-channel communications at broker-dealers and investment advisers. These investigations resulted in billions of dollars in aggregate penalties across the industry. The SEC imposed fines of $125 million on individual firms, with total industry penalties exceeding $2 billion by 2024. FINRA has brought parallel actions with fines ranging from hundreds of thousands to tens of millions of dollars. The firm should take the following steps: (1) Immediately deploy a text message archiving solution for all registered representatives. Solutions include firm-issued devices with built-in archiving, mobile archiving applications installed on personal devices (with employee consent), or enterprise mobility management platforms that capture text messages from approved applications. (2) Collect and preserve all available text messages from the affected registered representatives' personal devices. This may require cooperation from the representatives and potentially forensic data collection. (3) Conduct a review of the collected text messages to identify any customer complaints, trade instructions, or other records that should have been maintained under Rules 17a-3 and 17a-4. (4) Self-report the deficiency to FINRA and the SEC. Given the current enforcement environment, self-reporting is strongly advisable — regulators have imposed significantly higher penalties on firms that failed to self-report or that were discovered through examination rather than voluntary disclosure. (5) Strengthen the firm's policies to include: a clear prohibition on unapproved communication channels, mandatory use of the firm's archiving solution for all business communications, annual (or more frequent) attestations from registered representatives confirming compliance, technical controls where feasible (e.g., monitoring for unapproved application usage on firm-issued devices), and disciplinary consequences for violations. (6) Retrain all registered representatives on the firm's communications policies, the regulatory basis for the requirements, and the personal liability exposure for off-channel communications. The regulatory exposure is significant. In the current enforcement climate, the SEC and FINRA have treated off-channel communications failures as serious violations warranting substantial monetary penalties, undertakings to engage independent compliance consultants, and requirements to implement enhanced supervisory systems.

## Common Pitfalls
- Treating document retention as a one-time project rather than an ongoing program that requires monitoring, testing, and updating as platforms and regulations change
- Failing to distinguish between the different retention periods for different record types — applying a uniform three-year or six-year period when specific records have shorter, longer, or lifetime retention requirements
- Maintaining records for the required period but not in an "easily accessible place" during the first two years, resulting in inability to produce records promptly during an examination
- Assuming that cloud-based storage is automatically WORM-compliant — cloud storage must be configured with immutability settings (e.g., S3 Object Lock in compliance mode) to meet WORM requirements
- Failing to designate or maintain a current third-party access agent as required by Rule 17a-4(f), or failing to ensure the third party files its annual undertaking with the SEC
- Relying on written policies prohibiting unapproved communication channels without deploying technical controls or enforcement mechanisms — an unenforced policy is not an effective supervisory system
- Assuming that investment adviser recordkeeping obligations are less rigorous than broker-dealer obligations — Rule 204-2 requires comprehensive records of recommendations, communications, and supporting documentation
- Failing to capture and archive communications on collaboration platforms (Teams, Slack) even when those platforms are approved for business use
- Not maintaining a separate index of electronically stored records, or maintaining the index on the same medium as the records themselves
- Destroying records at the expiration of the minimum retention period without considering ongoing litigation holds, regulatory investigations, or customer arbitration matters that may require extended retention
- Confusing FINRA complaint retention requirements (4 years under Rule 4513) with the general SEC communications retention period (3 years under Rule 17a-4)
- Failing to update the document retention schedule after regulatory amendments — for example, the 2022 amendments to Rule 17a-4 changed certain requirements that may affect the firm's storage architecture and vendor relationships

## Cross-References
- **client-disclosures** (Layer 9): Records of disclosure document delivery (Form ADV, Form CRS, prospectuses, privacy notices) are themselves books and records subject to retention requirements under Rules 17a-4 and 204-2
- **sales-practices** (Layer 9): Supervisory records required under FINRA Rule 3110 — including exception reports, branch inspection reports, and written supervisory procedures — are a major component of books and records obligations
- **anti-money-laundering** (Layer 9): BSA/AML recordkeeping (SARs, CTRs, CIP documentation) feeds directly into the books-and-records framework and is subject to its own retention requirements that run parallel to Rules 17a-4 and 204-2
- **advertising-compliance** (Layer 9): Advertising materials and performance records are subject to retention requirements under Rule 17a-4 for broker-dealers and Rule 204-2(a)(11) for investment advisers
- **conflicts-of-interest** (Layer 9): Code of ethics records, personal trading reports, and conflict disclosure documentation are books and records that must be retained under both the BD and IA frameworks
- **know-your-customer** (Layer 9): CIP and CDD records collected during account opening are retained under Rule 17a-4 as customer account records and under BSA regulations for a minimum of five years after account closure
