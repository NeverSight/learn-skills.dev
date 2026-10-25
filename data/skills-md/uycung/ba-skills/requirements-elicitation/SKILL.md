---
name: requirements-elicitation
description: "Plan requirements elicitation, draft interview/workshop question sets, and turn meeting notes into sourced, unconfirmed elicitation results with a list of items to confirm; use before writing stories/FRs or after each stakeholder meeting."
---

# Requirements Elicitation

Framework from BABOK v3 chapter 4 (Prepare, Conduct, Confirm) and the Interviews and Item Tracking techniques. Respond in the user's language. The output of this skill is the input for `story-writer`, `nfr-writer` and `requirements-trace`.

## Principles
1. **Record exactly what was said, separate from what is inferred.** Every piece of information has a label: [Stated] (quoted/recorded from the source), [Inferred] (drawn by the skill), [Assumption]. Never turn an inference into a fact.
2. **Elicitation results stay "unconfirmed" until confirmed** with the source or cross-checked (BABOK 4.2.8, 4.3).
3. **Do not ask leading questions.** BABOK names the risk of unintentionally leading the interviewee (10.25.4.2). Prefer open questions, and ask for concrete examples and the real process.
4. **Every contradiction and open point is recorded and given an owner**; do not pick the right side yourself.
5. Keep confidentiality when the user asks to anonymize the source.

## Three modes
### A. Planning (Prepare)
From the objective and context the user gives, create an **Elicitation activity plan** (`templates/elicitation-plan.md`): session objective, scope (information needed, what is out of scope), participants and roles, chosen technique (with reasons), logistics, pre-reading, risks. Choose techniques using `references/techniques.md`.
### B. Drafting questions
Create an **interview/workshop guide**: opening, question groups by topic (with probing questions), closing. Allow marking which questions can be dropped if time runs short (BABOK 10.25.3). For a workshop: add the agenda, roles (facilitator, scribe, timekeeper), ground rules and defined outputs (10.50). For a survey: objective, sample, response threshold, pilot (10.45). Details in `references/workshops-surveys.md`.
### C. Processing notes (Conduct → Confirm)
Take notes/transcripts. Return:
1. **Elicitation results (unconfirmed)**: a table of item | type (need, rule, constraint, issue, assumption, open question) | content | label [Stated]/[Inferred] | source (who, when).
2. **Contradictions and gaps** compared with earlier notes/documents (if any).
3. **List to confirm**: which item, ask whom, ask what. Draft a short follow-up message/email ready to send to participants (BABOK stresses confirming early after the meeting).
4. **Tracking items (Item Tracking)** for issues/assumptions/dependencies: see `references/item-tracking.md`.
5. **New or differently-used terms** that appeared in the session (BABOK 10.23), to add to the glossary.
6. **Requirement candidates**: items that could become a story/FR/NFR/BR, not yet fully written; hand off to the corresponding skill.

## Reference files
- `references/techniques.md`: choosing techniques, the three styles of elicitation.
- `references/item-tracking.md`: tracking item attributes.
- `references/workshops-surveys.md`: workshops, surveys, collaborative games, glossary, interfaces, confirmation/communication.
- `templates/elicitation-plan.md`: plan and interview guide template.
