---
name: know-your-customer
description: "Guide the implementation of customer identification, due diligence, and ongoing monitoring under FINRA Rule 2090, CIP, and the FinCEN CDD Rule. Use when the user asks about customer onboarding identity verification, beneficial ownership collection for entity accounts, enhanced due diligence for PEPs or high-risk customers, customer risk rating systems, KYC refresh triggers, or documentary vs non-documentary verification. Also trigger when users mention 'account opening requirements', 'who is the beneficial owner', 'new client identity check', 'how often to update KYC', 'essential facts for the account', 'foreign customer onboarding', or ask what information must be gathered before opening an account."
---

# Know Your Customer

## Purpose
Guide the implementation of customer identification, due diligence, and ongoing monitoring requirements under federal and FINRA rules. This skill covers CIP, CDD, beneficial ownership, enhanced due diligence, and profile maintenance — enabling a user or agent to design compliant onboarding and customer monitoring processes.

## Layer
9 — Compliance & Regulatory Guidance

## Direction
prospective

## When to Use
- Designing customer onboarding or account opening workflows
- Implementing Customer Identification Programs (CIP)
- Collecting beneficial ownership information for legal entity accounts
- Determining when enhanced due diligence (EDD) is required
- Building customer risk rating and profiling systems
- Establishing triggers for KYC refresh and ongoing monitoring
- Understanding what "essential facts" must be gathered under FINRA Rule 2090
- Evaluating documentary vs non-documentary identity verification methods
- Designing systems that feed KYC data into suitability and AML processes

## Core Concepts

### FINRA Rule 2090 — Know Your Customer
Every FINRA member must use reasonable diligence, with regard to the opening and maintenance of every account, to know and retain the essential facts concerning every customer and concerning the authority of each person acting on behalf of the customer. "Essential facts" are those required to: (a) effectively service the account, (b) act in accordance with any special handling instructions, (c) understand the authority of each person acting on behalf of the customer, and (d) comply with applicable laws, regulations, and rules.

### Customer Identification Program (CIP)
Required under USA PATRIOT Act Section 326 and implementing regulations (31 CFR 1020.220 for banks; similar requirements apply to broker-dealers under SEC Rule 17a-8 and FINRA rules). The CIP must include:

- **Identity verification** for each customer opening an account: name, date of birth (for individuals), address, and identification number (SSN for US persons; passport number/country or other government ID for non-US persons)
- **Verification procedures** using documentary methods (government-issued ID), non-documentary methods (credit bureau checks, public database searches, financial statement review), or a combination
- **Recordkeeping** — retain identifying information and verification methods for 5 years after account closure
- **Comparison with government lists** — check customer names against OFAC and other government terrorist/sanctions lists
- **Customer notice** — inform customers that information is being collected to verify identity

### Customer Due Diligence (CDD) Rule
FinCEN's CDD Rule (31 CFR 1010.230, effective May 2018) requires covered financial institutions to:

1. **Identify and verify the identity of customers** (overlaps with CIP)
2. **Identify and verify the identity of beneficial owners of legal entity customers** — any individual who owns 25% or more of the equity interests, plus one individual with significant responsibility for managing the entity (a control person)
3. **Understand the nature and purpose of customer relationships** to develop a customer risk profile
4. **Conduct ongoing monitoring** to identify suspicious transactions and, on a risk basis, maintain and update customer information

The 25% beneficial ownership threshold applies to legal entities (corporations, LLCs, partnerships). Certain entities are exempt: publicly traded companies, regulated financial institutions, government entities, and others listed in the rule.

### Enhanced Due Diligence (EDD)
Higher-risk customers require additional scrutiny beyond standard CDD:

- **Politically Exposed Persons (PEPs)** — senior foreign political figures and their families/associates. No US regulatory definition mandates PEP screening for domestic customers, but FinCEN guidance and FATF standards expect it for foreign PEPs. Firms should understand the source of wealth and funds.
- **Foreign correspondent accounts** — BSA Section 312 requires EDD for correspondent accounts maintained for foreign financial institutions, with heightened requirements for institutions in jurisdictions of concern
- **High-risk jurisdictions** — countries identified by FATF, FinCEN advisories, or firm risk assessments as presenting elevated ML/TF risk
- **Complex ownership structures** — multi-layered entities, trusts with opaque beneficiary structures, nominee arrangements
- **Unusual account activity** — customers whose transaction patterns deviate significantly from expected activity based on their profile

EDD measures include: senior management approval for account opening, source of wealth/funds verification, more frequent account reviews, enhanced transaction monitoring, and ongoing negative media screening.

### Documentary vs Non-Documentary Verification
**Documentary methods:** Unexpired government-issued photo ID (driver's license, passport, state ID), documents showing formation of a legal entity (articles of incorporation, partnership agreement, trust instrument).

**Non-documentary methods:** Credit bureau inquiries, public database verification (Lexis-Nexis, etc.), financial statement verification, references from other financial institutions. Required as a backup when documentary verification is unavailable, inconclusive, or the customer is not physically present (e.g., online account opening).

Firms must use non-documentary methods in at least the following situations: (1) the customer opens an account without appearing in person, (2) the firm is not familiar with the documents presented, (3) other circumstances that increase risk.

### Ongoing Monitoring and Profile Updates
KYC is not a one-time event. Customer profiles must be updated when:

- **Material life events** occur (retirement, marriage/divorce, inheritance, job loss, significant health changes)
- **Account review triggers** fire (periodic reviews, risk-based reviews, transaction-triggered reviews)
- **Transaction patterns** deviate significantly from the established profile
- **The customer provides new information** that changes their investment profile
- **Regulatory changes** require additional information (e.g., new beneficial ownership requirements)

FINRA does not mandate a specific refresh cycle, but firms typically establish risk-based review schedules (e.g., annual review for high-risk accounts, every 3 years for standard risk).

### SEC Requirements for Investment Advisers
Investment advisers have a fiduciary duty to understand their clients, which creates KYC-like obligations independent of FINRA rules. Form ADV Part 2A describes the adviser's services and client relationships. The SEC expects advisers to gather sufficient information to fulfill their fiduciary duty of care — including financial situation, investment objectives, risk tolerance, and any constraints. FinCEN's 2024 final rule (31 CFR Part 1032, effective January 1, 2026) extends BSA/AML requirements — including CIP and CDD — to SEC-registered investment advisers.

### Recordkeeping Requirements
- **CIP records:** Identifying information, verification documents/methods, and resolution of discrepancies must be retained for 5 years after account closure
- **CDD/beneficial ownership:** Copies of beneficial ownership certification forms and verification records retained for 5 years after account closure
- **Account records:** FINRA Rule 4512 requires maintenance of customer name, tax ID, address, date of birth, employment status, associated person relationship, trusted contact person, and other information specified in the rule
- **Reliance on other institutions:** Under Section 326 reliance provisions, a firm may rely on another financial institution's CIP if: (a) the relying firm's CIP incorporates this reliance, (b) the other institution is subject to an AML program rule, and (c) the other institution enters into a written contract for this purpose

## Worked Examples

### Example 1: Opening a trust account without identifying beneficial owners
**Scenario:** A wealth management firm opens a revocable living trust account for a family trust. The account opening team collects the trust agreement and identifies the grantor/trustee but does not collect beneficial ownership information on the trust beneficiaries. The trust holds $2M in investable assets.
**Compliance Issues:** Potential CDD Rule violation. While revocable living trusts are generally exempt from the beneficial ownership requirement (since the grantor maintains control), irrevocable trusts and other legal entity structures require beneficial ownership identification. The team must correctly classify the trust type. Additionally, FINRA Rule 4512 requires identification of all persons authorized to transact in the account.
**Analysis:** The firm should have a clear trust classification workflow that determines: (1) whether beneficial ownership requirements apply based on the trust type, (2) who has authority to act on the account, and (3) what documentation is required. For revocable trusts, identifying the grantor/trustee as the beneficial owner and control person is typically sufficient, but the firm should verify the trust is truly revocable and document the determination. The trust agreement must be reviewed — not just collected.

### Example 2: Failing to update KYC after a client retires
**Scenario:** A long-standing client retires at age 65 after 20 years at the firm. Her account profile still lists her investment objective as "aggressive growth," risk tolerance as "high," and annual income at $250,000. Post-retirement, her income drops to $80,000 (Social Security and pension) and she begins taking regular distributions from the account. No profile update is triggered.
**Compliance Issues:** Stale KYC data leading to potential suitability violations. The client's investment profile has materially changed — time horizon has shifted, income has declined, liquidity needs have increased (regular distributions), and risk capacity has decreased. Continued aggressive growth recommendations based on outdated profile data would likely violate suitability obligations.
**Analysis:** The firm should have systems that flag material life events (age milestones, distribution patterns, income changes) as triggers for KYC refresh. A representative who knows a client has retired but does not update the profile is failing the "reasonable diligence" standard of Rule 2090. Best practice: establish automated triggers (client turns 65, regular withdrawals begin, account balance drops significantly) and require profile confirmation at each periodic review.

### Example 3: Onboarding a high-risk foreign entity
**Scenario:** A broker-dealer receives an account application from a newly formed LLC registered in Delaware with a single listed owner who is a citizen of a jurisdiction flagged in a FinCEN advisory. The stated purpose is "general investing." The LLC provides articles of organization but limited information about the source of funds.
**Compliance Issues:** Multiple red flags requiring enhanced due diligence: newly formed entity, high-risk jurisdiction connection, limited transparency on source of funds, Delaware LLC (common in layering structures). Standard CDD is insufficient.
**Analysis:** The firm must: (1) complete standard CDD including beneficial ownership (25% owners and one control person), (2) escalate to enhanced due diligence given the risk factors, (3) verify source of funds and source of wealth, (4) conduct OFAC screening on all identified individuals, (5) obtain senior management approval before opening, (6) establish enhanced ongoing monitoring. The firm should also consider whether the limited information provided is itself a red flag warranting a SAR filing or account refusal. Simply accepting "general investing" as a purpose statement for a high-risk entity is insufficient.

## Common Pitfalls
- Treating KYC as a one-time account-opening exercise rather than an ongoing obligation
- Collecting but not verifying beneficial ownership information — the CDD Rule requires both identification and verification
- Applying the same due diligence to all customers regardless of risk — risk-based approach is required
- Not documenting when a customer declines to provide information and failing to narrow the recommendation universe accordingly
- Relying solely on documentary verification for online/remote account opening without implementing non-documentary backup methods
- Failing to establish automated triggers for profile refresh (life events, transaction anomalies, age milestones)
- Not screening beneficial owners and control persons against OFAC and other sanctions lists
- Confusing the CDD Rule's beneficial ownership requirements with FINRA Rule 4512's account record requirements — they overlap but are distinct
- Incomplete trust classification leading to incorrect application of beneficial ownership requirements
- Not training frontline staff to recognize when a customer's circumstances have changed, triggering a profile update obligation

## Cross-References
- **anti-money-laundering** (Layer 9): KYC/CDD data feeds directly into AML monitoring and suspicious activity detection
- **investment-suitability** (Layer 9): Customer profile gathered through KYC is the foundation for suitability analysis
- **reg-bi** (Layer 9): Reg BI's Care Obligation requires understanding the customer's investment profile — sourced from KYC
- **investment-policy** (Layer 5): IPS constraints (time horizon, risk tolerance, liquidity) derive from KYC profiling
