---
name: legal-strategy
description: Analyze legal and regulatory risk, IP, contracts, privacy, governance, and employment questions as structured issue-spotting for counsel. Do not use this methodology as legal advice or for technical security implementation, CRM, or delivery execution.
license: MIT
metadata:
  tags: legal-strategy, clo, general-counsel, regulatory, ip-strategy, contract-risk,
    data-privacy, corporate-governance, employment-law
  source_repo: https://github.com/magnus919/hermes-profiles
---

# Legal Strategy — CLO/General Counsel Methodology

CLO-level methodology for legal strategy, regulatory compliance, IP management, contract risk, data privacy, corporate governance, and employment law. This skill provides the frameworks and reference material for a chief legal officer or general counsel profile.

## When to Load

| Trigger | What's Needed |
|---------|---------------|
| Regulatory compliance analysis | `references/regulatory-analysis.md` — GDPR, CCPA, AI Act, HIPAA, cross-border transfers |
| IP strategy development | `references/ip-strategy.md` — patents, trademarks, trade secrets, open source licensing |
| Contract risk assessment | `references/contract-risk.md` — indemnification, liability caps, force majeure, DPA |
| Data privacy framework design | `references/data-privacy.md` — privacy-by-design, DPIAs, data mapping, breach response |
| Corporate governance counsel | `references/regulatory-analysis.md` — board duties, fiduciary obligations |
| Employment law consideration | `references/ip-strategy.md` — IP assignment, classification, non-competes |

## Loading Order

```text
skill_view('legal-strategy')
# Then domain-specific references:
skill_view('legal-strategy', file_path='references/regulatory-analysis.md')
skill_view('legal-strategy', file_path='references/ip-strategy.md')
skill_view('legal-strategy', file_path='references/contract-risk.md')
skill_view('legal-strategy', file_path='references/data-privacy.md')
```

## Reference Files

| Reference | Purpose |
|-----------|---------|
| `references/regulatory-analysis.md` | GDPR, CCPA, AI Act risk categories, sector-specific (HIPAA, SOX, GLBA, PCI DSS), children's privacy, cross-border data transfers |
| `references/ip-strategy.md` | Patent types and process, trademark clearance and registration, trade secret management, open source licensing (permissive/copyleft), IP portfolio management |
| `references/contract-risk.md` | Indemnification clauses, liability cap tiers, force majeure (post-COVID), limitation of liability, data protection addenda, contract lifecycle management, risk scoring |
| `references/data-privacy.md` | Privacy-by-design (7 principles), DPIA process, data mapping/RoPA, breach response checklist, vendor privacy assessment |
| `references/decision-workflow.md` | Jurisdictional risk triage, counsel escalation, worked example, reusable memo, and owner routing matrix |

## Output Contract

The profile using this skill produces artifact pyramids. The response to any caller is the absolute path to `00-index.md`. See `artifact-pyramids` skill for the specification.

## Safety and Escalation

This methodology supports issue spotting and questions for counsel; it is not legal advice. Do not present a jurisdiction-specific conclusion as settled law. Escalate interpretation, filings, disputes, regulated activity, employment actions, cross-border transfers, and other high-impact or novel matters to licensed counsel, and record counsel's disposition in the durable artifact.

## When not to use

- Do not use for legal advice, filings, or jurisdiction-specific conclusions; escalate to licensed counsel.
- Do not use for technical security implementation; route to `security-audit-methodology`.

## Related Skills

- `artifact-pyramids` — output contract
- `security-audit-methodology` — technical security posture (complementary to privacy/regulatory)
- `opensource-contributions` — open source contribution compliance and CLAs
