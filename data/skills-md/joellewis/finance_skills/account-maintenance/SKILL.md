---
name: account-maintenance
description: "Process account maintenance requests across the full account lifecycle. Use when changing a client address or contact info and verifying identity, updating beneficiary designations after marriage divorce birth or death, re-registering or re-titling an account to a trust or new entity, selecting tax lot accounting methods or fixing cost basis records, applying legal holds compliance holds or Reg T freezes, setting up systematic withdrawals automatic investments or dividend reinvestment, processing a death notification or estate account setup, handling a QDRO or divorce decree for retirement accounts, responding to power of attorney or guardianship situations, closing accounts and managing escheatment, or designing periodic account review and data quality programs."
---

# Account Maintenance

## Purpose
Guide the operations of ongoing account maintenance in brokerage and advisory firms. Covers address and contact changes, beneficiary updates, account re-registration and re-titling, cost basis management, account restrictions and holds, standing instructions, and lifecycle events (marriage, divorce, death, incapacity). Enables designing and operating efficient account maintenance processes that satisfy regulatory requirements while minimizing operational risk.

## Layer
12 — Client Operations (Account Lifecycle & Servicing)

## Direction
both

## When to Use
- Processing a client address or contact information change and determining identity re-verification requirements
- Updating primary or contingent beneficiary designations after a life event
- Re-registering or re-titling an account (individual to trust, name change, entity restructuring)
- Selecting or changing tax lot accounting methods and managing cost basis records
- Applying or removing account restrictions (legal hold, compliance hold, Reg T freeze, death notification)
- Setting up or modifying standing instructions (systematic withdrawals, automatic investments, dividend reinvestment, standing wire/ACH)
- Processing a death notification, including account freeze, beneficiary claim, and estate account setup
- Handling divorce decree processing, including QDRO for retirement accounts and account division
- Responding to incapacity situations involving power of attorney or guardianship/conservatorship
- Closing accounts voluntarily or involuntarily and managing asset disposition, final billing, and escheatment
- Designing periodic account maintenance review processes and data quality programs
- Evaluating operational risk in account servicing workflows

## Core Concepts

### Contact Information Changes
Address and contact updates are among the most frequent account maintenance requests, but they carry meaningful fraud and elder abuse risk. Firms must balance client convenience with protective controls.

**Address change procedures:**
- **Client-initiated changes** may be submitted through the advisor, client portal, phone, or written request. Regardless of channel, the firm must verify the identity of the requesting party before processing the change. Common verification methods include knowledge-based authentication, callback to the phone number on file, or confirmation sent to the prior address or email.
- **Advisor-initiated changes** on behalf of a client should require documented client authorization. Verbal authorization must be noted with date, time, and the identity of the person providing authorization. Written or electronic authorization is preferred and creates a stronger audit trail.
- **Multi-system propagation** is a persistent operational challenge. When an address changes, the update must flow to all systems that store client contact data: CRM, custodian account master, correspondence system, billing system, and any third-party platforms. Failure to propagate consistently results in mail going to old addresses (privacy risk), incorrect tax form delivery (1099s, K-1s), and compliance exposure. Best practice is to designate a single system of record (typically CRM or custodian) and propagate changes outward via integration, rather than requiring manual updates in each system.
- **Temporary vs permanent changes** should be distinguished in the workflow. A client who is traveling or has a seasonal residence may need mail temporarily redirected without changing the legal address of record. The system should support a temporary address with an expiration date that reverts to the permanent address automatically.

**Third-party address change red flags:**
FINRA Regulatory Notice 07-43 and SEC guidance on senior investor protection highlight address changes as a key indicator of potential financial exploitation. Red flags that should trigger enhanced scrutiny include:
- Address change request from someone other than the account holder (especially if followed by a distribution request)
- Change to a P.O. Box when the prior address was a residential address
- Change to an address associated with a known bad actor or previously flagged account
- Multiple address changes in a short period
- Address change for a senior investor (age 65+) followed within 30 days by a large withdrawal or wire transfer
- Address change to a different state or country for a client with no known connection to that location

When a red flag is detected, the firm should place a temporary hold on the address change, contact the client at the prior contact information to confirm the request, and escalate to compliance or a designated senior investor protection contact if confirmation cannot be obtained.

**Notification requirements:**
Many custodians and regulatory expectations require that a confirmation of the address change be sent to both the old and new addresses. This dual notification provides the client an opportunity to detect an unauthorized change. The confirmation should include the date of the change, the new address, and instructions for contacting the firm if the change was not authorized.

### Beneficiary Management
Beneficiary designations determine the disposition of assets upon the account holder's death. Errors or omissions in beneficiary management are among the most consequential account maintenance failures because they are typically discovered only at death, when correction is impossible.

**Designation structure:**
- **Primary beneficiaries** receive assets first. Multiple primary beneficiaries share the assets according to specified percentages (must total 100%).
- **Contingent beneficiaries** receive assets only if all primary beneficiaries predecease the account holder or disclaim.
- **Per stirpes** means that if a beneficiary predeceases the account holder, that beneficiary's share passes to their descendants in equal shares by representation. Per stirpes is the more common election for family designations.
- **Per capita** means that if a beneficiary predeceases the account holder, that beneficiary's share is redistributed equally among the surviving beneficiaries. The predeceased beneficiary's descendants do not inherit.

**Beneficiary updates for life events:**
- **Marriage:** The client may want to add a spouse as primary beneficiary. For ERISA-governed retirement plans, the spouse is the default beneficiary unless the spouse provides written consent to a different designation. For IRAs and non-ERISA accounts, there is no automatic spousal beneficiary right, but advisors should prompt a review.
- **Divorce:** Beneficiary designations naming a former spouse are not automatically revoked by divorce in most states for non-ERISA accounts (the law varies by state and account type). The client must affirmatively update the designation. Failure to update after divorce is one of the most common and costly beneficiary errors. For ERISA plans, a QDRO may assign benefits to a former spouse regardless of the current designation.
- **Birth or adoption:** Clients should add new children as beneficiaries or adjust percentages. Per stirpes designations may automatically include new descendants, but per capita designations do not.
- **Death of a beneficiary:** If a primary beneficiary dies, the firm should notify the account holder and recommend updating the designation. If the deceased beneficiary's share is governed by per stirpes language, the share passes to their descendants; if per capita, the share redistributes to surviving beneficiaries.

**Retirement account beneficiary rules (SECURE Act):**
The SECURE Act of 2019 (and SECURE 2.0 Act of 2022) fundamentally changed inherited retirement account distribution rules:
- **Spouse beneficiaries** may roll the inherited account into their own IRA, treat it as their own, or take distributions over their life expectancy — the most flexible options.
- **Eligible designated beneficiaries** (minor children of the account holder, disabled or chronically ill individuals, individuals not more than 10 years younger than the deceased) may use the life expectancy method.
- **All other designated beneficiaries** (including adult children and non-spouse partners) must distribute the entire inherited account within 10 years of the account holder's death. There is no annual RMD requirement during the 10-year period if the account holder died before their required beginning date; if the account holder died after their required beginning date, annual distributions may be required within the 10-year window.
- **Non-designated beneficiaries** (estates, certain trusts, charities) follow either the 5-year rule or the deceased's remaining life expectancy, depending on whether the account holder died before or after the required beginning date.

These rules make beneficiary designation a critical planning decision. The choice between naming individuals, trusts, or other entities as beneficiaries has significant tax implications that should be coordinated with the tax-efficiency and financial-planning-integration skills.

**TOD/POD designations:**
Transfer on Death (TOD) for brokerage accounts and Payable on Death (POD) for bank accounts allow assets to pass to named beneficiaries outside of probate. TOD registrations are governed by the Uniform TOD Security Registration Act, adopted in most states. The designation overrides the will, so coordination with estate planning is essential. The firm should document the TOD beneficiary designation on the custodian's designated form and retain a copy.

**Beneficiary review cadence:**
Best practice is to review beneficiary designations at every major life event and at minimum during the annual or biennial client review meeting. The firm should maintain a process to flag accounts with outdated or missing beneficiary designations — for example, accounts with no beneficiary on file, accounts where the designated beneficiary has a flagged death record, or accounts that have not had a beneficiary review in more than 3 years.

### Account Re-Registration and Re-Titling
Re-registration changes the legal ownership or titling of an account. This is operationally more complex than a simple data update because it affects the legal rights to the account assets, may trigger tax consequences, and typically requires custodian processing with supporting documentation.

**Common re-registration events:**
- **Individual to revocable trust:** The most frequent re-registration. Assets move from the individual's name into the trust's name. Because a revocable trust is a grantor trust (the individual retains control), this is generally not a taxable event. The trust uses the grantor's SSN as its TIN. Required documentation typically includes a trust certification, the account holder's written instruction, and (depending on the custodian) a medallion signature guarantee.
- **Name change (marriage or divorce):** The account title changes to reflect the new legal name. Required documentation: legal name change document (marriage certificate, court order), government-issued ID in the new name (or a combination of old ID plus name change document), updated W-9.
- **Joint to individual (death of co-owner):** For JTWROS accounts, the surviving owner becomes the sole owner. Required documentation: death certificate and letter of instruction from the surviving owner. The custodian removes the deceased owner's name from the account. For TIC accounts, the deceased owner's share passes to their estate, requiring a different process.
- **Individual to estate:** Upon death, the individual account may need to be re-titled to the estate while probate is underway. Required documentation: death certificate, letters testamentary or letters of administration, EIN for the estate.
- **Trust to beneficiaries (trust termination):** When a trust terminates per its terms, assets are distributed to trust beneficiaries. Required documentation: trustee certification of termination, distribution instructions, beneficiary identification and account setup.
- **Entity restructuring:** LLC converting to corporation, partnership changes, mergers. Required documentation: entity formation/conversion documents, corporate resolutions, updated operating agreements.

**Tax implications of re-registration:**
- **Cost basis transfer:** When assets are re-registered without a change in beneficial ownership (e.g., individual to revocable trust, name change), the cost basis carries over unchanged. The original acquisition dates and cost lots transfer to the new registration.
- **Step-up in basis:** When assets transfer due to death, the beneficiary generally receives a stepped-up cost basis equal to the fair market value of the assets on the date of death (or alternate valuation date if elected by the estate). This step-up eliminates unrealized capital gains that existed during the decedent's lifetime. Community property assets may receive a full step-up on both halves at the first spouse's death in community property states.
- **Taxable transfers:** Re-registration that constitutes a gift (e.g., transferring assets from parent to child) or a sale (e.g., transferring assets to an unrelated party) may trigger gift tax or capital gains tax. The firm should not provide tax advice but should flag these situations and recommend the client consult a tax advisor.

**Medallion signature guarantee requirements:**
A medallion signature guarantee is a certification by a financial institution that a signature is genuine and that the signer has the authority to execute the transaction. Medallion guarantees are commonly required for: transfers of securities to a different name or entity, requests to change account registration, physical stock certificate transfers, and certain large-value transactions. The three medallion guarantee programs are STAMP (Securities Transfer Agents Medallion Program), SEMP (Stock Exchanges Medallion Program), and MSP (NYSE Medallion Signature Program). Not all financial institutions participate in all programs; the firm must verify that the guarantee is from an institution participating in an accepted program.

**Custodian processing:**
Re-registration timelines vary significantly by custodian and complexity. Simple name changes may process in 1-3 business days. Trust re-registrations typically take 3-7 business days. Estate re-registrations and complex entity changes may take 1-4 weeks, particularly if the custodian's legal department must review trust or entity documents. During processing, the account may be in a restricted state where trading is limited. The firm should set client expectations regarding processing times and any trading restrictions during the re-registration period.

### Cost Basis Management
Accurate cost basis tracking is essential for tax reporting (1099-B), client tax planning, and regulatory compliance. The firm's obligations depend on whether shares are "covered" (acquired after the applicable effective date under the Emergency Economic Stabilization Act of 2008) or "uncovered."

**Tax lot accounting methods:**
- **Specific identification (Spec ID):** The client or advisor selects which specific tax lots to sell. This provides maximum tax control — the ability to choose lots with the highest cost basis (minimizing gains) or lowest basis (harvesting losses). Requires lot-level identification at the time of the trade, either proactively or within the settlement period.
- **First In, First Out (FIFO):** The oldest shares are deemed sold first. This is the IRS default method if no other method is elected. FIFO tends to produce long-term capital gains (favorable tax rates) but may not minimize total tax liability.
- **Last In, First Out (LIFO):** The most recently acquired shares are deemed sold first. This tends to produce short-term capital gains but may result in lower gain amounts if recent purchases were at higher prices.
- **Highest In, First Out (HIFO):** The shares with the highest cost basis are deemed sold first. This minimizes realized gains and is often the preferred method for taxable accounts focused on tax efficiency.
- **Average cost:** Available only for mutual fund shares and shares acquired through dividend reinvestment plans. The average cost of all shares is used as the basis for each share sold. Once elected for a specific fund, average cost applies to all shares of that fund in the account.

**Cost basis transfer rules:**
- **ACATS transfers:** When securities transfer between brokers via ACATS, the delivering firm is required to transfer cost basis information for covered shares to the receiving firm. The receiving firm must use the transferred basis for 1099-B reporting. For uncovered shares, basis transfer is on a best-efforts basis. Discrepancies between transferred basis and the client's records should be identified and resolved promptly.
- **Re-registration transfers:** Cost basis carries over in non-taxable re-registrations (e.g., individual to revocable trust). For transfers due to death, the receiving account should reflect the stepped-up basis as of the date of death.
- **Gift transfers:** The recipient generally takes the donor's cost basis (carryover basis) for gains. If the fair market value at the time of gift is less than the donor's basis, special rules apply for determining basis for loss purposes (the basis is the FMV at the date of the gift).

**Corporate action adjustments:**
Corporate actions frequently alter cost basis, and errors in corporate action processing are a leading source of cost basis inaccuracies:
- **Stock splits and reverse splits:** The total cost basis remains the same; per-share basis adjusts proportionally. A 2-for-1 split halves the per-share basis; a 1-for-10 reverse split multiplies per-share basis by 10.
- **Mergers and acquisitions:** If the merger is a tax-free reorganization (stock-for-stock exchange), the cost basis of the old shares carries over to the new shares, allocated proportionally. If the merger involves cash consideration (cash-and-stock deal), the cash portion is taxable and reduces the basis allocated to the new shares.
- **Spin-offs:** The cost basis of the parent company shares is allocated between the parent and the spun-off entity based on the relative fair market values on the distribution date. The IRS typically provides allocation guidance or the companies publish allocation percentages.
- **Return of capital distributions:** Reduce the cost basis of the shares. If return of capital exceeds the cost basis, the excess is treated as capital gain. Accurate tracking of return of capital distributions over time is critical for partnerships, REITs, and MLPs.

**Wash sale tracking:**
The wash sale rule (IRC Section 1091) disallows a loss deduction if substantially identical securities are purchased within 30 days before or after the sale. The disallowed loss is added to the cost basis of the replacement shares. Firms must track wash sales within the same account and, for tax reporting purposes, across all accounts of the same taxpayer at the firm. Cross-account and cross-firm wash sale tracking remains the taxpayer's responsibility, but the firm should provide tools and reporting to assist.

**Covered vs uncovered shares and 1099-B reporting:**
For covered shares, the broker is required to report cost basis to the IRS on Form 1099-B and to apply the client's elected accounting method. For uncovered shares, the broker reports the sale proceeds but is not required to report cost basis (Box 1e is left blank). The client is responsible for reporting basis on their tax return for uncovered shares. The firm should maintain whatever historical basis records it has for uncovered shares and make them available to clients, but the obligation to report accurate basis to the IRS rests with the taxpayer.

### Account Restrictions and Holds
Restrictions limit or prevent transactions on an account. They may be imposed by the firm, a regulator, a court, or by operation of law. Proper restriction management protects the firm from liability and ensures compliance with legal and regulatory requirements.

**Types of restrictions:**
- **Death notification hold:** Upon receipt of a death notification, the firm must immediately restrict the deceased's accounts to prevent unauthorized transactions. No new trades, distributions, or changes should be processed until the firm receives appropriate legal documentation (death certificate, letters testamentary/administration, or beneficiary claim forms). Joint accounts with rights of survivorship are an exception — the surviving owner retains trading authority, but the deceased's name must be removed via re-registration.
- **Divorce/domestic relations hold:** When the firm receives a divorce decree or court order related to a domestic dispute, affected accounts may be restricted pending asset division. The restriction should prevent both parties from making withdrawals or transfers until the division is executed per the court order. QDRO processing for retirement accounts requires special handling (see Life Event Processing below).
- **Legal hold (litigation/subpoena):** A legal hold preserves account records and may restrict transactions when the firm receives a subpoena, litigation hold notice, or regulatory investigation notification. The hold prevents destruction of relevant records and may restrict the account holder's ability to close the account or transfer assets.
- **Compliance hold:** The firm's compliance department may restrict an account pending investigation of suspicious activity (SAR filing), suitability concerns, or other compliance issues. The restriction scope is determined by the nature of the concern — it may be a full freeze or limited to specific transaction types.
- **Reg T freeze:** Under Regulation T, if a client purchases securities and fails to pay for them by the payment date (settlement date), the account may be frozen for 90 days. During the freeze, the client can only purchase securities if the full purchase price is deposited in advance (cash before trade). The restriction is lifted after 90 days or upon application to the firm's credit department.
- **Margin restriction:** When a margin account is in a margin call (maintenance call, Reg T call, or house call) and the client fails to meet the call, the firm may restrict trading to liquidation-only until the call is met.
- **OFAC match:** If an account holder or associated party matches a name on the OFAC Specially Designated Nationals (SDN) list, the account must be blocked (frozen) immediately. All assets in the account are blocked and no transactions may be processed. The firm must file a blocking report with OFAC within 10 business days. The block remains until OFAC provides a specific license to unblock or the match is resolved as a false positive.
- **Garnishment and levy:** When the firm receives a valid garnishment order, tax levy (IRS or state), or attachment order from a court or government agency, the firm must comply by freezing the specified amount and/or remitting funds as directed. Retirement accounts have limited protection under ERISA and state law, requiring careful analysis before responding to a garnishment.

**Restriction application and removal procedures:**
Restrictions should be applied immediately upon receipt of the triggering event (death notification, court order, compliance directive). The restriction should be documented in the account master record and visible to all users who access the account, including advisors, operations staff, and client service representatives. Removal of restrictions requires documented authorization: compliance sign-off for compliance holds, receipt of legal documentation for death and divorce holds, passage of time for Reg T freezes, and OFAC license or false positive determination for OFAC blocks.

### Standing Instructions
Standing instructions are pre-authorized, recurring or default instructions on an account that execute automatically without requiring individual authorization for each occurrence.

**Common standing instruction types:**
- **Systematic withdrawal plan (SWP):** Periodic distributions from the account (monthly, quarterly, annually) in a fixed dollar amount or percentage. Common for retirement income accounts. The plan should specify the source (which holdings to sell or cash to distribute), the distribution method (check, ACH, wire), and tax withholding elections (federal and state).
- **Automatic investment plan (AIP):** Periodic contributions to the account, typically via ACH from a bank account, invested according to a specified allocation (model portfolio, specific funds, or dollar-cost averaging into specified securities).
- **Dividend reinvestment (DRIP):** Elections to reinvest dividends and capital gains distributions rather than receiving cash. DRIP elections may be set at the account level (all holdings) or at the individual security level. Reinvested shares create new tax lots at the reinvestment price.
- **Fee debit instructions:** Authorization for the firm to deduct advisory fees directly from the account. The instruction should specify the fee schedule, billing frequency (monthly, quarterly), and the billing source (which account to debit if the client has multiple accounts). SEC guidance requires that the fee authorization be documented in writing and that the client receive advance notice of fee debits.
- **Cash sweep instructions:** Direction for uninvested cash to be automatically swept into a designated vehicle — money market fund, bank deposit program (FDIC-insured sweep), or interest-bearing cash account. Sweep elections are typically set at account opening but may be changed.
- **Standing wire/ACH instructions:** Pre-authorized instructions for recurring or on-demand transfers to a specific external account (bank account, third-party account). Standing wire instructions reduce fraud risk by limiting wire destinations to pre-verified accounts. Adding a new wire destination should require enhanced verification (callback, written authorization, hold period before first use).

**Instruction modification procedures:**
Modifications to standing instructions should follow the same identity verification procedures as other account changes. Changes to fee debit instructions and distribution methods should be documented in writing. The firm should maintain an audit trail of all instruction changes, including the prior instruction, the new instruction, the date of change, and the identity of the requesting party and the processor.

### Life Event Processing
Life events trigger complex, multi-step account maintenance workflows that cut across multiple accounts and registration types. These events have legal, tax, and operational dimensions that require coordinated processing.

**Death notification and estate processing:**
1. **Receive and verify the death notification.** The firm may learn of a death from a family member, advisor, estate attorney, or obituary monitoring service. The firm should verify the notification by requesting a certified death certificate. A verbal notification is sufficient to trigger an immediate account restriction, but documentation is required before any further processing.
2. **Restrict all accounts.** Upon notification, immediately restrict all accounts in the deceased's name — individual accounts, the deceased's interest in joint accounts, retirement accounts, and any accounts where the deceased was an authorized party. For JTWROS accounts, the surviving owner retains access but the account must be re-registered.
3. **Identify account types and disposition paths.** Each account type follows a different disposition path:
   - *Individual taxable accounts:* Assets pass to the estate (if no TOD) or to TOD beneficiaries (if TOD is on file). Estate distribution requires letters testamentary.
   - *Joint accounts (JTWROS):* Assets pass to the surviving owner automatically. Re-register by removing the deceased's name upon receipt of the death certificate.
   - *Joint accounts (TIC):* The deceased's proportional share passes to their estate. The surviving owner retains their share.
   - *Retirement accounts (IRA, 401k):* Assets pass to the named beneficiary per the beneficiary designation on file. Beneficiary claims require the death certificate and a beneficiary claim form. Inherited IRA accounts must be established for each beneficiary.
   - *Trust accounts:* Disposition depends on the trust terms. The successor trustee takes control upon the death of the original trustee. If the trust terminates, assets are distributed to trust beneficiaries per the trust instrument.
   - *TOD accounts:* Assets transfer directly to named TOD beneficiaries upon receipt of the death certificate and beneficiary claim forms, bypassing probate.
4. **Process beneficiary claims and estate distributions.** For each account, collect the required documentation (death certificate, beneficiary claim form, letters testamentary, trust certification of successor trustee) and process the transfer or distribution. Establish new accounts as needed (inherited IRA for each beneficiary, estate account for the personal representative).
5. **Adjust cost basis.** Apply the step-up in basis to all assets as of the date of death (or alternate valuation date). Update cost basis records in the account master and portfolio management system.
6. **Tax reporting.** The deceased's final 1099 covers activity from January 1 through the date of death. Subsequent activity is reported under the estate's EIN or the beneficiary's SSN, depending on how and when assets are distributed.

**Divorce decree processing:**
- **Non-retirement accounts:** The divorce decree or marital settlement agreement specifies how accounts are divided. The firm processes the division by transferring the specified assets or dollar amounts to the receiving spouse's account. If the receiving spouse does not have an account, one must be opened. The transfer between spouses incident to divorce is not a taxable event (IRC Section 1041); cost basis carries over to the receiving spouse.
- **Retirement accounts — QDRO:** Division of ERISA-governed retirement plan assets requires a Qualified Domestic Relations Order (QDRO). The QDRO must be reviewed and accepted by the plan administrator. For IRAs (which are not ERISA-governed), a transfer incident to divorce is processed per the divorce decree without a QDRO, pursuant to IRC Section 408(d)(6).
- **Account restrictions during divorce:** The firm should restrict affected accounts upon receiving a court order or notification from either party's attorney. Restrictions prevent either party from depleting assets before the division is executed.

**Marriage processing:**
- **Name change:** Process the name change re-registration with supporting documentation (marriage certificate, updated ID).
- **Beneficiary review:** Prompt the client to review and update beneficiary designations on all accounts.
- **Account consolidation:** If both spouses have accounts at the firm, they may wish to establish joint accounts or consolidate household accounts. New joint account opening follows standard onboarding procedures.

**Incapacity:**
- **Power of attorney (POA):** A POA grants an agent authority to act on the account holder's behalf. The firm must review the POA document to confirm it grants authority over financial accounts, verify the agent's identity, and determine whether the POA is durable (survives incapacity) or springs into effect only upon incapacity. Many custodians have specific POA acceptance requirements and may require their own POA form.
- **Guardianship/conservatorship:** A court-appointed guardian or conservator presents court documentation granting authority over the incapacitated person's financial affairs. The firm must verify the court order, confirm its scope and jurisdiction, and establish the guardian/conservator as the authorized party on the account. Transactions by the guardian/conservator may be subject to court oversight and reporting requirements.
- **Senior investor protections:** FINRA Rule 2165 permits firms to place a temporary hold on disbursements from the account of a specified adult (age 65+) or an adult with a mental or physical impairment if the firm reasonably believes financial exploitation is occurring. The hold may last up to 25 business days (with a possible extension). The firm must notify the trusted contact person (FINRA Rule 4512) and document the basis for the hold.

### Account Closure
Account closure is the final stage of the account lifecycle. Whether voluntary or involuntary, the closure process must ensure complete asset disposition, final billing, and regulatory-compliant record retention.

**Voluntary closure:**
The account holder (or authorized party) requests closure. The firm processes the request by: (1) confirming the client's identity and authorization, (2) determining asset disposition — transfer to another firm via ACAT, liquidation and check/wire, or in-kind transfer to a specific account, (3) processing final fee billing and any outstanding charges, (4) generating final account statements and tax documents, and (5) closing the account in the custodian and internal systems. The firm should document the reason for closure (client-provided or advisor-noted) for business analytics and regulatory purposes.

**Involuntary closure:**
The firm may close an account without the holder's request in certain circumstances: prolonged inactivity (no activity and zero or de minimis balance for a defined period), failure to provide required documentation (CIP/KYC deficiencies), compliance determination (AML concerns, pattern of trading violations, unsuitable activity), or business decision (exiting a client segment, platform consolidation). Involuntary closure requires advance written notice to the account holder (typically 30 days), an opportunity for the client to transfer assets, and compliance review and approval.

**Abandoned property (escheatment):**
State unclaimed property laws require firms to identify and report abandoned accounts — accounts with no client-initiated activity for the state's dormancy period (typically 3-5 years, varying by state and property type). Before escheatment, the firm must conduct due diligence to locate the account holder (mailing, email, phone attempts, database searches). If the owner cannot be located, the assets are remitted to the state of the owner's last known address (or the firm's state of incorporation if no address is on file). Escheatment processing requires careful tracking because each state has different dormancy periods, due diligence requirements, reporting deadlines, and remittance procedures.

**Record retention post-closure:**
Closing an account does not terminate the firm's recordkeeping obligations. SEC Rule 17a-4 (broker-dealers) and Rule 204-2 (investment advisers) require retention of account records for specified periods after the account is closed — generally 6 years for most account records. The firm must maintain access to closed account records for regulatory examinations, client inquiries, and potential litigation. Records should be archived in a searchable, retrievable format.

## Worked Examples

### Example 1: Processing an account re-registration from individual to revocable trust

**Scenario:** A 62-year-old client with $3.2M across three accounts at the firm (individual taxable brokerage account with $2.1M, traditional IRA with $800K, and Roth IRA with $300K) has recently established a revocable living trust with her estate attorney. The trust names the client as grantor and trustee, with her adult son as successor trustee. The client wants to transfer the taxable brokerage account into the trust. The IRA and Roth IRA cannot be held in a trust (they must remain in the individual's name).

**Step-by-step processing:**

1. **Verify the request and gather documentation.** Confirm the client's identity and the nature of the request. Obtain: (a) a trust certification or the relevant pages of the trust agreement showing the trust name, date of establishment, grantor, trustee(s), successor trustee(s), and the trust's powers regarding investment accounts; (b) a signed letter of instruction from the client directing the re-registration; (c) an updated W-9 in the trust's name (using the client's SSN, since this is a grantor trust). Depending on the custodian, a medallion signature guarantee on the letter of instruction may be required.

2. **Review the trust document.** Operations or the compliance team reviews the trust certification to confirm: the trust is validly established, the client is the current trustee with authority to open and manage investment accounts, the trust is revocable (confirming grantor trust status and SSN usage), and there are no restrictions on the types of investments the trust can hold. Flag any unusual provisions for compliance review.

3. **Prepare the custodian re-registration request.** Complete the custodian's account re-registration or re-titling form. The new registration will read something like: "Jane A. Smith, Trustee of the Jane A. Smith Revocable Living Trust dated January 15, 2026." Submit the form, trust certification, W-9, and letter of instruction to the custodian.

4. **Confirm the tax treatment.** This re-registration is not a taxable event. The assets move from the individual's name to her revocable trust with no change in beneficial ownership. All existing tax lots, cost basis, and acquisition dates carry over unchanged. The account will continue to report under the client's SSN for tax purposes. Document this determination in the account notes.

5. **Update internal systems.** After the custodian confirms the re-registration: update the CRM to reflect the trust account and its relationship to the client record; update the portfolio management system's account registration; verify that the model portfolio assignment and investment restrictions carry over; confirm that the billing account linkage is maintained (fees are typically still billed to the trust account or another account in the household); update beneficiary designations on the IRA and Roth IRA if the client wishes to name the trust as a beneficiary (noting the tax implications — a trust as IRA beneficiary may limit stretch distribution options).

6. **Client communication.** Send the client a confirmation of the completed re-registration with the new account title. Remind the client that the IRA and Roth IRA remain in her individual name and that she should coordinate with her estate attorney to ensure beneficiary designations on those accounts align with the trust's distribution provisions.

**Key risks and controls:** Verify that the SSN (not a separate EIN) is used for the grantor trust — using an EIN would create tax reporting errors. Confirm that cost basis records are preserved through the re-registration; some custodian systems may reset cost basis if the re-registration is processed as a close-and-reopen rather than a title change. Monitor for this and correct any basis discrepancies immediately.

### Example 2: Handling a death notification across multiple accounts with different registration types

**Scenario:** The firm receives a call from the wife of a 71-year-old client who passed away two days ago. The deceased client held five accounts at the firm: (1) an individual taxable brokerage account ($1.4M), (2) a joint taxable brokerage account with his wife as JTWROS ($900K), (3) a traditional IRA ($650K) with his wife as primary beneficiary and two adult children as contingent beneficiaries, (4) a Roth IRA ($200K) with the same beneficiary designation, and (5) a revocable trust account ($500K) where the deceased was sole trustee and his wife is named as successor trustee. The firm also manages the wife's individual IRA ($400K) separately.

**Step-by-step processing:**

1. **Receive and document the notification.** Record the date and time of the notification, the identity of the person providing notification (the wife), and the relationship to the deceased. Express appropriate condolences. Explain that you will need a certified death certificate to proceed with account processing and outline the general timeline. Assign a dedicated operations contact or "estate services coordinator" as the single point of contact for the family.

2. **Immediately restrict the deceased's accounts.** Place a death restriction on all five accounts. For accounts (1), (3), (4), and (5), this means no trading, distributions, or changes until appropriate documentation is received. For account (2) — the JTWROS account — the wife retains access as the surviving owner, but place a notation that the deceased owner must be removed via re-registration. Do not restrict the wife's own IRA (account 6), as it is not an account of the deceased.

3. **Request required documentation.** Provide the wife with a checklist of documents needed for each account:
   - *All accounts:* Certified death certificate (at least 3 copies recommended).
   - *Individual taxable account (1):* If a TOD designation is on file, a beneficiary claim form. If no TOD, letters testamentary (if there is a will) or letters of administration (if intestate), and the estate's EIN.
   - *JTWROS account (2):* Death certificate only — the wife will become sole owner.
   - *Traditional IRA (3) and Roth IRA (4):* Beneficiary claim forms for the wife as primary beneficiary. The wife will need to decide whether to roll the traditional IRA into her own IRA (spousal rollover), treat it as her own, or establish an inherited IRA. For the Roth IRA, a spousal rollover into her own Roth IRA is typically the most advantageous option.
   - *Trust account (5):* Trust certification showing the wife as successor trustee, or the relevant pages of the trust agreement confirming successor trustee status.

4. **Process each account upon receipt of documentation.**
   - *Account 1 (individual taxable):* Assume a TOD designation naming the wife. Upon receipt of the death certificate and signed beneficiary claim form, transfer assets to the wife's account (or a new account in her name). Apply the step-up in basis — revalue all positions to their fair market value as of the date of death. If no TOD, assets pass to the estate: open an estate account titled "Estate of [Deceased], [Personal Representative] as Executor/Administrator," obtain the estate's EIN, and transfer assets to the estate account pending probate and distribution.
   - *Account 2 (JTWROS):* Upon receipt of the death certificate, re-register the account in the wife's name alone. Remove the deceased's name from the account title. The wife's SSN remains on the account. Apply the step-up in basis to the deceased's half of the account (50% of each position is stepped up to date-of-death FMV in non-community-property states; in community property states, both halves may be stepped up).
   - *Account 3 (traditional IRA):* The wife elects spousal rollover, rolling the $650K into her own traditional IRA. This is the most common election because it allows the wife to defer RMDs until she reaches age 73 and name her own beneficiaries. Process the rollover as a trustee-to-trustee transfer. Cost basis is not relevant for traditional IRA assets (fully taxable on distribution), but the transfer must be processed as a non-taxable rollover and reported on Form 1099-R with the appropriate distribution code.
   - *Account 4 (Roth IRA):* The wife elects to treat the inherited Roth as her own Roth IRA by rolling it into her existing or a new Roth IRA. This preserves the tax-free growth and eliminates any distribution requirements during her lifetime.
   - *Account 5 (trust account):* Upon receipt of the trust certification confirming the wife as successor trustee, re-title the account to reflect her as trustee: "[Wife's Name], Trustee of the [Trust Name]." Review the trust terms to determine if the trust continues (common with revocable trusts that become irrevocable upon death of the grantor) or terminates and distributes assets to beneficiaries. If the trust becomes irrevocable, it will need its own EIN going forward.

5. **Coordinate tax reporting.** The deceased's final tax year runs from January 1 to the date of death. Activity on accounts (1) through (5) through the date of death is reported under the deceased's SSN. Activity after the date of death is reported under the wife's SSN (for accounts she takes over), the estate's EIN (for estate accounts), or the trust's EIN (if the trust becomes irrevocable). Work with the custodian to ensure correct TIN assignment on all accounts post-death.

6. **Update all internal systems.** Update the CRM to reflect the death, change the household structure, reassign the advisor relationship to the wife as the primary client, update account registrations in the portfolio management system, and adjust the billing configuration (the wife may now be the billable party for all accounts). Schedule a follow-up meeting between the advisor and the wife (after an appropriate interval) to review the consolidated portfolio, update her investment policy, and adjust the financial plan.

**Key risks and controls:** The greatest risk is processing transactions on a deceased person's account before proper documentation is in hand — this can create legal liability and tax reporting errors. The second risk is incorrect cost basis after the step-up: every position must be revalued to the date-of-death FMV, and the custodian's automated step-up process should be verified against an independent price source. Third, ensure that IRA beneficiary elections (spousal rollover vs inherited IRA) are documented in writing, as the choice is irrevocable and has significant long-term tax implications.

### Example 3: Implementing systematic account maintenance review and data quality processes

**Scenario:** A mid-sized RIA with $5B AUM across 4,000 accounts has identified recurring data quality issues: 12% of accounts have no beneficiary designation on file, 8% have addresses that generate returned mail, 15% of trust accounts are missing current trust certifications, and the firm has no systematic process for reviewing accounts that have not been updated in more than 3 years. The firm wants to implement a proactive account maintenance review program to improve data quality, reduce operational risk, and satisfy regulatory expectations for books and records.

**Designing the review program:**

1. **Establish a data quality baseline.** Generate a comprehensive data quality report across all accounts, measuring completeness and accuracy for critical fields:
   - *Beneficiary designations:* Percentage of eligible accounts (retirement accounts, TOD accounts) with primary and contingent beneficiaries on file, percentage with beneficiary review within the past 3 years.
   - *Contact information:* Percentage of accounts with validated mailing addresses (no returned mail), percentage with email on file, percentage with phone number on file and verified.
   - *Trust and entity documentation:* Percentage of trust accounts with trust certification on file and dated within the past 5 years, percentage of entity accounts with current formation documents and beneficial ownership certification.
   - *Suitability profiles:* Percentage of accounts with investment profile updated within the past 3 years, percentage with risk tolerance questionnaire on file.
   - *Standing instructions:* Percentage of accounts with systematic plans that have not been reviewed in more than 2 years.
   - *Cost basis records:* Percentage of holdings with uncovered shares that have no historical cost basis on file.

2. **Prioritize remediation by risk and impact.** Not all data quality issues carry equal risk. Prioritize:
   - *High priority (remediate within 90 days):* Missing beneficiary designations on retirement accounts (disposition risk at death), returned mail with no valid address on file (regulatory and escheatment risk), accounts with compliance or legal holds that have not been reviewed in 6+ months.
   - *Medium priority (remediate within 180 days):* Stale trust certifications (operational risk at trustee change or death), outdated suitability profiles (regulatory risk for ongoing recommendations), missing cost basis on large positions (tax reporting risk).
   - *Lower priority (remediate within 12 months):* Missing email addresses, missing contingent beneficiary designations, standing instructions that have not been reviewed recently.

3. **Design the ongoing review cadence.** Establish a recurring review cycle:
   - *Annual account maintenance review:* Coincide with the annual client review meeting. The advisor reviews and confirms: contact information, beneficiary designations, suitability profile, investment restrictions, standing instructions, and account features. The review is documented in the CRM with a timestamp and the advisor's attestation that all information is current.
   - *Quarterly data quality reports:* Operations generates quarterly metrics showing data completeness rates, trending, and accounts requiring attention. The report is reviewed by the chief compliance officer and the operations manager.
   - *Triggered reviews:* Certain events trigger an immediate account review outside the annual cycle: returned mail, life event notification (marriage, divorce, birth, death), significant market events that may affect suitability, advisor departure (all accounts assigned to a departing advisor receive an expedited review by the successor advisor), and custodian platform migration.

4. **Implement operational workflows for common maintenance items.** For each maintenance category, define a standard operating procedure (SOP) that specifies:
   - *Who* can initiate the request (client, advisor, operations, compliance)
   - *What* documentation or verification is required
   - *How* the request is processed (system workflow, custodian submission)
   - *When* the request must be completed (service-level agreement)
   - *What* quality checks are performed before and after processing
   - *How* the completed action is documented and retained

   For example, the SOP for an address change specifies: the advisor or client initiates the request; identity verification is performed per firm policy (callback to phone on file for verbal requests, or written/electronic authorization); the address is updated in the CRM (system of record); the CRM integration propagates the change to the custodian and correspondence system; a confirmation is sent to both the old and new addresses; senior investor protections are applied if the client is 65+ and the change triggers a red flag; the change is completed within 2 business days; and the change record is retained in the CRM activity log.

5. **Assign accountability and measure progress.** Designate an "account data steward" — a member of the operations team responsible for data quality monitoring and remediation coordination. Publish a monthly data quality dashboard tracking: percentage of accounts with complete and current data across all critical fields, number of open remediation items by priority, average age of open items, and NIGO rates (as a proxy for data quality at the point of custodian submission). Set targets: 95% completeness for high-priority fields within 12 months, 90% for medium-priority fields within 18 months.

**Key risks and controls:** The primary risk in a data quality remediation program is client fatigue — contacting thousands of clients to update information can strain advisor relationships if not managed carefully. Mitigate this by embedding updates in existing client interactions (annual review meetings, service calls) rather than launching a standalone outreach campaign. The second risk is privacy: ensure that all outreach communications about account data comply with Reg S-P and do not disclose nonpublic personal information. Third, maintain an audit trail of all remediation activities for regulatory examination purposes — examiners expect to see a documented, systematic approach to data quality, not ad hoc corrections.

## Common Pitfalls
- Processing an address change without adequate identity verification, enabling unauthorized changes or elder financial exploitation
- Failing to update beneficiary designations after a divorce — the former spouse may inherit retirement account assets if the designation is not changed, regardless of the divorce decree (for non-ERISA accounts in most states)
- Re-registering an account as a close-and-reopen rather than a title change, which can reset cost basis records and create phantom taxable events
- Applying the wrong tax lot accounting method after an ACATS transfer because the receiving firm's default differs from the client's prior election
- Not placing an immediate restriction on all of a deceased client's accounts upon death notification, allowing unauthorized transactions
- Processing a power of attorney without verifying that the document grants authority over financial accounts and that the POA is durable (survives incapacity)
- Failing to distinguish between covered and uncovered shares when processing cost basis transfers, leading to incorrect 1099-B reporting
- Allowing a standing wire instruction to be added or changed without enhanced verification (callback, hold period), creating wire fraud exposure
- Not tracking return-of-capital distributions on partnerships, REITs, and MLPs, leading to overstated cost basis and incorrect gain/loss calculations
- Processing estate distributions before receiving letters testamentary or letters of administration, exposing the firm to liability if the distribution is challenged
- Neglecting escheatment obligations for dormant accounts, resulting in regulatory penalties from state unclaimed property audits
- Treating all joint accounts the same upon a co-owner's death — JTWROS and TIC accounts have fundamentally different disposition rules

## Cross-References
- **account-opening-workflow** (Layer 12, client-operations): Account opening establishes the initial registration, beneficiary designations, and standing instructions that this skill maintains throughout the account lifecycle
- **books-and-records** (Layer 9, compliance): Recordkeeping obligations for account maintenance documentation, including retention of change requests, authorizations, and correspondence per SEC Rules 17a-3/17a-4 and Rule 204-2
- **privacy-data-security** (Layer 9, compliance): Address changes, contact updates, and account data maintenance involve nonpublic personal information protected by Reg S-P; data quality processes must comply with privacy requirements
- **tax-efficiency** (Layer 5, policy-planning): Cost basis management, tax lot accounting method selection, and step-up in basis processing directly affect tax-efficient investing outcomes
- **client-onboarding** (Layer 10, advisory-practice): Onboarding collects the initial data (beneficiaries, suitability, contact information) that account maintenance keeps current throughout the relationship
- **corporate-actions** (Layer 12, client-operations): Corporate actions (splits, mergers, spin-offs, return of capital) alter cost basis and require coordination with the cost basis management processes described in this skill
- **account-transfers** (Layer 12, client-operations): ACATS and non-ACATS transfers interact with cost basis transfer rules and re-registration procedures; transfer processing often triggers account maintenance updates at the receiving firm
