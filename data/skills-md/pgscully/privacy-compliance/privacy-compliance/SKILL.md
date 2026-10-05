---
name: privacy-compliance
description: Review, audit and draft privacy and data-protection compliance artefacts across jurisdictions - the Australian Privacy Act 1988 and its 13 Australian Privacy Principles, the EU GDPR, the EU AI Act and the EU Data Act, and the California CCPA and its regulations. Use when handling personal or sensitive data, designing collection, storage, sharing, retention or deletion; auditing requirements, designs, code or documentation at any lifecycle stage; creating privacy policies, notices or consent flows; assessing cross-border transfers; planning for or responding to data breaches; or reviewing AI, connected-product, ad-tech and cloud features. Produces findings, audit reports or policy drafts that name the legislation and cite the relevant section, article or APP clause.
license: MIT
---

# Privacy review, audit and policy drafting

Work against the privacy legislation below to do one of three things:

- **Review** software, designs, data flows and written policies, and flag issues
  with precise citations (sections 1–5).
- **Draft or update a privacy policy / privacy notice**, with every required
  element traced to its provision (section 6).
- **Audit** requirements, designs, code and documentation against a defined scope
  and criteria at any lifecycle stage, producing a rated control matrix and a report
  (section 7).

Every mode starts by choosing the jurisdiction(s) below.

> This skill supports engineering, design and documentation work, not legal
> advice. Flag uncertainty and recommend qualified legal advice for novel,
> high-risk or disputed questions.

## 1. Choose the jurisdiction(s)

Determine which regimes apply before reviewing anything. If more than one applies,
review under each and report overlapping findings once, citing both.

| Regime                                         | Applies when                                                                                                                                                                                                                | Reference                   | Official text                                                                                                                                                                        |
| ---------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Australia — Privacy Act 1988 (Cth)**         | An APP entity (agency or organisation) with an Australian link, or a file number recipient / credit reporting body.                                                                                                         | `references/australia/`     | [legislation.gov.au](https://www.legislation.gov.au/C2004A03712/latest/text)                                                                                                         |
| **EU — GDPR (2016/679)**                       | Processing in the context of EU/EEA establishment, or offering goods/services to or monitoring people in the EU.                                                                                                            | `references/eu/gdpr.md`     | [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2016/679/oj)                                                                                                                             |
| **EU — AI Act (2024/1689)**                    | Placing on the market, putting into service or using AI systems with EU effect, including non-EU providers.                                                                                                                 | `references/eu/ai-act.md`   | [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)                                                                                                                            |
| **EU — Data Act (2023/2854)**                  | Connected products, related services, data sharing, cloud switching or unlawful governmental access with EU effect.                                                                                                         | `references/eu/data-act.md` | [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2023/2854/oj)                                                                                                                            |
| **USA / California — CCPA + CCPA Regulations** | A for-profit business doing business in California that meets a threshold (revenue, 100,000+ consumers/households, or 50%+ revenue from selling/sharing), or a service provider/contractor/third party handling their data. | `references/usa/`           | [CCPA statute](https://leginfo.legislature.ca.gov/faces/codes_displayText.xhtml?lawCode=CIV&division=3.&title=1.81.5.&part=4.); [CCPA Regulations](https://cppa.ca.gov/regulations/) |

The references summarise each instrument and cite the exact provisions. **This
package does not ship the full statutes** (to keep it small). Use the official
texts linked above to quote or verify a provision when a point is contested or
high-stakes. Per-instrument last-checked and last-updated dates are recorded in
`references/legislation-status.md`. When in doubt about which regime applies, state
the assumption.

## 2. Task A — review workflow

Work through these steps in order. Do not skip step 1 — most false positives come
from applying an obligation that does not apply.

1. **Establish scope.** For each candidate regime, confirm the entity/role, the
   territorial or Australian link, and any exemption or exclusion (e.g. Australian
   small-business and employee-record exemptions; GDPR household and criminal-law
   exclusions; AI Act military/defence, personal-use and R&D exclusions; Data Act
   micro/small-enterprise and non-production exclusions).
2. **Classify the data.** Identify personal data, sensitive/special-category data,
   and any regulated identifiers. Classification drives which clauses apply.
3. **Map the data lifecycle.** For each stage — collect, notify, store, use,
   disclose/share, transfer, retain, destroy — check the corresponding obligation.
4. **Check the special regimes** where relevant: breaches, impact assessments, AI
   risk classification, and government-access safeguards.
5. **Report findings** in the format below, each naming the legislation and
   citing the provision, with a severity.

## 3. Severity

- **Critical** — likely serious interference/breach, a prohibited practice, an
  unreported notifiable breach, or sensitive/special-category processing without a
  lawful basis; exposes the entity to penalties.
- **High** — clear breach of a specific provision with real harm potential.
- **Medium** — a gap likely to breach an obligation in some circumstances, or a
  missing required control.
- **Low** — documentation, policy or transparency improvements; no direct breach.

## 4. Output format

**Citation convention.** Every citation names the legislation *and* the provision —
never a bare `Art 6(1)(a)`, `s 26WE` or `§ 7013`. Name the instrument with its
official identifier on first use, then use the accepted abbreviation:

| Instrument                       | Cite as                                                                                  |
| -------------------------------- | ---------------------------------------------------------------------------------------- |
| AU Privacy Act 1988 (Cth)        | `Privacy Act 1988 (Cth) s 16C`; `Privacy Act 1988 (Cth) Sch 1 cl 11.1 (APP 11.1)`         |
| EU GDPR (Regulation (EU) 2016/679)   | `GDPR Art 6(1)(a)` (first use: `GDPR (Regulation (EU) 2016/679) Art 6(1)(a)`)         |
| EU AI Act (Regulation (EU) 2024/1689) | `AI Act Art 5(1)(f)` (first use: `AI Act (Regulation (EU) 2024/1689) Art 5(1)(f)`)    |
| EU Data Act (Regulation (EU) 2023/2854) | `Data Act Art 4(12)` (first use: `Data Act (Regulation (EU) 2023/2854) Art 4(12)`)    |
| California CCPA                  | `CCPA § 1798.120`                                                                        |
| CCPA Regulations (11 CCR)        | `CCPA Regs § 7013(c)(1)`                                                                  |

Cite to the finest useful granularity (article, paragraph, point, section, clause).
If several instruments apply to one finding, cite each separately — e.g.
`GDPR Art 6(1)(a); Privacy Act 1988 (Cth) APP 3.3`.

```
### [Severity] Short title
- **Issue:** what is wrong or risky.
- **Location:** file:line, component, design section or policy paragraph.
- **Obligation:** exact provision(s), naming the legislation, e.g. Privacy Act 1988 (Cth) Sch 1 cl 11.1 (APP 11.1); GDPR Art 6(1)(a); AI Act Art 5(1)(f); Data Act Art 4(12); CCPA § 1798.120; CCPA Regs § 7013(c)(1).
- **Why it applies:** tie the facts to the provision, including the regime, data class and any exemption/exclusion considered.
- **Recommendation:** a concrete, testable change.
```

End with a **Summary** (counts by severity, per regime) and a **Scope &
assumptions** note (what was reviewed, assumed scope, and any legal questions for
counsel).

## 5. Quick mapping: common patterns

| Pattern                                                                          | Check                                                                                                                                                                        |
| -------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| New field, form or telemetry event                                               | AU APP 3 + APP 5; GDPR Art 5(1)(c), 6, 13                                                                                                                                    |
| Consent / cookie banner / preference centre                                      | AU APP 3.3, APP 5; GDPR Art 7, 9                                                                                                                                             |
| Analytics, ad tech, trackers, lead gen                                           | AU APP 6, APP 7; GDPR Art 5(1)(b), 21, 22                                                                                                                                    |
| Cloud, offshore hosting, offshore support                                        | AU APP 8, s 16C; GDPR Art 44–49; Data Act Art 32                                                                                                                             |
| Logs, backups, warehouse, ML training data                                       | AU APP 11, APP 10; GDPR Art 5(1)(e), 25, 32; AI Act Art 10, 12                                                                                                               |
| Deletion / access / correction / portability                                     | AU APP 11.2, 12, 13; GDPR Art 15–20; Data Act Art 4, 30                                                                                                                      |
| Identity verification, IDs, biometrics                                           | AU APP 3, APP 9; GDPR Art 9; AI Act Art 5, Annex III                                                                                                                         |
| AI features (chat, scoring, detection)                                           | AI Act Art 5 prohibitions, Art 6/Annex III, Art 14, 26, 50; GDPR Art 22, 35                                                                                                  |
| Workplace monitoring / HR platforms                                              | AU s 7B(3) employee records; AI Act Art 5(1)(f), Art 26(7)                                                                                                                   |
| Incident response / breach runbooks                                              | AU Part IIIC (s 26WE, 26WH, 26WK, 26WL); GDPR Art 33–34                                                                                                                      |
| Connected products / IoT / cloud                                                 | Data Act Art 3–6, 30–32; GDPR Art 6, 20                                                                                                                                      |
| Public-body data requests                                                        | Data Act Art 14–18; GDPR Art 6(1)(e)                                                                                                                                         |
| Selling/sharing data, ad tech, "Do Not Sell or Share"                            | CCPA §§ 1798.120, 1798.135; CCPA Regs §§ 7013, 7025–7026                                                                                                                          |
| Sensitive personal information                                                   | CCPA § 1798.121; CCPA Regs §§ 7014, 7027                                                                                                                                          |
| Automated decisions / profiling / scoring                                        | CCPA Regs §§ 7200, 7220–7222 (ADMT); § 7150 (risk assessment); AI Act Art 5/6; GDPR Art 22                                                                                   |
| Writing or updating a privacy policy                                             | `references/australia/privacy-policy.md`, `references/eu/privacy-notice.md`, `references/usa/privacy-policy.md`, `assets/privacy-policy-template.md`                         |
| Auditing at any lifecycle stage (requirements, design, build, operation, change) | `references/audit.md`, `references/australia/audit-checklist.md`, `references/eu/audit-checklist.md`, `references/usa/audit-checklist.md`, `assets/audit-report-template.md` |

## 6. Task B — draft or update a privacy policy

Use this when asked to create or update a privacy policy or privacy notice. The
output is a drafted document plus a coverage check.

### 6.1 Gather the inputs

Ask for, or infer from the repository and mark as assumed, the following. Do not
invent facts — record unknowns as open questions.

- Entity: legal name, contact details, DPO (if any), EU representative or joint
  controllers (if any); entity type and jurisdictions in scope.
- Data: categories of personal information, and separately sensitive/
  special-category data.
- Collection: sources (direct, third parties, automatic) and means.
- Purposes and the **legal basis** for each (GDPR Art 6; and whether reliance is on
  consent or legitimate interests).
- Recipients and categories of recipients.
- Overseas disclosures/transfers: countries and safeguards.
- Retention periods or the criteria used to determine them.
- Marketing, profiling and automated decisions.
- Access, correction, complaint and opt-out mechanisms.

### 6.2 Draft

Start from `assets/privacy-policy-template.md` and fill it in. Keep it concise,
plain-language and up to date (Privacy Act 1988 (Cth) APP 1.3; GDPR Art 12). Delete
inapplicable
sections and remove the annotations before returning the final text.

Consult the jurisdiction requirement checklists while drafting:

- Australia — `references/australia/privacy-policy.md` (required contents in
  **APP 1.4**, collection-notice matters in **APP 5.2**, cross-border in **APP 8**).
- EU — `references/eu/privacy-notice.md` (transparency in **GDPR Art 12**, content
  for data collected from the subject in **GDPR Art 13**, from other sources in
  **GDPR Art 14**, plus GDPR Art 8, 21, 22, 26, 27, 37 and AI Act Art 50).
- USA / California — `references/usa/privacy-policy.md` (privacy policy and
  Notice at Collection content, opt-out/limit/financial-incentive notices, and the
  ADMT Pre-use Notice under CCPA Regs §§ 7011–7016, 7220).

Where more than one applies, produce a combined or layered notice that satisfies
all of them, with clearly separated jurisdiction sections where the wording
differs.

### 6.3 Validate and report

Return, after the draft:

1. **Coverage check** — a table mapping each required element (Privacy Act 1988 (Cth)
   APP 1.4(a)–(g); GDPR Art 13(1)–(2) / Art 14; CCPA Regs § 7011(e) / § 7012(e)) to the
   section of the draft that satisfies it.
2. **Gaps and open questions** — every placeholder or assumed fact that must be
   confirmed before publishing.
3. **Publication checklist** — dated and versioned, available free of charge and in
   an appropriate form (AU APP 1.5–1.6), reachable from every collection point, and
   consistent with what the system actually does.

## 7. Task C — audit across the lifecycle

Use this when asked to audit for privacy compliance. An audit is a structured,
evidence-based assessment against defined criteria that produces a rated control
matrix and a report — distinct from the ad-hoc review in Task A.

**Audits are not limited to code.** They apply at every stage, including before any
code exists. Establish the **stage(s)** first: it determines the artefacts you can
examine and the kind of finding you can raise.

| Stage                           | Primary artefacts                                                                                                     | Audit focus                                                                                                                                                                       |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Requirements / discovery**    | requirements, user stories, acceptance criteria, process and data-flow descriptions, business case, RFP, data sources | Is the *planned* processing lawful, necessary and proportionate? What privacy requirements must be added (notice, consent, retention, access/correction, cross-border, security)? |
| **Design / architecture**       | architecture and data models, API contracts, IaC plans, vendor/subprocessor selection, threat model, DPIA draft       | Are the required controls *designed in* (minimisation, security, retention, DPbD)?                                                                                                |
| **Development / build**         | code, config, migrations, tests, CI checks                                                                            | Are the designed and required controls *actually implemented*?                                                                                                                    |
| **Pre-release / readiness**     | release checklist, published notices, runbooks, training                                                              | Can the entity meet its obligations from day one?                                                                                                                                 |
| **Post-deployment / operation** | logs, access reviews, data-subject-request records, breach register, retention jobs, monitoring, training records     | Do the controls *operate effectively* over time?                                                                                                                                  |
| **Change / update**             | change requests, PRs, release notes, migrations, new data fields or vendors                                           | Does the change preserve compliance; does it introduce new processing?                                                                                                            |

An audit may cover one stage (e.g. a requirements review, a pre-release readiness
check, a change impact audit) or several. State which stages are in scope and which
are excluded. Where the audit is pre-code, findings will often be **requirements or
design gaps** rather than defects — recommend the requirement, control or design
change needed.

### 7.1 Plan

Record the objective; the **stage(s)** and **scope** (requirements/design set,
repositories, services, environments, documentation, period) with explicit
**exclusions**; the **criteria** (exact legislation and version); the approach
(evidence-based; note limits, e.g. design-only or no operating-effectiveness
testing); and where legal sign-off is required. Prioritise high-risk processing.

### 7.2 Collect evidence

Enumerate the evidence that exists **at the stage in scope** — before concluding.

- **Pre-code:** requirements and user stories, data-flow and process diagrams,
  architecture and data models (planned), vendor selection and data-processing
  intent, DPIA drafts, acceptance criteria.
- **Build and later:** schemas and migrations, collection points, consent
  configuration, IAM and encryption settings, retention/deletion jobs, subprocessor
  and transfer documents, rights workflows, logging, breach runbooks, vendor
  contracts, and operational records (DSR logs, access reviews, breach register).

Record **where** each item is (file:line, config path, document section, or planned
requirement ID). The full evidence map is in `references/audit.md` (section 2).

### 7.3 Test every control

Work through the jurisdiction checklist control by control and **rate each one**
(Conforms / Partially conforms / Does not conform / Not applicable / Not tested).
Adapt the procedure to the stage — for example, test necessity (AU APP 3; GDPR
Art 5(1)(c)) by challenging each planned data element at requirements, by inspecting
the schema at build, and by sampling real records in operation. At pre-code stages,
controls are assessed **by design**; state that operating effectiveness was not
tested.

- Australia — `references/australia/audit-checklist.md` (APP 1–13, Part IIIC,
  Schedule 2, and conditional credit-reporting/code controls).
- EU — `references/eu/audit-checklist.md` (GDPR principles, rights, security and
  transfers; AI Act; Data Act).
- USA / California — `references/usa/audit-checklist.md` (CCPA collection limits,
  notices, requests, contracts, security, and the cybersecurity-audit, risk-
  assessment and ADMT controls).

### 7.4 Report

Produce findings in the audit finding format (criteria, condition, evidence, cause,
effect, recommendation, management response), stating the **stage** for each; a
**control matrix** with a rating per control; an **evidence index**; and an
**overall opinion** (Reasonable assurance / Qualified / Adverse / Insufficient
evidence). Where the audit is pre-implementation, make clear that assurance is over
requirements and design only. Start from `assets/audit-report-template.md`; the
method and rating scales are in `references/audit.md`.

## 8. Bundled references

**Method and templates**

- `references/audit.md` — audit methodology, ratings, findings and report structure.
- `references/legislation-status.md` — last-checked/updated dates per instrument.
- `assets/audit-report-template.md` — fill-in audit report.
- `assets/privacy-policy-template.md` — fill-in policy template mapped to APP 1.4
  and GDPR Art 13/14.

**Australia** — see `references/australia/README.md` for orientation.

- `scope.md` — coverage, definitions, exemptions and permitted situations.
- `apps.md` — APP 1 to APP 13 clause-by-clause checklist.
- `privacy-policy.md` — APP privacy policy requirements and drafting checklist.
- `audit-checklist.md` — control-by-control audit procedures and evidence map.
- `breach-notification.md` — Part IIIC eligible data breaches.
- `statutory-tort.md` — Schedule 2 serious invasions of privacy.

**European Union**

- `references/eu/gdpr.md` — principles, lawful bases, rights, obligations, transfers, fines.
- `references/eu/privacy-notice.md` — GDPR Art 12–14 notice content and checklist.
- `references/eu/audit-checklist.md` — GDPR/AI Act/Data Act audit procedures.
- `references/eu/ai-act.md` — prohibitions, high-risk classification, requirements, transparency, GPAI.
- `references/eu/data-act.md` — data access/sharing, cloud switching, government access.

**USA / California** — see `references/usa/README.md` for orientation.

- `references/usa/ccpa.md` — CCPA obligations: collection limits, rights, notices,
  contracts, security, ADMT, cybersecurity audits, risk assessments, enforcement.
- `references/usa/privacy-policy.md` — required CCPA disclosures and policy content.
- `references/usa/audit-checklist.md` — CCPA control-by-control audit procedures.

## 9. Caveats

- This package ships summaries and citations, not the full statutes. Official texts:
  Australian Privacy Act 1988 compilation No. 104 (4 June 2026) —
  [legislation.gov.au](https://www.legislation.gov.au/C2004A03712/latest/text);
  GDPR — [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2016/679/oj); AI Act —
  [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/oj); Data Act —
  [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2023/2854/oj); CCPA and CCPA
  Regulations (effective 1 January 2026) — [CCPA statute](https://leginfo.legislature.ca.gov/faces/codes_displayText.xhtml?lawCode=CIV&division=3.&title=1.81.5.&part=4.)
  and [CPPA regulations](https://cppa.ca.gov/regulations/). Verify currency against
  the official register before relying on a citation in a high-stakes context.
- Each regime sits alongside others (e.g. Australian credit reporting and APP codes;
  the ePrivacy Directive, DMA, DSA, NIS2; other US state privacy laws; national
  Member State law). Note overlaps; this skill is not exhaustive.
- This skill is portable across agents that support the Agent Skills `SKILL.md`
  format (Claude, Codex, and others).
