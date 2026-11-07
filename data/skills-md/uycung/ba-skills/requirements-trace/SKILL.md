---
name: requirements-trace
description: "Build a traceability matrix and review coverage between goals, FRs, user stories, acceptance criteria, NFRs and tests; use when a BA needs to check a spec for gaps, analyze the impact of a requirement change, or prepare before sign-off/approval."
---

# Requirements Trace

Goal: link requirements to one another so you can see **what is not covered** and **what is affected if this changes**. Respond in the user's language. Works together with the `story-writer` skill (writes FRs/stories/AC) and `nfr-writer` (writes NFRs).

## Principles
1. **Link only when the link has value.** Traceability effort grows sharply with the number of requirements and the level of formality (BABOK 5.1.4.1). Ask the user which level they need: light (goal ↔ story ↔ AC), medium (add NFRs and business rules), full (add design and tests).
2. **Never invent links.** Record only links that have a basis in the documents the user supplied; inferred links are marked "proposed, needs confirmation".
3. **Every item has a stable code** that does not change when the content is edited. Default convention: `GOAL-xx`, `FR-xx`, `US-xx` (or an epic-based code such as `ORD-12`), `AC-xx.y`, `BR-xx` (business rule), `NFR-<characteristic>-xx`, `TC-xx`. If the team already has a convention, use it.
4. Use the correct relationship types (see `references/relationships.md`).

## Process
1. Collect the input documents (PRD, story list, NFR table...). If codes are missing, assign proposed codes and say so.
2. Choose the traceability level with the user (light/medium/full).
3. Build the catalogue of items and links using `templates/trace-matrix.md`.
4. Run the coverage checks (`references/coverage-checks.md`) and list the gaps by severity.
5. If the user states a change, do an impact analysis: which items are affected directly/indirectly, what must be edited, who needs to re-approve.
6. End with: **Gaps**, **Contradictions**, **To confirm**, and the proposed next step.

## A limit to state plainly
Traceability shows that each requirement links back to a goal; it does **not** show that the set of requirements is coherent (BABOK 7.4.2). If the user needs that checked, use viewpoints/views and the 5 link criteria.

## Attributes each requirement should have
Source (who/which document asked for it), priority, complexity, status (including approved: by whom, when), version. Attributes can change even when the requirement does not (BABOK 5.2.4.2).
ISO/IEC/IEEE 29148:2018, 5.2.8 (the standard itself was read) lists example attributes: a unique identifier (never changed and never reused even if the requirement is deleted), version, owner, stakeholder priority (scale 1 to 5 or High/Medium/Low), risk, rationale, difficulty, type. The standard does not list status, source or traceability links among those examples. Clause 6.5.2.2 recommends attaching the **verification method** when the requirement is created, with four values: inspection, analysis, demonstration, test; more on 29148 in the `requirements-review` skill, if installed. The rule "identifier never changed, never reused" should be applied to the IDs in the matrix.

## Reference files
- `references/relationships.md`: relationship types and how to record them.
- `references/coverage-checks.md`: coverage checks, impact analysis.
- `references/architecture-approval-review.md`: requirements architecture, link quality, change assessment, approval, review (BABOK 7.4, 5.4, 5.5, 10.37).
- `templates/trace-matrix.md`: matrix template and gap report.
