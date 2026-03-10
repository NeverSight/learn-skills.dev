---
name: check-relocation-documents
description: >
  Verify document completeness for each bureaucratic step of an EU/DACH
  relocation, flagging missing items and translation requirements. Use after
  creating a relocation plan and before beginning bureaucratic procedures, when
  preparing for a specific appointment (Buergeramt, Finanzamt), when unsure
  which documents need certified translation or apostille, after receiving a
  rejection or request for additional documents, or as a periodic check during
  the relocation process to ensure nothing has been overlooked.
license: MIT
allowed-tools: Read Grep Glob WebFetch WebSearch
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: relocation
  complexity: intermediate
  language: natural
  tags: relocation, documents, checklist, verification, translation
---

# Check Relocation Documents

Verify that all required documents are present, valid, and properly prepared for each bureaucratic step of an EU/DACH relocation, generating an actionable list of missing items and translation needs.

## When to Use

- After creating a relocation plan and before beginning bureaucratic procedures
- When preparing for a specific appointment (Buergeramt, Finanzamt, insurance office)
- When unsure which documents need certified translation or apostille
- After receiving a rejection or request for additional documents from an authority
- When a household member has a different nationality requiring separate document tracks
- As a periodic check during the relocation process to ensure nothing has been overlooked

## Inputs

### Required

- **Relocation plan**: Output from the plan-eu-relocation skill or equivalent, listing all bureaucratic steps
- **Destination country**: Germany, Austria, Switzerland, or other EU country
- **Nationality/nationalities**: For all household members
- **Document inventory**: List of documents currently in possession (originals and copies)

### Optional

- **Origin country**: For determining which documents need apostille or Hague Convention legalization
- **Employment contract**: To determine employer-provided documents (e.g., Arbeitgeberbescheinigung)
- **Language of existing documents**: To identify translation needs
- **Previous relocation experience**: Prior EU registrations that may simplify requirements
- **Special circumstances**: Recognized refugees, EU Blue Card holders, posted workers (different document requirements)

## Procedure

### Step 1: List All Bureaucratic Steps

Extract every registration, application, and notification step from the relocation plan.

1. Parse the relocation plan for all action items requiring document submission
2. Categorize steps by authority type:
   - Municipal registration offices (Buergeramt, Meldeamt, Einwohnerkontrolle)
   - Tax authorities (Finanzamt)
   - Health insurance providers (Krankenkasse, OeGK, Swiss insurer)
   - Social security offices (Rentenversicherung, Sozialversicherung, AHV)
   - Immigration/foreigners office (Auslaenderbehorde) if applicable
   - Banks and financial institutions
   - Schools and childcare facilities
   - Vehicle registration (Kfz-Zulassungsstelle)
   - Other (pet import, professional license recognition)
3. Order steps according to the dependency chain from the relocation plan
4. Note which steps share the same documents (to avoid redundant preparation)

**Expected:** A numbered list of all bureaucratic steps, categorized and ordered, with notes on shared document requirements.

**On failure:** If the relocation plan is incomplete or unavailable, build the step list from the destination country's official relocation checklist (e.g., Germany: make-it-in-germany.com, Austria: migration.gv.at, Switzerland: ch.ch/en/moving-switzerland).

### Step 2: Map Required Documents per Step

For each bureaucratic step, identify every document the authority requires.

1. For municipal registration (Anmeldung/Meldezettel):
   - Valid passport or national ID card (all household members)
   - Wohnungsgeberbestaetigung / rental contract / property deed
   - Marriage certificate (if registering as a couple)
   - Birth certificates (for children)
   - Previous registration confirmation (if moving within the country)
2. For tax registration:
   - Residence registration confirmation (Meldebestaetigung/Meldezettel)
   - Employment contract or business registration
   - Tax ID from origin country (for cross-border coordination)
   - Marriage certificate (for tax class assignment in Germany)
3. For health insurance enrollment:
   - Employment contract or proof of self-employment
   - Previous insurance confirmation or EHIC (European Health Insurance Card)
   - S1 form (for posted workers or cross-border situations)
   - Residence registration confirmation
4. For social security coordination:
   - A1 portable document (for posted workers)
   - E-forms or S-forms for benefit transfers
   - Employment history documentation
   - Social security number from origin country
5. For bank account opening:
   - Valid passport or national ID
   - Residence registration confirmation
   - Proof of income (employment contract or recent payslips)
   - Tax ID or Steueridentifikationsnummer (Germany)
6. For immigration/residence permits (non-EU nationals):
   - Valid passport with at least 6 months remaining validity
   - Biometric photos (specific format per country)
   - Employment contract or job offer letter
   - Proof of financial means
   - Health insurance confirmation
   - University degree with recognition (for EU Blue Card)
   - Criminal background check (may require apostille)
7. For vehicle re-registration:
   - Vehicle registration document (Fahrzeugbrief/Zulassungsbescheinigung Teil II)
   - Proof of insurance (eVB number in Germany)
   - TUeV/Pickerl/MFK inspection certificate
   - Residence registration confirmation
8. For school/childcare enrollment:
   - Birth certificates
   - Vaccination records (Impfpass)
   - Previous school reports with translations
   - Residence registration confirmation

**Expected:** A matrix mapping each bureaucratic step to its required documents, with document specifications (original required, copy acceptable, certified translation needed).

**On failure:** If requirements for a specific step are unclear, check the authority's website directly or call their service line. Requirements can change; do not rely solely on third-party guides older than 12 months.

### Step 3: Check Current Document Status

Compare the required documents against the current inventory to identify gaps.

1. For each required document, check:
   - **Have (original)**: Original document is in possession and accessible
   - **Have (copy only)**: Only a copy exists; original may need to be ordered
   - **Expired**: Document exists but validity period has passed
   - **Missing**: Document does not exist and must be obtained
   - **Not applicable**: Document is not needed for this specific case
2. For documents that are "Have (original)", verify:
   - The document is not damaged or illegible
   - Names match across all documents (watch for transliteration differences, maiden names, middle names)
   - The document will still be valid at the time it will be used (passports, ID cards, insurance cards)
3. For expired documents, determine:
   - Renewal processing time at issuing authority
   - Whether an expired document is accepted temporarily (some are, most are not)
   - Cost of renewal
4. For missing documents, determine:
   - Issuing authority and their processing time
   - Required supporting documents to obtain the missing document (recursive check)
   - Cost and payment method
   - Whether it can be ordered remotely or requires in-person appearance
5. Flag any documents where names do not match (e.g., passport has maiden name, marriage certificate has married name) -- these will likely require explanation or additional proof of name change

**Expected:** A status table for every required document: status (have/copy-only/expired/missing/N-A), validity date, and notes on any issues.

**On failure:** If document status cannot be confirmed (e.g., documents are in storage or with another party), mark as "unconfirmed" and treat as potentially missing for planning purposes.

### Step 4: Identify Translation and Apostille Requirements

Determine which documents need certified translation, apostille, or other legalization.

1. Check destination country language requirements:
   - Germany: Documents must generally be in German or accompanied by certified translation
   - Austria: Same as Germany; some offices accept English for EU documents
   - Switzerland: Depends on canton (German, French, Italian, or Romansh area)
2. Identify which documents are exempt from translation:
   - EU multilingual standard forms (Regulation 2016/1191) for birth, marriage, death, and other civil status documents between EU member states
   - Passports and national ID cards (universally accepted without translation)
   - EHIC (European Health Insurance Card)
3. For documents requiring translation:
   - Must be done by a sworn/certified translator (beeidigter Uebersetzer)
   - The translator must be certified in the destination country (not the origin country)
   - Typical turnaround: 3-10 business days
   - Cost: 30-80 EUR per page depending on language pair and complexity
4. Determine apostille or legalization requirements:
   - Documents from Hague Convention countries: apostille from issuing country's competent authority
   - Documents from non-Hague countries: full legalization chain (local notary, foreign ministry, embassy)
   - EU-internal documents: often exempt from apostille under EU regulations, but verify per document type
   - Switzerland is a Hague Convention member but not an EU member; rules differ
5. Check if the destination country accepts digital or electronic apostilles
6. Note that some documents require both apostille AND certified translation (the apostille itself may also need translation)

**Expected:** A translation/legalization matrix showing for each document: translation needed (yes/no), apostille needed (yes/no), estimated cost, and estimated processing time.

**On failure:** If uncertain whether a specific document needs apostille, contact the destination authority directly. Over-preparing (getting an unnecessary apostille) is better than under-preparing (being turned away at the appointment).

### Step 5: Generate Action List

Compile all findings into a prioritized, deadline-aware action list.

1. Merge all gaps (missing, expired, translation needed, apostille needed) into a single action list
2. For each action item, include:
   - Document name
   - Action required (obtain, renew, translate, apostille, replace)
   - Issuing authority or service provider
   - Estimated processing time
   - Estimated cost
   - Deadline (derived from when the document is first needed in the relocation timeline)
   - Priority (critical / high / medium / low)
3. Assign priority based on:
   - **Critical**: Blocks the first bureaucratic step (e.g., passport for Anmeldung) or has a non-negotiable deadline
   - **High**: Needed within the first 2 weeks after arrival; long processing time
   - **Medium**: Needed within the first month; reasonable processing time
   - **Low**: Needed eventually; no immediate deadline pressure
4. Order the list by:
   - First: Critical items sorted by longest processing time (start these first)
   - Then: High items sorted by deadline
   - Then: Medium and low items
5. Calculate total estimated cost for all document preparation
6. Add a "document folder" checklist for the day of each appointment, listing exactly which originals, copies, and translations to bring

**Expected:** A prioritized action list with deadlines, costs, and processing times, plus per-appointment packing lists for documents.

**On failure:** If processing times are uncertain (common for documents from countries with slower bureaucracies), use worst-case estimates and start the process as early as possible. Flag items where expedited processing is available at additional cost.

## Validation

- Every bureaucratic step from the relocation plan has at least one document mapped to it
- No document is listed as "status unknown" -- all must be confirmed as have/missing/expired/N-A
- Translation requirements reference the destination country's official language requirements
- Apostille requirements are verified against Hague Convention membership of the issuing country
- Deadlines in the action list align with the relocation timeline from plan-eu-relocation
- Priority assignments are consistent (no "low" priority item that blocks a "critical" step)
- The total cost estimate is calculated and presented
- Per-appointment document checklists are generated for at least the first three bureaucratic steps

## Common Pitfalls

- **Assuming EU documents need no preparation**: While EU regulations simplify cross-border document acceptance, most offices still require translations and some require apostilles even between EU states
- **Name mismatches across documents**: Transliteration from non-Latin scripts, use of maiden vs. married names, and middle name inconsistencies are the most common reason for rejection at appointments
- **Relying on photocopies**: Most DACH authorities require original documents for inspection and keep certified copies; bring originals even if you think copies will suffice
- **Ordering translations too late**: Sworn translators often have 1-2 week backlogs, and this extends during peak relocation season (August-September)
- **Forgetting the apostille on the translation**: Some authorities require the apostille on the original document AND a separate certified translation of the apostilled document
- **Not checking document validity periods**: A passport valid for 2 more months may be rejected if the authority requires 6 months remaining validity
- **Ignoring the multilingual EU forms**: For civil status documents between EU countries, multilingual standard forms (available from the issuing authority) can eliminate the need for translation entirely -- but you must request them explicitly
- **Assuming digital documents are accepted**: Most DACH government offices still require physical documents; PDF printouts of digital-only documents may not be accepted without additional verification

## Related Skills

- [plan-eu-relocation](../plan-eu-relocation/SKILL.md) -- Create the relocation plan that feeds into this document check
- [navigate-dach-bureaucracy](../navigate-dach-bureaucracy/SKILL.md) -- Detailed guidance for the procedures these documents are needed for
