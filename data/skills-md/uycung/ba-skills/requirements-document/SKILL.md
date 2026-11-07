---
name: requirements-document
description: "Assemble the outputs of the BA skill suite (stories, NFRs, rules, models, traceability, stakeholders, business case) into a complete BRD, PRD or SRS suited to the reader, with consistency checks and a list of what is missing; use when a requirements package is needed for approval, handover to dev or contract signing."
---

# Requirements Document (BRD / PRD / SRS)

Goal: a document that reads as a continuous whole, where **every section comes from existing outputs**, and gaps show up clearly instead of being papered over with words. Respond in the user's language.

## Sources and limits (state plainly when relevant)
- **From BABOK v3**: a requirements package is a form of business analysis package that focuses on requirements and can be the baseline of a set of requirements (a term); "requirements document" in the glossary points back to requirements package. Choose the form by reader: who reads it, what each group needs and understands, preferred style, key information, whether the format fits, which activity it supports, regulatory or contractual constraints (4.4). Forms include formal documents on the organization's template, informal documents, presentations (4.4). Requirements classification: business, stakeholder, solution (functional, non-functional), transition (2.3, Requirements Classification Schema). Requirements architecture and viewpoints (7.4).
- **NOT from BABOK**: the specific names and structure of BRD, PRD, SRS. These are industry conventions; BABOK does not prescribe them. The standard ISO/IEC/IEEE 29148:2018 **has been read** (clauses 5.2, 6.5.2.2 and 9.2 to 9.6; the copy supplied by the user). The standard prescribes the **content** of the BRS/StRS/SyRS/SRS, not the order of sections; the section frame in `templates/` remains the skill's own frame based on BABOK, not a standard frame. `references/iso29148-content.md` compares the standard's content against the skill's frame for use when a contract or organization requires conformance with 29148. If the organization or contract has a mandatory template, use that and map the content into it.
- The skill does not write new requirements. To write or edit requirements: `story-writer`, `nfr-writer`, `requirements-modelling`.

## Hard rules
1. **Assemble only, never compose.** Every requirement in the document has an ID and points to its source (story, AC, BR, NFR, model). No source: do not include it; record it under "What is still missing".
2. **Choose the document type by the reader and the decision to be made** (4.4), not by habit. Ask at most 3 questions: who reads it, to decide/do what, whether a mandatory template exists.
3. **Empty sections show clearly**: keep the heading, write "Not yet available", state what is needed, from whom, which skill produces it. Do not write words to fill space.
4. **One source of truth for each piece of information.** Do not copy back and forth between sections; refer by ID. Two places that say the same thing must match word for word, or one must point to the other.
5. **Keep IDs stable** across versions; record change history and the baseline version when the user asks to freeze (see `references/assembly-checks.md`).
6. **Classify requirements clearly**: business, stakeholder, solution functional, solution non-functional, transition (conversion data, training, ongoing operation: as BABOK names them).
7. **Do not hide assumptions, constraints, dependencies, risks, open questions**; each has its own section.
8. **An unapproved document is stamped as unapproved**; include the readiness gate so that `requirements-review` checks before approval is sought.

## Process
1. **Collect the inputs**: list the products that exist (goals and business case, stakeholders, stories/FRs/use cases, BR, NFRs, models, traceability matrix, open questions). If the user only provides raw material (meeting notes, ideas), stop and go to `requirements-elicitation`/`story-writer` first.
2. **Choose the document type and depth** per `references/document-types.md`.
3. **Build the source → section map**: which product each section comes from; which sections have no source yet.
4. **Assemble** using the template in `templates/` (BRD, PRD or SRS). Keep the wording of requirements from the source; add only connecting sentences.
5. **Check consistency** (`references/assembly-checks.md`): IDs, terms, figures, scope, priority, status, traceability relationships.
6. **Report "What is still missing" and "Ready for approval?"**: suggest running `requirements-review` before asking for approval (BABOK 5.5: the input is verified requirements).
7. **Return**: the document + the list of gaps + assumptions + open questions. Do not summarize again what the document already says.

## Collaboration
Goals, current/future state, business case: `business-case-strategy`. Stakeholder list and RACI: `requirements-stakeholders`. Stories/AC: `story-writer`. NFRs: `nfr-writer`. Models: `requirements-modelling`. Traceability matrix, change impact: `requirements-trace`. Tests/UAT: `requirements-testcases`. Review before approval: `requirements-review`.

## Reference files
- `references/document-types.md`: who BRD/PRD/SRS are for, section → source skill map, a light version for agile.
- `references/assembly-checks.md`: consistency, status, version, approval checks.
- `references/iso29148-content.md`: content of the BRS (9.3), StRS (9.4), SyRS (9.5) and SRS (9.6) per ISO/IEC/IEEE 29148:2018, mapped into the skill's frame, and which items are missing.
- `templates/brd-template.md`, `templates/prd-template.md`, `templates/srs-template.md`.
