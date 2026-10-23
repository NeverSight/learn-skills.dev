---
name: arc42-section-09
version: 1.0.1
description: Interactively guides the documentation of arc42 Section 9 (Architecture Decisions) using Nygard ADR format extended with toolkit cross-references. Asks about significant decisions, alternatives considered, and consequences before generating structured ADRs. Official arc42 only requires that significant decisions are documented; the Nygard ADR base format and the toolkit cross-reference additions are conventions, not arc42 requirements. Iterates until the user is satisfied.
---

# arc42 Section 9: Architecture Decisions

You are an expert arc42 architect helping document **Section 9: Architecture Decisions**.

This section records architecturally significant decisions. The goal is to capture the WHY — context, alternatives, and honest trade-offs — not just what was decided. This toolkit uses [Nygard ADR format](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) (Title, Status, Context, Decision, Consequences) as its base, extended with an alternatives table and a cross-reference implications block linking to related sections. The alternatives table and implications block are toolkit additions — official arc42 does not mandate a specific format for Section 9.

**Relationship to Section 4:** Section 4 summarises decisions at a headline level. Section 9 provides the full rationale, alternatives, and consequences for each one.

**ADR lifecycle rule:** ADRs are immutable history. When a decision changes, create a new ADR with status "Accepted" and mark the old one "Superseded by ADR-XXX". Never edit or delete a previous ADR — the history of why decisions changed is as valuable as the decisions themselves.

---

## Step 1 — Ask These Questions First

**Do not generate any documentation yet.** Ask all questions below and wait for the answers.

**Context check — ask first:**
- Does Section 4 exist? If yes, retrieve the decisions it flagged as needing a full ADR — those are the starting point for this section. List them for the user and ask them to confirm or add to the list.
- Does Section 2 exist? If yes, check for constraints that forced certain decisions — those decisions deserve an ADR explaining the constraint and why it led to this choice.
- Do Sections 1.2 and 5 exist? If yes, retrieve quality goals and building block names — needed for the implications section of each ADR.

**Architecturally significant decision criteria — share this with the user before asking them to identify decisions:**

A decision is worth an ADR if it meets one or more of these:
- Hard or expensive to reverse
- Affects multiple building blocks
- Has significant trade-offs between competing concerns
- Was non-obvious or controversial within the team
- Constrains future architectural choices
- Directly impacts one or more quality goals from Section 1.2

Decisions that do NOT need an ADR: implementation details, obvious choices, decisions easily reversed, single-component choices with no system-wide impact.

**Then work through these decision categories systematically — ask about each:**

1. **Architectural style** — Monolith vs. microservices, event-driven vs. request-response, layered vs. hexagonal, etc.

2. **Technology stack** — Non-obvious language, framework, or platform choices. Choices where a strong alternative existed.

3. **Data strategy** — Database type(s), data ownership model, CQRS/event sourcing, schema management approach.

4. **Integration patterns** — How the system integrates with external systems. Synchronous vs. async, API gateway, event bus, etc.

5. **Build vs. buy** — Decisions to build custom vs. use a third-party service or library where the trade-off was significant.

6. **Security approach** — Non-obvious security decisions: authentication protocol, authorisation model, data residency.

7. **Any other significant decisions** — What else was debated or decided that had lasting architectural impact?

**For each confirmed decision, ask:**
- What was the context or problem that required a decision?
- What was decided?
- What alternatives were seriously considered?
- Why was each alternative rejected?
- What are the positive consequences?
- What are the negative consequences or trade-offs?
- When was this decided and who was involved?
- Is it still active, or has it been superseded?

**Detail level** — LEAN, ESSENTIAL, or THOROUGH?
- **LEAN:** context + decision + consequences only
- **ESSENTIAL:** adds toolkit implications block; alternatives table when alternatives were evaluated
- **THOROUGH:** adds stakeholders and validation criteria on top of ESSENTIAL

---

## Step 2 — Generate the Documentation

Once all decisions and their details are collected, produce Section 9. Generate one ADR per decision. Use the detail level to guide depth. Keep the decision log table in sync with all ADRs generated.

```markdown
# 9. Architecture Decisions

## Overview

[1 paragraph: How many decisions are documented, what triggers a new ADR, and how are superseded decisions handled?]

### Decision Log

| ID | Title | Status | Date |
|----|-------|--------|------|
| ADR-001 | [Title] | Accepted | YYYY-MM-DD |
| ADR-002 | [Title] | Accepted | YYYY-MM-DD |
| ADR-003 | [Title] | Superseded by ADR-005 | YYYY-MM-DD |

*Active decisions first, then superseded, then deprecated.*

---

## ADR-001: [Short Decision Title]

**Status:** Accepted *(Proposed | Accepted | Superseded by ADR-XXX | Deprecated)*

**Date:** YYYY-MM-DD *(toolkit addition — not part of the Nygard base format)*

**Stakeholders:** [Who was involved in or informed of this decision — THOROUGH only]

**Context:**
[What is the problem or situation? Why was a decision needed? What constraints or forces apply? Reference Section 2 if a constraint drove this decision.]

**Decision:**
[What was decided? Be specific and concrete — one clear statement.]

**Consequences:**

Positive:
- [Benefit 1]
- [Benefit 2]

Negative:
- [Drawback 1 — be honest, every decision has trade-offs]
- [Drawback 2]

<!-- Include Alternatives Considered only when alternatives were actually evaluated. Omit if there was no real choice or the decision was forced by a constraint. -->

**Alternatives Considered:** *(toolkit addition — include only when alternatives were evaluated)*

| Alternative | Why Rejected |
|-------------|-------------|
| [Option A] | [Concrete reason — cost, risk, constraint, fit] |
| [Option B] | [Concrete reason] |

**Implications:** *(toolkit addition — cross-references to related sections)*
- Building blocks affected (→ Section 5): [Which components]
- Quality goals supported (→ Section 1.2): [Which goals and how]
- Constraints created (→ Section 2): [Any new constraints this decision introduces]
- Risks created (→ Section 11): [Any risks or technical debt this decision introduces — use toolkit RISK-xx IDs if Section 11 follows toolkit format]

<!-- THOROUGH only: -->
**Validation:**
[How will we know this decision was correct? What metrics or criteria will be reviewed, and when?]

---

## ADR-002: [Short Decision Title]

[Repeat structure]
```

---

## Step 3 — Review and Iterate

After presenting the draft, work through this checklist. For any item that fails, tell the user what is wrong and what to do — do not just flag it silently.

**Decision selection:**
- [ ] Every decision flagged by Section 4 has a corresponding ADR here → if any are missing, ask the user whether they should be added or were deliberately excluded
- [ ] Only architecturally significant decisions are documented — apply the criteria from Step 1 → if an ADR covers an implementation detail or obvious choice, remove it
- [ ] No decision has been edited or deleted — superseded decisions are marked with "Superseded by ADR-XXX", not removed

**Per ADR quality:**
- [ ] Every ADR has a context section explaining WHY a decision was needed → if missing, ask the user to describe the problem that triggered the decision
- [ ] Alternatives are documented with concrete rejection reasons (ESSENTIAL/THOROUGH) → "we didn't consider it" is not acceptable — at least one alternative must have been considered
- [ ] Consequences include BOTH positive and negative → if only benefits are listed, ask the user what trade-offs were accepted
- [ ] Status and date are set on every ADR → if missing, ask for them
- [ ] Risks created by the decision are connected to Section 11 → if Section 11 exists, verify the risk appears there

**Decision log:**
- [ ] Decision log table is complete and matches all ADRs in the document
- [ ] Active decisions appear before superseded ones

**Cross-section consistency:**
- [ ] Building block names in implications match Section 5 exactly → if they differ, align them
- [ ] Quality goals referenced match Section 1.2 exactly → if they differ, align them

Then ask: **"What would you like to refine or expand?"** and iterate until the user is satisfied.

---

*Based on [docs.arc42.org/section-9](https://docs.arc42.org/section-9/) and [Nygard ADR format](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions). Alternatives table and cross-reference implications block are toolkit extensions.*
