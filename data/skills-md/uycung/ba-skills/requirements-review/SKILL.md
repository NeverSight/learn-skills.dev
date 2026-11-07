---
name: requirements-review
description: "Review the quality of requirements documents (stories, FRs, use cases, NFRs, rules, models, PRDs) per BABOK: check they are written correctly (verify) and meet the need (validate), return a findings report with severity and a ready-to-approve verdict; use before asking for approval or handing over to dev/testers, or to plan a review session."
---

# Requirements Review

Framework from BABOK v3: Verify Requirements (7.2), Validate Requirements (7.3), Reviews (10.37), Approve Requirements (5.5). Respond in the user's language. This skill **grades the document, not the people** (10.37.2: reviews target the work product).

## Two different questions
- **Verify**: are the requirements written correctly (clear, complete, consistent, verifiable, using the right notation)? This is a condition for being ready for validation.
- **Validate**: do the requirements really serve the business goal, fall within the solution scope, and bring benefit to stakeholders? Validation can start before verification is finished but **cannot finish before it** (7.3.3).
Always say which question the report is answering. Final quality is decided by the stakeholders (7.2.2): the skill only points out where the risks are.

## Hard rules
1. **Every finding points to the exact sentence/section/code at fault**, names the characteristic violated, why it is a problem, and how to fix it. No vague remarks like "not clear".
2. **Never change business content yourself.** You may propose rewording; where information is missing, turn it into a question with someone to answer it; do not fill in numbers or guess rules.
3. **Distinguish certain defects from suspicions.** Certain defects: self-contradiction within the document, a missing mandatory field, a vague word with no criterion. Suspicions: need confirmation from someone who knows the business; record as "suspicion".
4. **The severity levels are the skill's convention** (not BABOK's): Blocker (cannot be built/tested/approved without a fix), Should fix (causes misunderstanding or rework), Suggestion (improvement). State the criteria for choosing the level.
5. A verdict at the end of the report: **Ready / Conditional / Not ready** for the next step (validate, approve, or handing to the team), with specific conditions.
6. Never claim "the document passes" just because no defects were found: state the scope that was checked (which items, which characteristics) and what could not be checked for lack of information.

## Process
1. **Identify**: the kind of work product (story, use case, NFR, model, whole PRD), the review objective (find defects, check standards, confirm completeness and correctness, consensus, problem solving, education: 10.37.3), the level of formality. Ask at most 3 questions if missing: who uses this document, whether the team has a glossary/standard templates, where the business goal and scope are.
2. **Verify** each item against the 9 quality characteristics and the verify activities (`references/quality-characteristics.md`, `references/verify-validate.md`). Use the checklist that fits the document type (`references/checklists.md`).
3. **Cross-check** between items and models: something mentioned in one place but missing in another, terms used inconsistently, contradictory rules.
4. **Validate** when goals, scope and a description of the future state exist: assumptions, measurable evaluation criteria, scope compatibility (`references/verify-validate.md`). If these inputs are missing, say plainly that validation can only be partial.
5. **Build the report** per `templates/review-report.md`: scope checked, findings table, verdict, tracking items (item tracking), questions needing an answer.
6. When the user has made fixes: **re-check** each earlier finding (resolved / still open / new), do not re-evaluate from scratch.

## Three modes
- **A. Document review** (default): steps 1 to 5.
- **B. Plan a review session**: choose the technique by objective and risk level, roles (author, reviewer, facilitator, scribe), agenda, checklist to send beforehand, how results are recorded (`references/review-techniques.md`).
- **C. Re-check after fixes**: step 6.

## Collaboration with other skills
Missing links or coverage found: hand off to `requirements-trace`. Story/AC to rewrite: `story-writer`. NFR without a measure: `nfr-writer`. A wrong or incomplete model: `requirements-modelling`. Tracking items: short form in `templates/review-report.md`; the full attribute list is in the `requirements-elicitation` skill (item tracking), if installed.

## Reference files
- `references/quality-characteristics.md`: the 9 characteristics, check questions, typical defects, fixes.
- `references/verify-validate.md`: verify activities, validate elements, readiness gate before approval.
- `references/review-techniques.md`: 7 techniques, roles, when to use.
- `references/checklists.md`: checklists by document type.
- `references/iso29148.md`: ISO/IEC/IEEE 29148:2018 checked against the standard itself: 9 characteristics for individual requirements, 5 for the whole set, keywords and word groups to avoid, attributes, 4 verification methods, clause 9 content. Supplements the 9 BABOK characteristics; does not replace them.
- `templates/review-report.md`: report template.
