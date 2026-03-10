---
name: dpia-sentinel-oliver-schmidt-prietz
description: |
  GDPR Data Protection Impact Assessment (DPIA) guidance under Article 35 GDPR, EDPB Guidelines WP 248 rev.01, EDPB Opinion 28/2024 (AI), and national SA blacklists/whitelists. Triggers: "DPIA", "DSFA", "Datenschutz-Folgenabschätzung", "impact assessment", "Art. 35", "do I need a DPIA", descriptions of new high-risk processing (profiling, AI, biometrics, large-scale monitoring, special category data), Art. 36 prior consultation questions, national blacklist/whitelist queries.
metadata:
  author: Oliver Schmidt-Prietz
  license: AGPL-3.0
  version: 2026.02.10
---

# DPIA Sentinel

## Disclaimer (show at session start)

> **Important:** This provides structured GDPR Article 35 guidance based on EDPB Guidelines and national SA requirements. It is not legal advice. Involve your DPO (Art. 35(2)) and qualified counsel for final decisions.

## Routing

Determine what the user needs and load references accordingly:

| User Need | Load These References | Action |
|-----------|----------------------|--------|
| "Do I need a DPIA?" / threshold question | `references/edpb-criteria.md` + relevant jurisdiction file(s) | Run threshold assessment |
| Full DPIA | `edpb-criteria.md` + jurisdiction(s) + `references/risk-catalog.md` + `scoring.md` | Walk through assessment phases |
| Document generation (.docx) | `references/templates.md` + docx generation skill (`/mnt/skills/public/docx/SKILL.md` in Claude.ai Projects, or `docx-processing-anthropic` skill in Claude Code; if unavailable, generate well-formatted Markdown as fallback) | Generate Word document |
| Specific legal question | Load relevant reference only | Answer directly |

**Jurisdiction selection:** Ask two questions: (1) Where is the controller's main establishment? (2) Where are the data subjects located? Load **all** jurisdiction files that are relevant — this may be multiple files for multi-jurisdictional processing. See `references/edpb-criteria.md` → "Multi-Jurisdictional DPIA Analysis" for the full decision framework.

Available jurisdiction files:
- `references/jurisdictions/de-dsk.md` — Germany
- `references/jurisdictions/fr-cnil.md` — France
- `references/jurisdictions/ie-dpc.md` — Ireland
- `references/jurisdictions/be-apd.md` — Belgium
- `references/jurisdictions/nl-ap.md` — Netherlands
- `references/jurisdictions/it-garante.md` — Italy
- `references/jurisdictions/pl-uodo.md` — Poland
- `references/jurisdictions/whitelists.md` — France, Czech Republic, Spain, Austria

For jurisdictions not covered by a dedicated file, rely on the EDPB nine-criteria analysis in `references/edpb-criteria.md` and note that the user should check their national SA's Art. 35(4) list directly.

## Assessment Flow

**Threshold → Description → Necessity/Proportionality → Risks → Mitigations → Residual Risk → Art. 36 Check → Documentation**

This is the logical sequence, not a rigid script. Adapt to the user: if they provide rich context upfront, skip intake questions. If they're experienced, move faster. If they're new to DPIAs, explain more.

The assessment is **iterative**: if mitigations in later stages change the processing design, revisit earlier analysis and flag this to the user.

## Legal Precision Points

These are areas where Claude's training knowledge may be imprecise. Always apply these rules:

1. **Art. 35(3) triggers are absolute.** If any of the three mandatory cases apply (systematic extensive automated evaluation with legal/significant effect; large-scale special category/criminal data; systematic monitoring of publicly accessible areas on large scale), a DPIA is required — no balancing, no judgment call.

2. **The two-criteria rule is a presumption, not a mandate.** Meeting 2+ of the 9 EDPB criteria creates a strong presumption a DPIA is needed. But a DPIA *may* be needed with only 1 criterion, and *may* be justified as unnecessary with 2 — if thoroughly documented. See WP 248 rev.01, p. 11.

3. **Art. 9 is cumulative with Art. 6.** Special category data always needs BOTH a legal basis under Art. 6 AND an exception under Art. 9(2). These are separate legal hurdles.

4. **"Large scale" has no fixed number.** The EDPB uses four factors: number of subjects, data volume, duration, geographic extent. An individual doctor is not large scale; a regional hospital is. Never cite a specific numerical threshold.

5. **National blacklists are additive, not exhaustive.** Processing not on a blacklist may still require a DPIA. A blacklist entry in the relevant jurisdiction overrides whitelist exemptions from other jurisdictions.

6. **Multi-jurisdictional processing requires checking ALL relevant blacklists.** Art. 35(4) lists are territorial — the DPIA obligation is triggered if the processing matches a blacklist in ANY jurisdiction where the controller is established OR where data subjects are located. The one-stop-shop mechanism (Art. 56) governs enforcement jurisdiction, but it does NOT limit which Art. 35(4) lists apply to the DPIA obligation itself. A single DPIA can address multiple jurisdictions, but the threshold analysis must run against each applicable national list. See `references/edpb-criteria.md` → "Multi-Jurisdictional DPIA Analysis" for details.

7. **DPIA must happen before processing begins** (Art. 35(1)). It is a pre-processing obligation, not a retroactive compliance exercise. If processing has already started, the DPIA should still be done but note this as a compliance gap.

8. **AI requires dual-phase analysis** (EDPB Opinion 28/2024). Training and deployment are separate processing activities with distinct risk profiles. A deployer cannot simply rely on the model provider's DPIA.

9. **Art. 36 prior consultation is sequential to the DPIA, not part of it.** The DPIA identifies residual risk; if that risk remains high after all feasible mitigations, Art. 36 requires consulting the SA before processing begins. The SA has 8 weeks (extendable by 6).

10. **Pseudonymization as risk reducer** (EDPB Guidelines 01/2025 on Pseudonymisation, adopted 17 January 2025): Effective pseudonymization with technically separated additional information can meaningfully reduce likelihood scores in risk assessment. But it must be genuine — if re-identification is trivial, it doesn't reduce risk.

11. **Risk assessment is from the data subject's perspective.** A DPIA assesses risks to rights and freedoms of natural persons (Recital 75), not corporate/business risks. Identity theft risk to the individual, not reputational risk to the company.

12. **AI Act FRIA is distinct from DPIA.** For high-risk AI systems under the AI Act, a Fundamental Rights Impact Assessment (FRIA) may also be required. DPIA (data protection risks) and FRIA (broader fundamental rights) are complementary — one does not replace the other.

## Output Formats

**Threshold result:** Present a clear verdict (DPIA Required / Recommended / Not Required) with the reasoning showing Art. 35(3) check, criteria analysis, and national list check.

**Risk register:** Table with Risk ID, Description, Rights Category, Likelihood (1-5), Severity (1-5), Score, Level. Use the scoring methodology in `references/scoring.md`.

**Residual risk overview:** Summary showing total risks by level before and after mitigation, plus overall position (Acceptable / Acceptable with Conditions / Art. 36 Consultation Required).

**Documents:** Generate .docx files following `references/templates.md`. Always read the docx skill first.
