---
name: adr
description: Record, edit, or review an Architecture Decision Record, or investigate a consequential rationale gap that code and maintained documentation will not preserve.
---

# ADR

Preserve why a consequential direction exists. The useful result is a minimal durable record or a reasoned conclusion that another document—or no document—is better.

## Route the request

- **Explicit creation:** qualify the gap. When an ADR is warranted, reconcile conventions, write, then compress and verify without a second creation gate; otherwise return the classification.
- **Detected gap:** qualify it, recommend the right artifact, and stop until the user opts in.
- **Existing ADR edit:** inspect the record and its history, then preserve decision history, compress, and verify. A semantic replacement returns through explicit creation for the new ADR.
- **Existing ADR review:** inspect the record and its history, apply the qualification, history, compression, and verification checks read-only, then report findings.
- **Another document or no document:** return the classification and stop after qualification.

## 1. Qualify the rationale gap

Inspect relevant code, documentation, existing ADRs, project language, and history before asking for discoverable facts. State what the project does, what evidence supports it, which rationale remains unknown, and why that missing why matters to future change or risk.

Apply the **after-implementation test**: could a new contributor understand the rationale from the completed code and maintained documentation? An ADR is warranted when the answer remains no and the content is a consequential decision rather than an implementation plan, domain explanation, operating guide, or specification.

Treat observed facts, supported inferences, hypotheses, and unknowns distinctly. Ask the fewest material questions, one at a time when answers determine the next branch.

For a gap detected during other work, finish the active work and make the recommendation with the concrete missing why.

Completion criterion: the gap is classified as ADR, another document type, or no new document, with uncertainty stated honestly.

## 2. Reconcile conventions

Inspect the repository's ADR location, naming, template, language, status vocabulary, and history. Follow a sound existing convention. Bring a materially weaker convention or structural migration to the user as a separate decision.

When no convention exists, use:

- `docs/adrs/`;
- a monotonic four-digit identifier and decision-focused title;
- `ADR-0007: Use transactional outbox` as title form;
- creation date in `YYYY-MM-DD`;
- `Proposed`, `Accepted`, or `Superseded` as status.

Completion criterion: destination, next unused identity, language, status, and document shape are known before writing.

## 3. Write the minimum sufficient record

Start from [`templates/adr.md`](templates/adr.md) when the project has no stronger template. Keep the required record to title, creation date, status, context, and decision with rationale.

- **Context:** include only forces, constraints, domain terms, and uncertainty needed to understand the choice.
- **Decision:** state what was chosen and why in one coherent explanation.
- **Consequences:** add only material costs, risks, responsibilities, benefits, or lost flexibility.
- **Alternatives considered:** add only genuine alternatives needed to understand the choice.
- **References:** use versioned durable sources as supplemental evidence; keep the central why in the ADR.

Keep realization details—classes, schemas, commands, configuration, code paths, and implementation steps—in implementation artifacts. State incomplete history as uncertainty rather than reconstructing intent.

Completion criterion: a new contributor can understand the choice and its rationale without receiving an implementation plan or following a link for the central explanation.

## 4. Preserve decision history

Apply editorial corrections directly when meaning remains stable. A changed decision, rationale, or material consequence normally becomes a new ADR that supersedes the old one; link both records reciprocally and retain their identities.

When a direct semantic edit has a justified benefit, explain the history cost and obtain an explicit human choice before applying it. Preserve past uncertainty and rationale as they were understood at the time.

Completion criterion: editorial changes preserve meaning, and semantic changes have an explicit history disposition with resolving supersession links when used.

## 5. Compress and verify

For every passage ask: if it disappears, is the why harder to understand? During creation or editing, remove passages that fail. During review, report them without changing the record. Then confirm a new contributor can understand the rationale without reconstructing it elsewhere.

Verify identity, date, status, location, uncertainty labels, durable references, reciprocal supersession, and any final diff. Report the reviewed or changed path, captured decision, remaining uncertainty, findings, and related status changes.

Completion criterion: creation or editing leaves only passages that contribute to the why; review reports every passage that does not; and every reviewed or changed artifact is accounted for.
