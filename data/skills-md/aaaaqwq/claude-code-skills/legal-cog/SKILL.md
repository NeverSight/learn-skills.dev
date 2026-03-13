---
name: legal-cog
description: "Legal demands two things: frontier-level reasoning and precision document generation. CellCog delivers both. #1 on DeepResearch Bench (Feb 2026) for the intelligence that legal work requires, paired with state-of-the-art document generation for contracts, NDAs, terms of service, privacy policies, compliance reviews, and legal research. AI contract generator, legal document drafting, NDA creator, terms of service, privacy policy, compliance, legal AI."
metadata:
  openclaw:
    emoji: "⚖️"
author: CellCog
dependencies: [cellcog]
---

# Legal Cog - AI Legal Documents Powered by CellCog

**Legal demands two things: frontier-level reasoning and precision document generation.** CellCog delivers both.

Legal is the frontier of human intelligence — and it's done best when powered by the frontier of AI intelligence. #1 on DeepResearch Bench (Feb 2026) for the deep reasoning that legal work requires, paired with state-of-the-art PDF generation for documents that look as professional as the thinking behind them.

---

## Prerequisites

This skill requires the `cellcog` skill for SDK setup and API calls.

```bash
clawhub install cellcog
```

**Read the cellcog skill first** for SDK setup. This skill shows you what's possible.

**Quick pattern (v1.0+):**
```python
result = client.create_chat(
    prompt="[your legal document request]",
    notify_session_key="agent:main:main",
    task_label="legal-task",
    chat_mode="agent"
)
```

---

## Important Note

CellCog generates legal documents using frontier AI reasoning and research. However, **AI-generated legal documents should be reviewed by a qualified attorney** before execution — especially for high-value contracts, regulated industries, or jurisdiction-specific requirements. CellCog provides an excellent starting point that saves significant time and cost, but human legal review remains important for critical documents.

---

## What You Can Create

### Contracts & Agreements

Professional contracts with proper clause structure:

- **Freelance Agreements**: "Create a freelance services agreement for a web development project"
- **Employment Contracts**: "Draft an employment contract for a senior engineer in California"
- **Consulting Agreements**: "Create a consulting agreement with milestone-based payments"
- **Partnership Agreements**: "Draft a partnership agreement for a 60/40 equity split startup"
- **Licensing Agreements**: "Create a software licensing agreement for SaaS distribution"

**Example prompt:**
> "Create a freelance contractor agreement:
> 
> Client: Acme Corp (Delaware C-Corp)
> Contractor: Jane Smith (Web Developer, sole proprietor)
> Project: E-commerce website redesign
> Duration: 3 months (March 1 – May 31, 2026)
> Payment: $15,000 (50% upfront, 50% on completion)
> 
> Include: Scope of work, deliverables, payment terms, IP ownership (work-for-hire),
> confidentiality, non-solicitation, termination clauses, dispute resolution (arbitration).
> 
> Professional legal formatting with numbered clauses."

### NDAs & Confidentiality

Protect your information:

- **Mutual NDA**: "Create a mutual NDA between two companies exploring a partnership"
- **Employee NDA**: "Draft an employee confidentiality agreement with non-compete"
- **Investor NDA**: "Create an NDA for sharing financial information with potential investors"
- **Vendor NDA**: "Draft a one-way NDA for a vendor accessing our customer data"

### Terms & Policies

Legal foundations for digital products:

- **Terms of Service**: "Create terms of service for a SaaS platform"
- **Privacy Policy**: "Draft a GDPR and CCPA-compliant privacy policy for a mobile app"
- **Cookie Policy**: "Create a cookie consent policy for a European-facing website"
- **Acceptable Use Policy**: "Draft an acceptable use policy for a community platform"
- **EULA**: "Create an end-user license agreement for desktop software"
- **Return Policy**: "Draft a refund and return policy for an e-commerce store"

**Example prompt:**
> "Create a comprehensive privacy policy for:
> 
> Company: HealthTrack (health & fitness mobile app)
> Data collected: Name, email, health metrics, workout data, location (optional)
> Third parties: Stripe (payments), Firebase (analytics), AWS (hosting)
> Jurisdictions: Must comply with GDPR (EU users), CCPA (California), and HIPAA (health data)
> 
> Include: Data collection, use, storage, sharing, user rights, data deletion, breach notification,
> children's privacy (13+ only), and contact information.
> 
> Professional formatting, clear language (not impenetrable legalese)."

### Legal Research & Compliance

Research-powered legal intelligence:

- **Regulatory Research**: "Research GDPR requirements for AI-powered SaaS products"
- **Compliance Checklists**: "Create a SOC 2 compliance checklist for a startup"
- **Legal Memos**: "Draft a legal memo on intellectual property considerations for AI-generated content"
- **Jurisdiction Analysis**: "Compare contractor vs. employee classification rules across US states"

### Startup Legal Documents

Essential documents for founders:

- **SAFE Notes**: "Create a SAFE note template for a pre-seed round"
- **Founder Agreements**: "Draft a co-founder agreement with vesting schedules"
- **Advisor Agreements**: "Create an advisor agreement with 0.5% equity and 2-year vesting"
- **Board Resolutions**: "Draft a board resolution for approving a new equity plan"

---

## Why CellCog for Legal?

### The Two Pillars

**1. Intelligence** — Legal work requires deep reasoning about context, jurisdiction, edge cases, and implications. CellCog's #1 ranking on DeepResearch Bench means it reasons about legal nuances at a level other AI tools can't match.

**2. Document Generation** — Legal documents need precise formatting, proper clause numbering, consistent terminology, and professional presentation. CellCog's state-of-the-art PDF generation produces documents that look like they came from a top law firm.

| Generic AI | CellCog Legal Cog |
|-----------|-------------------|
| Generic contract templates | Jurisdiction-aware, context-specific drafting |
| Basic text output | Professional PDF with proper legal formatting |
| Surface-level clauses | Deep reasoning about edge cases and implications |
| One format | Contracts, policies, memos, research — all from one platform |

---

## Chat Mode for Legal

| Scenario | Recommended Mode |
|----------|------------------|
| Single contract, NDA, or policy | `"agent"` |
| Complex multi-document legal packages | `"agent"` |
| Deep regulatory research or compliance analysis | `"agent team"` |

**Use `"agent"` for most legal documents.** CellCog handles contracts, policies, and standard legal documents excellently in agent mode.

**Use `"agent team"` for complex legal research** — multi-jurisdiction compliance analysis, regulatory deep-dives, or when the legal reasoning itself is the deliverable.

---

## Tips for Better Legal Documents

1. **Specify jurisdiction**: "A contract" is vague. "A Delaware-governed contract for California-based parties" gives CellCog the legal context it needs.

2. **Name the parties clearly**: Include entity types (LLC, Corp, sole proprietor) and locations.

3. **Define the deal terms**: Payment amounts, timelines, equity splits, deliverables — the more specific, the better.

4. **State what clauses matter**: "Include IP assignment, non-compete, and arbitration" focuses the document.

5. **Indicate formality level**: "Standard startup-friendly language" vs. "formal corporate tone" changes the output significantly.
