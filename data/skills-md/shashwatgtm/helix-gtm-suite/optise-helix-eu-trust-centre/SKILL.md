---
name: optise-helix-eu-trust-centre
description: >
  Write or audit a Trust Centre page that answers the 8 questions European
  buyers ask before they buy: GDPR compliance, data storage, residency, DPA,
  subprocessors, data collection and retention, third-party AI providers and
  security standards. Produces the full page in an extractable format with a
  BLUF, answer blocks, JSON-LD schema and a DPA request call to action. Use
  whenever the user needs to draft, audit, or expand a Trust Centre page, trust
  portal, GDPR FAQ, security centre, or any page answering EU compliance
  questions. Never invents data residency, certifications, or subprocessors.
  Method: Optise answer ordering (Q1, Q2, Q3, Q8, Q4, Q5, Q6, Q7) for European
  procurement reviews. Authored by Optise + Helix GTM Consulting.
license: Proprietary
metadata:
  authors: "Optise; Helix GTM Consulting"
  version: "1.4.0"
---

# Optise–Helix EU Trust Centre Generator

Generates a complete EU Trust Centre page that answers all 8 canonical EU buyer questions in procurement-optimized order, with JSON-LD FAQPage schema and a DPA request CTA.

This is the European differentiator skill. EU B2B buyers evaluate compliance before anything else — a company without a findable, extractable Trust Centre is functionally invisible to EU procurement processes even if it's technically compliant. This skill turns compliance facts into citable, AI-engine-readable content.

The 8 questions come from the Optise EU AEO Playbook, Section 7 (page 12). The output order (Q1→Q2→Q3→Q8→Q4→Q5→Q6→Q7) is proprietary — it optimizes for the filter-then-verify flow EU security reviewers actually use.

---


## Section 0 — Operating Principles (MANDATORY — read before any workflow step)

This skill operates under TWO mandatory reference files that together define all operating rules. **Read both files first**, before executing any workflow step in this SKILL.md. The rules in both files are non-negotiable and override any conflicting instruction in this SKILL.md body.

1. **`references/operating-principles.md`** — the shared core: Rule 0 to Rule 10 (session hygiene, URL verification, source-tier discipline, code-content verification, Schema.org currency, legal-citation accuracy, verify-before-recommend, prediction discipline, claim tagging, verification order, verification log), plus the mandatory output disclaimer. They apply to every skill in this plugin.

2. **`references/plugin-specific-rules.md`** — the plugin-specific tail: additional operational rules tailored to the skills in THIS plugin. Read this file AFTER the shared core, not instead of it. If this plugin currently has no plugin-specific rules, the file will be a stub explaining the architecture.

### Critical reminders that apply to every invocation of this skill

These are the highest-frequency rules from the two files above. Reading the full files is still mandatory — these reminders are a quick-reference, not a substitute.

- **Web search and web fetch ARE available** in Claude Code's default toolset. "I don't have web access" is never a valid excuse to skip verification of a specific factual claim.
- **English-only at v1** — never generate prompts, copy, headings, or client-facing text in non-English languages (German, French, Dutch, Spanish, Italian, Portuguese, Polish, etc.), even on explicit user request. This is a hard block, not a confirmation gate. Refuse the request and explain that multilingual may ship in v2 with native-speaker review.
- **4-tier source hierarchy applies to all factual claims.** Tier 1: official primary sources (press releases, Crunchbase, Wikipedia, SEC filings). Tier 2: reputable analyst firms (Gartner, Forrester, IDC, G2, Capterra, GigaOm, SoftwareReviews). Tier 3: reputable business and trade press (WSJ, FT, Reuters, Bloomberg, HBR, TechCrunch, named-VC content, named-founder blogs). Tier 4: use only with the mandatory disclaimer `[Tier 4 — directional only, not authoritative]` (random blogs, anonymous posts, AI-generated comparison sites, Forbes Contributor, paid placements, vendor reseller content), as operating-principles Rule 2 requires. If only Tier 4 sources are available, the claim is unverified and MUST be flagged.
- **Verify competitor relationships** before building ANY competitor-targeted page or content (operating-principles Rule 9, step 2, and Plugin Rule 1 in `plugin-specific-rules.md`). Run: `"[user] acquired [competitor]"`, `"[competitor] acquired by"`, `"[competitor] Crunchbase acquisition"`, `"[user] vs [competitor]"`. Any positive ownership hit is a HARD STOP under Plugin Rule 1 (no harmful output about named companies).
- **Auto-verify URLs** via `web_fetch` before marking them `[EXISTS]`. Only ask the user about URLs when fetch returns an ambiguous result (403, 429, 500, timeout, redirect loop). Do not ask the user about every URL; that is endless interrogation, not verification.
- **Question Budget: maximum 3 HARD STOP questions per invocation, consolidated into ONE message.** Never run an endless Q&A sequence. If more than 3 HARD STOPs exist, pick the top 3 by priority (harm triggers → irreversible scope → reversible details) and defer the rest to `Assumption:` flags in the output.
- **Flag every assumption** with an explicit `Assumption:` prefix in the output so users can correct anything the skill got wrong. Use the `[User to add: <description>]` placeholder convention for any field where the user must supply specific information.

### Conflict resolution

If a domain rule in Section 7 of this SKILL.md (or any other section) appears to conflict with a rule in `operating-principles.md` or `plugin-specific-rules.md`, the operating principles win. Domain rules MAY add specific enforcement for a skill's particular failure modes, but they MUST NOT weaken the operating principles. When in doubt, escalate the conflict to the user as a HARD STOP question rather than silently picking one interpretation.

---

## Section 1 — Golden Rule

**Never invent the user's compliance data. If the user doesn't know their data residency, subprocessor list, AI provider stack, or security certifications, use `[User to add: ...]` placeholders. Getting this wrong gets companies sued — placeholders are never the wrong answer; invented facts always are.**

---

## Section 2 — Role / Context Detection

Detect persona using `references/personas.md`. Adapt output:

| Persona | Output adaptation |
|---|---|
| **CEO / Founder** | Generate the page. Close with a CFO-grade ask. State a cost of not publishing only if the user supplies pipeline data; never estimate it (operating-principles Rule 7). |
| **Marketing / Growth Lead (default)** | Full page + JSON-LD schema + section-by-section copy + DPA CTA + handoff note. |
| **Web Team** | Full page as HTML file with JSON-LD in `<head>`. Skip marketing framing. Ready to paste into CMS. |
| **RevOps / Sales Ops** | Add a "what to log in CRM when a buyer hits this page" section with suggested UTM parameters and lead scoring impact. |
| **Security / Privacy / Legal (primary audience)** | Lead with legal precision. Flag every assumption. Add "what your DPO should verify before publishing." Highest fidelity output. |

**Detection signals:** see `references/personas.md`. Default for this skill is Security/Privacy/Legal or Marketing depending on context (unlike other skills where default is Marketing only).

**Platform mode:**
- **Connected:** use memory for prior Trust Centre drafts; offer to extend rather than regenerate
- **Manual / API:** JSON in (company facts), JSON out (page content + schema)
- **Mixed:** ask for missing fields only

**Urgency:** "Quick" → output only the 4 highest-priority questions (Q1, Q2, Q3, Q8) in abbreviated form. Time-stamped.

---

## Section 3 — Priority Framework

**Question priority order** (NOT the sequential order — this is what to fill first if the user has incomplete data):

1. **Q1 (GDPR compliance)** — Must answer. If "no" or "unsure", halt and ask user to confirm before writing.
2. **Q2 (Where is data stored)** — Must answer. If unknown, use `[User to add: exact region]` — never assume EU.
3. **Q8 (Security standards)** — Highest-frequency follow-up question from EU procurement. Answer even if certifications are in-progress.
4. **Q3 (EU data residency)** — Distinct from Q2. Q2 is where data IS, Q3 is what OPTIONS the buyer has.
5. **Q4 (DPA availability)** — Near-universal requirement. If no DPA exists yet, flag as P0.
6. **Q5 (Subprocessors)** — Publishing the list is the #1 trust signal for DACH Mittelstand buyers.
7. **Q6 (Data collection and retention)** — Important but lower procurement-priority than Q1-Q5.
8. **Q7 (Third-party AI providers)** — Growing in importance as EU AI Act obligations phase in (many apply from August 2026; verify exact dates per Rule 5).

**Tie-breakers:**
1. **EU AI Act matters more in 2026.** As more EU AI Act obligations apply from August 2026, elevate Q7 from "lower priority" to "medium priority."
2. **Regulated verticals change the order.** Health-tech adds BfArM/DiGA as Q8-adjacent. Fin-tech adds DORA as Q8-adjacent.
3. **Never skip a question.** Even if the answer is "not applicable" or "we don't use third-party AI", the question must be present so procurement reviewers see a complete list.

---

## Section 4 — Workflow Steps

### Step 0: Detect mode

- **New page** (default) — generate a fresh Trust Centre from user-provided facts
- **Section-only** — generate one specific section (e.g., just the DPA question)
- **Audit existing** — user has a published Trust Centre URL → hand off to `optise-helix-fitq-audit` with a custom prompt: *"Audit this URL for FITq, but specifically check whether each of the 8 EU buyer questions from `references/eu-buyer-questions.md` has a visible, extractable answer. For any question that's missing or weak, output the question number and the gap. Do not write new content — flag gaps only."* When FITq returns results, this skill reads the gap list and offers to generate replacement sections for any gaps.

### Step 1: Capture inputs

**Required (minimum):**
- Company name
- GDPR compliance status (yes/no/in-progress)
- Data residency (exact region — not "EU", the specific AWS/GCP/Azure region or data center city)
- DPA availability (available / in development / negotiable for enterprise only)

**Optional but preferred:**
- Subprocessor list (or link to live page)
- Security certifications (SOC 2, ISO 27001, BSI C5, etc. — with status: certified / in-progress / planned)
- Third-party AI providers and data flow
- Data retention periods
- Named DPO or Security Officer
- EU market focus (to prioritize DACH / Nordic / France-specific trust signals)

**Failure mode:** If fewer than 4 required inputs provided → ask once, listing all 4 required fields. Don't proceed with partial required inputs.

### Step 2: Detect persona

Use `references/personas.md`. Default is Security/Privacy/Legal for this skill (not Marketing) when signal is ambiguous.

### Step 3: Load the 8 EU buyer questions from reference

Read `references/eu-buyer-questions.md`. Apply the Answer Assembly Rule ordering (Q1→Q2→Q3→Q8→Q4→Q5→Q6→Q7).

### Step 4: Write the page BLUF (40-60 words)

Use Pattern 6 (Compliance Anchor) from the BLUF writer rules. The BLUF must:
- Name the GDPR compliance status
- Name the data residency region(s)
- Name the DPA availability
- Name 1-2 security certifications
- Link to full page answers

**Example BLUF structure (every fact comes from the user or stays a placeholder):**
> [Company name] is [User to add: GDPR status] with [User to add: certifications and their exact status]. Customer data is stored in [User to add: exact region(s)]. Our Data Processing Agreement is [User to add: how to get it], and our [User to add: number] subprocessors are published at [User to add: link] [User to add: change-notice policy, if any].

### Step 5: Write each of the 8 question sections

For each question, use the template from `references/eu-buyer-questions.md`. Each section:
- Question as H2 heading (question-form, verbatim)
- 1-sentence direct answer
- 3-5 sentence plain-language expansion
- "Where to verify" links
- `[User to add: ...]` placeholders for any missing facts

**Failure mode:** If any required fact is missing, insert the placeholder rather than inventing. Never fill in "EU" when region is unknown. Never claim certifications that aren't actually held.

### Step 6: Generate JSON-LD FAQPage schema

Build a JSON-LD block with all 8 Q&A pairs. Each Answer's `text` field mirrors the visible 1-sentence direct answer from Step 5. Apply operating-principles Rule 4: FAQPage is not eligible for Google rich results on corporate compliance pages, so either use `Organization` + `hasCredential` + `WebPage`, or keep FAQPage for other AI parsers with the Rule 4 disclosure note.

### Step 7: Add DPA CTA block

Two options depending on user input:
- **Self-serve DPA download available:** *"Download our DPA: [link]. [User to add: signing steps, for example pre-signed and needing only your countersignature, only if the user confirms]"*
- **DPA requires request:** *"Email [User to add: DPA email] to request a DPA. [User to add: turnaround time, only if the user states one]"*

### Step 8: Add the "what your DPO should verify" section (Security persona) or skip (other personas)

For Security persona output only, add a pre-publish verification checklist:
- Data residency matches current infrastructure
- Subprocessor list is complete and current
- Certification statuses are current (not expired)
- DPA link resolves
- DPO contact is correct
- AI provider data flows are accurate

### Step 9: Format output per persona

Use Section 5 format.

### Step 10: Hand off

- If user wants to audit the published Trust Centre page for AEO visibility → `optise-helix-fitq-audit`
- If user wants prompts that will cite this Trust Centre → `optise-helix-prompt-pack-builder`
- If user needs a BLUF for a different page → `optise-helix-bluf-writer`

---

## Section 5 — Output Format (with Concrete Examples)

### Standard format (Marketing persona, default)

```markdown
**Built for:** [persona]
**Company:** [name]
**Inputs used:** [summary of provided facts]
**Inputs missing:** [list of fields where placeholders were inserted]

---

## Trust & Compliance

[BLUF - 40-60 words]

### Is [Company] GDPR compliant?
[1-sentence answer]
[3-5 sentence expansion]
**Where to verify:** [links]

### Is customer data stored in the EU?
[same format]

### Does [Company] offer EU data residency?
[same format]

### What security standards does [Company] meet?
[same format — note: Q8 moved up per Answer Assembly Rule]

### Can I get a DPA for [Company]?
[same format]

### Who are [Company]'s subprocessors?
[same format with subprocessor table]

### What data does [Company] collect and how long is it retained?
[same format with retention table]

### Does [Company] use third-party AI providers?
[same format]

---

**Need a DPA now?** [CTA block]

---

## JSON-LD FAQPage schema (for <head> or inline)

```json
{...}
```

## Suggested next step
[Handoff]
```

### Example 1: Happy path (Marketing lead, partial data, real company: Pipedrive)

*Example only: Pipedrive is a real company used to show how this skill works, using public information from its own website. It is not a customer, partner or endorser of Helix GTM Consulting, and nothing here is advice to or about it.*

> **Built for:** Marketing / Growth Lead
> **Company:** Pipedrive
> **Inputs used:** GDPR and ISO/IEC 27001:2022 are listed under Compliance on the company's own Trust Center (stated by user, source https://trustcenter.pipedrive.com/, read on 3 October 2026)
> **Inputs missing:** SOC 2 status, controller or processor role, data residency region, DPA availability and route, subprocessors and change-notice policy, AI providers, retention periods, DPO contact
>
> ---
>
> ## Trust & Compliance
>
> Pipedrive's Trust Center lists GDPR and ISO/IEC 27001:2022 under Compliance. Customer data is stored in [User to add: specific AWS/GCP/Azure region; do not publish "EU" without the exact region]. Our Data Processing Agreement is [User to add: availability and how to request it]. [User to add: where the subprocessor list and retention policy are published].
>
> ### Is Pipedrive GDPR compliant?
>
> Pipedrive's Trust Center lists GDPR under Compliance. Pipedrive acts as [User to add: Data Processor, Data Controller, or both] under EU Regulation 2016/679.
>
> [User to add: which GDPR obligations to describe, for example processor obligations (Article 28), records of processing (Article 30), security of processing (Article 32), breach notification to the supervisory authority (Article 33), and whether a record of processing activities is maintained]. [User to add: name and contact of your DPO or Privacy Lead].
>
> **Where to verify:** [User to add: link to DPA page] · [User to add: link to GDPR FAQ]
>
> ### Is customer data stored in the EU?
>
> `[User to add: direct answer: YES with exact region, or NO/partial with explanation. Do not leave this blank. Do not write "EU" without the specific region.]`
>
> `[User to add: 3-5 sentence expansion describing the primary and backup regions, whether data leaves those regions for any operations, and who makes the decision if region changes.]`
>
> **Where to verify:** `[User to add: link to data residency page]`
>
> ### Does Pipedrive offer EU data residency?
>
> `[User to add: YES/NO/on specific plans, with the plan name and how to request it]`
>
> `[User to add: expansion describing what data stays in the region, any exceptions for support/analytics/AI processing, and who the customer notifies to elect residency]`
>
> **Where to verify:** `[User to add: link]`
>
> ### What security standards does Pipedrive meet?
>
> Pipedrive's Trust Center lists ISO/IEC 27001:2022 under Compliance.
>
> | Standard | Status | Verification |
> |---|---|---|
> | SOC 2 Type 2 | `[User to add: status]` | `[User to add: evidence]` |
> | ISO 27001 | Listed as ISO/IEC 27001:2022 on the Trust Center (stated by user) | https://trustcenter.pipedrive.com/ |
> | GDPR | Listed on the Trust Center (stated by user) | `[User to add: evidence, for example DPA]` |
> | EU AI Act | `[User to add: status and risk category, or "not applicable"]` | `[User to add: evidence]` |
>
> `[User to add: penetration testing frequency and vendor, incident notification commitment, security team contact]`
>
> ### Can I get a DPA for Pipedrive?
>
> `[User to add: Yes / No / Enterprise only; how to get it; whether it incorporates the EU SCCs; pre-signed or signed by both parties; turnaround time for standard and negotiated versions]`
>
> **Where to verify:** `[User to add: DPA request email or link]`
>
> ### Who are Pipedrive's subprocessors?
>
> `[User to add: full subprocessor table with: Subprocessor | Service | Data type processed | Region]`
>
> **Example row format:**
>
> | Subprocessor | Service | Data type | Region |
> |---|---|---|---|
> | [name] | [hosting/email/billing/LLM] | [customer content/metadata/anonymous] | [region] |
>
> `[User to add: how and how far in advance customers are notified of new subprocessors, or "no notice commitment"]`
>
> **Where to verify:** `[User to add: link to live subprocessor page]`
>
> ### What data does Pipedrive collect and how long is it retained?
>
> `[User to add: retention table covering account info, usage telemetry, customer content, support tickets, with purpose and retention period per row]`
>
> ### Does Pipedrive use third-party AI providers?
>
> `[User to add: YES/NO, which providers, what data flows to them, customer content scope, opt-out mechanism]`
>
> ---
>
> **Need a DPA now?** `[User to add: DPA request route and turnaround, only as the user states them]`
>
> ---
>
> ## JSON-LD schema
>
> [Rule 4 note: FAQPage is no longer eligible for Google rich results on corporate compliance pages. Included for AI parsers that read FAQ markup. For Google eligibility, use `Organization` + `hasCredential` + `WebPage` instead.]
>
> ```json
> {
>   "@context": "https://schema.org",
>   "@type": "FAQPage",
>   "mainEntity": [
>     {
>       "@type": "Question",
>       "name": "Is Pipedrive GDPR compliant?",
>       "acceptedAnswer": {
>         "@type": "Answer",
>         "text": "Pipedrive's Trust Center lists GDPR under Compliance."
>       }
>     },
>     {
>       "@type": "Question",
>       "name": "Is customer data stored in the EU?",
>       "acceptedAnswer": {
>         "@type": "Answer",
>         "text": "[User to add: direct answer with exact region before publishing this schema]"
>       }
>     }
>     // ... 6 more Q&A pairs for Q3-Q7
>   ]
> }
> ```
>
> ## ⚠️ Before publishing
>
> This draft still contains `[User to add: ...]` placeholders covering the controller or processor role, data residency, DPA, subprocessors, retention, AI providers, and security details. **Do not publish with placeholders visible.** Fill in each one with real facts from your infrastructure, legal, and security teams, or delay publishing until the facts are known. Publishing a Trust Centre with unfilled placeholders is worse than not publishing one at all (EU buyers will assume you're hiding something).
>
> ## Suggested next step
> Gather the missing facts from Engineering, Legal, and Security. Once complete, re-run this skill with the full input set, or run `optise-helix-fitq-audit` on the published page to verify it scores well on FITq Trust signal.

### Example 2 — Edge case (user wants just the DPA section)

> **Section-only mode:** Q4 (DPA availability) only.
>
> ### Can I get a DPA for [Company]?
>
> **Inputs used (stated by user):** DPA available to all customers before contract execution; pre-signed; incorporates the 2021 EU SCCs; covers Annex II and Annex III; negotiated DPAs for enterprise.
>
> Yes. Our Data Processing Agreement is available to all customers and can be signed before contract execution.
>
> The [Company] DPA incorporates the EU Standard Contractual Clauses (SCCs) where data transfers outside the EU are involved. It is pre-signed by [Company] and only requires the customer's countersignature. The DPA covers processing instructions, security measures (Annex II), subprocessor list (Annex III), and data subject rights handling. Negotiated DPAs are available for [User to add: enterprise tier].
>
> **Where to verify / how to get it:** Email [User to add: DPA email] OR [link to self-serve DPA download page].
>
> ## Partial JSON-LD (FAQPage fragment for just Q4)
>
> ```json
> {
>   "@context": "https://schema.org",
>   "@type": "Question",
>   "name": "Can I get a DPA for [Company]?",
>   "acceptedAnswer": {
>     "@type": "Answer",
>     "text": "Yes. Our Data Processing Agreement incorporates EU SCCs and is pre-signed. Countersign and return to activate."
>   }
> }
> ```

### Example 3 — CEO persona, hypothetical complete input

> **Built for:** CEO / Founder
> **Company:** [Company name]
>
> ## Trust Centre page — ready to ship
>
> [Full page content, generated from all provided facts]
>
> **Your CFO-grade ask:** Publishing this page is mostly formatting work for the CMS. EU procurement reviewers check compliance answers early, so a missing Trust Centre can stop deals at that checkpoint. [User to add: pipeline data if you want an estimate of the cost of not publishing; the skill does not estimate it without data (Rule 7).]

### Example 4 — Manual / JSON mode (real company: Pipedrive)

*Example only: Pipedrive is a real company used to show how this skill works, using public information from its own website. It is not a customer, partner or endorser of Helix GTM Consulting, and nothing here is advice to or about it.*

The inputs below are copied from the company's own public pages (https://trustcenter.pipedrive.com/ and https://www.pipedrive.com/en/subprocessors, read on 3 October 2026). Everything the user did not state stays a placeholder.

**Input:**
```json
{
  "company_name": "Pipedrive",
  "gdpr_status": "listed under Compliance on the Trust Center",
  "data_residency": "[User to add: exact region(s)]",
  "dpa": {"available": "[User to add]", "mechanism": "[User to add]", "url": "[User to add]"},
  "certifications": ["GDPR (listed)", "ISO/IEC 27001:2022 (listed)", "SOC 2 Type 2 (listed)"],
  "ai_providers": [{"provider": "[AI provider]", "via": "[endpoint and region]", "data_flow": "[User to add]"}],
  "dpo_contact": "[User to add]",
  "subprocessor_page_url": "https://www.pipedrive.com/en/subprocessors",
  "mode": "manual"
}
```

**Output:**
```json
{
  "page_title": "Trust & Compliance: Pipedrive",
  "bluf": "Pipedrive's Trust Center lists GDPR, ISO/IEC 27001:2022 and SOC 2 Type 2 under Compliance, and its sub-processors are listed at pipedrive.com/en/subprocessors. Customer data is stored in [User to add: exact region(s)]. Our Data Processing Agreement is [User to add: how to get it]. [User to add: DPO contact].",
  "sections": [
    {"question": "Is Pipedrive GDPR compliant?", "answer": "..."},
    {"question": "Is customer data stored in the EU?", "answer": "[User to add: direct answer with exact region]"}
    // ... all 8 sections
  ],
  "json_ld_schema": {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": []
  },
  "schema_note": "Rule 4: FAQPage is not eligible for Google rich results on this page type; use Organization + hasCredential + WebPage for Google.",
  "dpa_cta": {
    "type": "request",
    "text": "[User to add: DPA request route and turnaround, only as the user states them]",
    "url": null
  },
  "placeholders_remaining": ["data residency region", "DPA availability and route", "DPO contact", "subprocessor change-notice policy", "retention periods", "AI providers"],
  "generated_at": "2026-04-12T12:55:00Z"
}
```

---

## Section 6 — Edge Case Handling

### Universal
- **First-time user:** 3-sentence intro explaining what an EU Trust Centre is. Offer to generate.
- **Returning user:** Check memory for prior draft. Offer to extend/update.
- **Rushed user:** Output only Q1, Q2, Q3, Q8 (the "filter questions"). Flag Q4-Q7 as pending. Time-stamp.
- **Frustrated user (prior version was wrong):** Ask what was wrong — fact, tone, structure? Rewrite addressing that.
- **Out-of-scope:** If user asks for a privacy policy (different document), decline and refer to a legal tool.
- **Multilingual request:** Decline per project rule (English-only at v1). Reply: *"v1 is English-only across all EU markets. A German/French/Spanish Trust Centre needs native legal review — I can't guarantee legal precision in translation. Publish the English version, then have local counsel translate and review before localizing. Multilingual ships in v2 if there's demand."*

### Data
- **Full data (all 4 required + most optional):** Highest quality output.
- **4 required only:** Generate page with placeholders for all optional fields. Flag which are missing.
- **Fewer than 4 required:** Ask once for all missing required fields.
- **"We're EU-hosted" (vague):** Push back once for the specific region.
- **US-hosted:** Write honestly. Never fake EU residency.
- **Conflicting data:** Flag the conflict ("You said Frankfurt earlier, but the subprocessor list shows us-east-1. Which is accurate?"). When user input conflicts with memory (e.g., user now says "SOC 2 certified" but memory says "SOC 2 in progress"), confirm the current status before generating — never silently overwrite.
- **Stale data (memory from >3 months ago):** Confirm before using.

### Platform
- **Connected mode:** Use memory for prior drafts.
- **Manual / API:** JSON in, JSON out.
- **Mixed mode:** Use memory where available, ask for missing fields.

### Context
- **Normal:** Full 8-question page.
- **Crisis / urgent:** 4 filter questions only.
- **Regulated vertical (health-tech, fin-tech):** Add vertical-specific supplementary questions (BfArM/DiGA/MDR for health; DORA/MiCA/PSD2 for fin-tech).
- **Startup pre-certification:** Write the page with "in progress" status on certifications. Don't hide that they're incomplete — honesty is the signal.
- **Enterprise with existing Trust Centre:** Offer to audit the existing one instead of regenerating.

### Composition rules
- **Rushed + No data residency:** Halt. Ask for residency first. "Rushed mode can't bypass the #1 question."
- **CEO + Missing data:** Generate with placeholders. Close with "delay publishing until all placeholders are filled — a half-done Trust Centre is worse than none."
- **Security + Manual mode:** Structured JSON output with a `dpo_verification_checklist` field added.
- **Regulated vertical + Rushed:** Output the 4 filter questions + 1 vertical-specific question (the most critical for that vertical). Flag the rest as pending.
- **Manual mode + any persona:** Manual wins.
- **Rushed + Regulated vertical + Partial data:** HALT if Q1 (GDPR) or Q2 (residency) is missing — these cannot be bypassed even in rushed mode for regulated verticals. If Q1 and Q2 are present but other fields are missing, generate the 4 filter questions (Q1/Q2/Q3/Q8) plus 1 vertical-specific question (BfArM for health, DORA for fin-tech). Flag all remaining as pending. Liability is too high to skip compliance questions in rushed mode for regulated verticals.

---

## Section 7 — Anti-Hallucination Rules

All 9 base rules from `references/anti-hallucination-base.md` apply. Additionally:

**Domain rule 1:** Never assume EU data residency. The moment the user says "EU-hosted" without specifying the region, push back. Writing "data stored in EU" when the real location is AWS us-east-1 gets companies sued for misrepresentation to EU customers.

**Domain rule 2:** Never invent subprocessor names. If the user doesn't provide a list, use the template with `[User to add: ...]` placeholders in every row.

**Domain rule 3:** Never claim certifications the user hasn't verified. "SOC 2 Type II certified" and "SOC 2 Type II in progress" are legally distinct claims — use exactly what the user says.

**Domain rule 4:** Never fabricate a DPO name or contact. If the user doesn't name one, use `[User to add: DPO name and contact]`.

**Domain rule 5:** Never write an EU AI Act compliance claim without a user-provided risk classification. The Act has specific categories (minimal / limited / high / unacceptable risk) — claiming "compliant" without knowing your category is a legal risk.

**Domain rule 6:** Never publish placeholders. If the output contains `[User to add: ...]` strings, the final output must include the pre-publish warning from Example 1 ("Do not publish with placeholders visible").

**Domain rule 8:** Never let an example or template sentence become a claim. Worked examples in this file name one real company (Pipedrive) and use only what its own public pages say, with the source address; every compliance fact in the output must come from the user in this session or stay a `[User to add: ...]` placeholder.

**Domain rule 7:** Never translate legal language to other EU languages. The project rule is English-only at v1. Legal translations require native legal review.

---

## Section 8 — Trigger Phrases

### Explicit triggers
- "generate a Trust Centre page"
- "write my EU Trust Centre"
- "answer the 8 EU buyer questions"
- "GDPR FAQ page"
- "DPA page"
- "subprocessor disclosure page"
- "compliance FAQ"
- "Optise Trust Centre"
- "EU compliance page"

### Contextual triggers
- User mentions GDPR, DPA, subprocessors, or data residency AND asks for page content
- User has just run FITq audit that flagged Trust < 15 on an EU market page
- User has just run prompt-pack-builder with 4+ Cat 4 (EU Privacy) prompts
- User mentions selling into EU AND asks about compliance pages
- User in a regulated vertical asking about compliance

### Do NOT trigger when
- User wants a full privacy policy (different doc type)
- User wants a Terms of Service
- User wants security whitepaper (longer-form, different format)
- User wants a single BLUF → defer to `optise-helix-bluf-writer`
- User wants to audit an existing page → defer to `optise-helix-fitq-audit`

### Handoff to other skills
- User wants prompts that will cite this Trust Centre → `optise-helix-prompt-pack-builder`
- User wants the published page audited → `optise-helix-fitq-audit`
- User wants agent-readiness check on the Trust Centre → `optise-helix-race-audit`
- User wants to track whether the Trust Centre gets cited → `optise-helix-aeo-tracker`
