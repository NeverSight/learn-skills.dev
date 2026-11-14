---
name: india-privacy-policy
description: Drafts complete, lawful privacy policies and standalone DPDP consent notices for websites, apps and businesses serving users in India, under the Digital Personal Data Protection Act 2023 and DPDP Rules 2025, plus the interim IT Act s.43A / SPDI Rules 2011, IT Intermediary Rules 2021, CERT-In directions, e-commerce rules and sector overlays. Use when asked to write, review, update or audit a privacy policy, privacy notice, consent notice, cookie policy, grievance/data-rights page, or DPDP compliance copy for an Indian product.
license: MIT
metadata:
  author: lokesh-azad
  version: "1.0.0"
  jurisdiction: India
  law_last_checked: "2026-11-14"
---

# India Privacy Policy

Produce a privacy policy package that is accurate to the product, consistent with Indian law, and written in plain language. You are drafting, not giving legal advice: always say so in the handoff.

## 1. Check legal status first (never skip)

The law is phasing in and details move. Before drafting:

1. If web search is available, verify the points below against official sources (MeitY, egazette.gov.in, PIB) and note the date you checked. If not, say your knowledge may be outdated.
   - Has Rule 1 of the DPDP Rules been amended to change the dates?
   - Has the Government notified startup exemptions (s.17(3)), Significant Data Fiduciaries, or restricted countries for transfers (s.16)?
2. Pick the regime phase. Baseline as last checked (14 Nov 2025 notification, G.S.R. 846(E)):

| Phase | What applies |
|---|---|
| Now, until DPDP substantive duties start (baseline 13 May 2027) | IT Act s.43A and SPDI Rules 2011 (privacy policy, written consent for sensitive data, grievance officer), IT Intermediary Rules 2021, Consumer Protection (E-Commerce) Rules 2020, CERT-In Directions 2022, sector rules |
| From that date | DPDP Act ss.5-16 and Rules 3, 5-16, 22-23: notice, consent, security, breach reporting, erasure, rights, children. s.43A and SPDI Rules fall away when DPDP s.44(2) commences |
| Consent Manager provisions (Rule 4) | 13 Nov 2026 onward; optional for fiduciaries |

3. Default recommendation: draft a **DPDP-ready** policy now. It satisfies the interim rules and avoids a rewrite. Set an effective date and keep a version history.

Details, section references and penalties: `references/legal-framework.md`.

## 2. Gather facts

Never invent facts about the business. Fill what you can from the repo, then ask the user once, in one batch, for the rest (`references/intake-questionnaire.md`).

If you have code access, scan for real data flows instead of guessing:

- Dependencies and scripts: analytics (gtag, GA4, Mixpanel, PostHog, Clarity, Hotjar), error tracking (Sentry), auth (Firebase, Auth0, Clerk, Supabase), payments (Razorpay, Stripe, PayU, Cashfree), messaging (Twilio, MSG91, WhatsApp API), ads pixels (Meta, Google Ads), maps, AI APIs, CDN and hosting regions.
- Forms and models: every field collected (name, phone, email, address, DOB, Aadhaar/PAN, location, photos, health data), cookies and localStorage keys, file uploads, server logs.

Output a data inventory table first and have the user confirm it.

## 3. Classify

Decide and state each of these in your assumptions list:

- Role: Data Fiduciary, Data Processor, or both. A pure service provider processing a client's data is a processor: draft a short processor notice and point to the client's policy, not a full fiduciary policy.
- Children (under 18) likely users? Triggers verifiable parental consent and bans tracking, behavioural monitoring and targeted ads aimed at children.
- Sensitive categories (passwords, financial, health, biometrics, sexual orientation under SPDI; also anything high-risk).
- Scale: possible Significant Data Fiduciary, or the e-commerce/gaming/social thresholds in Rule 8 (Third Schedule).
- Cross-border flows (cloud region, SaaS tools, support tools, AI APIs).
- Sector overlays (fintech, health, edtech, telecom, e-commerce, AI): `references/sector-overlays.md`.
- Audience outside India (EU/UK/US states): out of scope here. Flag it and recommend separate regional addenda.

## 4. Deliverables

Produce these, in this order:

1. **Data inventory**: table of data category, source, purpose, legal basis, recipient, retention.
2. **Privacy Policy**: full public document from `references/policy-template.md`.
3. **Consent Notice (DPDP Rule 3)**: a separate, standalone, itemised notice shown at the point of collection, from `references/consent-notice-template.md`. A privacy policy link alone does not satisfy Rule 3, because the notice must be understandable independently of other information.
4. **Cookie/tracker notice** (if non-essential trackers exist).
5. **Rights and grievance page text** (how to access, correct, erase, nominate, complain; published response period).
6. **Assumptions and open items**: every placeholder, every unverified fact, every legal judgement call.

Use the user's format preference if given (Markdown, Word, HTML page). Default to Markdown.

## 5. Drafting rules

Always:
- Use specific, itemised data and purposes. "To improve our services" is not a purpose. "To send order status SMS" is.
- Separate consent per purpose. Required purposes are described as necessary for the service; optional ones (marketing, analytics, AI training, third-party sharing) get their own unticked choice.
- Give withdrawal a route as easy as giving consent, and say what happens after withdrawal (stop processing, instruct processors, erase unless law requires retention).
- Name a real contact: DPO or person answering for processing (Rule 9), Grievance Officer (SPDI Rule 5(9), IT Rules 2021, E-Commerce Rules), publish the grievance response period (Rule 14, max 90 days), and explain the Data Protection Board route after the grievance route is exhausted (s.13).
- State retention per category in concrete terms, including legal minimums (logs: CERT-In 180 days, DPDP Rule 6/8 one year).
- Offer English plus Eighth Schedule languages for the notice (s.5(3), s.6(3)). Provide a Hindi version only if asked, labelled for native-speaker review.
- Use `{{PLACEHOLDER}}` for anything unknown: legal name, CIN/LLPIN, address, officer names, emails, retention periods, vendors.

Never:
- Write "by using this site you consent" as the consent mechanism, or rely on pre-ticked boxes, bundled consent or dark patterns (see CCPA Dark Patterns Guidelines 2023).
- Claim "fully compliant", "100% secure", "we never share your data" or "we do not sell data" unless the user confirmed it and it is true.
- Promise things the business does not do (encryption, India-only storage, deletion timelines).
- Copy another company's policy text.
- Invent registration numbers, officer names, addresses, or vendor lists.
- Add GDPR/CCPA boilerplate unless the audience requires it.
- Collect or describe processing for children's tracking, behavioural monitoring or targeted advertising.

## 6. Quality check

Before handing over:

1. Run `python3 scripts/check_policy.py <policy.md>`. Fix every FAIL. Review every WARN. Leftover placeholders are expected only if you list them in open items.
2. Walk through `references/compliance-checklist.md`.
3. Confirm the policy matches the data inventory exactly: every vendor and data category appears, nothing extra.

## 7. Handoff message

Keep it short:

- What was produced and where.
- Regime phase assumed and the date law was checked.
- Top open items (placeholders, facts to confirm, decisions for the owner).
- One-line disclaimer: this is a draft, not legal advice. Recommend review by an Indian-qualified lawyer before publishing, especially for health, finance, children's data, or large user bases.

## Reference map

| File | Read when |
|---|---|
| `references/legal-framework.md` | You need section/rule citations, penalties, interim vs DPDP duties |
| `references/policy-template.md` | Writing the Privacy Policy |
| `references/consent-notice-template.md` | Writing the Rule 3 notice and UI copy |
| `references/intake-questionnaire.md` | You must ask the user for facts |
| `references/sector-overlays.md` | Fintech, health, edtech, e-commerce, telecom, AI, employment |
| `references/compliance-checklist.md` | Final QA |
| `scripts/check_policy.py` | Automated structural check |
